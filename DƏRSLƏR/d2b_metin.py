#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-2B — ADDIM 22–26 mətnləri.

Hər addım 4 hissədən ibarətdir:
  A      — «niyə» (geniş nəzəri izah)
  B      — kod (fayllar BACKEND qovluğundan canlı oxunur)
  C      — yoxlama əmrləri
  D      — həqiqi çıxış (qurucu tərəfindən icra olunur)
Əlavə: «Yeni anlayışlar», «Kodun sətir-sətir izahı», «Tez-tez verilən suallar».
"""

ADIMLAR = []


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 22 — STATİSTİKA
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 22,
    "ad": "Statistika — groupBy, aggregate və baza funksiyaları",
    "a": """
<p>2A-da yazdığımız API sadəcə <em>sətirləri</em> verir. Amma rəhbərlik
«14 əməkdaşın siyahısını göstər» demir — o deyir:
<strong>«hansı mərkəzdə neçə əməkdaş var və orta maaş nə qədərdir?»</strong>.
Bu, tamam başqa tip sorğudur: <em>aqreqasiya</em>.</p>

<h4>Ən pis həll — JavaScript-də saymaq</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const hamisi = await prisma.emekdaslar.findMany();   // 14 sətir
const saylar = {};
for (const e of hamisi) {
  saylar[e.merkez_id] = (saylar[e.merkez_id] ?? 0) + 1;
}</pre>
<p>14 sətirdə işləyir. 100 000 sətirdə isə:</p>
<ul>
  <li>Bütün sətirlər bazadan <strong>şəbəkə ilə</strong> gəlir
      (yüzlərlə meqabayt).</li>
  <li>Server onları yaddaşda saxlayır (yaddaş tükənə bilər).</li>
  <li>Baza <em>artıq</em> bunu bacarır — biz sadəcə işi yanlış yerə
      köçürmüşük.</li>
</ul>
<p><strong>Qayda:</strong> aqreqasiyanı <em>bazada</em> et. Baza bunun
üçün optimallaşdırılıb (indekslər, paralellik, yaddaş idarəsi).</p>

<h4>Prisma-nın cavabı: <code>groupBy</code> və <code>aggregate</code></h4>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Metod</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Nə edir</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">SQL qarşılığı</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>count()</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Sətir sayı</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>SELECT count(*)</code></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>aggregate()</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Bütün cədvəl üzrə cəm,
        orta, min, maks</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>SELECT sum(...), avg(...)</code></td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>groupBy()</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Qruplar üzrə aqreqat</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>SELECT ... GROUP BY ...</code></td>
  </tr>
</table>

<p><code>groupBy</code>-nin nəticəsi belə görünür:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
[
  { merkez_id: 1, _count: { _all: 2 }, _avg: { maas: Decimal }, _sum: {...} },
  { merkez_id: 2, _count: { _all: 2 }, _avg: { maas: Decimal }, _sum: {...} },
  ...
]</pre>
<p>Diqqət yetirin: <strong>ad yoxdur</strong> — yalnız
<code>merkez_id</code>. Səbəb: SQL <code>GROUP BY</code> yalnız
qruplaşdırılan sütunları və aqreqatları qaytarır. Adı göstərmək üçün
<em>ikinci</em> sorğu göndərib nəticələri yaddaşda birləşdiririk
(<code>Map</code> ilə). Bu, iki sorğudur — <strong>N+1 deyil</strong>,
çünki sorğu sayı mərkəz sayından asılı deyil.</p>

<h4>⚠️ <code>Decimal</code> → <code>number</code> çevrilməsi</h4>
<p><code>_sum</code> və <code>_avg</code> nəticələri
<code>Prisma.Decimal</code> obyektidir. Onları birbaşa JSON-a qoysaq,
Prisma <em>mətn</em> kimi göndərir (<code>"33000"</code>). Statistika
üçün isə ədəd lazımdır — frontend qrafik çəkməlidir, toplama
aparmalıdır.</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
function eded(d: Prisma.Decimal | number | null | undefined): number {
  if (d === null || d === undefined) return 0;
  const n = Number(d);
  return Number.isFinite(n) ? Math.round(n * 100) / 100 : 0;
}</pre>
<p>⚠️ <code>Number.isFinite</code> yoxlaması vacibdir: <code>NaN</code>
gələrsə (məsələn bütün maaşlar <code>null</code>-dırsa), JSON-da
<code>NaN</code> <em>qeyri-qanuni</em> dəyərdir və frontend onu
oxuya bilməz. Ona görə 0 qaytarırıq.</p>

<h4>Bazada ARTIQ YAZILMIŞ funksiyalar</h4>
<p>Baza dərslərində (Baza-1, Baza-2) PostgreSQL-də PL/pgSQL funksiyaları
yazmışdıq. Onlar <em>indi də oradadır</em>:</p>
<table style="width:100%;border-collapse:collapse;font-size:.88rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Funksiya</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Nə qaytarır</th>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>kadrlar.fn_maas_fondu()</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Aktiv əməkdaşların maaş cəmi</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>tehsil.fn_sertifikasiya_ortalamasi()</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Keçən sertifikatların orta balı</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>struktur.fn_shobe_sayi(merkez_id)</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Mərkəzdəki şöbə sayı</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>kadrlar.fn_emekdas_tam_adi(id)</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">«Soyad Ad Ata adı» mətni</td>
  </tr>
</table>
<p><strong>Niyə onları işlədirik?</strong> Çünki həmin məntiq artıq
SQL-də var və <em>başqa hesabatlarda da</em> istifadə olunur. Eyni
məntiqi iki yerdə yazsaq (bir dəfə SQL-də, bir dəfə TypeScript-də),
onlar vaxt keçdikcə <strong>uyğunsuz olacaq</strong>: biri düzəldiləcək,
digəri yox. Buna <em>ikili həqiqət</em> (dual source of truth) deyilir
və o, məlumat səhvlərinin klassik mənbəyidir.</p>

<h4>Prisma-dan SQL funksiyasını çağırmaq: <code>$queryRaw</code></h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const netice = await this.prisma.$queryRaw&lt;{ cem: Prisma.Decimal }[]&gt;`
  SELECT kadrlar.fn_maas_fondu() AS cem`;</pre>
<p>⚠️ <strong>Niyə şablon sətri (template literal) və niyə adi sətir
birləşdirmə deyil?</strong> Çünki Prisma şablon sətrindəki
<code>${...}</code> ifadələrini <em>avtomatik parametrləşdirir</em> —
yəni SQL-in içinə birbaşa yeridilmir, ayrıca parametr kimi göndərilir.
Bu, <strong>SQL inyeksiyasının qarşısını alır</strong>:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
// ⚠️ BELƏ ETMƏK OLMAZ — SQL İNYEKSİYASI!
await prisma.$queryRawUnsafe(
  `SELECT struktur.fn_shobe_sayi(${merkezId}) AS say`
);</pre>
<p><code>$queryRawUnsafe</code> adı təsadüfi deyil — o, <em>təhlükəlidir</em>
və yalnız istifadəçi məlumatı olmayan dinamik SQL üçün nəzərdə tutulub.
Bizim <code>merkezId</code> istifadəçidən gəlir — deməli
<code>$queryRaw</code> işlətməliyik.</p>

<h4>⚠️ Niyə <code>$transaction</code> — 13 sorğu bir mənzərə üçün?</h4>
<p><code>umumi()</code> metodu 13 fərqli göstərici yığır: əməkdaş sayı,
aktiv/passiv, maaş aqreqatları, 6 əlaqə cəmi, 2 baza funksiyası,
cədvəl sayı. Onları ayrı-ayrı göndərsəydik, <em>aradakı boşluqlarda</em>
başqa istifadəçi məlumat dəyişə bilərdi və hesabat
<strong>uyğunsuz</strong> olardı:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
cem = 14
aktiv = 14
passiv = 0     ← 14 = 14 + 0 ✓
# ...amma aralarında yeni əməkdaş əlavə olundu:
doktorant = 10
sertifikat = 10  ← rəqəmlər artıq fərqli anda aiddir</pre>
<p><code>$transaction</code> massiv forması hamısını <strong>bir
snapshot</strong>-dan oxuyur. Üstəlik performans qazancı var: 13 sorğu
bir şəbəkə gediş-gəlişində gedir.</p>

<h4>N+1 problemi <code>butunMerkezler()</code>-də</h4>
<p>Tapşırıq: hər mərkəz üçün şöbə və əməkdaş sayını göstər. Sadəlövh
həll:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const merkezler = await prisma.merkezler.findMany();     // 1 sorğu
for (const m of merkezler) {
  m.shobe_sayi = await prisma.shobeler.count({...});     // 10 sorğu
  m.emekdas_sayi = await prisma.emekdaslar.count({...}); // 10 sorğu
}
// CƏMİ: 21 sorğu</pre>
<p>Buna <strong>N+1 problemi</strong> deyilir: 1 sorğu ilə başlayırıq,
sonra hər nəticə üçün <em>əlavə</em> N sorğu göndəririk. Mərkəz sayı
10 yox, 1 000 olsaydı — 2 001 sorğu!</p>
<p>Bizim həll: <strong>3 sorğu</strong>.</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const [shobeSaylari, emekdasSaylari] = await Promise.all([
  prisma.shobeler.groupBy({ by: ['merkez_id'], _count: { _all: true } }),
  prisma.emekdaslar.groupBy({ by: ['merkez_id'], where: {...}, _count: {...} }),
]);</pre>
<p>İki <code>groupBy</code> <code>Promise.all</code> ilə
<strong>paralel</strong> gedir, sonra nəticələri <code>Map</code> ilə
birləşdiririk. Sorğu sayı mərkəz sayından <em>asılı deyil</em> — bu,
N+1-in həllidir.</p>
""",
    "anlayis": [
        ("Aqreqasiya",
         "Çoxlu sətirdən <em>bir</em> nəticə çıxarmaq: cəm, orta, say, "
         "minimum, maksimum."),
        ("groupBy",
         "Sətirləri qruplara bölüb hər qrup üzrə aqreqat hesablamaq. "
         "SQL <code>GROUP BY</code>-ın Prisma qarşılığı."),
        ("aggregate",
         "Qruplaşdırmadan bütün dəst üzrə aqreqat. "
         "<code>_sum</code>, <code>_avg</code>, <code>_min</code>, "
         "<code>_max</code>, <code>_count</code>."),
        ("_count._all",
         "«Bu qrupda neçə sətir var». <code>_all</code> — «hansı sahə olursa "
         "olsun, sətirləri say»."),
        ("$queryRaw",
         "Xam SQL göndərmək. Şablon sətri parametrləri "
         "<strong>avtomatik</strong> parametrləşdirir."),
        ("$queryRawUnsafe",
         "Təhlükəli variant — parametrləşdirmə yoxdur. İstifadəçi məlumatı "
         "ötürməyin."),
        ("PL/pgSQL",
         "PostgreSQL-in prosedur dili. Funksiyalar <em>bazanın içində</em> "
         "saxlanılır və istənilən müştəridən çağırıla bilər."),
        ("N+1 problemi",
         "1 əsas sorğu + hər nəticə üçün N əlavə sorğu. Məlumat artdıqca "
         "fəlakətə çevrilir."),
        ("Promise.all",
         "Asılı olmayan asinxron əməliyyatları <strong>paralel</strong> "
         "işlədir. Ümumi vaxt cəminə yox, ən yavaşının vaxtına bərabərdir."),
        ("Ikili həqiqət (dual source of truth)",
         "Eyni məntiqin iki yerdə yazılması. Vaxt keçdikcə onlar "
         "uyğunsuzlaşır — məlumat səhvlərinin klassik mənbəyi."),
        ("Seçicilik (selectivity)",
         "Sorğunun nə qədər sətri «seçdiyi». Yüksək seçicilik (az sətir) — "
         "indeks üçün yaxşıdır."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) <code>statistika-sorgu.dto.ts</code> — kiçik, amma tam</h5>
<ul>
  <li><code>aktiv: 'aktiv' | 'hamisi'</code> — statistikanı <em>yalnız
      aktiv</em> əməkdaşlar üzrə, yoxsa hamısı üzrə almaq. Bu seçim
      vacibdir: işdən çıxmış əməkdaşların maaşı «orta maaş»a düşsəydi,
      göstərici yanıltıcı olardı.</li>
  <li><code>min_say</code> — «3-dən az əməkdaşı olan mərkəzləri
      göstərmə». Hesabatda kiçik qrupları gizlətmək üçün tipik
      ehtiyacdır (məxfilik və oxunaqlılıq baxımından).</li>
  <li><code>siralama: 'say' | 'ad' | 'orta_maas'</code> — hansı sütun
      üzrə sıralansın. ⚠️ Diqqət: bu sıralama <strong>yaddaşda</strong>
      aparılır (<code>Array.sort</code>), SQL-də yox — çünki
      <code>groupBy</code>-nin nəticəsi artıq qrup massividir.
      Böyük data üçün SQL-də sıralamaq daha yaxşı olardı (bax FAQ).</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2) <code>eded()</code> köməkçisi</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
function eded(d: Prisma.Decimal | number | null | undefined): number {
  if (d === null || d === undefined) return 0;
  const n = Number(d);
  return Number.isFinite(n) ? Math.round(n * 100) / 100 : 0;
}</pre>
<ul>
  <li>Üç tipi qəbul edir: <code>Decimal</code> (Prisma aqreqatları),
      <code>number</code> (<code>count</code>), <code>null</code>
      (boş qrup).</li>
  <li><code>Math.round(n * 100) / 100</code> — iki onluq rəqəmə
      yuvarlaqlaşdırma. <code>toFixed(2)</code> işlətmədik, çünki o,
      <em>mətn</em> qaytarır; statistika üçün isə <strong>ədəd</strong>
      lazımdır (frontend qrafik çəkəcək).</li>
  <li><code>Number.isFinite</code> — <code>NaN</code> və
      <code>Infinity</code>-ni tutur. <code>isNaN()</code> funksiyası
      <em>işləməzdi</em>, çünki o, dəyəri əvvəlcə ədədə çevirir:
      <code>isNaN('abc')</code> → <code>true</code>, amma
      <code>isNaN(undefined)</code> da <code>true</code>. Ona görə
      <code>Number.isNaN</code> / <code>Number.isFinite</code> daha
      dəqiqdir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3) <code>umumi()</code> — 13 sorğu, bir tranzaksiya</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const [cem, aktiv, passiv, maasAqreqat, ...] = await this.prisma.$transaction([
  this.prisma.emekdaslar.count(),
  ...
]);</pre>
<p>Massiv formasındaki <code>$transaction</code> <strong>massiv
qaytarır</strong> və destrukturizasiya ilə dəyişənlərə paylanır.
Diqqət: massivdəki sıra ilə dəyişənlərin sırası <em>üst-üstə
düşməlidir</em> — TypeScript bunu yoxlayır, çünki nəticə tipi
massivdir.</p>
<p>⚠️ <code>$queryRaw</code> çağırışları da massivdədir — Prisma onları
da eyni tranzaksiyada işlədir.</p>

<h5 style="color:#334155;margin-top:1rem">4) <code>merkezler()</code> — groupBy + Map birləşməsi</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const adlar = new Map(merkezler.map((m) => [m.id, m.ad]));</pre>
<ul>
  <li><code>new Map(massiv.map(...))</code> — <em>cütlər massivindən</em>
      Map yaratmağın qısa yolu. Hər cüt <code>[açar, dəyər]</code>
      formatındadır.</li>
  <li><code>adlar.get(id)</code> — O(1) axtarış. Massivdə
      <code>find()</code> işlətsəydik O(n) olardı və 100 mərkəzdə
      10 000 müqayisə demək idi.</li>
  <li><code>q.merkez_id === null</code> halı ayrıca işlənir: bəzi
      əməkdaşların mərkəzi təyin olunmayıb. Onları
      <code>'(mərkəz təyin olunmayıb)'</code> kimi göstəririk — hesabatda
      <code>null</code> görmək çaşqınlıq yaradır.</li>
  <li><code>minSay</code> filtri <strong>Map-dən ƏVVƏL</strong> yox,
      sonra tətbiq olunur. Səbəb: filtr SQL-də olsaydı,
      <code>groupBy</code> <code>having</code> tələb edərdi (Prisma hələ
      onu dəstəkləmir). Kiçik data üçün yaddaşda filtr kifayətdir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">5) <code>butunMerkezler()</code> — N+1-in həlli</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const [shobeSaylari, emekdasSaylari] = await Promise.all([
  this.prisma.shobeler.groupBy({ by: ['merkez_id'], _count: { _all: true } }),
  this.prisma.emekdaslar.groupBy({
    by: ['merkez_id'], where: { aktiv: true }, _count: { _all: true },
  }),
]);</pre>
<ul>
  <li><code>Promise.all</code> — iki <code>groupBy</code> bir-birindən
      <em>asılı deyil</em>, ona görə paralel göndərilir.</li>
  <li>Sonra iki <code>Map</code> yaradılır və
      <code>merkezler.map(...)</code> içində hər mərkəz üçün saylar
      <code>?? 0</code> ilə götürülür. <code>??</code> (nullish
      coalescing) — «yoxdursa 0». <code>||</code> işlətsəydik
      <code>0</code> dəyəri də «yoxdur» sayılardı, amma burada nəticə
      eyni olardı; prinsipcə isə <code>??</code> düzgündür.</li>
  <li>⚠️ <code>emekdasSaylari</code> filtrində
      <code>merkez_id !== null</code> yoxlaması var — çünki
      <code>groupBy</code> nəticəsində <code>null</code> açarı ola
      bilər və <code>BigInt(null)</code> xəta verər.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">6) <code>skriptler/statistika_yoxla.ts</code> — niyə servisi əl ilə yaradırıq</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const prisma = new PrismaService();
await prisma.onModuleInit();
const s = new StatistikaService(prisma);</pre>
<p>Nest konteyneri olmadan servisi <em>əl ilə</em> yaradırıq. Bu, daha
sadədir və <code>tsx</code> ilə işləyir. ⚠️ Nest <strong>tətbiqini</strong>
<code>tsx</code> ilə qaldırmaq isə <em>işləmir</em> — səbəbini ADDIM 26-da
izah edəcəyik (esbuild dekorator metadatasını yazmır).</p>
""",
    "fayllar": [
        "src/emekdaslar/statistika/dto/statistika-sorgu.dto.ts",
        "src/emekdaslar/statistika/statistika.service.ts",
        "src/emekdaslar/statistika/statistika.controller.ts",
        "skriptler/statistika_yoxla.ts",
    ],
    "goster": ["src/emekdaslar/emekdaslar.service.ts"],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then echo "  ✓ tip xətası yoxdur"; else echo "  ✗ tip xətası var"; fi

