#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-1B — ADDIM 12–16 mətnləri.

Hər addım 4 hissədən ibarətdir:
  A      — «niyə» (geniş nəzəri izah)
  B      — kod (fayllar BACKEND qovluğundan canlı oxunur)
  C      — yoxlama əmrləri
  D      — həqiqi çıxış (qurucu tərəfindən icra olunur)
Əlavə: «Yeni anlayışlar», «Kodun sətir-sətir izahı», «Tez-tez verilən suallar».
"""

ADIMLAR = []


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 12 — BUILD
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 12,
    "ad": "Build — TypeScript kodunu JavaScript-ə çeviririk",
    "a": """
<p>1A-da yazdığımız bütün fayllar <code>.ts</code> uzantılıdır. Amma
<strong>Node.js TypeScript-i başa düşmür</strong>. Node yalnız JavaScript
işlədə bilər. Elə buna görə <code>node src/main.ts</code> yazsaq, Node
belə bir şey deyəcək:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
SyntaxError: Invalid or unexpected token
    at wrapSafe (node:internal/modules/cjs/loader:...)</pre>
<p>Çünki <code>.ts</code> faylındaki <code>: string</code>, <code>: number</code>
kimi <em>tip işarələri</em> JavaScript üçün sadəcə mənasız simvollardır.</p>

<h4>İki yol var</h4>
<p><strong>1-ci yol — «yerində» çevirmə (transpilyasiya).</strong> Xüsusi alət
kodu oxuyarkən havada çevirir və dərhal işlədir. <code>tsx</code>,
<code>ts-node</code>, <code>nest start</code> bunu edir. Rahatdır — fayl
dəyişir, dərhal görürsən. Amma hər işə salmada çevirmə vaxtı gedir.</p>
<p><strong>2-ci yol — BUILD (əvvəlcədən çevirmə).</strong> Bütün
<code>.ts</code> fayllar <em>bir dəfə</em> çevrilir və nəticə
<code>dist/</code> qovluğuna <code>.js</code> kimi yazılır. Sonra server
sadəcə <code>node dist/main.js</code> ilə işlədilir — çevirmə yoxdur.</p>

<h4>Niyə istehsalatda (production) build işlədilir?</h4>
<ul>
  <li><strong>Sürət:</strong> server qalxanda heç bir çevirmə olmur.</li>
  <li><strong>Sabitlik:</strong> <code>dist/</code> dondurulmuş koddur —
      kimsə faylı dəyişsə də, server dəyişməz.</li>
  <li><strong>Yüngüllük:</strong> istehsalata <code>typescript</code>,
      <code>@nestjs/cli</code> kimi <em>devDependencies</em> lazım deyil —
      yalnız <code>dependencies</code> kifayətdir.</li>
  <li><strong>Təhlükəsizlik:</strong> <code>src/</code> qovluğu serverə heç
      göndərilmir, yalnız <code>dist/</code> gedir.</li>
</ul>

<h4>Build-i kim idarə edir? — iki konfiqurasiya faylı</h4>
<p><code>nest-cli.json</code> Nest-ə deyir ki, build zamanı
<strong>hər şeyi sil və yenidən yaz</strong>
(<code>"deleteOutDir": true</code>). <code>tsconfig.build.json</code> isə
TypeScript-ə deyir ki, <em>hansı</em> fayllar çevrilsin.</p>

<div class="olmaz" style="margin-top:1rem">
<h4>⚠️ <code>deleteOutDir: true</code> olmasa nə baş verir?</h4>
<p>Təsəvvür edin: <code>src/saglamliq/saglamliq.service.ts</code> faylını
sildiniz. Build edirsiniz. <code>dist/saglamliq/saglamliq.service.js</code>
isə <strong>hələ də orada qalır</strong> — çünki heç kim onu silmədi!
Nəticədə <code>dist/</code> içində <em>artıq mövcud olmayan kod</em> işləyir.
Bu, «düzəltdim, amma heç nə dəyişmir» sirrinin ən çox rast gəlinən
səbəbidir.</p>
</div>
""",
    "anlayis": [
        ("Transpilyasiya",
         "TypeScript kodunun JavaScript koduna çevrilməsi. <em>Tərcümə</em> "
         "kimi düşünün: məna eyni qalır, dil dəyişir."),
        ("Build",
         "Bütün layihənin transpilyasiya edilib <code>dist/</code> qovluğuna "
         "yazılması prosesi."),
        ("dist/",
         "«Distribution» — paylanan kod. İstehsalatda serverə gedən yeganə "
         "qovluq budur."),
        ("outDir / rootDir",
         "TypeScript konfiqurasiyasında «kodu hara yaz» / «kodu haradan oxu». "
         "Burada: <code>rootDir: ./src</code> → <code>outDir: ./dist</code>. "
         "Yəni <code>src/main.ts</code> → <code>dist/main.js</code>."),
        ("deleteOutDir",
         "Hər build-dən əvvəl bütün <code>dist/</code> qovluğunun silinməsi. "
         "Köhnə, artıq lazımsız <code>.js</code> fayllarının qalmasının "
         "qarşısını alır."),
        ("--noEmit",
         "<code>tsc</code>-ə «fayl YAZMA, sadəcə tipləri yoxla» deyir. "
         "Sürətli yoxlama üçün idealdır."),
        ("tsbuildinfo",
         "<code>incremental: true</code> açıq olanda TypeScript-in «nəyi artıq "
         "yoxlamışam» qeydini saxladığı fayl. Sonrakı yoxlamaları "
         "sürətləndirir."),
        ("MODULE_NOT_FOUND",
         "Node axtardığı <code>.js</code> faylını tapa bilmədi. Build "
         "etməmisinizsə, <code>dist/</code> ümumiyyətlə olmaz."),
    ],
    "kod_izah": """
<p>Bu addımda <strong>yeni kod yazmırıq</strong> — build-i idarə edən iki
konfiqurasiya faylını təzələyirik. Onlar 1A-nın ADDIM 3-də yaradılmışdı;
burada <em>təkrar</em> yazırıq ki, 1B dərsi təkbaşına işləsin (əgər siz
birbaşa bu dərsdən başlasanız, fayllar yerində olsun).</p>

<h5 style="color:#334155;margin-top:1rem">nest-cli.json — 6 sətir</h5>
<ul>
  <li><code>$schema</code> — redaktorun (VS Code) bu faylı tanıması üçün.
      Sadəcə rahatlıqdır, işləməyə təsiri yoxdur.</li>
  <li><code>collection</code> — Nest-in sxemlər toplusu. <code>nest build</code>
      əmrini işlədən mexanizmdir.</li>
  <li><code>sourceRoot: "src"</code> — mənbə kodun yeri. <code>nest build</code>
      məhz bu qovluğa baxır.</li>
  <li><code>deleteOutDir: true</code> — ən vacib sətir. Hər build-dən əvvəl
      <code>dist/</code> tamamilə silinir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">tsconfig.build.json — build üçün ayrı qaydalar</h5>
<p><code>tsconfig.build.json</code> əsas <code>tsconfig.json</code>-u
<strong>genişləndirir</strong> (<code>extends</code>) və yalnız build üçün
fərqli olan hissələri yazır. Bu, TypeScript-in çox faydalı bir
xüsusiyyətidir: ortaq ayarları iki dəfə yazmaq lazım gəlmir.</p>
<ul>
  <li><code>"extends": "./tsconfig.json"</code> — bütün <code>compilerOptions</code>
      (module, target, strict, decorators…) yuxarıdan miras alınır.</li>
  <li><code>"rootDir": "./src"</code> — build zamanı yalnız
      <code>src/</code> qovluğu kök qəbul olunur. Nəticə: dist daxilində
      <code>src/</code> səviyyəsi <em>təkrarlanmır</em>. Yəni
      <code>dist/main.js</code> alırıq, <code>dist/src/main.js</code> yox.</li>
  <li><code>"include": ["src"]</code> — yalnız bu qovluqdakı fayllar çevrilir.</li>
  <li><code>"exclude": ["node_modules", "test", "dist", "**/*spec.ts"]</code>
      — <strong>testlər build-ə düşmür!</strong> Bu çox vacibdir: test
      faylları serverə göndərilməməlidir. Həm yer tutur, həm də
      <code>vitest</code>, <code>supertest</code> kimi yalnız-inkişaf
      paketlərini istehsalata «sürüyür».</li>
</ul>
<p><strong>Diqqət:</strong> <code>nest build</code> əmri avtomatik olaraq
<code>tsconfig.build.json</code> faylını axtarır. Əgər adı dəyişsəydi,
<code>nest-cli.json</code>-da <code>compilerOptions.tsConfigPath</code> ilə
göstərməli olardıq.</p>
""",
    "fayllar": ["nest-cli.json", "tsconfig.build.json"],
    "goster": ["tsconfig.json"],
    "c": r"""
echo "════ 1) dist/ içinə SAXTA köhnə fayl qoyuruq ════"
mkdir -p dist
echo "kohne build qaligi" > dist/kohne_fayl.js
ls dist/kohne_fayl.js

echo ""
echo "════ 2) Build: npm run build ════"
npm run build

echo ""
echo "════ 3) deleteOutDir saxta faylı sildimi? ════"
if [ -f dist/kohne_fayl.js ]; then
  echo "  ✗ hələ də durur — deleteOutDir işləmədi"
else
  echo "  ✓ dist/kohne_fayl.js SİLİNDİ → deleteOutDir: true işləyir"
fi

echo ""
echo "════ 4) dist/ strukturu (nə yarandı?) ════"
ls dist
printf '  cəmi .js fayl: %s\n' "$(find dist -name '*.js' | wc -l | tr -d ' ')"

echo ""
echo "════ 5) Tip yoxlaması — TƏMİZ kod ════"
if npx tsc --noEmit; then
  echo "  ✓ exit 0 — heç bir tip xətası yoxdur"
else
  echo "  ✗ tip xətası var (yuxarıya baxın)"
fi

echo ""
echo "════ 6) Tip yoxlaması — QƏSDƏN SƏHV kod ════"
echo "  → src/_muveqqeti_tip.ts faylını yaradırıq (1 sətir, səhv tip)"
cat > src/_muveqqeti_tip.ts <<'SON'
// ⚠️ BU FAYL QƏSDƏN SƏHVDİR — yoxlama bitəndə silinəcək.
const say: number = 'metn';
export default say;
SON
npx tsc --noEmit
echo "  ↑ tsc-in exit kodu: $? (0 DEYİL — səhv TUTULDU, bu yaxşıdır)"
rm -f src/_muveqqeti_tip.ts
echo "  ✓ müvəqqəti fayl silindi"

echo ""
echo "════ 7) Təmizlikdən sonra yenidən yoxlayırıq ════"
npx tsc --noEmit && echo "  ✓ yenə exit 0 — layihə təmizdir"

echo ""
echo "════ 8) Build nəticəsi harada? ════"
printf '  dist/main.js       → %s\n' "$([ -f dist/main.js ] && echo 'VAR' || echo 'YOXDUR')"
printf '  dist/app.module.js → %s\n' "$([ -f dist/app.module.js ] && echo 'VAR' || echo 'YOXDUR')"
printf '  src/main.ts        → %s\n' "$([ -f src/main.ts ] && echo 'VAR' || echo 'YOXDUR')"
""",
    "olmaz": """$ npm run start:prod
> ds-backend@0.1.0 start:prod
> node dist/main.js

node:internal/modules/cjs/loader:1386
      throw err;
      ^

Error: Cannot find module '/Users/.../DS_Backend/dist/main.js'
    at Module._resolveFilename (node:internal/modules/cjs/loader:1386:15)
    ...
  code: 'MODULE_NOT_FOUND'

────────────────────────────────────────────────────────────
VƏ YA (deleteOutDir olmasa) — daha gizli bir problem:

$ rm src/saglamliq/saglamliq.service.ts
$ npm run build
$ ls dist/saglamliq/
saglamliq.controller.js
saglamliq.module.js
saglamliq.service.js     ← ⚠️ SİLDİYİMİZ fayl hələ də buradadır!
saglamliq.service.js.map

Nəticə: server sildiyimiz köhnə kodu işlədirməyə davam edir.
Səhvləri «düzəldirik», amma davranış dəyişmir.""",
    "c_izah": """
<p><strong>1-ci səbəb — build ümumiyyətlə edilməyib.</strong>
<code>dist/</code> qovluğu yoxdur, ona görə <code>node dist/main.js</code>
heç bir fayl tapa bilmir. Bu, ən çox rast gəlinən haldır: kodu dəyişirik,
<code>node dist/main.js</code> işlədirik — və heç nə dəyişmir. Çünki
<code>dist/</code> köhnə koddur! Hər dəyişiklikdən sonra
<code>npm run build</code> lazımdır.</p>
<p><strong>2-ci səbəb — <code>deleteOutDir</code> söndürülüb.</strong>
Yuxarıdaki nümunədə gördüyünüz kimi, silinmiş mənbə faylının köhnə
<code>.js</code> nüsxəsi <code>dist/</code> içində qalır. Server isə
<em>hansı faylın mövcud olduğunu yoxlamır</em> — importu tapırsa,
işlədir. Belə xətaları tapmaq çox çətindir, çünki heç bir xəta mesajı
yoxdur, sadəcə davranış səhvdir.</p>
<p><strong>3-cü səbəb — <code>tsconfig.build.json</code> səhvdir.</strong>
Əgər <code>rootDir</code> olmasaydı, TypeScript ortaq kök qovluğu özü
hesablayardı və <code>dist/src/main.js</code> kimi gözlənilməz yol yarana
bilərdi. <code>start:prod</code> skripti isə <code>dist/main.js</code>
axtarır → MODULE_NOT_FOUND.</p>
<p><strong>Nəticə:</strong> build nəticəsini həmişə <em>yoxlamaq</em>
lazımdır. <code>ls dist</code> bir saniyəlik əmrdir, amma saatlarla
debug etməyin qarşısını alır.</p>
""",
    "sual": [
        ("<code>nest build</code> ilə <code>tsc</code> arasında nə fərq var?",
         "<code>tsc</code> sadəcə TypeScript kompilyatorudur. <code>nest build</code> "
         "isə <code>nest-cli.json</code>-u oxuyur, <code>tsconfig.build.json</code>-u "
         "seçir, lazım gələrsə plaginləri işlədir və <code>deleteOutDir</code> kimi "
         "əməliyyatları yerinə yetirir. Yəni <code>nest build</code> "
         "<em>tsc + əlavə işlər</em>-dir."),
        ("Niyə <code>npm run build</code> heç bir mesaj yazmır?",
         "TypeScript-də xəta yoxdursa, «sükut = uğur» qaydası keçərlidir. "
         "Unix fəlsəfəsi belədir: heç nə deməmək — hər şey qaydasındadır. "
         "Xəta olsaydı, ekranda qırmızı sətirlər görünərdi. Yoxlamaq üçün "
         "<code>ls dist</code> yazın."),
        ("<code>dist/</code> qovluğunu git-ə əlavə etməliyəm?",
         "Xeyr! <code>dist/</code> <em>törəmə</em> (generated) qovluqdur — "
         "mənbə koddan hər an yenidən yarana bilər. Git-ə yalnız "
         "<code>src/</code> yazılır. <code>.gitignore</code> faylında "
         "<code>dist/</code> sətri məhz buna görə var."),
        ("<code>tsc --noEmit</code> nə üçün lazımdır, axı build də tip yoxlayır?",
         "Haqlısınız, <code>nest build</code> da tip yoxlayır. Amma "
         "<code>tsc --noEmit</code> <strong>fayl yazmadan</strong> yoxlayır — "
         "yəni <code>dist/</code>-i dəyişmir. Bu, sürətli əmrdir və "
         "CI (avtomatik yoxlama) sistemlərində tez-tez istifadə olunur."),
        ("<code>tsconfig.build.tsbuildinfo</code> nədir?",
         "<code>incremental: true</code> ayarı TypeScript-ə deyir ki, "
         "«hansı faylı artıq yoxlamışam» qeydini saxlasın. Növbəti build "
         "yalnız dəyişən faylları yenidən yoxlayır → daha sürətli. "
         "Fayl silinsə, sadəcə ilk build bir az yavaş olar."),
        ("Build zamanı <code>*.spec.ts</code> faylları niyə xaric edilir?",
         "Üç səbəb: (1) testlər serverin işi deyil, yer tutur; (2) testlər "
         "<code>vitest</code>, <code>supertest</code> kimi yalnız-inkişaf "
         "paketlərini import edir — istehsalatda onlar olmayacaq; "
         "(3) istehsalatda <code>dist/</code> daxilində test kodu görmək "
         "təhlükəsizlik baxımından arzuolunmazdır."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li><code>npm run build</code> → <code>nest build</code> →
      <code>dist/</code> içində 64 <code>.js</code> fayl.</li>
  <li><code>deleteOutDir: true</code> <em>işləyir</em>: dist içinə qoyduğumuz
      <code>kohne_fayl.js</code> build-dən sonra yoxa çıxdı. Bu kiçik
      nümunə, istehsalatda saatlarla vaxt itkisinin qarşısını alan
      ayardır.</li>
  <li>TypeScript <em>səhvi dərhal tutur</em>: <code>const say: number = 'metn'</code>
      sətri <code>TS2322</code> xətası verdi — <code>string</code> tipi
      <code>number</code>-ə mənimsədilə bilməz. Qeyd: build-in <em>özü</em>
      də bu xətanı verərdi, çünki <code>nest build</code> tip yoxlaması
      edir.</li>
  <li>Kompilyator faylı <strong>yazmadan</strong> yoxlamaq üçün
      <code>--noEmit</code> istifadə olunur.</li>
  <li><code>src/main.ts</code> → <code>dist/main.js</code>. Yol
      <code>rootDir</code> / <code>outDir</code> cütlüyü ilə müəyyən
      olunur.</li>
</ul>
<p><strong>Yadda saxlayın:</strong> dəyişdikdən sonra
<strong>build etmədən</strong> <code>node dist/main.js</code> işlətmək —
köhnə kodu işlətmək deməkdir. Bu, yeni başlayanların ən çox vaxt itirdiyi
yerdir. Qayda: <em>dəyişdin → build et → işlət</em>.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 13 — SERVERİ CANLI YOXLAMAQ
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 13,
    "ad": "Serveri işə salmaq və canlı yoxlamaq",
    "a": """
