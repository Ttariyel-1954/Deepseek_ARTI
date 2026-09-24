#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-2A — ADDIM 17–21 mətnləri.

Hər addım 4 hissədən ibarətdir:
  A      — «niyə» (geniş nəzəri izah)
  B      — kod (fayllar BACKEND qovluğundan canlı oxunur)
  C      — yoxlama əmrləri
  D      — həqiqi çıxış (qurucu tərəfindən icra olunur)
Əlavə: «Yeni anlayışlar», «Kodun sətir-sətir izahı», «Tez-tez verilən suallar».
"""

ADIMLAR = []


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 17 — DTO-LAR
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 17,
    "ad": "DTO-lar — giriş məlumatını qapıda yoxlayırıq",
    "a": """
<p>İndiyə qədər yazdığımız yeganə endpoint <code>/api/v1/saglamliq</code> idi
və o, <em>heç bir giriş məlumatı qəbul etmirdi</em>. İndi isə istifadəçi
bizə məlumat <strong>göndərəcək</strong>: yeni əməkdaşın adını, soyadını,
vəzifəsini… Bu məlumat düzgündürmü? Onu kim yoxlayacaq?</p>

<h4>Problem: istifadəçiyə etibar etmək olmaz</h4>
<p>Frontend yaxşı yazılıb, formaları yoxlayır — amma API-yə <em>yalnız
brauzer</em> müraciət etmir. Sorğu birbaşa <code>curl</code> ilə,
Postman ilə, köhnə bir mobil tətbiqlə, ya da pis niyyətli bir skriptlə
gələ bilər. Frontend yoxlaması <strong>rahatlıq üçündür</strong>, təhlükəsizlik
üçün deyil. <em>Həqiqi yoxlama serverdə olmalıdır.</em></p>

<p>Yoxlama olmasa nə olar? Təsəvvür edin, kimsə belə sorğu göndərir:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
POST /api/v1/emekdaslar
{ "ad": "A", "cinsiyyet_id": 999, "maas": -50 }</pre>
<p>Nəticə: ya baza özü xəta verir (anlaşılmaz İngilis dilli mesajla,
500 kodu ilə), ya da <em>daha pis</em> — sətir bazaya düşür və
hesabatlar sonra səhv çıxır. Bir sətirlik zibil məlumatı təmizləmək
üçün günlərlə vaxt gedə bilər.</p>

<h4>Həll: DTO</h4>
<p><strong>DTO</strong> — <em>Data Transfer Object</em>, «məlumat ötürmə
obyekti». Sadə dillə: <strong>istifadəçidən gələn məlumatın
<em>formasıdır</em></strong>. Sinif kimi yazılır, hər sahənin üstünə
yoxlama qaydaları (<em>dekoratorlar</em>) qoyulur.</p>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export class EmekdasYaratDto {
  @IsString() @MinLength(2) @MaxLength(60)
  ad!: string;
  ...
}</pre>

<p>Oxunuşu: «<code>ad</code> mətn olmalıdır, ən azı 2, ən çoxu 60 simvol».
Bu sinif təkbaşına heç nə etmir — onu <strong>işə salan</strong> mexanizm
lazımdır.</p>

<h4>İşə salan mexanizm: ValidationPipe</h4>
<p>1A-nın ADDIM 11-də <code>main.ts</code> faylında bu sətirləri yazmışdıq:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,            // DTO-da olmayan sahələri sil
    forbidNonWhitelisted: true, // ...və ya şikayət et
    transform: true,            // "5" → 5 kimi çevirmələr
  }),
);</pre>
<p>Nest hər sorğuda bu borudan (pipe) keçir:</p>
<ol>
  <li>Controller metodunun parametrinə baxır: hansı <em>sinif</em> gözlənilir?</li>
  <li>Gələn xam JSON-u həmin sinfin <strong>nüsxəsinə</strong> çevirir
      (<code>transform: true</code>).</li>
  <li>Bütün dekorator qaydalarını işlədir.</li>
  <li>Qayda pozulubsa → <code>400 Bad Request</code> və
      <strong>hansı sahənin</strong> səhv olduğunu izah edən siyahı.</li>
  <li>Hər şey qaydasındadırsa → controller metoduna <em>təmiz obyekt</em>
      ötürülür.</li>
</ol>
<p>Yəni controller metodunun içində <strong>bir dənə də <code>if</code>
yoxlaması yazmırıq</strong>. Kod təmiz qalır, yoxlama isə bir yerdə,
açıq-aşkar görünür.</p>

<h4>Nə üçün ÜÇ ayrı DTO?</h4>
<table style="width:100%;border-collapse:collapse;font-size:.92rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">DTO</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Harada</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Fərqi</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>EmekdasSorguDto</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>GET</code> sorğusu
        (<code>?seife=1</code>)</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">URL-dən gələn hər şey
        <strong>mətndir</strong>; hamısı istəyə bağlıdır və standart dəyəri var</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>EmekdasYaratDto</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>POST</code> gövdəsi</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>ad</code>,
        <code>soyad</code>, <code>ata_adi</code>, <code>cinsiyyet_id</code>,
        <code>vezife_id</code> — <strong>mütləqdir</strong></td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>EmekdasYenileDto</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>PATCH</code> gövdəsi</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Hamısı</strong>
        istəyə bağlıdır — istifadəçi yalnız dəyişdirmək istədiyini göndərir</td>
  </tr>
</table>
<p>Eyni sahələr iki dəfə yazılır — bu, təkrarçılıqdır (DRY prinsipinə ziddir).
Alternativ var: <code>PartialType(EmekdasYaratDto)</code> ilə yeniləmə DTO-sunu
avtomatik yaratmaq. Amma onda <code>@nestjs/mapped-types</code> paketini
<code>package.json</code>-a əlavə etmək lazımdır. Öyrənmə mərhələsində açıq
yazmaq daha faydalıdır: hər sahənin niyə istəyə bağlı olduğunu
<em>görürsünüz</em>. ADDIM 17-nin sonundaki FAQ-da bu mövzuya qayıdırıq.</p>

<h4>⚠️ Ən incə detal: URL-dən gələn məlumat MƏTDİR</h4>
<p><code>GET /emekdaslar?limit=5</code> sorğusunda <code>5</code> rəqəm
deyil, <strong>mətn</strong> <code>"5"</code>-dir. HTTP protokolu belədir:
URL yalnız mətn daşıyır. Ona görə <code>@Type(() => Number)</code>
dekoratoru lazımdır:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Type(() => Number)
@IsInt({ message: 'limit tam ədəd olmalıdır' })
@Min(1) @Max(100)
limit: number = 20;</pre>
<p>Bu olmasa <code>@IsInt()</code> həmişə uğursuz olardı — çünki
<code>"5"</code> mətndir! Bu, yeni başlayanların ən çox ilişib qaldığı
yerdir.</p>

<h4>Niyə <code>@Max(100)</code>?</h4>
<p>Bu, <strong>qoruyucu hədddir</strong> (rate limiting-in sadə forması).
Təsəvvür edin, kimsə <code>?limit=99999999</code> göndərir. Server bütün
14 sətri yox — milyonlarla sətri yaddaşa yükləməyə çalışar və
<em>yaddaş tükənər</em>. Bir sətirlik <code>@Max(100)</code> bunun
qarşısını alır. Həddi <em>həmişə</em> təyin edin.</p>

<h4>Axtarış üçün <code>@MaxLength(50)</code></h4>
<p>Eyni məntiq: <code>?axtar=</code> parametrinə 10 000 simvolluq mətn
göndərilsə, bazada <code>LIKE '%...%'</code> sorğusu son dərəcə yavaş
işləyər (hər sətirdə tam mətn müqayisəsi). 50 simvol kifayətdir.</p>

<h4>Sıralama üçün AĞ SİYAHI — ən vacib təhlükəsizlik detalı</h4>
<p><code>siralama</code> parametri birbaşa SQL-in <code>ORDER BY</code>
hissəsinə düşür. Əgər istifadəçi istənilən sütun adını göndərə bilsəydi,
bu, <strong>ikinci dərəcəli SQL inyeksiyası</strong> adlanan boşluq
yaradardı. Ona görə DTO-da icazəli sütunların siyahısı var:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export const SIRALANA_BILEN = ['soyad', 'ad', 'ise_baslama', 'maas', 'id'] as const;
...
@IsIn(SIRALANA_BILEN, { message: `siralama yalnız bunlardan biri ola bilər: ...` })</pre>
<p><code>@IsIn</code> yalnız siyahıdaki dəyərləri qəbul edir. Bundan
başqa hər şey <code>400</code> alır. Bu naxışın adı
<strong>ağ siyahı</strong> (whitelist) və ya «allowlist»-dir.</p>
""",
    "anlayis": [
        ("DTO",
         "Data Transfer Object — istifadəçidən gələn məlumatın formasını "
         "təyin edən sinif. Yoxlama qaydaları dekoratorlarla yazılır."),
        ("Dekorator",
         "<code>@IsString()</code> kimi «@» ilə başlayan işarələr. Onlar "
         "sinifə/sahəyə <em>metaməlumat</em> bağlayır; kitabxanalar bu "
         "metaməlumatı oxuyub qərar verir."),
        ("Pipe (boru)",
         "Nest-də məlumatın controller-ə çatmazdan əvvəl keçdiyi "
         "emal mərhələsi: çevirmə (transform) və yoxlama (validate)."),
        ("class-validator",
         "<code>@IsString</code>, <code>@Min</code>, <code>@IsEmail</code> "
         "kimi dekoratorları təmin edən paket. Nest onunla ayrılmaz "
         "işləyir."),
        ("class-transformer",
         "<code>@Type(() => Number)</code> kimi çevirmə dekoratorlarını "
         "təmin edən paket. Xam JSON-u sinif nüsxəsinə çevirir."),
        ("whitelist",
         "<code>true</code> olanda DTO-da olmayan sahələr sükutla "
         "<strong>silinir</strong>."),
        ("forbidNonWhitelisted",
         "<code>true</code> olanda DTO-da olmayan sahə <strong>400 xətası</strong> "
         "verir. <code>whitelist</code>-dən sərt variantdır."),
        ("transform: true",
         "Mətnləri ədədə/boolean-a çevirməyə icazə verir "
         "(<code>\"5\" → 5</code>). Olmasa, sorğu parametrləri ilə işləmək "
         "mümkün olmaz."),
        ("Ağ siyahı (allowlist)",
         "«Yalnız bu dəyərlərə icazə ver» prinsipi. «Qara siyahı»dan "
         "(«bunları qadağan et») qat-qat təhlükəsizdir."),
        ("Sıralama inyeksiyası",
         "İstifadəçinin göndərdiyi dəyərin birbaşa <code>ORDER BY</code>-a "
         "düşməsi. Ağ siyahı ilə qarşısı alınır."),
        ("Standart dəyər (default)",
         "<code>limit: number = 20</code> — parametr verilməzsə istifadə "
         "olunan dəyər. Ona görə parametrsiz sorğu da işləyir."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) <code>emekdas-sorgu.dto.ts</code> — GET parametrləri</h5>
<ul>
  <li><code>@IsOptional()</code> — bu sahə göndərilməzsə, qalan bütün
      yoxlamaları <em>keç</em>. Vacib nüans: class-validator üçün
      «göndərilməyib» həm <code>undefined</code>, həm də <code>null</code>
      deməkdir. Yəni <code>?aktiv=</code> (boş dəyər) də
      <code>@IsOptional</code> sayılır və <code>@IsIn</code> işləməyəcək.
      Bu, praktikada nadir haldır, amma bilmək lazımdır.</li>
  <li><code>@Type(() => Number) @IsInt()</code> — <strong>cütlük</strong>.
      <code>@Type</code> mətni ədədə çevirir, <code>@IsInt</code> isə
      çevrilənin həqiqətən tam ədəd olduğunu yoxlayır. Yalnız
      <code>@Type</code> yazsanız, <code>"abc"</code> → <code>NaN</code>
      olar və heç bir xəta çıxmaz! Yalnız <code>@IsInt</code> yazsanız,
      <code>"5"</code> mətn olduğu üçün həmişə uğursuz olar.</li>
  <li><code>seife: number = 1</code> — sinif sahəsinin <em>standart
      dəyəri</em>. Sinif nüsxəsi yarananda TypeScript bu dəyəri təyin
      edir. <code>transform: true</code> olmasa bu işləməz — çünki
      Nest sadəcə JSON-u <code>Object.assign</code> edər.</li>
  <li><code>SIRALANA_BILEN</code> — <code>as const</code> ilə yazılıb.
      Faydası: TypeScript onu <em>dəyişməz</em> hesab edir və
      <code>@IsIn</code> üçün uyğun tip verir. <code>as const</code>
      olmasa tip <code>string[]</code> olardı və heç bir qoruma
      qalmazdı.</li>
  <li><code>aktiv: 'aktiv' | 'passiv' | 'hamisi' = 'aktiv'</code> —
      <em>birləşmə tipi</em> (union type). TypeScript-ə «bu sahə yalnız
      bu üç mətndən biri ola bilər» deyir. Yoxlama həm <code>@IsIn</code>
      ilə <em>işləmə vaxtı</em>, həm də TypeScript ilə <em>yazma
      vaxtı</em> təmin olunur. Bu ikiqat qoruma çox faydalıdır.</li>
  <li><code>merkez_id?: number</code> — sual işarəsi «istəyə bağlı»
      deməkdir. <code>@IsOptional()</code> ilə birlikdə işlədilir:
      TypeScript tipi yoxlayır, class-validator isə gələn məlumatı.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2) <code>emekdas-yarat.dto.ts</code> — POST gövdəsi</h5>
<ul>
  <li><code>ad!: string</code> — <strong>qeyri-müəyyən təyinat işarəsi</strong>
      (<em>definite assignment assertion</em>). Sual işarəsinin
      <em>əksi</em>dir: «bu sahə mütləq doldurulacaq, amma mən onu
      konstruktorda doldurmuruq — sən narahat olma». Olmasa TypeScript
      <code>strictPropertyInitialization</code> səbəbindən xəta verərdi.
      Onu dolduran <code>ValidationPipe</code>-dır.</li>
  <li><code>@MinLength(2)</code> — «A» adlı əməkdaş olmaz. Bu, real
      məlumat keyfiyyəti qaydasıdır. Azərbaycan adları arasında 2
      hərfli ad var (məsələn «Əli» 3 hərfdir), ona görə 2 həddi
      təhlükəsizdir.</li>
  <li><code>@MaxLength(60)</code> — bazada sütun <code>text</code>-dir,
      yəni <em>limitsizdir</em>. Amma limitsiz saxlamaq da yaxşı deyil:
      biri 1 MB-lıq «ad» göndərsə, hesabatlar oxunmaz olar. Yoxlama
      bazada deyil, <strong>tətbiqdə</strong> olmalıdır ki, xəta mesajı
      aydın olsun.</li>
  <li><code>@IsEmail({}, { message: '...' })</code> — birinci arqument
      seçimlər obyektidir (boş), ikincisi isə mesaj. Mesajı
      Azərbaycanca yazmaq vacibdir: istifadəçi «email must be an email»
      əvəzinə aydın izah görməlidir.</li>
  <li><code>@IsDateString()</code> — ISO 8601 formatını yoxlayır.
      <code>2026-01-15</code> keçər, <code>15.01.2026</code> keçməz.
      Bu vacibdir, çünki bazada <code>@db.Date</code> sütunudur və
      PostgreSQL yalnız ISO formatını etibarlı oxuyur.</li>
  <li><code>@IsNumber({ maxDecimalPlaces: 2 })</code> — pul üçün.
      Bazada <code>numeric(12,2)</code>-dir; 3 onluq rəqəm göndərsək,
      Prisma onu <em>yuvarlaqlaşdırar</em> və istifadəçi «100.555
      yazdım, 100.56 oldu» deyə şikayət edər. Yoxlama bunun qarşısını
      alır: səhv məlumat <strong>sükutla dəyişdirilmir</strong>,
      rədd edilir.</li>
  <li><code>@Max(9999999999.99)</code> — <code>numeric(12,2)</code>
      tipinin üst həddi: 10 rəqəm tam + 2 onluq. Bu həddi aşan dəyər
      bazada <code>out of range</code> xətası verərdi (500 kodu ilə).
      DTO-da tutmaq daha yaxşıdır.</li>
  <li><code>@IsBoolean()</code> — <strong>diqqət</strong>: JSON-da
      <code>true</code>/<code>false</code> göndərilməlidir.
      <code>"true"</code> mətni <code>@IsBoolean</code>-dan keçməz.
      (Səbəb: <code>transform: true</code> yalnız
      <code>@Type(() => Boolean)</code> varsa çevirir, biz isə onu
      qəsdən qoymamışıq — çünki <code>Boolean("false")</code>
      JavaScript-də <code>true</code>-dur! Bu çox məşhur tələdir.)</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3) <code>emekdas-yenile.dto.ts</code> — PATCH gövdəsi</h5>
<p>Struktur <code>EmekdasYaratDto</code> ilə eynidir, üç fərqlə:</p>
<ul>
  <li>Hər sahədə <code>@IsOptional()</code> var. <strong>Niyə?</strong>
      Çünki PATCH «qismən yeniləmə» deməkdir: istifadəçi yalnız
      <code>{"maas": 3000}</code> göndərə bilər. <code>@IsOptional</code>
      olmasa, <code>@IsString()</code> qaydası çatışmayan
      <code>ad</code> üçün işləyər və «ad mətn olmalıdır» xətası
      çıxardı — halbuki istifadəçi <code>ad</code>-ı heç göndərməyib.</li>
  <li>Sahələr <code>?</code> ilə işarələnib (<code>ad?: string</code>) —
      TypeScript də bilir ki, bunlar ola da bilər, olmaya da.</li>
  <li>Servisdə <code>undefined</code> yoxlaması var:
      <code>if (dto.maas !== undefined) data.maas = dto.maas;</code>.
      <strong>Bu çox vacibdir!</strong> <code>if (dto.maas)</code>
      yazsaydıq, <code>0</code> dəyəri (maaş 0) <em>yanlış</em> sayılıb
      atlanardı. JavaScript-də <code>0</code>, <code>""</code> və
      <code>false</code> «yalançı» dəyərlərdir. Ona görə
      <strong>həmişə</strong> <code>!== undefined</code> yazın.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">4) <code>skriptler/dto_yoxla.ts</code> — yoxlama skripti</h5>
<ul>
  <li><code>import 'reflect-metadata'</code> — <strong>mütləqdir</strong>.
      Dekoratorlar öz metaməlumatlarını bu kitabxananın yaddaşında
      saxlayır. Bu sətir olmasa <code>@IsString()</code> kimi
      dekoratorlar <em>heç nə etmir</em> və bütün yoxlamalar sükutla
      işləməyəcək. Ən məkrli səhv növüdür: heç bir xəta çıxmır,
      sadəcə API zibil qəbul edir.</li>
  <li><code>new ValidationPipe({...})</code> — <code>main.ts</code>-dəki
      <em>eyni</em> konfiqurasiya. Beləliklə skriptin nəticəsi canlı
      API-nin nəticəsi ilə üst-üstə düşür. Testin «real» olması
      bundan ibarətdir.</li>
  <li><code>boru.transform(govde, { type: 'body', metatype: Dto })</code> —
      Nest-in daxildə çağırdığı metodun <em>eynisi</em>.
      <code>type: 'body'</code> / <code>'query'</code> fərqi var:
      sorğu parametrləri üçün Nest əlavə çevirmə edir.</li>
  <li><code>catch (x)</code> içində
      <code>(x as { getResponse?: () => unknown }).getResponse?.()</code> —
      Nest-in <code>BadRequestException</code> obyektindən cavabı
      çıxarırıq. Orada <code>message</code> <em>massivdir</em> — hər
      pozulmuş qayda üçün bir sətir.</li>
  <li><code>kecdi</code> / <code>xeta</code> sayğacları və
      <code>process.exit(1)</code> — skript bash üçün <em>test</em>ə
      çevrilir. Çıxış kodu <code>0</code> olmasa, yekun testlər
      uğursuz sayır.</li>
</ul>
""",
    "fayllar": [
        "src/emekdaslar/dto/emekdas-sorgu.dto.ts",
        "src/emekdaslar/dto/emekdas-yarat.dto.ts",
        "src/emekdaslar/dto/emekdas-yenile.dto.ts",
        "skriptler/dto_yoxla.ts",
    ],
    "goster": ["src/main.ts"],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then
  echo "  ✓ tip xətası yoxdur"