echo ""
echo "════ 2) Statistika modulu ════"
wc -l src/emekdaslar/statistika/*.ts src/emekdaslar/statistika/dto/*.ts | sed 's/^/      /'
printf '      aqreqat istifadəsi : %s\n' "$(grep -c '_count\|_avg\|_sum\|_min\|_max' src/emekdaslar/statistika/statistika.service.ts)"
printf '      $queryRaw çağırışı : %s\n' "$(grep -c 'queryRaw' src/emekdaslar/statistika/statistika.service.ts)"
printf '      $transaction       : %s\n' "$(grep -c 'transaction' src/emekdaslar/statistika/statistika.service.ts)"

echo ""
echo "════ 3) Bazadaki PL/pgSQL funksiyaları ════"
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
psql "$DBURL" -At -c "
SELECT '      ' || n.nspname || '.' || p.proname
  FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
 WHERE n.nspname NOT IN ('pg_catalog','information_schema','public')
 ORDER BY 1;" 2>/dev/null

echo ""
echo "════ 4) Marşrutlar ════"
grep -n "@Get('statistika" src/emekdaslar/statistika/statistika.controller.ts | sed 's/^/      /'

echo ""
echo "════ 5) CANLI statistika yoxlaması ════"
npx tsx skriptler/statistika_yoxla.ts
""",
    "olmaz": """`groupBy` olmasa — JavaScript-də saysaq:

const hamisi = await prisma.emekdaslar.findMany();   // BÜTÜN sətirlər
const saylar = {};
for (const e of hamisi) saylar[e.merkez_id] = (saylar[e.merkez_id] ?? 0) + 1;

14 sətirdə:   ~8 ms,  3 KB trafik
100 000 sətirdə: ~4 SANİYƏ, ~250 MB trafik

  ← ⚠️ Server 250 MB-ı yaddaşa yükləyir, sonra onu
     JavaScript-də sayır. 10 istifadəçi eyni anda sorğu
     göndərsə — 2.5 GB. Server çökür.

  ← ⚠️ Üstəlik verilənlər səhv ola bilər: biri sorğu
     gedərkən yeni əməkdaş əlavə etsə, say uyğunsuz olar.

────────────────────────────────────────────────────────────
`$transaction` olmasa — 13 ayrı sorğu:

cem      = 14
aktiv    = 14
passiv   = 0
  ...arada yeni əməkdaş əlavə olundu...
doktorant = 11
sertifikat = 11

  ← ⚠️ Hesabat İKİ FƏRQLİ ANA aiddir. «14 əməkdaş, amma
     11 doktorant» — hansı düzgündür? Heç biri tam deyil.

────────────────────────────────────────────────────────────
`$queryRawUnsafe` işlətsək:

const merkezId = req.query.merkez_id;   // istifadəçidən!
await prisma.$queryRawUnsafe(
  `SELECT struktur.fn_shobe_sayi(${merkezId})`
);

Sorğu:  ?merkez_id=1); DROP TABLE kadrlar.emekdaslar; --
Nəticə:  ⚠️ CƏDVƏL SİLİNDİ. Bütün əməkdaş məlumatı getdi.

  ← Ona görə şablon sətri (`$queryRaw`) işlədirik —
     Prisma ${...} ifadələrini PARAMETR kimi göndərir.""",
    "c_izah": """
<p><strong>Birinci qazanc: iş bazada qalır.</strong> 14 sətirdə fərq
görünmür — amma bu, <em>aldadıcıdır</em>. Statistika endpointləri
zamanla <strong>böyüyən</strong> dataya işləyir. Bugün 14, sabah 140,
bir ildən sonra 14 000. JavaScript-də sayma həlli bu gün işləyir və
sabah çökür. <code>groupBy</code> isə datanın ölçüsündən
<em>asılı olmayaraq</em> eyni miqdarda trafik göndərir (yalnız
nəticəni).</p>
<p><strong>İkincisi: bir tranzaksiya, bir həqiqət.</strong> 13
göstərici bir hesabatda görünürsə, onlar <em>eyni ana</em> aid
olmalıdır. <code>$transaction</code> bunu təmin edir. Bu, xüsusilə
maliyyə hesabatlarında həlledicidir: «gəlir 100 000, xərc 95 000» —
əgər bu rəqəmlər fərqli anlara aiddirsə, hesabat <em>yalan
danışır</em>.</p>
<p><strong>Üçüncüsü: baza funksiyaları kod təkrarını azaldır.</strong>
<code>kadrlar.fn_maas_fondu()</code> funksiyası artıq mövcuddur və
<em>başqa yerlərdə</em> (hesabatlar, Excel ixracı, digər servislər)
istifadə olunur. Onu TypeScript-də yenidən yazsaq, iki versiya
yaranardı: biri düzəldiləndə digəri köhnələr və rəqəmlər
uyğunsuzlaşardı. Ona görə <strong>mövcud məntiqi təkrar istifadə
edirik</strong>.</p>
<p><strong>Dördüncüsü: N+1-in ölçüsü.</strong> Sadəlövh həll 21 sorğu,
bizim həll 3 sorğu göndərir. Mərkəz sayı 1 000 olsaydı: 2 001 sorğu
qarşı 3. Bu, <em>xətti</em> (linear) artımla <em>sabit</em> (constant)
artım arasındaki fərqdir — miqyaslanmanın (scaling) açarıdır.</p>
<p><strong>Beşincisi: <code>$queryRaw</code> təhlükəsizliyi.</strong>
Prisma şablon sətri <code>${...}</code> ifadələrini parametr kimi
göndərir. Bu, <em>avtomatikdir</em> — yəni düzgün yazsanız, SQL
inyeksiyası <strong>mümkün deyil</strong>. Yeganə təhlükə
<code>$queryRawUnsafe</code> işlətməkdir. Bu funksiyanın adı sizə
xəbərdarlıqdır: «burada təhlükəsizlik sizin məsuliyyətinizdir».</p>
""",
    "sual": [
        ("<code>groupBy</code>-də <code>having</code> yoxdur. <code>min_say</code> filtrini necə edim?",
         "Prisma hazırda <code>having</code>-i dəstəkləmir, ona görə filtr nəticə üzərində <em>yaddaşda</em> tətbiq olunur (<code>.filter((q) => q._count._all >= minSay)</code>). Bu, qrup sayı az olduqda (onlarla, yüzlərlə) tamamilə məqbuldur. Milyonlarla qrup olsaydı, <code>$queryRaw</code> ilə əl ilə SQL yazmaq lazım gələrdi. Praktikada qrup sayı adətən azdır — mərkəz, şöbə, vəzifə kimi kateqoriyalar yüzlərlə ölçülür."),
        ("<code>_avg</code> dəqiq nəticə verirmi? Axı <code>Decimal</code> sürüşən nöqtədir.",
         "Bəli, <code>Decimal</code> <em>sürüşən nöqtə deyil</em> — o, dəqiq onluq ədəddir. PostgreSQL-də <code>avg(numeric)</code> dəqiq hesablanır. Bizim <code>eded()</code> funksiyası isə nəticəni <code>number</code>-ə çevirir və <em>oradа</em> dəqiqlik itə bilər (2^53 həddi). Maaşlar üçün bu, praktiki problem deyil (milyard manat maaş olmaz), amma <em>bilmək</em> lazımdır: TypeScript-in <code>number</code> tipi pul üçün nəzəri olaraq uyğun deyil."),
        ("Niyə <code>merkezler()</code> iki sorğu göndərir? <code>include</code> ilə bir sorğu olmazdımı?",
         "Xeyr, çünki <code>groupBy</code> əlaqələri <em>dəstəkləmir</em> — o, xam SQL <code>GROUP BY</code>-a çevrilir və orada əlaqə anlayışı yoxdur. Alternativ: <code>merkezler.findMany({ include: { emekdaslar: true } })</code> edib JavaScript-də qruplaşdırmaq. Amma bu, <strong>N+1-ə qayıtmaqdır</strong> — bütün əməkdaş sətirləri şəbəkə ilə gələr. İki sorğu (biri aqreqat, biri adlar üçün) daha yaxşıdır."),
        ("Baza funksiyasını çağırmaq üçün niyə <code>Prisma.sql</code> işlətmədim?",
         "<code>Prisma.sql</code> dinamik SQL parçaları qurmaq üçündür (məsələn şərti olaraq <code>WHERE</code> əlavə etmək). Bizim halda sorğu <em>sabіtdir</em> — yalnız bir parametr dəyişir. Şablon sətri bu iş üçün daha sadə və oxunaqlıdır. Dinamik hissə olsaydı, <code>Prisma.sql</code> və <code>Prisma.join</code> lazım gələrdi."),
        ("13 sorğu bir <code>$transaction</code>-da — bu, bazanı bloklamırmı?",
         "Bu, <em>oxu</em> tranzaksiyasıdır (yalnız <code>SELECT</code>). PostgreSQL-də oxu tranzaksiyaları sətirləri bloklamır (MVCC — Multi-Version Concurrency Control sayəsində). Yalnız <code>UPDATE</code>/<code>DELETE</code> sətir kilidləri qoyur. Üstəlik tranzaksiya çox qısadır (millisaniyələr). Uzun tranzaksiyalar isə problemdir — onlardan çəkinmək lazımdır."),
        ("<code>eded()</code> funksiyasını <code>src/common/</code>-a köçürməliyəm?",
         "Hazırda yalnız <code>StatistikaService</code> istifadə edir, ona görə yerində saxlamaq düzgündür. İkinci servis də ehtiyac duysa, köçürmək lazımdır. Qayda: <strong>iki dəfə təkrar etsən — çıxar</strong> (DRY). Vaxtından əvvəl çıxarmaq isə lazımsız abstraksiya yaradır."),
        ("Statistikanı keşləmək (cache) lazımdırmı?",
         "Hazırda yox — 37 millisaniyə çəkir. Amma bu endpoint <em>hər dashboard açılışında</em> çağırılacaq və data böyüdükcə yavaşlayacaq. O zaman həllər: (1) nəticəni Redis-də 60 saniyə saxlamaq; (2) <em>materialized view</em> yaratmaq və onu vaxtaşırı yeniləmək (`REFRESH MATERIALIZED VIEW`); (3) hesablanmış göstəriciləri ayrıca cədvəldə saxlamaq. Hər üçü «keş»dir — seçim datanın nə qədər tez dəyişdiyindən asılıdır."),
        ("<code>butunMerkezler()</code>-də <code>Promise.all</code> niyə lazımdır? Axı Prisma sorğuları onsuz da paralel gedir?",
         "<em>Xeyr</em>, getmir. JavaScript tək axınlıdır (single-threaded) və <code>await</code> ardıcıl işləyir: <code>await a(); await b();</code> → b, a bitəndən sonra başlayır. Yalnız <code>Promise.all</code> (və ya <code>$transaction</code> massiv forması) onları <em>eyni anda</em> göndərir. Bu, yeni başlayanların ən çox səhv başa düşdüyü mövzudur."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>Statistika servisi <strong>21 yoxlamadan</strong> keçdi — hamısı real
      bazada.</li>
  <li><strong>Ümumi mənzərə:</strong> 14 əməkdaş (14 aktiv, 0 passiv),
      maaş fondu <strong>33 000 AZN</strong>, orta maaş
      <strong>2 357.14 AZN</strong>, 48 cədvəl.
      Hesablanma <strong>37 ms</strong>.</li>
  <li><strong>Baza funksiyası Prisma ilə üst-üstə düşdü:</strong>
      <code>fn_maas_fondu()</code> = 33 000 = Prisma <code>_sum</code>.
      İki fərqli yolla eyni nəticə — bu, təsdiqdir.</li>
  <li><strong>Mərkəzlər üzrə:</strong> 9 qrup, ən böyüyü «Funksional
      şöbələr» (3 əməkdaş, orta maaş 1 466.67).</li>
  <li><strong>N+1 həlli:</strong> 10 mərkəz + 36 şöbə + 14 əməkdaş
      <strong>3 sorğu</strong> ilə (sadəlövh həll 21 sorğu olardı).</li>
  <li><strong>SQL inyeksiya cəhdi zərərsiz oldu</strong> — cədvəl
      yerindədir, 14 əməkdaş toxunulmazdır.</li>
</ul>
<p>Növbəti addımda bir əməkdaşın <em>bütün</em> bağlı məlumatını
göstərəcəyik — və sorğu sayını <strong>ölçəcəyik</strong>.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 23 — ƏLAQƏLƏR
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 23,
    "ad": "Əlaqələr — N+1 problemi və sorğu sayını ölçmək",
    "a": """
<p>2A-da bir əməkdaşın <em>əsas kartını</em> göstərdik. Real həyatda isə
HR mütəxəssisi bir əməkdaşa baxanda <strong>hər şeyi</strong> görmək
istəyir: hansı doktorantlara rəhbərlik edir, hansı sertifikatları var,
nə vaxt məzuniyyətdə olub, elmi şurada üzvdürmü.</p>
<p>Bazada bu məlumat <strong>6 ayrı cədvəldədir</strong>:</p>
<table style="width:100%;border-collapse:collapse;font-size:.88rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Cədvəl</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Əlaqə sütunu</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Tiпi</th>
  </tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0"><code>elm.doktorantlar</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>rehber_id</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">1 → N</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0"><code>tehsil.sertifikasiya</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>emekdas_id</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">1 → N</td></tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0"><code>kadrlar.mezuniyyetler</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>emekdas_id</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">1 → N</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0"><code>kadrlar.is_tecrubesi</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>emekdas_id</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">1 → N</td></tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0"><code>elm.tedqiqat_layiheleri</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>rehber_id</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">1 → N</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0"><code>struktur.elmi_shura_uzvleri</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>emekdas_id</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">1 → N</td></tr>
</table>

<h4>⚠️ N+1 problemi — «yavaş kod»un ən çox rast gəlinən səbəbi</h4>
<p>Sadəlövh həll: əvvəlcə əməkdaşı oxu, sonra hər əlaqəni ayrıca soruş.
Bu, <strong>7 sorğu</strong> deməkdir. Pis görünmür.</p>
<p>Amma <em>siyahı</em> üçün bunu etsək — fəlakətdir:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const emekdaslar = await prisma.emekdaslar.findMany();   // 1 sorğu
for (const e of emekdaslar) {
  e.doktorantlar = await prisma.doktorantlar.findMany({ where: { rehber_id: e.id } });
}                                                          // 14 sorğu
// CƏMİ: 15 sorğu</pre>
<p>14 əməkdaş → 15 sorğu. 1 000 əməkdaş → <strong>1 001 sorğu</strong>.
Hər sorğu şəbəkə gediş-gəlişidir (adətən 1–10 millisaniyə). 1 001 sorğu
= <strong>1–10 saniyə</strong> yalnız <em>gözləməyə</em>.</p>
<p>Buna <strong>N+1 problemi</strong> deyilir. Adı belədir: 1 əsas sorğu
+ N əlavə sorğu.</p>

<h4>Prisma bunu özü həll edirmi?</h4>
<p><strong>Qismən.</strong> Prisma <code>include</code> işlədəndə hər
əlaqə üçün <em>ayrı</em> SQL sorğusu göndərir. Ölçdük:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
await prisma.emekdaslar.findUnique({
  where: { id: 1n },
  include: { vezifeler: true, merkezler: true, cinsiyyet: true },
});
// → 4 sorğu:  1 əsas + 3 əlaqə</pre>
<p>Yəni 14 əməkdaş üçün <code>include</code> ilə 7 əlaqə = <strong>8
sorğu</strong> (əməkdaş başına yox — <em>ümumi</em>). Bu, N+1
<em>deyil</em>, çünki sorğu sayı sətir sayından asılı deyil. Amma
<em>sabit əlavə yükdür</em>.</p>
<p>Prisma 5+ versiyalarında PostgreSQL üçün
<code>relationLoadStrategy: 'join'</code> seçimi var — o, SQL
<code>JOIN</code> ilə <strong>bir</strong> sorğu göndərir. Bizim
quruluşda bu seçim <em>əlçatan deyil</em> (generator konfiqurasiyası
tələb edir), ona görə ölçmə ilə işləyirik.</p>

<h4>Ölçməni necə aparırıq? — Prisma-nın sorğu loqu</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const prisma = new PrismaClient({
  adapter: new PrismaPg({ connectionString: process.env.DATABASE_URL! }),
  log: [{ emit: 'event', level: 'query' }],       // ← sorğu hadisələrini yay
});

const sorgular: string[] = [];
prisma.$on('query', (e) => sorgular.push(e.query));   // ← hər sorğunu yaz

// ...sorğunu işlət...
console.log('Sorğu sayı:', sorgular.length);</pre>
<p><strong>Bu, dərsin ən dəyərli alətidir.</strong> «Yəqin ki bu yavaşdır»
demək yerinə, <em>həqiqi rəqəmi</em> görürük. Optimallaşdırma məhz belə
başlayır: əvvəlcə ölç, sonra dəyiş.</p>

<h4>Üç yanaşmanın müqayisəsi</h4>
<table style="width:100%;border-collapse:collapse;font-size:.88rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Yanaşma</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Sorğu sayı</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Nə vaxt işlədin</th>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>icmal()</code> — yalnız saylar</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>1</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">«3 doktorantı var» — məlumatın
        özü lazım deyil</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>hamisi()</code> — Promise.all</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">12</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Tam məlumat lazımdır; altı sorğu
        paralel gedir</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>birSorquda()</code> — bir
        <code>findUnique</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">12</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Kod daha qısadır, sorğu sayı
        <strong>eyni</strong></td>
  </tr>
</table>
<p>⚠️ <strong>Ən vacib nəticə:</strong> <code>hamisi()</code> ilə
<code>birSorquda()</code> <em>eyni sayda</em> sorğu göndərir. Yəni sorğu
sayını <strong>kod üslubu</strong> yox, <em>Prisma-nın strategiyası</em>
müəyyən edir. Fərqi yalnız <code>icmal()</code> yaradır — çünki o,
<code>_count</code> işlədir və məlumatın özünü heç oxumur.</p>

<h4>⚠️ <code>_count</code> — bir sorğuda bütün saylar</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
await prisma.emekdaslar.findUnique({
  where: { id: BigInt(id) },
  select: {
    id: true, ad: true,
    _count: {
      select: {
        doktorantlar: true, sertifikasiya: true, mezuniyyetler: true,
        is_tecrubesi: true, tedqiqat_layiheleri: true, elmi_shura_uzvleri: true,
      },
    },
  },
});</pre>
<p>Prisma bunu SQL-də <strong>alt sorğulara</strong>
(<code>(SELECT count(*) ...)</code>) çevirir — yəni <em>bir</em> SQL
sorğusu gedir. Ölçdük: <strong>1 sorğu</strong>. Bu, 12 sorğuya qarşı
<strong>12 qat</strong> azdır.</p>
<p>Nəticə: əgər istifadəçiyə yalnız <em>saylar</em> lazımdırsa (məsələn
kartın üzərində nişanlar: «4 doktorant», «1 şura üzvlüyü»),
<code>_count</code> işlədin. Tam siyahı lazımdırsa, 12 sorğu
qaçılmazdır.</p>

<h4>⚠️ <code>movcudYoxla()</code> — təkrar yoxlamanın qiyməti</h4>
<p>Hər public metod əvvəlcə «bu əməkdaş varmı?» yoxlayır. Bu,
<em>düzgün</em> davranışdır — 404 qaytarmaq üçün lazımdır. Amma
<code>hamisi()</code> altı metodu çağırsa və hər biri yoxlasa,
<strong>6 lazımsız sorğu</strong> gedər.</p>
<p>Həll: yoxlamasız <em>xam</em> versiyaları ayırmaq:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
async doktorantlar(id: number) {          // ictimai
  await this.movcudYoxla(id);             // ← bir dəfə yoxla
  return this.doktorantlarXam(id);        // ← sonra işlə
}
private async doktorantlarXam(id: number) { /* yoxlama yoxdur */ }</pre>
<p>Bu naxışın adı <strong>«nazik sarğı»</strong> (thin wrapper)-dir.
Ölçmə göstərdi: bu düzəliş <strong>1 sorğu</strong> qənaət etdi
(13 → 12). Kiçik görünür, amma prinsip vacibdir:
<em>eyni yoxlamanı təkrar etmə</em>.</p>
""",
    "anlayis": [
        ("N+1 problemi",
         "1 əsas sorğu + hər nəticə üçün N əlavə sorğu. Sətir sayı artdıqca "
         "sorğu sayı da <em>xətti</em> artır."),
        ("Sorğu sayğacı",
         "Prisma-nın <code>log: [{ emit: 'event', level: 'query' }]</code> "
         "və <code>$on('query', ...)</code> mexanizmi. Həqiqi sorğu sayını "
         "ölçməyə imkan verir."),
        ("_count",
         "Prisma-nın əlaqə sayğacı. SQL-də alt sorğuya çevrilir — "
         "<strong>bir</strong> sorğu."),
        ("include vs select",
         "<code>include</code> əlaqələri <em>əlavə</em> edir; "
         "<code>select</code> isə tam nəzarət verir — nə götürüləcəyini "
         "siz seçirsiniz."),
        ("Promise.all",
         "Asılı olmayan sorğuları paralel işlədir. Sorğu <em>sayını</em> "
         "azaltmır, <em>vaxtını</em> azaldır."),
        ("Nazik sarğı (thin wrapper)",
         "Ortaq yoxlamanı bir yerdə saxlayıb, ağır işi ayrı private metoda "
         "çıxarmaq naxışı."),
        ("Boş massiv ≠ null",
         "Əlaqə yoxdursa Prisma <code>[]</code> qaytarır, <code>null</code> "
         "yox. Ona görə <code>?.length</code> yazmaq lazım deyil."),
        ("relationLoadStrategy",
         "Prisma seçimi: <code>'query'</code> (hər əlaqə üçün ayrı sorğu) "
         "və ya <code>'join'</code> (bir SQL JOIN). Bizim quruluşda "
         "<code>'join'</code> əlçatan deyil."),
        ("Mapper",
         "Xam baza sətrini API cavabına çevirən funksiya. Əlaqələr üçün də "
         "lazımdır: <code>BigInt</code>, <code>Decimal</code>, tarixlər."),
        ("Ölçmədən optimallaşdırma",
         "«Yəqin bu yavaşdır» — ən pis başlanğıc. Əvvəlcə rəqəmi ölçün, "
         "sonra dəyişin."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) <code>movcudYoxla()</code> — tək ortaq yoxlama</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
private async movcudYoxla(id: number): Promise<{ tam_ad: string; aktiv: boolean }> {
  const e = await this.prisma.emekdaslar.findUnique({
    where: { id: BigInt(id) },
    select: { id: true, ad: true, soyad: true, ata_adi: true, aktiv: true },
  });
  if (!e) throw new NotFoundException(...);
  return { tam_ad: `${e.soyad} ${e.ad} ${e.ata_adi}`, aktiv: e.aktiv };
}</pre>
<ul>
  <li><code>private</code> — bu metod sinfin <em>içi</em> üçündür; controller
      onu çağıra bilməz.</li>
  <li>Yalnız <strong>5 sütun</strong> oxuyur (<code>select</code>) — tam
      sətri oxumaq lazım deyil. Bu, 18 sütun yerinə 5 sütundur.</li>
  <li>Qaytarılan obyekt <em>iki</em> şey verir: tam ad (təkrar hesablamamaq
      üçün) və aktivlik. Beləliklə çağıran tərəf əlavə sorğu göndərmir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2) Nazik sarğı naxışı</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
async doktorantlar(id: number): Promise<DoktorantCavabi[]> {
  await this.movcudYoxla(id);
  return this.doktorantlarXam(id);
}

private async doktorantlarXam(id: number): Promise<DoktorantCavabi[]> {
  const setirler = await this.prisma.doktorantlar.findMany({ ... });
  return setirler.map(...);
}</pre>
<p>⚠️ <strong>Niyə bu vacibdir?</strong> <code>hamisi()</code> altı
metodu çağırır. Əgər o, <em>ictimai</em> versiyaları çağırsaydı,
6 dəfə eyni yoxlama gedərdi — 6 lazımsız sorğu. Ona görə
<code>hamisi()</code> <em>xam</em> versiyaları çağırır.</p>

<h5 style="color:#334155;margin-top:1rem">3) <code>icmal()</code> — <code>_count</code> sehrİ</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
select: {
  id: true, ad: true, soyad: true, ata_adi: true, aktiv: true,
  _count: {
    select: {
      doktorantlar: true, sertifikasiya: true, mezuniyyetler: true,
      is_tecrubesi: true, tedqiqat_layiheleri: true, elmi_shura_uzvleri: true,
    },
  },
}</pre>
<ul>
  <li><code>_count</code> <em>select</em> içindədir — yəni aqreqat da
      seçilə bilən sahədir.</li>
  <li>Nəticə <code>e._count.doktorantlar</code> kimi oxunur.</li>
  <li>Prisma bunu bir SQL sorğusuna çevirir: hər əlaqə
      <code>(SELECT count(*) FROM ... WHERE ...)</code> alt sorğusuna.</li>
  <li><code>cem_elaqe</code> — altı sayın cəmi. Hesablamanı serverdə
      edirik ki, frontend sadəcə göstərsin.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">4) <code>orderBy</code> əlaqə daxilində</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
this.prisma.doktorantlar.findMany({
  where: { rehber_id: BigInt(id) },
  select: { ... },
  orderBy: { qebul_tarixi: 'desc' },
});</pre>
<p>Hər əlaqə üçün <em>öz</em> sıralaması var: doktorantlar qəbul tarixinə
görə azalan, sertifikatlar imtahan tarixinə görə, məzuniyyətlər başlama
tarixinə görə. Məntiqlidir: ən yeni məlumat yuxarıda olsun.</p>
<p>⚠️ <code>null</code> dəyərlər: PostgreSQL-də <code>DESC</code>
sıralamada <code>NULL</code>-lar <em>əvvəldə</em> gəlir. Əgər tarixi
olmayan sətirlər yuxarıda görünsün istəmirsinizsə,
<code>nulls: 'last'</code> əlavə etmək lazımdır. Bizdə bu,
problem deyil — çünki əksər sətirlərin tarixi var.</p>

<h5 style="color:#334155;margin-top:1rem">5) Mapper-in əlaqələr üçün vacibliyi</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
doktorantlar: setirler.map((d) => ({
  id: d.id,
  ad_soyad: `${d.soyad} ${d.ad} ${d.ata_adi}`,
  status: d.status,
  proqram: d.doktorantura_proqramlari?.ad ?? null,
  qebul_tarixi: tarix(d.qebul_tarixi),
  ...
}))</pre>
<ul>
  <li><code>ad</code>, <code>soyad</code>, <code>ata_adi</code> ayrı
      sütunlardır — biz onları <code>ad_soyad</code> kimi
      <strong>birləşdiririk</strong>. Frontend üçün bu, hazır
      göstərişdir.</li>
  <li><code>d.doktorantura_proqramlari?.ad ?? null</code> — əlaqə
      <em>nullable</em> ola bilər (<code>?</code>) və <code>??</code>
      «yoxdursa null». İki işarə birlikdə lazımdır.</li>
  <li><code>tarix()</code> — 2A-dan tanış köməkçi:
      <code>Date</code> → <code>YYYY-MM-DD</code>.</li>
  <li>⚠️ <code>sertifikasiya.bal</code> <code>Decimal</code>-dir və
      <code>pul()</code> ilə mətnə çevrilir. Burada adı «pul» olsa da,
      bal üçün də işləyir — funksiya sadəcə <code>toFixed(2)</code>
      edir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">6) <code>skriptler/elaqeler_yoxla.ts</code> — sorğu sayğacı</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const saygar = new PrismaClient({
  adapter: new PrismaPg({ connectionString: process.env.DATABASE_URL! }),
  log: [{ emit: 'event', level: 'query' }],
});
const sorgular: string[] = [];
saygar.$on('query', (e) => sorgular.push(e.query.replace(/\s+/g, ' ')));

const xidmet = new ElaqelerService(saygar as unknown as PrismaService);</pre>
<ul>
  <li>⚠️ <code>as unknown as PrismaService</code> — <em>tip çevirməsi</em>.
      <code>PrismaClient</code> və <code>PrismaService</code> eyni API-yə
      malikdir (<code>PrismaService</code> onu <em>genişləndirir</em>),
      amma TypeScript bunu bilmir. Servis yalnız <code>emekdaslar</code>,
      <code>doktorantlar</code> kimi <em>delegate</em>-ləri işlədir və
      onlar hər iki tipdə var.</li>
  <li><code>e.query.replace(/\s+/g, ' ')</code> — SQL-dəki sətir keçidləri
      və boşluqları tək boşluğa salır ki, çap zamanı oxunaqlı olsun.</li>
  <li>Skript ölçməni <strong>3 dəfə</strong> edir və <em>minimumu</em>
      götürür — ilk sorğu həmişə yavaş olur (bağlantı, keş).</li>
</ul>
""",
    "fayllar": [
        "src/emekdaslar/elaqeler/elaqeler.service.ts",
        "src/emekdaslar/elaqeler/elaqeler.controller.ts",
        "skriptler/elaqeler_yoxla.ts",
    ],
    "goster": ["src/emekdaslar/statistika/statistika.service.ts"],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then echo "  ✓ tip xətası yoxdur"; else echo "  ✗ tip xətası var"; fi