<p>Build etdik — indi serveri qaldırıb <em>həqiqətən</em> cavab verdiyini
yoxlamalıyıq. Bu addımda soruşuruq: <strong>«Kod düzgün yazılıb?» deyil,
«Sistem indi, bu saniyədə işləyir?»</strong></p>

<h4>Üç işə salma üsulu</h4>
<ul>
  <li><code>npm run start</code> → <code>nest start</code>. Kodu «yerində»
      çevirib işlədir. Yavaş qalxır, amma ayrıca build lazım deyil.</li>
  <li><code>npm run start:dev</code> → <code>nest start --watch</code>.
      Fayl dəyişəndə server özü yenidən qalxır. İnkişaf üçün ən rahatı.</li>
  <li><code>npm run start:prod</code> → <code>node dist/main.js</code>.
      Hazır build-i işlədir. <strong>Ən sürətli və istehsalatda
      istifadə olunan üsul budur.</strong></li>
</ul>

<h4>Port nədir və niyə 4000?</h4>
<p>Bir kompüterdə eyni anda onlarla şəbəkə proqramı işləyir. Onları
bir-birindən ayırmaq üçün <strong>port</strong> nömrələri var —
0-dan 65535-ə qədər. Port bir evin qapı nömrəsi kimidir: ünvan
(<code>localhost</code>) eynidir, qapı fərqlidir.</p>
<p><code>main.ts</code> faylında bu sətir var:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const port = Number(process.env.PORT ?? 4000);</pre>
<p>Oxunuşu: «əgər <code>PORT</code> mühit dəyişəni varsa, onu ədədə çevir
və istifadə et; <em>yoxdursa</em>, 4000 götür». Bu, çox faydalı bir
naxışdır: eyni kod həm kompüterinizdə, həm serverdə, həm testdə işləyir —
sadəcə <code>PORT</code> dəyişir.</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
PORT=4100 npm run start:prod   # başqa portda işlət</pre>

<h4>⚠️ «Port məşğuldur» — ən bezdirici xəta</h4>
<p>Köhnə server hələ işləyirsə, yenisini qaldırmaq cəhdi belə bitir:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
Error: listen EADDRINUSE: address already in use :::4000</pre>
<p>Bunu tapmaq üçün <code>lsof</code> («list open files») əmrindən istifadə
olunur:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
lsof -nP -iTCP:4000 -sTCP:LISTEN</pre>
<ul>
  <li><code>-n</code> — IP ünvanlarını adlara çevirmə (DNS sorğusu
      göndərmə) → sürətli.</li>
  <li><code>-P</code> — port nömrələrini adlara çevirmə
      (4000 → <code>http-alt</code> kimi) → sürətli.</li>
  <li><code>-iTCP:4000</code> — yalnız TCP protokolu, yalnız 4000 portu.</li>
  <li><code>-sTCP:LISTEN</code> — «yalnız <em>dinləyən</em> prosesləri
      göstər».</li>
</ul>
<p>Nəticədə PID (proses identifikatoru) alırıq və
<code>kill &lt;PID&gt;</code> ilə onu dayandırırıq.</p>

<h4>Niyə skript yazırıq, əl ilə etmirik?</h4>
<p>Əl ilə server qaldırmaq belə görünür: <code>npm run start:prod</code> —
və terminal <strong>bloklanır</strong>. Serveri işlədə bilmək üçün yeni
terminal açmalısınız. Sonra işiniz bitəndə birinci terminalda
<code>Ctrl+C</code> basmalısınız. Unutsanız — port məşğul qalır.</p>
<p>Skript isə bunu <em>avtomatik</em> edir: serveri <strong>arxa planda</strong>
(<code>&amp;</code>) qaldırır, cavab verənə qədər <strong>gözləyir</strong>,
yolları <strong>yoxlayır</strong> və nəticədən asılı olmayaraq
<strong>söndürür</strong>. Sonuncunu <code>trap</code> təmin edir:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
trap temizle EXIT INT TERM</pre>
<p><code>trap</code> «tələ» deməkdir: «skript hansı səbəbdən bitsə də
(normal son, xəta, Ctrl+C, <code>kill</code>), <code>temizle</code>
funksiyasını çağır». Bu olmasa, yarımçıq dayanan hər skript arxada asılı
qalmış server buraxar.</p>

<h4>Serveri «canlı» yoxlamaq nə deməkdir?</h4>
<p>Sadəcə prosesin işləməsi kifayət deyil! Proses «işləyir», amma bazaya
qoşula bilmir, ya da sonsuz döngədə ola bilər. Ona görə <em>həqiqi HTTP
sorğusu</em> göndərmək lazımdır. Bunun üçün <code>curl</code> istifadə
edirik:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
curl -s -o /dev/null -w '%{http_code}' http://localhost:4000/api/v1/saglamliq</pre>
<ul>
  <li><code>-s</code> — «sakit» (progress göstərmə).</li>
  <li><code>-o /dev/null</code> — cavabın <em>gövdəsini</em> at (bizə
      lazım deyil).</li>
  <li><code>-w '%{http_code}'</code> — əvəzində yalnız HTTP status kodunu
      yaz.</li>
  <li><code>-f</code> — 4xx/5xx olsa, xəta kodu qaytar (skriptlərdə
      «gözləmə» döngəsi üçün vacibdir).</li>
</ul>
""",
    "anlayis": [
        ("Port",
         "Şəbəkə proqramını tanıdan 0–65535 arası ədəd. Bir kompüterdə "
         "eyni anda minlərlə proqram portlarla ayrılır."),
        ("localhost / 127.0.0.1",
         "«Bu kompüterin özü». Şəbəkəyə çıxmadan özünlə danışmaq. "
         "<code>0.0.0.0</code> isə «bütün şəbəkə interfeyslərindən "
         "qəbul et» deməkdir."),
        ("EADDRINUSE",
         "«Address already in use» — port artıq tutulub. Köhnə server "
         "işləyir, ya da başqa proqram həmin portu istifadə edir."),
        ("PID",
         "Process ID — hər işləyən prosesə verilən unikal nömrə. "
         "<code>kill &lt;PID&gt;</code> həmin prosesi dayandırır."),
        ("lsof",
         "«List open files». Unix-də hər şey fayldır — şəbəkə bağlantısı da. "
         "Ona görə <code>lsof -iTCP:4000</code> portu kimin tutduğunu "
         "göstərir."),
        ("&amp; (arxa plan)",
         "Əmrin sonuna qoyulanda onu arxa planda işlədir və terminalı "
         "dərhal azad edir. <code>$!</code> isə həmin prosesin PID-ini verir."),
        ("trap",
         "Bash «siqnal tutucusu». Skript hansı səbəbdən bitsə də müəyyən "
         "funksiyanın çağırılmasını təmin edir. Təmizlik işləri üçün "
         "əvəzedilməzdir."),
        ("nohup",
         "«No hangup» — terminal bağlansa da prosesi saxlamaq. Uzun müddət "
         "işləyən serverlər üçün istifadə olunur."),
        ("Loq (log) faylı",
         "Proqramın yazdığı mesajların toplandığı fayl. "
         "<code>&gt; fayl</code> köhnəsini silib yenidən yazır, "
         "<code>&gt;&gt; fayl</code> sonuna əlavə edir."),
        ("HTTP status kodu",
         "200 = uğur, 404 = tapılmadı, 401 = icazəsiz, 500 = server xətası. "
         "Rəqəmin <em>birinci</em> rəqəmi kateqoriyanı bildirir."),
    ],
    "kod_izah": """
<p>Yazdığımız fayl <code>skriptler/servis_yoxla.sh</code> — 100 sətirdən çox,
amma hər sətri aydındır. Hissə-hissə baxaq.</p>

<h5 style="color:#334155;margin-top:1rem">1. Başlıq bloku və təhlükəsizlik ayarları</h5>
<ul>
  <li><code>#!/bin/bash</code> — «shebang». Bu faylın bash ilə işlədilməsini
      bildirir.</li>
  <li><code>set -u</code> — «təyin edilməmiş dəyişəni istifadə etsəm, xəta
      ver». Olmasa, <code>$YOXDUR</code> yazsaq bash onu sakitcə boş sətir
      sayar və səhv <em>çox sonra</em>, tamam başqa yerdə üzə çıxar.
      <strong>Diqqət:</strong> <code>set -e</code> (hər xətada çıx)
      qəsdən qoymuruq — çünki skriptin bəzi əmrləri «uğursuz olmalıdır»
      (məsələn portun boş olduğunu yoxlayarkən).</li>
  <li><code>cd "$(dirname "$0")/.." || exit 1</code> — bu çox incə bir
      hiylədir. <code>$0</code> skriptin öz yoludur. <code>dirname</code>
      onun qovluğunu verir (<code>.../skriptler</code>), <code>/..</code>
      isə bir səviyyə yuxarı çıxır → layihənin kökü. Beləliklə skripti
      <strong>haradan</strong> işlətsəniz də (layihə içindən, evdən, başqa
      qovluqdan) düzgün yerə keçir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2. Təmizlik funksiyası və trap</h5>
<ul>
  <li><code>PID=""</code> — əvvəlcə boş. <code>set -u</code> ilə birlikdə
      bu vacibdir: dəyişən təyin olunmasa, <code>trap</code> içində
      <code>$PID</code> oxunarkən skript çökərdi.</li>
  <li><code>kill -0 "$PID"</code> — <em>heç nə öldürmür!</em> Yalnız
      «bu PID hələ yaşayırmı?» sualına cavab verir. Belə yoxlama olmasa,
      artıq bitmiş prosesi <code>kill</code> etməyə çalışıb yalancı xəta
      mesajı alardıq.</li>
  <li><code>wait "$PID"</code> — prosesin tam bitməsini gözləyir.
      <code>kill</code> yalnız <em>siqnal göndərir</em>, proses dərhal
      ölmür. <code>wait</code> olmasa, skript bitəndə port hələ də bir neçə
      millisaniyə məşğul qala bilər.</li>
  <li><code>trap temizle EXIT INT TERM</code> — üç hal: <code>EXIT</code>
      (skript normal və ya xəta ilə bitdi), <code>INT</code> (Ctrl+C),
      <code>TERM</code> (<code>kill</code> siqnalı).</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3. İlkin yoxlamalar (fail fast)</h5>
<ul>
  <li>Əvvəlcə <code>dist/main.js</code> varmı? Yoxsa dərhal aydın mesajla
      çıxırıq: «Əvvəlcə <code>npm run build</code>». Bu prinsipin adı
      <strong>fail fast</strong>-dir: problemi <em>ilk mümkün anda</em>,
      <em>aydın mesajla</em> bildir.</li>
  <li>Sonra port boşdurmu? Məşğuldursa <code>lsof</code> çıxışını
      göstəririk ki, istifadəçi dərhal PID-i görsün.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">4. Serveri qaldırmaq</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
PORT="$PORT" node dist/main.js &gt;"$LOQ" 2&gt;&amp;1 &amp;
PID=$!</pre>
<ul>
  <li><code>PORT="$PORT" node ...</code> — yalnız <em>bu</em> əmr üçün
      mühit dəyişəni. Skriptin qalan hissəsinə təsir etmir.</li>
  <li><code>&gt;"$LOQ"</code> — standart çıxışı (stdout) loq faylına yönləndir.</li>
  <li><code>2&gt;&amp;1</code> — xəta çıxışını (stderr) da <em>eyni yerə</em>
      göndər. <code>2&gt;&amp;1</code> olmasa, xəta mesajları terminala
      düşərdi və loq yarımçıq olardı.</li>
  <li><code>&amp;</code> — arxa planda işlət.</li>
  <li><code>PID=$!</code> — <code>$!</code> «ən son arxa plana salınmış
      prosesin PID-i» deməkdir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">5. «Hazırdır?» döngəsi — polling</h5>
<p>Server dərhal qalxmır: əvvəlcə modullar yüklənir, Prisma bazaya qoşulur.
Ona görə dövrə ilə soruşuruq — maksimum 60 dəfə, aralarında 0.5 saniyə
(yəni 30 saniyə). Buna <strong>polling</strong> deyilir.</p>
<p>Döngüdə iki yoxlama var: (1) <code>curl</code> uğurludursa — hazırdır;
(2) proses hələ yaşayırmı — yoxsa <code>break</code> edirik, çünki ölmüş
prosesi 30 saniyə gözləmək mənasızdır. İkinci yoxlama olmasa, server
dərhal çöksə də skript yarım dəqiqə <em>boş yerə</em> gözləyərdi.</p>