else
  echo "  ✗ tip xətası var (yuxarıya baxın)"
fi

echo ""
echo "════ 2) DTO faylları ════"
ls -1 src/emekdaslar/dto/ | sed 's/^/      /'
printf '      cəmi sətir: %s\n' "$(cat src/emekdaslar/dto/*.ts | wc -l | tr -d ' ')"

echo ""
echo "════ 3) Yoxlama qaydalarının sayı ════"
printf '      @Is… dekoratoru : %s\n' "$(grep -c '@Is' src/emekdaslar/dto/*.ts | awk -F: '{s+=$2} END {print s}')"
printf '      @Type / @Min / @Max : %s\n' "$(grep -cE '@(Type|Min|Max)' src/emekdaslar/dto/*.ts | awk -F: '{s+=$2} END {print s}')"
printf '      Azərbaycanca mesaj  : %s\n' "$(grep -c 'message:' src/emekdaslar/dto/*.ts | awk -F: '{s+=$2} END {print s}')"

echo ""
echo "════ 4) REAL validasiya matrisi ════"
npx tsx skriptler/dto_yoxla.ts
""",
    "olmaz": """DTO və ValidationPipe olmasa nə olardı?

$ curl -X POST http://localhost:4000/api/v1/emekdaslar \\
    -H 'Content-Type: application/json' \\
    -d '{"ad":"A","cinsiyyet_id":999,"maas":-50}'

HTTP/1.1 500 Internal Server Error