echo ""
echo "════ 2) Əlaqələr modulu ════"
printf '      servis sətirləri : %s\n' "$(wc -l < src/emekdaslar/elaqeler/elaqeler.service.ts | tr -d ' ')"
printf '      ictimai metodlar : %s\n' "$(grep -cE '^  async [a-z]' src/emekdaslar/elaqeler/elaqeler.service.ts)"
printf '      xam (private)    : %s\n' "$(grep -cE '^  private async [a-z]+Xam' src/emekdaslar/elaqeler/elaqeler.service.ts)"
printf '      endpoint sayı    : %s\n' "$(grep -c '@Get' src/emekdaslar/elaqeler/elaqeler.controller.ts)"
echo "      ── endpoint-lər ──"
grep -oE "@Get\('[^']*'\)" src/emekdaslar/elaqeler/elaqeler.controller.ts | sed "s/^/        /"

echo ""
echo "════ 3) Əlaqəli cədvəllərdə real məlumat ════"
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
psql "$DBURL" -At -c "
SELECT '      ' || c.ad || ': ' || c.say
  FROM (SELECT 'doktorantlar' ad, count(*)::text say FROM elm.doktorantlar
        UNION ALL SELECT 'sertifikasiya', count(*)::text FROM tehsil.sertifikasiya
        UNION ALL SELECT 'mezuniyyetler', count(*)::text FROM kadrlar.mezuniyyetler
        UNION ALL SELECT 'is_tecrubesi', count(*)::text FROM kadrlar.is_tecrubesi
        UNION ALL SELECT 'tedqiqat_layiheleri', count(*)::text FROM elm.tedqiqat_layiheleri
        UNION ALL SELECT 'elmi_shura_uzvleri', count(*)::text FROM struktur.elmi_shura_uzvleri) c;" 2>/dev/null

echo ""
echo "════ 4) CANLI ölçmə — sorğu sayı və vaxt ════"
npx tsx skriptler/elaqeler_yoxla.ts
""",
    "olmaz": """N+1 problemi — siyahıda hər sətir üçün ayrı sorğu:

// SADƏLÖVH HƏLL
const emekdaslar = await prisma.emekdaslar.findMany();     // 1 sorğu
for (const e of emekdaslar) {
  e.doktorantlar = await prisma.doktorantlar.findMany({
    where: { rehber_id: e.id },
  });
}

14 əməkdaş   →  15 sorğu   →  ~50 ms      ✅ işləyir
100 əməkdaş  → 101 sorğu   →  ~400 ms     ⚠️ yavaşlayır
1 000 əməkdaş→1001 sorğu   →  ~4 SANİYƏ   ❌ qəbuledilməz
10 000       →10001 sorğu  →  ~40 SANİYƏ  ❌❌ server timeout

  ← ⚠️ Problem datanın BÖYÜMƏSİ ilə üzə çıxır. Test bazasında
     (14 sətir) hər şey «işləyir». İstehsalata çıxanda isə
     səhifə açılmır və səbəb aydın deyil — çünki kod
     dəyişməyib, DATA dəyişib.

────────────────────────────────────────────────────────────
movcudYoxla() təkrarı olmadan:

hamisi() → movcudYoxla()        // 1 sorğu
         → doktorantlar()       //   movcudYoxla() + sorğu = 2
         → sertifikatlar()      //   movcudYoxla() + sorğu = 2
         → mezuniyyetler()      //   movcudYoxla() + sorğu = 2
         → tecrube()            //   movcudYoxla() + sorğu = 2
         → layiheler()          //   movcudYoxla() + sorğu = 2
         → shura()              //   movcudYoxla() + sorğu = 2
         CƏMİ: 13 sorğu (12 yerinə)

  ← ⚠️ Altı LAZIMSIZ yoxlama. Hər biri ~2 ms = 12 ms boş
     yerə gözləmə. Yüzlərlə istifadəçidə bu, bazaya minlərlə
     lazımsız sorğu deməkdir.

────────────────────────────────────────────────────────────
Ölçmədən «optimallaşdırmaq»:

// «Bilirəm ki bu yavaşdır, include-i select-ə çevirim»
await prisma.emekdaslar.findMany({ select: { ... } });

  ← ⚠️ Ölçməmişdən əvvəl «optimallaşdırma» çox vaxt heç nəyi
     dəyişmir, ya da daha pis edir. Düzgün ardıcıllıq:
     1) ölç  2) dar boğazı tap  3) dəyiş  4) YENİDƏN ölç.""",
    "c_izah": """
<p><strong>Birinci nəticə: sorğu sayı ÖLÇÜLDÜ.</strong>
<code>icmal()</code> → <strong>1 sorğu</strong>.
<code>hamisi()</code> → <strong>12 sorğu</strong>.
<code>birSorquda()</code> → <strong>12 sorğu</strong>.</p>
<p>Üçüncü rəqəm ən maraqlısıdır: kod tamam fərqli yazılıb (altı ayrı
metod <code>Promise.all</code> ilə qarşı bir <code>findUnique</code>),
amma sorğu sayı <em>eynidir</em>. Səbəb: Prisma-nın standart
strategiyası hər əlaqə üçün ayrı SQL sorğusu göndərir —
<em>kod üslubundan asılı olmayaraq</em>. Bunu bilmək vacibdir, çünki
yeni başlayanlar tez-tez «<code>include</code> işlətsəm, bir sorğu
olar» deyə düşünürlər. <strong>Olmayacaq.</strong></p>
<p><strong>İkinci nəticə: <code>_count</code> həqiqətən işləyir.</strong>
1 sorğu qarşı 12 sorğu — <strong>12 qat</strong> fərq. Bu, dərsin ən
böyük optimallaşdırma qazancıdır. Praktik qayda: <em>əgər yalnız say
lazımdırsa, heç vaxt tam məlumatı çəkmə</em>.</p>
<p><strong>Üçüncüsü: <code>Promise.all</code> vaxtı azaldır, sorğu
sayını yox.</strong> Ardıcıl 6 ms, paralel 6 ms — 14 sətirdə fərq
görünmür. Amma <em>uzaq bazada</em> (şəbəkə gecikməsi 50 ms olsa)
fərq <em>6 × 50 = 300 ms</em> qarşı <em>50 ms</em> olardı.
Yəni <code>Promise.all</code> şəbəkə gecikməsini
<strong>gizlədir</strong>, sorğu sayını yox.</p>
<p><strong>Dördüncüsü: təkrar yoxlama real pul deməkdir.</strong>
<code>movcudYoxla()</code>-nı altı dəfə çağırmaq 6 lazımsız sorğu
deməkdir. Bu, kiçik görünür, amma <em>hər</em> endpoint çağırışında
təkrarlanır. Gündə 10 000 sorğu × 6 = 60 000 lazımsız sorğu. Baza
serveri boş yerə yüklənir.</p>
<p><strong>Beşincisi: boş əlaqə <code>[]</code>-dir, <code>null</code>
yox.</strong> <code>findMany</code> heç nə tapmasa <em>boş massiv</em>
qaytarır. Ona görə <code>?.length</code> və ya <code>?? []</code>
yazmaq lazım deyil — bu, əlaqə üçün <code>null</code> qaytaran
<code>findUnique</code>-dən fərqli davranışdır.</p>
""",
    "sual": [
        ("<code>relationLoadStrategy: 'join'</code> işlətsəm, bir sorğu olar?",
         "Nəzəri olaraq bəli — SQL <code>JOIN</code> ilə bir sorğu. Amma bizim quruluşda bu seçim <strong>əlçatan deyil</strong>: <code>Unknown argument relationLoadStrategy</code> xətası verir. Səbəb: generator blokunda xüsusi <code>previewFeatures</code> ayarı tələb olunur. Onu aktiv etsəydik, sxemi dəyişmək və klienti yenidən yaratmaq lazım gələrdi. Dərsin məqsədi isə <em>problemi görmək və ölçmək</em>dir — hansı alətlə həll etdiyimiz ikinci dərəcəlidir."),
        ("<code>_count</code> niyə belə sürətlidir? Axı SQL-də <code>count(*)</code> yavaş ola bilər.",
         "PostgreSQL-də <code>count(*)</code> həqiqətən <em>bütün</em> cədvəli oxuyur (MVCC səbəbindən). Amma bizim halda say <em>filtrli</em>dir (<code>WHERE rehber_id = 6</code>) və indeksdən istifadə edir. Üstəlik alt sorğu <em>bir</em> cədvəl üçün deyil — altısı bir sorğuda gedir. Əgər cədvəl milyonlarla sətir olsaydı, materialized view və ya saxlanmış sayğac daha yaxşı olardı."),
        ("<code>as unknown as PrismaService</code> təhlükəli deyilmi?",
         "Bu, <em>tip</em> çevirməsidir — işləmə vaxtında heç nə dəyişmir. Təhlükə ondadır ki, TypeScript sizi səhvdən xəbərdar edə bilməz. Bizim halda risk minimaldır: <code>PrismaService</code> <code>PrismaClient</code>-i <em>genişləndirir</em>, yəni hər <code>PrismaClient</code> metodunu ehtiva edir. Yeganə əlavə <code>yoxla()</code> metodudur və servis onu işlətmir. Daha təmiz alternativ: <code>PrismaClient</code> tipini qəbul edən konstruktor yazmaq, amma bu, istehsalat kodunu test üçün dəyişmək deməkdir."),
        ("Səhifələmə (pagination) əlaqələrdə necə olmalıdır?",
         "Vacib sualdır. Bir əməkdaşın 500 sertifikatı ola bilər — hamısını qaytarmaq düzgün deyil. Bizim halda ən çoxu 4 doktorant var, ona görə səhifələmə qoymaduq. Real sistemdə hər əlaqə endpoint-i üçün <code>?seife&amp;limit</code> əlavə etmək lazımdır. Alternativ: <code>take: 20</code> kimi sərt hədd qoyub, qalanı üçün ayrı endpoint vermək."),
        ("Niyə hər əlaqə üçün ayrı endpoint var? <code>/:id/tam</code> onsuz da hamısını verir.",
         "Çünki frontend həmişə hamısını istəmir. Məsələn əməkdaş kartının ilk ekranında yalnız əsas məlumat və saylar görünür; istifadəçi «Doktorantlar» tabına keçəndə isə yalnız o məlumat yüklənir. Ayrı endpoint-lər <strong>lazy loading</strong> imkanı verir — şəbəkə trafiki azalır və səhifə tez açılır. <code>/:id/tam</code> isə «hər şeyi bir dəfə yüklə» halı üçündür."),
        ("Sorğu loqu istehsalatda yandırılmalıdırmı?",
         "Xeyr! <code>log: [{ emit: 'event', level: 'query' }]</code> hər sorğunu yaddaşda saxlayır və yavaşlatır. Onun yeri: <em>test</em> və <em>optimallaşdırma</em>. İstehsalatda yalnız <code>['warn', 'error']</code> səviyyələri açılır. Əgər konkret problemi araşdırmaq lazımdırsa, müvəqqəti yandırıb söndürmək olar."),
        ("<code>Promise.all</code> ilə <code>$transaction</code> massiv formasının fərqi nədir?",
         "<code>Promise.all</code> sorğuları <em>paralel</em> göndərir, amma hər biri <strong>ayrı tranzaksiyadır</strong> — biri uğursuz olsa, digərləri işləyib qalar. <code>$transaction</code> massiv forması isə hamısını <strong>bir tranzaksiyada</strong> işlədir: biri pozulsa, hamısı geri qaytarılır. Oxuma üçün fərq yalnız <em>tutarlılıq</em>dadır; yazma üçün isə fərq <strong>həlledicidir</strong>."),
        ("Bu kodda <code>N+1</code> qalıbmı?",
         "Endpoint səviyyəsində yox — hər endpoint sabit sayda sorğu göndərir. Amma <em>siyahı + əlaqə</em> birləşsəydi, N+1 yenidən peyda ola bilərdi. Ona görə qayda: <strong>siyahı endpoint-lərində heç vaxt dövr içində sorğu göndərmə</strong>. Əgər əlaqə lazımdırsa, <code>include</code> (sabit sayda sorğu) və ya <code>groupBy</code> ilə <em>toplu</em> oxu."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>Əlaqə servisi <strong>17 yoxlamadan</strong> keçdi.</li>
  <li><strong>Ölçülmüş sorğu sayları:</strong>
      <code>icmal()</code> = <strong>1</strong>,
      <code>hamisi()</code> = <strong>12</strong>,
      <code>birSorquda()</code> = <strong>12</strong>.</li>
  <li><strong>Ən vacib tapıntı:</strong> <code>hamisi()</code> və
      <code>birSorquda()</code> eyni sayda sorğu göndərir — sorğu sayını
      <em>kod üslubu</em> yox, Prisma-nın strategiyası müəyyən edir.
      Yeganə real qazanc <code>_count</code>-dadır
      (<strong>12 qat</strong> az).</li>
  <li><strong>Real məlumat:</strong> ID 6 (Talıbov Tariyel İsmayıl) —
      4 doktorant, 1 şura üzvlüyü, 1 təcrübə, 1 layihə, cəmi 7 əlaqə.</li>
  <li><strong>Baza funksiyası təsdiqləndi:</strong>
      <code>kadrlar.fn_emekdas_tam_adi(6)</code> = TypeScript tərəfdəki
      hesablama ilə <em>eyni</em> nəticə.</li>
  <li><strong>Təkrarlanan yoxlama düzəldildi:</strong> xam metodlar
      ayırmaqla 1 lazımsız sorğu aradan qalxdı.</li>
  <li><strong>Boş əlaqə</strong> <code>[]</code> qaytarır,
      <code>null</code> yox.</li>
</ul>
<p>Növbəti addımda <em>toplu</em> əməliyyatlara keçirik: 50 sətri bir
sorğuda yaratmaq və <strong>atomiklik</strong> — yarısı yazılan partiya
olmaması.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 24 — TOPLU ƏMƏLİYYATLAR
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 24,
    "ad": "Toplu əməliyyatlar — createMany, updateMany və atomiklik",
    "a": """
<p>Təsəvvür edin: institut yeni tədris ili üçün <strong>40 müəllimi</strong>
sistemə daxil etməlidir. Əl ilə 40 dəfə forma doldurmaq — yarım gün.
Bizə <em>toplu</em> endpoint lazımdır.</p>