<h5 style="color:#334155;margin-top:1rem">6. Nəticənin yoxlanması və qərar</h5>
<ul>
  <li><code>kod() { curl -s -o /dev/null -w '%{http_code}' "$1"; }</code> —
      kiçik köməkçi funksiya. Üç yeri yoxlayırıq.</li>
  <li><code>/api/v1/saglamliq</code> → <code>200</code> olmalıdır.</li>
  <li><code>/docs</code> → Swagger sənədləşdirmə səhifəsi, <code>200</code>.</li>
  <li><code>/saglamliq</code> (prefikssiz) → <code>404</code> olmalıdır.
      Bu <em>əks yoxlamadır</em> (negative test): prefiksin həqiqətən
      işlədiyini sübut edir. Əgər bu yol <code>200</code> qaytarsaydı,
      <code>setGlobalPrefix</code> işləmirdi.</li>
</ul>
<p>Skriptin <strong>çıxış kodu</strong> vacibdir: uğurlu halda
<code>0</code>, xəta halda <code>1</code>. Elə buna görə bu skripti sonra
testlərdə (ADDIM 14–16) rahat istifadə edə biləcəyik — <code>if bash
skriptler/servis_yoxla.sh; then ...</code>.</p>
""",
    "fayllar": ["skriptler/servis_yoxla.sh"],
    "goster": ["src/main.ts"],
    "c": r"""
echo "════ A) Əvvəlcə build-in təzə olduğuna əmin olaq ════"
npm run build

echo ""
echo "════ B) Serveri qaldırırıq, yoxlayırıq, söndürürük ════"
bash skriptler/servis_yoxla.sh
NETICE=$?
echo "  → skriptin exit kodu: $NETICE"

echo ""
echo "════ C) Server söndürüldükdən sonra port boşdurmu? ════"
if lsof -nP -iTCP:4000 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "  ✗ XƏTA: port hələ də məşğuldur — trap işləmədi!"
else
  echo "  ✓ port boşdur — trap təmizliyi yerinə yetirdi"
fi

echo ""
echo "════ D) Loq faylı — server nə yazdı? ════"
tail -n 8 /tmp/arti_server_4000.log

echo ""
echo "════ E) Port MƏŞĞUL olanda skript nə edir? ════"
echo "  → 4100 portunu süni şəkildə tuturuq"
python3 -m http.server 4100 --bind 127.0.0.1 >/dev/null 2>&1 &
TUTAN=$!
sleep 1.5
PORT=4100 bash skriptler/servis_yoxla.sh
echo "  → exit kodu: $? (1 gözlənilir — skript problemi TANIDI)"
kill $TUTAN 2>/dev/null
wait $TUTAN 2>/dev/null
echo "  ✓ süni tutucu dayandırıldı"
""",
    "olmaz": """Əl ilə server qaldırsaq (skript olmadan):

$ npm run start:prod
> ds-backend@0.1.0 start:prod
> node dist/main.js

[Nest] ... LOG [BAŞLANGIC] API hazırdır → http://localhost:4000/api/v1
  ← ⚠️ TERMINAL BLOKLANDI. Bu pəncərədə heç nə yaza bilməzsiniz.

Yeni terminal açıb yoxlayırıq:
$ curl http://localhost:4000/api/v1/saglamliq
{"status":"saglam", ...}
  ← İşləyir, amma...

İndi skripti yenidən işlətmək istəsək:
$ bash skriptler/servis_yoxla.sh
Error: listen EADDRINUSE: address already in use :::4000
  ← ⚠️ Köhnə serveri söndürməyi UNUTMUŞUQ.

Və əl ilə yoxlamada ƏSAS problem: biz yalnız
/api/v1/saglamliq yolunu yoxladıq. Prefiksin işlədiyini,
/docs-un açıldığını, ya da özünün təmiz söndüyünü
YOXLAMADIQ. İnsan yorulur və addımları atlayır.""",
    "c_izah": """
<p><strong>Ən başlıca fərq: yoxlama <em>təkrarlana bilən</em> olur.</strong>
Əl ilə yoxlamada hər dəfə eyni 4 addımı yadda saxlamalı və təkrarlamalısınız.
Bir dəfə unutsanız — səhv buraxılıb gedəcək. Skript isə həmişə
<em>eyni</em> yoxlayır. Buna «təkrarlana bilən yoxlama» deyilir.</p>
<p><strong>İkincisi: təmizlik zəmanətlidir.</strong> <code>trap</code>
olmadan skript xəta ilə yarıda dayansa, arxa planda işləyən server
qalardı. Növbəti cəhd <code>EADDRINUSE</code> verərdi və səbəbi
anlaşılmazdı: «dünən işləyirdi, bu gün niyə işləmir?» Cavab: dünənki
server hələ də işləyir.</p>
<p><strong>Üçüncüsü: <code>-f</code> olmadan polling səhv işləyir.</strong>
<code>curl -f</code> olmasa, <code>curl</code> 500 xətası üçün də
<code>0</code> qaytarar («sorğu göndərildi, cavab gəldi»). Yəni server
«xəta verirəm» deyə-deyə skript «hazırdır» deyərdi. <code>-f</code>
(«fail») məhz bunun qarşısını alır.</p>
<p><strong>Dördüncüsü: <code>/saglamliq</code> yoxlaması.</strong> Bu
«mənfi test» olmasa, prefiksin işlədiyinə <em>əmin</em> ola bilməzdik.
Yalnız «işləyən yolları» yoxlamaq çox vaxt kifayət etmir — <em>işləməməli
olan</em> yolları da yoxlamaq lazımdır.</p>
""",
    "sual": [
        ("Skript serveri niyə <code>npm run start:prod</code> ilə deyil, birbaşa "
         "<code>node dist/main.js</code> ilə qaldırır?",
         "Çünki <code>npm</code> əlavə bir proses (alt qat) yaradır. "
         "<code>kill</code> etsək, npm ölür, amma onun altındaki Node prosesi "
         "<em>yaşamağa davam edir</em> və port məşğul qalır. Birbaşa "
         "<code>node</code> işlətməklə <code>$!</code> məhz serverin PID-ini "
         "verir və <code>kill</code> dəqiq hədəfə dəyir."),
        ("<code>kill -0</code> nə edir? Axı <code>0</code> siqnalı yoxdur.",
         "Doğrudan da <code>0</code> real siqnal deyil — bu, Unix-in xüsusi "
         "«yoxlama» siqnalıdır. Proses mövcuddursa uğur qaytarır, mövcud "
         "deyilsə xəta. Yəni <code>kill -0 $PID</code> = «bu PID hələ "
         "yaşayırmı?». Heç nəyi öldürmür."),
        ("Niyə <code>sleep 0.5</code> — bəs 1 saniyə yaxşı deyil?",
         "Yaxşıdır, amma server adətən 1 saniyədən tez hazır olur. 0.5 saniyə "
         "seçməklə həm tez hazır olan serveri gözləmirik, həm də 60 cəhd × "
         "0.5 = 30 saniyə kifayət qədər səbirli oluruq. Bu, «gecikmə və "
         "səbir arasında tarazlıq»dır."),
        ("<code>lsof</code> macOS-da həmişə varmı?",
         "Bəli, macOS ilə birlikdə gəlir (BSD versiyası). Linux-da bəzən "
         "ayrıca qurulmalıdır (<code>apt install lsof</code>). Alternativ: "
         "<code>netstat -tulpn | grep 4000</code>."),
        ("Serveri arxa planda buraxdım və terminalı bağladım. Nə olar?",
         "Terminal bağlananda ona bağlı proseslərə <code>SIGHUP</code> "
         "siqnalı gedir və proses adətən ölür. Amma <code>nohup</code> və ya "
         "Docker/systemd ilə qaldırılmışsa, yaşamağa davam edir — o zaman "
         "<code>lsof -nP -iTCP:4000 -sTCP:LISTEN</code> ilə tapıb "
         "<code>kill</code> etmək lazımdır."),
        ("Loqu niyə <code>/tmp</code> qovluğuna yazırıq?",
         "Çünki loq <em>müvəqqəti</em> fayldır — layihənin bir hissəsi deyil, "
         "git-ə düşməməlidir. <code>/tmp</code> həm də hər port üçün ayrı ad "
         "verməyə imkan verir (<code>/tmp/arti_server_4100.log</code>), beləcə "
         "paralel yoxlamalar bir-birini pozmur."),
        ("<code>wait $PID</code> mütləqdirmi?",
         "Funksional olaraq həmişə deyil, amma <em>yaxşı təcrübədir</em>. "
         "Səbəb: <code>kill</code> yalnız siqnal göndərir. Prosesə «öl» "
         "deyirik, amma o, təmizlənmə işlərini (baza bağlantısını bağlamaq "
         "kimi) görəndən sonra ölür. <code>wait</code> bu müddətdə gözləyir. "
         "Olmazsa, dərhal ardınca portu yoxlasaq — hələ məşğul görünə bilər."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>Server <strong>canlı</strong> yoxlanıldı: <code>/api/v1/saglamliq</code>
      → <code>200</code>, cavabda <code>"status":"saglam"</code> və
      <code>"cedvel_sayi":48</code>.</li>
  <li><code>/docs</code> → <code>200</code>: Swagger sənədləşdirməsi
      işləyir.</li>
  <li><code>/saglamliq</code> (prefiks olmadan) → <code>404</code>. Bu
      <strong>müsbət nəticədir</strong> — <code>setGlobalPrefix('api/v1')</code>
      həqiqətən işlədiyini sübut edir.</li>
  <li>Skript bitdikdən sonra port <strong>boşdur</strong>: <code>trap</code>
      öz işini gördü. Əl ilə qaldırsaydıq, bu serveri söndürməyi unuda
      bilərdik.</li>
  <li>Port məşğul olanda skript <strong>aydın Azərbaycanca mesaj</strong>
      verdi, tutan prosesin PID-ini göstərdi və <code>exit 1</code> ilə
      dayandı — serveri qaldırmağa <em>cəhd belə etmədi</em>.</li>
</ul>
<p><strong>Mühüm fikir:</strong> yoxlama <em>avtomatik</em> və
<em>təkrarlana bilən</em> olmalıdır. Bu skripti hər dəyişiklikdən sonra
işlədə bilərsiniz — 3 saniyə çəkir və 4 şeyi yoxlayır. Növbəti iki addımda
bu ideyanı <strong>testlərə</strong> çevirəcəyik: insan gözü ilə oxumaq
əvəzinə, kompüter <em>özü</em> qərar verəcək ki, hər şey qaydasındadır,
ya yox.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 14 — VİTEST QURULMASI
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 14,
    "ad": "Test nədir və Vitest-in qurulması",
    "a": """
<p>İndiyə qədər kodu <em>əl ilə</em> yoxladıq: serveri qaldırdıq,
<code>curl</code> ilə baxdıq, gözümüzlə oxuduq. Bu yaxşıdır, amma
<strong>kifayət deyil</strong>. Bu addımdan başlayaraq kompüter
<em>özü</em> qərar verəcək ki, hər şey qaydasındadır, ya yox.</p>

<h4>Test nədir?</h4>
<p><strong>Test — kodun gözlənilən davranışını yoxlayan koddur.</strong>
Başqa sözlə: bir dəfə yazırsan, hər dəfə işlədirsən. Test üç suala cavab
verir:</p>
<ol>
  <li>Nə edirik? (hazırlıq — <em>Arrange</em>)</li>
  <li>Nə baş verir? (hərəkət — <em>Act</em>)</li>
  <li>Nə gözləyirik? (yoxlama — <em>Assert</em>)</li>
</ol>
<p>Bu üç hərfin adı <strong>AAA naxışı</strong>dır. Hər yaxşı test bu
quruluşdadır.</p>

<h4>Test növləri — piramida</h4>
<table style="width:100%;border-collapse:collapse;font-size:.93rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Növ</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Nəyi yoxlayır</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Sürəti</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Nə qədər</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Vahid (unit)</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Tək funksiya və ya sinif.
        Baza, şəbəkə — heç nə lazım deyil.</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">millisaniyə</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Çox olmalıdır</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>İnteqrasiya</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Bir neçə hissənin birlikdə
        işləməsi (məsələn servis + baza).</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">saniyə</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Bir neçə</td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>e2e (end-to-end)</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Bütöv sistem: real HTTP
        sorğusu, real baza, real cavab.</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">saniyə</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Az, amma dəyərli</td>
  </tr>
</table>
<p>Piramidanın altı geniş, üstü dar olmalıdır: <em>çox unit, az e2e</em>.
Səbəb: unit testlər sürətli və sabitdir; e2e testlər həqiqi mühitə
bağlıdır — baza xəstələnəndə onlar da «xəstələnir».</p>

<h4>Test nə üçün lazımdır? Dörd real səbəb</h4>
<ol>
  <li><strong>Reqressiya qorunması.</strong> Köhnə işləyən bir şeyi
      sındırdığınızı dərhal öyrənirsiniz. Test olmasa — istifadəçi
      deyəndə öyrənirsiniz.</li>
  <li><strong>Canlı sənədləşdirmə.</strong> Test kodu oxuyan şəxs görür ki,
      <code>yoxla()</code> nə qaytarmalıdır. Şərhlər köhnəlir, testlər
      <em>işlədiyi müddətcə</em> doğrudur.</li>
  <li><strong>Refaktor cəsarəti.</strong> Kodu təmizləməyə qorxmadan
      başlayırsınız: testlər «heç nə sınmadı» deyəcək.</li>
  <li><strong>Dizayn yaxşılaşır.</strong> Test yazmaq çətin olan kod
      adətən <em>pis yazılmış</em> koddur. Test yazmaq sizi daha yaxşı
      dizayn etməyə məcbur edir.</li>
</ol>

<h4>Niyə Vitest, bəs Jest?</h4>
<p><strong>Jest</strong> uzun illər standart idi. Amma layihəmiz
<code>"type": "module"</code> (ESM) işlədir və TypeScript yazır. Jest-i bu
kombinasiya üçün qurmaq üçün əlavə alətlər (<code>ts-jest</code>,
<code>babel</code>, <code>transform</code> konfiqurasiyaları) lazımdır.
<strong>Vitest</strong> isə TypeScript və ESM-i <em>birbaşa</em> başa
düşür — çünki Vite-in üzərində qurulub və eyni mexanizmdən istifadə edir.
API-si Jest ilə demək olar eynidir (<code>describe</code>,
<code>it</code>, <code>expect</code>), ona görə öyrənmək asandır.</p>

<h4>Niyə İKİ konfiqurasiya faylı?</h4>
<p>Bu, dərsin ən vacib dizayn qərarıdır. Səbəblər:</p>
<ul>
  <li><strong>Fərqli sürət tələbi.</strong> Unit testlər 200 millisaniyədə
      bitir, e2e testlər 3 saniyə çəkə bilər. Onları qarışdırsaq, hər
      dəfə hamısını gözləmək lazım gələr.</li>
  <li><strong>Fərqli mühit tələbi.</strong> Unit testlər bazasız işləyir.
      E2e testlər <em>baza olmadan işləyə bilməz</em>. Onları ayırsaq,
      yeni işə başlayan həmkar bazanı qurmadan <code>npm test</code>
      işlədə bilər.</li>
  <li><strong>Paralellik.</strong> Vitest unit testləri
      <em>paralel</em> işlədir (sürətli). E2e testlər isə
      <code>fileParallelism: false</code> ilə <em>ardıcıl</em> —
      çünki hamısı eyni bazaya yazır və bir-birini poza bilər.</li>