{"ugur":false,"xeta":{"kod":"DAXILI_XETA",
 "mesaj":"\\nInvalid `prisma.emekdaslar.create()` invocation:\\n\\n
 Foreign key constraint violated on the constraint:
 `emekdaslar_cinsiyyet_id_fkey`"}}

  ← ⚠️ İstifadəçi 500 görür və «server sındı» düşünür.
     Halbuki SƏHV ONDADIR, serverdə yox.

────────────────────────────────────────────────────────────
VƏ YA daha pis hal — bazada CHECK qaydası olmasaydı:

$ curl -X POST ... -d '{"ad":"A","soyad":"B","ata_adi":"C",
                         "cinsiyyet_id":1,"vezife_id":6,"maas":-50}'
HTTP/1.1 201 Created
{"...": "...", "maas": "-50.00", "ad": "A"}

  ← ⚠️ MƏNFİ MAAŞ bazaya DÜŞDÜ. Heç bir xəta yoxdur.
     Ay sonu hesabatı çıxanda məlum olacaq ki, kiminsə
     maaşı minus 50 manatdır. Kim düzəldəcək? Nə vaxt?

────────────────────────────────────────────────────────────
VƏ YA sıralama ağ siyahısı olmasa:

$ curl 'http://localhost:4000/api/v1/emekdaslar?siralama=parol_hash'

  ← ⚠️ ORDER BY parol_hash — istifadəçi sütun adlarını
     sadalayaraq bazanın strukturunu öyrənə bilər.
     Bu, məlumat sızmasının başlanğıcıdır.""",
    "c_izah": """
<p><strong>Ən başlıca qazanc: yoxlama BİR yerdədir.</strong> Yoxlama
controller-də, servisdə və bazada səpələnsəydi, üç fərqli yerdə üç fərqli
mesaj olardı. DTO ilə hamısı bir faylda, açıq-aşkar görünür. Yeni
proqramçı gələndə «bu sahə üçün hansı qaydalar var?» sualına cavab
<em>bir fayla baxmaqla</em> alınır.</p>
<p><strong>İkincisi: xəta mesajı istifadəçi üçündür.</strong> Diqqət
yetirin, bütün mesajlar Azərbaycancadır və <em>nə etmək lazım olduğunu</em>
deyir: «ad ən azı 2 simvol olmalıdır». Xam Prisma xətası isə
<code>Foreign key constraint violated on the constraint:
emekdaslar_cinsiyyet_id_fkey</code> kimi texniki mətndir — istifadəçi
üçün mənasızdır, proqramçı üçün isə <em>çox vaxt yanlış yerdə</em>
axtarışa səbəb olur.</p>
<p><strong>Üçüncüsü: <code>transform: true</code> olmasa heç nə
işləməzdi.</strong> URL-dən gələn hər şey mətndir. <code>@Type(() => Number)</code>
+ <code>transform</code> cütlüyü olmasa, <code>?limit=5</code> sorğusu
həmişə 400 qaytarardı. Bu, HTTP protokolunun təbiətindən irəli gəlir:
URL mətn quruluşudur.</p>
<p><strong>Dördüncüsü: <code>@Max(100)</code> və <code>@MaxLength(50)</code>
qoruyucu həddlərdir.</strong> Onlar olmasa, bir nəfər
<code>?limit=99999999</code> göndərib serverin yaddaşını dolduraraq
<em>bütün digər istifadəçilər üçün</em> xidməti dayandıra bilər. Bu,
«xidmətdən imtina» (Denial of Service) hücumunun ən sadə formasıdır və
bir sətirlik hədlə qarşısı alınır.</p>
<p><strong>Beşincisi: <code>skriptler/dto_yoxla.ts</code> — test
mədəniyyətinin başlanğıcı.</strong> 25 fərqli halı <em>avtomatik</em>
yoxlayır. Yeni bir qayda əlavə edəndə, sadəcə skripti işlədirik —
köhnə qaydaları sındırmadığımıza əmin oluruq. Bu, 1B-də öyrəndiyimiz
«reqressiya qorunması» prinsipinin <em>əməli</em> tətbiqidir.</p>
""",
    "sual": [
        ("DTO ilə TypeScript <em>interface</em> arasında nə fərq var?",
         "<code>interface</code> yalnız <em>yazma vaxtı</em> mövcuddur — "
         "koda çevriləndə tamamilə yox olur. DTO isə <strong>sinifdir</strong>: "
         "işləmə vaxtında da mövcuddur, dekorator metaməlumatı daşıyır və "
         "Nest onu həqiqi obyektə çevirə bilir. Ona görə yoxlama üçün "
         "<code>interface</code> yaramır."),
        ("Niyə <code>whitelist</code> ilə <code>forbidNonWhitelisted</code> "
         "eyni vaxtda? Biri kifayət deyilmi?",
         "<code>whitelist: true</code> yad sahələri <em>sükutla silir</em>. "
         "Bu, təhlükəsizdir, amma gizlidir: istifadəçi <code>emeil</code> "
         "(səhv yazılış) göndərir, sahə silinir, e-poçt isə boş qalır — "
         "heç bir xəbərdarlıq yoxdur. <code>forbidNonWhitelisted: true</code> "
         "isə dərhal 400 qaytarır və problemi göstərir. İkisi birlikdə "
         "həm təhlükəsiz, həm də aydın nəticə verir."),
        ("<code>@Type(() => Number)</code> yerinə "
         "<code>ParseIntPipe</code> işlətsəm olmaz?",
         "<code>ParseIntPipe</code> tək bir parametr (məsələn "
         "<code>:id</code>) üçündür. Bizim <code>limit</code>, "
         "<code>seife</code>, <code>merkez_id</code> kimi <em>beş</em> "
         "sahəmiz var və onlar bir obyektdə gəlir. Hər biri üçün ayrı "
         "boru yazmaq <code>@Query('limit', ParseIntPipe)</code> kimi "
         "controller-i dağıdardı. DTO yanaşması daha səliqəlidir."),
        ("Niyə <code>PartialType</code> işlətmədim? Bu, kod təkrarı deyilmi?",
         "Haqlısınız, təkrardır. <code>PartialType(EmekdasYaratDto)</code> "
         "bir sətirlə eyni nəticəni verərdi. Səbəb: <code>PartialType</code> "
         "<code>@nestjs/mapped-types</code> paketindədir və onu "
         "<code>package.json</code>-a <em>açıq</em> əlavə etmək lazımdır "
         "(hazırda yalnız dolayı asılılıq kimi mövcuddur). Dolayı asılılığa "
         "güvənmək pis təcrübədir: paket yenilənəndə gözlənilmədən yox ola "
         "bilər. Öyrənmə mərhələsində açıq yazmaq daha faydalıdır."),
        ("Sahə adlarını Azərbaycanca yazmaq olarmı "
         "(<code>ad</code>, <code>soyad</code>) — bu normaldırmı?",
         "Bəli, və bu layihədə <em>düzgün</em> seçimdir: baza sxemi artıq "
         "Azərbaycanca adlarla yazılıb. Qayda budur: <strong>daxili "
         "adlandırma bir dildə olmalıdır</strong>. Yarısı İngilis, yarısı "
         "Azərbaycan olan kod ən pisdir. Bizim bütün layihəmiz Azərbaycan "
         "adlandırması ilə gedir — ardıcıl davam edirik."),
        ("<code>message</code> yazmasam nə olar?",
         "class-validator-ın standart İngilis mesajı gələr: "
         "<code>ad must be longer than or equal to 2 characters</code>. "
         "İşləyir, amma istifadəçi üçün narahatdır. Bütün mesajları "
         "Azərbaycanca yazmaq bir dəfəlik zəhmətdir və hər xəta halında "
         "<em>qat-qat</em> fayda gətirir."),
        ("Bu DTO-ları bazadaki sütunlardan <em>avtomatik</em> yaratmaq olmaz?",
         "Olar — məsələn Prisma-nın <code>zod-prisma-types</code> kimi "
         "generatorları ilə. Amma avtomatik yaranan DTO-larda "
         "<em>biznes qaydaları</em> olmur: baza <code>email</code> sütununun "
         "e-poçt olduğunu bilmir, <code>maas</code>-ın mənfi ola bilməyəcəyini "
         "isə CHECK qaydası ilə bilir. DTO əl ilə yazılır, çünki orada "
         "<strong>biznesin qaydaları</strong> ifadə olunur, baza tipi yox."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>Üç DTO yazdıq: sorğu (GET), yaratma (POST), yeniləmə (PATCH) — cəmi
      <strong>25 validasiya qaydası</strong> real matrisdə yoxlanıldı və
      <em>hamısı</em> gözlənildiyi kimi işlədi.</li>
  <li><strong>Mətn → ədəd çevrilməsi işləyir:</strong>
      <code>?limit=5&amp;seife=2</code> sorğusu
      <code>{seife: 2, limit: 5}</code> obyektinə çevrildi.</li>
  <li><strong>Standart dəyərlər işləyir:</strong> parametrsiz sorğu
      <code>{seife: 1, limit: 20, aktiv: 'aktiv', siralama: 'soyad', tertib: 'asc'}</code>
      verdi.</li>
  <li><strong>Həddlər qoruyur:</strong> <code>limit=0</code> və
      <code>limit=500</code> rədd edildi.</li>
  <li><strong>Ağ siyahı qoruyur:</strong>
      <code>siralama=parol</code> rədd edildi, yalnız icazəli sütunlar
      keçir.</li>
  <li><strong>Yad sahə tutulur:</strong> gövdədəki <code>yoluxucu</code>
      sahəsi <code>property yoluxucu should not exist</code> xətası verdi.</li>
</ul>
<p><strong>Vacib nəticə:</strong> bütün bu yoxlamalar bizim
<em>yazdığımız bir sətir <code>if</code> olmadan</em> işləyir. Yalnız
dekoratorlar sayəsində. Bu, NestJS-in əsas gücüdür: <strong>«nə
olmalıdır»</strong> deyirik, <strong>«necə yoxlanılır»</strong> isə
kitabxananın işidir.</p>
<p>Növbəti addımda bazadan gələn məlumatı <em>əks istiqamətdə</em>
emal edəcəyik. Orada bizi gözlənilməz bir problem gözləyir:
<code>bigint</code> və <code>Decimal</code> tipləri JSON-a
çevrilmir.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 18 — CAVAB MAPPER-İ VƏ BIGINT PROBLEMİ
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 18,
    "ad": "Cavab mapper-i — BigInt və Decimal problemi",
    "a": """
<p>Giriş məlumatını yoxlamağı öyrəndik. İndi <em>əks istiqamətə</em>
baxaq: bazadan gələn məlumatı istifadəçiyə necə göndəririk?</p>

<h4>İlk cəhd: sətri olduğu kimi qaytaraq</h4>
<p>Ən sadə fikir belədir: Prisma sətri nə qaytarırsa, onu da göndərək.
Axı niyə əlavə iş görək?</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const setir = await this.prisma.emekdaslar.findMany();
return setir;   // ← BELƏ ETMƏK OLMAZ!</pre>
<p>Bu kod <strong>işləməyəcək</strong>. Nest cavabı JSON-a çevirməyə
çalışanda bu xəta çıxacaq:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
TypeError: Do not know how to serialize a BigInt</pre>
<p>Və istifadəçi <code>500 Internal Server Error</code> görəcək. Niyə?</p>

<h4>Səbəb 1: <code>BigInt</code> — JavaScript-in xüsusi tipi</h4>
<p>Bazada <code>emekdaslar.id</code> sütunu <code>bigint</code> tipindədir.
Prisma onu JavaScript-in <code>BigInt</code> tipinə çevirir:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
console.log(typeof setir[0].id);   // "bigint"
console.log(setir[0].id);          // 1n     ← sonda "n" hərfi
console.log(setir[0].id + 1);      // 2n</pre>
<p><code>BigInt</code> JavaScript-ə <strong>sonradan</strong> əlavə olunub
(2019) və JSON standartı ondan <em>əvvəl</em> yaranıb. JSON-da BigInt üçün
heç bir yazılış forması yoxdur. Ona görə
<code>JSON.stringify(1n)</code> <em>qəsdən</em> xəta verir — JavaScript
sizə «bu dəyəri itirmədən necə yazacağımı bilmirəm» deyir.</p>
<p><strong>Niyə mətn kimi göndəririk?</strong> Çünki JavaScript
<code>number</code> tipi 2<sup>53</sup>-dən (təxminən 9 kvadrilyon) böyük
tam ədədləri <em>dəqiq saxlaya bilmir</em>:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
console.log(9007199254740993);      // 9007199254740992  ← 1 itdi!
console.log(9007199254740993n);     // 9007199254740993n ← dəqiq</pre>
<p>Bizim ID-lər hələ kiçikdir, amma <code>bigint</code> sütunu
<em>gələcəkdə</em> böyümək üçün seçilib (məsələn log cədvəlləri milyardlarla
sətir ola bilər). Ona görə <strong>ID-ni həmişə mətn kimi göndərin</strong>
— bu, beynəlxalq təcrübədir (Google, Twitter API-ləri də belə edir).</p>

<h4>Səbəb 2: <code>Decimal</code> — pul üçün dəqiq tip</h4>
<p><code>maas</code> sütunu <code>numeric(12,2)</code>-dir və Prisma onu
<code>Decimal</code> obyektinə çevirir. Niyə sadəcə <code>number</code>
deyil? Çünki <strong>sürüşən nöqtəli ədədlər pulla işləmək üçün
yararsızdır</strong>:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
console.log(0.1 + 0.2);          // 0.30000000000000004   ← ⚠️
console.log(0.1 + 0.2 === 0.3);  // false</pre>
<p>Bu, JavaScript-in səhvi deyil — <em>IEEE 754</em> standartının
təbiətidir. 0.1 ikilik sistemdə sonsuz kəsr verir. Bir maaş 3500.1
olsaydı və min sətir toplansaydı, hesabat <strong>qəpik səviyyəsində</strong>
səhv çıxardı. Ona görə pul üçün <code>Decimal</code> işlədilir.</p>
<p><code>Decimal</code> obyektini JSON-a çevirmək <em>olar</em> — Prisma
onun üçün <code>toJSON()</code> metodu təyin edib və nəticə mətn olur
(<code>"3500.00"</code>). Amma biz bunu <strong>açıq</strong> edirik:
<code>e.maas.toFixed(2)</code> — beləliklə <em>həmişə</em> iki onluq rəqəm
olur. API istehlakçısı (frontend) üçün bu, gözlənilən davranışdır.</p>

<h4>Həll: mapper funksiyası</h4>
<p><strong>Mapper</strong> — bir formadan digərinə çevirən funksiya.
Bizim halda: <em>baza sətri → API cavabı</em>. Bu, <strong>arxitektura
qərarıdır</strong> və çox mühümdür: baza strukturunu istifadəçiyə
<em>olduğu kimi</em> göstərmirik.</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Sahə</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Bazada</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">API-də</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Niyə?</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>id</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>bigint</code> (<code>1n</code>)</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>"1"</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">JSON BigInt bilmir</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>maas</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>Decimal</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>"3500.00"</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Pul dəqiqliyi</td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>dogum_tarixi</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>Date</code>
        (saatla)</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>"1978-04-12"</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Bizə yalnız gün lazımdır</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>cinsiyyet</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">əlaqə obyekti</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>{id, ad}</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Frontend <code>ad</code>-ı göstərsin</td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>vezifeler</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">cədvəl adı ilə</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>vezife</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Tək ədəd, cəm deyil</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>yas</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">yoxdur</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>48</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Hesablanır — deməli həmişə dəqiqdir</td>
  </tr>
</table>

<h4>⚠️ <code>select</code> — <code>include</code>-dan daha yaxşıdır</h4>
<p>Prisma-da əlaqələri qoşmaq üçün iki yol var:</p>
<ul>
  <li><code>include: { cinsiyyet: true }</code> — bütün sütunları gətirir.</li>
  <li><code>select: { cinsiyyet: { select: { id: true, ad: true } } }</code> —
      <strong>yalnız lazım olanları</strong>.</li>
</ul>
<p><code>cinsiyyet</code> cədvəlində 3 sütun var (<code>id</code>,
<code>ad</code>, <code>qisa_ad</code>), fərq kiçikdir. Amma
<code>emekdaslar</code> cədvəlində 18 sütun, <code>elmi_shura_uzvleri</code>
kimi cədvəllərdə isə onlarla sütun var. <code>include</code> ilə
<em>hamısı</em> bazadan oxunur və şəbəkə ilə ötürülür. 10 000 sətirlik
siyahıda bu, <strong>onlarla meqabayt</strong> lazımsız məlumat deməkdir.</p>
<p>Bizim yanaşmamız: <code>EMEKDAS_SECIM</code> adlı <em>bir</em> sabit
obyekt yazırıq və onu hər yerdə təkrar istifadə edirik. Beləliklə
siyahı, tək oxuma, yaratma və yeniləmə — hamısı <em>eyni</em> formanı
qaytarır. Frontend bir formanı öyrənir, hər yerdə işlədir.</p>
""",
    "anlayis": [
        ("BigInt",
         "JavaScript-in ixtiyari böyüklükdə tam ədəd tipi. <code>1n</code> "
         "kimi yazılır. JSON onu <em>dəstəkləmir</em>."),
        ("2^53 həddi",
         "<code>Number.MAX_SAFE_INTEGER</code> = 9007199254740991. Bundan "
         "böyük tam ədədlər <code>number</code> tipində dəqiqliyini itirir."),
        ("Decimal",
         "Dəqiq onluq ədəd tipi. Pul və faiz hesablamaları üçün. "
         "Sürüşən nöqtəli <code>number</code>-dən fərqli olaraq "
         "yuvarlaqlaşdırma səhvi vermir."),
        ("IEEE 754",
         "Kompyuterlərin onluq ədədləri saxlama standartı. "
         "<code>0.1 + 0.2 ≠ 0.3</code> olmasının səbəbi."),
        ("Mapper",
         "Bir formadan digərinə çevirən funksiya. Bizdə: xam baza sətri → "
         "API cavabı."),
        ("select / include",
         "Prisma-da hansı sütunların oxunacağını seçmək. "
         "<code>select</code> daha nəzarətli və yüngüldür."),
        ("toISOString()",
         "<code>Date</code> obyektini <code>2026-01-15T00:00:00.000Z</code> "
         "mətninə çevirir. <code>.slice(0, 10)</code> ilə yalnız günü "
         "götürürük."),
        ("toFixed(2)",
         "Ədədi iki onluq rəqəmlə mətnə çevirir: <code>3500</code> → "
         "<code>\"3500.00\"</code>."),
        ("UncheckedCreateInput",
         "Prisma tipi: xarici açarları <code>cinsiyyet_id</code> kimi "
         "birbaşa qəbul edir. <code>CreateInput</code> isə "
         "<code>connect</code> tələb edir."),
        ("GetPayload",
         "<code>Prisma.emekdaslarGetPayload&lt;{ select: typeof SECIM }&gt;</code> — "
         "seçim obyektindən nəticənin tipini <em>avtomatik</em> çıxarır. "
         "Əl ilə tip yazmaq lazım gəlmir."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) <code>EMEKDAS_SECIM</code> — bir dəfə yaz, hər yerdə işlət</h5>
<ul>
  <li><code>as const</code> — <strong>açar sözdür</strong>. Onsuz TypeScript
      bu obyektin tipini <code>{ id: boolean; ad: boolean; ... }</code>
      kimi ümumiləşdirər. <code>as const</code> ilə isə hər dəyər
      <em>literal</em> (<code>true</code>) olaraq qalır və
      <code>Prisma.emekdaslarGetPayload</code> ondan dəqiq nəticə tipini
      çıxara bilir.</li>
  <li><code>cinsiyyet: { select: { id: true, ad: true } }</code> — əlaqənin
      <em>içindən</em> də seçim edirik. Yəni <code>qisa_ad</code> sütunu
      bazadan <em>heç oxunmur</em> — bu, şəbəkə trafikini azaldır.</li>
  <li><code>EMEKDAS_SECIM</code> <code>select</code> kimi istifadə olunur:
      <code>findMany({ select: EMEKDAS_SECIM })</code>. Prisma obyekti
      <em>paylaşmaq</em> təhlükəsizdir, çünki Prisma onu dəyişmir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2) <code>EmekdasSetiri</code> — tipi avtomatik çıxarırıq</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export type EmekdasSetiri = Prisma.emekdaslarGetPayload&lt;{ select: typeof EMEKDAS_SECIM }&gt;;</pre>
<p>Bu sətri <em>əl ilə</em> yazmaq mümkün deyil — nəticə tipi çox
mürəkkəbdir (18 sütun + 7 əlaqə). <code>GetPayload</code> onu
seçim obyektindən <em>hesablayır</em>. Faydası: <code>EMEKDAS_SECIM</code>-ə
yeni sütun əlavə etsəniz, tip <strong>avtomatik</strong> yenilənir.
Əl ilə yazılmış tip isə köhnələr və səssizcə səhv olardı.</p>

<h5 style="color:#334155;margin-top:1rem">3) <code>EmekdasCavabi</code> — API müqaviləsi</h5>
<p>Bu, <code>interface</code>-dir (sinif deyil!), çünki burada
<em>yoxlama</em> lazım deyil — yalnız formanı təsvir edirik.
Diqqət yetirin, burada <code>bigint</code> və <code>Decimal</code>
<strong>yoxdur</strong>: yalnız <code>string</code>, <code>number</code>,
<code>boolean</code> və <code>null</code>. Yəni bu tip
<em>JSON-a təhlükəsiz çevrilir</em>.</p>

<h5 style="color:#334155;margin-top:1rem">4) <code>tarix()</code> köməkçisi</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
function tarix(d: Date | null): string | null {
  return d ? d.toISOString().slice(0, 10) : null;
}</pre>
<ul>
  <li><code>d ? ... : null</code> — <code>dogum_tarixi</code> bazada
      <em>nullable</em>-dır. <code>null</code> üçün
      <code>toISOString()</code> çağırsaq, «Cannot read properties of
      null» xətası alardıq.</li>
  <li><code>toISOString()</code> → <code>"1978-04-12T00:00:00.000Z"</code>.
      <code>slice(0, 10)</code> ilk 10 simvolu götürür →
      <code>"1978-04-12"</code>.</li>
  <li><strong>Niyə saatı atırıq?</strong> Çünki sütun
      <code>@db.Date</code>-dir — orada saat <em>yoxdur</em>.
      <code>T00:00:00.000Z</code> hissəsi sadəcə texniki əlavədir və
      frontend-i çaşdırır («niyə hamının doğum tarixi gecə yarısıdır?»).</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">5) <code>yasHesabla()</code> — düzgün yaş hesablanması</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
let yas = indi.getUTCFullYear() - d.getUTCFullYear();
const ayFerqi = indi.getUTCMonth() - d.getUTCMonth();
if (ayFerqi &lt; 0 || (ayFerqi === 0 &amp;&amp; indi.getUTCDate() &lt; d.getUTCDate())) {
  yas -= 1;
}</pre>
<p>Sadəlövh həll <code>indi.getFullYear() - d.getFullYear()</code> olardı —
və <strong>səhv</strong> olardı: 1978-12-31 doğumlu şəxs 2026-01-01-də
hələ 47 yaşındadır, sadəlövh hesablama isə 48 deyərdi. Biz ay və günü də
yoxlayırıq.</p>
<p><code>getUTC*</code> metodları işlədirik (yerli <code>getFullYear</code>
yox) — çünki <code>Date</code> obyekti UTC-də saxlanılır və server
başqa saat qurşağında olsa, yerli metodlar <em>bir gün</em> sürüşə bilər.</p>

<h5 style="color:#334155;margin-top:1rem">6) <code>hazirla()</code> — əsas funksiya</h5>
<ul>
  <li><code>id: String(e.id)</code> — BigInt → mətn. <strong>Ən vacib
      sətir.</strong></li>
  <li><code>tam_ad: `${e.soyad} ${e.ad} ${e.ata_adi}`</code> — şablon
      sətri (template literal). Rəsmi sənədlərdəki sıra: Soyad, Ad,
      Ata adı.</li>
  <li><code>cinsiyyet: e.cinsiyyet ? {...} : null</code> — əlaqə
      <em>nullable</em> ola bilər, ona görə yoxlayırıq. Diqqət: Prisma-da
      əlaqə sahəsinin adı <code>cinsiyyet</code>, cədvəlin adı da
      <code>cinsiyyet</code> — təsadüf deyil, sxemdə belə təyin olunub.</li>
  <li><code>vezifeler</code> → <code>vezife</code> — <strong>ad
      dəyişdiririk</strong>. Bazada cədvəl adı cəmdir
      (<code>vezifeler</code>), çünki bir əməkdaşın <em>bir</em>
      vəzifəsi var. API-də tək ad daha aydındır. Bu, mapper-in
      vəzifəsidir: baza adlarını <em>istifadəçiyə görə</em>
      düzəltmək.</li>
  <li><code>maas: e.maas === null ? null : e.maas.toFixed(2)</code> —
      <code>Decimal</code> → <code>"3500.00"</code>. Diqqət:
      <code>e.maas ? ...</code> yazsaydıq, <code>0.00</code> maaş
      <code>null</code> olardı! Yenə <code>=== null</code> yoxlaması.</li>
  <li><code>yaradilma: e.yaradilma.toISOString()</code> — bu sütun
      <code>Timestamptz</code>-dir (saatla), ona görə tam ISO göndəririk.
      Frontend özü yerli vaxta çevirəcək.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">7) <code>skriptler/mapper_yoxla.ts</code></h5>
<ul>
  <li>Skript <code>prisma.emekdaslar.findUnique({ where: { id: 1n } })</code>
      ilə ID 1-i oxuyur — <strong><code>1n</code></strong>, sadəcə
      <code>1</code> yox. Bu vacibdir: <code>1</code> yazsaq Prisma
      «Expected BigInt, provided Int» xətası verər.</li>
  <li>Əvvəlcə <code>JSON.stringify(xam)</code> çağırır və
      <code>try/catch</code> ilə xətanı <em>tutur</em> — proqram
      çökmür, xətanı göstərir.</li>
  <li>Sonra <code>hazirla(xam)</code> edib yenidən çalışır — və işləyir.</li>
  <li>Sonda fərq cədvəli çap edir: <code>bigint → string</code>,
      <code>object → string</code>. <em>Gözlə görünən</em> sübut.</li>
</ul>
""",
    "fayllar": [
        "src/emekdaslar/dto/emekdas-cavab.dto.ts",
        "skriptler/mapper_yoxla.ts",
    ],
    "goster": ["src/saglamliq/saglamliq.service.ts"],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then
  echo "  ✓ tip xətası yoxdur"
else
  echo "  ✗ tip xətası var"
fi

echo ""
echo "════ 2) Bazadaki REAL tiplər ════"
echo "  → PostgreSQL sütun tipləri:"
psql -U arti_user -h localhost -p 5432 -d arti_baza -At -c "
SELECT '      ' || column_name || ' : ' || data_type
  FROM information_schema.columns
 WHERE table_schema='kadrlar' AND table_name='emekdaslar'
   AND column_name IN ('id','maas','dogum_tarixi','yaradilma','ad')
 ORDER BY ordinal_position;" 2>/dev/null || echo "      (psql əlçatan deyil)"

echo ""
echo "  → JavaScript-də qarşılığı:"
echo "      bigint  → BigInt  (JSON-a ÇEVRİLMİR)"
echo "      numeric → Decimal (JSON-a çevrilir, amma mətn kimi)"
echo "      date    → Date    (ISO mətn kimi çevrilir)"

echo ""
echo "════ 3) CANLI sübut: mapper problemi həll edir ════"
npx tsx skriptler/mapper_yoxla.ts
""",
    "olmaz": """Mapper olmasa — sətir olduğu kimi qaytarılsa:

$ curl http://localhost:4000/api/v1/emekdaslar

HTTP/1.1 500 Internal Server Error

TypeError: Do not know how to serialize a BigInt
    at JSON.stringify (<anonymous>)
    at ExpressAdapter.reply
    at RouterResponseController.apply

  ← ⚠️ İstifadəçi «server sındı» düşünür. Loglarda isə
     anlaşılmaz bir TypeScript xətası var.

────────────────────────────────────────────────────────────
VƏ YA id-ni sadəcə Number()-ə çevirsək:

const setir = await prisma.emekdaslar.findMany();
return setir.map(e => ({ ...e, id: Number(e.id) }));

→ İşləyir... AMBIQ gələcəkdə:

$ node -e "console.log(Number(9223372036854775807n))"
9223372036854776000
  ← ⚠️ Dəyər DƏYİŞDİ! İki fərqli sətir eyni ID ala bilər
     və frontend yanlış əməkdaşı göstərər.

────────────────────────────────────────────────────────────
VƏ YA `include` ilə hər şeyi qaytarsaq:

SELECT id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi,
       vezife_id, shobe_id, merkez_id, email, telefon,
       is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama,
       maas, aktiv, yaradilma, ...
  ← ⚠️ 10 000 sətirlik siyahıda ~4 MB artıq trafik.
     Mobil şəbəkədə bu, 20 saniyə gözləmə deməkdir.""",
    "c_izah": """
<p><strong>Niyə bu problemi «kiçik» adlandırmaq olmaz?</strong> Çünki
<code>BigInt</code> xətası <em>yalnız</em> JSON-a çevirmə mərhələsində
çıxır — yəni servis işləyir, baza sorğusu uğurludur, TypeScript heç bir
xəta vermir. Səhv <strong>ən son mərhələdə</strong>, istifadəçiyə cavab
göndərilərkən ortaya çıxır. Bu tip xətaları tapmaq çətindir, çünki
<code>console.log(setir)</code> <em>düzgün</em> görünür:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
{ id: 1n, ad: 'Elnur', maas: Decimal { d: [3500], e: 0, s: 1 } }</pre>
<p>Konsol BigInt-i və Decimal-i <em>göstərir</em>, ona görə «hər şey
qaydasındadır» təəssüratı yaranır. Problem yalnız
<code>JSON.stringify</code> çağırılanda üzə çıxır.</p>
<p><strong>İkinci səbəb: mapper — təhlükəsizlik qatıdır.</strong> Təsəvvür
edin, bazaya sonradan <code>parol_hash</code> sütunu əlavə olundu
(<code>istifadeciler</code> cədvəlində artıq var!). Əgər sətri olduğu
kimi qaytarsaydıq, bu sütun <strong>avtomatik olaraq</strong> API
cavabına düşərdi — heç kim fərqinə varmadan. Mapper ilə isə yalnız
<em>açıq şəkildə sadalanmış</em> sahələr göndərilir. Yeni sütun
əlavə olunsa, heç nə sızmır.</p>
<p><strong>Üçüncüsü: <code>select</code> performans deməkdir.</strong>
Bazadan oxunan hər bayt əvvəlcə serverin yaddaşına, sonra şəbəkəyə,
sonra frontend-in yaddaşına gedir. 18 sütun yerinə 11 sütun oxumaq
<strong>40% az</strong> məlumat deməkdir. 14 sətirdə hiss olunmur;
100 000 sətirdə isə fərq saniyələrlə ölçülür.</p>
<p><strong>Dördüncüsü: <code>mapper_yoxla.ts</code> — sübutun
avtomatlaşdırılması.</strong> «BigInt JSON-a çevrilmir» cümləsini
<em>oxumaq</em> bir şeydir, <em>görmək</em> isə tamam başqadır. Skript
hər iki halı yan-yana qoyur: xəta və həll. Bundan sonra bu problemi
bir daha yaşamayacaqsınız — çünki mexanizmi öz gözünüzlə gördünüz.</p>
""",
    "sual": [
        ("Niyə sadəcə <code>BigInt.prototype.toJSON</code> yazmırıq? "
         "Bir sətirlə həll olunmazdı?",
         "Olar və bəzi layihələr belə edir: "
         "<code>BigInt.prototype.toJSON = function() { return this.toString() }</code>. "
         "Amma bu, <strong>qlobal <code>prototype</code>-i dəyişməkdir</strong> — "
         "yəni bütün proqramda, o cümlədən kitabxanalarda. Riskli və gizli "
         "yan təsirləri var. Mapper isə <em>açıq</em> və <em>yerdə</em> "
         "edir: cavabın hansı sahələrinin mətn olduğunu kodda görürsünüz."),
        ("<code>maas</code>-ı mətn yox, ədəd göndərsəm frontend-ə problem olar?",
         "Qismən. Kiçik maaşlarda (3500.00) heç bir fərq yoxdur. Amma "
         "frontend-də <code>Number(\"3500.00\")</code> edib yenidən "
         "hesablamalar aparsanız, sürüşən nöqtə səhvi geri qayıdır. "
         "Beynəlxalq təcrübə: <strong>pulu həmişə mətn kimi ötür, "
         "hesablamanı backend et</strong>. Stripe, PayPal və digər ödəniş "
         "API-ləri belə edir."),
        ("<code>yas</code> sahəsini hər cavabda hesablamaq baha deyilmi?",
         "Bir <code>Date</code> çıxması və iki müqayisədir — praktikada "
         "heç nə. Əsl faydası: yaş <em>heç vaxt köhnəlmir</em>. "
         "Bazada saxlasaydıq, hər ad günündə bütün sətirləri yeniləmək "
         "lazım gələrdi (və ya cron işi yazmalı olardıq). Hesablanan "
         "dəyər həmişə dəqiqdir."),
        ("Niyə <code>elmi_shura_uzvleri</code> kimi əlaqələri qoşmuruq?",
         "Çünki bu addımda <em>bir</em> əməkdaşın əsas kartını göstəririk. "
         "Bir əməkdaşın 4 doktorantı, 1 şura üzvlüyü, 1 sertifikatı ola "
         "bilər — hamısını hər siyahı sorğusuna qoşsaq, cavab "
         "<strong>partlayar</strong> (ingiliscə buna <em>cartesian "
         "explosion</em> deyilir). Bu əlaqələr ayrı endpoint-lərlə "
         "verilməlidir — 2B dərsinin mövzusudur."),
        ("<code>EMEKDAS_SECIM</code>-i faylda <code>const</code> kimi "
         "saxlamaq yaxşıdır? Adətən sabitlər ayrı faylda olur.",
         "Ümumiyyətlə haqlısınız. Amma bu sabit <em>yalnız</em> bu DTO "
         "ilə mənalıdır — onu cavab tipi ilə bir yerdə saxlamaq "
         "birləşməni (cohesion) gücləndirir. Praktik qayda: sabiti "
         "onu <strong>istifadə edən ən yaxın yerə</strong> qoy. "
         "İki-üç modul istifadə etməyə başlasa, o zaman ayrı fayla "
         "köçürmək lazımdır."),
        ("<code>toFixed(2)</code> yuvarlaqlaşdırır. Bu, məlumat itkisi deyilmi?",
         "Bazada <code>numeric(12,2)</code>-dir — yəni orada <em>artıq</em> "
         "iki onluqdan çox rəqəm yoxdur. <code>toFixed(2)</code> heç nəyi "
         "dəyişmir, sadəcə göstərişi səliqəli edir "
         "(<code>3500</code> → <code>\"3500.00\"</code>). Əgər sütun "
         "<code>numeric(12,4)</code> olsaydı, məlumat itkisi olardı — "
         "o zaman <code>toFixed(4)</code> yazmalı olardıq."),
        ("Bu mapper-i hər servisdə təkrar yazacağıqmı?",
         "Hər servisin <em>öz</em> mapper-i olur, çünki hər resursun "
         "sahələri fərqlidir. Amma ümumi köməkçilər "
         "(<code>tarix()</code>, <code>yasHesabla()</code>) "
         "<code>src/common/</code> qovluğuna köçürülə bilər. "
         "Qayda: <strong>iki dəfə təkrar etsən — çıxar</strong>. "
         "Bizdə hələ bir servis var, ona görə gözləyirik."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li><strong>Problem canlı görüldü:</strong> xam baza sətrini
      <code>JSON.stringify</code> etmək
      <code>Do not know how to serialize a BigInt</code> xətası verdi.
      Əgər mapper olmasaydı, API <code>500</code> qaytarardı.</li>
  <li><strong>Həll təsdiqləndi:</strong> <code>hazirla()</code>-dan sonra
      həmin sərt <em>problemsiz</em> JSON-a çevrildi — 525 simvol,
      içində bir dənə də <code>bigint</code> və ya
      <code>Decimal</code> yoxdur.</li>
  <li><strong>Tip çevrilmələri:</strong>
      <code>bigint → string</code>, <code>Decimal(object) → string</code>,
      <code>Date(object) → "YYYY-MM-DD"</code>,
      <code>vezifeler → vezife</code> (ad dəyişdi),
      <code>yas</code> hesablandı.</li>
  <li><strong>Mövcud bazadan real məlumat:</strong> ID 1 — Əliyev Elnur
      Qəzənfər, Direktor, 3500.00 AZN, 48 yaş, Fəlsəfə doktoru, Dosent.</li>
</ul>
<p><strong>Ən vacib dərs:</strong> <em>baza tipini birbaşa istifadəçiyə
göstərmə</em>. Bu, həm <code>BigInt</code> kimi texniki problemləri
həll edir, həm təhlükəsizlik qatı yaradır (yeni sütunlar avtomatik
sızmır), həm də API-ni <strong>sabit müqavilə</strong> edir: baza
strukturu dəyişsə də, frontend heç nə hiss etmir.</p>
<p>Növbəti addımda bu mapper-i və <code>select</code>-i işlədən
<strong>servisi</strong> yazacağıq: səhifələmə, axtarış, filtr və
CRUD əməliyyatları.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 19 — SERVİS
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 19,
    "ad": "Servis — Prisma ilə CRUD, səhifələmə və xəta çevirməsi",
    "a": """
<p>Laylı arxitekturada (layered architecture) hər hissənin <em>bir</em>
işi var:</p>
<table style="width:100%;border-collapse:collapse;font-size:.93rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Qat</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">İşi</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Bilməməli olduğu</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Controller</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">HTTP: hansı yol, hansı metod,
        hansı status kodu</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">SQL, Prisma, biznes qaydaları</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Service</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Biznes məntiqi, baza sorğuları,
        qaydalar</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">HTTP nədir, hansı status
        kodu qaytarılır</td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Prisma</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">SQL yazmaq, bağlantı, tiplər</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Biznes qaydaları</td>
  </tr>
</table>
<p>Bu ayrılıq niyə vacibdir? Çünki <strong>eyni servisi</strong> həm HTTP
controller, həm cron işi, həm CLI skripti, həm də test çağıra bilər.
Servis «HTTP-dən xəbərsiz» olsa, onu istənilən yerdə işlətmək olar.
Bizim <code>skriptler/servis_yoxla.ts</code> faylı məhz bunun
<em>canlı sübutudur</em>: servisi HTTP olmadan çağırır.</p>

<h4>Səhifələmə (pagination) — niyə mütləqdir?</h4>
<p>Təsəvvür edin, API <code>GET /emekdaslar</code> sorğusuna
<strong>bütün</strong> sətirləri qaytarır. 14 sətirdə problem yoxdur.
Amma <code>audit_log</code> cədvəlində milyonlarla sətir olacaq. Üç
problem yaranır:</p>
<ol>
  <li><strong>Yaddaş.</strong> Server milyon sətri RAM-a yükləyər.</li>
  <li><strong>Şəbəkə.</strong> Cavab yüzlərlə meqabayt olar.</li>
  <li><strong>Frontend.</strong> Brauzer belə cavabı göstərə bilməz.</li>
</ol>
<p>Həll: <strong>səhifələmə</strong>. İstifadəçi deyir «mənə 20-ci
səhifədən 20 sətir ver». Prisma-da iki parametr var:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
skip: (sehife - 1) * limit,   // neçə sətri ATLA
take: limit,                  // neçəsini GÖTÜR</pre>
<p>Riyaziyyat sadədir: 3-cü səhifə, hər səhifədə 20 sətir →
<code>(3-1) × 20 = 40</code> sətri atla, sonrakı 20-ni götür.</p>
<p>⚠️ <strong>Klassik səhv:</strong> <code>skip: sehife * limit</code>
yazmaq. O zaman 1-ci səhifə ilk 20 sətri <em>atlayar</em> və istifadəçi
onları heç vaxt görməz. <code>(sehife - 1)</code> mütləqdir.</p>

<h4>⚠️ <code>$transaction</code> — cem və siyahı bir yerdə</h4>
<p>İstifadəçiyə iki şey lazımdır: <em>neçə səhifə var</em> və
<em>bu səhifədəki sətirlər</em>. Sadəlövh həll iki ayrı sorğu göndərməkdir:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const cem = await this.prisma.emekdaslar.count({ where });
const setirler = await this.prisma.emekdaslar.findMany({ where, ... });</pre>
<p>Problem: <strong>aradakı boşluqda</strong> başqa bir istifadəçi yeni
əməkdaş əlavə edə bilər. Nəticədə <code>cem = 15</code>, amma
<code>melumat.length = 14</code> ola bilər. Frontend «15 nəticə var,
14-ü göstərirəm» deyə çaşar.</p>
<p>Həll: hər iki sorğunu <em>bir tranzaksiyada</em> göndərmək:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const [cem, setirler] = await this.prisma.$transaction([
  this.prisma.emekdaslar.count({ where }),
  this.prisma.emekdaslar.findMany({ where, ... }),
]);</pre>
<p>Prisma <strong>massiv formasında</strong> <code>$transaction</code>
işlədəndə hər iki sorğunu <em>eyni</em> tranzaksiyada icra edir — yəni
ikisi arasında heç nə dəyişə bilməz. Üstəlik <em>daha sürətlidir</em>:
şəbəkə gediş-gəlişi bir dəfədir, iki dəfə yox.</p>

<h4>Xəta çevirməsi — <code>cevir()</code> niyə lazımdır?</h4>
<p>Prisma xətaları texnikidir: <code>P2002</code>,
<code>P2003</code>. HTTP cavabında bunlar görünməməlidir. Hər kodun
<em>bir</em> HTTP qarşılığı var:</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Prisma</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Mənası</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">HTTP</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>P2002</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Unikal sütunda təkrar
        (bizdə <code>email</code>)</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>409 TOQQUSMA</code></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>P2003</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Xarici açar pozuldu
        (olmayan <code>vezife_id</code>)</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>400 YANLIS_SORGU</code></td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>P2025</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Yeniləmə/silmə üçün sətir
        tapılmadı</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>404 TAPILMADI</code></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0">digər</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Gözlənilməz</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>400</code> + loq</td>
  </tr>
</table>
<p>Niyə <code>409</code>? Çünki <strong>404</strong> «resurs yoxdur»,
<strong>400</strong> «sorğunuz səhvdir», <strong>409 Conflict</strong> isə
«sorğunuz düzgündür, amma sistemin cari vəziyyəti ilə ziddiyyət təşkil
edir» deməkdir. E-poçtun təkrar olması məhz budur: sorğu səhv deyil,
sadəcə həmin e-poçt artıq mövcuddur.</p>

<h4>⚠️ Silmə: <code>delete</code> yox, <em>yumşaq silmə</em></h4>
<p>Bu, dərsin ən vacib arxitektura qərarıdır. <code>emekdaslar</code>
cədvəlinə <strong>16 cədvəl</strong> bağlıdır. Onların bir hissəsi
<code>onDelete: Cascade</code> ilə bağlıdır (əlaqəli sətirlər
<em>avtomatik silinir</em>), digərləri isə <code>NoAction</code> ilə
(<em>silməyə icazə verilmir</em>).</p>
<table style="width:100%;border-collapse:collapse;font-size:.88rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Cədvəl</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Davranış</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Nəticə</th>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>mezuniyyetler</code>,
        <code>vezife_teyinatlari</code>, <code>rehberlik</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>Cascade</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Əməkdaşla birlikdə
        <strong>silinir</strong></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>doktorantlar</code>,
        <code>istifadeciler</code>, <code>elmi_shura_uzvleri</code>,
        <code>sertifikasiya</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>NoAction</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Silməyə <strong>icazə
        verilmir</strong> (<code>P2003</code>)</td>
  </tr>
</table>
<p>Bizim 14 əməkdaşın <strong>hamısının</strong> ən azı bir
<code>rehberlik</code> və ya <code>elmi_shura_uzvleri</code> sətri var.
Yəni hamısı «silinməz»dir. Bu, səhv deyil — <em>qəsdən</em> belədir:
PostgreSQL sizə «bu şəxsin doktorantları var, onları yetim buraxmaq
istəyirsinizmi?» deyir.</p>
<p>Real həyatda isə belə olur: <strong>əməkdaş işdən çıxır, amma
məlumatı qalmalıdır</strong>. Keçmiş illərin hesabatları, elmi işlərin
rəhbərlik tarixçəsi, şura qərarları — hamısı həmin ada bağlıdır. Ona
görə bizim <code>sil()</code> metodu <em>iki</em> strategiya işlədir:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
asılı qeyd VARSA → YUMŞAQ SİLMƏ  (aktiv = false)
asılı qeyd YOXDURSA → ADİ SİLMƏ  (sətir bazadan çıxır)</pre>
<p>Bu yanaşmanın adı <strong>soft delete</strong> (yumşaq silmə) və
<em>hard delete</em> (sərt silmə) fərqidir. Sənaye standartı budur:
əksər ciddi sistemlər heç vaxt həqiqi silmə etmir.</p>

<h4>Axtarış: <code>contains</code> + <code>mode: 'insensitive'</code></h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
where.OR = [
  { ad:    { contains: sorgu.axtar, mode: 'insensitive' } },
  { soyad: { contains: sorgu.axtar, mode: 'insensitive' } },
  { ata_adi: { contains: sorgu.axtar, mode: 'insensitive' } },
  { email: { contains: sorgu.axtar, mode: 'insensitive' } },
];</pre>
<ul>
  <li><code>OR</code> — «bunlardan <em>hər hansı biri</em> uyğun gəlsə».</li>
  <li><code>contains</code> — SQL-də <code>LIKE '%mətn%'</code>. Yəni
      axtarış sözü adın <em>içində</em> də ola bilər.</li>
  <li><code>mode: 'insensitive'</code> — böyük-kiçik hərf fərqini
      görməməzlik. Bunun üçün PostgreSQL-də <code>ILIKE</code>
      işlədilir.</li>
</ul>
<p>⚠️ <strong>Azərbaycan hərfləri ilə diqqət:</strong>
<code>insensitive</code> rejimi <em>Unicode</em> səviyyəsində işləyir,
amma <code>İ</code>/<code>i</code> və <code>I</code>/<code>ı</code>
cütlükləri Türk dillərində xüsusi haldır. Test edin — bizim nümunədə
<code>əliyev</code> və <code>ƏLİYEV</code> hər ikisi 2 nəticə verir,
yəni işləyir.</p>
""",
    "anlayis": [
        ("Laylı arxitektura",
         "Proqramı məsuliyyətə görə qatlara bölmək: controller (HTTP), "
         "service (məntiq), data (baza). Hər qat yalnız öz işini bilir."),
        ("Səhifələmə (pagination)",
         "Böyük nəticə dəstini kiçik hissələrlə vermək. "
         "<code>skip</code> + <code>take</code>."),
        ("skip / take",
         "Prisma-da «neçə sətri atla» / «neçəsini götür». SQL-də "
         "<code>OFFSET</code> / <code>LIMIT</code>."),
        ("$transaction",
         "Bir neçə sorğunu <em>atomik</em> şəkildə — ya hamısı, ya heç biri — "
         "icra etmək. Massiv forması eyni tranzaksiyada paralel işlədir."),
        ("P2002 / P2003 / P2025",
         "Prisma-nın bilinən xəta kodları: unikal pozuntu / xarici açar "
         "pozuntusu / sətir tapılmadı."),
        ("409 Conflict",
         "«Sorğu düzgündür, amma sistemin vəziyyəti ilə ziddiyyətdir». "
         "Təkrar e-poçt üçün doğru koddur."),
        ("Yumşaq silmə (soft delete)",
         "Sətri bazadan çıxarmaq yerinə <code>aktiv = false</code> etmək. "
         "Tarixi məlumat qorunur, əlaqələr pozulmur."),
        ("Cascade / NoAction",
         "Xarici açar davranışı: <code>Cascade</code> — əlaqəli sətirlər "
         "silinir; <code>NoAction</code> — silməyə icazə verilmir."),
        ("contains / mode",
         "Prisma-da mətn axtarışı. <code>insensitive</code> hərf "
         "böyüklüyünü nəzərə almır."),
        ("Mapper-in servisdə işlədilməsi",
         "<code>setirler.map(hazirla)</code> — massivin hər elementini "
         "mapper-dən keçirir. Qısa yol: <code>.map(funksiya)</code>."),
        ("Logger",
         "Nest-in daxili loq aləti. <code>log</code> / <code>warn</code> / "
         "<code>error</code> səviyyələri var; yazılan mesaj server "
         "loqunda görünür."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) İki cavab interfeysi</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export interface SehifeCavabi {
  ugur: true; sehife: number; limit: number;
  cem: number; sehife_sayi: number;
  melumat: EmekdasCavabi[];
}</pre>
<ul>
  <li><code>ugur: true</code> — <em>literal tip</em>. Bu sahə yalnız
      <code>true</code> ola bilər. Niyə? Çünki 1A-nın ADDIM 8-ində
      xətalar üçün <code>ugur: false</code> formatını təyin etmişdik.
      İndi frontend sadəcə <code>if (cavab.ugur)</code> yazır və
      TypeScript hansı formanın gözlənildiyini <em>özü</em> bilir.</li>
  <li><code>sehife_sayi</code> — <code>Math.ceil(cem / limit)</code>.
      Frontend «1 2 3 … 7» düymələrini bununla çəkir. Serverdə hesablamaq
      daha yaxşıdır: frontend riyaziyyatla məşğul olmasın.</li>
  <li><code>melumat</code> — sətirlər massivi. Adı <code>data</code> da ola
      bilərdi; Azərbaycan adlandırması seçdiyimiz üçün
      <code>melumat</code>.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2) <code>hamisi()</code> — oxuma</h5>
<ul>
  <li><code>const where: Prisma.emekdaslarWhereInput = {};</code> —
      <strong>sorğu obyekti</strong>. Əvvəlcə boşdur; şərtlər yalnız
      <em>verildikdə</em> əlavə olunur. Alternativ — hər halda
      <code>where: { aktiv: true, axtar: undefined }</code> yazmaq —
      işləyər, amma lazımsız şərtlər SQL-i şişirdər.</li>
  <li><code>if (sorgu.aktiv === 'aktiv')</code> — <strong>üç hal</strong>
      var: <code>aktiv</code> → <code>where.aktiv = true</code>,
      <code>passiv</code> → <code>false</code>,
      <code>hamisi</code> → <em>heç bir şərt qoymuruq</em>. Sonuncu vacibdir:
      <code>where.aktiv = undefined</code> yazsaq Prisma onu
      işlədərdi? Xeyr, işlətməzdi — amma şərti <em>heç yazmamaq</em>
      daha aydındır.</li>
  <li><code>if (sorgu.merkez_id !== undefined)</code> — yenə
      <code>!== undefined</code>. <code>if (sorgu.merkez_id)</code>
      yazsaydıq, <code>merkez_id = 0</code> olan sətirlər filtrdən
      yan keçərdi. Bizim ID-lər 1-dən başlayır, amma bu,
      <em>təsadüfdür</em> — koda güvənmək olmaz.</li>
  <li><code>const orderBy = { [sorgu.siralama]: sorgu.tertib } as Prisma.emekdaslarOrderByWithRelationInput;</code> —
      <strong>hesablanan açar</strong> (computed key). Obyektin açarı
      dəyişən ola bilər: <code>{ [x]: y }</code>. <code>as</code> isə
      TypeScript-ə «bu düzgün tipdir, inan mənə» deyir. Təhlükəsizlik
      DTO-daki <code>@IsIn</code> ilə təmin olunur — yəni
      <code>as</code> <em>yalnız</em> tip üçündür, işləmə vaxtı yoxlama
      deyil.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3) <code>biri()</code> — tək oxuma</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const setir = await this.prisma.emekdaslar.findUnique({
  where: { id: BigInt(id) },
  select: EMEKDAS_SECIM,
});
if (!setir) throw new NotFoundException(`ID ${id} olan əməkdaş tapılmadı`);</pre>
<ul>
  <li><code>findUnique</code> — Prisma-nın <em>unikal</em> sütun üzrə
      axtarışı. <code>id</code> birincil açardır, ona görə
      <code>findUnique</code> mümkündür və <code>findFirst</code>-dan
      sürətlidir.</li>
  <li><code>BigInt(id)</code> — <strong>mütləqdir</strong>. Controller-dən
      gələn <code>id</code> JavaScript <code>number</code>-dir
      (<code>ParseIntPipe</code> onu elə edib), Prisma isə
      <code>BigInt</code> gözləyir. Yazmasaq:
      <code>Argument \`id\`: Invalid value provided. Expected BigInt,
      provided Int.</code></li>
  <li><code>if (!setir)</code> — Prisma tapılmayanda <code>null</code>
      qaytarır (<em>xəta atmır</em>). Ona görə bu yoxlama bizim
      məsuliyyətimizdir. <code>update</code> və <code>delete</code> isə
      <em>xəta atır</em> (<code>P2025</code>) — bu fərqi yadda saxlayın.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">4) <code>yarat()</code> — yaratma</h5>
<ul>
  <li><code>Prisma.emekdaslarUncheckedCreateInput</code> — <strong>checked</strong>
      versiyasında xarici açarlar belə yazılır:
      <code>cinsiyyet: { connect: { id: dto.cinsiyyet_id } }</code>.
      <strong>Unchecked</strong> versiyasında isə birbaşa:
      <code>cinsiyyet_id: dto.cinsiyyet_id</code>. Biz sadə olanı seçirik.
      ⚠️ İkisini qarışdırmaq olmaz: <code>UncheckedCreateInput</code>-da
      <code>cinsiyyet: {...}</code> yazsanız TypeScript xəta verər.</li>
  <li><code>ad: dto.ad.trim()</code> — <strong>təmizləmə</strong>.
      <code>"  Elnur  "</code> kimi dəyər bazaya düşsə, axtarışda
      tapılmaz və hesabatda səliqəsiz görünər. <code>.trim()</code>
      boşluqları kənardan silir.</li>
  <li><code>is_status_id: dto.is_status_id ?? 1</code> — <em>nullish
      coalescing</em>. «Əgər <code>null</code> və ya
      <code>undefined</code>-dirsə, 1 götür». Diqqət:
      <code>||</code> işlətmək <em>səhv</em> olardı — çünki
      <code>0 || 1</code> da 1 verir. <code>??</code> yalnız
      <code>null</code>/<code>undefined</code> üçün işləyir.
      <code>is_status_id = 0</code> olsaydı (belə ID yoxdur, amma
      prinsipcə), <code>??</code> onu saxlayardı.</li>
  <li><code>dogum_tarixi: gun(dto.dogum_tarixi)</code> — köməkçi
      funksiya. Aşağıda izah olunub.</li>
  <li><code>try/catch</code> + <code>throw this.cevir(x)</code> —
      Prisma xətasını HTTP xətasına çeviririk. <code>throw</code>
      mütləqdir: <code>cevir</code> <em>qaytarır</em>, atmaq isə
      çağıranın işidir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">5) <code>yenile()</code> — qismən yeniləmə</h5>
<ul>
  <li><strong>⚠️ Bu addımın ən böyük tələsi:</strong>
      <code>Object.keys(dto)</code> <em>işləmir</em>!
      <code>tsconfig.json</code>-da <code>target: ES2023</code>-dür və bu,
      TypeScript-in <code>useDefineForClassFields</code> davranışını işə
      salır: sinifdə elan olunan <strong>hər</strong> sahə, dəyəri
      <code>undefined</code> olsa da, obyektdə <em>açar</em> kimi mövcud
      olur. Yəni istifadəçi <code>{}</code> göndərsə belə,
      <code>Object.keys(dto).length</code> <strong>16</strong> qaytarır və
      boş-gövdə qoruyucusu <em>heç vaxt işləmir</em>. Düzgün yol —
      yalnız <code>undefined</code> olmayanları saymaq:</li>
</ul>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const verilen = Object.entries(dto)
  .filter(([, deyer]) =&gt; deyer !== undefined)
  .map(([ad]) =&gt; ad);

if (verilen.length === 0) {
  throw new BadRequestException('Yeniləmək üçün ən azı bir sahə göndərilməlidir');
}</pre>
<ul>
  <li><code>Object.entries(dto)</code> — <code>[açar, dəyər]</code>
      cütlərindən ibarət massiv.</li>
  <li><code>.filter(([, deyer]) =&gt; deyer !== undefined)</code> —
      <em>destrukturizasiya</em> ilə ikinci elementi (dəyəri) götürür və
      yalnız həqiqətən göndərilənləri saxlayır. Birinci elementin adı
      lazım olmadığı üçün boş buraxılıb:
      <code>[, deyer]</code>.</li>
  <li><code>.map(([ad]) =&gt; ad)</code> — qalan cütlərdən yalnız
      açarları çıxarır. Nəticə: <code>['maas']</code> kimi siyahı —
      loq mesajında istifadə olunur.</li>
  <li><code>if (verilen.length === 0) throw new BadRequestException(...)</code> —
      boş PATCH mənasızdır. 400 qaytarırıq. <em>Alternativ:</em>
      dəyişməmiş sətri qaytarmaq da olar (idempotentlik üçün), amma
      aydın xəta mesajı daha faydalıdır.</li>
  <li><code>if (dto.ad !== undefined) data.ad = dto.ad.trim();</code> —
      <strong>16 belə sətir</strong>. Uzundur, amma <em>açıqdır</em>.
      Qısa yol <code>data = { ...dto }</code> olardı — amma o zaman
      DTO-nun <code>cinsiyyet_id</code> kimi sahələri birbaşa
      Prisma-ya gedərdi və <code>dogum_tarixi</code> mətni
      <code>Date</code>-ə çevrilməzdi. Açıq yazmaq <em>çevrilməni</em>
      mümkün edir.</li>
  <li>⚠️ <code>prisma.update</code> tapılmayanda <code>P2025</code>
      atır — onu <code>cevir()</code> tutub <code>404</code> edir.
      Ona görə burada ayrıca <code>findUnique</code> yoxlaması
      lazım deyil.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">6) <code>sil()</code> — iki strategiya</h5>
<ul>
  <li>Əvvəlcə <code>findUnique</code> ilə sətri <em>tapırıq</em> —
      çünki mövcud olmayan ID üçün <code>404</code> qaytarmalıyıq
      (silmə cəhdi deyil).</li>
  <li><code>asililariSay(id)</code> — 7 cədvəli bir tranzaksiyada sayır.
      Nəticə obyekt kimi qaytarılır: istifadəçi <em>hansı</em>
      qeydlərin mane olduğunu görür.</li>
  <li><code>Object.values(asili).reduce((a, b) =&gt; a + b, 0)</code> —
      bütün sayları toplayır. <code>reduce</code>-un ikinci arqumenti
      (<code>0</code>) <em>başlanğıc dəyəridir</em>; onsuz boş massiv
      xəta verərdi.</li>
  <li><code>this.log.warn(...)</code> — yumşaq silmə <strong>log
      səviyyəsində xəbərdarlıqdır</strong>. Çünki bu, diqqət tələb edən
      hadisədir: kimsə əməkdaşı «sildi», halbuki sətir bazada qaldı.
      Gələcəkdə audit üçün bu qeyd lazım ola bilər.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">7) <code>gun()</code> köməkçisi və saat qurşağı tələsi</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
function gun(m: string | undefined): Date | null {
  return m ? new Date(`${m}T00:00:00Z`) : null;
}</pre>
<p>Niyə sadəcə <code>new Date('1990-05-12')</code> yazmırıq? Çünki
JavaScript bu formatı <strong>UTC kimi</strong> oxuyur, sonra isə
<code>Date</code> obyektini <em>yerli</em> vaxtda göstərir. Azərbaycan
UTC+4 olduğu üçün nəticə <code>1990-05-12T04:00:00+04:00</code> olur —
yəni gün eynidir. Amma server UTC-5-də olsaydı (Amerika), nəticə
<code>1990-05-11T19:00:00-05:00</code> olardı və bazaya <strong>11 may</strong>
yazılardı! Bir gün sürüşməsi — doğum tarixlərində ciddi səhvdir.</p>
<p><code>T00:00:00Z</code> yazmaqla biz <em>açıq</em> şəkildə «gecə
yarısı UTC» deyirik. Bu, hər saat qurşağında sabit nəticə verir.</p>

<h5 style="color:#334155;margin-top:1rem">8) <code>skriptler/servis_yoxla.ts</code></h5>
<ul>
  <li><code>import 'reflect-metadata'</code> və
      <code>import 'dotenv/config'</code> — <strong>birinci iki
      sətir</strong>. Birincisi dekoratorlar üçün, ikincisi
      <code>.env</code>-dən <code>DATABASE_URL</code> oxumaq üçün.
      Sıra vacibdir: <code>dotenv</code> PrismaService-dən əvvəl
      işləməlidir.</li>
  <li><code>new PrismaService()</code> — Nest konteyneri olmadan
      <em>əl ilə</em> yaradırıq. Servisin konstruktoru sadəcə adapter
      qurur, bağlantı isə <code>onModuleInit()</code>-də açılır — ona
      görə onu <em>əl ilə</em> çağırırıq.</li>
  <li><code>try / finally</code> — <code>finally</code> bloku
      <strong>həmişə</strong> işləyir: xəta olsa da, olmasa da.
      Müvəqqəti sətirlərin təmizlənməsi orada yazılıb. Bu olmasa,
      skript yarıda çöksə, bazada zibil sətirlər qalardı.</li>
  <li><code>await prisma.$transaction(async (tx) =&gt; { ... })</code> —
      <strong>callback forması</strong>. Burada silmə cəhdi edirik və
      dərhal sonra <code>throw</code> — nəticə <em>heç vaxt commit
      olunmur</em>. Yəni real məlumat təhlükədə deyil.</li>
  <li><code>process.exit(0 / 1)</code> — skriptin çıxış kodu. Bash
      üçün bu, «test keçdi / keçmədi» deməkdir.</li>
</ul>
""",
    "fayllar": [
        "src/emekdaslar/emekdaslar.service.ts",
        "skriptler/servis_yoxla.ts",
    ],
    "goster": ["src/prisma/prisma.service.ts"],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then
  echo "  ✓ tip xətası yoxdur"
else
  echo "  ✗ tip xətası var"
fi

echo ""
echo "════ 2) Servisin strukturu ════"
printf '      sətir sayı      : %s\n' "$(wc -l < src/emekdaslar/emekdaslar.service.ts | tr -d ' ')"
printf '      public metodlar : %s\n' "$(grep -cE '^  async [a-z]' src/emekdaslar/emekdaslar.service.ts)"
grep -nE '^  async [a-z]' src/emekdaslar/emekdaslar.service.ts | sed 's/^/      /'

echo ""
echo "════ 3) Bazadaki asılılıq (silmə üçün vacib) ════"
psql -U arti_user -h localhost -p 5432 -d arti_baza -c "
SELECT
  (SELECT count(*) FROM kadrlar.mezuniyyetler m
     JOIN kadrlar.emekdaslar e ON e.id = m.emekdas_id) AS cascade_olan,
  (SELECT count(*) FROM struktur.elmi_shura_uzvleri s
     WHERE s.emekdas_id IS NOT NULL) AS bloklayan_shura,
  (SELECT count(*) FROM elm.doktorantlar d
     WHERE d.rehber_id IS NOT NULL) AS bloklayan_doktorant;" 2>/dev/null | sed 's/^/      /'

echo ""
echo "════ 4) CANLI: servisin bütün əməliyyatları ════"
npx tsx skriptler/servis_yoxla.ts
""",
    "olmaz": """`cevir()` olmasa — Prisma xətası birbaşa istifadəçiyə getsəydi:

$ curl -X POST http://localhost:4000/api/v1/emekdaslar \\
    -H 'Content-Type: application/json' \\
    -d '{"ad":"Test","soyad":"Test","ata_adi":"Test",
         "cinsiyyet_id":1,"vezife_id":6,
         "email":"elnur.eliyev@arti.edu.az"}'