<h4>Ən pis həll — dövr içində bir-bir</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
for (const e of emekdaslar) {
  await prisma.emekdaslar.create({ data: e });   // 40 sorğu
}</pre>
<p><strong>İki problem:</strong></p>
<ol>
  <li><strong>Sürət.</strong> 40 sorğu × 2 ms = 80 ms yalnız şəbəkəyə.
      <code>createMany</code> ilə isə <em>1 sorğu</em>.</li>
  <li><strong>Atomiklik YOXDUR.</strong> 25-ci sətirdə xəta olsa, ilk
      24 sətir bazada <em>qalar</em>. İstifadəçi «40 müəllim əlavə etdim»
      düşünür, əslində 24-ü əlavə olunub. Hansı 24? Bilmir.</li>
</ol>
<p>İkinci problem <strong>daha ciddi</strong>dir. Yarımçıq yazılmış
məlumatı düzəltmək çox çətindir: hansı sətirlər yazıldığını bilmək üçün
tarixçəyə baxmaq lazımdır (əgər varsa).</p>

<h4>Həll 1: <code>createMany</code> — bir INSERT</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
await prisma.emekdaslar.createMany({ data: [ {...}, {...}, ... ] });</pre>
<p>Prisma bunu SQL-də belə göndərir:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
INSERT INTO kadrlar.emekdaslar (ad, soyad, ...) VALUES
  ('A', 'B', ...),
  ('C', 'D', ...),
  ...;</pre>
<p><strong>Bir sorğu, atomik.</strong> PostgreSQL-də <code>INSERT</code>
ifadəsi <em>atomikdir</em>: bir sətir pozuntunu pozsa, heç biri yazılmır.</p>
<p>⚠️ Amma <code>createMany</code> <strong>sətirləri qaytarmır</strong> —
yalnız <code>{ count: 40 }</code>. Yaratdığımız ID-ləri görmək üçün
<code>createManyAndReturn</code> lazımdır.</p>

<h4>Həll 2: <code>createManyAndReturn</code> — sətirlərlə birlikdə</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const setirler = await prisma.emekdaslar.createManyAndReturn({
  data,
  select: { id: true, ad: true, soyad: true },
  skipDuplicates: false,
});</pre>
<p>Bu, PostgreSQL-in <code>INSERT ... RETURNING *</code> xüsusiyyətini
işlədir. Nəticə əsl sətirlərdir — ID-lər daxil.</p>
<p>⚠️ <strong>BigInt tələsi:</strong> <code>id</code> BigInt-dir. Nəticəni
<code>console.log</code> və ya <code>JSON.stringify</code> ilə çap etsəniz,
<code>Do not know how to serialize a BigInt</code> xətası alacaqsınız.
Mapper-dən keçirin: <code>String(s.id)</code>.</p>

<h4><code>skipDuplicates</code> — «təkrarı atla»</h4>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Ayar</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Nəticə</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Nə vaxt</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>false</code> (standart)</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Təkrar varsa → <strong>xəta</strong>,
        HEÇ NƏ yazılmır</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">İstifadəçi səhvini bilməlidir</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>true</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Təkrar <strong>atlanır</strong>,
        qalanı yazılır</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Excel idxalı — köhnə sətirlər
        artıq varsa</td>
  </tr>
</table>
<p>Hansını seçmək? <strong>Bizə aydınlıq lazımdır</strong>. Excel-dən
100 sətir idxal edirsinizsə və 3-ü artıq varsa, <em>sükutla atlamaq</em>
yaxşıdır — amma istifadəçiyə <strong>demək</strong> lazımdır:
«97 yaradıldı, 3 atlandı». Bizim cavab obyektimiz məhz bunu edir.</p>

<h4>⚠️ <code>updateMany</code> — sətirləri QAYTARMIR</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const netice = await prisma.emekdaslar.updateMany({
  where: { id: { in: idler } },
  data: { aktiv: false },
});
// netice = { count: 5 }   ← sətirlər yox, yalnız SAY</pre>
<p>⚠️ <strong>Bu, çox vacib fərqdir.</strong> <code>updateMany</code>
<em>nəyi</em> dəyişdiyini demir — yalnız <em>neçəsini</em>. Əgər
istifadəçiyə yenilənmiş sətirləri göstərmək lazımdırsa, ayrıca
<code>findMany</code> göndərmək lazımdır.</p>
<p>Üstəlik: <code>count</code> göndərilən ID sayından <strong>az</strong>
ola bilər — bəzi ID-lər mövcud deyil. Bunu <em>sükutla qəbul etmək</em>
ən pis davranışdır. Bizim servis fərqi hesablayır və
<code>tapilmayan</code> sahəsində qaytarır.</p>

<h4>⚠️ <code>multiply</code> — atomik sahə əməliyyatı</h4>
<p>Toplu maaş artımını necə etmək? Sadəlövh həll:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
// ⚠️ TƏHLÜKƏLİ — «lost update» problemi
const setirler = await prisma.emekdaslar.findMany({ where: {...} });
for (const s of setirler) {
  await prisma.emekdaslar.update({
    where: { id: s.id },
    data: { maas: Number(s.maas) * 1.1 },   // ← OXU, hesabla, YAZ
  });
}</pre>
<p>Problem: <em>oxu</em> ilə <em>yaz</em> arasında başqa istifadəçi həmin
sətri dəyişsə, onun dəyişikliyi <strong>itər</strong>. Bu, bank
sistemlərində məşhur <em>lost update</em> problemidir.</p>
<p>Düzgün həll — hesablamanı <strong>bazanın içində</strong> etmək:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
await prisma.emekdaslar.updateMany({
  where,
  data: { maas: { multiply: 1.1 } },   // ← SQL: SET maas = maas * 1.1
});</pre>
<p>Bu, SQL-də <code>UPDATE ... SET maas = maas * 1.1 WHERE ...</code>
olur. Oxu-yaz arasında <em>boşluq yoxdur</em> — baza əməliyyatı
atomik yerinə yetirir. Prisma digər atomik əməliyyatları da dəstəkləyir:
<code>increment</code>, <code>decrement</code>, <code>multiply</code>,
<code>divide</code>, <code>set</code>.</p>

<h4>⚠️ FAİZ TƏLƏSİ — +10% sonra −10% geri qaytarmır!</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
3000 × 1.1 = 3300
3300 × 0.9 = <strong>2970</strong>   ← 3000 DEYİL!</pre>
<p>Bu, riyazi faktdır: faiz artımı <strong>geri qaytarıla bilməz</strong>
sadəcə əks faizlə. 30 AZN <em>yox oldu</em>. Düzgün geri qaytarma
<strong>bölməkdir</strong>: <code>3300 ÷ 1.1 = 3000</code>.</p>
<p>Bu, real sistemlərdə ciddi problemdir: «səhvən 10% artırdım, geri
qaytarım» deyəndə <em>bütün maaşlar</em> 30 AZN azalır. Düzgün həll:
əvvəlki qiymətləri <em>yazmaq</em> (audit loqundan və ya ehtiyat
nüsxədən), ya da <code>divide</code> işlətmək.</p>

<h4>⚠️ Filtrsiz toplu əməliyyat — QADAĞAN</h4>
<p>Ən təhlükəli ssenari: kimsə <code>{"faiz": 50}</code> göndərir və
heç bir filtr yoxdur. Nəticə: <strong>bütün</strong> əməkdaşların maaşı
50% artır. Geri qaytarmaq üçün audit loqundan <em>hər</em> sətri
bərpa etmək lazımdır.</p>
<p>Bizim servis bunu qəti qadağan edir:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const filterler = [dto.idler, dto.merkez_id, dto.vezife_id]
  .filter((x) => x !== undefined);

if (filterler.length === 0) {
  throw new BadRequestException(
    'Filtrsiz toplu maaş dəyişikliyi qadağandır — ' +
    'idler, merkez_id və ya vezife_id göndərin',
  );
}</pre>
<p>Bu naxışın adı <strong>«təhlükəsiz standart»</strong> (secure
default)-dir: təhlükəli əməliyyat üçün <em>açıq</em> icazə tələb olunur.</p>

<h4>⚠️ Validasiya massiv üzrə: <code>@ValidateNested({ each: true })</code></h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@IsArray()
@ArrayMinSize(1)
@ArrayMaxSize(50)
@ValidateNested({ each: true })
@Type(() => EmekdasYaratDto)
emekdaslar!: EmekdasYaratDto[];</pre>
<p>⚠️ <strong>Üç dekorator birlikdə lazımdır:</strong></p>
<ul>
  <li><code>@IsArray()</code> — ümumi tip yoxlaması. <strong>Tək başına
      KİFAYƏT DEYİL</strong> — massivin <em>elementlərini</em> yoxlamır.</li>
  <li><code>@Type(() => EmekdasYaratDto)</code> — xam JSON obyektlərini
      <em>sinif nüsxələrinə</em> çevirir. Bu olmasa, elementlər sadə
      obyekt qalar və <code>@ValidateNested</code> onları yoxlaya
      bilməz.</li>
  <li><code>@ValidateNested({ each: true })</code> — hər nüsxəni
      <strong>ayrıca</strong> yoxlayır. <code>each: true</code> olmasa
      massiv yox, tək obyekt gözlənilir.</li>
</ul>
<p><code>@ArrayMaxSize(50)</code> isə <em>qoruyucu hədddir</em>: biri
50 000 sətir göndərsə, server yaddaşı tükənər.</p>
""",
    "anlayis": [
        ("Toplu əməliyyat (bulk)",
         "Bir sorğuda çoxlu sətir üzərində əməliyyat. Şəbəkə gediş-gəlişini "
         "və tranzaksiya sayını azaldır."),
        ("createMany",
         "Bir <code>INSERT</code> ilə N sətir. <code>{ count: N }</code> "
         "qaytarır — sətirləri yox."),
        ("createManyAndReturn",
         "SQL <code>INSERT ... RETURNING</code>. Yaradılan sətirləri "
         "(ID-lər daxil) qaytarır."),
        ("skipDuplicates",
         "Unikal pozuntusu olan sətirləri xəta vermədən atlayır. Excel "
         "idxalı üçün idealdır."),
        ("updateMany",
         "Bir <code>UPDATE</code> ilə N sətir. Yalnız "
         "<code>{ count }</code> qaytarır."),
        ("Atomiklik",
         "«Ya hamısı, ya heç biri». PostgreSQL-də tək <code>INSERT</code>/"
         "<code>UPDATE</code> ifadəsi atomikdir."),
        ("Atomik sahə əməliyyatı",
         "<code>{ maas: { multiply: 1.1 } }</code> → SQL-də "
         "<code>SET maas = maas * 1.1</code>. Oxu-yaz boşluğu yoxdur."),
        ("Lost update",
         "Oxu → hesabla → yaz naxışında, aralıqda başqa istifadəçinin "
         "dəyişikliyinin itməsi."),
        ("@ValidateNested({ each: true })",
         "Massivin HƏR elementini ayrıca yoxlayır. "
         "<code>@Type(() => ...)</code> ilə birlikdə işlədilməlidir."),
        ("@ArrayMaxSize",
         "Massivin maksimum uzunluğu — yaddaş qoruyucusu."),
        ("Təhlükəsiz standart (secure default)",
         "Təhlükəli əməliyyat üçün <em>açıq</em> icazə tələb etmək. "
         "Unutqanlıq nəticəni dəyişməz."),
        ("Faiz tələsi",
         "+10% sonra −10% əvvəlki dəyəri qaytarmır: "
         "<code>x·1.1·0.9 = 0.99x</code>."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) <code>toplu.dto.ts</code> — üç DTO</h5>
<ul>
  <li><code>TopluYaratDto</code> — massiv + <code>tekrarlariAtla</code>
      bayrağı. Limitlər: ən azı 1, ən çoxu 50 sətir.</li>
  <li><code>TopluAktivlikDto</code> — <code>idler</code> (mütləq,
      1–100) + <code>aktiv</code>. ⚠️ <code>idler</code>-in
      <strong>mütləq</strong> olması qoruyucu qərardır: filtrsiz toplu
      dəyişiklik bütün cədvəli dəyişə bilər.</li>
  <li><code>MaasArtimDto</code> — <code>faiz</code> (−50…+100) və üç
      <em>istəyə bağlı</em> filtr. «Ən azı biri verilməlidir» yoxlaması
      <em>servisdədir</em>, çünki orada mesaj daha aydın yazıla bilir.</li>
</ul>
<p>⚠️ <code>@Min(-50)</code> niyə? Çünki <code>faiz = -100</code> olsaydı,
əmsal <code>1 + (-100/100) = 0</code> olardı və
<code>multiply: 0</code> <strong>bütün maaşları sıfırlayardı</strong>.
Bu, fəlakət olardı. Hədd bunun qarşısını alır.</p>

<h5 style="color:#334155;margin-top:1rem">2) <code>topluYarat()</code> — xəritələmə</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const data: Prisma.emekdaslarUncheckedCreateInput[] = dto.emekdaslar.map((e) => ({
  ad: e.ad.trim(),
  ...
  is_status_id: e.is_status_id ?? 1,
  email: e.email ?? null,
  ...
}));</pre>
<ul>
  <li>Hər element <em>əl ilə</em> xəritələnir — DTO-dan birbaşa
      Prisma-ya ötürmürük. Səbəb: <code>dogum_tarixi</code> mətni
      <code>Date</code>-ə çevrilməlidir, <code>trim()</code> tətbiq
      olunmalıdır, standart dəyərlər qoyulmalıdır.</li>
  <li><code>?? 1</code> — <code>is_status_id</code> verilməzsə «Aktiv».
      <code>??</code> işlədirik, <code>||</code> yox — çünki
      <code>0 || 1</code> də 1 verərdi, halbuki <code>0</code> etibarlı
      dəyər ola bilər.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3) <code>createManyAndReturn</code> + BigInt</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const setirler = await this.prisma.emekdaslar.createManyAndReturn({
  data,
  select: { id: true, ad: true, soyad: true, email: true },
  skipDuplicates: dto.tekrarlariAtla ?? false,
});

const idler = setirler.map((s) => String(s.id));   // ← BigInt → mətn
const atlanan = data.length - setirler.length;      // ← nə qədər atlandı</pre>
<ul>
  <li><code>String(s.id)</code> — <strong>mütləqdir</strong>, yoxsa JSON
      cavabı 500 verər.</li>
  <li><code>atlanan</code> — göndərilən ilə yaradılanın fərqi. İstifadəçiyə
      <em>demək</em> lazımdır ki, nə qədər sətir atlandı.</li>
  <li><code>skipDuplicates: dto.tekrarlariAtla ?? false</code> —
      standart <code>false</code> (təhlükəsiz standart: xəta ver,
      sükutla atlama).</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">4) <code>topluAktivlik()</code> — fərqi bildirmək</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const netice = await this.prisma.emekdaslar.updateMany({
  where: { id: { in: idler } },
  data: { aktiv: dto.aktiv },
});

const tapilmayan = dto.idler.length - netice.count;
if (tapilmayan > 0) {
  this.log.warn(`${tapilmayan} ID tapılmadı: ${dto.idler.join(', ')}`);
}</pre>
<p>⚠️ <code>log.warn</code> — <em>xəbərdarlıq</em> səviyyəsi, çünki bu,
gözlənilməz haldır (istifadəçi mövcud olmayan ID göndərib). Cavabda da
<code>tapilmayan</code> sahəsi qaytarılır.</p>

<h5 style="color:#334155;margin-top:1rem">5) <code>maasArtim()</code> — filtrsiz qadağa</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const filterler = [dto.idler, dto.merkez_id, dto.vezife_id]
  .filter((x) => x !== undefined);

if (filterler.length === 0) throw new BadRequestException(...);

const where: Prisma.emekdaslarWhereInput = { maas: { not: null } };
if (dto.idler) where.id = { in: dto.idler.map((i) => BigInt(i)) };
if (dto.merkez_id !== undefined) where.merkez_id = dto.merkez_id;
if (dto.vezife_id !== undefined) where.vezife_id = dto.vezife_id;

const emsal = 1 + dto.faiz / 100;
await this.prisma.emekdaslar.updateMany({
  where,
  data: { maas: { multiply: emsal } },
});</pre>
<ul>
  <li><code>{ maas: { not: null } }</code> — maaşı olmayan sətirləri
      kənarlaşdırır. Onsuz <code>count</code> yanıltıcı olardı (sətir
      «dəyişdi», amma dəyər <code>null</code> qaldı).</li>
  <li><code>1 + dto.faiz / 100</code> — faizi əmsala çevirir.
      <code>10% → 1.1</code>, <code>−10% → 0.9</code>.</li>
  <li><code>multiply</code> — atomik, bazada hesablanır.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">6) <code>atomiklikYoxla()</code> — rollback sübutu</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const auditEvvel = await this.prisma.audit_log.count({ where: {...} });

try {
  await this.prisma.$transaction(async (tx) => {
    await tx.emekdaslar.create({ data: {...} });   // 1-ci
    await tx.emekdaslar.create({ data: {...} });   // 2-ci
    throw new Error('QƏSDƏN XƏTA: tranzaksiya geri qaytarılmalıdır');
  });
} catch (x) { xetaMetni = (x as Error).message; }

const qalan = await this.prisma.emekdaslar.count({ where: {...} });
const auditSonra = await this.prisma.audit_log.count({ where: {...} });</pre>
<ul>
  <li><strong>İnteraktiv tranzaksiya</strong> — callback forması. Burada
      sıra ilə bir neçə əməliyyat etmək və <em>qərar verə</em> bilmək
      olur (məsələn «əgər X varsa, Y etmə»).</li>
  <li>İki sətir yaradılır, sonra <strong>qəsdən xəta atılır</strong>.
      Nəticədə heç biri qalmamalıdır.</li>
  <li>⚠️ <strong>Ən incə detal:</strong> audit loqu da artmamalıdır!
      Baza trigger-i <code>AFTER INSERT</code>-dır, amma trigger
      <em>COMMIT</em> anında təsir edir. Tranzaksiya geri qaytarılsa,
      trigger-in yazdığı sətir də <strong>yox olur</strong>. Bu,
      düzgün və gözlənilən davranışdır.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">7) <code>skriptler/toplu_yoxla.ts</code> — təmizlik</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
} finally {
  const silindi = await prisma.emekdaslar.deleteMany({
    where: { email: { startsWith: 'toplu.' } },
  });
  const qalan = await prisma.emekdaslar.count();
  console.log(`  → təmizlik: ${silindi.count} test sətri silindi, bazada ${qalan} əməkdaş`);
  await prisma.$disconnect();
}</pre>
<p><code>finally</code> bloku <strong>həmişə</strong> işləyir — xəta
olsa da, olmasa da. Beləliklə test yarıda çöksə belə, zibil sətirlər
qalmır. <code>deleteMany</code> filtri isə yalnız <em>bizim</em>
prefiksi (<code>toplu.</code>) hədəfləyir — real məlumata toxunmur.</p>
""",
    "fayllar": [
        "src/emekdaslar/toplu/dto/toplu.dto.ts",
        "src/emekdaslar/toplu/toplu.service.ts",
        "src/emekdaslar/toplu/toplu.controller.ts",
        "skriptler/toplu_yoxla.ts",
    ],
    "goster": ["src/emekdaslar/elaqeler/elaqeler.service.ts"],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then echo "  ✓ tip xətası yoxdur"; else echo "  ✗ tip xətası var"; fi

echo ""
echo "════ 2) Toplu modulu ════"
printf '      DTO qaydaları    : %s\n' "$(grep -c '@' src/emekdaslar/toplu/dto/toplu.dto.ts)"
printf '      servis sətirləri : %s\n' "$(wc -l < src/emekdaslar/toplu/toplu.service.ts | tr -d ' ')"
printf '      endpoint sayı    : %s\n' "$(grep -cE '@(Get|Post|Patch)' src/emekdaslar/toplu/toplu.controller.ts)"
echo "      ── vacib Prisma əməliyyatları ──"
for m in createManyAndReturn updateMany deleteMany multiply 'BadRequestException'; do
  printf '        %-22s %s\n' "$m" "$(grep -c "$m" src/emekdaslar/toplu/toplu.service.ts)"
done

echo ""
echo "════ 3) Nazik validasiya yoxlaması ════"
echo "      @ValidateNested({ each: true }) + @Type cütlüyü:"
grep -A2 '@ValidateNested' src/emekdaslar/toplu/dto/toplu.dto.ts | sed 's/^/        /'

echo ""
echo "════ 4) CANLI toplu əməliyyat yoxlaması ════"
npx tsx skriptler/toplu_yoxla.ts
""",
    "olmaz": """Atomiklik olmasa — dövr içində bir-bir yaratmaq:

const natamam = [];
for (const e of emekdaslar) {
  try {
    await prisma.emekdaslar.create({ data: e });
  } catch (x) {
    natamam.push(e.email);   // ← 25-ci sətirdə xəta
    break;
  }
}

Nəticə: 24 sətir bazada QALDI, 16 yazılmadı.

  ← ⚠️ İstifadəçi «40 müəllim əlavə etdim» düşünür.
     Əslində 24-ü əlavə olunub.
  ← ⚠️ Hansı 24? Cavab yoxdur. Siyahını yenidən
     yoxlamaq üçün Excel-i əl ilə müqayisə etmək
     lazımdır — 40 sətir üçün yarım saat.
  ← ⚠️ Yenidən cəhd etsəniz, İLK 24 SƏTİR TƏKRAR
     yazılacaq (əgər unikal sütun yoxdursa)!

────────────────────────────────────────────────────────────
multiply yerinə oxu-hesabla-yaz:

const setirler = await prisma.emekdaslar.findMany({ where });
for (const s of setirler) {
  const yeni = Number(s.maas) * 1.1;
  await prisma.emekdaslar.update({ where: { id: s.id },
                                   data: { maas: yeni } });
}

  ⏱  An 1:  A istifadəçisi oxuyur → maas = 3000
  ⏱  An 2:  B istifadəçisi oxuyur → maas = 3000
  ⏱  An 3:  A yazır → 3300
  ⏱  An 4:  B yazır → 3300   ← ⚠️ A-nın dəyişikliyi İTDİ!

  ← İki 10% artım tətbiq olunmalı idi (3630), amma
     nəticə 3300-dür. Bu, «lost update» problemidir.

────────────────────────────────────────────────────────────
Filtrsiz maaş artımı:

$ curl -X PATCH .../toplu/maas-artim -d '{"faiz":50}'

Filtr yoxdursa: BÜTÜN 14 əməkdaşın maaşı 50% artır.
Fondu: 33 000 → 49 500 AZN.

  ← ⚠️ Geri qaytarmaq üçün audit loqundan HƏR sətri
     fərdi şəkildə bərpa etmək lazımdır. Ay sonu
     hesabatı artıq səhv çıxıb.""",
    "c_izah": """
<p><strong>Birinci nəticə: bir sorğu, 3 sətir.</strong>
<code>createManyAndReturn</code> ilə 3 əməkdaş
<strong>1 SQL sorğusunda</strong> yaradıldı (ölçdük: 1 sorğu).
Dövr içində etsəydik 3 sorğu olardı — 14 sətirdə 14, 500 sətirdə 500.</p>
<p><strong>İkinci nəticə: atomiklik sübut olundu.</strong> Təkrar e-poçt
olan partiya <code>400</code> aldı və <strong>heç bir sətir
yazılmadı</strong> (3 → 3). Bu, <code>try/catch</code> ilə dövr
yazmağın <em>heç vaxt</em> verə bilməyəcəyi zəmanətdir.</p>
<p><strong>Üçüncüsü: <code>skipDuplicates</code> fərqi.</strong>
<code>false</code> ilə: 3 göndərdik, 0 yazıldı (xəta).
<code>true</code> ilə: 3 göndərdik, 2 yazıldı, 1 atlandı.
İkisi də düzgün davranışdır — sadəcə fərqli <em>niyyət</em> üçündür.</p>
<p><strong>Dördüncüsü: atomic multiply işləyir.</strong>
<code>updateMany</code> + <code>multiply: 1.1</code> ilə 5 sətirin maaşı
<em>dəqiq</em> 10% artdı. Yoxlama: hər sətir üçün
<code>yeni = köhnə × 1.1</code>. Sonra <code>divide: 1.1</code> ilə
<em>dəqiq</em> bərpa olundu.</p>
<p><strong>Beşincisi: FAİZ TƏLƏSİ canlı görüldü.</strong> +10% sonra
−10%: 3000 → 3300 → <strong>2970</strong>. 30 AZN itdi.
Bu, dərsin ən praktik tapıntısıdır: <em>«səhvən artırdım, geri
qaytarım»</em> sadəcə əks faiz yazmaqla <strong>mümkün deyil</strong>.
Düzgün yol: bölmək, ya da dəqiq qiymətləri yenidən yazmaq.</p>
<p><strong>Altıncısı: filtrsiz artım qadağandır.</strong>
<code>{"faiz": 50}</code> sorğusu <code>400</code> aldı və ümumi maaş
fondu <strong>dəyişmədi</strong> (42 009 = 42 009). Bu bir sətirlik
yoxlama, ay sonu fəlakətinin qarşısını alır.</p>
<p><strong>Yeddincisi: rollback audit loqunu da geri qaytarır.</strong>
<code>atomiklikYoxla()</code> 3 sətir yazmağa cəhd etdi, xəta atdı və
nəticədə <strong>bazada 0 sətir, audit loqunda 0 artım</strong>. Trigger
<code>AFTER INSERT</code> olsa da, <code>COMMIT</code> olmayanda onun
yazdığı sətir də yox olur.</p>
""",
    "sual": [
        ("<code>createMany</code> niyə sətirləri qaytarmır? Bu, Prisma-nın çatışmazlığı deyilmi?",
         "Qismən haqlısınız — bu, uzun müddət Prisma-nın məhdudiyyəti idi və <code>createManyAndReturn</code> məhz buna görə əlavə olundu. Səbəb: SQL-də <code>INSERT ... RETURNING</code> bütün bazalarda eyni cür işləmir (MySQL uzun müddət dəstəkləmirdi). Prisma əvvəlcə ən ümumi yolu seçdi. İndi PostgreSQL, SQLite və CockroachDB üçün <code>createManyAndReturn</code> var."),
        ("Niyə <code>createMany</code> Prisma <code>@default</code> dəyərlərini işlətmir?",
         "Bu, vacib fərqdir! Prisma-nın <strong>tətbiq</strong> səviyyəli standart dəyərləri (<code>@default(cuid())</code>, <code>@default(uuid())</code> kimi funksiyalar) <code>createMany</code>-də işləmir, çünki Prisma SQL-i <em>birbaşa</em> qurur və hər sətir üçün JavaScript funksiyası çağırmır. Amma <strong>baza</strong> səviyyəli standartlar (<code>@default(now())</code>, <code>@default(autoincrement())</code>) işləyir. Bizim sxemdə hamısı baza səviyyəsindədir — ona görə problem yoxdur."),
        ("<code>multiply: 1.1</code> dəqiq nəticə verirmi? Axı <code>1.1</code> ikilik sistemdə dəqiq deyil.",
         "Çox yaxşı sual! <code>1.1</code> JavaScript-də <em>təqribi</em> ədəddir. Amma hesablama <strong>SQL-də</strong> baş verir: PostgreSQL <code>numeric</code> tipi ilə işləyir və <code>numeric × numeric</code> dəqiqdir. JavaScript yalnız <code>1.1</code> ədədini SQL parametri kimi göndərir — orada o, <code>numeric</code>-ə çevrilir. Nəticə <code>Decimal(12,2)</code>-yə yuvarlaqlaşdırılır. Yoxladıq: 3000 × 1.1 = 3300.00 dəqiq."),
        ("<code>deleteMany</code> ilə təmizlik təhlükəli deyilmi? Səhv filtr bütün cədvəli silər.",
         "Bəli, <code>deleteMany</code> ən təhlükəli Prisma metodudur — filtrsiz çağırış bütün sətirləri silir. Ona görə biz onu yalnız <code>finally</code> blokunda və <strong>konkret prefikslə</strong> (<code>email: { startsWith: 'toplu.' }</code>) işlədirik. İstehsalat kodunda <code>deleteMany</code>-dən çəkinmək və ya onu «soft delete» ilə əvəz etmək lazımdır. Əlavə qoruma: <code>where</code> obyektinin boş olub-olmadığını yoxlayan köməkçi funksiya yazmaq."),
        ("50 sətir həddi niyə? Bəs 500 müəllim idxal etmək lazımdırsa?",
         "50 həddi <em>bir HTTP sorğusu</em> üçündür — cavab vaxtını və yaddaşı qoruyur. 500 sətir üçün <strong>hissə-hissə</strong> göndərmək lazımdır: frontend 50-lik paketlərə bölür və ardıcıl göndərir. Daha yaxşı həll: <em>asinxron idxal</em> — faylı yükləyirsiniz, server arxa planda emal edir və nəticəni bildirişlə göndərir. Bu, 2C/2D dərslərinin mövzusudur."),
        ("<code>@ValidateNested({ each: true })</code> olmasa nə olar?",
         "Massiv qəbul edilər, amma elementləri <strong>yoxlanılmaz</strong>. Yəni <code>{\"ad\":\"A\"}</code> kimi natamam sətir keçər və Prisma <code>P2012</code> (Required field missing) xətası verər — istifadəçi 500 görər. Ən pis hal: elementlər sadə obyekt qalar (sinif nüsxəsi olmaz), <code>@Type</code> çevrilmələri işləməz və <code>cinsiyyet_id: \"1\"</code> mətn kimi qalar."),
        ("Toplu əməliyyatı geri qaytarmaq (undo) mümkündürmü?",
         "Avtomatik yox. Variantlar: (1) <strong>audit loqu</strong> — oradan əvvəlki dəyərləri bərpa etmək (bizim trigger yalnız «nə vaxt, nə oldu» yazır, köhnə dəyəri yox — onu tətbiq səviyyəsində əlavə etmək lazımdır); (2) <strong>ehtiyat nüsxə</strong> əməliyyatdan əvvəl; (3) <strong>tranzaksiya + təsdiq</strong> — istifadəçi nəticəni görüb təsdiqləyənə qədər <code>COMMIT</code> etməmək. Praktikada ən çox işlədilən: əməliyyatdan əvvəl təsir olunacaq sətirləri <em>göstərmək</em> və təsdiq istəmək."),
        ("Bu endpoint-lər üçün <code>@UseGuards</code> lazım deyilmi? Hər kəs maaşı dəyişə bilər!",
         "Mütləq lazımdır — və bu, <strong>Dərs 3-ün</strong> mövzusudur. Hazırda heç bir autentifikasiya yoxdur, yəni API açıqdır. Real sistemdə: (1) JWT token tələb olunmalı; (2) toplu əməliyyatlar üçün <code>admin</code> rolu yoxlanmalı; (3) audit loquna <em>hansı istifadəçinin</em> etdiyi yazılmalı. Bizim audit servisi artıq <code>istifadeci</code> sahəsini dəstəkləyir — sadəcə hələ token oxumuruq."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>Toplu servis <strong>21 yoxlamadan</strong> keçdi.</li>
  <li><strong>Bir sorğu, N sətir:</strong> 3 əməkdaş
      <code>createManyAndReturn</code> ilə <strong>1 SQL
      sorğusunda</strong> yaradıldı.</li>
  <li><strong>Atomiklik sübut olundu:</strong> təkrar e-poçt olan partiya
      <code>400</code> aldı və bazaya <strong>heç nə</strong> yazılmadı.</li>
  <li><strong>skipDuplicates:</strong> 3 göndərildi → 2 yaradıldı,
      1 atlandı (və istifadəçiyə bildirildi).</li>
  <li><strong>Atomik multiply:</strong> <code>×1.1</code> →
      <code>÷1.1</code> ilə <em>dəqiq</em> bərpa.</li>
  <li><strong>FAİZ TƏLƏSİ canlı görüldü:</strong> +10% sonra −10%
      3000 → <strong>2970</strong>. 30 AZN itdi. Düzgün yol —
      <em>bölmək</em>.</li>
  <li><strong>Filtrsiz artım qadağandır:</strong> <code>400</code> və
      ümumi maaş fondu dəyişmədi.</li>
  <li><strong>ROLLBACK audit loqunu da geri qaytarır:</strong> 3 sətir
      cəhdi → bazada 0, audit artımı 0.</li>
  <li><strong>Baza toxunulmaz:</strong> 5 test sətri silindi,
      14 əməkdaş qaldı.</li>
</ul>
<p>Növbəti addımda <strong>audit loquna</strong> dərindən baxacağıq:
bazada artıq trigger var, onu oxuyacaq və tətbiq səviyyəsində necə
zənginləşdirməyi öyrənəcəyik.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 25 — AUDIT
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 25,
    "ad": "Audit loqu — baza trigger-i və tətbiq səviyyəsində izləmə",
    "a": """
<p>«Kim bu əməkdaşın maaşını dəyişdi?» — bu sualı cavablandıra bilmək,
ciddi ERP sistemini hobbi layihəsindən ayıran əsas xüsusiyyətdir.
Buna <strong>audit loqu</strong> (izləmə jurnalı) deyilir.</p>

<h4>Sürpriz: audit loqu ARTIQ işləyir!</h4>
<p>Baza dərslərində (Baza-1 / Baza-2) biz PostgreSQL-də trigger yazmışdıq.
O, <em>indi də oradadır</em> və işləyir:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
CREATE OR REPLACE FUNCTION audit.fn_audit_yaz()
 RETURNS trigger LANGUAGE plpgsql AS $function$
DECLARE v_setir_id TEXT;
BEGIN
    IF TG_OP = 'DELETE' THEN v_setir_id := OLD.id::TEXT;
    ELSE v_setir_id := NEW.id::TEXT; END IF;

    INSERT INTO audit.audit_log (cedvel_adi, emeliyyat, setir_id,
                                 istifadeci, qeyd)
    VALUES (TG_TABLE_SCHEMA || '.' || TG_TABLE_NAME, TG_OP, v_setir_id,
            current_user, 'Trigger ilə avtomatik qeyd');
    RETURN NULL;
END; $function$</pre>
<p>Və dörd cədvələ bağlanıb:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
kadrlar.emekdaslar        → trg_emekdaslar_audit       (INSERT/UPDATE/DELETE)
elm.tedqiqat_layiheleri   → trg_tedqiqat_layiheleri_audit
maliyye.budce             → trg_budce_audit
maliyye.satinalmalar      → trg_satinalmalar_audit</pre>
<p>Bazada <strong>5 400-dən çox</strong> audit qeydi var və onlar bizim
heç bir kod yazmadan yaranıb. Bu, <em>trigger yanaşmasının</em> gücüdür:
tətbiq səhv yazsa da, unutsa da, loq <strong>həmişə</strong> yazılır.</p>

<h4>Trigger nə BİLMİR?</h4>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Sual</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Trigger bilir?</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Nə üçün</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Hansı cədvəl, hansı əməliyyat?</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">✅ Bəli</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>TG_TABLE_NAME</code>, <code>TG_OP</code></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0">Hansı sətir (ID)?</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">✅ Bəli</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>NEW.id</code> / <code>OLD.id</code></td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Baza istifadəçisi?</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">✅ Bəli</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>current_user</code> = <code>arti_user</code></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0">Hansı <strong>API</strong> istifadəçisi?</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">❌ Xeyr</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Trigger HTTP başlıqlarını görmür</td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>NƏYİ</strong> dəyişdi (köhnə → yeni)?</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">❌ Xeyr</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Trigger yalnız «oldu» yazır, dəyərləri yox</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>NİYƏ</strong> dəyişdi?</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">❌ Xeyr</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Əmrin nömrəsi, səbəbi — tətbiq bilir</td>
  </tr>
</table>
<p>Yəni trigger <em>karkası</em> verir; <strong>konteksti</strong> tətbiq
əlavə etməlidir. Bu dərsdə hər ikisini birləşdiririk.</p>

<h4>Audit loqunun sxemi</h4>
<table style="width:100%;border-collapse:collapse;font-size:.88rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Sütun</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Tip</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Qeyd</th>
  </tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0"><code>id</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>bigint</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">⚠️ JSON-a çevrilmir — mətnə salınmalıdır</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0"><code>cedvel_adi</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>text</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">Sxem daxil: <code>kadrlar.emekdaslar</code></td></tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0"><code>emeliyyat</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>text</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>INSERT</code> / <code>UPDATE</code> / <code>DELETE</code></td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0"><code>setir_id</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>text</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>⚠️ MƏTN, bigint deyil!</strong></td></tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0"><code>istifadeci</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>text</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">Standart: <code>CURRENT_USER</code></td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0"><code>vaxt</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>timestamptz</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">Saat qurşağı ilə</td></tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0"><code>qeyd</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>text</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">Sərbəst mətn</td></tr>
</table>

<h4>⚠️ Niyə <code>setir_id</code> MƏTNDİR, <code>bigint</code> deyil?</h4>
<p>Loq <strong>müxtəlif cədvəllərdən</strong> gəlir. Onların açarları
fərqli tiplərdədir:</p>
<ul>
  <li><code>kadrlar.emekdaslar.id</code> → <code>bigint</code></li>
  <li><code>struktur.merkezler.id</code> → <code>integer</code></li>
  <li>Gələcəkdə əlavə olunacaq cədvəllərdə → <code>uuid</code> ola bilər</li>
</ul>
<p>Hamısını bir sütunda saxlamaq üçün <strong>ən ümumi tip</strong>
lazımdır — mətn. Bu, <em>şüurlu güzəşt</em>dir: tip təhlükəsizliyini
itiririk, amma universal loq qazanırıq.</p>
<p>⚠️ Praktik nəticə: loqdan sətri tapmaq üçün
<code>String(id)</code> işlətmək lazımdır, <code>BigInt(id)</code> yox.
Yanlış yazsaq heç nə tapılmaz — çünki <code>'6'</code> ilə
<code>6</code> fərqli dəyərlərdir.</p>

<h4>Trigger + tətbiq = tam mənzərə</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
async yaz(klient: Prisma.TransactionClient, melumat: AuditYazDto) {
  const setir = await klient.audit_log.create({
    data: {
      cedvel_adi: melumat.cedvel_adi,
      emeliyyat: melumat.emeliyyat,
      setir_id: melumat.setir_id ?? null,
      qeyd: melumat.qeyd ?? null,
      istifadeci: melumat.istifadeci ?? null,
    },
    select: { id: true },
  });
  return { id: String(setir.id) };
}</pre>
<p>⚠️ <strong>Niyə <code>klient</code> parametrdir?</strong> Çünki loq
<em>həmin tranzaksiyanın içində</em> yazılmalıdır. Əgər ayrıca
<code>this.prisma</code> işlətsəydik, iki problem yaranardı:</p>
<ol>
  <li>Məlumat dəyişikliyi geri qaytarılsa, <strong>loq qalar</strong> —
      yalançı qeyd.</li>
  <li>Loq yazıla bilməsə, məlumat dəyişikliyi <em>yenə də</em> commit
      olunar — audit boşluğu.</li>
</ol>
<p><code>Prisma.TransactionClient</code> tipi məhz tranzaksiya daxilindəki
klienti bildirir və o, <code>$transaction</code>, <code>$connect</code>
kimi metodları <em>ehtiva etmir</em> — yəni tranzaksiya içində yeni
tranzaksiya başlatmaq mümkün deyil. Bu, <strong>tip səviyyəsində
qorumadır</strong>.</p>

<h4>⚠️ ŞƏXSİ MƏLUMAT (PII) audit loqunda</h4>
<p>Audit loqu <em>uzun müddət</em> saxlanılır və çox vaxt geniş oxucu
dairəsi olur (təhlükəsizlik, audit, rəhbərlik). Ona görə buraya
<strong>şəxsi məlumat yazmaq olmaz</strong>:</p>
<table style="width:100%;border-collapse:collapse;font-size:.88rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">❌ YAZMAYIN</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">✅ YAZIN</th>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0">«Maaş 3500 → 3850»</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">«Maaş sahəsi dəyişdirildi (əməkdaş ID 1)»</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0">«Parol: abc123»</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">«Parol yeniləndi»</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0">«FIN kod: 5AB12CD»</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">«Şəxsi məlumat yeniləndi»</td>
  </tr>
</table>
<p>Niyə? Çünki loq <em>silinmir</em> və loqdan məlumat sızması,
əsas cədvəldən sızmaqdan qat-qat təhlükəlidir — orada
<strong>tarixçə</strong> var.</p>