</ul>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
npm test           →  vitest run                          (unit)
npm run test:unit  →  vitest run                          (unit)
npm run test:e2e   →  vitest run --config vitest.config.e2e.ts
npm run test:izle  →  vitest                              (nəzarət rejimi)</pre>

<div class="olmaz" style="margin-top:1rem">
<h4>⚠️ Bu ayrı-seçkilik olmasa nə olar?</h4>
<p>Bütün testlər bir dəstdə olsa: <code>npm test</code> hər dəfə
<strong>real bazanı tələb edərdi</strong>. Baza söndürülübsə, yaxud
başqa maşında işləyirsinizsə — sadəcə kodun qrammatikasını yoxlamaq
üçün belə testlər uğursuz olardı. Nəticə: komanda «testlər onsuz da
keçmir» deyib onlara baxmağı dayandırar. <strong>Etibarını itirən test
dəsti, test dəsti olmayandan pisdir.</strong></p>
</div>
""",
    "anlayis": [
        ("Test",
         "Kodun gözlənilən davranışını avtomatik yoxlayan kod. Bir dəfə "
         "yazılır, min dəfə işlədilir."),
        ("Unit test",
         "Tək bir funksiya/sinif üçün test. Xarici asılılıqlar (baza, "
         "şəbəkə) saxta obyektlərlə əvəz olunur."),
        ("e2e test",
         "«End-to-end» — başdan-başa. Real HTTP sorğusu göndərilir, real "
         "baza oxunur. Sistemi istifadəçinin gördüyü kimi yoxlayır."),
        ("Mock / Saxta obyekt",
         "Real asılılığın yerinə qoyulan yalançı nüsxə. «Baza varmış kimi "
         "davran» deyirik. Testi sürətli və təcrid olunmuş edir."),
        ("AAA naxışı",
         "Arrange (hazırla) → Act (hərəkət et) → Assert (yoxla). Hər "
         "yaxşı testin quruluşu."),
        ("Vitest",
         "Vite üzərində qurulmuş test aləti. TypeScript və ESM-i birbaşa "
         "başa düşür, Jest API-si ilə uyğundur."),
        ("globals: true",
         "Vitest konfiqurasiyasında <code>describe</code>, <code>it</code>, "
         "<code>expect</code> funksiyalarını qlobal edir — hər faylda "
         "import etmək lazım gəlmir."),
        ("include / exclude",
         "«Hansı fayllar test sayılsın» / «hansılar sayılmasın». Glob "
         "naxışları ilə yazılır (<code>src/**/*.spec.ts</code>)."),
        ("fileParallelism",
         "<code>false</code> olanda test faylları paralel deyil, ardıcıl "
         "işlədilir. Eyni bazaya yazan testlər üçün mütləqdir."),
        ("testTimeout",
         "Bir testin maksimum icra müddəti (millisaniyə). E2e üçün "
         "<code>30_000</code> = 30 saniyə."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) package.json — yeni skriptlər</h5>
<p><code>scripts</code> bölməsinə dörd sətir əlavə olundu. <code>scripts</code>
nədir? Bu, «qısa ad ↔ uzun əmr» cədvəlidir. <code>npm run test:e2e</code>
yazanda npm əslində <code>vitest run --config vitest.config.e2e.ts</code>
işlədir. Faydası: komandada hər kəs <em>eyni</em> əmri işlədir, uzun
əmri yadda saxlamaq lazım gəlmir.</p>
<p><strong>Diqqət:</strong> <code>node_modules/.bin</code> qovluğu
<code>PATH</code>-a avtomatik əlavə olunur. Ona görə <code>npx vitest</code>
yazmaq lazım deyil — npm skripti içərisində sadəcə <code>vitest</code>
kifayətdir.</p>

<h5 style="color:#334155;margin-top:1rem">2) vitest.config.ts — vahid testlər</h5>
<ul>
  <li><code>import { defineConfig } from 'vitest/config'</code> —
      <code>defineConfig</code> yalnız tip yoxlaması üçün köməkçidir:
      yazdığınız açar sözləri redaktor yoxlaya bilir və səhv yazsanız
      dərhal xəbərdarlıq alırsınız.</li>
  <li><code>export default defineConfig({...})</code> — konfiqurasiya
      obyekti. Vitest işə düşəndə bu faylı oxuyur.</li>
  <li><code>globals: true</code> — <code>describe</code>, <code>it</code>,
      <code>expect</code>, <code>vi</code> funksiyalarını qlobal edir.
      <strong>Yan təsir:</strong> TypeScript bunları tanısın deyə
      <code>tsconfig.json</code>-da <code>"types": ["vitest/globals"]</code>
      olmalıdır — 1A-nın ADDIM 3-də bunu artıq yazmışdıq.</li>
  <li><code>environment: 'node'</code> — test mühiti. Varsayılan
      <code>'node'</code>-dur, amma açıq yazmaq niyəti göstərir:
      <em>biz brauzer yox, Node yoxlayırıq</em>. (Frontend-də
      <code>'jsdom'</code> olur.)</li>
  <li><code>include: ['src/**/*.spec.ts']</code> — yalnız
      <code>src/</code> qovluğundaki <code>*.spec.ts</code> faylları test
      sayılır. <strong>Bu, ayrı-seçkiliyin əsas mexanizmidir.</strong>
      Qeyd: <code>saglamliq.e2e-spec.ts</code> faylı bu naxışa
      <em>düşmür</em>, çünki adı <code>.spec.ts</code> ilə deyil,
      <code>-spec.ts</code> ilə bitir.</li>
  <li><code>exclude: ['**/node_modules/**', '**/dist/**', '**/*.e2e-spec.ts']</code>
      — <em>qoruyucu kəmər</em> (defense in depth). Hazırda birinci iki
      naxış Vitest-in artıq varsayılan etdiyi istisnalardır, üçüncüsü isə
      <code>include</code> səbəbindən heç bir əlavə iş görmür. Amma
      <code>include</code> gələcəkdə genişləndirilsə (məsələn
      <code>'**/*.spec.ts'</code> edilsə), bu sətir e2e testlərinin vahid
      dəstinə sızmasının qarşısını alır. <strong>Bunu qəsdən saxlayırıq:
      konfiqurasiya gələcək səhvlərə qarşı da dayanıqlı olmalıdır.</strong>
      C hissəsində bunu real nümunə ilə göstərəcəyik.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3) vitest.config.e2e.ts — e2e testlər</h5>
<ul>
  <li><code>include: ['test/**/*.e2e-spec.ts']</code> — yalnız
      <code>test/</code> qovluğu. Test fayllarının <code>src/</code>
      xaricində saxlanması beynəlxalq konvensiyadır: mənbə kod və test
      kod qarışmır, həm də <code>tsconfig.build.json</code> onları
      avtomatik xaric edir.</li>
  <li><code>fileParallelism: false</code> — fayllar paralel yox, növbə ilə
      işlədilir. Səbəb: hər e2e testi eyni <code>arti_baza</code> bazasına
      qoşulur. Paralel işləsəydilər, birinin yazdığını digəri oxuyub
      gözlənilməz nəticə verə bilər.</li>
  <li><code>testTimeout: 30_000</code> — hər test üçün 30 saniyə. Varsayılan
      5 saniyədir, amma ilk dəfə bazaya qoşulma (Prisma-nın özünü
      hazırlaması) 5 saniyədən çox çəkə bilər. <code>30_000</code>-daki
      <code>_</code> işarəsi sadəcə oxunaqlılıq üçündür — JavaScript
      rəqəmlərdə alt xətti nəzərə almır.</li>
  <li><code>hookTimeout: 30_000</code> — <code>beforeAll</code> /
      <code>afterAll</code> kimi «qarmaqlar» üçün də eyni müddət.
      Xüsusilə vacibdir: <code>beforeAll</code> içində bütün Nest
      tətbiqini qururuq.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">4) Niyə konfiqurasiya faylının adı <code>vitest.config.ts</code>-dir?</h5>
<p>Vitest işə düşəndə <em>öncəlik sırası ilə</em> bu adları axtarır:
<code>vitest.config.ts</code>, <code>vitest.config.js</code>,
<code>vite.config.ts</code> və s. Beləliklə heç bir parametr yazmadan
sadəcə <code>npx vitest</code> işlətmək kifayətdir. İkinci fayl
<code>vitest.config.e2e.ts</code> adlandığı üçün <em>avtomatik
tapılmır</em> — ona görə <code>--config</code> ilə açıq göstərilir.</p>
""",
    "fayllar": ["package.json", "vitest.config.ts", "vitest.config.e2e.ts"],
    "goster": [],
    "c": r"""
echo "════ 1) Vitest qurulubmu? ════"
npx vitest --version

echo ""
echo "════ 2) package.json-da hansı skriptlər var? ════"
npm pkg get scripts

echo ""
echo "════ 3) Vahid konfiqurasiyası YÜKLƏNİRMİ? ════"
echo "  Qeyd: hələ test faylı yazmamışıq, ona görə filtr veririk ki,"
echo "  heç nə işləməsin. Vacib olan — vitest konfiqurasiyanı OXUDU və"
echo "  öz include/exclude sətirlərini göstərdi."
echo ""
npx vitest run --config vitest.config.ts --passWithNoTests hele-yoxdur

echo ""
echo "════ 4) E2E konfiqurasiyası YÜKLƏNİRMİ? ════"
npx vitest run --config vitest.config.e2e.ts --passWithNoTests hele-yoxdur

echo ""
echo "════ 5) Vahid konfiqurasiyası HANSI faylları görür? ════"
npx vitest list --config vitest.config.ts

echo ""
echo "════ 6) E2E konfiqurasiyası HANSI faylları görür? ════"
npx vitest list --config vitest.config.e2e.ts

echo ""
echo "════ 7) NƏ ÜÇÜN ayrı-seçkilik vacibdir? (canlı sübut) ════"
echo "  → müvəqqəti konfiqurasiya yaradırıq ki, hər iki növü bir yerə yığsın:"
cat > vitest.saltsiz.config.ts <<'SON'
import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: { globals: true, environment: 'node',
          include: ['**/*.spec.ts', '**/*.e2e-spec.ts'] },
});
SON
npx vitest list --config vitest.saltsiz.config.ts
echo ""
echo "  ↑ GÖRDÜYÜNÜZ KİMİ: qarışdıranda 3 vahid testin YANINA 4 e2e test də"
echo "    düşür. Yəni 'npm test' hər dəfə real baza tələb edərdi."
rm -f vitest.saltsiz.config.ts
echo "  ✓ müvəqqəti konfiqurasiya silindi"

echo ""
echo "════ 8) Təmizlik yoxlaması ════"
printf '  vitest.saltsiz.config.ts → %s\n' "$([ -f vitest.saltsiz.config.ts ] && echo 'HƏLƏ DURUR' || echo 'yoxdur (yaxşıdır)')"
printf '  vitest.config.ts         → %s\n' "$([ -f vitest.config.ts ] && echo 'VAR' || echo 'YOXDUR')"
printf '  vitest.config.e2e.ts     → %s\n' "$([ -f vitest.config.e2e.ts ] && echo 'VAR' || echo 'YOXDUR')"
""",
    "olmaz": """Konfiqurasiya faylları olmasa nə olar?

$ npm test

 RUN  v4.1.11


 No test files found, exiting with code 1
  ← ⚠️ Vitest heç bir test tapmır, çünki hansı fayllara
     baxacağını bilmir. Varsayılan naxış .spec.ts/.test.ts-dir,
     amma layihəmizdə `src/` və `test/` ayrılığı var və
     e2e fayllarının `--config` ilə açıq göstərilməsi lazımdır.

────────────────────────────────────────────────────────────
VƏ YA hər şey bir konfiqurasiyada olsa:

$ npm test
 ✓ src/saglamliq/saglamliq.service.spec.ts (3 tests)
 ❯ test/saglamliq.e2e-spec.ts (4 tests | 1 failed)
   × GET /api/v1/saglamliq → 200, baza qoşulub, 48 cədvəl

 Test Files  1 failed | 1 passed (2)
  ← ⚠️ Baza söndürülmüş maşında SADƏCƏ KODU yoxlamaq
     istəyirdik, amma e2e testlər də işlədi və uğursuz oldu.
     Nəticə: komanda testlərə baxmağı dayandırır.""",
    "c_izah": """
<p><strong>Ən başlıca səbəb: testlərin etibarlılığı.</strong> Əgər
<code>npm test</code> hər dəfə real baza tələb etsəydi, yeni işə başlayan
həmkar bazanı qurmadan kodu yoxlaya bilməzdi. Baza bir gün söndürülsə,
bütün testlər «uğursuz» olardı — halbuki kod <em>tamam</em> düzgündür.
Buna <strong>yalançı mənfi</strong> (false negative) deyilir və o, test
mədəniyyətini öldürür.</p>
<p><strong>İkincisi: sürət.</strong> Vahid testlər 3 testi 200 millisaniyədə
bitirir. E2e testlər 4 testi təxminən yarım saniyəyə. Bu kiçik fərq
görünür, amma 500 testli real layihədə vahid dəst 2 saniyə, qarışıq dəst
2 dəqiqə çəkə bilər. Siz isə kodu <em>hər</em> yadda saxlayanda işlədirsiniz.
2 dəqiqə olsa, işlətməyəcəksiniz.</p>
<p><strong>Üçüncüsü: paralellik.</strong> Vahid testlər təcrid olunduğu
üçün paralel işlədilə bilər (Vitest hər prosessor nüvəsindən istifadə edir).
E2e testləri paralel işlətmək isə <em>təhlükəlidir</em>: ikisi eyni
cədvələ yazsa, nəticə təsadüfi olur. <code>fileParallelism: false</code>
məhz buna görə var.</p>
<p><strong>Dördüncüsü: <code>--passWithNoTests</code>.</strong> Bu
parametr olmasa, «heç test tapılmadı» <em>xəta</em> sayılır və exit kodu
1 olur. Bizim addımda isə test faylları hələ yazılmayıb — biz yalnız
konfiqurasiyanın <em>düzgün oxunduğunu</em> yoxlayırıq. Nəticədə çıxışda
<code>include:</code> və <code>exclude:</code> sətirlərini görürük — bu,
konfiqurasiyanın həqiqətən yükləndiyinin sübutudur.</p>
""",
    "sual": [
        ("Test yazmaq vaxt itkisi deyilmi? Kodu iki dəfə yazıram axı.",
         "Qısa müddətdə bəli, uzun müddətdə xeyir. Təcrübə göstərir ki, "
         "səhvlərin ən bahalısı <em>istehsalatda</em> tapılan səhvdir. Bir "
         "dəfə test yazmaq üçün 20 dəqiqə sərf etsəniz, həmin səhvi 2 ay "
         "sonra, müştəri şikayət edəndə tapmaq üçün 3 saat sərf etməkdən "
         "yaxşıdır. Üstəlik test bir dəfə yazılır, min dəfə işlədir."),
        ("Nə qədər test yazmalıyam? 100% əhatə (coverage) lazımdırmı?",
         "Xeyr. 100% əhatə <em>məqsəd deyil</em>. Əsas biznes məntiqini, "
         "xəta hallarını və sərhəd vəziyyətlərini yoxlayın. Sadə "
         "<code>getter</code>/<code>setter</code> funksiyaları üçün test "
         "yazmaq vaxt itkisidir. Praktikada 70–85% əhatə çox yaxşı "
         "göstəricidir."),
        ("<code>describe</code> ilə <code>it</code> arasında nə fərq var?",
         "<code>describe</code> — <em>qrup</em>dur («bu fayl SaglamliqService "
         "servisini yoxlayır»). <code>it</code> — <em>tək testdir</em> "
         "(«baza cavab verəndə status saglam olur»). <code>describe</code> "
         "içində bir neçə <code>it</code> ola bilər; hətta iç-içə "
         "<code>describe</code> da mümkündür."),
        ("Niyə <code>it</code>? Adı qəribədir.",
         "İngilis dilində testləri oxuya-oxyuya demək üçün: "
         "<em>«it should return saglam when database responds»</em> — "
         "«o, baza cavab verəndə saglam qaytarmalıdır». Yəni "
         "<code>it('baza cavab verəndə status saglam olur')</code> cümlə "
         "kimi oxunur. <code>test</code> funksiyası da eynidir — Vitest "
         "hər ikisini dəstəkləyir."),
        ("<code>npm test</code> ilə <code>npx vitest</code> arasında fərq?",
         "<code>npx vitest</code> <em>nəzarət (watch) rejimində</em> işləyir: "
         "fayl dəyişəndə testləri avtomatik yenidən işlədir və siz "
         "<code>q</code> basana qədər davam edir. <code>npm test</code> isə "
         "<code>vitest run</code>-dır — bir dəfə işləyib bitir. CI "
         "(avtomatik yoxlama) üçün <code>run</code> lazımdır, inkişaf "
         "zamanı isə nəzarət rejimi daha rahatdır."),
        ("Konfiqurasiya faylını <code>.js</code> kimi yaza bilərəmmi?",
         "Bilərsiniz — Vitest həm <code>.ts</code>, həm <code>.js</code>, "
         "həm <code>.mts</code> qəbul edir. <code>.ts</code> seçməyin "
         "üstünlüyü: <code>defineConfig</code> tipi yoxlanılır və səhv "
         "açar söz yazsanız redaktor dərhal xəbərdarlıq edir. "
         "Məsələn <code>testTimeot</code> (səhv yazılış) dərhal qırmızı "
         "görünəcək."),
        ("<code>exclude</code> sətrindəki <code>**/*.e2e-spec.ts</code> lazımsız deyilmi?",
         "Hazırda <em>əlavə iş görmür</em> — <code>include</code> onsuz da "
         "yalnız <code>src/**/*.spec.ts</code>-ə baxır və e2e faylının adı "
         "bu naxışa düşmür. Amma onu saxlamaq <strong>müdafiə qatı</strong> "
         "(defense in depth) prinsipidir: gələcəkdə kimsə "
         "<code>include</code>-u genişləndirsə, e2e testlər avtomatik "
         "qorunmuş olacaq. Konfiqurasiya yalnız <em>bugünkü</em> vəziyyətə "
         "deyil, sabahkı dəyişikliyə də dayanıqlı olmalıdır."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>Vitest qurulub və versiyası <code>4.1.11</code>-dir.</li>
  <li><code>package.json</code>-da dörd test skripti var:
      <code>test</code>, <code>test:unit</code>, <code>test:izle</code>,
      <code>test:e2e</code>.</li>
  <li>Hər iki konfiqurasiya <strong>uğurla yüklənir</strong> — çıxışda
      hər birinin öz <code>include</code> və <code>exclude</code> sətirləri
      görünür. Bu, «vitest faylı oxudu» sualına qəti cavabdır.</li>
  <li><code>vitest list</code> ilə <em>sübut etdik</em> ki, vahid
      konfiqurasiyası yalnız 3 vahid testi görür, e2e konfiqurasiyası isə
      yalnız 4 e2e testi.</li>
  <li>Müvəqqəti olaraq hər ikisini bir konfiqurasiyaya yığdıqda
      <strong>7 test birlikdə</strong> göründü — ayrı-seçkiliyin nə üçün
      lazım olduğunu öz gözümüzlə gördük.</li>
</ul>
<p><strong>Diqqət yetirin:</strong> bu addımda <em>hələ bir dənə də test
yazmamışıq</em>. Biz yalnız <strong>altyapı</strong> qurduq: alət,
konfiqurasiya, əmrlər. Bu, tikinti bənzətməsi ilə desək — <em>iskelet
qurduq, divarları hələ çəkməmişik</em>. Növbəti iki addımda divarları
çəkəcəyik: əvvəl vahid, sonra e2e testlər.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 15 — VAHİD (UNIT) TEST
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 15,
    "ad": "Vahid (unit) test yazırıq — bazasız yoxlama",
    "a": """
<p>Altyapı hazırdır. İndi <strong>ilk həqiqi testimizi</strong> yazırıq.
Hədəf: <code>SaglamliqService.yoxla()</code> metodu. Bu metod 1A-nın ADDIM
9-da yazılmışdı və o, <code>PrismaService.yoxla()</code> çağırır, sonra
cavabı formatlayır.</p>

<h4>Vahid testin əsas ideyası — TƏCRİDLƏMƏ</h4>
<p>Vahid test «bütün sistemi» yoxlamır. O, <em>tək bir vahidi</em> —
bir sinfi və ya funksiyanı — yoxlayır. Amma <code>SaglamliqService</code>
təkbaşına işləyə bilmir: ona <code>PrismaService</code> lazımdır. Real
<code>PrismaService</code> isə bazaya qoşulur.</p>
<p>Əgər real bazadan istifadə etsəydik üç problem yaranardı:</p>
<ol>
  <li><strong>Asılılıq.</strong> Baza olmayan maşında test işləməz.</li>
  <li><strong>Sürət.</strong> Hər testdən əvvəl şəbəkə gediş-gəlişi
      lazım gələr.</li>
  <li><strong>Nəzarət.</strong> Bazada 48 cədvəl varsa test keçər, 47 olsa
      uğursuz olar. Biz isə servisin <em>məntiqini</em> yoxlayırıq, baza
      sayını yox.</li>
</ol>
<p>Həll: real asılılığı <strong>saxta obyektlə</strong> (mock) əvəz edirik.
Bunu belə edirik:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
{ provide: PrismaService, useValue: prisma }</pre>
<p>Oxunuşu: «Nest, <code>PrismaService</code> istəyən hər kəsə mənim
<code>prisma</code> obyektimi ver». Nest-in <strong>DI (dependency
injection)</strong> sistemi bunu dəstəkləyir — testdə «saxta təchizatçı»
qeydiyyatdan keçiririk.</p>

<h4>Nest-in test qabı — <code>Test.createTestingModule</code></h4>
<p>Bu, «kiçik bir Nest tətbiqi» yaradır — yalnız test üçün. Real
<code>AppModule</code>-u yükləmirik, sadəcə yoxlamaq istədiyimiz servisi
və onun asılılığını qeydiyyatdan keçiririk. Nəticədə test
<strong>millisaniyələrlə</strong> işləyir.</p>

<h4><code>vi.fn()</code> — saxta funksiya</h4>
<p><code>vi.fn()</code> xüsusi funksiya yaradır: heç nə etmir, amma
<em>çağırışları yadda saxlayır</em>. Ona «nə vaxt çağırılsa, bunu qaytar»
demək olar:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
prisma.yoxla.mockResolvedValue({ cedvelSayi: 48, gecikmeMs: 3 });</pre>
<p><code>mockResolvedValue</code> — «Promise uğurla bu dəyərlə bitsin».
<code>mockRejectedValue</code> — «Promise bu xəta ilə rədd edilsin».
İkincisi xəta halını yoxlamaq üçündür.</p>

<h4>Nə üçün <code>beforeEach</code>?</h4>
<p>Hər testdən <em>əvvəl</em> işləyir və təmiz vəziyyət yaradır. Vacibdir,
çünki: əgər birinci test <code>prisma.yoxla</code> funksiyasına
<code>mockResolvedValue</code> qoysa və ikinci test də eyni funksiyadan
istifadə etsə, ikinci test <em>birincinin</em> sazlamaşından asılı olar.
Buna <strong>test asılılığı</strong> deyilir və ən pis problemdir: testlər
tək-tək keçər, birlikdə uğursuz olar.</p>

<h4>Üç testimiz — üç fərqli yanaşma</h4>
<table style="width:100%;border-collapse:collapse;font-size:.92rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Test</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Nəyi yoxlayır</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0">1. «baza cavab verəndə status saglam olur»</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Xoşbəxt yol</strong> (happy path):
        hər şey qaydasında olanda nə qaytarılır</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0">2. «cavabda ISO formatlı vaxt olur»</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Format yoxlaması</strong>:
        <code>vaxt</code> sahəsi həqiqətən ISO 8601-dir</td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0">3. «baza xəta verəndə xəta YUXARI ötürülür»</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Xəta yolu</strong>:
        xəta udulmur, çağırana ötürülür</td>
  </tr>
</table>
<p><strong>Diqqət:</strong> yeni başlayanlar adətən yalnız birinci növü
yazırlar. Amma səhvlər <em>ikinci</em> və <em>üçüncü</em> yolda olur.
Üçüncü test xüsusilə vacibdir: əgər <code>yoxla()</code> xətanı «udub»
boş cavab qaytarsaydı, sağlamlıq endpointi <code>200</code> verərdi və
baza əslində ölü olsa da sistem «sağlam» görünərdi. Testlər məhz bu
sükutlu səhvi tutur.</p>

<h4>ISO 8601 nədir?</h4>
<p><code>2026-09-23T15:45:57.490Z</code> — beynəlxalq tarix formatı.
<code>T</code> tarixlə vaxtı ayırır, <code>Z</code> isə «UTC (Greenwich)
vaxtı» deməkdir. Niyə bu format? Çünki o, <em>mətn kimi</em>
<strong>əlifba sırası ilə düzülə bilir</strong>: <code>"2026-01"</code>
<code>"2026-09"</code>-dan kiçikdir. Həm də bütün dünyada eyni oxunur —
Amerika formatı (<code>09/23/2026</code>) ilə Avropa formatı
(<code>23/09/2026</code>) qarışıqlığı yoxdur.</p>
<p>Testdə bunu necə yoxlayırıq?</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
expect(new Date(c.vaxt).toISOString()).toBe(c.vaxt);</pre>
<p>Hiylə budur: mətni <code>Date</code> obyektinə çeviririk, sonra
yenidən ISO mətninə çeviririk. Əgər nəticə <em>eyni</em> mətndirsə,
deməli ilkin mətn düzgün ISO formatındadır. Əgər <code>vaxt</code>
<code>"23.09.2026"</code> kimi yazılsaydı, <code>new Date()</code> onu
başqa cür oxuyardı və müqayisə uğursuz olardı.</p>
""",
    "anlayis": [
        ("Test təcridi (isolation)",
         "Testin digər testlərdən və xarici sistemlərdən asılı olmaması. "
         "Hər test təkbaşına, istənilən sırada işləyə bilməlidir."),
        ("Mock / stub / spy",
         "Saxta obyekt növləri. <em>Stub</em> — sabit cavab verir. "
         "<em>Spy</em> — çağırışları yazır. <em>Mock</em> — hər ikisini "
         "edir. <code>vi.fn()</code> əslində hər üçünü edə bilir."),
        ("DI (Dependency Injection)",
         "«Asılılıq yeritmə». Sinif özü asılılığını yaratmır — kənardan "
         "alır. Ona görə testdə onu saxtası ilə əvəz etmək mümkündür."),
        ("beforeEach / afterEach",
         "Hər testdən əvvəl / sonra işləyən funksiyalar. Təmiz vəziyyət "
         "yaratmaq və resursları azad etmək üçün."),
        ("beforeAll / afterAll",
         "Bütün testlərdən əvvəl / sonra BİR DƏFƏ işləyir. Bahalı "
         "hazırlıq (baza bağlantısı, tətbiqin qurulması) üçün."),
        ("toBe / toEqual",
         "<code>toBe</code> — eynilik (<code>Object.is</code>), primitiv "
         "dəyərlər üçün. <code>toEqual</code> — dərin müqayisə, obyekt və "
         "massivlər üçün."),
        ("rejects.toThrow()",
         "«Bu Promise rədd edilməli və bu mesajla xəta verməlidir». Xəta "
         "yolunu yoxlamağın ən qısa üsulu."),
        ("ISO 8601",
         "<code>2026-09-23T15:45:57.490Z</code> — beynəlxalq tarix-vaxt "
         "formatı. Əlifba sırası ilə düzülə bilir, dünyada eyni oxunur."),
        ("Assertion (iddia)",
         "<code>expect(...)...</code> sətri. Testin «qərar verdiyi» yerdir. "
         "İddia yalan çıxsa — test uğursuz olur."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">Sətir-sətir</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
import { Test } from '@nestjs/testing';
import { SaglamliqService } from './saglamliq.service.js';
import { PrismaService } from '../prisma/prisma.service.js';</pre>
<ul>
  <li><code>Test</code> — Nest-in test köməkçisi. <code>createTestingModule</code>
      metodu onun içindədir.</li>
  <li>İki import da <code>.js</code> ilə bitir — bu, 1A-nın ADDIM 3-də
      öyrəndiyimiz qaydadır: fayl <code>.ts</code>-dir, amma ESM
      importunda <code>.js</code> yazılır. <strong>Unutsanız,
      «Cannot find module» xətası alacaqsınız.</strong></li>
</ul>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
describe('SaglamliqService (unit)', () => {</pre>
<p><code>describe</code> test qrupunu açır. Adı aydın yazırıq — çıxışda
bu ad görünəcək və hansı testin uğursuz olduğunu dərhal anlayacağıq.</p>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
  let servis: SaglamliqService;
  let prisma: { yoxla: ReturnType&lt;typeof vi.fn&gt; };</pre>
<ul>
  <li><code>let</code> (const yox) — çünki <code>beforeEach</code> içində
      yenidən təyin olunacaq.</li>
  <li><code>prisma</code>-nın tipi <em>əl ilə</em> yazılıb: «içində
      <code>yoxla</code> adlı funksiya olan obyekt». Real
      <code>PrismaService</code> tipini istifadə etmirik, çünki
      saxta obyektin bütün metodları yoxdur.</li>
  <li><code>ReturnType&lt;typeof vi.fn&gt;</code> —
      «<code>vi.fn()</code> nə qaytarırsa, o tip». Belə yazmaqla Vitest
      versiyası dəyişəndə tip avtomatik uyğunlaşır.</li>
</ul>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
  beforeEach(async () =&gt; {
    prisma = { yoxla: vi.fn() };</pre>
<p>Hər testdən əvvəl <em>yeni</em> saxta obyekt yaradılır. Bu bir sətir
test təcridini təmin edir. Onu silmək ən çox edilən səhvdir — və nəticəsi
çox məkrlidir: testlər <em>tək-tək keçər, birlikdə uğursuz olar</em>.</p>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
    const modul = await Test.createTestingModule({
      providers: [
        SaglamliqService,
        { provide: PrismaService, useValue: prisma },
      ],
    }).compile();</pre>
<ul>
  <li><code>providers</code> massivi — «bu modulda hansı siniflər var».
      <code>SaglamliqService</code> <em>sinfin özü</em> kimi verilir: Nest
      onu özü yaradacaq.</li>
  <li><code>{ provide: PrismaService, useValue: prisma }</code> —
      <strong>dərsin ən vacib sətri.</strong> <code>provide</code> —
      «nəyin yerinə», <code>useValue</code> — «nə verilsin». Beləliklə
      Nest <code>PrismaService</code>-i <em>heç vaxt yaratmır</em>,
      deməli bazaya heç vaxt qoşulmur.</li>
  <li><code>.compile()</code> — modulu «yığır»: asılılıq qrafını həll edir.
      <code>await</code> lazımdır, çünki bu asinxron əməliyyatdır (Nest
      lazım gələrsə faylları oxuyur).</li>
</ul>
<p><strong>Nə üçün <code>SaglamliqModule</code>-u import etmirik?</strong>
Çünki o modul <code>PrismaModule</code>-u da gətirərdi və o da real
<code>PrismaService</code> yaradardı. Testdə modul yerinə
<em>birbaşa təchizatçıları</em> veririk — daha nəzarətli və sürətli.</p>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
    servis = modul.get(SaglamliqService);
  });</pre>
<p><code>modul.get(...)</code> Nest-dən hazır nüsxəni istəyir. Bu andan
etibarən <code>servis.yoxla()</code> çağıra bilərik.</p>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
  it('baza cavab verəndə status "saglam" olur', async () =&gt; {
    prisma.yoxla.mockResolvedValue({ cedvelSayi: 48, gecikmeMs: 3 });

    const c = await servis.yoxla();

    expect(c.status).toBe('saglam');
    expect(c.baza.qosulub).toBe(true);
    expect(c.baza.cedvel_sayi).toBe(48);
    expect(c.baza.gecikme_ms).toBe(3);
  });</pre>
<ul>
  <li><strong>Arrange:</strong> <code>mockResolvedValue</code> ilə saxta
      bazanın cavabını təyin edirik. Diqqət: burada <code>cedvelSayi</code>
      (camelCase) yazırıq, çünki bu, Prisma-nın daxili adıdır.</li>
  <li><strong>Act:</strong> <code>await servis.yoxla()</code> — həqiqi
      metodu çağırırıq. Test edilən <em>əsl</em> koddur.</li>
  <li><strong>Assert:</strong> dörd iddia. Diqqət yetirin:
      <code>cedvel_sayi</code> (snake_case) — çünki servis cavabı
      xarici dünya üçün <em>yoxlamadan keçirir</em>. Bu iki adın fərqi
      təsadüfi deyil və test məhz bu çevrilməni yoxlayır.</li>
  <li><code>async</code> / <code>await</code> — <code>yoxla()</code>
      Promise qaytarır, ona görə gözləmək lazımdır. <code>await</code>
      unudulsa, test <em>həmişə keçərdi</em> (çünki iddialar işləməyə
      vaxt tapmazdı). Bu, ən məkrli test səhvidir!</li>
</ul>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
  it('baza xəta verəndə xəta YUXARI ötürülür (udulmur)', async () =&gt; {
    prisma.yoxla.mockRejectedValue(new Error('bağlantı yoxdur'));

    await expect(servis.yoxla()).rejects.toThrow('bağlantı yoxdur');
  });</pre>
<ul>
  <li><code>mockRejectedValue</code> — saxta baza <em>xəta verir</em>.</li>
  <li><code>rejects.toThrow(...)</code> — «bu Promise rədd edilməli və
      xəta mesajında bu mətn olmalıdır». <code>await</code> mütləqdir,
      yoxsa Vitest iddianın nəticəsini gözləməz.</li>
  <li><strong>Nə üçün bu test dəyərlidir?</strong> Çünki asan
      «düzəliş» <code>try/catch</code> ilə xətanı udmaq olardı. O zaman
      baza ölü olsa da API <code>200 "saglam"</code> qaytarardı —
      monitorinq sistemi heç nə görməzdi. Bu test həmin səhvi
      <em>dərhal</em> tutur.</li>
</ul>
""",
    "fayllar": ["src/saglamliq/saglamliq.service.spec.ts"],
    "goster": ["src/prisma/prisma.service.ts"],
    "c": r"""
echo "════ 1) Vahid testləri işlədirik ════"
npx vitest run

echo ""
echo "════ 2) Hər testin adı ilə (verbose) ════"
npx vitest run --reporter=verbose

echo ""
echo "════ 3) SÜBUT: vahid testlər BAZAYA TOXUNMUR ════"
echo "  → DATABASE_URL-i qəsdən YANLIŞ veririk."
echo "    9999 portunda heç bir baza yoxdur — qoşulmaq mümkün deyil."
echo ""
DATABASE_URL="postgresql://yoxdur:yoxdur@localhost:9999/yoxdur" npx vitest run
echo "  ↑ exit kodu: $? — 0 olmalıdır, çünki baza HEÇ SORUŞULMADI"

echo ""
echo "════ 4) QIRMIZI test nə görünür? ════"
echo "  → qəsdən səhv iddia olan müvəqqəti test yaradırıq:"
cat > src/saglamliq/_muveqqeti.spec.ts <<'SON'
import { describe, expect, it } from 'vitest';

describe('qəsdən səhv test', () => {
  it('2 + 2 = 5 olmalıdır — bu YANLIŞ gözləntidir', () => {
    expect(2 + 2).toBe(5);
  });
});
SON
npx vitest run src/saglamliq/_muveqqeti.spec.ts
echo "  ↑ exit kodu: $? — 1 olmalıdır: uğursuz test bunu BİLDİRİR"
rm -f src/saglamliq/_muveqqeti.spec.ts
echo "  ✓ müvəqqəti test silindi"

echo ""
echo "════ 5) Təmizlikdən sonra yenidən ════"
npx vitest run
printf '  _muveqqeti.spec.ts → %s\n' "$([ -f src/saglamliq/_muveqqeti.spec.ts ] && echo 'HƏLƏ DURUR' || echo 'yoxdur (yaxşıdır)')"
""",
    "olmaz": """Mock (saxta) olmadan nə olardı?

$ npx vitest run

 ❯ src/saglamliq/saglamliq.service.spec.ts (3 tests | 3 failed)

 FAIL  SaglamliqService (unit) > baza cavab verəndə status "saglam" olur
 PrismaClientInitializationError:
   Can't reach database server at `localhost:5432`
     Please make sure your database server is running at `localhost:5432`.

  ← ⚠️ Test SERVİSİN MƏNTİQİNİ yoxlamaq istəyirdi, amma
     BAZAYA görə uğursuz oldu. Kod isə TAMAM düzgündür.

────────────────────────────────────────────────────────────
VƏ YA `beforeEach` olmasa:

 $ npx vitest run
  ✓ 3 test keçdi

 $ npx vitest run --sequence.shuffle
  ✓ 2 test keçdi, ✗ 1 test uğursuz
  ← ⚠️ Testlər TƏK-TƏK keçir, BİRLİKDƏ uğursuz olur.
     Səbəb: birinci test saxta bazanı sazlayır, digərləri
     onun «zibilini» miras alır.

────────────────────────────────────────────────────────────
VƏ YA `await` unudulsa:

 expect(c.status).toBe('saglam');   // ← await yoxdur

  ✓ test KEÇDİ   ← ⚠️ YALANÇI YAŞIL! İddialar heç vaxt
                    icra olunmadı, çünki Promise hələ
                    həll olunmamışdı.""",
    "c_izah": """
<p><strong>Birinci və ən güclü sübut — 3-cü bölmə.</strong>
<code>DATABASE_URL</code> dəyişənini <code>localhost:9999</code>-a
yönləndirdik — orada heç bir baza yoxdur. Əgər test real
<code>PrismaService</code> işlətsəydi, <em>dərhal</em>
<code>ECONNREFUSED</code> xətası alardıq. Amma test
<strong>keçdi</strong>. Bu, təcridin danılmaz sübutudur: saxta obyekt
sayəsində baza heç soruşulmadı.</p>
<p><strong>İkinci sübut — 4-cü bölmə.</strong> Qəsdən səhv bir test
yazdıq: <code>expect(2 + 2).toBe(5)</code>. Aldığımız çıxış nə göstərir?
<code>- Expected + Received</code> fərqini, fayl adını, sətir nömrəsini və
kodu <code>exit 1</code> ilə dayandırdı. Bu, testin
<em>işlədiyinin</em> sübutudur — «həmişə yaşıl» bir test dəsti faydasızdır.
Bizim testimiz qırmızı ola <em>bilir</em>, deməli yaşıl olması mənalıdır.</p>
<p><strong>Nə üçün bu qədər ətraflı?</strong> Çünki test yazmağın bir
tələsi var: <em>heç vaxt uğursuz ola bilməyən test</em> yazmaq asandır.
Məsələn <code>expect(true).toBe(true)</code> həmişə keçər, amma heç nə
yoxlamır. Ona görə peşəkar yanaşma belədir: <strong>əvvəlcə testi yaz,
onun qırmızı olduğunu gör, sonra kodu yaz və yaşıl olsun.</strong> Buna
TDD (Test-Driven Development) deyilir.</p>
<p><strong>Üçüncü nüans:</strong> 4-cü bölmədə müvəqqəti faylı filtr kimi
verdik (<code>npx vitest run src/saglamliq/_muveqqeti.spec.ts</code>).
Vitest mövqeyə görə verilən arqumentləri <em>filtr</em> kimi başa düşür:
yalnız adı uyğun gələn faylları işlədir. Ona görə əsas 3 testimiz
işləmədi — və bu, vaxt qazandırdı.</p>
""",
    "sual": [
        ("Saxta (mock) obyekt «real kodu» yoxlamır ki! Test yalançı deyilmi?",
         "Bu, ən yaxşı sualdır. Vahid test <em>həqiqətən</em> yoxlamır ki, "
         "Prisma bazaya qoşula bilir. O, yalnız bunu yoxlayır: "
         "<strong>«əgər baza belə cavab versə, servis düzgün formatlayırmı?»</strong>. "
         "Baza ilə həqiqi əlaqəni isə <em>e2e test</em> yoxlayır (ADDIM 16). "
         "İkisi birlikdə tam mənzərəni verir — buna «test piramidası» deyilir."),
        ("<code>vi.fn()</code> əvəzinə sadəcə <code>() =&gt; ({...})</code> yazsam olmaz?",
         "Sadə funksiya da işləyər, amma <code>vi.fn()</code> əlavə imkanlar "
         "verir: (1) <code>mockResolvedValue</code> kimi rahat metodlar; "
         "(2) <code>expect(prisma.yoxla).toHaveBeenCalledTimes(1)</code> ilə "
         "«neçə dəfə çağırıldı» yoxlaması; (3) <code>toHaveBeenCalledWith</code> "
         "ilə «hansı arqumentlərlə çağırıldı» yoxlaması. Sadə funksiya ilə "
         "bunlar üçün əl ilə sayğac yazmalı olardınız."),
        ("Nə üçün <code>prisma</code> obyektində yalnız <code>yoxla</code> var?",
         "Çünki <code>PrismaService</code> 48 model metodu daşıyır "
         "(<code>emekdaslar</code>, <code>merkezler</code>…). Hamısını saxta "
         "etmək lazımsız zəhmətdir. Test yalnız <em>istifadə olunan</em> "
         "metodları saxta edir. Bu prinsipin adı «test double minimalizmi»dir: "
         "yalnız ehtiyac olanı ver."),
        ("<code>toEqual</code> ilə <code>toBe</code>-i qarışdırsam nə olar?",
         "<code>toBe</code> <em>eyniliyi</em> yoxlayır (<code>Object.is</code>). "
         "İki ayrı <code>{a:1}</code> obyekti <em>eyni deyil</em> — ikisi "
         "yaddaşda fərqli yerdədir. Ona görə "
         "<code>expect({a:1}).toBe({a:1})</code> uğursuz olar, "
         "<code>expect({a:1}).toEqual({a:1})</code> isə keçər. Ədədlər, "
         "mətnlər, boolean-lar üçün <code>toBe</code> daha sürətli və "
         "aydındır."),
        ("Test faylı <code>src/</code> içində olmalıdır, <code>test/</code> yox?",
         "Vahid testlər adətən yoxladıqları faylın <em>yanında</em> olur: "
         "<code>saglamliq.service.ts</code> + <code>saglamliq.service.spec.ts</code>. "
         "Faydası: kodu dəyişəndə testi dərhal görürsən, onu tapmaq üçün "
         "aramaq lazım gəlmir. E2e testlər isə bütün tətbiqi yoxladığı üçün "
         "ayrı <code>test/</code> qovluğunda saxlanır."),
        ("Testlərin adını Azərbaycanca yazmaq olar?",
         "Bəli, və <em>məsləhətdir</em>! Testin adı elə <em>cümlə</em> kimi "
         "oxunmalıdır: <code>it('baza cavab verəndə status \"saglam\" olur')</code>. "
         "Uğursuz olanda çıxışda bu cümlə görünür və nəyin sındığını dərhal "
         "anlayırsınız. İngilis dilində yazmaq texniki məcburiyyət deyil."),
        ("Test nədir — <code>dist/</code> içinə düşür?",
         "Xeyr. <code>tsconfig.build.json</code> faylında "
         "<code>\"exclude\": [..., \"**/*spec.ts\"]</code> sətri var — "
         "ADDIM 12-də bunu gördük. Yəni testlər istehsalat build-inə "
         "düşmür. Sonda ADDIM 16-da bunu <code>find</code> ilə "
         "yoxlayacağıq."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>3 vahid test yazdıq və hamısı <strong>keçdi</strong> — ümumi müddət
      təxminən 200 millisaniyə.</li>
  <li><strong>Təcrid sübut olundu:</strong> <code>DATABASE_URL</code>-i
      mövcud olmayan bazaya yönləndirdik, testlər yenə də keçdi. Yəni
      vahid testlər bazadan <em>heç asılı deyil</em>.</li>
  <li><strong>Qırmızı testi gördük:</strong> səhv iddia
      <code>exit 1</code>, fayl adı, sətir nömrəsi və
      <code>- Expected + Received</code> fərqini verdi. Test dəstimizin
      uğursuz ola <em>biləcəyini</em> təsdiqlədik — bu, onun
      etibarlılığının açarıdır.</li>
  <li><code>beforeEach</code> + <code>vi.fn()</code> +
      <code>{ provide, useValue }</code> — üçlüyü Nest-də vahid testin
      <em>əsas naxışıdır</em>. Bunu bir dəfə öyrəndikdən sonra istənilən
      servis üçün test yaza bilərsiniz.</li>
</ul>
<p><strong>Ölçü:</strong> 3 test · ~200 ms · baza tələb olunmur.
Müqayisə üçün: növbəti addımdaki 4 e2e test ~400 ms çəkir və
<strong>real baza tələb edir</strong>. Fərqi hiss edirsiniz?</p>
<p><strong>Növbəti addımda</strong> eyni funksionallığı — sağlamlıq
endpointini — bu dəfə <em>bütöv</em> yoxlayacağıq: həqiqi HTTP sorğusu,
həqiqi Nest tətbiqi, həqiqi baza. İkisi bir-birini tamamlayır.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 16 — E2E TEST
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 16,
    "ad": "e2e test yazırıq — bütöv sistemi yoxlayırıq",
    "a": """
<p>Vahid testdə <code>SaglamliqService</code>-i <em>təcrid etdik</em>:
saxta baza verdik. Amma bir sual qaldı: <strong>«Bütün bunlar birlikdə
həqiqətən işləyirmi?»</strong> Modullar düzgün bağlanıbmı?
<code>main.ts</code>-dəki prefiks həqiqətən tətbiq olunurmu? Xəta filtri
işləyirmi? Real baza cavab verirmi?</p>
<p>Bu suallara yalnız <strong>e2e test</strong> cavab verir. «e2e» —
<em>end-to-end</em>, «başdan-başa». Sistem istifadəçinin gördüyü kimi
yoxlanılır: HTTP sorğusu göndərilir, cavab yoxlanılır.</p>

<h4>Vahid test ilə e2e testin fərqi</h4>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0"></th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Vahid (ADDIM 15)</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">e2e (bu addım)</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Nə qurulur</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Yalnız bir servis + saxta asılılıq</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Bütöv <code>AppModule</code></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Baza</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Saxta — lazım deyil</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Real</strong> — mütləqdir</td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Sorğu</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Birbaşa metod çağırışı</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Həqiqi HTTP (supertest)</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Nə tutur</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Məntiq səhvləri</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Bağlantı, prefiks, filtr, baza səhvləri</td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Sürət</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">~30 ms / test</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">~35 ms / test + qurulma ~150 ms</td>
  </tr>
</table>

<h4>⚠️ ƏN VACİB TƏLƏ: <code>main.ts</code> TƏKRARLANMALIDIR</h4>
<p>Diqqət yetirin: <code>main.ts</code> faylında bunlar var idi:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
app.setGlobalPrefix('api/v1');
app.useGlobalPipes(new ValidationPipe({ ... }));
app.useGlobalFilters(new AllExceptionsFilter());</pre>
<p>Amma bu sətirlər <code>bootstrap()</code> funksiyasının içindədir və
<code>bootstrap()</code> yalnız <code>main.ts</code> <em>işə salınanda</em>
çağırılır. Testdə isə biz <code>main.ts</code>-i işlətmirik — özümüz
tətbiqi qururuq. Deməli bu üç sətri <strong>testdə əl ilə təkrarlamalıyıq</strong>.</p>
<div class="olmaz" style="margin-top:1rem">
<h4>⚠️ Təkrar etməsək nə olar? — YALANÇI YAŞIL</h4>
<pre style="background:#fff;color:#7f1d1d;border-radius:8px;padding:1rem 1.1rem">
// main.ts-dəki konfiqurasiya testdə YOXDUR:
app = modul.createNestApplication();
await app.init();

// ...və sonra:
await request(app.getHttpServer())
  .get('/api/v1/saglamliq')
  .expect(200);

→ FAIL: expected 200 "OK", got 404 "Not Found"
  ← ⚠️ Test UĞURSUZ olur, halbuki KOD düzgündür!
     Çünki test tətbiqində prefiks təyin olunmayıb.

DAHA PİSİ: əgər testi prefikssiz yazsaydıq —
  .get('/saglamliq').expect(200)
— test KEÇƏRDİ, amma istehsalatda
  404 alardıq. Bu, YALANÇI YAŞIL testdir:
  test «hər şey qaydasındadır» deyir, real sistem isə sınıqdır.</pre>
</div>
<p>Ona görə test faylında <code>beforeAll</code> bloku
<code>main.ts</code>-in <em>güzgüsüdür</em>. Bu, NestJS-də çox tanınan bir
tələdir və həlləri var:</p>
<ul>
  <li><strong>Bizim seçimimiz:</strong> konfiqurasiyanı testdə təkrarla.
      Sadədir, aydındır, əlavə fayl tələb etmir.</li>
  <li><strong>Alternativ:</strong> <code>src/app.setup.ts</code> faylı
      yaradıb konfiqurasiyanı ora köçürmək və həm <code>main.ts</code>,
      həm test onu çağırsın. Daha «quru» (DRY), amma bir fayl artıq.</li>
</ul>

<h4>Niyə <code>app.listen()</code> yox, <code>app.init()</code>?</h4>
<p><code>app.listen(4000)</code> — serveri <em>real şəbəkə portunda</em>
dinləməyə başlayır. Testdə buna ehtiyac yoxdur. <code>app.init()</code>
isə tətbiqi hazırlayır (modulları həll edir, DI qrafını qurur, baza
bağlantısını açır), amma port tutmur. Faydaları:</p>
<ul>
  <li>Port məşğul ola bilməz — testlər paralel işləyə bilər.</li>
  <li>Testlər üçün real şəbəkə lazım deyil.</li>
  <li><code>supertest</code> daxili HTTP serveri özü idarə edir.</li>
</ul>

<h4><code>supertest</code> nədir?</h4>
<p>Bu paket HTTP serverini <em>birbaşa yaddaşda</em> işlədir və sorğuları
ona ötürür. Yəni həqiqi TCP bağlantısı qurulur, amma <code>localhost:4000</code>
ünvanına <em>deyil</em>, sizin tətbiq obyektinizə. API-si çox aydındır:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
await request(app.getHttpServer())
  .get('/api/v1/saglamliq')
  .expect(200);</pre>
<p><code>.expect(200)</code> — status kodu yoxlayır və uyğun gəlməsə testi
uğursuz edir. Zəncirvari yazılış (chaining) sayəsində bir sorğu bir neçə
yoxlamanı birləşdirir.</p>

<h4>Niyə <code>afterAll</code> içində <code>app.close()</code>?</h4>
<p>Bu, <strong>mütləqdir</strong>. <code>app.init()</code> Prisma
bağlantısını açdı. <code>app.close()</code> olmasa:</p>
<ul>
  <li>Vitest prosesi <em>bitməyəcək</em> — açıq TCP bağlantısı prosesi
      diri saxlayır. Terminalda sanki «donub». Yaxşı halda Vitest
      xəbərdarlıq verir, pis halda <code>Ctrl+C</code> lazım gəlir.</li>
  <li>PostgreSQL-də istifadə olunmayan bağlantılar yığılır. Çox testdən
      sonra baza <code>too many clients already</code> xətası verir.</li>
</ul>

<h4>Dörd testimiz</h4>
<ol>
  <li><strong>Xoşbəxt yol:</strong> <code>GET /api/v1/saglamliq</code> →
      <code>200</code>, gövdədə <code>status: "saglam"</code>,
      <code>baza.qosulub: true</code>, <code>baza.cedvel_sayi: 48</code>.
      Bu test real bazaya <em>toxunur</em>.</li>
  <li><strong>Kök yol:</strong> <code>GET /api/v1</code> → <code>200</code>
      və <code>prefiks: "/api/v1"</code>. Modulun düzgün bağlandığını
      təsdiqləyir.</li>
  <li><strong>Əks yoxlama:</strong> <code>GET /saglamliq</code> (prefiks
      olmadan) → <code>404</code>. Prefiksin həqiqətən işlədiyinin
      sübutu.</li>
  <li><strong>Xəta formatı:</strong> <code>GET /api/v1/yoxdur</code> →
      <code>404</code> və gövdədə <code>ugur: false</code>,
      <code>xeta.kod: "TAPILMADI"</code>. Bu, 1A-nın ADDIM 8-də yazdığımız
      <code>AllExceptionsFilter</code>-in işlədiyini sübut edir.</li>
</ol>
<p>Diqqət: 3-cü və 4-cü testlər <strong>«mənfi» testlərdir</strong> —
uğursuzluq yollarını yoxlayırlar. Onlar olmasa, API-nin «səhv olanda
düzgün davrandığını» bilməzdik.</p>
""",
    "anlayis": [
        ("e2e (end-to-end)",
         "«Başdan-başa». Bütöv sistemi istifadəçinin gördüyü kimi yoxlayan "
         "test: real HTTP, real baza, real cavab."),
        ("supertest",
         "Node HTTP serverlərini yaddaşda yoxlayan kitabxana. Şəbəkə portu "
         "tutmur, sorğuları birbaşa tətbiqə ötürür."),
        ("createNestApplication()",
         "Nest modulundan işlək tətbiq nüsxəsi yaradır — amma "
         "<code>main.ts</code>-dəki konfiqurasiya <em>daxil deyil</em>."),
        ("app.init() / app.close()",
         "Tətbiqi port tutmadan hazırla / resursları azad et. "
         "<code>close()</code> olmasa Vitest prosesi bitmir."),
        ("beforeAll / afterAll",
         "Bütün testlərdən əvvəl bir dəfə tətbiqi qur, sonra bir dəfə bağla. "
         "Hər test üçün yenidən qurmaq çox yavaş olardı."),
        ("Mənfi test",
         "«Uğursuz olmalı olan» halı yoxlayan test (məsələn 404 gözləmək). "
         "Xoşbəxt yol qədər vacibdir."),
        ("Yalançı yaşıl (false green)",
         "Test keçir, amma real sistem sınıqdır. Səbəb: test real "
         "konfiqurasiyanı yoxlamır."),
        ("ValidationPipe",
         "Gələn məlumatı yoxlayan və çevirən Nest mexanizmi. "
         "<code>whitelist</code> + <code>transform</code> ayarları ilə."),
        ("AllExceptionsFilter",
         "Bütün xətaları tutub <em>vahid</em> JSON formatına salan filtr. "
         "Frontend həmişə eyni quruluşu gözləyə bilir."),
        ("DRY prinsipi",
         "«Don't Repeat Yourself» — eyni kodu iki yerdə yazma. Bizim "
         "halda <code>main.ts</code> və test konfiqurasiyası təkrarlanır; "
         "bu, şüurlu bir güzəştdir."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">Sətir-sətir</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
import { INestApplication, ValidationPipe } from '@nestjs/common';
import { Test, TestingModule } from '@nestjs/testing';
import request from 'supertest';
import { AppModule } from '../src/app.module.js';
import { AllExceptionsFilter } from '../src/common/filters/all-exceptions.filter.js';</pre>
<ul>
  <li><code>INestApplication</code> — tətbiq obyektinin tipi.
      <code>app.getHttpServer()</code> metodu ondadır.</li>
  <li><code>request</code> — <strong>default import</strong>
      (<code>import request from 'supertest'</code>), qıvrım mötərizəsiz.
      Səbəb: <code>supertest</code> <code>export =</code> sintaksisi ilə
      yazılıb (CommonJS) və <code>esModuleInterop</code> ayarı bunu
      dəstəkləyir.</li>
  <li>Fayl <code>test/</code> qovluğundadır, ona görə <code>src/</code>-ə
      yol <code>../src/...</code> kimi yazılır. Yenə <code>.js</code>
      uzantısı ilə.</li>
</ul>
<p><strong>Qeyd — <code>supertest/types</code> tələsi:</strong> Nest-in
şablonlarında tez-tez <code>import { App } from 'supertest/types'</code>
sətri olur və <code>app: INestApplication&lt;App&gt;</code> yazılır. Bizim
konfiqurasiyada (<code>moduleResolution: "nodenext"</code> +
<code>resolvePackageJsonExports: true</code>) bu import
<strong>işləmir</strong>: <code>supertest</code> paketinin
<code>package.json</code>-unda <code>exports</code> bölməsi olmadığı üçün
TypeScript <code>supertest/types</code> alt yolunu tapa bilmir və
<code>TS2307</code> xətası verir. Ona görə sadə
<code>INestApplication</code> tipini istifadə edirik. Bu xəta
«Tanış xətalar» bölməsində də qeyd olunub.</p>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
describe('Sağlamlıq (e2e)', () =&gt; {
  let app: INestApplication;

  beforeAll(async () =&gt; {
    const modul: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();</pre>
<ul>
  <li><code>beforeAll</code> — <em>bir dəfə</em>, bütün testlərdən əvvəl.
      Niyə <code>beforeEach</code> deyil? Çünki tətbiqi qurmaq bahalıdır
      (~150 ms). Hər testdən əvvəl qursaydıq, 4 test = 600 ms əlavə vaxt.</li>
  <li><code>imports: [AppModule]</code> — <strong>bütöv</strong> tətbiq
      modulu. Nest bütün asılılıq qrafını özü qurur: <code>ConfigModule</code>
      → <code>.env</code> oxuyur, <code>PrismaModule</code> → bazaya
      qoşulur, <code>SaglamliqModule</code> → endpoint-i qeydiyyatdan
      keçirir.</li>
  <li><code>.compile()</code> — DI qrafını həll edir. Bu mərhələdə
      <code>PrismaService</code> <em>yaradılır</em> — yəni
      <code>DATABASE_URL</code> oxunur və adapter qurulur.
      <strong>Bazaya həqiqi qoşulma isə <code>init()</code>-də olur.</strong></li>
</ul>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
    app = modul.createNestApplication();

    // ⚠️ main.ts-dəki konfiqurasiya BURADA TƏKRARLANIR:
    app.setGlobalPrefix('api/v1');
    app.useGlobalPipes(
      new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }),
    );
    app.useGlobalFilters(new AllExceptionsFilter());

    await app.init();
  });</pre>
<ul>
  <li><code>createNestApplication()</code> — Nest tətbiq obyekti yaradır.
      Hələ <em>işləmir</em> — sadəcə obyektdir.</li>
  <li>Üç konfiqurasiya sətri <code>main.ts</code>-in güzgüsüdür.
      <strong>Sıra vacibdir:</strong> əvvəlcə prefiks, sonra pipe, sonra
      filtr. Bu, <code>main.ts</code>-dəki sıra ilə eyni olmalıdır ki,
      davranış tam üst-üstə düşsün.</li>
  <li><code>await app.init()</code> — modulların
      <code>onModuleInit</code> qarmaqlarını çağırır. <code>PrismaService</code>
      üçün bu, <code>$connect()</code> deməkdir — <em>bu anda</em>
      bazaya həqiqi bağlantı açılır.</li>
</ul>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
  afterAll(async () =&gt; {
    await app.close();
  });</pre>
<p><code>app.close()</code> — <code>onModuleDestroy</code> qarmaqlarını
çağırır → <code>PrismaService.$disconnect()</code>. Unudulsa, Vitest
prosesi asılı qalar. Bu, e2e testlərdə ən çox rast gəlinən «testlər keçir,
amma terminal donur» probleminin səbəbidir.</p>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
  it('GET /api/v1/saglamliq → 200, baza qoşulub, 48 cədvəl', async () =&gt; {
    const c = await request(app.getHttpServer())
      .get('/api/v1/saglamliq')
      .expect(200);

    expect(c.body.status).toBe('saglam');
    expect(c.body.baza.qosulub).toBe(true);
    expect(c.body.baza.cedvel_sayi).toBe(48);
  });</pre>
<ul>
  <li><code>app.getHttpServer()</code> — Nest-in altındaki Express serveri.
      <code>supertest</code> onu dinləyir.</li>
  <li><code>.get('/api/v1/saglamliq')</code> — tam yol, prefiks daxil.</li>
  <li><code>.expect(200)</code> — iki iş görür: statusu yoxlayır
      <em>və</em> cavabı gözləyir. Ona görə <code>await</code> lazımdır.</li>
  <li><code>c.body</code> — cavabın JSON kimi oxunmuş gövdəsi.
      <code>supertest</code> <code>Content-Type: application/json</code>
      gördükdə avtomatik parse edir.</li>
  <li><code>48</code> — bazamızdaki cədvəl sayı. <strong>Diqqət:</strong>
      bu rəqəm dəyişsə (yeni cədvəl əlavə olunsa), test də yenilənməlidir.
      Bu, «kırılgan test» (brittle test) nümunəsidir. Alternativ:
      <code>expect(c.body.baza.cedvel_sayi).toBeGreaterThan(40)</code>
      yazmaq. Amma <em>dəqiq</em> rəqəm daha güclü siqnaldır: baza
      sxemi dəyişdisə, bunu bilmək istəyirik.</li>
</ul>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
  it('prefikssiz yol → 404', async () =&gt; {
    await request(app.getHttpServer()).get('/saglamliq').expect(404);
  });</pre>
<p>Bir sətirlik, amma çox güclü test. <code>setGlobalPrefix</code> sətri
silib yoxlamaq üçün <em>yeganə</em> yol budur. Əgər kimsə
<code>main.ts</code>-dən prefiksi silsə, bu test <em>dərhal</em> qırmızı
olar.</p>

<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
  it('olmayan yol → vahid xəta formatı', async () =&gt; {
    const c = await request(app.getHttpServer())
      .get('/api/v1/yoxdur')
      .expect(404);

    expect(c.body.ugur).toBe(false);
    expect(c.body.xeta.kod).toBe('TAPILMADI');
    expect(typeof c.body.vaxt).toBe('string');
  });</pre>
<ul>
  <li>Bu test <code>AllExceptionsFilter</code>-i yoxlayır. Filtr olmasaydı,
      Nest-in <em>varsayılan</em> cavabı gələrdi:
      <code>{"statusCode":404,"message":"Cannot GET /api/v1/yoxdur","error":"Not Found"}</code>.
      Frontend isə <code>ugur</code> sahəsini gözləyir.</li>
  <li><code>typeof c.body.vaxt === 'string'</code> — <em>tip yoxlaması</em>.
      Dəqiq dəyəri bilmirik (indi olan vaxtdır), amma tipini bilirik.
      Bu, «kırılgan olmayan» yoxlamadır.</li>
</ul>
""",
    "fayllar": ["test/saglamliq.e2e-spec.ts"],
    "goster": ["src/common/filters/all-exceptions.filter.ts"],
    "c": r"""
echo "════ 1) e2e testləri işlədirik ════"
npx vitest run --config vitest.config.e2e.ts

echo ""
echo "════ 2) Hər testin adı ilə (verbose) ════"
npx vitest run --config vitest.config.e2e.ts --reporter=verbose

echo ""
echo "════ 3) SÜBUT: e2e testlər BAZASIZ KEÇMİR ════"
echo "  → DATABASE_URL-i qəsdən yanlış veririk (9999 portunda baza yoxdur)."
echo "    Vahid testlər bu halda KEÇMİŞDİ — indi gözləyirik ki KEÇMƏSİN:"
echo ""
DATABASE_URL="postgresql://yoxdur:yoxdur@localhost:9999/yoxdur" npx vitest run --config vitest.config.e2e.ts
echo "  ↑ exit kodu: $? — 1 gözlənilir: baza olmadan 200 ala bilmərik"

echo ""
echo "════ 4) npm skriptləri ilə (əzbərləmək lazım deyil) ════"
npm test
npm run test:e2e

echo ""
echo "════ 5) Build nəticəsinə test düşübmü? ════"
npm run build
printf '  dist içində *spec* fayl sayı: %s  (0 olmalıdır)\n' "$(find dist -name '*spec*' | wc -l | tr -d ' ')"
echo "  → tapılan fayllar (boş olmalıdır):"
find dist -name '*spec*' | head -5 | sed 's/^/      /'

echo ""
echo "════ 6) YEKUN: hər şey bir yerdə ════"
echo "  a) Tip yoxlaması:"
npx tsc --noEmit && echo "     ✓ təmizdir"
echo ""
echo "  b) Vahid testlər:"
npx vitest run 2>&1 | tail -6
echo ""
echo "  c) e2e testlər:"
npx vitest run --config vitest.config.e2e.ts 2>&1 | tail -6
""",
    "olmaz": """`main.ts`-dəki konfiqurasiya testdə təkrarlanmasa:

$ npx vitest run --config vitest.config.e2e.ts

 ❯ test/saglamliq.e2e-spec.ts (4 tests | 2 failed)

 FAIL  GET /api/v1/saglamliq → 200, baza qoşulub, 48 cədvəl
 AssertionError: expected 404 "Not Found", got 404 "Not Found"
   ← ⚠️ Prefiks təyin olunmadığı üçün yol TAPILMADI.

 FAIL  olmayan yol → vahid xəta formatı
 AssertionError: expected undefined to be false
   ← ⚠️ Filtr təyin olunmadığı üçün cavab vahid formatda DEYİL.

────────────────────────────────────────────────────────────
VƏ YA `afterAll` içində `app.close()` olmasa:

$ npx vitest run --config vitest.config.e2e.ts
 ✓ test/saglamliq.e2e-spec.ts (4 tests) 143ms

 Test Files  1 passed (1)
      Tests  4 passed (4)

  ...
  ← ⚠️ PROSES BİTMİR. Terminal donur. `Ctrl+C` lazım gəlir.
     Səbəb: Prisma-nın açıq TCP bağlantısı prosesi diri saxlayır.

────────────────────────────────────────────────────────────
VƏ YA test prefikssiz yazılsa (YALANÇI YAŞIL):

 .get('/saglamliq').expect(200)
  ✓ 4 test keçdi
  ← ⚠️ Testlər YAŞIL, istehsalatda isə bütün sorğular 404 alır.
     Test heç vaxt sınaqdan keçirmədiyi şeyi «təsdiqlədi».""",
    "c_izah": """
<p><strong>Birinci müşahidə — 3-cü bölmə.</strong> Vahid testlərdə eyni
yanlış <code>DATABASE_URL</code> ilə testlər <em>keçdi</em>. İndi isə
e2e testlər <strong>uğursuz oldu</strong>. Bu, iki test növünün fərqini
göstərən ən aydın sübutdur: e2e test həqiqətən bazaya <em>toxunur</em>,
vahid test isə yox.</p>
<p>Maraqlıdır ki, 4 testdən yalnız <strong>biri</strong> uğursuz oldu.
Səbəb: <code>/api/v1</code>, <code>/saglamliq</code> (404) və
<code>/api/v1/yoxdur</code> yolları bazaya sorğu göndərmir. Yalnız
<code>/api/v1/saglamliq</code> bazadan cədvəl sayını oxuyur. Bu, test
dəstinin <em>dəqiq</em> olduğunu göstərir — hər test öz məsuliyyətini
bilir.</p>
<p><strong>İkinci müşahidə — 5-ci bölmə.</strong>
<code>find dist -name '*spec*'</code> əmri <strong>boş</strong> nəticə
verir. Bu o deməkdir ki, <code>tsconfig.build.json</code> faylındaki
<code>"exclude": [..., "**/*spec.ts"]</code> sətri işləyir və testlər
istehsalat build-inə düşmür. ADDIM 12-də bunu «nəzəri» olaraq
öyrənmişdik — indi <em>əməli</em> sübutunu gördük.</p>
<p><strong>Üçüncü müşahidə — 4-cü bölmə.</strong> <code>npm test</code> və
<code>npm run test:e2e</code> skriptləri eyni nəticəni verir. Bu vacibdir,
çünki komandada hər kəs <em>eyni</em> əmri işlədir. Uzun
<code>--config</code> parametrini xatırlamaq lazım deyil — və deməli
səhv yazmaq riski yoxdur.</p>
<p><strong>Ən mühüm nəticə:</strong> vahid testlər <em>məntiqi</em>
sürətli yoxlayır, e2e testlər isə <em>bütövlüyü</em>. İkisi bir-birinin
əvəzi deyil. Gündəlik işdə <code>npm test</code> işlədin (sürətli),
commit etməzdən əvvəl <code>npm run test:e2e</code> də işlədin (dərin).</p>
""",
    "sual": [
        ("Niyə <code>main.ts</code> konfiqurasiyasını testdə təkrarlayırıq? "
         "Bu, DRY prinsipini pozmur?",
         "Pozur, və bu, <em>şüurlu</em> bir güzəştdir. Nest-in rəsmi "
         "sənədləşdirməsində də bu naxış təklif olunur. Səbəb: "
         "<code>main.ts</code> <code>bootstrap()</code> funksiyasını "
         "çağırır, test isə onu çağırmır (çünki <code>bootstrap()</code> "
         "<code>app.listen()</code> edir və prosesi bloklayır). Daha "
         "«təmiz» həll: konfiqurasiyanı <code>src/app.setup.ts</code> "
         "faylına köçürüb hər iki yerdən çağırmaq. Amma bu, bir fayl "
         "artırır və kiçik layihələrdə artıq mürəkkəblik yaradır."),
        ("<code>supertest</code> niyə həqiqi port istifadə etmir? Bu, testi "
         "«real» etmir ki?",
         "Yaxşı sual. <code>supertest</code> <em>müvəqqəti</em> port "
         "ayırır (adətən <code>0</code> — «işletim sistemi özü seç»), "
         "sorğunu göndərir, sonra bağlayır. Yəni TCP səviyyəsində "
         "<strong>həqiqi</strong> HTTP sorğusudur. Yeganə fərq: "
         "ünvan <code>localhost:4000</code> deyil, <code>127.0.0.1:54321</code> "
         "kimi təsadüfi portdur. Marşrutlaşdırma, prefiks, filtrlər, "
         "JSON parse — hamısı <em>eyni</em> koddan keçir."),
        ("48 rəqəmi dəyişsə, test sınacaq. Bu yaxşı deyilmi?",
         "Bu, iki tərəfi olan qərardır. <em>Kırılgan test</em> (brittle) "
         "pis hesab olunur — çox vaxt yalançı uğursuzluq verir. Amma "
         "bazanın <em>sxemi</em> dəyişibsə, bunu bilmək "
         "<strong>istəyirik</strong>: 48 → 49 oldusa, kiminsə cədvəl "
         "əlavə etdiyini bilirik. Alternativ: "
         "<code>toBeGreaterThan(40)</code>. Mən Bunu <em>dəqiq</em> "
         "saxlayırdım, amma komanda ilə razılaşmaq lazımdır."),
        ("e2e testləri hər dəfə işlətmək çox vaxt almır?",
         "Bu layihədə yox — 4 test 400 millisaniyə çəkər. Böyük "
         "layihələrdə (1000+ e2e test) bəli, 10 dəqiqə çəkə bilər. "
         "Ona görə praktika belədir: inkişaf zamanı sürətli dəsti "
         "(vahid) işlət, commit/PR zamanı hər ikisini. CI sistemində "
         "isə hər ikisi avtomatik işlədilir."),
        ("<code>Test.createTestingModule</code> ilə "
         "<code>NestFactory.create</code> fərqi nədir?",
         "<code>NestFactory.create</code> — <em>istehsalat</em> üçündür: "
         "bütün tətbiqi qurur və real server dinləməyə hazır edir. "
         "<code>Test.createTestingModule</code> — <em>test</em> üçündür: "
         "eyni DI qrafını qurur, amma hər təchizatçını "
         "<code>overrideProvider</code> ilə əvəz etməyə imkan verir. "
         "Yəni test versiyası daha <em>çevikdir</em>."),
        ("<code>beforeAll</code> əvəzinə <code>beforeEach</code> işlətsəm nə olar?",
         "Testlər yenə keçər, amma yavaş olar: hər test üçün tətbiq "
         "yenidən qurulur, bazaya yenidən qoşulur. 4 test × ~150 ms = "
         "600 ms əlavə. Böyük dəstdə bu, dəqiqələrə çevrilir. Qayda: "
         "<em>dəyişməz</em> hazırlıq üçün <code>beforeAll</code>, "
         "<em>hər testdə təzələnməli</em> vəziyyət üçün "
         "<code>beforeEach</code>."),
        ("Bu test faylları da <code>dist/</code>-ə düşür?",
         "Xeyr — 5-ci bölmədə <code>find dist -name '*spec*'</code> "
         "əmrinin boş nəticəsini gördük. <code>tsconfig.build.json</code> "
         "faylındaki <code>include: [\"src\"]</code> və "
         "<code>exclude: [..., \"**/*spec.ts\"]</code> birlikdə bunu "
         "təmin edir."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>4 e2e test yazdıq, hamısı <strong>keçdi</strong> — real bazaya
      qoşularaq, həqiqi HTTP sorğuları ilə.</li>
  <li><strong>e2e testlər bazadan asılıdır:</strong> yanlış
      <code>DATABASE_URL</code> ilə 4 testdən biri uğursuz oldu. Vahid
      testlər isə <em>eyni</em> halda keçmişdi. Fərq sübut olundu.</li>
  <li><strong>Testlər build-ə düşmür:</strong>
      <code>find dist -name '*spec*'</code> boş nəticə verdi.</li>
  <li><code>ALL IN ONE</code>: <code>tsc --noEmit</code> təmiz,
      <code>npm test</code> → 3/3, <code>npm run test:e2e</code> → 4/4.</li>
</ul>

<h3 style="color:#0f766e;margin-top:1.4rem">📘 Dərs 1B-nin yekunu</h3>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.7rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Addım</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Nə öyrəndik</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Əməli sübut</th>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>12</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Build, <code>dist/</code>,
        <code>deleteOutDir</code>, tip yoxlaması</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Saxta fayl build-dən
        sonra yoxa çıxdı; <code>TS2322</code> xətası tutuldu</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>13</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Serveri qaldırmaq,
        portlar, <code>lsof</code>, <code>trap</code>, <code>curl</code></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">200/200/404 alındı;
        skriptdən sonra port boşaldı</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>14</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Test anlayışı,
        Vitest, iki konfiqurasiya</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Üç konfiqurasiya
        müqayisə edildi: 3 : 4 : 7 test</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>15</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">Vahid test,
        <code>mock</code>, <code>beforeEach</code>, xəta yolu</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">3/3 keçdi —
        <em>bazasız</em>; qırmızı test görüldü</td>
  </tr>
  <tr>
    <td style="padding:.45rem;border:1px solid #e2e8f0"><strong>16</strong></td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">e2e test,
        <code>supertest</code>, mənfi testlər, təmizlik</td>
    <td style="padding:.45rem;border:1px solid #e2e8f0">4/4 keçdi —
        real baza ilə; bazasız uğursuz oldu</td>
  </tr>
</table>

<h3 style="color:#0f766e;margin-top:1.4rem">🚀 Növbəti addımlar</h3>
<p>Artıq sizin <strong>işləyən, yığılan və test edilən</strong> bir
backend skeletiniz var. İndi biznes məntiqinə keçə bilərsiniz:</p>
<ol>
  <li><strong>Dərs 2 — İlk CRUD modulu:</strong> <code>emekdaslar</code>
      cədvəli üçün tam CRUD (yarat, oxu, yenilə, sil). DTO-lar,
      validasiya, səhifələmə (pagination), filtr.</li>
  <li><strong>Dərs 3 — Autentifikasiya:</strong> JWT, <code>bcryptjs</code>
      ilə şifrə hash-lənməsi, rollar (RBAC), <code>@UseGuards</code>.</li>
  <li><strong>Dərs 4 — Excel hesabatları:</strong> <code>ExcelJS</code> ilə
      <code>.xlsx</code> ixracı, fayl endirmə endpointi.</li>
  <li><strong>Dərs 5 — Swagger sənədləşdirmə:</strong>
      <code>@ApiProperty</code>, <code>@ApiTags</code> ilə peşəkar API
      sənədləri.</li>
  <li><strong>Dərs 6 — Docker:</strong> <code>Dockerfile</code> +
      <code>docker-compose.yml</code> ilə bütün sistemi bir əmrlə qaldırmaq.</li>
</ol>

<p style="background:#f0fdfa;border-left:5px solid #14b8a6;border-radius:10px;
          padding:1rem 1.2rem;margin-top:1rem">
<strong>💡 Ən vacib vərdiş:</strong> hər yeni funksiya üçün test yazın.
Əvvəlcə <em>qırmızı</em> testi yazın (kod hələ yoxdur, test uğursuzdur),
sonra kodu yazın və <em>yaşıl</em> olsun. Bu, TDD-dir və sizi
«düzəltdim, amma nəyisə sındırdım» cəhənnəmindən xilas edir.
</p>
""",
})