HTTP/1.1 500 Internal Server Error
{"ugur":false,"xeta":{"kod":"DAXILI_XETA",
 "mesaj":"\\nInvalid `prisma.emekdaslar.create()` invocation:\\n\\n
 Unique constraint failed on the fields: (`email`)"}}

  ← ⚠️ 500! Halbuki bu, İSTİFADƏÇİ xətasıdır (409 olmalıdır).
     Frontend 500-ü «server sındı» kimi oxuyur və istifadəçiyə
     «bir az sonra yenidən cəhd edin» deyir. İstifadəçi isə
     saatlarla eyni xətanı təkrarlayır — çünki e-poçt
     həqiqətən təkraralır.

────────────────────────────────────────────────────────────
`$transaction` olmasa:

$ curl 'http://localhost:4000/api/v1/emekdaslar?limit=20&seife=1'
{"cem": 15, "melumat": [ ...14 sətir... ]}
  ← ⚠️ cem=15, amma 14 sətir gəldi. Aralarında başqa
     istifadəçi sətir əlavə etdi. Frontend «1 nəticə
     gizli qaldı» düşünüb sonsuz döngəyə düşə bilər.

────────────────────────────────────────────────────────────
Yumşaq silmə olmasa:

$ curl -X DELETE http://localhost:4000/api/v1/emekdaslar/1
HTTP/1.1 500 Internal Server Error
{"xeta":{"kod":"DAXILI_XETA","mesaj":
 "Foreign key constraint violated on the constraint:
  `elmi_shura_uzvleri_emekdas_id_fkey`"}}

  ← ⚠️ Direktorun şura üzvlüyü var. Silmək üçün əvvəlcə
     şura qeydini silmək lazımdır — amma o qeyd
     BİR İLLİK QƏRARIN tarixçəsidir!""",
    "c_izah": """
<p><strong>Birinci nəticə: servis HTTP-dən tam asılısız işləyir.</strong>
<code>skriptler/servis_yoxla.ts</code> heç bir server qaldırmadan,
port tutmadan, controller-dən keçmədən 34 yoxlamanı icra etdi. Bu,
laylı arxitekturanın <em>əməli</em> faydasıdır: problem yarananda
dərhal bilirik ki, o, servisdədir, yoxsa HTTP qatında.</p>
<p><strong>İkinci nəticə: yumşaq silmə real bazada işləyir.</strong>
Test iki halı göstərdi: asılı qeydi olmayan müvəqqəti əməkdaş
<code>hard</code> silindi (sətir bazadan çıxdı), asılı qeydi olan isə
<code>soft</code> silindi (<code>aktiv = false</code> oldu, sətir qaldı).
İkisi də <code>200</code> qaytarır, amma cavabdaki <code>nov</code> sahəsi
<em>hansının baş verdiyini</em> deyir. Bu, dürüst API dizaynıdır.</p>
<p><strong>Üçüncü nəticə: FK qoruması sübut olundu.</strong> ID 1-i
<code>$transaction</code> içində silməyə cəhd etdik və baza
<code>P2003</code> ilə imtina etdi. Üstəlik <code>throw</code> sətri
nəticənin <em>heç vaxt commit olunmamasını</em> təmin edir — yəni
test <em>təhlükəsizdir</em>. Bu naxışı yadda saxlayın: real bazada
dağıdıcı əməliyyatı yoxlamaq lazım gələndə həmişə tranzaksiya
içində edin.</p>
<p><strong>Dördüncü nəticə: axtarış hərf böyüklüyünə həssas deyil.</strong>
<code>əliyev</code> və <code>ƏLİYEV</code> — hər ikisi 2 nəticə verdi.
Bu, Azərbaycan dilində vacibdir, çünki istifadəçi <code>ə</code> hərfini
klaviaturada tapa bilmir və <code>e</code> yazır.</p>
<p><strong>Nəticə:</strong> servis hazırdır, amma onu <em>çağıran</em>
yoxdur. Növbəti addımda HTTP qatını — controller-i və modulu —
yazacağıq.</p>
""",
    "sual": [
        ("Niyə servisdə <code>throw new NotFoundException()</code> var? "
         "Bu, HTTP anlayışı deyilmi?",
         "Çox düzgün müşahidədir və bu, NestJS-in şüurlu seçimidir. "
         "Rəsmi olaraq servis HTTP-dən xəbərsiz olmalıdır. Amma Nest-in "
         "<code>HttpException</code> ailəsi praktikada rahatdır: onu "
         "<em>hər hansı</em> qatdan atmaq olar və qlobal filtr onu düzgün "
         "statusa çevirir. Daha «təmiz» alternativ: servis öz xəta sinfini "
         "atsın (<code>TapilmadiXetasi</code>) və controller onu HTTP-ə "
         "çevirsin. Bu, daha çox kod tələb edir. Kiçik-orta layihələrdə "
         "Nest yanaşması standartdır."),
        ("<code>$transaction</code> niyə <code>count</code> və "
         "<code>findMany</code> üçün lazımdır? Axı heç nə dəyişmirik.",
         "Dəyişmirik, amma <em>oxuyuruq</em> — və oxuma da tutarlı olmalıdır. "
         "Prisma massiv tranzaksiyası hər iki sorğunu <strong>eyni "
         "snapshot</strong>-dan oxuyur. Onsuz arada əlavə olunan sətir "
         "nəticələri uyğunsuz edə bilər. Üstəlik performans qazancı var: "
         "iki sorğu bir şəbəkə gediş-gəlişində gedir."),
        ("<code>BigInt(id)</code> yerinə <code>Number</code>-i saxlayıb "
         "Prisma-ya <code>BigInt</code> göndərməsək?",
         "Prisma tipi yoxlayır və <code>Expected BigInt, provided Int</code> "
         "xətası verir. Alternativ olaraq sxemdə <code>id</code>-ni "
         "<code>Int</code> etmək olardı — amma o zaman 2<sup>31</sup> "
         "(~2.1 milyard) sətir həddi olardı. <code>audit_log</code> kimi "
         "cədvəllər üçün bu, real hədddir. <code>BigInt</code>-də qalmaq "
         "düzgün qərardır."),
        ("<code>asililariSay()</code> hər silmədə 7 sorğu göndərir. "
         "Bu, baha deyilmi?",
         "Bir tranzaksiyada, indekslənmiş sütunlar üzrə <code>count</code> "
         "sorğularıdır — millisaniyələrlə işləyir. Silmə isə <em>nadir</em> "
         "əməliyyatdır (ildə bir neçə dəfə). Burada aydınlıq sürətdən "
         "vacibdir. Əgər bunun əksinə, siyahı endpoint-i olsaydı, "
         "optimallaşdırma lazım gələrdi."),
        ("Niyə <code>findUnique</code> null qaytarır, "
         "<code>update</code> isə xəta atır — bu uyğunsuzluq deyilmi?",
         "Uyğunsuzluqdur, amma <em>qəsdən</em> belədir. Prisma-nın "
         "məntiqi: <code>findUnique</code> «axtar və tap» əməliyyatıdır — "
         "tapmamaq normal nəticədir (<code>null</code>). "
         "<code>update</code>/<code>delete</code> isə «<em>bu sətri</em> "
         "dəyiş» əməliyyatlarıdır — sətir yoxdursa, niyyətiniz "
         "həyata keçmədi, deməli xətadır (<code>P2025</code>). Bu, "
         "SQL-in <code>UPDATE ... WHERE</code> davranışından fərqlidir və "
         "bilmək vacibdir."),
        ("Axtarışda <code>%</code> işarəsi göndərsəm nə olar?",
         "Prisma parametrləşdirilmiş sorğu göndərir, ona görə "
         "SQL inyeksiyası <strong>mümkün deyil</strong>. Amma "
         "<code>%</code> <code>LIKE</code>-ın xüsusi simvoludur və "
         "<code>contains: '%'</code> bütün sətirləri tapar. Yəni "
         "təhlükəsizlik problemi yox, sadəcə gözlənilməz nəticə. "
         "İstəsəniz DTO-da <code>@Matches(/^[^%_]*$/)</code> ilə "
         "qadağan edə bilərsiniz."),
        ("<code>Logger</code> yerinə <code>console.log</code> yazsam olmaz?",
         "İşləyər, amma itirəcəyiniz çox şey var: (1) Nest-in loq "
         "səviyyələri (<code>log</code>/<code>warn</code>/<code>error</code>) "
         "istehsalatda filtrələnə bilər; (2) kontekst adı "
         "(<code>[EMEKDASLAR]</code>) avtomatik əlavə olunur; "
         "(3) gələcəkdə fayla/sistemə yönləndirmək asandır. "
         "<code>console.log</code> isə həmişə standart çıxışa gedir."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>Servisin <strong>bütün əməliyyatları</strong> HTTP olmadan,
      birbaşa çağırışla yoxlanıldı: <em>34 yoxlama, hamısı keçdi</em>.</li>
  <li><strong>Oxuma:</strong> səhifələmə (<code>cem=14</code>,
      <code>sehife_sayi</code>), sıralama, axtarış (hərf
      böyüklüyündən asılı olmayan), filtr (merkez, aktivlik).</li>
  <li><strong>Yaratma:</strong> yeni əməkdaş yaradıldı, mapper düzgün
      çevirdi (<code>maas: "1500.50"</code>, <code>ise_baslama:
      "2026-02-01"</code>), standart status (<code>Aktiv</code>) tətbiq
      olundu.</li>
  <li><strong>Yeniləmə:</strong> yalnız göndərilən sahələr dəyişdi
      (<code>vezife_id</code>, <code>maas</code>), <code>ad</code>
      toxunulmaz qaldı. Boş gövdə <code>400</code> aldı.</li>
  <li><strong>Silmə — iki hal:</strong> asılısız əməkdaş
      <code>hard</code>, asılısı olan <code>soft</code>. Real bazada,
      real nəticə ilə.</li>
  <li><strong>FK qoruması:</strong> ID 1-i silmək cəhdi
      <code>P2003</code> ilə bloklandı — və tranzaksiya sayəsində
      <em>heç nə dəyişmədi</em> (bazada yenə 14 əməkdaş).</li>
</ul>
<p><strong>Validasiya + mapper + servis = tam biznes məntiqi.</strong>
İndi bunu HTTP üzərinə qoymaq qalır. Növbəti addımda controller və
modulu yazacağıq — və o zaman API <em>həqiqətən</em> işləyəcək.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 20 — CONTROLLER, MODUL VƏ SERVER
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 20,
    "ad": "Controller və modul — API-ni serverə qoşuruq",
    "a": """
<p>Servis hazırdır, amma onu <em>çağıran</em> yoxdur. İndi HTTP qatını
yazırıq: controller, modul və kök modula qoşulma.</p>

<h4>REST nədir?</h4>
<p><strong>REST</strong> — <em>Representational State Transfer</em>, veb
API-lərinin dizayn üslubu. Əsas fikri: <strong>URL resursu bildirir,
HTTP metodu isə hərəkəti</strong>.</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Metod</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Yol</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Mənası</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Status</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>GET</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>/emekdaslar</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Siyahını ver</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>200</code></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>GET</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>/emekdaslar/5</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Birini ver</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>200</code></td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>POST</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>/emekdaslar</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Yenisini yarat</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>201</code></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>PATCH</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>/emekdaslar/5</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Bir hissəsini dəyiş</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>200</code></td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>DELETE</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>/emekdaslar/5</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Sil</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>200</code></td>
  </tr>
</table>
<p>Diqqət yetirin: URL-də <strong>fel yoxdur</strong>. Yazmırıq
<code>/emekdaslar/yarat</code> və ya <code>/emekdaslar/sil</code>.
Yazırıq <code>POST /emekdaslar</code> və <code>DELETE
/emekdaslar/5</code>. Fel <em>metodun özündədir</em>. Bu, REST-in
əsas qaydasıdır.</p>

<h4>PATCH yoxsa PUT?</h4>
<ul>
  <li><code>PUT</code> — resursu <strong>tamamilə</strong> əvəz edir.
      Göndərmədiyiniz hər sahə silinir (və ya standart dəyərə qayıdır).</li>
  <li><code>PATCH</code> — <strong>qismən</strong> dəyişir. Yalnız
      göndərdikləriniz toxunulur.</li>
</ul>
<p>Biz <code>PATCH</code> seçirik, çünki real həyatda istifadəçi
<em>bir</em> sahəni dəyişir (məsələn maaşı). <code>PUT</code> ilə 16 sahəni
hamısını göndərmək məcburiyyəti olsaydı, birini unutsaq
<strong>sükutla silinərdi</strong> — ən təhlükəli API səhvlərindən biri.</p>

<h4>Status kodları — niyə <code>200</code> yox, <code>201</code>?</h4>
<p><code>201 Created</code> — «yeni resurs yaradıldı». Bu, sadəcə
formalite deyil: frontend <code>201</code> görəndə bilir ki, cavabın
gövdəsində <em>yeni yaradılmış obyekt</em> var və onu siyahıya əlavə
etmək olar. <code>200</code> isə «sorğunuz işləndi, amma xüsusi bir şey
olmadı» deməkdir.</p>
<p>Nest-də bu, bir dekoratorla edilir:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Post()
@HttpCode(201)
yarat(@Body() dto: EmekdasYaratDto) { ... }</pre>
<p>Əslində Nest <code>POST</code> üçün <code>201</code>-i
<em>avtomatik</em> qaytarır. <code>@HttpCode(201)</code> yazmağımızın
səbəbi — <strong>aydınlıq</strong>: kodu oxuyan şəxs statusu dərhal
görür, sənədə baxmağa ehtiyac qalmır.</p>

<h4>⚠️ Marşrut sırası — gizli tələ</h4>
<p>Bu, NestJS-də ən çox vaxt itirilən mövzudur. Təsəvvür edin,
controller-də belə yazıbsınız:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Get(':id')          // ← YUXARIDA
biri(@Param('id', ParseIntPipe) id: number) { ... }

@Get('statistika')   // ← AŞAĞIDA
statistika() { ... }</pre>
<p>İndi <code>GET /emekdaslar/statistika</code> sorğusu göndəririk.
Nest marşrutları <strong>yuxarıdan aşağıya</strong> yoxlayır və
<code>:id</code> naxışına <em>ilk</em> rast gəlir. «statistika» sözü
<code>id</code> kimi tutulur, <code>ParseIntPipe</code> isə onu ədədə
çevirə bilmir:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
400 Bad Request
{"xeta":{"kod":"YANLIS_SORGU",
 "mesaj":"Validation failed (numeric string is expected)"}}</pre>
<p>Ən məkrli tərəfi: <em>statistika endpointi heç vaxt çağırılmır</em>.
Onu debug etmək üçün saatlar gedə bilər. <strong>Qayda: konkret yollar
həmişə <code>:param</code>-dan yuxarıda yazılır.</strong> Bizim
controller-də hələ konkret yol yoxdur — amma 2B dərsində
<code>statistika</code> əlavə edəndə bu sıra artıq hazırdır.</p>

<h4>Nə üçün controller-də <code>if</code> yoxdur?</h4>
<p>Controller-in bütün metodları <em>bir sətirdir</em>:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Get(':id')
biri(@Param('id', ParseIntPipe) id: number) {
  return this.xidmet.biri(id);
}</pre>
<p>Bu, <strong>qəsdən</strong> belədir. Controller yalnız «körpü»dür:
HTTP parametrini götürür, servisə ötürür, nəticəni qaytarır. Bütün
yoxlama DTO-da, bütün məntiq servisdədir. Faydası: controller-i oxumaq
5 saniyə çəkir və <em>bütün API səthi</em> bir ekranda görünür.</p>

<h4>Modul — hissələri bir yerə yığan qab</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Module({
  controllers: [EmekdaslarController],
  providers: [EmekdaslarService],
  exports: [EmekdaslarService],
})
export class EmekdaslarModule {}</pre>
<ul>
  <li><code>controllers</code> — HTTP marşrutlarını qeydiyyatdan keçirir.</li>
  <li><code>providers</code> — Nest-in <em>yaradacağı</em> siniflər.
      Yəni <code>EmekdaslarService</code> <code>new</code> ilə deyil,
      Nest tərəfindən yaradılır və asılılıqları (PrismaService)
      <em>avtomatik</em> ötürülür.</li>
  <li><code>exports</code> — başqa modul bu servisi istəyə bilsin.
      Bizdə hələ istəyən yoxdur, amma 2B-də hesabat modulu istəyəcək.</li>
</ul>
<p>⚠️ <strong>Diqqət:</strong> <code>imports</code> bölməsində
<code>PrismaModule</code> <em>yoxdur</em>. Səbəb: 1A-nın ADDIM 7-də onu
<code>@Global()</code> elan etdik. Qlobal modulun <code>exports</code>
etdiyi hər şey bütün modullara açıqdır. Yazsaq da xəta olmazdı, amma
lazımsız təkrar olardı.</p>

<h4>Kök modula qoşulma</h4>
<p><code>app.module.ts</code> faylına <code>EmekdaslarModule</code>-u
əlavə edirik. Bu olmasa, modul <em>heç vaxt yüklənməyəcək</em> və bütün
endpoint-lər <code>404</code> qaytaracaq. Nest modulları
<strong>açıq şəkildə</strong> qoşmağı tələb edir — bu, kodun
strukturunu görünən edir.</p>
""",
    "anlayis": [
        ("REST",
         "Veb API dizayn üslubu: URL resursu, HTTP metodu hərəkəti bildirir. "
         "URL-də fel olmur."),
        ("Resurs",
         "REST-in əsas anlayışı — «şey». Bizdə <code>emekdaslar</code>. "
         "URL həmişə <em>cəm</em> ilə yazılır."),
        ("PATCH vs PUT",
         "<code>PATCH</code> qismən, <code>PUT</code> tamamilə əvəz edir. "
         "Real API-lərdə <code>PATCH</code> daha çox işlədilir."),
        ("201 Created",
         "«Yeni resurs yaradıldı». <code>POST</code> üçün düzgün status."),
        ("409 Conflict",
         "Sorğu düzgündür, amma resursun cari vəziyyəti ilə ziddiyyətdir "
         "(təkrar e-poçt)."),
        ("@Param / @Query / @Body",
         "Nest dekoratorları: URL hissəsi / sorğu parametrləri / sorğu "
         "gövdəsi. Hər biri müvafiq DTO ilə yoxlanıla bilər."),
        ("ParseIntPipe",
         "URL-dən gələn mətni ədədə çevirir. Çevrilmirsə "
         "<code>400</code> qaytarır — bazaya sorğu getmir."),
        ("Marşrut sırası",
         "Nest marşrutları <em>elan sırası</em> ilə yoxlayır. "
         "<code>:id</code> konkret yollardan sonra yazılmalıdır."),
        ("Modul",
         "Nest-də tətbiqin tikinti bloku: <code>controllers</code>, "
         "<code>providers</code>, <code>imports</code>, "
         "<code>exports</code>."),
        ("DI (asılılıq yeritmə)",
         "Nest sinifləri özü yaratmır — konstruktorda <em>istəyir</em>, "
         "Nest isə ötürür. Ona görə testdə saxtası ilə əvəz etmək "
         "mümkündür."),
        ("Marşrut cədvəli",
         "Server qalxanda Nest-in loga yazdığı siyahı: "
         "<code>Mapped {/api/v1/emekdaslar, GET} route</code>."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) Controller başlığı</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Controller('emekdaslar')
export class EmekdaslarController {
  constructor(private readonly xidmet: EmekdaslarService) {}
}</pre>
<ul>
  <li><code>@Controller('emekdaslar')</code> — bu sinfin bütün
      marşrutlarının <em>prefiksi</em>. Qlobal
      <code>setGlobalPrefix('api/v1')</code> ilə birlikdə tam yol
      <code>/api/v1/emekdaslar</code> olur.</li>
  <li><code>private readonly xidmet</code> — <strong>TypeScript-in qısa
      yazılışı</strong>. Bu bir sətir üç iş görür: (1) xüsusi sahə
      yaradır, (2) konstruktor parametrini ona mənimsədir, (3)
      <code>readonly</code> edir (dəyişdirilə bilməz). Adi yazılışla
      dörd sətir olardı.</li>
  <li><code>xidmet</code> adı — Azərbaycan dilində «service»
      qarşılığı. Bəzi yerlərdə <code>servis</code> də işlədə bilərdik;
      <code>xidmet</code> seçdik.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2) Beş endpoint</h5>
<ul>
  <li><code>@Get()</code> — <strong>heç bir arqument yoxdur</strong>,
      yəni tam olaraq <code>/api/v1/emekdaslar</code>. Boş mötərizə
      mütləqdir: <code>@Get</code> (mötərizəsiz) yazmaq da işləyər,
      amma bəzi versiyalarda problem yaradır — həmişə
      <code>@Get()</code> yazın.</li>
  <li><code>@Query() sorgu: EmekdasSorguDto</code> — <strong>bütün</strong>
      sorğu parametrlərini bir DTO-da yığır. Nest
      <code>?seife=1&amp;limit=5&amp;aktiv=passiv</code> mətnini
      avtomatik <code>EmekdasSorguDto</code> nüsxəsinə çevirir.
      Yoxlama (Addım 17-də yazdığımız qaydalar) bu anda işləyir.</li>
  <li><code>@Get(':id')</code> — iki nöqtəli parametr. URL-in bu
      hissəsi dəyişəndir. <code>ParseIntPipe</code> onu ədədə çevirir;
      <code>/emekdaslar/abc</code> → <code>400</code>.</li>
  <li><code>@Body() dto: EmekdasYaratDto</code> — sorğunun JSON
      gövdəsini sinfə çevirir və yoxlayır. Gövdə boşdursa və ya
      mütləq sahə çatışmırsa → <code>400</code>.</li>
  <li><code>@Patch(':id')</code> — həm yol parametri, həm gövdə alır.
      İki parametrin <strong>sırası vacib deyil</strong>, Nest
      dekoratorlara baxır.</li>
  <li><code>@Delete(':id')</code> — gövdə yoxdur, yalnız ID.
      Yumşaq və ya adi silmə qərarını servis verir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3) Niyə <code>return</code> kifayətdir?</h5>
<p>Metodlarda <code>res.json(...)</code> və ya <code>res.status(...)</code>
çağırışı <em>yoxdur</em>. Nest bunu özü edir: metodun qaytardığı dəyəri
götürür, JSON-a çevirir və göndərir. <code>async</code> metodlarda
Promise-i <em>gözləyir</em>. Xəta atılsa (<code>throw</code>), qlobal
filtr onu tutub düzgün statusla formatlaşdırır.</p>
<p>Bu, həm daha qısa, həm də daha <strong>test edilə bilən</strong> koddur:
metod sadəcə dəyər qaytarır, HTTP ilə məşğul olmur.</p>

<h5 style="color:#334155;margin-top:1rem">4) Modul</h5>
<p>Üç bölmə var: <code>controllers</code>, <code>providers</code>,
<code>exports</code>. <code>imports</code> yoxdur — səbəbini
yuxarıda (A hissəsində) izah etdik: <code>PrismaModule</code>
<code>@Global()</code>-dir.</p>
<p><code>exports: [EmekdaslarService]</code> — bu sətir olmasa, başqa
modul <code>EmekdaslarService</code>-i konstruktorunda istəyəndə Nest
<code>Nest can't resolve dependencies</code> xətası verər. Export
etmək «bu servisi paylaşmağa icazə verirəm» deməkdir.</p>

<h5 style="color:#334155;margin-top:1rem">5) <code>app.module.ts</code> — bir sətirlik dəyişiklik</h5>
<p>İki dəyişiklik: <code>import</code> sətri və
<code>imports</code> massivinə əlavə. Kiçik görünür, amma
<strong>həlledicidir</strong>: bu olmasa bütün endpoint-lər
<code>404</code> qaytarar və səbəbi heç bir xəta mesajında
görünməz.</p>
<p>Yeri də vacibdir: <code>EmekdaslarModule</code> <code>imports</code>
massivinin <em>sonunda</em> əlavə etdik. Nest modulları asılılıq sırası
ilə deyil, qrafı həll edərək yükləyir — amma oxunaqlılıq üçün əlaqəli
modulları bir yerdə saxlamaq yaxşıdır.</p>

<h5 style="color:#334155;margin-top:1rem">6) Marşrut cədvəli — serverin «nə bilirəm» siyahısı</h5>
<p>Server qalxanda Nest hər marşrutu loga yazır:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
[Nest] LOG [RouterExplorer] Mapped {/api/v1/emekdaslar, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/emekdaslar/:id, GET} route +1ms
...</pre>
<p>Bu siyahı <strong>ən faydalı debug alətidir</strong>. «Endpoint
tapılmır» problemi yarananda ilk baxılacaq yer budur: marşrut ümumiyyətlə
qeydiyyatdan keçibmi? Yoxsa <code>app.module.ts</code>-ə əlavə etməyi
unudubsuq?</p>
""",
    "fayllar": [
        "src/emekdaslar/emekdaslar.controller.ts",
        "src/emekdaslar/emekdaslar.module.ts",
        "src/app.module.ts",
    ],
    "goster": ["src/saglamliq/saglamliq.controller.ts"],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then
  echo "  ✓ tip xətası yoxdur"
else
  echo "  ✗ tip xətası var"
fi

echo ""
echo "════ 2) Build ════"
npm run build && echo "  ✓ build tamamlandı"

PORT="${PORT:-4000}"
LOQ="/tmp/arti_2a_${PORT}.log"

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "  ✗ $PORT portu məşğuldur — əvvəlcə boşaldın"
  exit 1
fi

PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
temizle() { kill "$PID" 2>/dev/null; wait "$PID" 2>/dev/null; true; }
trap temizle EXIT INT TERM

hazir=0
i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  curl -fsS "http://localhost:$PORT/api/v1/saglamliq" -o /dev/null 2>/dev/null && { hazir=1; break; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.5
done
if [ "$hazir" != "1" ]; then
  echo "  ✗ server qalxmadı"
  tail -n 20 "$LOQ" | sed 's/^/      /'
  exit 1
fi
echo "  ✓ server hazırdır (PID $PID, $i cəhd)"

echo ""
echo "════ 3) Qeydiyyatdan keçmiş marşrutlar ════"
grep 'Mapped {' "$LOQ" | sed 's/.*Mapped //' | sed 's/ route.*//' | sort -u | sed 's/^/      /'

echo ""
echo "════ 4) GET /api/v1/emekdaslar?limit=2 ════"
curl -s -o /tmp/arti_2a_1.json -w '      status: %{http_code}\n' "http://localhost:$PORT/api/v1/emekdaslar?limit=2"
python3 -c "
import json
d = json.load(open('/tmp/arti_2a_1.json'))
print('      cem=%s  sehife=%s/%s  gosterilen=%s' % (d['cem'], d['sehife'], d['sehife_sayi'], len(d['melumat'])))
for e in d['melumat']:
    print('        - id=%s  %s  |  %s  |  %s AZN' % (e['id'], e['tam_ad'], e['vezife']['ad'], e['maas']))
"

echo ""
echo "════ 5) GET /api/v1/emekdaslar/1 — tam cavab ════"
curl -s -o /tmp/arti_2a_2.json -w '      status: %{http_code}\n' "http://localhost:$PORT/api/v1/emekdaslar/1"
python3 -m json.tool /tmp/arti_2a_2.json | sed 's/^/      /'

echo ""
echo "════ 6) Status kodları ════"
KODK() { curl -s -o /dev/null -w '%{http_code}' "http://localhost:$PORT$1"; }
printf '      %-34s → %s\n' "/api/v1/emekdaslar" "$(KODK /api/v1/emekdaslar)"
printf '      %-34s → %s\n' "/api/v1/emekdaslar/1" "$(KODK /api/v1/emekdaslar/1)"
printf '      %-34s → %s\n' "/api/v1/emekdaslar/999999" "$(KODK /api/v1/emekdaslar/999999)"
printf '      %-34s → %s\n' "/api/v1/emekdaslar/abc" "$(KODK /api/v1/emekdaslar/abc)"
printf '      %-34s → %s\n' "/api/v1/emekdaslar?limit=500" "$(KODK '/api/v1/emekdaslar?limit=500')"
printf '      %-34s → %s\n' "/emekdaslar (prefiks olmadan)" "$(KODK /emekdaslar)"

echo ""
echo "════ 7) Swagger-də yeni endpoint-lər ════"
curl -s "http://localhost:$PORT/docs-json" -o /tmp/arti_2a_openapi.json
python3 -c "
import json
d = json.load(open('/tmp/arti_2a_openapi.json'))
print('      OpenAPI versiyası:', d.get('openapi'))
for yol in sorted(d.get('paths', {})):
    metodlar = ', '.join(sorted(m.upper() for m in d['paths'][yol]))
    print('      %-32s %s' % (yol, metodlar))
"
""",
    "olmaz": """Controller və ya modul olmasa:

$ curl http://localhost:4000/api/v1/emekdaslar

HTTP/1.1 404 Not Found
{"ugur":false,"xeta":{"kod":"TAPILMADI",
 "mesaj":"Cannot GET /api/v1/emekdaslar"},
 "yol":"/emekdaslar","vaxt":"..."}

  ← ⚠️ 404. Səbəb nədir? Üç ehtimal var:
     1. Controller faylı yoxdur
     2. Modul yaradılıb, amma app.module.ts-ə əlavə olunmayıb
     3. Marşrut yolu səhv yazılıb

     ⚠️ Server heç bir xəta vermir! Loglarda "Mapped
     {/api/v1/emekdaslar, GET}" sətri YOXDUR. Yeganə
     diaqnostika aləti məhz həmin sətirdir.

────────────────────────────────────────────────────────────
Marşrut sırası səhv olsa:

@Get(':id')          // yuxarıda
@Get('statistika')   // aşağıda

$ curl http://localhost:4000/api/v1/emekdaslar/statistika
HTTP/1.1 400 Bad Request
{"xeta":{"kod":"YANLIS_SORGU",
 "mesaj":"Validation failed (numeric string is expected)"}}

  ← ⚠️ "statistika" :id kimi tutuldu. Statistika
     endpointi HEÇ VAXT çağırılmır və heç bir xəta
     bunu demir.

────────────────────────────────────────────────────────────
PrismaModule @Global() olmasaydı və imports-a
əlavə etməsəydik:

Error: Nest can't resolve dependencies of the
EmekdaslarService (?, PrismaService). Please make sure
that the argument PrismaService at index [0] is available
in the EmekdaslarModule context.

  ← Bu xəta serverin QALXMASINA mane olur — yaxşıdır,
     çünki dərhal bilirik.""",
    "c_izah": """
<p><strong>Ən mühüm nəticə — marşrut cədvəli.</strong> Server 7
endpoint-i qeydiyyatdan keçirdi və hamısı logda görünür. Bu siyahı
olmasa, «404 gəlir, niyə?» sualına cavab tapmaq çox çətin olardı.
Praktikada ilk baxılacaq yer <em>həmişə</em> budur.</p>
<p><strong>İkincisi: prefiks işləyir.</strong>
<code>/api/v1/emekdaslar</code> → <code>200</code>, amma
<code>/emekdaslar</code> (prefiks olmadan) → <code>404</code>. Bu,
1A-nın ADDIM 11-də yazdığımız <code>setGlobalPrefix('api/v1')</code>
sətrinin <em>hələ də</em> işlədiyini sübut edir.</p>
<p><strong>Üçüncüsü: yoxlama zənciri tam işləyir.</strong>
<code>/emekdaslar/abc</code> → <code>400</code>
(<code>ParseIntPipe</code>), <code>/emekdaslar/999999</code> →
<code>404</code> (servisdəki <code>NotFoundException</code>),
<code>?limit=500</code> → <code>400</code> (DTO-daki
<code>@Max(100)</code>). Hər qat öz işini görür və <em>heç biri</em>
digərinin işinə qarışmır.</p>
<p><strong>Dördüncüsü: Swagger avtomatik yeniləndi.</strong> Heç bir
əlavə kod yazmadıq, amma <code>/docs</code> səhifəsində beş yeni
endpoint göründü. Nest controller-i oxuyub OpenAPI sənədini
<em>özü</em> yaradır. Bu, 2B/2C dərslərində <code>@ApiProperty</code>
əlavə edərək daha da zənginləşdiriləcək.</p>
<p><strong>Nəticə:</strong> API işləyir. Amma onu <em>əl ilə</em>
yoxlamaq yorucudur — hər dəfə 7 <code>curl</code> əmri yazmaq lazımdır.
Növbəti addımda bunu <em>bir skriptə</em> çevirəcəyik.</p>
""",
    "sual": [
        ("Niyə controller-də <code>@HttpCode(201)</code> yazdıq, axı Nest onsuz da 201 qaytarır?", "Aydınlıq üçün. Kodu oxuyan şəxs statusu dərhal görür və Nest-in sənədinə baxmağa ehtiyac qalmır. Bundan əlavə, gələcəkdə kimsə <code>@Post</code>-u <code>@Put</code>-a dəyişsə, status da açıq şəkildə görünəcək. Kiçik bir sətir, böyük oxunaqlılıq qazancı."),
        ("<code>ParseIntPipe</code> yerinə özüm yoxlasam olmaz?", "Olar, amma <code>ParseIntPipe</code> artıq yazılıb, test edilib və düzgün xəta mesajı verir. Öz yoxlamanızı yazsanız, eyni kodu təkrar etmiş olarsınız. Nest-in hazır boruları (<code>ParseIntPipe</code>, <code>ParseBoolPipe</code>, <code>ParseUUIDPipe</code>) məhz bunun üçündür."),
        ("Sinif adı niyə <code>EmekdaslarController</code> — cəm şəklində?", "Çünki bu controller <em>bütün</em> əməkdaşlar resursunu idarə edir. Fayl adları da cəm olur: <code>emekdaslar.controller.ts</code>. Bu, Nest CLI-ın standartıdır və böyük layihələrdə hansı faylın nəyə aid olduğunu dərhal göstərir."),
        ("Modulu <code>AppModule</code>-a əlavə etməyi unutsam, kompilyator xəbərdarlıq edərmi?", "Xeyr — və bu, ən məkrli tərəfidir. TypeScript xəta vermir, Nest xəta vermir, server uğurla qalxır. Sadəcə endpoint-lər <code>404</code> qaytarır. Yeganə diaqnostika aləti başlanğıc logundaki marşrut cədvəlidir. Ona görə server qalxanda loqa baxmaq <em>vərdiş</em> olmalıdır."),
        ("<code>@Controller('emekdaslar')</code> yerinə <code>@Controller('api/v1/emekdaslar')</code> yazsam olar?", "Olar, amma onda prefiks <em>hər</em> controller-də təkrarlanardı və <code>setGlobalPrefix</code>-in mənası qalmazdı. İndi prefiksi bir yerdə (main.ts) dəyişirik və bütün API təsir alır. Məsələn <code>api/v2</code>-yə keçmək lazım olsa, bir sətir dəyişir."),
        ("Swagger bütün endpoint-ləri avtomatik gördü — necə?", "Nest <code>SwaggerModule.createDocument(app, konfiq)</code> çağırışında bütün qeydiyyatdan keçmiş marşrutları gəzir. Parameter tipləri (DTO sinifləri) <code>reflect-metadata</code> vasitəsilə oxunur. Ona görə <code>@Body() dto: EmekdasYaratDto</code> yazmaq kifayətdir — Nest DTO-nun sahələrini özü çıxarır."),
        ("Controller-də <code>async</code> yazmamışam, amma servis <code>Promise</code> qaytarır. Problem olarmı?", "Olmaz. Nest <code>Promise</code>-i özü gözləyir. <code>async</code>/<code>await</code> yalnız metodun içində <em>əlavə</em> əməliyyat etmək lazım olanda (məsələn iki servisi ardıcıl çağırmaq) lazımdır. Bizdə metod sadəcə «ötür və qaytar» etdiyi üçün <code>return this.xidmet.biri(id)</code> kifayətdir."),
        ("<code>xidmet</code> əvəzinə <code>service</code> yazsam?", "İşləyər — bu, sadəcə dəyişən adıdır. Amma bütün layihə Azərbaycan adlandırması ilə getdiyi üçün ardıcıllıq vacibdir. Qarışıq adlandırma (yarısı İngilis, yarısı Azərbaycan) kodu oxumağı çətinləşdirir. Komanda daxilində <em>bir</em> qayda seçib ona əməl etmək lazımdır."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li><strong>7 marşrut</strong> qeydiyyatdan keçdi və hamısı logda
      görünür: <code>GET /api/v1</code>, <code>GET /api/v1/saglamliq</code>,
      <code>GET /api/v1/emekdaslar</code>, <code>GET /api/v1/emekdaslar/:id</code>,
      <code>POST /api/v1/emekdaslar</code>, <code>PATCH /api/v1/emekdaslar/:id</code>,
      <code>DELETE /api/v1/emekdaslar/:id</code>.</li>
  <li><strong>Canlı məlumat gəldi:</strong> ID 1 — Əliyev Elnur Qəzənfər,
      Direktor, 3500.00 AZN. Bütün sahələr mapper-dən düzgün keçib:
      <code>id</code> mətn, <code>maas</code> mətn, tarixlər
      <code>YYYY-MM-DD</code>, əlaqələr obyekt kimi.</li>
  <li><strong>Prefiks işləyir:</strong> prefikssiz yol <code>404</code>
      qaytarır.</li>
  <li><strong>Yoxlama zənciri:</strong> <code>400</code> (mətn ID),
      <code>404</code> (olmayan ID), <code>400</code> (limit həddi) —
      hər biri öz qatında tutulur.</li>
  <li><strong>Swagger avtomatik yeniləndi:</strong> <code>/docs</code>
      səhifəsində beş yeni endpoint, heç bir əlavə kod yazmadan.</li>
</ul>
<p><strong>API işləyir.</strong> İndi son addımda onu
<em>sistematik</em> yoxlayacağıq — CRUD dövranını əvvəldən axıra
işlədən bir skript yazacağıq.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 21 — BÜTÖV CRUD AXINI
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 21,
    "ad": "Bütöv CRUD axını — hər şeyi bir skriptdə yoxlayırıq",
    "a": """
<p>Endpoint-lər işləyir, amma onları əl ilə yoxlamaq yorucudur. Hər
dəfə 7-8 <code>curl</code> əmri yazmaq, status kodlarını yadda saxlamaq,
cavabları göz ilə tutuşdurmaq lazımdır. İnsan yorulur və addım atlayır —
1B dərsində bunu «təkrarlana bilən yoxlama» adlandırmışdıq.</p>
<p>Bu addımda <code>skriptler/crud_yoxla.sh</code> faylını yazırıq:
<strong>19 yoxlamanı</strong> avtomatik icra edən, nəticəni cədvəl kimi
göstərən və <em>çıxış kodu</em> ilə qərar verən bir skript.</p>

<h4>CRUD dövranı — «qızıl yol»</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
POST   /emekdaslar        → 201  (yeni sətir yaranır, ID alırıq)
GET    /emekdaslar/{id}   → 200  (yaratdığımızı oxuyuruq)
PATCH  /emekdaslar/{id}   → 200  (bir sahəsini dəyişirik)
DELETE /emekdaslar/{id}   → 200  (silirik)
GET    /emekdaslar/{id}   → 404  (getdi — təsdiq)</pre>
<p>Bu beş addım <strong>həmişə</strong> birlikdə yoxlanılmalıdır. Yalnız
<code>POST</code>-u yoxlamaq kifayət deyil: bəlkə sətir yaranır, amma
<em>oxunmur</em>? Bəlkə silinir, amma <em>silmə nəticə vermir</em>?
Dövran tamamlanmalıdır.</p>

<h4>⚠️ Sıra prinsipi — hər şey simmetrik olmalıdır</h4>
<p>Skriptin ən mühüm hissəsi <strong>əvvəl/sonra</strong> yoxlamasıdır:</p>
<ol>
  <li>Başlanğıcda sətir sayını yadda saxla: <code>EVVEL=14</code>.</li>
  <li>Bütün CRUD əməliyyatlarını et.</li>
  <li>Sonda yenidən say: <code>SONRA=14</code>.</li>
  <li>Bərabərdirsə → baza <em>toxunulmaz</em> qalıb.</li>
</ol>
<p>Bu naxış olmasa, test <em>özü</em> zibil buraxır: hər işlətmədə bir
sətir əlavə olunur və 100 işlətmədən sonra bazada 100 saxta əməkdaş
olur. Buna <strong>test çirklənməsi</strong> (test pollution) deyilir və
əsl məlumatı zibildən ayırmaq çox çətinləşir.</p>

<h4>Yoxlanılan xəta halları — «qızıl yol» kifayət deyil</h4>
<p>Real API-nin <em>səhv</em> halda nə etdiyini bilmək ən az
«düzgün» haldaki qədər vacibdir. Skript səkkiz xəta halını yoxlayır:</p>
<table style="width:100%;border-collapse:collapse;font-size:.88rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Sorğu</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Gözlənilən</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Nəyi sübut edir</th>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>POST</code> natamam gövdə</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>400</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">DTO validasiyası işləyir</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>POST</code> <code>vezife_id: 99</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>400</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Prisma <code>P2003</code> → 400 çevrilir</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>POST</code> təkrar e-poçt</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>409</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Prisma <code>P2002</code> → 409 çevrilir</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>POST</code> yad sahə</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>400</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>forbidNonWhitelisted</code></td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>GET /999999</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>404</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Servisdəki <code>NotFoundException</code></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>PATCH /999999</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>404</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Prisma <code>P2025</code> → 404</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>GET /abc</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>400</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>ParseIntPipe</code></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>GET ?limit=500</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><code>400</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">DTO həddi</td>
  </tr>
</table>
<p>Hər sətrin <em>öz səbəbi</em> var. Əgər biri uğursuz olsa, dərhal
bilirik hansı qat sındı: DTO, Prisma çevirməsi, yoxsa servis məntiqi.</p>

<h4>Niyə <code>DELETE</code>-dən sonra yenidən <code>GET</code> edirik?</h4>
<p>Bu, <strong>müsbət təsdiq</strong> deyil — <em>mənfi</em> təsdiqdir.
<code>DELETE</code> <code>200</code> qaytardı, amma bu, sətrin
həqiqətən getdiyini <em>sübut etmir</em>: server «sildim» deyib
heç nə etməyə bilər. Yalnız ardınca <code>GET</code> edib
<code>404</code> almaq həqiqi sübutdur.</p>
<p>Bu naxış bütün testlərdə keçərlidir: <strong>əvvəl və sonra</strong>
vəziyyəti yoxla, yalnız «əməliyyat uğurlu oldu» mesajına güvənmə.</p>

<h4>Niyə skript <em>onlarla</em> yoxlama aparır, amma <code>exit</code> yalnız bir dəfə?</h4>
<p>Skript <code>KECDI</code> və <code>XETA</code> sayğaclarını saxlayır və
<strong>hamısını</strong> işlədib bitirir. Yalnız sonda qərar verir.
Səbəb: birinci xətada dayansaydıq, qalan problemləri <em>görməzdik</em>.
Bir dəfə işlədib 3 problemi görmək, 3 dəfə işlədib hər dəfə birini
görməkdən yaxşıdır.</p>
<p>Bu, test alətlərinin ümumi davranışıdır: Vitest, Jest, pytest —
hamısı bütün testləri işlədir, sonra hesabat verir.</p>
""",
    "anlayis": [
        ("CRUD dövranı",
         "Create → Read → Update → Delete → təsdiq. Tam dövranı yoxlamaq "
         "yalnız bir addımı yoxlamaqdan qat-qat güclüdür."),
        ("Qızıl yol (happy path)",
         "Hər şey düzgün olanda sistemin davranışı. Yeganə yoxlanılan yol "
         "olmamalıdır."),
        ("Test çirklənməsi",
         "Testin özünün bazada zibil buraxması. «Əvvəl/sonra» yoxlaması "
         "bunu aşkar edir."),
        ("Simmetriya yoxlaması",
         "Başlanğıc və son vəziyyətin eyni olması. Yaxşı testin "
         "əlamətidir."),
        ("Mənfi təsdiq",
         "«Olması lazım olan şey yoxdur» yoxlaması. Silmədən sonra "
         "<code>404</code> almaq kimi."),
        ("Çıxış kodu (exit code)",
         "<code>0</code> = uğur, qeyri-sıfır = uğursuzluq. Skriptləri "
         "CI sistemlərinə və digər skriptlərə bağlayan mexanizm."),
        ("Sayğac naxışı",
         "<code>KECDI</code>/<code>XETA</code> dəyişənləri. Bütün "
         "yoxlamaları işlədib sonda <em>bir</em> qərar vermək."),
        ("trap",
         "Skript hansı səbəbdən bitsə də təmizlik funksiyasını çağırır. "
         "Server və müvəqqəti fayllar arxada qalmır."),
        ("Unikal e-poçt hiyləsi",
         "<code>test.crud.${date +%s}@...</code> — hər işlətmədə fərqli "
         "e-poçt. Təkrar işlətmə «409 təkrar» xətası vermir."),
        ("İdempotentlik",
         "Eyni əməliyyatın təkrar işlədilməsi nəticəni dəyişmir. "
         "<code>DELETE</code> idempotentdir: ikinci cəhd <code>404</code> "
         "verir, amma vəziyyət eyni qalır."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) Skriptin karkası</h5>
<ul>
  <li><code>cd "$(dirname "$0")/.." || exit 1</code> — 1B dərsindən tanış
      hiylə: skripti <em>haradan</em> işlətsəniz də layihə kökünə keçir.
      <code>skriptler/</code> içindən <code>..</code> bir səviyyə
      yuxarıdır.</li>
  <li><code>TMP="/tmp/arti_crud_$$"</code> — <code>$$</code> skriptin
      <em>öz PID-i</em>dir. Beləcə eyni anda iki nüsxə işləsə, onların
      müvəqqəti faylları toqquşmaz.</li>
  <li><code>temizle()</code> + <code>trap temizle EXIT INT TERM</code> —
      həm serveri söndürür, həm müvəqqəti qovluğu silir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2) <code>sorqu()</code> — ürək funksiyası</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
sorqu() {
  METOD="$1"; YOL="$2"; GOVDE="$3"; GOZLE="$4"
  if [ -z "$GOVDE" ]; then
    KOD=$(curl -s -o "$CAVAB" -w '%{http_code}' -X "$METOD" "$YOL")
  else
    KOD=$(curl -s -o "$CAVAB" -w '%{http_code}' -X "$METOD" "$YOL" \\
          -H 'Content-Type: application/json' -d "$GOVDE")
  fi
  ...
}</pre>
<ul>
  <li><code>$1</code>…<code>$4</code> — <em>mövqe parametrləri</em>.
      Funksiyaya belə çağırılır:
      <code>sorqu POST "$BAZ" '{...}' 201</code>.</li>
  <li><code>curl -s -o "$CAVAB" -w '%{http_code}'</code> — cavabın
      <em>gövdəsini</em> fayla yazır, <em>status kodunu</em> isə ekrana.
      <code>$(...)</code> onu tutub dəyişənə yazır.
      <strong>Diqqət:</strong> <code>-w</code> olmasa, status kodunu
      öyrənmək üçün cavabı parse etməli olardıq.</li>
  <li><code>-H 'Content-Type: application/json'</code> — <strong>mütləqdir</strong>.
      Bu başlıq olmasa, Express gövdəni JSON kimi parse etmir və
      <code>@Body()</code> boş obyekt alır → <code>400</code>, amma
      səbəbi anlaşılmaz olur.</li>
  <li><code>[ "$KOD" = "$GOZLE" ]</code> — uğur yoxlaması. Bərabərdirsə
      <code>KECDI++</code>, deyilsə <code>XETA++</code> və cavabın ilk
      300 simvolu göstərilir. Bu son detal <strong>debug üçün
      əvəzedilməzdir</strong>: uğursuzluğun səbəbini dərhal görürsünüz.</li>
  <li><code>QISA="${YOL#$BAZ}"</code> — <em>prefiks silmə</em>. <code>#</code>
      işarəsi «əvvəldən bu naxışı sil» deməkdir. Beləcə uzun
      <code>http://localhost:4000/api/v1/emekdaslar</code> əvəzinə qısa
      <code>emekdaslar</code> görünür.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3) <code>saha()</code> — cavabdan dəyər oxumaq</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
saha() {
  python3 -c "
import json, sys
d = json.load(open('$TMP/cavab.json'))
for a in sys.argv[1:]:
    d = d.get(a) if isinstance(d, dict) else None
    if d is None: break
print('' if d is None else ...)
" "$@"
}</pre>
<p>Bash özü JSON-u <em>oxuya bilmir</em> — ona görə <code>python3</code>-ü
köməyə çağırırıq. <code>"$@"</code> funksiyaya verilən bütün arqumentləri
python-a ötürür: <code>saha data id</code> → <code>d['data']['id']</code>.</p>
<p>Alternativ: <code>jq</code> aləti (macOS-da əvvəlcədən yoxdur).
<code>python3</code> isə macOS ilə gəlir — ona görə onu seçdik.</p>

<h5 style="color:#334155;margin-top:1rem">4) Unikal e-poçt</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
EPOX=$(date +%s)
EPOST="test.crud.${EPOX}@arti.edu.az"</pre>
<p><code>date +%s</code> — Unix vaxtı (1970-ci ildən bu yana saniyələr).
Hər saniyə fərqli ədəd verir, ona görə e-poçt <strong>unikal</strong>
olur və skripti ard-arda 10 dəfə işlətsək də <code>409</code> xətası
<em>gözlənilməz yerdə</em> çıxmır.</p>
<p>Skriptin <em>ikinci</em> hissəsində isə <code>409</code>-u
<strong>qəsdən</strong> yaradırıq — eyni e-poçtu ikinci dəfə göndərməklə.
Yəni eyni skriptdə həm unikallıq, həm təkrar yoxlanılır.</p>

<h5 style="color:#334155;margin-top:1rem">5) URL kodlaşdırması</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
sorqu GET "$BAZ?axtar=%C6%8Fliyev" "" 200</pre>
<p><code>%C6%8F</code> — <code>Ə</code> hərfinin UTF-8 kodlaşdırılmış
forması. <strong>Niyə açıq yazmırıq?</strong> Çünki URL-də qeyri-ASCII
simvollar texniki olaraq icazəli deyil. <code>curl</code> onları
avtomatik kodlaşdıra <em>bilər</em>, amma bu, versiya və mühitdən asılıdır.
Açıq kodlaşdırma <strong>hər yerdə</strong> işləyir.</p>
<p>Əgər skriptdə Azərbaycan hərfi yazmaq lazım olsa, terminalda
<code>python3 -c "import urllib.parse; print(urllib.parse.quote('Əliyev'))"</code>
ilə kodu öyrənə bilərsiniz.</p>

<h5 style="color:#334155;margin-top:1rem">6) Nəticə bloku</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
if [ "$XETA" -eq 0 ]; then
  printf '  ✓ BÜTÜN CRUD VƏ XƏTA HALLARI DÜZGÜN İŞLƏYİR\\n'
  exit 0
fi
printf '  ✗ %s YOXLAMA UĞURSUZ\\n' "$XETA"
printf '  server loqu: %s\\n' "$LOQ"
exit 1</pre>
<p>Uğursuz halda log faylının yolunu göstəririk — istifadəçi dərhal
oraya baxıb səbəbi tapa bilər. Yaxşı xəta mesajı <em>nə olub</em> və
<em>hara baxmalı</em> olduğunu deyir.</p>
""",
    "fayllar": ["skriptler/crud_yoxla.sh"],
    "goster": [],
    "c": r"""
echo "════ 1) Skriptin sintaksisi ════"
if bash -n skriptler/crud_yoxla.sh; then
  echo "  ✓ bash sintaksisi düzgündür"
else
  echo "  ✗ sintaksis xətası var"
  exit 1
fi
printf '      sətir sayı     : %s\n' "$(wc -l < skriptler/crud_yoxla.sh | tr -d ' ')"
printf '      yoxlama sayı   : %s\n' "$(grep -c '^sorqu ' skriptler/crud_yoxla.sh)"

echo ""
echo "════ 2) Bazanın vəziyyəti (əvvəl) ════"
psql -U arti_user -h localhost -p 5432 -d arti_baza -At -c "
SELECT '      emekdaslar: ' || count(*) FROM kadrlar.emekdaslar;" 2>/dev/null

echo ""
echo "════ 3) BÜTÖV CRUD AXINI ════"
bash skriptler/crud_yoxla.sh
NETICE=$?

echo ""
echo "════ 4) Bazanın vəziyyəti (sonra) ════"
psql -U arti_user -h localhost -p 5432 -d arti_baza -At -c "
SELECT '      emekdaslar: ' || count(*) FROM kadrlar.emekdaslar;" 2>/dev/null

echo ""
echo "  → skriptin çıxış kodu: $NETICE"
""",
    "olmaz": """Skript olmasa — hər dəfə əl ilə yoxlamaq:

$ curl -X POST http://localhost:4000/api/v1/emekdaslar \\
    -H 'Content-Type: application/json' \\
    -d '{"ad":"Test","soyad":"Yoxlayici","ata_adi":"Sistem",
         "cinsiyyet_id":1,"vezife_id":6}'
{"id":"27","ad":"Test",...}

$ curl http://localhost:4000/api/v1/emekdaslar/27
{"id":"27",...}

$ curl -X PATCH http://localhost:4000/api/v1/emekdaslar/27 \\
    -H 'Content-Type: application/json' -d '{"maas":2500}'
{"id":"27","maas":"2500.00",...}

$ curl -X DELETE http://localhost:4000/api/v1/emekdaslar/27
{"nov":"hard",...}

  ← ✅ Dövran işlədi. AMMA:

  • Status kodlarını GÖRMÜRSÜNÜZ — curl onları yalnız
    -w ilə göstərir, siz isə yazmadınız.
  • 400/404/409 hallarını YOXLAMADINIZ.
  • Sətri bazadan həqiqətən sildiyinizi YOXLAMADINIZ.
  • Sətir sayının dəyişdiyini YOXLAMADINIZ.
  • Bu 4 əmri hər dəfə YENİDƏN yazacaqsınız.
  • Kimsə kodu dəyişəndə, yoxlamanı TƏKRARLAMAYACAQSINIZ.

────────────────────────────────────────────────────────────
VƏ YA ən pis hal — sətri silməyi unutsaq:

$ curl -X POST ... (10 dəfə işlədildi)

$ curl 'http://localhost:4000/api/v1/emekdaslar'
{"cem": 24, ...}
  ← ⚠️ Bazada 10 saxta "Test Yoxlayici" əməkdaşı var.
     Hansı real, hansı test? Ayırd etmək mümkün deyil.
     Onları əl ilə tapıb silmək yarım saat vaxt aparacaq.""",
    "c_izah": """
<p><strong>Birinci qazanc: <code>curl</code>-un <code>-w '%{http_code}'</code>
bayrağı.</strong> Onsuz biz yalnız cavabın gövdəsini görürük. Server
<code>201</code> yerine <code>200</code> qaytarsa, fərqi <em>görməyəcəyik</em> —
JSON eyni görünür. Status kodu API müqaviləsinin bir hissəsidir və onu
yoxlamaq mütləqdir.</p>
<p><strong>İkincisi: sərhəd halları.</strong> Yuxarıdaki əl ilə
yoxlamada yalnız «hər şey düzgün olanda» nə baş verdiyini gördük.
Amma real istifadəçilər <em>səhv</em> məlumat göndərir: natamam forma,
təkrar e-poçt, səhv ID. Skriptin 19 yoxlamasından <strong>8-i</strong>
məhz bu hallara aiddir. Onlar olmasa, xəta idarəsinin işlədiyini
bilməzdik.</p>
<p><strong>Üçüncüsü: simmetriya.</strong> <code>EVVEL=14</code> və
<code>SONRA=14</code>. Bu iki rəqəm bərabər olmasa, test <em>özü</em>
problemin mənbəyi olub. Bu, xüsusilə komanda işində vacibdir: biri
skripti işlədir, digəri bazada gözlənilməz dəyişiklik görür və
səbəbi tapılmır. Simmetriya yoxlaması belə halların qarşısını alır.</p>
<p><strong>Dördüncüsü: çıxış kodu.</strong> Skript <code>exit 0</code>
və ya <code>exit 1</code> qaytarır. Bu, onu <strong>CI/CD boru
xəttinə</strong> qoşmağa imkan verir: hər <code>git push</code>-da
avtomatik işləsin və uğursuz olsa, birləşdirmə (merge) bloklansın.
Bu, 2A dərsinin əsl nəticəsidir: kod <em>yalnız sizin maşınınızda</em>
deyil, hər yerdə işlədiyini sübut edir.</p>
<p><strong>Beşincisi: skript sənədləşdirmədir.</strong> Yeni bir
proqramçı layihəyə qoşulanda <code>skriptler/</code> qovluğuna baxır və
<em>dərhal</em> görür ki, bu API-də hansı əməliyyatlar var və necə
işlədilir. On min söz yazmaqdan qat-qat faydalıdır.</p>
""",
    "sual": [
        ("Niyə <code>bash skriptler/crud_yoxla.sh</code>, bəs <code>./skriptler/crud_yoxla.sh</code> deyil?", "Hər iki üsul işləyir, amma <code>bash</code> ilə çağırmaq daha etibarlıdır: faylın icra icazəsi (<code>chmod +x</code>) olmasa da işləyir və şebang (<code>#!/bin/bash</code>) sətri səhv olsa da problem yaratmır. Skriptləri paylaşanda bu, əlavə bir narahatlığı aradan qaldırır."),
        ("Niyə <code>jq</code> yox, <code>python3</code>?", "<code>jq</code> çox güclü alətdir, amma macOS-da <em>əvvəlcədən quraşdırılmır</em>. <code>python3</code> isə macOS və demək olar bütün Linux sistemlərində var. Dərsin qaydası: <strong>əlavə quraşdırma tələb etməyən alətlər seç</strong> — şagirdin yolu qısalsın."),
        ("Skripti hər dəfə <code>node dist/main.js</code> ilə server qaldırır. Bu, yavaş deyilmi?", "Build ~3 saniyə, serverin qalxması ~1 saniyə çəkir. Ümumi 4-5 saniyə — 19 yoxlama üçün məqbul qiymətdir. Sürəti artırmaq üçün serveri <em>əvvəlcədən</em> qaldırıb skriptə ötürmək olardı, amma onda skript təkbaşına işləyə bilməzdi. <strong>Sadəlik sürətdən üstündür</strong>: skript özü hər şeyi idarə edir."),
        ("<code>DELETE</code> üçün niyə <code>204 No Content</code> yox, <code>200</code>?", "<code>204</code> o zaman işlədilir ki, cavabın gövdəsi olmasın. Bizim <code>DELETE</code> isə <strong>gövdə qaytarır</strong>: silmə növü (<code>soft</code>/<code>hard</code>), mesaj və asılı qeydlərin sayı. Yəni cavab məlumat daşıyır, deməli <code>200</code> düzgündür. <code>204</code> qaytarsaydıq, istifadəçi nə baş verdiyini <em>bilməyəcəkdi</em> — xüsusilə yumşaq silmədə bu, vacibdir."),
        ("Test skripti uğursuz olanda nə etməliyəm?", "Əvvəlcə skriptin göstərdiyi <em>cavab gövdəsinə</em> baxın — uğursuz hər yoxlama öz cavabını çap edir. Sonra server loguna: skript sonda yolunu verir (<code>/tmp/arti_crud_PORT.log</code>). Ən çox rast gəlinən səbəblər: (1) köhnə server işləyir, (2) <code>npm run build</code> köhnədir, (3) bazada əvvəlki testdən zibil sətir qalıb."),
        ("Bu skripti Vitest testlərinə çevirmək olmaz?", "Olar və böyük layihələrdə belə edilir. Amma bu skriptin bir üstünlüyü var: <strong>həqiqi HTTP serverinə</strong> işləyir — build edilmiş <code>dist/main.js</code>-ə, real portda. Vitest-in <code>supertest</code>-i yaddaşda işləyir. İkisi tamamlayıcıdır: Vitest sürətli və tez-tez, bu skript isə «istehsalat kimi» və az-az."),
        ("Skripti Windows-da işlətmək olar?", "Birbaşa yox — <code>bash</code> və <code>curl</code> lazımdır. Seçimlər: (1) WSL (Windows Subsystem for Linux) — tövsiyə olunur; (2) Git Bash — işləyir, amma bəzi əmrlər fərqlidir; (3) Docker konteynerində işlətmək. Komandada hamı eyni mühitdə işləməlidir deyə, çox vaxt Docker seçilir — bu, Dərs 6-nın mövzusudur."),
        ("Skriptlərdə Azərbaycan şərhləri var — bu yaxşıdırmı?", "Bu layihədə <strong>bəli</strong>, çünki komanda Azərbaycandilli və şagirdlər Azərbaycanca öyrənir. Vacib qayda: <em>ardıcıl</em> olmaq. Yarısı İngilis, yarısı Azərbaycan olan kod ən pis haldir. Hər halda <strong>dəyişən adları</strong> daha diqqətli seçilməlidir: <code>GOVDE</code>, <code>GOZLE</code> kimi adlar ASCII yazılmalıdır, çünki <code>bash</code> qeyri-ASCII dəyişən adlarını <em>qəbul etmir</em>. Bu, ADDIM 21-də real olaraq yaşadığımız problemdir."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li><strong>19 yoxlama</strong> avtomatik icra olundu və hamısı keçdi:
      5 qızıl yol addımı, 8 xəta halı, 3 siyahı/filtr/axtarış yoxlaması,
      2 idempotentlik yoxlaması və 1 simmetriya yoxlaması.</li>
  <li><strong>CRUD dövranı tamamlandı:</strong> yarat → oxu → dəyiş →
      sil → təsdiq. Hər addımın status kodu gözlənilən idi.</li>
  <li><strong>Xəta kodları düzgün işləyir:</strong>
      <code>400</code> (validasiya), <code>400</code> (xarici açar),
      <code>409</code> (təkrar e-poçt), <code>404</code> (tapılmadı),
      <code>400</code> (mətn ID).</li>
  <li><strong>Filtr və axtarış işləyir:</strong> səhifələmə
      (<code>seife=2</code>), sıralama (<code>soyad asc</code>),
      axtarış (<code>Əliyev</code> → 2 nəticə), filtr
      (<code>merkez_id=1</code> → 3 əməkdaş).</li>
  <li><strong>Baza toxunulmaz qaldı:</strong> əvvəl 14, sonra 14.
      Test özü heç bir zibil buraxmadı.</li>
</ul>

<h3 style="color:#0f766e;margin-top:1.4rem">📘 Dərs 2A-nın yekunu</h3>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.7rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Addım</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Nə öyrəndik</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Əməli sübut</th>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>17</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">DTO, class-validator,
        <code>ValidationPipe</code>, ağ siyahı</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">25 validasiya
        qaydası yoxlanıldı</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>18</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Mapper, BigInt,
        Decimal, <code>select</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">BigInt xətası canlı
        görüldü və həll edildi</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>19</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Servis, səhifələmə,
        <code>$transaction</code>, yumşaq silmə</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">34 yoxlama — hamısı
        real bazada</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>20</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">REST, controller,
        modul, DI</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">7 marşrut qeydiyyatdan
        keçdi, Swagger yeniləndi</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>21</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Bütöv CRUD dövranı,
        xəta halları, simmetriya</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">19 yoxlama, baza
        toxunulmaz</td>
  </tr>
</table>

<h3 style="color:#0f766e;margin-top:1.4rem">🚀 2B dərsində nə olacaq</h3>
<ol>
  <li><strong>Əlaqələr:</strong> bir əməkdaşın doktorantları,
      sertifikatları, şura üzvlüyü — ayrı endpoint-lərlə.</li>
  <li><strong>Statistika:</strong> <code>GET /emekdaslar/statistika</code> —
      Prisma <code>groupBy</code> və <code>aggregate</code> ilə
      mərkəz/vəzifə üzrə hesabatlar. Burada marşrut sırası qaydası
      həqiqətən lazım olacaq!</li>
  <li><strong>Toplu əməliyyatlar:</strong> <code>createMany</code>,
      <code>updateMany</code> və Excel-dən idxal.</li>
  <li><strong>Audit loq:</strong> hər dəyişikliyi
      <code>audit.audit_log</code> cədvəlinə yazmaq (tranzaksiya
      içində).</li>
  <li><strong>Optimallaşdırma:</strong> <code>select</code> ilə
      müqayisə, indekslərin rol, <code>EXPLAIN ANALYZE</code>.</li>
</ol>

<p style="background:#f0fdfa;border-left:5px solid #14b8a6;border-radius:10px;
          padding:1rem 1.2rem;margin-top:1rem">
<strong>💡 Ən vacib vərdiş:</strong> hər yeni endpoint yazandan sonra
<em>dərhal</em> onu yoxlayan bir sətir əlavə edin — istər skriptə,
istər testə. Bir dəfə yazılan yoxlama min dəfə işləyir. Bu dərsdə
gördüyünüz <code>skriptler/</code> qovluğu məhz belə yaranıb: hər addım
öz yoxlama alətini özü ilə gətirir.
</p>
""",
})