<h4>Loqun paylanması: <code>groupBy</code> yenidən</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
await this.prisma.audit_log.groupBy({
  by: ['cedvel_adi', 'emeliyyat'],
  _count: { _all: true },
});</pre>
<p>⚠️ İki sütun üzrə qruplaşdırma <em>kəsişmə</em> verir:
hər cədvəl × hər əməliyyat üçün bir sətir. Frontend üçün əlverişli
formaya salmaq lazımdır — biz <code>Map</code> ilə cədvəl üzrə
yığırıq və INSERT/UPDATE/DELETE saylarını ayrı sütunlara paylayırıq.</p>
""",
    "anlayis": [
        ("Audit loqu",
         "«Kim, nə vaxt, nəyi etdi» jurnalı. Dəyişməz (append-only) "
         "olmalıdır — qeydlər silinmir."),
        ("Trigger",
         "Bazada müəyyən hadisə (INSERT/UPDATE/DELETE) baş verəndə "
         "<em>avtomatik</em> işləyən funksiya."),
        ("AFTER INSERT trigger",
         "<code>AFTER</code> — əməliyyatdan SONRA işləyir. "
         "<code>BEFORE</code> isə məlumatı dəyişə bilər (məsələn "
         "<code>gun_sayi</code> hesablanması)."),
        ("TG_OP / TG_TABLE_NAME",
         "Trigger daxilində mövcud xüsusi dəyişənlər: əməliyyat növü və "
         "cədvəl adı."),
        ("current_user",
         "PostgreSQL-in <em>baza</em> səviyyəli istifadəçisi "
         "(<code>arti_user</code>). API istifadəçisi deyil!"),
        ("TransactionClient",
         "Tranzaksiya daxilindəki Prisma klienti. "
         "<code>$transaction</code> metodunu ehtiva etmir — yəni iç-içə "
         "tranzaksiya mümkün deyil."),
        ("PII",
         "Personally Identifiable Information — şəxsi məlumat. Audit "
         "loqunda <em>olmamalıdır</em>."),
        ("Append-only",
         "Yalnız əlavə oluna bilən. Silmə və dəyişmə qadağandır — "
         "əks halda izləmə mənasını itirir."),
        ("Rollback",
         "Tranzaksiyanı geri qaytarmaq. Trigger-in yazdığı sətir də geri "
         "qaytarılır, çünki o, həmin tranzaksiyanın bir hissəsidir."),
        ("groupBy iki sütun üzrə",
         "<code>by: ['a', 'b']</code> → <code>GROUP BY a, b</code>. "
         "Hər kombinasiya üçün bir sətir."),
        ("Kontekst zənginləşdirməsi",
         "Trigger-in bilmədiyi məlumatı (API istifadəçisi, səbəb, IP) "
         "tətbiq səviyyəsində əlavə etmək."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) <code>hazirla()</code> — BigInt və mətn sütunu</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
function hazirla(e: { id: bigint; ... }): AuditCavabi {
  return {
    id: String(e.id),          // ← BigInt → mətn (mütləq!)
    cedvel_adi: e.cedvel_adi,
    emeliyyat: e.emeliyyat,
    setir_id: e.setir_id,      // ← ARTIQ mətndir, çevirmək lazım deyil
    istifadeci: e.istifadeci,
    vaxt: e.vaxt.toISOString(),
    qeyd: e.qeyd,
  };
}</pre>
<p>⚠️ Diqqət: <code>id</code> üçün <code>String()</code> lazımdır, amma
<code>setir_id</code> üçün <em>yox</em> — o, bazada artıq
<code>text</code>-dir. Bu asimmetriya qarışıqlıq yarada bilər, amma
səbəbi yuxarıda izah olunub (müxtəlif cədvəllərin müxtəlif açar
tipləri).</p>

<h5 style="color:#334155;margin-top:1rem">2) <code>hamisi()</code> — üç filtri birləşdirmək</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const where: Prisma.audit_logWhereInput = {};
if (sorgu.cedvel) where.cedvel_adi = { contains: sorgu.cedvel, mode: 'insensitive' };
if (sorgu.emeliyyat) where.emeliyyat = sorgu.emeliyyat;
if (sorgu.axtar) {
  where.OR = [
    { qeyd: { contains: sorgu.axtar, mode: 'insensitive' } },
    { setir_id: { contains: sorgu.axtar, mode: 'insensitive' } },
    { istifadeci: { contains: sorgu.axtar, mode: 'insensitive' } },
  ];
}</pre>
<ul>
  <li><code>cedvel</code> üçün <code>contains</code> — istifadəçi
      <code>emekdaslar</code> yazsa da tapılsın (tam adı
      <code>kadrlar.emekdaslar</code>-dır).</li>
  <li><code>emeliyyat</code> üçün isə <em>dəqiq</em> uyğunluq —
      DTO-da <code>@IsIn</code> ilə məhdudlaşdırılıb.</li>
  <li><code>axtar</code> üç sütunda <code>OR</code> ilə axtarır.</li>
  <li>⚠️ <code>orderBy: { id: 'desc' }</code> — ən yeni qeyd yuxarıda.
      <code>vaxt</code> üzrə sıralamaq da olar, amma <code>id</code>
      <em>monoton artandır</em> və indekslənmişdir (birincil açar) —
      daha sürətlidir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3) <code>statistika()</code> — iki sütunlu groupBy-ni yığmaq</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const xerite = new Map&lt;string, {...}&gt;();

for (const q of cedvelUzre) {
  const m = xerite.get(q.cedvel_adi) ??
    { cedvel_adi: q.cedvel_adi, cem: 0, insert: 0, update: 0, delete: 0 };
  const say = q._count._all;
  m.cem += say;
  if (q.emeliyyat === 'INSERT') m.insert += say;
  else if (q.emeliyyat === 'UPDATE') m.update += say;
  else if (q.emeliyyat === 'DELETE') m.delete += say;
  xerite.set(q.cedvel_adi, m);
}</pre>
<ul>
  <li>⚠️ <code>xerite.get(...) ?? {...}</code> — <strong>yeni obyekt
      yaradılır</strong>, sonra dəyişdirilir və yenidən <code>set</code>
      olunur. Map-də <em>obyektin özünü</em> dəyişmək də işləyər
      (referans saxlanılır), amma yeni obyekt yaratmaq
      funksional üsluba daha yaxındır.</li>
  <li><code>else if</code> zənciri — digər əməliyyat növləri
      (<code>POST</code>, <code>PATCH</code> kimi tətbiq səviyyəli
      qeydlər) cəmə düşür, amma üç əsas sütuna yox.</li>
  <li><code>.sort((a, b) =&gt; b.cem - a.cem)</code> — ən çox qeyd olan
      cədvəl yuxarıda.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">4) <code>tranzaksiyaNumayisi()</code> — atomikliyin sübutu</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
await this.prisma.$transaction(async (tx) => {
  const e = await tx.emekdaslar.create({ data: {...}, select: { id: true } });

  const a = await this.yaz(tx, {                 // ← AYNI tranzaksiya!
    cedvel_adi: 'kadrlar.emekdaslar',
    emeliyyat: 'INSERT',
    setir_id: String(e.id),
    istifadeci: 'api@arti.edu.az',
    qeyd: 'Nümayiş: əməkdaş yaradıldı (tranzaksiya sınağı)',
  });
  auditId = a.id;

  throw new Error('QƏSDƏN XƏTA: hər ikisi geri qaytarılmalıdır');
});</pre>
<ul>
  <li><code>tx</code> — tranzaksiya klienti. Həm <code>emekdaslar.create</code>,
      həm <code>audit_log.create</code> onunla gedir.</li>
  <li><code>this.yaz(tx, ...)</code> — servis metodu klienti
      <em>parametr</em> kimi qəbul edir. Bu, dizayn qərarıdır: metod
      «harada yazacağını» bilmir, çağıran qərar verir.</li>
  <li><code>throw</code> — tranzaksiyanı ləğv edir. Nəticə:
      <strong>nə əməkdaş, nə audit qeydi</strong>.</li>
  <li><code>auditId</code> dəyişəni <em>xaricdə</em> saxlanılır — çünki
      tranzaksiya içində yaranan ID-ni sübut kimi göstərmək istəyirik
      («ID alındı, amma bazada yoxdur»).</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">5) <code>triggerNumayisi()</code> — trigger-in sübutu</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const evvel = await this.prisma.audit_log.count();

const e = await this.prisma.emekdaslar.create({ data: {...}, select: { id: true } });
await this.prisma.emekdaslar.update({ where: { id: e.id }, data: { maas: 2000 } });
await this.prisma.emekdaslar.delete({ where: { id: e.id } });

const sonra = await this.prisma.audit_log.count();
// sonra - evvel === 3   ← INSERT + UPDATE + DELETE</pre>
<p>⚠️ Bu metod <strong>heç bir audit kodu yazmır</strong> — loq
tamamı trigger tərəfindən yaranır. Bu, sübutun ən güclü formasıdır.</p>
<p>⚠️ <strong>Qeyd:</strong> bu 3 audit sətri bazada <em>qalır</em> —
audit loqu əbədidir və onu silmirik. Bu, dərsin
<em>şüurlu</em> nəticəsidir.</p>

<h5 style="color:#334155;margin-top:1rem">6) <code>audit.controller.ts</code> — marşrut sırası</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Get()                    hamisi()
@Get('statistika')        statistika()
@Get('trigger-numayisi')  triggerNumayisi()
@Get('tranzaksiya-numayisi') tranzaksiyaNumayisi()
@Post()                   yaz()
@Get(':id')               biri()          ← ƏN SONDA!
</pre>
<p>Bu dəfə toqquşma <em>eyni controllerin</em> içindədir: «statistika»
və «:id» hər ikisi 1 seqmentdir. Sıra səhv olsa, <code>statistika</code>
400 qaytarar. Faydalı vərdiş: <strong><code>:id</code>-ni faylın ən
sonuna qoyun</strong>.</p>
""",
    "fayllar": [
        "src/audit/dto/audit-sorgu.dto.ts",
        "src/audit/audit.service.ts",
        "src/audit/audit.controller.ts",
        "src/audit/audit.module.ts",
        "skriptler/audit_yoxla.ts",
    ],
    "goster": ["src/emekdaslar/toplu/toplu.service.ts"],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then echo "  ✓ tip xətası yoxdur"; else echo "  ✗ tip xətası var"; fi

echo ""
echo "════ 2) Audit modulu ════"
wc -l src/audit/*.ts src/audit/dto/*.ts | sed 's/^/      /'
printf '      endpoint sayı : %s\n' "$(grep -cE '@(Get|Post)' src/audit/audit.controller.ts)"
echo "      ── marşrut sırası ──"
grep -nE "@(Get|Post)\(" src/audit/audit.controller.ts | sed 's/^/        /'

echo ""
echo "════ 3) Bazadaki trigger-lər ════"
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
psql "$DBURL" -At -c "
SELECT '      ' || event_object_schema || '.' || event_object_table
       || ' → ' || trigger_name
  FROM information_schema.triggers
 WHERE trigger_schema NOT IN ('pg_catalog','information_schema')
 GROUP BY 1, event_object_schema, event_object_table, trigger_name
 ORDER BY 1;" 2>/dev/null

echo ""
echo "════ 4) Audit loqunun həcmi ════"
psql "$DBURL" -At -c "
SELECT '      cəmi qeyd   : ' || count(*) FROM audit.audit_log;
SELECT '      cədvəl sayı : ' || count(DISTINCT cedvel_adi) FROM audit.audit_log;" 2>/dev/null
psql "$DBURL" -c "
SELECT cedvel_adi, emeliyyat, count(*) AS say
  FROM audit.audit_log GROUP BY cedvel_adi, emeliyyat
 ORDER BY say DESC LIMIT 6;" 2>/dev/null | sed 's/^/      /'

echo ""
echo "════ 5) CANLI audit yoxlaması ════"
npx tsx skriptler/audit_yoxla.ts
""",
    "olmaz": """Audit loqu olmasa:

$ curl -X PATCH .../emekdaslar/1 -d '{"maas":99999}'
{"id":"1", ... "maas":"99999.00"}

  ← ✅ Sorğu uğurlu. Heç bir xəta yoxdur.

Bir həftə sonra mühasib soruşur:
  «Direktorun maaşı niyə 3 500 yerinə 99 999 görünür?»

$ # Kim dəyişdi?
$ # Nə vaxt?
$ # Nədən?
$ # Nə idi əvvəl?

  ← ⚠️ HEÇ BİR CAVAB YOXDUR. Məlumat itib.
     Geri qaytarmaq üçün ehtiyat nüsxədən bərpa
     lazımdır — və həmin həftənin BÜTÜN digər
     dəyişiklikləri də itəcək.

────────────────────────────────────────────────────────────
Yalnız trigger olsa, tətbiq loqu olmasa:

$ psql -c "SELECT * FROM audit.audit_log
            WHERE cedvel_adi='kadrlar.emekdaslar'
            ORDER BY id DESC LIMIT 1"

 id    | 5503
 cedvel| kadrlar.emekdaslar
 emeliy| UPDATE
 setir | 1
 istif | arti_user            ← ⚠️ BAZA istifadəçisi
 vaxt  | 2026-09-24 11:43:58
 qeyd  | Trigger ilə avtomatik qeyd

  ← ⚠️ «arti_user» — bu, API-nin bazaya qoşulduğu
     texniki istifadəçidir. 50 nəfər eyni adla
     görünür. «KİM dəyişdi?» sualı cavabsız qalır.
  ← ⚠️ «NƏYİ dəyişdi?» də yoxdur — yalnız «UPDATE oldu».

────────────────────────────────────────────────────────────
Audit loquna şəxsi məlumat yazsaq:

INSERT INTO audit.audit_log (..., qeyd) VALUES
  (..., 'Maaş 3500 → 99999, FIN 5AB12CD, parol abc123');

  ← ⚠️ Loq SİLİNMİR və çox vaxt geniş oxucu dairəsi
     var. Bir sızma halında bütün maaş TARİXÇƏSİ,
     bütün parollar, bütün FIN kodları ələ keçər.
     Əsas cədvəldən sızmaq isə yalnız CARİ
     vəziyyəti verər — tarixçəni yox.""",
    "c_izah": """
<p><strong>Birinci nəticə: trigger HƏQİQƏTƏN işləyir.</strong>
<code>triggerNumayisi()</code> üç əməliyyat etdi (yarat, dəyiş, sil) və
audit loqu <strong>dəqiq 3 qeyd</strong> artdı —
<code>INSERT</code>, <code>UPDATE</code>, <code>DELETE</code>. Biz heç
bir audit kodu yazmadıq; hamısı bazada baş verdi.</p>
<p><strong>İkincisi: istifadəçi məlumatı bazadan gəlir.</strong>
Qeydlərdə <code>arti_user</code> görünür — bu,
<code>current_user</code> dəyəridir. Yəni trigger <em>baza
səviyyəsini</em> bilir, amma API səviyyəsini bilmir. Bu boşluğu
tətbiq doldurur.</p>
<p><strong>Üçüncüsü: <code>setir_id</code> mətn kimi saxlanılır.</strong>
Yoxladıq: <code>typeof qeydler[0].setir_id === 'string'</code>. Bu,
loqun universal olmasını təmin edir — gələcəkdə <code>uuid</code>
açarlı cədvəllər də əlavə oluna bilər.</p>
<p><strong>Dördüncüsü: atomiklik audit üçün də keçərlidir.</strong>
<code>tranzaksiyaNumayisi()</code> əməkdaş + audit qeydini bir
tranzaksiyada yazdı, sonra xəta atdı. Nəticə: <strong>bazada 0
əməkdaş, audit artımı 0</strong>. Üstəlik skript yoxladı ki, alınan
audit ID-si bazada <em>həqiqətən yoxdur</em>.</p>
<p><strong>Beşincisi: əl ilə yazma işləyir.</strong>
<code>yazTek()</code> ilə <code>skript@arti.edu.az</code> istifadəçisi
adına qeyd yazdıq və onu oxuduq. Yəni API istifadəçisini loqa
<strong>özümüz</strong> yaza bilirik — Dərs 3-də JWT tokenindən
oxuyacağıq.</p>
<p><strong>Altıncısı: loqun həcmi böyükdür.</strong> 5 400-dən çox
qeyd, 25 müxtəlif cədvəl. Ən çoxu <code>auth.login</code>
(<code>POST</code>, 2 300+) və <code>struktur.merkezler</code>.
Bu, real istifadəni göstərir — loq <em>boş</em> deyil, həqiqi
sistemin izidir.</p>
""",
    "sual": [
        ("Audit loqunu tətbiqdə yazsaq, trigger lazım deyilmi?",
         "<strong>İkisi də lazımdır</strong> və fərqli işlər görürlər. Trigger <em>təminatdır</em>: tətbiq səhv yazsa, unutsa, kimsə birbaşa SQL ilə dəyişsə belə, loq yazılır. Tətbiq loqu isə <em>kontekst</em> verir: hansı API istifadəçisi, nə üçün. Trigger-i söndürüb yalnız tətbiq loquna güvənsək, kimsə <code>psql</code> ilə əl ilə dəyişsə heç bir iz qalmaz."),
        ("Audit loqu özü də audit olunmalıdırmı? Yəni loqu kim dəyişdi?",
         "Nəzəri olaraq bəli (buna «audit the auditor» deyilir), praktikada isə həddindən artıq mürəkkəbləşir. Real həllər: (1) loq cədvəlinə <code>UPDATE</code>/<code>DELETE</code> hüququnu <em>heç kimə</em> verməmək (yalnız <code>INSERT</code> və <code>SELECT</code>); (2) loqu ayrıca bazaya və ya yazıla-bilməyən saxlanc yerbəyə (WORM storage) köçürmək; (3) müntəzəm hash zənciri (blokçeyn üsulu) saxlamaq. Bizim halda trigger yalnız <code>INSERT</code> edir — bu, ilk addımdır."),
        ("<code>istifadeci</code> sahəsinə <code>CURRENT_USER</code> yazmaq düzgündürmü? Hər kəs <code>arti_user</code>-dir.",
         "Bu, trigger-in <em>təbii</em> məhdudiyyətidir, səhv deyil. Trigger yalnız baza bağlantısının istifadəçisini bilir. Real sistemlərdə <code>SET LOCAL app.istifadeci = 'ali@arti.edu.az'</code> kimi <em>sessiya dəyişəni</em> qoyulur və trigger onu oxuyur: <code>current_setting('app.istifadeci', true)</code>. Bu, gözəl həlldir, amma trigger funksiyasını dəyişmək tələb edir — 2C dərsinin mövzusu."),
        ("Audit loqunu nə qədər saxlamaq lazımdır?",
         "Asılıdır: (1) <strong>təhlükəsizlik</strong> loqu (giriş cəhdləri) — 90 gün adətən kifayətdir; (2) <strong>maliyyə</strong> loqu — vergi qanunvericiliyi tələb edir (Azərbaycanda 5 il); (3) <strong>kadr</strong> loqu — işçinin iş müddəti + 5 il. Praktik həll: loqu <em>partiyalarla</em> arxivləşdirmək — 1 ildən köhnə qeydləri ayrıca cədvələ (və ya fayla) köçürmək. Bizim <code>audit_log</code> hələ kiçikdir (5 400 sətir, 872 KB), amma böyüyəcək."),
        ("<code>groupBy</code> iki sütun üzrə — niyə birbaşa istifadə etmirik?",
         "Nəticə <em>kəsişmə</em> formatındadır: <code>{cedvel_adi, emeliyyat, _count}</code>. Frontend üçün isə əlverişli forma sətir-cədvəldir: hər cədvəl bir sətir, INSERT/UPDATE/DELETE ayrı sütunlar. Ona görə <code>Map</code> ilə yığırıq. Alternativ: SQL-də <code>FILTER</code> və ya <code>crosstab</code> işlətmək — daha sürətli olardı, amma <code>$queryRaw</code> tələb edir. 5 400 sətirdə yaddaşda yığmaq tamamilə məqbuldur."),
        ("Audit loqunda <code>vaxt</code> niyə <code>timestamptz</code>-dir, <code>timestamp</code> deyil?",
         "<strong>Çox vacib fərq!</strong> <code>timestamp</code> saat qurşağı məlumatını saxlamır — yalnız «rəqəmsal» vaxtı. <code>timestamptz</code> isə dəyəri UTC-də saxlayır və oxuyanda yerli vaxta çevirir. Audit üçün <code>timestamptz</code> <em>mütləqdir</em>: server başqa ölkəyə köçsə və ya yay/qış vaxtı dəyişsə, loqun düzgün oxunması bundan asılıdır. Bizim sxemdə <code>@db.Timestamptz(6)</code> yazılıb."),
        ("Trigger-i söndürmək (disable) olarmı? Test üçün lazım olsa.",
         "Olar: <code>ALTER TABLE kadrlar.emekdaslar DISABLE TRIGGER trg_emekdaslar_audit;</code>. Amma <strong>təhlükəlidir</strong> — söndürməyi unutsanız, loq sükutla işləməyi dayandırar və bunu <em>heç vaxt</em> bilməyəcəksiniz. Testlərdə belə etmək əvəzinə, test məlumatını ayrı prefikslə yaradıb sonra <em>silə</em> bilərsiniz — audit qeydləri qalar, bu normaldır. Əgər mütləq lazımdırsa, söndürməni <code>try/finally</code> ilə sarın."),
        ("Bu loqu frontend-də necə göstərmək lazımdır?",
         "Tipik dizayn: cədvəl görünüşü — tarix, istifadəçi, cədvəl, əməliyyat, sətir ID. Filtirlər: tarix aralığı, cədvəl, əməliyyat növü, istifadəçi. Ən vacib detallar: (1) <strong>səhifələmə</strong> — mütləqdir (5 400 qeyd); (2) <strong>sıralama</strong> — ən yeni yuxarıda; (3) <strong>detallar paneli</strong> — sətirə klikləyəndə tam qeyd; (4) <strong>ixrac</strong> — CSV/Excel (Dərs 4). Bizim API bütün bunları dəstəkləyir."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>Audit servisi <strong>28 yoxlamadan</strong> keçdi.</li>
  <li><strong>Loq artıq mövcuddur:</strong> 25 cədvəl üzrə minlərlə
      qeyd, heç bir audit kodu yazmadan — baza trigger-i sayəsində.</li>
  <li><strong>Trigger sübut olundu:</strong> 3 əməliyyat (yarat, dəyiş,
      sil) → <strong>dəqiq 3 audit qeydi</strong>
      (<code>INSERT</code>, <code>UPDATE</code>, <code>DELETE</code>).</li>
  <li><strong>Baza istifadəçisi avtomatik yazılır:</strong>
      <code>current_user</code> = <code>arti_user</code>.</li>
  <li><strong><code>setir_id</code> mətndir</strong> — müxtəlif açar
      tiplərini birləşdirmək üçün şüurlu güzəşt.</li>
  <li><strong>Tətbiq səviyyəsində yazma işləyir:</strong> API
      istifadəçisi (<code>skript@arti.edu.az</code>) loqa yazıldı və
      oxundu.</li>
  <li><strong>Atomiklik audit üçün də keçərlidir:</strong> əməkdaş +
      audit bir tranzaksiyada; xəta → <strong>heç biri qalmadı</strong>.</li>
  <li><strong>Baza toxunulmaz:</strong> 14 əməkdaş, test zibili 0.
      ⚠️ Audit loqu isə <em>artdı</em> — bu, gözlənilən və
      <em>düzgün</em> davranışdır (loq əbədidir).</li>
</ul>
<p>Son addımda hər şeyi <strong>birləşdirəcəyik</strong>: modul qrafı,
marşrut sırası, optimallaşdırma və tam canlı yoxlama.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 26 — OPTİMALLAŞDIRMA, MARŞRUT SIRASI VƏ YEKUN
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 26,
    "ad": "Optimallaşdırma, marşrut sırası və yekun qoşulma",
    "a": """
<p>Dörd modul yazdıq: statistika, əlaqələr, toplu, audit. Amma onlar
<em>tətbiqə qoşulmayıb</em> — yəni endpoint-lər işləmir. Bu addımda
hər şeyi birləşdiririk və dərsin ən incə mövzusunu —
<strong>marşrut sırası</strong>nı canlı sübut edirik.</p>

<h4>Modul qrafı — Nest-də hər şey AÇIQ olmalıdır</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
AppModule
├── ConfigModule     (qlobal — .env oxuyur)
├── PrismaModule     (@Global — baza bağlantısı)
├── SaglamliqModule  (1A)
├── EmekdaslarModule (2A + 2B)
└── AuditModule      (2B)</pre>
<p>⚠️ <strong>Nest modulları avtomatik tapmır.</strong> Fayl
<code>src/</code> qovluğunda olsa da, <code>imports</code>-a əlavə
olunmasa <em>heç vaxt yüklənməyəcək</em>. Və ən pisi: heç bir xəta
çıxmır — sadəcə endpoint-lər <code>404</code> qaytarır. Yeganə
diaqnostika aləti serverin başlanğıc logundaki <strong>marşrut
cədvəli</strong>dir.</p>

<h4>⚠️⚠️ MARŞRUT SIRASI — dərsin ən məkrli tələsi</h4>
<p>Dörd controller <code>emekdaslar</code> prefiksini paylaşır. Onların
yollarına baxaq:</p>
<table style="width:100%;border-collapse:collapse;font-size:.88rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Controller</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Nümunə yol</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Seqment</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Toqquşur?</th>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>StatistikaController</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/statistika</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">2</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">⚠️ <strong>BƏLİ</strong></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>ElaqelerController</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/:id/icmal</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">3</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">✅ Xeyr</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>TopluController</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/toplu/yarat</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">3</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">✅ Xeyr</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>EmekdaslarController</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/:id</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">2</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">⚠️ <strong>BƏLİ</strong></td>
  </tr>
</table>
<p>Express marşrutları <strong>ELAN SIRASI</strong> ilə yoxlayır — birinci
uyğun gələn qalib gəlir. Əgər <code>EmekdaslarController</code> əvvəl
gəlsəydi:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
GET /api/v1/emekdaslar/statistika
  → @Get(':id') uyğun gəlir («statistika» = :id)
  → ParseIntPipe «statistika» sözünü ədədə çevirə bilmir
  → HTTP 400 Validation failed (numeric string is expected)

⚠️ Statistika endpointi HEÇ VAXT çağırılmır.
⚠️ Heç bir xəta mesajı səbəbi DEMİR.
⚠️ /emekdaslar/5 İŞLƏYİR — problem sükutla gizlənir.</pre>
<p><strong>Həll:</strong> <code>controllers</code> massivində
<code>:id</code> olan controller-i <strong>ƏN SONA</strong> qoyun.</p>

<h4>⚠️ Niyyə saxlayın: alt modul KİFAYƏT ETMİR</h4>
<p>İlk cəhddə biz <code>StatistikaModule</code>-u ayrı modul kimi yazıb
<code>imports</code>-a əlavə etdik — məntiqli görünürdü. Nəticə:
<strong>yenə 400</strong>. Səbəb: Nest <em>əvvəlcə modulun ÖZ
controller-lərini, sonra import olunanlarınkını</em> qeydiyyatdan
keçirir. Yəni <code>:id</code> yenə qabağa düşür.</p>
<p>Çıxış yolu: bütün controller-ləri <strong>BİR</strong> modulun
<code>controllers</code> massivində, <em>açıq</em> sıra ilə yazmaq.</p>

<h4>⚠️ Express 5 — <code>:id([0-9]+)</code> artıq İŞLƏMİR</h4>
<p>Express 4-də məşhur bir həll var idi: marşrut parametrini
<em>regex</em> ilə məhdudlaşdırmaq:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
@Get(':id([0-9]+)')       // ⚠️ Express 4-də işləyirdi
→ PathError: Unexpected ( at index 22</pre>
<p>Express 5 <code>path-to-regexp</code> 8-i işlədir və bu,
<em>inline regex</em>-i <strong>dəstəkləmir</strong>. Ona görə yeganə
etibarlı həll <strong>sıra qaydası</strong>dır. Bu, 2025-ci ildə
Express 5-ə keçidlə yaranan geniş yayılmış problemdir.</p>

<h4>Optimallaşdırma: <code>EXPLAIN ANALYZE</code></h4>
<p>PostgreSQL-in sorğu planını görmək üçün:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF, SUMMARY OFF)
SELECT count(*) FROM audit.audit_log
 WHERE cedvel_adi = 'kadrlar.emekdaslar';</pre>
<p>Nəticə iki növdən biri olur:</p>
<table style="width:100%;border-collapse:collapse;font-size:.88rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Plan</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Mənası</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Yaxşı/pis</th>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>Seq Scan</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Bütün cədvəl başdan-başa oxunur</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Kiçik cədvəldə yaxşı,
        böyükdə pis</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>Index Scan</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">İndeksdən istifadə edilir</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Yaxşı — az sətir oxunur</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>Index Only Scan</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Yalnız indeks oxunur —
        cədvələ heç baxılmır</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Ən yaxşı</td>
  </tr>
</table>
<p>⚠️ <strong>Ən vacib müşahidə: indeksin olması onun
İŞLƏDİLƏCƏYİ demək deyil.</strong> Planlaşdırıcı (planner) qərar verir
və o, <em>statistikaya</em> əsaslanır. Kiçik cədvəldə
<code>Seq Scan</code> <strong>daha sürətlidir</strong> — çünki indeksə
baxmaq, sonra cədvələ qayıtmaq əlavə işdir.</p>

<h4>Nə vaxt indeks işlədilmir?</h4>
<ol>
  <li><strong>Cədvəl kiçikdirsə.</strong> 14 sətir üçün
      <code>Seq Scan</code> həmişə daha sürətlidir.</li>
  <li><strong>Seçicilik aşağıdırsa.</strong> Sorğu sətirlərin 14%-ni
      qaytarırsa, indeksdən keçmək faydasızdır — cədvəli başdan-başa
      oxumaq daha yaxşıdır.</li>
  <li><strong><code>ILIKE '%mətn%'</code>.</strong> B-ağacı indeksi
      yalnız <em>soldan</em> uyğunluqda kömək edir. <code>%</code> ilə
      başlayan axtarış <strong>heç vaxt</strong> indeks işlətmir.</li>
  <li><strong>Funksiya tətbiq olunubsa.</strong>
      <code>WHERE lower(ad) = 'elnur'</code> — indeks <code>lower(ad)</code>
      üzrə yaradılmayıbsa, işlədilmir.</li>
</ol>

<h4>Nə etmək lazımdır?</h4>
<table style="width:100%;border-collapse:collapse;font-size:.88rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Problem</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Həll</th>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Tam mətn axtarışı yavaşdır</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>pg_trgm</code> genişlənməsi +
        <code>GIN</code> indeksi, ya da <code>to_tsvector</code> (FTS)</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0">Statistika köhnəlib</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>ANALYZE</code> işlədin
        (planner statistikasını yeniləyir)</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Çox sorğu gedir (N+1)</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>_count</code>,
        <code>groupBy</code>, <code>Promise.all</code> (ADDIM 23)</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0">Hesabat hər dəfə yenidən
        hesablanır</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Keş (Redis) və ya
        <em>materialized view</em></td>
  </tr>
</table>

<h4>⚠️ <code>tsx</code> Nest tətbiqini işlədə BİLMİR</h4>
<p>Bu, dərsin praktik tapıntısıdır. <code>npx tsx</code> Nest tətbiqini
qaldırmağa çalışsaq:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
TypeError: Cannot read properties of undefined (reading 'biri')
    at EmekdaslarController.biri</pre>
<p>Səbəb: <code>tsx</code> <em>esbuild</em> işlədir və esbuild
<code>emitDecoratorMetadata</code>-nı <strong>dəstəkləmir</strong>.
Nest konstruktor parametrlərinin tiplerini məhz bu metadatanı oxuyaraq
öyrənir. Metadata olmayanda DI işləmir və <code>this.xidmet</code>
<code>undefined</code> olur.</p>
<p><strong>Nəticə:</strong> Nest tətbiqini <em>həmişə</em>
<code>dist/</code>-dən işlədin (<code>node dist/main.js</code>).
<code>tsx</code> isə <strong>servis səviyyəsindəki</strong> testlər üçün
əladır — orada servisləri <em>əl ilə</em> yaradırıq.</p>
""",
    "anlayis": [
        ("Modul qrafı",
         "Nest tətbiqinin modul ağacı. Hər modul <code>imports</code> ilə "
         "açıq şəkildə qoşulur."),
        ("Marşrut sırası",
         "Express marşrutları <em>elan sırası</em> ilə yoxlayır. Birinci "
         "uyğun gələn qalib gəlir."),
        ("`:id` toqquşması",
         "Ümumi parametr (`:id`) konkret yolla toqquşur, əgər əvvəl "
         "elan olunubsa."),
        ("EXPLAIN ANALYZE",
         "Sorğunu HƏQİQƏTƏN işlədir və planı faktiki rəqəmlərlə göstərir. "
         "<code>EXPLAIN</code> isə yalnız planı təxmin edir."),
        ("Seq Scan",
         "Cədvəlin başdan-başa oxunması. Kiçik cədvəldə ən sürətli yoldur."),
        ("Index Scan",
         "İndeksdən istifadə. Yalnız lazım olan sətirlər oxunur."),
        ("Index Only Scan",
         "Yalnız indeks oxunur, cədvələ heç baxılmır — ən sürətli."),
        ("Seçicilik (selectivity)",
         "Sorğunun seçdiyi sətir nisbəti. Yüksək seçicilik (az sətir) — "
         "indeks üçün yaxşıdır."),
        ("B-ağacı indeksi",
         "Sıralanmış ağac quruluşu. Soldan uyğunluqda işləyir, ortadan "
         "axtarışda yox."),
        ("Planner statistikası",
         "PostgreSQL-in cədvəl haqqında topladığı məlumat "
         "(sətir sayı, dəyər paylanması). <code>ANALYZE</code> yeniləyir."),
        ("emitDecoratorMetadata",
         "TypeScript-in dekorator metadatasını koda yazması. Nest DI "
         "bunsuz işləmir."),
        ("Materialized view",
         "Sorğunun nəticəsini <em>fiziki</em> saxlayan cədvəl. Sürətli "
         "oxunur, amma <code>REFRESH</code> tələb edir."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) <code>emekdaslar.module.ts</code> — sıra AÇIQ yazılır</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Module({
  imports: [PrismaModule],
  controllers: [
    StatistikaController, // «statistika»  →  :id-dən ƏVVƏL
    ElaqelerController,   // «:id/...»     →  3 seqment, toqquşmur
    TopluController,      // «toplu/...»   →  3 seqment, toqquşmur
    EmekdaslarController, // «:id»         →  ƏN SONDA!
  ],
  providers: [
    EmekdaslarService, StatistikaService, ElaqelerService, TopluService,
  ],
  exports: [
    EmekdaslarService, StatistikaService, ElaqelerService, TopluService,
  ],
})
export class EmekdaslarModule {}</pre>
<ul>
  <li><code>imports: [PrismaModule]</code> — <code>PrismaModule</code>
      <code>@Global()</code> olsa da, açıq yazırıq. Səbəb: modul
      <em>təkbaşına</em> da işləyə bilməlidir (gələcəkdə ayrı tətbiq
      kimi).</li>
  <li><code>controllers</code> massivindəki <strong>sıra</strong> —
      funksionaldır, kosmetik deyil.</li>
  <li><code>providers</code> — dörd servis. Nest onları
      <em>singleton</em> kimi yaradır (hər sorğuda yox, bir dəfə).</li>
  <li><code>exports</code> — başqa modul (məsələn gələcək hesabat modulu)
      bunları istəyə bilər. Bu olmasa,
      <code>Nest can't resolve dependencies</code> xətası çıxar.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2) <code>app.module.ts</code> — kök qraf</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    SaglamliqModule,
    EmekdaslarModule,
    AuditModule,
  ],
})
export class AppModule {}</pre>
<p>⚠️ <code>EmekdaslarModule</code> əvvəl, <code>AuditModule</code>
sonra — amma bu sıra <em>vacib deyil</em>, çünki onların prefiksləri
fərqlidir (<code>emekdaslar</code> və <code>audit</code>). Toqquşma
yalnız <em>eyni prefiksli</em> controller-lər arasında olur və o,
<code>EmekdaslarModule</code>-un içində həll olunur.</p>

<h5 style="color:#334155;margin-top:1rem">3) <code>skriptler/2b_yoxla.sh</code> — tam yoxlama</h5>
<p>Skript 48 yoxlama aparır və altı bölməyə bölünüb:</p>
<ol>
  <li><strong>Statistika</strong> — 7 yoxlama</li>
  <li><strong>Əlaqələr</strong> — 15 yoxlama</li>
  <li><strong>Toplu əməliyyatlar</strong> — 11 yoxlama</li>
  <li><strong>Audit</strong> — 12 yoxlama</li>
  <li><strong>Marşrut sırası</strong> — 6 yoxlama</li>
  <li><strong>Təmizlik</strong> — 2 yoxlama</li>
</ol>
<p>⚠️ Skriptin ən mühüm hissəsi <strong>təmizlik</strong>dir: həm
server prosesi, həm müvəqqəti fayllar, həm də test sətirləri
<code>trap</code> ilə təmizlənir. Test sətirləri
<code>b&lt;zaman&gt;.%</code> prefiksi ilə yaradılır və
<code>psql</code> ilə silinir.</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
temizle() {
  [ -n "$PID" ] && kill "$PID" 2>/dev/null
  [ -n "$PID" ] && wait "$PID" 2>/dev/null
  if [ -f .env ]; then
    DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
    psql "$DBURL" -At -c "
      DELETE FROM struktur.elmi_shura_uzvleri WHERE emekdas_id IN (...);
      DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'b%.%';" >/dev/null 2>&1
  fi
  rm -rf "$TMP"
  true
}
trap temizle EXIT INT TERM</pre>
<p>⚠️ <code>DBURL</code> oxunması: <code>cut -d= -f2-</code> —
<em>ikinci</em> sahədən sonuna qədər götürür (çünki parolun içində
<code>=</code> ola bilər). <code>sed 's/^"//; s/"$//'</code> isə
dırnaqları silir.</p>

<h5 style="color:#334155;margin-top:1rem">4) Marşrut sırasının CANLI sübutu</h5>
<p>C blokunda bunu <em>real serverdə</em> edirik:</p>
<ol>
  <li>Modul faylını ehtiyata kopyalayırıq.</li>
  <li>Controller sırasını <strong>qəsdən səhv</strong> edirik.</li>
  <li>Build edib serveri qaldırırıq → <code>/statistika</code>
      <code>400</code> verir.</li>
  <li>Faylı <strong>bayt-bayt</strong> bərpa edirik.</li>
  <li>Yenidən build edib yoxlayırıq → <code>200</code>.</li>
</ol>
<p>⚠️ <code>trap</code> ilə bərpa təmin olunur — skript yarıda çöksə
belə, fayl ilk vəziyyətinə qaytarılır. Sonda
<code>diff</code> ilə <em>bayt-bayt</em> eynilik yoxlanılır.</p>
""",
    "fayllar": [
        "src/emekdaslar/emekdaslar.module.ts",
        "src/app.module.ts",
        "skriptler/2b_yoxla.sh",
    ],
    "goster": ["src/audit/audit.module.ts"],
    "c": r"""
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
PID=""

echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then echo "  ✓ tip xətası yoxdur"; else echo "  ✗ tip xətası var"; fi

echo ""
echo "════ 2) Modul qrafı ════"
echo "  ── app.module.ts ──"
grep -A7 'imports: \[' src/app.module.ts | head -8 | sed 's/^/      /'
echo "  ── emekdaslar.module.ts (CONTROLLER SIRASI) ──"
grep -A6 'controllers: \[' src/emekdaslar/emekdaslar.module.ts | head -7 | sed 's/^/      /'

echo ""
echo "════ 3) Build və tam yoxlama (48 yoxlama) ════"
npm run build >/dev/null 2>&1
bash skriptler/2b_yoxla.sh 2>&1 | tail -30

echo ""
echo "════ 4) MARŞRUT SIRASI — CANLI SÜBUT ════"
KOK="src/emekdaslar/emekdaslar.module.ts"
EHTIYAT="/tmp/modul_ehtiyat_$$.bak"
cp "$KOK" "$EHTIYAT"
berpa() {
  cp "$EHTIYAT" "$KOK"
  [ -n "$PID" ] && kill "$PID" 2>/dev/null
  [ -n "$PID" ] && wait "$PID" 2>/dev/null
  true
}
trap berpa EXIT INT TERM

echo "  ── 4a) Sıra QƏSDƏN səhv edilir: EmekdaslarController qabağa ──"
python3 - <<'PYX'
import pathlib
p = pathlib.Path('src/emekdaslar/emekdaslar.module.ts')
s = p.read_text(encoding='utf-8')
A = "    StatistikaController, // «statistika»  →  :id-dən ƏVVƏL\n"
B = "    EmekdaslarController, // «:id»         →  ƏN SONDA!\n"
ORTA = "    ElaqelerController,   // «:id/...»     →  3 seqment, toqquşmur\n    TopluController,      // «toplu/...»   →  3 seqment, toqquşmur\n"
kohne = A + ORTA + B
yeni = B + A + ORTA
assert s.count(kohne) == 1, 'gözlənilən sıra tapılmadı'
p.write_text(s.replace(kohne, yeni), encoding='utf-8')
print('      ✓ controllers sırası DƏYİŞDİRİLDİ')
PYX
grep -A5 'controllers: \[' "$KOK" | sed -n '2,5p' | sed 's/^/      /'
npm run build >/dev/null 2>&1
PORT="${PORT:-4000}" node dist/main.js >/tmp/2b_sira.log 2>&1 &
PID=$!
for i in $(seq 1 60); do curl -fsS "http://localhost:$PORT/api/v1/saglamliq" -o /dev/null 2>/dev/null && break; sleep 0.5; done
printf '      /emekdaslar/statistika → %s   ← ⚠️ GÖZLƏNİLƏN 400\n' "$(curl -s -o /tmp/2b_s1.json -w '%{http_code}' "http://localhost:$PORT/api/v1/emekdaslar/statistika")"
printf '      cavab: %s\n' "$(head -c 130 /tmp/2b_s1.json)"
printf '      /emekdaslar/5          → %s   ← bu İŞLƏYİR, problemi GİZLƏDİR\n' "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:$PORT/api/v1/emekdaslar/5")"
kill $PID 2>/dev/null; wait $PID 2>/dev/null; PID=""

echo ""
echo "  ── 4b) Fayl BAYT-BAYT bərpa edilir ──"
cp "$EHTIYAT" "$KOK"
if diff -q "$EHTIYAT" "$KOK" >/dev/null; then echo "      ✓ bərpa olundu (diff: fərq yoxdur)"; fi
grep -A5 'controllers: \[' "$KOK" | sed -n '2,5p' | sed 's/^/      /'
npm run build >/dev/null 2>&1
PORT="${PORT:-4000}" node dist/main.js >/tmp/2b_sira2.log 2>&1 &
PID=$!
for i in $(seq 1 60); do curl -fsS "http://localhost:$PORT/api/v1/saglamliq" -o /dev/null 2>/dev/null && break; sleep 0.5; done
printf '      /emekdaslar/statistika → %s   ← ✓ DÜZGÜN\n' "$(curl -s -o /tmp/2b_s2.json -w '%{http_code}' "http://localhost:$PORT/api/v1/emekdaslar/statistika")"
printf '      /emekdaslar/5          → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:$PORT/api/v1/emekdaslar/5")"
printf '      /emekdaslar/abc        → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:$PORT/api/v1/emekdaslar/abc")"
kill $PID 2>/dev/null; wait $PID 2>/dev/null; PID=""
trap - EXIT INT TERM
diff -q "$EHTIYAT" "$KOK" >/dev/null && echo "      ✓ SON YOXLAMA: modul faylı ilk vəziyyətindədir"

echo ""
echo "════ 5) OPTİMALLAŞDIRMA — EXPLAIN ANALYZE ════"
i=0
while IFS= read -r sorqu; do
  i=$((i + 1))
  printf '\n  ── %d) %s\n' "$i" "$sorqu"
  psql "$DBURL" -c "EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF, SUMMARY OFF) $sorqu" 2>/dev/null \
    | grep -E 'Scan|Filter|Rows Removed|Index Cond|Sort Method|Heap Fetches' | sed 's/^/      /'
done <<'SQLX'
SELECT * FROM audit.audit_log WHERE id = (SELECT max(id) FROM audit.audit_log)
SELECT count(*) FROM audit.audit_log WHERE cedvel_adi = 'kadrlar.emekdaslar'
SELECT count(*) FROM audit.audit_log WHERE cedvel_adi LIKE 'ai.%'
SELECT count(*) FROM audit.audit_log WHERE istifadeci = 'arti_user'
SELECT id, soyad FROM kadrlar.emekdaslar ORDER BY soyad LIMIT 5
SQLX

echo ""
echo "  ── İndekslər (emekdaslar) ──"
psql "$DBURL" -At -c "
SELECT '      ' || indexname || ' → ' || regexp_replace(indexdef, '.*USING ', '')
  FROM pg_indexes WHERE schemaname='kadrlar' AND tablename='emekdaslar';" 2>/dev/null

echo ""
echo "  ── Cədvəl ölçüləri (planner niyə belə qərar verir) ──"
psql "$DBURL" -c "
SELECT relname AS cedvel, n_live_tup AS setir,
       pg_size_pretty(pg_total_relation_size(relid)) AS olcu
  FROM pg_stat_user_tables
 WHERE relname IN ('emekdaslar','audit_log','doktorantlar','sertifikasiya')
 ORDER BY n_live_tup DESC;" 2>/dev/null | sed 's/^/      /'

echo ""
echo "════ 6) YEKUN VƏZİYYƏT ════"
psql "$DBURL" -At -c "
SELECT '      əməkdaş        : ' || count(*) FROM kadrlar.emekdaslar;
SELECT '      audit qeydi    : ' || count(*) FROM audit.audit_log;
SELECT '      cədvəl         : ' || count(*) FROM information_schema.tables
 WHERE table_schema NOT IN ('pg_catalog','information_schema');
SELECT '      test zibili    : ' || count(*) FROM kadrlar.emekdaslar
 WHERE email LIKE 'b%.%@arti.edu.az' OR email LIKE 'toplu.%' OR email LIKE 'audit.%';" 2>/dev/null
printf '      TypeScript fayl: %s\n' "$(find src -name '*.ts' | wc -l | tr -d ' ')"
printf '      yoxlama skripti: %s\n' "$(ls -1 skriptler/ | wc -l | tr -d ' ')"
""",
    "olmaz": """Modul qoşulmasa — endpoint-lər 404:

const app = await NestFactory.create(AppModule);
// app.module.ts-də EmekdaslarModule YOXDUR

$ curl http://localhost:4000/api/v1/emekdaslar/statistika
HTTP/1.1 404 Not Found
{"ugur":false,"xeta":{"kod":"TAPILMADI",
 "mesaj":"Cannot GET /api/v1/emekdaslar/statistika"}}

  ← ⚠️ Server QALXIR, heç bir xəta yoxdur. Sadəcə
     endpoint yoxdur. Yeganə diaqnostika: başlanğıc
     logundaki marşrut cədvəli.

────────────────────────────────────────────────────────────
Controller sırası səhv olsa:

@Module({ controllers: [EmekdaslarController, StatistikaController] })

$ curl .../emekdaslar/statistika
HTTP/1.1 400 Bad Request
{"xeta":{"kod":"YANLIS_SORGU",
 "mesaj":"Validation failed (numeric string is expected)"}}

  ← ⚠️ Statistika HEÇ VAXT işləmir. Xəta mesajı «ədəd
     gözlənilirdi» deyir — halbuki istifadəçi düzgün
     URL yazıb.
  ← ⚠️ /emekdaslar/5 İŞLƏYİR. Yəni «API işləyir» təəssüratı
     yaranır və problem günlərlə tapılmır.

────────────────────────────────────────────────────────────
Express 4 sintaksisi ilə düzəltmək istəsək:

@Get(':id([0-9]+)')

PathError [TypeError]: Unexpected ( at index 22
    at consumeUntil (path-to-regexp/dist/index.js:130:23)

  ← ⚠️ Express 5 path-to-regexp 8-i işlədir və inline
     regex DƏSTƏKLƏMİR. Express 4-dən keçən layihələrdə
     bu, geniş yayılmış problemdir.

────────────────────────────────────────────────────────────
Ölçmədən indeks əlavə etsək:

CREATE INDEX idx_telefon ON kadrlar.emekdaslar (telefon);

EXPLAIN ANALYZE SELECT ... ORDER BY telefon LIMIT 5
→ Seq Scan on emekdaslar  (actual rows=14)

  ← ⚠️ İndeks YARADILDI, amma İŞLƏDİLMİR — 14 sətirdə
     seq scan daha sürətlidir. Boş yerə disk və
     yazma vaxtı xərcləndi.""",
    "c_izah": """
<p><strong>Birinci nəticə: 48 yoxlama keçdi.</strong> Dərs 2B-nin bütün
endpoint-ləri canlı serverdə işləyir — statistika, əlaqələr, toplu
əməliyyatlar və audit.</p>
<p><strong>İkincisi: marşrut sırası CANLI sübut olundu.</strong> Eyni
server, eyni kod — yeganə fərq <code>controllers</code> massivindəki
sıra. Nəticə:</p>
<ul>
  <li><strong>Səhv sıra:</strong> <code>/statistika</code> →
      <code>400</code>, amma <code>/5</code> → <code>200</code>.
      Problem <em>sükutla</em> gizlənir.</li>
  <li><strong>Düzgün sıra:</strong> <code>/statistika</code> →
      <code>200</code>, <code>/5</code> → <code>200</code>,
      <code>/abc</code> → <code>400</code> (bu düzgün davranışdır).</li>
</ul>
<p>Və fayl <strong>bayt-bayt</strong> bərpa olundu — <code>diff</code>
heç bir fərq göstərmədi. Yəni nümayiş təhlükəsizdir.</p>
<p><strong>Üçüncüsü: indeks olması işlədilməsi demək deyil.</strong>
BEŞ fərqli EXPLAIN nəticəsi gördük:</p>
<ol>
  <li><strong>PK üzrə bərabərlik</strong> (1 sətir) → <code>Index
      Scan</code> — mükəmməl seçicilik.</li>
  <li><strong>İndeksli sütunda bərabərlik</strong> (470/5482 = 8.6%)
      → <code>Index Only Scan</code> — indeks kifayət etdi.</li>
  <li><strong>İndeksli sütunda <code>LIKE 'ai.%'</code></strong>
      (785/5482 = 14%) → <code>Seq Scan</code> — seçicilik
      aşağıdır, indeks faydasızdır.</li>
  <li><strong>İndekssiz sütun</strong> (<code>istifadeci</code>) →
      <code>Seq Scan</code> — indeks yoxdur.</li>
  <li><strong>14 sətirlik cədvəl</strong> → <code>Seq Scan</code> —
      indeks <em>var</em>, amma kiçik cədvəldə lazımsızdır.</li>
</ol>
<p><strong>Dördüncüsü: planner statistikaya əsaslanır.</strong>
Nəticə 2 ilə 3-ün fərqi <em>yalnız</em> seçicilikdir (8.6% qarşı 14%).
PostgreSQL hər iki halda cədvəli oxuyur, amma birinci halda
<code>Index Only Scan</code> kifayət edir. Bu, «indeks əlavə et, hər şey
sürətlənər» fikrinin niyə <strong>yanlış</strong> olduğunu göstərir.</p>
<p><strong>Beşincisi: <code>ANALYZE</code> vacibdir.</strong> Planner
statistikası köhnələrsə, səhv plan seçə bilər. Böyük dəyişikliklərdən
(və ya toplu idxaldan) sonra <code>ANALYZE</code> işlətmək yaxşı
təcrübədir. PostgreSQL-də <code>autovacuum</code> bunu özü edir, amma
güclü dəyişiklikdən sonra əl ilə də etmək olar.</p>
""",
    "sual": [
        ("Niyə controller-ləri bir modulda saxlayırıq? Ayrı modullar daha təmiz deyilmi?",
         "Ayrı modullar <em>adətən</em> daha təmizdir — biz də ilk cəhddə belə etdik. Problem Nest-in <strong>qeydiyyat sırasındadır</strong>: əvvəlcə modulun öz controller-ləri, sonra import olunanlar. Ona görə <code>:id</code> yenə qabağa düşür. Alternativlər: (1) statistikanı fərqli prefiksə köçürmək (<code>/api/v1/statistika/emekdaslar</code>) — o zaman ayrı modul işləyər; (2) Nest-in <code>RouterModule</code> ilə əl ilə sıra təyin etmək (mürəkkəbdir). Biz açıq sıra seçdik, çünki o, <em>görünən</em> və <em>proqnozlaşdırıla biləndir</em>."),
        ("Bu problemi testlərlə tutmaq olarmı?",
         "Mütləq! Ən sadə test: hər <em>konkret</em> yol üçün <code>expect(200)</code> yazmaq. Bizim <code>2b_yoxla.sh</code> skripti məhz bunu edir — «marşrut sırası» bölməsi altı yolu yoxlayır. Daha sistemli yanaşma: bütün marşrut cədvəlini çıxarıb, <code>:id</code>-dən əvvəl gələn konkret yol olub-olmadığını avtomatik yoxlayan test yazmaq. Bu, 2C dərsinin mövzusudur."),
        ("<code>EXPLAIN</code> ilə <code>EXPLAIN ANALYZE</code> fərqi nədir?",
         "<code>EXPLAIN</code> sorğunu <strong>işlətmir</strong> — yalnız planı göstərir və <em>təxmini</em> xərc verir. <code>EXPLAIN ANALYZE</code> isə sorğunu <strong>həqiqətən işlədir</strong> və <em>faktiki</em> rəqəmləri göstərir. ⚠️ Diqqət: <code>ANALYZE</code> ilə <code>DELETE</code>/<code>UPDATE</code> yoxlamayın — sorğu həqiqətən işləyəcək! Oxuma sorğuları üçün isə <code>ANALYZE</code> daha dəqiq məlumat verir."),
        ("Niyə <code>Index Only Scan</code>-da <code>Heap Fetches: 453</code> var? Bu, indeksin işləmədiyini göstərmir?",
         "Xeyr — bu normaldır. <code>Index Only Scan</code> cədvələ <em>heç baxmamağa</em> çalışır, amma PostgreSQL <strong>visibility map</strong>-i təzə olmayanda bəzi sətirlər üçün cədvələ müraciət edir. <code>VACUUM</code> işlədikdən sonra bu rəqəm azalır və ya sıfır olur. Praktiki nəticə: nizami <code>VACUUM</code>/<code>autovacuum</code> <em>vacibdir</em> — o, yalnız yer boşaltmır, həm də bu tip optimallaşdırmaları işə salır."),
        ("<code>LIMIT 5</code> ilə <code>ORDER BY soyad</code> indeks işlətmirsə, necə sürətləndirim?",
         "Bu halda indeks <em>düzgün qurulmayıb</em>. <code>ORDER BY soyad LIMIT 5</code> üçün <strong>uyğun sıralanmış</strong> indeks lazımdır: <code>CREATE INDEX ... ON emekdaslar (soyad)</code> — bizdə belədir. Amma planner yenə <code>Seq Scan</code> seçir, çünki cədvəl 14 sətirdir. 10 000 sətirdə həmin sorğu <em>mütləq</em> <code>Index Scan</code> işlədəcək. Ona görə belə qərarları test bazasında deyil, <em>real həcmli</em> datада yoxlamaq lazımdır."),
        ("Bütün bunları yazmaq çox vaxt aldı. Bu, həqiqətən lazımdırmı?",
         "Suallarınız tamamilə haqlıdır və cavab <em>asılıdır</em>: (1) <strong>Prototip/MVP</strong> üçün — yox, sadə CRUD kifayətdir. (2) <strong>Real ERP</strong> üçün — bəli, çünki: audit loqu <em>qanuni tələbdir</em> (kadr və maliyyə sənədləşməsi); toplu əməliyyatlar <em>istifadəçi tələbidir</em> (100 müəllimi əl ilə daxil etmək olmaz); statistika <em>rəhbərlik tələbidir</em>. Optimallaşdırma isə <em>sonra</em> gəlir — əvvəlcə işləyən sistem, sonra sürətli sistem. Bizim dərsdə hər ikisini göstərdik."),
        ("Modul faylını dəyişib sonra bərpa edən skript təhlükəli deyilmi?",
         "Bir az riskli, amma <code>trap</code> ilə qorunur: skript <em>hansı səbəbdən</em> bitsə də (xəta, Ctrl+C, normal son), <code>berpa()</code> funksiyası işləyir. Üstəlik sonda <code>diff -q</code> ilə <strong>bayt-bayt</strong> eynilik yoxlanılır. Daha təhlükəsiz alternativ: faylı əl ilə düzəltmək əvəzinə <em>ayrı</em> müvəqqəti modul faylı yaradıb onu import etmək. Bizim yanaşma isə oxucuya <strong>həqiqi serverdə</strong> nəticəni göstərir — bu, dərsin məqsədidir."),
        ("Dərs 2B bitdi. Növbəti addım nədir?",
         "Təklif olunan ardıcıllıq: (1) <strong>2C — Autentifikasiya və rollar</strong>: JWT, bcryptjs, <code>@UseGuards</code>, RBAC (kim nə edə bilər), audit loquna <em>hansı istifadəçinin</em> yazılması; (2) <strong>2D — Excel hesabatları və fayl idxalı</strong>: ExcelJS ilə ixrac, CSV/Excel idxalı, uzun işlərin arxa planda görülməsi; (3) <strong>3 — Frontend</strong>: bu API-ni istehlak edən interfeys. Hər üçü üçün altyapı hazırdır: modul qrafı, audit loqu, toplu əməliyyatlar və yoxlama skriptləri."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li><strong>48 canlı yoxlama</strong> keçdi — Dərs 2B-nin bütün
      endpoint-ləri işləyir.</li>
  <li><strong>Modul qrafı quruldu:</strong> <code>AppModule</code> →
      <code>EmekdaslarModule</code> (4 controller) + <code>AuditModule</code>.</li>
  <li><strong>Marşrut sırası CANLI sübut olundu:</strong> səhv sıra
      <code>/statistika</code>-nı <code>400</code> edir, düzgün sıra
      <code>200</code>. Fayl bayt-bayt bərpa olundu.</li>
  <li><strong>5 fərqli EXPLAIN planı</strong> görüldü:
      <code>Index Scan</code>, <code>Index Only Scan</code> və üç
      <code>Seq Scan</code> halı. Ən vacib nəticə:
      <em>indeksin olması onun işlədiləcəyi demək deyil</em>.</li>
  <li><strong>Express 5 tapıntısı:</strong> <code>:id([0-9]+)</code>
      artıq işləmir — yeganə həll sıra qaydasıdır.</li>
  <li><strong><code>tsx</code> məhdudiyyəti:</strong> Nest tətbiqini
      <code>tsx</code> ilə qaldırmaq mümkün deyil (esbuild dekorator
      metadatasını yazmır).</li>
</ul>

<h3 style="color:#0f766e;margin-top:1.4rem">📘 Dərs 2B-nin yekunu</h3>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.7rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Addım</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Nə öyrəndik</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Əməli sübut</th>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>22</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Statistika:
        <code>groupBy</code>, <code>aggregate</code>, PL/pgSQL,
        <code>$queryRaw</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">21 yoxlama;
        baza funksiyası Prisma ilə üst-üstə düşdü</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>23</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Əlaqələr, N+1,
        <code>_count</code>, sorğu sayğacı</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">1 qarşı 12 sorğu
        ölçüldü</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>24</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Toplu əməliyyatlar,
        atomiklik, <code>multiply</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">21 yoxlama;
        faiz tələsi canlı görüldü</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>25</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Audit loqu, trigger,
        tranzaksiyada izləmə</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">28 yoxlama;
        trigger 3 qeyd yazdı</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>26</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Modul qrafı, marşrut
        sırası, <code>EXPLAIN ANALYZE</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">48 canlı yoxlama;
        400 ↔ 200 sübutu</td>
  </tr>
</table>

<h3 style="color:#0f766e;margin-top:1.4rem">📊 Dərs 2A + 2B — ümumi
nəticə</h3>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.7rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Göstərici</th>
    <th style="text-align:right;padding:.45rem;border:1px solid #e2e8f0">Dəyər</th>
  </tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0">Endpoint sayı
      (<code>emekdaslar</code> + <code>audit</code>)</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0;text-align:right">28</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0">Yoxlama skripti</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0;text-align:right">6</td></tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0">Yekun test
      (IA + IB + IIA + IIB)</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0;text-align:right">40</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0">Bazada cədvəl</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0;text-align:right">48</td></tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0">Audit qeydi</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0;text-align:right">5 400+</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0">Real əməkdaş</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0;text-align:right">14</td></tr>
</table>

<h3 style="color:#0f766e;margin-top:1.4rem">🚀 Sonrakı dərslər</h3>
<ol>
  <li><strong>2C — Autentifikasiya və rollar:</strong> JWT token,
      <code>bcryptjs</code> ilə parol hash-lənməsi, <code>@UseGuards</code>,
      RBAC (rol əsaslı icazə), audit loquna istifadəçinin yazılması.</li>
  <li><strong>2D — Excel və fayl idxalı:</strong> <code>ExcelJS</code> ilə
      hesabat ixracı, CSV/Excel idxalı, uzun işlərin arxa planda
      görülməsi (queue).</li>
  <li><strong>3 — Frontend:</strong> bu API-ni istehlak edən interfeys —
      cədvəllər, filtrlər, formalar, dashboard.</li>
  <li><strong>4 — Docker və yerləşdirmə:</strong> bütün sistemi bir
      əmrlə qaldırmaq, istehsalat konfiqurasiyası.</li>
</ol>

<p style="background:#f0fdfa;border-left:5px solid #14b8a6;border-radius:10px;
          padding:1rem 1.2rem;margin-top:1rem">
<strong>💡 Dərsin ən vacib vərdişi:</strong> <em>ölç</em>. Sorğu sayını
ölç (<code>$on('query')</code>), vaxtı ölç (<code>EXPLAIN ANALYZE</code>),
nəticəni ölç (test skriptləri). «Yəqin ki, bu yavaşdır» və «yəqin ki,
bu işləyir» — hər ikisi <em>optimallaşdırmanın</em> və
<em>düzəltmənin</em> ən pis başlanğıcıdır. Rəqəm görmədən kod
dəyişməyin.
</p>
""",
})
