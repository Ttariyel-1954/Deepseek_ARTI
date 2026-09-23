# -*- coding: utf-8 -*-
"""DS_Backend-1A — addım 1–11 üçün GENİŞ izahlar (I kurs tələbələri üçün).

Hər addım üçün:
  ad       — addımın başlığı
  a        — A hissəsi: bu addım niyə var (geniş)
  anlayis   — terminlər lüğəti (yeni anlayışlar)
  kod_izah — B hissəsindən SONRA: kodun sətir-sətir izahı
  fayllar  — BACKEND-dən oxunacaq fayllar
  c        — C hissəsi: yoxlama əmrləri (real icra olunur → D bloku)
  olmaz    — bu kod olmasa nə olardı
  c_izah   — C-nin nəticəsinin izahı
  sual     — tez-tez verilən suallar
  d_izah   — D-dən sonra: sistemin vəziyyəti
"""

ADIMLAR = [
    # ═══════════════════════════════════════════════════════════════
    dict(
        no=1,
        ad="Layihə qovluğu və skelet",
        a="""<p>İlk sual budur: <strong>backend kodu hara yazılır?</strong> Kompüterinizdə
        onlarla layihə ola bilər — hər birinin öz qovluğu olmalıdır. Bu qovluq
        backend-in <em>evi</em>dir: kod, konfiqurasiya, asılılıqlar və testlər
        hamısı orada yaşayır.</p>
        <p>Bu dərsdə qurduğumuz layihə <code>~/Deepseek_ARTI/DS_Backend</code>
        qovluğunda olacaq. Niyə «DS_Backend»? Çünki eyni ana qovluqda başqa
        hissələr də var — baza (<code>DS_Baza</code>), dərslər
        (<code>DƏRSLƏR</code>). Hər hissənin öz yeri olsa, heç nə qarışmır.</p>
        <p><strong>Node.js layihəsi nə ilə başlayır?</strong> <code>package.json</code>
        faylı ilə. Bu fayl layihənin <em>şəxsiyyət vəsiqəsi</em>dir: adı,
        versiyası, hansı paketlərə ehtiyacı olduğu və hansı əmrləri işlədə
        bildiyi orada yazılır. Fayl olmasa, <code>npm</code> layihənin nə
        olduğunu bilmir.</p>
        <p>Bu addımda hələ kod yazmırıq — sadəcə sahəni hazırlayırıq.
        Bu, təməl qazmağa bənzəyir: görünən iş yoxdur, amma sonrakı hər şey
        bundan asılıdır.</p>""",
        anlayis=[
            ("Node.js", "JavaScript kodunu brauzerdən kənarda — yəni serverdə — işlədən mühit."),
            ("npm", "Node Package Manager — paketləri quraşdıran və layihə əmrlərini işlədən alət."),
            ("Paket (package)", "Başqasının yazdığı hazır kod parçası. Məsələn NestJS bir paketdir."),
            ("Asılılıq (dependency)", "Layihənizin işləməsi üçün lazım olan paket."),
            ("CWD", "Current Working Directory — terminalın hazırda «dayandığı» qovluq."),
        ],
        kod_izah="""<p>Bu addımda fayl yaradılmır — yalnız qovluq. Aşağıdaki əmrlər
        qovluğu yaradır və içinə girir:</p>
        <p><code>mkdir -p ~/Deepseek_ARTI/DS_Backend</code> — qovluq yaradır.
        <code>-p</code> işarəsi «arana qovluqları da yarat, varsa xəta vermə»
        deməkdir. Bu işarə olmasa, <code>Deepseek_ARTI</code> yoxdursa əmr xəta
        verərdi.</p>
        <p><code>cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"</code> — terminalı həmin qovluğa
        keçirir. <code>~</code> işarəsi ev qovluğunuzu bildirir
        (<code>/Users/royatalibova</code>). Bundan sonra bütün əmrlər bu
        qovluğun içində işləyəcək.</p>
        <p>⚠️ <strong>Vacib vərdiş:</strong> hər dəfə yeni terminal açanda ilk
        işiniz <code>cd</code> ilə layihə qovluğuna keçmək olmalıdır. Əks halda
        <code>npm</code> «package.json tapılmadı» deyəcək.</p>""",
        fayllar=[],
        c="""# 1) Layihə qovluğunu YARADIRIQ
#    -p işarəsi: arana qovluqları da yaradır və qovluq artıq
#    varsa xəta vermir («already exists» deməz).
mkdir -p ~/Deepseek_ARTI/DS_Backend

# 2) İçinə keçirik
cd ~/Deepseek_ARTI/DS_Backend

echo "── Qovluq yerindədirmi? ──"
pwd
echo
echo "── İçində nə var? (hələ boşdur) ──"
ls -la
echo
echo "── Alətlərin versiyaları ──"
echo "  node: $(node -v)"
echo "  npm:  $(npm -v)"
echo
echo "── Node hansı qovluqda quraşdırılıb? ──"
which node
which npm""",
        olmaz="""$ cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
-bash: cd: /Users/royatalibova/Deepseek_ARTI/DS_Backend: No such file or directory

   # ⚠️ Qovluq yoxdursa, sonrakı BÜTÜN addımlar sınır: package.json
   # yarada bilməzsiniz, npm install işləməz, server qalxmaz.
   # Xəta mesajı «No such file or directory» olur və səbəb çox vaxt
   # sadəcə yazı səhvidir (məsələn «DS_Backend» yerinə «DS-Backend»).""",
        c_izah="""<p><code>pwd</code> əmri «print working directory» deməkdir — hazırda
        hansı qovluqda olduğunuzu göstərir. Bu, ən çox işlədilən diaqnostika
        əmridir: nə vaxt «fayl tapılmadı» xətası görsəniz, əvvəlcə
        <code>pwd</code> yazın.</p>
        <p><code>ls -la</code> qovluğun içini göstərir. <code>-l</code> uzun
        format, <code>-a</code> isə gizli faylları da göstərir (<code>.</code>
        ilə başlayanlar). Yeni qovluqda yalnız <code>.</code> və
        <code>..</code> görünəcək — bunlar «bu qovluq» və «üst qovluq»
        deməkdir.</p>""",
        sual=[
            ("Qovluğun adını dəyişsəm nə olar?",
             "Heç nə olmaz — sadəcə hər dəfə <code>cd</code> əmrində yeni adı yazmalısınız. Amma dərs boyu eyni adı işlətmək qarışıqlığın qarşısını alır."),
            ("Layihəni başqa yerə köçürə bilərəm?",
             "Bəli. Amma o zaman bütün <code>cd</code> əmrlərindəki yolu dəyişməlisiniz. Dərslərdə <code>~/Deepseek_ARTI/DS_Backend</code> yolu işlədilir."),
            ("Node.js quraşdırılmayıbsa?",
             "<code>node -v</code> əmri «command not found» versə, nodejs.org saytından LTS versiyanı quraşdırın. Bu dərs Node 22+ tələb edir."),
        ],
        d_izah="""<p>Sistemin vəziyyəti: <strong>boş bir qovluq</strong> və işləyən
        Node.js. Bu, hələ layihə deyil — sadəcə layihənin yeri. Növbəti addımda
        bu qovluğa <code>package.json</code> əlavə edib onu həqiqi Node.js
        layihəsinə çevirəcəyik.</p>""",
    ),

    # ═══════════════════════════════════════════════════════════════
    dict(
        no=2,
        ad="package.json və asılılıqlar",
        a="""<p><code>package.json</code> layihənin <strong>şəxsiyyət
        vəsiqəsi</strong>dir. Onda üç vacib şey yazılır: layihənin adı,
        <em>hansı paketlərə ehtiyacı olduğu</em> və <em>hansı əmrləri işlədə
        bildiyi</em>.</p>
        <p><strong>Niyə paketlərə ehtiyac var?</strong> Çünki hər şeyi sıfırdan
        yazmaq aylar çəkər. NestJS bizə modul, controller, servis kimi hazır
        quruluşlar verir; Prisma bazaya sorğu göndərməyi asanlaşdırır;
        class-validator gələn məlumatı yoxlayır. Biz onları <em>istifadə
        edirik</em>, özümüz yazmırıq.</p>
        <p><strong>İki növ asılılıq var.</strong> <code>dependencies</code> —
        proqram işləyərkən lazım olan paketlər (məsələn NestJS). 
        <code>devDependencies</code> — yalnız <em>işləyərkən inkişaf
        mərhələsində</em> lazım olanlar (məsələn TypeScript kompilyatoru,
        test aləti). Server işə salınanda devDependencies yüklənmir — bu,
        yaddaşa qənaət edir.</p>
        <p><strong>Skriptlər</strong> isə qısa yollardır: <code>npm run
        build</code> yazmaq, uzun bir əmri yadda saxlamaqdan asandır.</p>""",
        anlayis=[
            ("package.json", "Layihənin manifesti — adı, asılılıqları və əmrləri."),
            ("dependencies", "Proqramın İŞLƏMƏSİ üçün lazım olan paketlər."),
            ("devDependencies", "Yalnız inkişaf/mərhələsində lazım olan paketlər (test, kompilyator)."),
            ("npm script", "package.json-da saxlanan qısa əmr. `npm run ad` ilə işlədilir."),
            ("semver", "Versiya yazılışı: `^4.4.0` = «4.4.0 və yuxarı, amma 5.0.0-dan aşağı»."),
            ("node_modules", "Quraşdırılmış paketlərin fiziki yerləşdiyi qovluq. Git-ə salınmır."),
        ],
        kod_izah="""<p><code>package.json</code>-da baxmalı olduğunuz yerlər:</p>
        <p><strong>1) <code>"type": "module"</code></strong> — layihənin müasir
        ESM (ECMAScript Modules) üsulu ilə işlədiyini bildirir. Bunun nəticəsi
        odur ki, <em>bütün import-larda fayl uzantısı <code>.js</code> yazılmalıdır</em>
        — hətta fayl <code>.ts</code> olsa belə! Bu, yeni başlayanların ən çox
        səhv saldığı qaydadır.</p>
        <p><strong>2) <code>scripts</code> bölməsi</strong> — burada
        <code>build</code> (<code>nest build</code>), <code>start:dev</code>
        (dəyişiklikləri izləyib avtomatik yenidən başladan rejim) və
        <code>start:prod</code> (yığılmış kodu işlədən rejim) var.</p>
        <p><strong>3) <code>dependencies</code></strong> — NestJS paketləri,
        Prisma müştərisi və adapteri, validasiya paketləri.</p>
        <p>⚠️ <strong>Diqqət:</strong> bu faylı əl ilə yazmaq əvəzinə adətən
        <code>npm install paket-adi</code> işlədilir və npm faylı özü
        yeniləyir. Bizim dərsdə isə fayl tam verilir ki, hər şey eyni olsun.</p>""",
        fayllar=["package.json"],
        c="""cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

echo "── Layihə haqqında ──"
python3 -c "
import json
d = json.load(open('package.json'))
print('  ad       :', d['name'])
print('  versiya  :', d['version'])
print('  modul tipi:', d.get('type', 'commonjs'))
"
echo
echo "── Skriptlər (qısa əmrlər) ──"
python3 -c "
import json
for k, v in json.load(open('package.json'))['scripts'].items():
    print('  npm run %-14s → %s' % (k, v))
"
echo
echo "── Asılılıqlar ──"
python3 -c "
import json
d = json.load(open('package.json'))
print('  İŞLƏMƏ üçün (dependencies):', len(d.get('dependencies', {})))
print('  İNKİŞAF üçün (devDependencies):', len(d.get('devDependencies', {})))
"
echo
echo "── Quraşdırıldımı? ──"
if [ -d node_modules ]; then
  echo "  ✓ node_modules var ($(ls node_modules | wc -l | tr -d ' ') paket)"
else
  echo "  ✗ node_modules yoxdur — «npm install» işlədin"
fi""",
        olmaz="""$ npm run build
npm error code ENOENT
npm error syscall open
npm error path /Users/royatalibova/Deepseek_ARTI/DS_Backend/package.json
npm error errno -2

   # ⚠️ package.json olmasa npm heç nə edə bilmir. «ENOENT» =
   # «Error NO ENTry» = fayl tapılmadı. Səbəb: ya fayl yoxdur, ya da
   # terminal səhv qovluqdadır (pwd ilə yoxlayın).

$ npm test
npm error Missing script: "test"

   # ⚠️ Skript təyin olunmasa, npm onu tapa bilmir. Ona görə
   # package.json-daki «scripts» bölməsi vacibdir.""",
        c_izah="""<p>Bu yoxlama üç suala cavab verir: <em>fayl yerindədirmi?</em>,
        <em>hansı əmrləri işlədə bilirəm?</em> və <em>paketlər
        quraşdırılıbmı?</em></p>
        <p><code>node_modules</code> qovluğu <code>npm install</code> əmrinin
        nəticəsidir. Onu əl ilə yaratmaq olmaz — həmişə npm yaradır. Bu qovluq
        çox böyük olur (yüzlərlə meqabayt), ona görə git-ə salınmır:
        <code>package.json</code> kifayətdir ki, başqa kompüterdə
        <code>npm install</code> eyni paketləri yenidən quraşdırsın.</p>""",
        sual=[
            ("`npm install` nə qədər çəkir?",
             "İlk dəfə 1-3 dəqiqə çəkə bilər, çünki paketlər internetdən yüklənir. Sonrakı dəfələr keşdən oxunduğu üçün saniyələrlə ölçülür."),
            ("`node_modules`-u silmək olar?",
             "Bəli, tam təhlükəsizdir. Sonra <code>npm install</code> işlədin və hər şey bərpa olunacaq — çünki hansı paketlərin lazım olduğu <code>package.json</code>-da yazılıb."),
            ("`^` işarəsi nə deməkdir?",
             "<code>^4.4.0</code> → «4.4.0 və ya daha yeni 4.x versiyası, amma 5.0.0 yox». Belə kiçik yenilənmələr gəlsin, amma qırıcı dəyişikliklər avtomatik gəlməsin."),
            ("`dependencies` ilə `devDependencies` fərqi nədir?",
             "İstehsalatda (production) serverdə yalnız <code>dependencies</code> quraşdırılır: <code>npm install --omit=dev</code>. Test alətləri və kompilyator orada lazım deyil."),
        ],
        d_izah="""<p>Sistemin vəziyyəti: layihə artıq <strong>həqiqi Node.js
        layihəsidir</strong>. <code>npm</code> onu tanıyır, əmrləri işlədə bilir
        və bütün lazımi paketlər <code>node_modules</code>-dadır. Amma hələ
        <em>heç bir kod yoxdur</em> — növbəti addımda TypeScript-in necə
        işləyəcəyini təyin edəcəyik.</p>""",
    ),

    # ═══════════════════════════════════════════════════════════════
    dict(
        no=3,
        ad="TypeScript konfiqurasiyası",
        a="""<p><strong>Niyə JavaScript yox, TypeScript?</strong> JavaScript-də
        dəyişənin tipi yoxdur: <code>let yas = "iyirmi"</code> yazsanız, heç kim
        sizi saxlamır. TypeScript isə deyir: «bu dəyişən ədəd olmalıdır» və
        səhvi <em>kodu işlətməzdən əvvəl</em> göstərir. Böyük layihələrdə bu,
        saatlarla vaxta qənaət edir.</p>
        <p><strong>Konfiqurasiya nə üçün iki fayldır?</strong>
        <code>tsconfig.json</code> layihənin <em>ümumi</em> qaydalarıdır — onu
        redaktor (VS Code) oxuyur və sizə kömək edir.
        <code>tsconfig.build.json</code> isə yalnız <em>yığım</em> (build)
        üçündür və test fayllarını kənarda qoyur. Belə ki test faylları
        istehsalat koduna düşmür.</p>
        <p>⚠️ <strong>Ən vacib üç ayar:</strong></p>
        <p><code>experimentalDecorators: true</code> — NestJS
        <code>@Controller()</code>, <code>@Injectable()</code> kimi işarələri
        işlədir. Bu ayar sönsə, heç bir modul işləməz.</p>
        <p><code>emitDecoratorMetadata: true</code> — NestJS-in asılılıqları
        <em>avtomatik</em> tapması üçün lazımdır. Bu olmasa, hər servisi əl ilə
        bağlamaq lazım gələrdi.</p>
        <p><code>module: "nodenext"</code> — müasir modul sistemi. Bunun
        nəticəsi: import-larda <code>.js</code> uzantısı mütləqdir.</p>""",
        anlayis=[
            ("TypeScript", "JavaScript + tiplər. Kod yazarkən səhvləri tutur, sonra adi JavaScript-ə çevrilir."),
            ("transpile / compile", "TypeScript kodunu brauzerin/serverin başa düşdüyü JavaScript-ə çevirmək."),
            ("decorator", "Kodun üzərinə yazılan `@İşarə` — sinfə və ya metoda əlavə məlumat verir."),
            ("metadata", "Kod haqqında «kodun özü» — NestJS bundan istifadə edib asılılıqları tapır."),
            ("strict", "TypeScript-in ən sərt yoxlama rejimi. Səhvləri erkən tutur."),
            ("target", "Hansı JavaScript versiyasına çevrilsin (məsələn ES2023)."),
            ("NodeNext", "Node.js-in müasir modul qaydası: import-da `.js` uzantısı tələb edir."),
        ],
        kod_izah="""<p><strong><code>tsconfig.json</code> — ümumi qaydalar.</strong>
        <code>strict: true</code> bütün sərt yoxlamaları açır. Öyrənmə
        mərhələsində bu, əvvəlcə çətin görünür, amma sizi çox səhvdən qoruyur.</p>
        <p><code>moduleResolution: "nodenext"</code> ilə birlikdə
        <code>module: "nodenext"</code> işlədilir — bu ikisi
        <em>cütlükdür</em>, biri olmadan digəri işləmir.</p>
        <p><strong><code>tsconfig.build.json</code> — yalnız yığım
        üçün.</strong> <code>extends</code> sözü «yuxarıdaki fayldan miras al»
        deməkdir. Sonra <code>exclude</code> ilə test qovluğunu kənarlaşdırır.
        Beləliklə <code>npm run build</code> yalnız istehsalat kodunu yığır.</p>
        <p><strong><code>nest-cli.json</code> — NestJS-in öz ayarları.</strong>
        <code>sourceRoot: "src"</code> kodu haradan götürsün, <code>deleteOutDir:
        true</code> isə hər yığımdan əvvəl köhnə <code>dist</code> qovluğunu
        təmizləsin. Bu olmasa, silinmiş faylların köhnə nüsxələri
        <code>dist</code>-də qalıb çaşqınlıq yaradardı.</p>
        <p>⚠️ <strong>Nə üçün <code>.js</code> uzantısı?</strong> Fayl
        <code>src/main.ts</code> olsa da, import belə yazılır:
        <code>import ... from './app.module.js'</code>. Səbəb: Node.js yığılmış
        JavaScript fayllarını işlədəcək və orada uzantı <code>.js</code>-dir.
        Bu qayda pozulsa, <code>ERR_MODULE_NOT_FOUND</code> xətası alırsınız.</p>""",
        fayllar=["tsconfig.json", "tsconfig.build.json", "nest-cli.json"],
        c="""cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

echo "── TypeScript-in gördüyü YEKUN ayarlar ──"
npx tsc --showConfig 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)['compilerOptions']
for a in ['target','module','moduleResolution','strict',
          'experimentalDecorators','emitDecoratorMetadata',
          'outDir','rootDir','esModuleInterop','skipLibCheck']:
    print('  %-24s %s' % (a, d.get(a, '—')))
"
echo
echo "── NestJS ayarları ──"
python3 -c "
import json
d = json.load(open('nest-cli.json'))
c = d.get('compilerOptions', {})
print('  sourceRoot     :', d.get('sourceRoot'))
print('  deleteOutDir   :', c.get('deleteOutDir'))
print('  collection     :', d.get('collection'))
"
echo
echo "── Yığım nəyi KƏNARDA qoyur? ──"
python3 -c "
import json
print('  exclude:', json.load(open('tsconfig.build.json')).get('exclude'))
\"""",
        olmaz="""$ npm run build
src/main.ts:1:1 - error TS1219: Experimental support for decorators is a
feature that is subject to change in a future release. Set the
'experimentalDecorators' option in your 'tsconfig' or 'jsconfig' to
remove this warning.

src/app.module.ts:5:1 - error TS1206: Decorators are not valid here.

   # ⚠️ «experimentalDecorators» olmasa NestJS-in @İşarə-ləri TANINMIR.
   # Nəticə: heç bir modul, controller, servis işləmir — build sınır.

$ npm run start:prod
Error [ERR_MODULE_NOT_FOUND]: Cannot find module '/.../dist/app.module.js'
imported from /.../dist/main.js

   # ⚠️ Import-da «.js» uzantısı unudulsa, Node faylı tapa bilmir.
   # TypeScript xəbərdarlıq vermir, amma işləyəndə sınır — ona görə
   # bu qayda əzbərlənməlidir.""",
        c_izah="""<p><code>npx tsc --showConfig</code> əmri TypeScript-in
        <em>həqiqətən</em> işlətdiyi ayarları göstərir — miras alınanlar da
        daxil. Bu, «faylda yazdım, amma işləmirsə» hallarını tapmaq üçün əla
        üsuldur.</p>
        <p>Diqqət yetirin: <code>tsconfig.json</code>-da <code>strict</code>
        yazılıb, amma <code>--showConfig</code> onu <code>true</code> kimi
        göstərir. Çünki <code>strict</code> aslında bir qrup ayarın qısa
        yazılışıdır.</p>
        <p><code>deleteOutDir: true</code> xüsusilə vacibdir: hər yığımdan
        əvvəl <code>dist</code> silinir. Bu olmasa, köhnə fayllar qalır və
        «dəyişikliyim niyə təsir etmir?» sualı yaranır.</p>""",
        sual=[
            ("`.ts` faylı niyə `.js` kimi import olunur?",
             "Çünki işləyən kod TypeScript deyil, yığılmış JavaScript-dir. Node.js <code>dist/app.module.js</code> faylını axtarır. Bu, «NodeNext» modul sisteminin qaydasıdır."),
            ("`strict: false` etsəm nə olar?",
             "Build asan keçər, amma <code>null</code> və <code>undefined</code> ilə bağlı səhvlər yalnız işləyəndə görünər — o zaman tapmaq çox çətindir. Öyrənmə mərhələsində sərt saxlamaq daha faydalıdır."),
            ("`dist` nədir?",
             "Yığılmış JavaScript kodunun qovluğu. Siz <code>src</code>-də TypeScript yazırsınız, <code>npm run build</code> isə onu <code>dist</code>-ə çevirir. Server <code>dist/main.js</code>-i işlədir."),
            ("Redaktorum niyə xəta göstərmir, amma terminal göstərir?",
             "Redaktor <code>tsconfig.json</code>-u, terminal isə <code>npm run build</code> vasitəsilə <code>tsconfig.build.json</code>-u işlədir. İkisi fərqli ayar işlədə bilər."),
        ],
        d_izah="""<p>Sistemin vəziyyəti: layihə artıq <strong>TypeScript
        layihəsidir</strong>. Kompilyator decorator-ları tanıyır, sərt tip
        yoxlaması açıqdır və yığım qaydaları ayrılmışdır. Hələ kod yoxdur,
        amma kod yazmaq üçün bütün şərait hazırdır.</p>""",
    ),

    # ═══════════════════════════════════════════════════════════════
    dict(
        no=4,
        ad=".env — baza açarı koddan ayrılır",
        a="""<p><strong>Ən çox edilən təhlükəsizlik səhvi:</strong> baza şifrəsini
        koda yazmaq. <code>const sifre = "arti_secret_2025"</code> — bu sətir
        git-ə düşəndə şifrə <em>əbədi olaraq</em> tarixçədə qalır. Kodu silmək
        kifayət etmir, çünki köhnə commit-lərdə qalır.</p>
        <p><strong>Həll: mühit dəyişənləri.</strong> Şifrə koddan çıxarılıb
        <code>.env</code> faylına salınır, kod isə onu <em>adı ilə</em>
        oxuyur: «<code>DATABASE_URL</code> nədir?» Kod heç vaxt şifrənin özünü
        bilmir. Beləliklə eyni kod həm kompüterinizdə, həm serverdə işləyir —
        sadəcə <code>.env</code> faylı fərqli olur.</p>
        <p>⚠️ <strong><code>.env</code> git-ə salınmamalıdır.</strong> Bunun
        üçün <code>.gitignore</code> faylı var. Əvəzində
        <code>.env.example</code> saxlanılır — orada şifrə yerinə nümunə olur.
        Yeni işçi layihəni götürəndə <code>.env.example</code>-i kopyalayıb öz
        şifrəsini yazır.</p>""",
        anlayis=[
            ("Mühit dəyişəni (env var)", "Əməliyyat sisteminin koda verdiyi adlı dəyər. `DATABASE_URL`, `PORT` kimi."),
            (".env", "Mühit dəyişənlərinin faylda saxlandığı yer. Git-ə salınmır."),
            (".env.example", "Şifrəsiz NÜMUNƏ faylı — git-ə salınır ki, hansı dəyişənlər lazım olduğu bilinsin."),
            (".gitignore", "Git-in NƏZƏRƏ ALMAYACAĞI faylların siyahısı."),
            ("DATABASE_URL", "Baza ünvanı: `postgresql://istifadeci:sifre@host:port/baza_adi`."),
            ("sirr (secret)", "Açıqlanmamalı olan məlumat — şifrə, API açarı, token imza açarı."),
        ],
        kod_izah="""<p><strong><code>.env</code> faylının quruluşu:</strong>
        <code>AD="dəyər"</code>. Dırnaqlar məcburi deyil, amma dəyərdə xüsusi
        işarə varsa (məsələn <code>#</code>) mütləqdir.</p>
        <p><code>DATABASE_URL</code>-i hissələrə ayıraq:
        <code>postgresql://</code> — protokol;
        <code>arti_user:arti_secret_2025</code> — istifadəçi adı və şifrə;
        <code>@localhost:5432</code> — server ünvanı və port;
        <code>/arti_baza</code> — baza adı.</p>
        <p><strong><code>.gitignore</code>-da nə var?</strong>
        <code>node_modules/</code> (çox böyükdür),
        <code>.env</code> (şifrə var),
        <code>dist/</code> (yığılmış kod — yenidən yığıla bilər),
        <code>src/generated/</code> (Prisma özü yaradır).</p>
        <p>⚠️ <strong>Terminalda <code>DATABASE_URL</code> artıq təyin
        olunubsa?</strong> O zaman <code>.env</code>-dəki dəyər <em>üstələnir</em>
        — çünki mövcud mühit dəyişəni fayldan üstündür. Bu, çaşqınlıq yaradır.
        Ona görə dərslərdə hər dəfə <code>unset DATABASE_URL PGHOST</code>
        işlədilir: «əvvəl təmizlə, sonra fayldan oxu».</p>""",
        fayllar=[".env.example", ".gitignore"],
        c="""cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── .env faylı (şifrə GİZLƏDİLİR) ──"
python3 -c "
import re, pathlib
for x in pathlib.Path('.env').read_text().splitlines():
    if not x.strip() or x.startswith('#'):
        continue
    a, _, d = x.partition('=')
    d = d.strip('\\\"')
    if 'SIFRE' in a or 'SECRET' in a or 'PASSWORD' in a or 'URL' in a:
        print('  %-18s %s  (dəyər gizlədilib)' % (a, '•' * 24))
    else:
        print('  %-18s %s' % (a, d))
"
echo
echo "── DATABASE_URL hissələri ──"
python3 -c "
import re, pathlib
m = re.search(r'DATABASE_URL=\\\"([^\\\"]+)\\\"', pathlib.Path('.env').read_text())
u = m.group(1)
sxem, _, qalan = u.partition('://')
kimlik, _, host = qalan.partition('@')
ist, _, sifre = kimlik.partition(':')
host, _, baza = host.partition('/')
print('  protokol :', sxem)
print('  istifadəçi:', ist)
print('  şifrə    :', '•' * len(sifre), '(%d simvol)' % len(sifre))
print('  host:port:', host)
print('  baza adı :', baza)
"
echo
echo "── Git nəyi NƏZƏRƏ ALMIR? ──"
grep -v '^#' .gitignore | grep -v '^$' | sed 's/^/  /'
echo
echo "── .env həqiqətən qorunurmu? ──"
git -C ~/Deepseek_ARTI check-ignore -v DS_Backend/.env 2>/dev/null \
  || echo "  (layihə hələ git-də deyil)"
""",
        olmaz="""$ git add -A && git commit -m "ilk versiya"
$ git log --oneline
a1b2c3d ilk versiya

   # ⚠️ .gitignore olmasaydı, .env də git-ə düşərdi. Şifrə artıq
   # tarixçədədir — kodu silsəniz də qalır, çünki köhnə commit
   # dəyişməzdir. Şifrəni dəyişməkdən başqa çıxış yolu qalmır.

$ cat src/prisma/prisma.service.ts
const url = 'postgresql://arti_user:arti_secret_2025@localhost:5432/arti_baza';

   # ⚠️ Şifrə koda yazılsa, kodu görən HƏR KƏS bazaya girə bilər.
   # Həm də eyni kodu başqa kompüterdə işlətmək mümkün olmaz:
   # hər yerdə şifrəni əl ilə dəyişmək lazım gələrdi.""",
        c_izah="""<p>Bu yoxlamanın ən mühüm hissəsi <strong>şifrənin heç vaxt
        ekrana çıxmamasıdır</strong>. Diqqət yetirin: skript şifrəni
        <code>•</code> ilə göstərir. Bu, sadəcə nəzakət deyil — ekran
        görüntüləri, ekran yazıları və terminal tarixçəsi tez-tez paylaşılır.
        Şifrə orada görünsə, sızır.</p>
        <p><code>git check-ignore</code> əmri «bu fayl git tərəfindən
        sayılırmı?» sualına cavab verir. Əgər fayl sayılırsa (ignore
        olunmursa), <code>git add</code> onu götürəcək — bu təhlükə işarəsidir.</p>""",
        sual=[
            ("`.env`-i başqa kompüterə necə köçürüm?",
             "Köçürməyin! <code>.env.example</code>-i kopyalayın, yeni kompüterdə <code>.env</code> adı ilə saxlayın və öz şifrənizi yazın. Şifrələr heç vaxt kodla birlikdə daşınmır."),
            ("Şifrəni dəyişmək istəsəm?",
             "Yalnız <code>.env</code> faylını dəyişin — kodda heç nə dəyişmir. Bu, mühit dəyişənlərinin əsas üstünlüyüdür."),
            ("`unset DATABASE_URL` nə üçün lazımdır?",
             "Əgər terminalda köhnə bir <code>DATABASE_URL</code> qalıbsa, o, <code>.env</code>-dəki dəyəri üstələyir və siz səhv bazaya qoşulursunuz. <code>unset</code> köhnə dəyəri silir."),
            ("`.env` faylı varsa, `dotenv` paketi nə edir?",
             "Faylı oxuyub mühit dəyişənlərinə çevirir. Node.js özü <code>.env</code> faylını tanımır — paket vasitəsilə oxunur."),
        ],
        d_izah="""<p>Sistemin vəziyyəti: <strong>şifrələr koddan ayrılıb</strong>
        və git-dən qorunur. Bu andan etibarən kod yaza bilərik — heç bir yerdə
        şifrə yazmayacağıq, sadəcə <code>process.env.DATABASE_URL</code>
        deyəcəyik.</p>""",
    ),

    # ═══════════════════════════════════════════════════════════════
    dict(
        no=5,
        ad="Prisma sxeması — bazanı oxuyub tipləri çıxarmaq",
        a="""<p>Bazamız artıq mövcuddur: 48 cədvəl, 12 sxem, minlərlə sütun.
        <strong>Onu TypeScript-ə necə tanıdacağıq?</strong> Hər cədvəl üçün əl
        ilə tip yazmaq həftələr çəkər və hər dəyişiklikdə yenidən yazmaq
        lazım gələrdi.</p>
        <p>Burada <strong>Prisma</strong> köməyə gəlir. Prisma bir
        <em>ORM</em>-dir (Object-Relational Mapping): cədvəlləri TypeScript
        obyektlərinə çevirir. <code>prisma db pull</code> əmri bazaya qoşulur,
        bütün cədvəlləri oxuyur və onların təsvirini
        <code>schema.prisma</code> faylına yazır. Sonra
        <code>prisma generate</code> həmin təsvirdən TypeScript tiplərini
        yaradır.</p>
        <p><strong>Nəticə:</strong> redaktorunuz <code>emekdaslar</code>
        cədvəlinin hansı sütunları olduğunu <em>bilir</em>. Səhv sütun adı
        yazsanız, dərhal xəbərdarlıq alırsınız — bazaya sorğu göndərməzdən
        əvvəl.</p>""",
        anlayis=[
            ("ORM", "Object-Relational Mapping — cədvəlləri obyekt kimi işlətməyə imkan verən qat."),
            ("Prisma", "TypeScript üçün müasir ORM. Sxemadan tipləri avtomatik yaradır."),
            ("introspection (db pull)", "Bazanı oxuyub sxem faylını AVTOMATİK yazmaq."),
            ("generator", "Sxemadan kod (TypeScript tipləri) yaradan hissə."),
            ("datasource", "Bazaya necə qoşulacağını bildirən hissə."),
            ("sxem (schema)", "PostgreSQL-də cədvəllərin qrupu: `kadrlar`, `struktur`, `tehsil`."),
            ("prisma.config.ts", "Prisma 7-də ayarlar faylı — baza ünvanı buradan verilir."),
        ],
        kod_izah="""<p><strong>Başlanğıc sxem yalnız iki blokdan ibarətdir:</strong></p>
        <p><code>generator client</code> — hansı kod yaradılsın və hara
        yazılsın. <code>output = "../src/generated/prisma"</code> deməkdə
        məqsəd: yaradılan kod <code>node_modules</code>-da deyil, layihənin
        içində olsun ki, redaktor onu görsün.</p>
        <p><code>datasource db</code> — hansı bazaya qoşulacaq və hansı sxemlər
        oxunacaq.</p>
        <p>⚠️⚠️ <strong>Ən çox edilən səhv:</strong>
        <code>schemas = [...]</code> sətri <em>bir sətirdə</em> olmalıdır.
        Sətri bölsəniz Prisma belə xəta verir:</p>
        <p><code>P1012: This line is not a valid definition within a
        datasource.</code></p>
        <p>⚠️ <strong>İkinci səhv:</strong> <code>url</code> sahəsini sxemaya
        yazmaq. Prisma 7-də baza ünvanı artıq
        <code>prisma.config.ts</code>-də verilir, sxemada yox.</p>
        <p><strong><code>prisma.config.ts</code>:</strong>
        <code>import 'dotenv/config'</code> sətri <code>.env</code> faylını
        oxuyur — bu olmasa <code>DATABASE_URL</code> tapılmır və
        <code>db pull</code> «datasource.url required» xətası verir.</p>""",
        fayllar=["prisma/schema.prisma", "prisma.config.ts"],
        c="""cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── Sxemanın əsas blokları ──"
grep -nE '^(generator|datasource)|^  (provider|output|url|schemas)' prisma/schema.prisma | head -8
echo
echo "── Bazadan nə oxundu? ──"
echo "  model sayı : $(grep -c '^model ' prisma/schema.prisma)"
echo "  @@schema   : $(python3 -c "
import re
s = open('prisma/schema.prisma').read()
print(len(re.findall(r'@@schema', s)))")"
echo "  sətir sayı : $(wc -l < prisma/schema.prisma | tr -d ' ')"
echo
echo "── İlk model nümunə ──"
sed -n '/^model merkezler /,/^}/p' prisma/schema.prisma | head -14 | sed 's/^/  /'
echo
echo "── Sxemanın etibarlılığı ──"
npx prisma validate 2>&1 | tail -2 | sed 's/^/  /'
echo
echo "── Yaradılan klient ──"
echo "  src/generated/prisma: $(ls src/generated/prisma 2>/dev/null | wc -l | tr -d ' ') fayl"
[ -f src/generated/prisma/client.ts ] && echo "  ✓ client.ts var" || echo "  ✗ client.ts YOXDUR\"""",
        olmaz="""$ npx prisma db pull
Error: P1012

error: Error validating: This line is not a valid definition within a datasource.
  -->  prisma/schema.prisma:8
   |
 8 |     "ai", "audit", "elm",
   |     ^^^^^^^^^^^^^^^^^^^^^

   # ⚠️ «schemas» sətri BÖLÜNMÜŞDÜR. Prisma onu bir sətir gözləyir.
   # Düzgün: schemas = ["ai", "audit", "elm", "kadrlar", ...]

$ npx prisma db pull
Error: The datasource.url property is required in your Prisma config
file when using prisma db pull.

   # ⚠️ prisma.config.ts yoxdur, ya da adı səhvdir (məsələn
   # «prisma.config.ts.txt»), ya da içində dotenv import edilməyib.
   # Prisma .env faylını ÖZÜ oxumur — onu kiminsə oxuması lazımdır.

$ npm run build
src/prisma/prisma.service.ts:3:10 - error TS2307: Cannot find module
'../generated/prisma/client.js'

   # ⚠️ «prisma generate» işlədilməmişdir → tiplər yoxdur → import
   # tapılmır. Hər «db pull»-dan sonra «generate» də işlədilməlidir.""",
        c_izah="""<p>Bu yoxlama üç suala cavab verir: <em>sxemada düzgün bloklar
        varmı?</em>, <em>bazadan nə qədər cədvəl oxundu?</em> və <em>TypeScript
        tipləri yaradıldımı?</em></p>
        <p>48 model gözlənilir — bu, bazamızdaki cədvəl sayıdır. Əgər sayı
        daha azdırsa, <code>schemas</code> siyahısından bəzi sxemlər düşüb.</p>
        <p><code>prisma validate</code> əmri <em>qoşulmadan</em> sxemi yoxlayır
        — sürətli diaqnostika üçün idealdır.</p>""",
        sual=[
            ("`db pull` bazanı dəyişirmi?",
             "Xeyr. O, yalnız <em>oxuyur</em>. Bazada heç nə yaradılmır, dəyişdirilmir və silinmir. Tam təhlükəsizdir."),
            ("Baza dəyişsə nə olar?",
             "Yenidən <code>npx prisma db pull</code> və <code>npx prisma generate</code> işlədin. Tiplər yenilənəcək."),
            ("`schema.prisma` da git-ə salınmalıdırmı?",
             "Bəli, mütləq. Bu fayl kodun bir hissəsidir. Yalnız <code>src/generated/</code> salınmır, çünki onu hər kəs özü yarada bilər."),
            ("48 modeli əl ilə yazmaq lazımdırmı?",
             "Xeyr — <code>db pull</code> hamısını avtomatik yazır. Siz sadəcə generator və datasource bloklarını əvvəlcədən yaradırsınız."),
        ],
        d_izah="""<p>Sistemin vəziyyəti: <strong>baza artıq TypeScript üçün
        tanışdır</strong>. 48 cədvəl, 12 sxem tiplər kimi mövcuddur. Hələ
        bazaya sorğu göndərə bilmirik — bunun üçün bağlantı qurmalıyıq.
        Növbəti addım məhz budur.</p>""",
    ),

    # ═══════════════════════════════════════════════════════════════
    dict(
        no=6,
        ad="PrismaService — baza bağlantısı",
        a="""<p>Hər HTTP sorğusu üçün yeni baza bağlantısı açsaq, sistem çox
        tez boğular. Baza serveri bağlantı sayını məhdudlaşdırır (adətən
        100 civarı). Ona görə <strong>bağlantı bir dəfə açılır və hamı onu
        paylaşır</strong>.</p>
        <p><code>PrismaService</code> məhz bunun üçündür: NestJS işə
        düşəndə bir dəfə qoşulur (<code>onModuleInit</code>), proqram
        bağlananda düzgün bağlanır (<code>onModuleDestroy</code>), bütün
        servislər isə <em>eyni</em> bağlantıdan istifadə edir.</p>
        <p>⚠️ <strong>Prisma 7-də vacib dəyişiklik:</strong> sadəcə
        <code>new PrismaClient()</code> yazmaq kifayət etmir. Baza sürücüsü
        (adapter) <em>açıq şəkildə</em> verilməlidir:
        <code>new PrismaPg({ connectionString })</code>. Bu olmasa,
        <code>PrismaClientInitializationError</code> alırsınız.</p>""",
        anlayis=[
            ("Service", "NestJS-də iş məntiqini saxlayan sinif. `@Injectable()` ilə işarələnir."),
            ("Dependency Injection", "«Mənə lazım olan şeyi özün ver» prinsipi. NestJS konstruktordan oxuyur."),
            ("onModuleInit", "NestJS-in modul işə düşəndə çağırdığı xüsusi metod."),
            ("Adapter", "Prisma ilə baza sürücüsü (pg) arasındaki körpü. Prisma 7-də məcburidir."),
            ("connection pool", "Bağlantıların hovuzu — açılıb-saxlanılan bağlantılar toplusu."),
            ("Singleton", "Tək nüsxə — bütün proqram boyu bir obyekt."),
        ],
        kod_izah="""<p><code>@Injectable()</code> işarəsi NestJS-ə deyir: «bu sinfi
        özün yarada bilərsən». Bu olmasa, NestJS onu tanımır.</p>
        <p><code>constructor(config: ConfigService)</code> — DI nümunəsi.
        NestJS <code>ConfigService</code>-i özü yaradıb verir; biz
        <code>new ConfigService()</code> yazmırıq.</p>
        <p><code>config.get&lt;string&gt;('DATABASE_URL')</code> —
        <code>.env</code>-dən dəyəri adı ilə oxuyur. Dəyər yoxdursa, aydın
        xəta mesajı verilir ki, «niyə işləmir?» sualı yaranmasın.</p>
        <p><code>new PrismaPg({ connectionString })</code> — baza sürücüsünü
        Prisma-ya tanıdır. Sonra <code>super({ adapter })</code> ilə
        <code>PrismaClient</code>-ə verilir.</p>
        <p><code>onModuleInit()</code> — NestJS işə düşəndə <em>bir dəfə</em>
        çağırılır. Burada <code>$connect()</code> edilir. Niyə? Çünki ilk
        sorğuda qoşulmaq istifadəçiyə gecikmə kimi hiss olunardı.</p>
        <p><code>yoxla()</code> metodu — sistemin <em>canlı olub-olmadığını</em>
        yoxlayır. Sadəcə «işləyirəm» demir, bazaya həqiqi sorğu göndərir və
        cavabı ölçür. Sağlamlıq endpointi bunu işlədəcək.</p>""",
        fayllar=["src/prisma/prisma.service.ts"],
        c="""cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

echo "── Fayl yerindədirmi? ──"
ls -l src/prisma/prisma.service.ts
echo
echo "── Baza bağlantısını BİRBAŞA yoxlayaq ──"
npx tsx -e "
import 'dotenv/config';
import { PrismaService } from './src/prisma/prisma.service.ts';
void (async () => {
  const s = new PrismaService({ get: () => process.env.DATABASE_URL } as never);
  await s.onModuleInit();
  const n = await s.yoxla();
  console.log('  bağlantı   : quruldu');
  console.log('  cədvəl sayı:', n.cedvelSayi);
  console.log('  gecikmə    :', n.gecikmeMs, 'ms');
  await s.onModuleDestroy();
  console.log('  bağlantı bağlandı');
})();
\"""",
        olmaz="""$ npx tsx -e "import { PrismaService } from './src/prisma/prisma.service.ts'; ..."
Error: PrismaClientInitializationError:
Prisma Client could not be constructed.
Driver adapter not found.

   # ⚠️ «adapter» verilməyibsə Prisma 7 işləmir. Bu, Prisma 6-dan
   # keçəndə ən çox rastlanan xətadır: köhnə dərsliklərdə
   # «new PrismaClient()» yazılır, amma 7-də bu kifayət etmir.

$ npm run start:prod
Error: DATABASE_URL təyin olunmayıb — .env faylını yoxlayın

   # ⚠️ Bu, BİZİM yazdığımız aydın xəta mesajıdır. Olmasaydı Prisma
   # anlaşılmaz bir xəta verərdi və siz saatlarla səbəb axtarardınız.""",
        c_izah="""<p>Bu yoxlama serveri qaldırmadan <strong>birbaşa baza
        bağlantısını</strong> sınayır. Bu çox faydalı texnikadır: problem
        serverdədir, yoxsa bazadadır — dərhal bilirsiniz.</p>
        <p><code>npx tsx -e "..."</code> əmri TypeScript faylını birbaşa
        işlədir (yığım tələb etmir). Diqqət: import-da
        <code>.ts</code> uzantısı yazılır — çünki bu, yığılmış kod deyil,
        birbaşa TypeScript-dir. Layihə fayllarının <em>içində</em> isə
        <code>.js</code> yazılır.</p>
        <p><code>{ get: () => process.env.DATABASE_URL }</code> —
        <code>ConfigService</code>-in yerinə sadə bir saxta obyekt veririk.
        Beləliklə NestJS-i işə salmadan servisi sınaya bilirik.</p>""",
        sual=[
            ("`onModuleInit` nə vaxt çağırılır?",
             "NestJS tətbiqi işə düşəndə, yəni server qalxarkən BİR DƏFƏ. Hər sorğuda deyil."),
            ("Bağlantı kəsilərsə nə olar?",
             "Prisma özü yenidən qoşulmağa çalışır. <code>yoxla()</code> metodu bu halı <code>qosulub: false</code> kimi göstərir."),
            ("`$disconnect()` nə vaxt lazımdır?",
             "Proqram bağlananda. Ona görə <code>onModuleDestroy</code> metodunda çağırılır — əks halda bağlantılar açıq qalar."),
            ("Nə üçün bağlantı bir dənədir?",
             "Hər sorğuda yeni bağlantı açmaq 100-200 ms çəkir və baza serverini boğur. Bir bağlantı paylaşılarsa, sistem sürətli və sabit işləyir."),
        ],
        d_izah="""<p>Sistemin vəziyyəti: <strong>TypeScript kodu bazaya
        qoşula bilir</strong>. Bu, çox vacib mərhələdir — artıq «kod» ilə
        «məlumat» arasında körpü var. Amma bu servisi hər modulda ayrıca
        import etmək yorucudur; növbəti addımda onu hamıya açacağıq.</p>""",
    ),

    # ═══════════════════════════════════════════════════════════════
    dict(
        no=7,
        ad="PrismaModule — @Global() ilə paylaşılan bağlantı",
        a="""<p>Təsəvvür edin: layihədə 20 servis var və hamısı bazaya
        müraciət edir. Hər birinin <code>imports</code> siyahısına
        <code>PrismaModule</code> yazmaq həm yorucu, həm də səhvə açıqdır —
        biri unudulsa, həmin servis işləmir.</p>
        <p><code>@Global()</code> işarəsi bu problemi həll edir: modul
        <strong>bir dəfə</strong> kök modula qoşulur və bundan sonra
        <em>bütün</em> layihə boyu əlçatan olur. Eynilə evdəki elektrik
        xətti kimi: hər otaq üçün ayrıca generator qurmaq lazım deyil.</p>
        <p>⚠️ <strong>Diqqət:</strong> hər şeyi <code>@Global()</code> etmək
        yaxşı fikir deyil. Yalnız həqiqətən hər yerdə lazım olan şeylər
        (baza bağlantısı, konfiqurasiya) qlobal olmalıdır. Əks halda kodun
        asılılıqları görünməz olur və «bu haradan gəldi?» sualı yaranır.</p>""",
        anlayis=[
            ("Module", "NestJS-də əlaqəli hissələri bir yerə yığan qutu."),
            ("@Global()", "Modulu bütün layihə üçün əlçatan edən işarə."),
            ("imports", "Modulun istifadə etdiyi başqa modullar."),
            ("providers", "Modulun yaratdığı servislər."),
            ("exports", "Modulun BAŞQALARINA verdiyi servislər."),
        ],
        kod_izah="""<p><code>@Global()</code> — bu modulu qlobal edir. Diqqət
        yetirin: bu işarə <em>yalnız</em> kök modula qoşulan modullar üçün
        işləyir.</p>
        <p><code>providers: [PrismaService]</code> — NestJS bu sinfi yaradır
        və tək nüsxə kimi saxlayır.</p>
        <p><code>exports: [PrismaService]</code> — bu sətir olmasa, başqa
        modullar <code>PrismaService</code>-i <em>görə bilməz</em>. Bu, ən çox
        unudulan sətirdir: modul qlobaldır, amma servis ixrac olunmayıb.
        Nəticə: <code>Nest can't resolve dependencies of ...</code> xətası.</p>""",
        fayllar=["src/prisma/prisma.module.ts"],
        c="""cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

echo "── Modulun məzmunu ──"
cat src/prisma/prisma.module.ts | sed 's/^/  /'
echo
echo "── @Global() varmı? ──"
grep -n '@Global\\|exports' src/prisma/prisma.module.ts | sed 's/^/  /'
echo
echo "── Kök modul bu modulu qoşubmu? ──"
grep -n 'PrismaModule' src/app.module.ts 2>/dev/null | sed 's/^/  /' || echo "  (app.module.ts hələ yoxdur — addım 10-da yaradılacaq)\"""",
        olmaz="""$ npm run start:prod
Error: Nest can't resolve dependencies of the SaglamliqService (?).
Please make sure that the argument PrismaService at index [0] is
available in the SaglamliqModule context.

   # ⚠️ Bu xəta «exports: [PrismaService]» sətri unudulanda çıxır:
   # modul qlobaldır, amma servis başqalarına verilmir.

$ npm run start:prod
Error: Nest can't resolve dependencies of the SaglamliqService (?).

   # ⚠️ «@Global()» olmasa və SaglamliqModule-un «imports» siyahısına
   # PrismaModule yazılmasa, eyni xəta çıxır. Hər modulda təkrar
   # yazmaq lazım gələrdi — @Global() bu təkrarı aradan qaldırır.""",
        c_izah="""<p>Bu yoxlama modulun həm <code>@Global()</code> işarəsini,
        həm də <code>exports</code> sətrini yoxlayır. İkisi birlikdə
        olmalıdır — biri digərini əvəz etmir.</p>
        <p>Sonuncu yoxlama göstərir ki, <code>app.module.ts</code> hələ
        yoxdur. Bu normaldır: kök modul 10-cu addımda yaradılacaq. O vaxta
        qədər modul «asılı» vəziyyətdədir — fayl var, amma heç kim onu
        işlətmir.</p>""",
        sual=[
            ("`@Global()` nə üçün lazımdır, onsuz da işləyir?",
             "İşləyir, amma hər modulda <code>imports: [PrismaModule]</code> yazmalısınız. 20 modulda 20 dəfə. Biri unudulsa, xəta yaranır."),
            ("`exports` ilə `providers` fərqi nədir?",
             "<code>providers</code> servisi modulun İÇİNDƏ yaradır. <code>exports</code> isə onu BAŞQA modullara verir. Yalnız providers yazsanız, servis modulun içində qalır."),
            ("Nə üçün konfiqurasiya da qlobal edilmir?",
             "Edilir — <code>ConfigModule.forRoot({ isGlobal: true })</code> ilə. Bu, növbəti addımlarda görünəcək."),
        ],
        d_izah="""<p>Sistemin vəziyyəti: <strong>baza bağlantısı bütün layihəyə
        açıqdır</strong>. İstənilən modul <code>PrismaService</code>-i
        konstruktorunda istəyə bilər və NestJS onu avtomatik verəcək. Hələ
        heç bir endpoint yoxdur — növbəti addımda xətaları vahid formata
        salacağıq.</p>""",
    ),

    # ═══════════════════════════════════════════════════════════════
    dict(
        no=8,
        ad="AllExceptionsFilter — vahid xəta formatı",
        a="""<p>Xəta həmişə olacaq: istifadəçi yanlış məlumat göndərəcək, baza
        cavab verməyəcək, kodda səhv olacaq. <strong>Sual budur: xəta necə
        görünməlidir?</strong></p>
        <p>NestJS-in standart cavabı <code>{ statusCode, message, error }</code>
        formasındadır. Amma bu format <em>hər yerdə eyni deyil</em>: bəzən
        <code>message</code> sətir, bəzən massiv olur. Frontend developer isə
        hər dəfə «bu dəfə hansı format gəldi?» deyə yoxlamağa məcbur qalır.</p>
        <p><strong>Həllimiz:</strong> bütün xətaları <em>tək</em> formata
        salırıq:</p>
        <p><code>{ ugur: false, xeta: { kod, mesaj, detallar? }, yol, vaxt }</code></p>
        <p><code>kod</code> sahəsi maşın üçündür (<code>TAPILMADI</code>,
        <code>ICAZE_YOXDUR</code>) — proqram onu yoxlayır. <code>mesaj</code>
        isə insan üçündür. Bu ayrılıq çox vacibdir: mesajı dəyişsəniz, proqram
        sınmır.</p>""",
        anlayis=[
            ("Exception Filter", "Xəta baş verəndə cavabı formalaşdıran xüsusi sinif."),
            ("@Catch()", "«BÜTÜN xəta növlərini tut» işarəsi."),
            ("HttpException", "NestJS-in bilinen HTTP xətası (404, 400, 403...)."),
            ("status kod", "HTTP cavab kodu: 200 uğurlu, 400 yanlış sorğu, 404 tapılmadı, 500 server xətası."),
            ("xəta kodu", "Proqramın yoxladığı sabit ad: `TAPILMADI`, `ICAZE_YOXDUR`."),
            ("detallar", "Validasiya xətalarının siyahısı — hansı sahə nə üçün yanlışdır."),
        ],
        kod_izah="""<p><code>KOD_XERITESI</code> — status kodunu oxunaqlı ada
        çevirir. Niyə? Çünki <code>if (xeta.kod === 'ICAZE_YOXDUR')</code>
        yazmaq, <code>if (xeta.status === 403)</code> yazmaqdan daha
        oxunaqlıdır. Rəqəm dəyişsə (məsələn 403 → 401), kod dəyişmir.</p>
        <p><code>if (xeta instanceof HttpException)</code> — bu, NestJS-in
        <em>bizim</em> atdığı xətadır (məsələn <code>NotFoundException</code>).
        Onun statusu və mesajı var.</p>
        <p><code>else if (xeta instanceof Error)</code> — bu isə
        <em>gözlənilməz</em> xətadır (kod səhvi). Bu halda status 500 olur və
        xəta <strong>loqa yazılır</strong> (<code>this.log.error</code>), çünki
        bunu developer görməlidir.</p>
        <p>⚠️ <strong>Validasiya xətaları xüsusi haldır:</strong> NestJS onları
        massiv kimi verir. Biz massivi <code>mesaj</code>-a yığmırıq — əvəzində
        ümumi «Validasiya xətası» yazıb detalları ayrı sahəyə qoyuruq. Beləliklə
        frontend həmişə eyni uzunluqda mesaj görür.</p>""",
        fayllar=["src/common/filters/all-exceptions.filter.ts"],
        c="""cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

echo "── Fayl yerindədirmi? ──"
ls -l src/common/filters/all-exceptions.filter.ts
echo
echo "── Status → kod xəritəsi ──"
grep -E "^  [0-9]{3}:" src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'
echo
echo "── Cavabın 4 sahəsi (koddan) ──"
grep -A8 'cavab.status(status).json' src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'
echo
echo "── Gözlənilməz xəta loqa yazılırmı? ──"
grep -n 'log.error' src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'""",
        olmaz="""$ curl -s localhost:4000/api/v1/bele-yol-yoxdur
{"statusCode":404,"message":"Cannot GET /api/v1/bele-yol-yoxdur","error":"Not Found"}

   # ⚠️ Filter olmasa NestJS-in STANDART formatı gəlir. Frontend
   # developer hər endpoint üçün fərqli format gözləməli olur:
   # bəzən «message», bəzən «error», bəzən «xeta.mesaj».
   # Nəticə: hər yeni endpoint-də frontend kodu dəyişir.

$ curl -s localhost:4000/api/v1/struktur/merkezler?limit=500
{"statusCode":400,"message":["limit 100-dən çox ola bilməz"],"error":"Bad Request"}

   # ⚠️ Burada «message» MASSİVDİR. Frontend «mesajı göstər» əmri
   # versə, ekranda «[object Object]» və ya sınıq mətn görünər.

   # Bizim formatda isə həmişə eynidir:
   #   xeta.mesaj    → «Validasiya xətası»   (həmişə sətir)
   #   xeta.detallar → ["limit 100-dən çox ola bilməz"]  (massiv)""",
        c_izah="""<p>Bu addımda server hələ qalxmır (o, 11-ci addımdadır), ona görə
        canlı nümunə göstərilmir. Amma kodun özü bütün cavabı müəyyən edir:
        <code>cavab.status(status).json({...})</code> sətri.</p>
        <p>Xəritədə 6 status kodu var. Diqqət yetirin ki,
        <code>422</code> və <code>409</code> kimi nadir kodlar da
        siyahıdadır — gələcəkdə lazım olacaq.</p>
        <p><code>log.error</code> sətri çox vacibdir: gözlənilməz xətalar
        terminalda <em>yığın izi</em> (stack trace) ilə birlikdə yazılır.
        Bu olmasa, 500 xətasının səbəbini tapmaq mümkün olmazdı.</p>""",
        sual=[
            ("Nə üçün `kod` və `mesaj` ayrıdır?",
             "Çünki proqram <code>kod</code>-u yoxlayır, insan isə <code>mesaj</code>-ı oxuyur. Mesajı tərcümə etsəniz və ya dəyişsəniz, proqram kodu sınmır."),
            ("500 xətasında istifadəçiyə nə göstərilir?",
             "«Daxili server xətası» — texniki detallar göstərilmir. Səbəb təhlükəsizlikdir: xəta mətni baza strukturu haqqında məlumat verə bilər."),
            ("Filter qlobal necə olur?",
             "<code>main.ts</code>-də <code>app.useGlobalFilters(new AllExceptionsFilter())</code> ilə. Bu, 11-ci addımdadır."),
        ],
        d_izah="""<p>Sistemin vəziyyəti: <strong>bütün xətalar üçün vahid format
        hazırdır</strong>. Hələ heç bir endpoint yoxdur, amma hansı xəta
        gəlirsə-gəlsin, cavabı bu sinif formalaşdıracaq. Növbəti addımda ilk
        həqiqi endpoint-i yaradacağıq.</p>""",
    ),

    # ═══════════════════════════════════════════════════════════════
    dict(
        no=9,
        ad="Sağlamlıq modulu — ilk işləyən endpoint",
        a="""<p>Bu, dərsin <strong>ən sevincli anıdır</strong>: ilk dəfə
        brauzerdən (və ya <code>curl</code> ilə) cavab alacağıq. Amma endpoint
        sadəcə «mən varam» deməməlidir.</p>
        <p><strong>Niyə?</strong> Təsəvvür edin: server işləyir, cavab verir,
        amma baza bağlantısı kəsilib. İstifadəçi «sistem sağlamdır» görüb
        işinə davam edir, sonra hər sorğu xəta verir. Bu, ən pis
        vəziyyətdir — problem <em>gizli</em> qalır.</p>
        <p>Ona görə sağlamlıq endpointi bazaya <em>həqiqi sorğu</em>
        göndərir və nəticəni göstərir: cədvəl sayı, gecikmə (millisaniyə ilə).
        Bu rəqəmlər sistemin vəziyyətini bir baxışda göstərir.</p>
        <p>Belə endpoint-lər həm də monitorinq üçün istifadə olunur: xarici
        xidmət hər 30 saniyədə bu ünvana müraciət edir və <code>200</code>
        gəlmirsə, sizə zəng edir.</p>""",
        anlayis=[
            ("Endpoint", "Müəyyən ünvana (URL) bağlı əməliyyat. `GET /saglamliq` kimi."),
            ("Controller", "HTTP sorğularını qarşılayan sinif. `@Controller()` ilə işarələnir."),
            ("Service", "İş məntiqini saxlayan sinif. Controller onu çağırır."),
            ("@Get()", "«Bu metod GET sorğusunu qarşılayır» işarəsi."),
            ("health check", "Sistemin canlı olub-olmadığını yoxlayan endpoint."),
            ("latency / gecikmə", "Sorğunun nə qədər vaxt aldığı."),
        ],
        kod_izah="""<p><strong>Service</strong> (<code>saglamliq.service.ts</code>) —
        işi görən hissə. <code>this.prisma.yoxla()</code> çağırır və nəticəni
        oxunaqlı formata salır. Cavabda <code>cedvel_sayi</code> və
        <code>gecikme_ms</code> var — bunlar təsadüfi rəqəmlər deyil, həqiqi
        ölçmələrdir.</p>
        <p><strong>Controller</strong> (<code>saglamliq.controller.ts</code>) —
        HTTP qatı. İki endpoint var:</p>
        <p><code>GET /api/v1</code> — kök ünvan. Sadəcə API haqqında qısa
        məlumat verir (ad, versiya, sənədləşdirmə ünvanı). Bu, «ünvanı düzgün
        yazmışam?» sualına cavab verir.</p>
        <p><code>GET /api/v1/saglamliq</code> — əsl sağlamlıq yoxlaması.</p>
        <p>⚠️ Diqqət: <code>@Controller()</code> <em>boş</em> yazılıb. Bu
        o deməkdir ki, marşrutlar birbaşa kökdən başlayır. Əgər
        <code>@Controller('saglamliq')</code> yazsaydıq, ünvan
        <code>/api/v1/saglamliq/saglamliq</code> olardı — təkrar.</p>
        <p><strong>Module</strong> — üçünü bir yerə yığır:
        controller-lər və service-lər burada qeydiyyatdan keçir.</p>""",
        fayllar=[
            "src/saglamliq/saglamliq.service.ts",
            "src/saglamliq/saglamliq.controller.ts",
            "src/saglamliq/saglamliq.module.ts",
        ],
        c="""cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

echo "── Modulun hissələri ──"
ls -1 src/saglamliq/ | sed 's/^/  /'
echo
echo "── Controller-də hansı endpoint-lər var? ──"
grep -nE "@(Get|Post|Controller)" src/saglamliq/saglamliq.controller.ts | sed 's/^/  /'
echo
echo "── Sağlamlıq yoxlamasını BİRBAŞA sınayaq ──"
npx tsx -e "
import 'dotenv/config';
import { PrismaService } from './src/prisma/prisma.service.ts';
import { SaglamliqService } from './src/saglamliq/saglamliq.service.ts';
void (async () => {
  const p = new PrismaService({ get: () => process.env.DATABASE_URL } as never);
  await p.onModuleInit();
  const s = new SaglamliqService(p);
  const c = await s.yoxla();
  console.log(JSON.stringify(c, null, 2).split('\\n').map(x => '  ' + x).join('\\n'));
  await p.onModuleDestroy();
})();
\"""",
        olmaz="""$ curl -s localhost:4000/api/v1/saglamliq
curl: (7) Failed to connect to localhost port 4000: Connection refused

   # ⚠️ Bu endpoint olmasa, «sistem işləyirmi?» sualına cavab vermək
   # üçün bazaya əl ilə qoşulmaq lazım gələrdi:
   #   psql -U arti_user -d arti_baza -c "SELECT 1"
   # Monitorinq sistemi isə ümumiyyətlə bilməzdi ki, API sağdır.

$ curl -s localhost:4000/api/v1/saglamliq
{"status":"saglam"}

   # ⚠️ Əgər endpoint sadəcə «saglam» desəydi (bazaya baxmadan),
   # baza kəsilsə də «saglam» cavabı gələrdi — YALANÇI siqnal.
   # Ona görə cavabda cedvel_sayi və gecikme_ms var.""",
        c_izah="""<p>Bu yoxlama serveri qaldırmadan <strong>servisi birbaşa</strong>
        işlədir. Bu, çox faydalı üsuldur: endpoint-in məntiqi düzgündürmü,
        yoxsa problem HTTP qatındadır — ayırd edə bilirsiniz.</p>
        <p>Gözlənilən nəticə: <code>status: "saglam"</code>,
        <code>qosulub: true</code>, <code>cedvel_sayi: 48</code> və kiçik bir
        gecikmə. Əgər <code>qosulub: false</code> gəlsə, problem bazadadır —
        <code>.env</code>-i və PostgreSQL-in işlədiyini yoxlayın.</p>""",
        sual=[
            ("Nə üçün `@Controller()` boşdur?",
             "Marşrutlar kökdən başlasın deyə. <code>@Controller('saglamliq')</code> yazsaq, ünvan <code>/saglamliq/saglamliq</code> olardı."),
            ("Sağlamlıq endpointi qorunmalıdırmı?",
             "Xeyr — monitorinq sistemləri ona parolsuz müraciət etməlidir. Bu dərsdə hələ autentifikasiya yoxdur; 3-cü dərsdə <code>@Public()</code> ilə açıq saxlanılacaq."),
            ("`gecikme_ms` nə üçün vacibdir?",
             "Baza yavaşlayırsa, bu rəqəm artır. 200 ms-dən yuxarı davamlı artım problem siqnalıdır — həll etməzdən əvvəl görürsünüz."),
            ("Şəbəkə olmadan bu endpoint işləyərmi?",
             "Baza yerli (localhost) olduğu üçün işləyir. Baza başqa serverdə olsaydı, şəbəkə kəsiləndə <code>qosulub: false</code> gələrdi."),
        ],
        d_izah="""<p>Sistemin vəziyyəti: <strong>işləyən servis məntiqi var</strong>,
        amma hələ onu HTTP-yə bağlamamışıq. Yəni kod hazırdır, qapı isə
        bağlıdır. Növbəti addımda kök modulu yaradıb bu hissələri bir-birinə
        bağlayacağıq.</p>""",
    ),

    # ═══════════════════════════════════════════════════════════════
    dict(
        no=10,
        ad="app.module.ts — kök modul",
        a="""<p>Modullar ayrı-ayrı tikinti blokları kimidir: biri baza
        bağlantısı, digəri endpoint-lər. Amma <strong>kim onları bir yerə
        yığacaq?</strong> Bunu kök modul — <code>AppModule</code> edir.</p>
        <p>NestJS tətbiqi işə düşəndə <em>ilk</em> bu modulu oxuyur və
        <code>imports</code> siyahısındaki hər modulu növbə ilə yükləyir.
        Modul yoxdursa, onun endpoint-ləri <em>mövcud deyil</em> — sanki heç
        yazılmamış kimi.</p>
        <p><strong><code>ConfigModule.forRoot({ isGlobal: true })</code></strong>
        sətri <code>.env</code> faylını oxuyur və bütün layihəyə açır.
        <code>isGlobal</code> olmasa, hər modulda ayrıca import etmək lazım
        gələrdi.</p>
        <p>⚠️ <strong>Bu fayl tez-tez dəyişən fayldır.</strong> Hər yeni modul
        yaradanda buraya iki sətir əlavə olunur: biri <code>import</code>,
        digəri <code>imports</code> siyahısına. Unutmaq asandır — o zaman
        endpoint-lər «yoxa çıxır» və səbəb görünmür.</p>""",
        anlayis=[
            ("AppModule", "Tətbiqin kök modulu — hamısını bir yerə yığır."),
            ("imports", "Bu modulun istifadə etdiyi digər modulların siyahısı."),
            ("ConfigModule", "NestJS-in konfiqurasiya modulu — `.env` oxuyur."),
            ("isGlobal", "«Bu modulu hər yerə aç» ayarı."),
            ("bootstrap", "Tətbiqin ilk işə düşmə prosesi."),
        ],
        kod_izah="""<p><code>import { Module } from '@nestjs/common'</code> —
        <code>@Module()</code> işarəsini gətirir.</p>
        <p><code>ConfigModule.forRoot({ isGlobal: true })</code> —
        <code>.env</code> faylını oxuyur. <code>forRoot</code> sözü «bu modulun
        <em>əsas</em> qurulmasıdır» deməkdir; oxşar modullar
        <code>forFeature</code> işlədir.</p>
        <p><code>PrismaModule</code> — bazaya qoşulma. <code>@Global()</code>
        olduğu üçün burada bir dəfə qeyd etmək kifayətdir.</p>
        <p><code>SaglamliqModule</code> — endpoint-lərimizi gətirir.</p>
        <p>⚠️ <strong>Sıra vacibdirmi?</strong> Bu dərsdə xeyr. Amma
        <code>ConfigModule</code>-un <em>birinci</em> olması yaxşı vərdişdir:
        digər modullar konfiqurasiyadan asılı ola bilər.</p>""",
        fayllar=["src/app.module.ts"],
        c="""cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

echo "── Kök modulun məzmunu ──"
cat -n src/app.module.ts | sed 's/^/  /'
echo
echo "── Hansı modullar qoşulub? ──"
grep -nE 'Module,' src/app.module.ts | grep -v '@' | sed 's/^/  /'
echo
echo "── ConfigModule qlobaldırmı? ──"
grep -n 'isGlobal' src/app.module.ts | sed 's/^/  /'
echo
echo "── Saglamliq modulu qoşulubmu? ──"
grep -c 'SaglamliqModule' src/app.module.ts | sed 's/^/  sayı: /'""",
        olmaz="""$ curl -s localhost:4000/api/v1/saglamliq
{"ugur":false,"xeta":{"kod":"TAPILMADI","mesaj":"Cannot GET /api/v1/saglamliq"},"yol":"/api/v1/saglamliq"}

   # ⚠️ Fayllar yerindədir, kod düzgündür, build keçir — AMMA endpoint
   # YOXDUR. Səbəb: modul kök modula qoşulmayıb. NestJS onu yükləmir,
   # ona görə marşrut da qeydiyyatdan keçmir.
   # Bu, ən çətin tapılan səhvlərdən biridir: heç bir xəta mesajı yoxdur.

$ npm run start:prod
Error: Cannot find module '/.../dist/app.module.js'

   # ⚠️ main.ts faylı app.module.ts-i import edir. Fayl yoxdursa,
   # server heç qalxmır.""",
        c_izah="""<p>Bu yoxlama «hamısı bir yerdədir?» sualına cavab verir.
        Xüsusilə son iki yoxlama vacibdir: <code>isGlobal</code> və
        modulların siyahısı.</p>
        <p>Əgər <code>SaglamliqModule</code> sayı 0-dırsa, build keçəcək, amma
        endpoint 404 verəcək. Bu səhvi tutmaq üçün məhz bu yoxlama
        lazımdır.</p>""",
        sual=[
            ("Modulu qoşmağı unutsam necə biləcəm?",
             "Ən yaxşı üsul: endpoint-i çağırmaq. 404 gəlirsə və fayllar yerindədirsə, deməli modul qoşulmayıb. Yoxlamaq üçün <code>grep -c 'ModulAdi' src/app.module.ts</code> işlədin."),
            ("Nə üçün `ConfigModule` qlobal edilir?",
             "Çünki demək olar hər servis konfiqurasiyadan nəsə oxuyur. Qlobal olmasa, hər modulda <code>imports: [ConfigModule]</code> yazmalı olardıq."),
            ("Modulların sırası nəyə təsir edir?",
             "Adətən heç nəyə. Amma bəzi hallarda modul başqasının servisini işlədə bilər — o zaman asılılıq sırası önəmli olur."),
        ],
        d_izah="""<p>Sistemin vəziyyəti: <strong>bütün hissələr bir-birinə
        bağlandı</strong>. Baza bağlantısı, xəta filtri və sağlamlıq modulu
        artıq kök modulun tərkibindədir. Amma tətbiqi hələ <em>işə salan</em>
        fayl yoxdur — növbəti, sonuncu addım məhz budur.</p>""",
    ),

    # ═══════════════════════════════════════════════════════════════
    dict(
        no=11,
        ad="main.ts — serveri işə salırıq",
        a="""<p>Bu, dərsin <strong>zirvə nöqtəsidir</strong>: bu fayl yazıldıqdan
        sonra server həqiqətən qalxır və brauzerdən cavab almaq mümkün olur.</p>
        <p><code>main.ts</code> tətbiqin <em>giriş qapısıdır</em>. NestJS bu
        faylı oxuyur, kök modulu yükləyir, HTTP serverini açır və portu
        dinləməyə başlayır. Bu fayl olmasa, bütün yazdığımız kod «ölü» qalır —
        heç nə işləmir.</p>
        <p>Burada dörd vacib iş görülür:</p>
        <p><strong>1) Qlobal prefiks</strong> — bütün endpoint-lər
        <code>/api/v1</code> ilə başlayır. Niyə? Gələcəkdə API-ın ikinci
        versiyası çıxanda köhnəni pozmadan <code>/api/v2</code> əlavə etmək
        mümkün olsun.</p>
        <p><strong>2) Validasiya qatı</strong> — gələn məlumat yoxlanılır.
        <code>whitelist</code> yalnız icazəli sahələri saxlayır,
        <code>transform</code> isə sətirləri ədədə çevirir.</p>
        <p><strong>3) Qlobal xəta filtri</strong> — 8-ci addımda yazdığımız
        filtri bütün tətbiqə şamil edir.</p>
        <p><strong>4) Swagger sənədləşdirmə</strong> — brauzerdə açılan
        interaktiv sənəd. Bütün endpoint-ləri görmək və <em>sınamaq</em>
        mümkündür.</p>""",
        anlayis=[
            ("bootstrap", "Tətbiqi işə salan funksiya."),
            ("global prefix", "Bütün marşrutların qarşısına əlavə olunan hissə: `/api/v1`."),
            ("ValidationPipe", "Gələn məlumatı DTO qaydalarına görə yoxlayan qat."),
            ("whitelist", "«DTO-da olmayan sahələri sil» ayarı."),
            ("transform", "«Məlumatı lazımi tipə çevir» ayarı (məsələn «5» → 5)."),
            ("Swagger", "API-ı brauzerdə sənədləşdirən və sınamağa imkan verən alət."),
            ("port", "Şəbəkə qapısı nömrəsi. 4000, 3000 kimi."),
        ],
        kod_izah="""<p><code>NestFactory.create(AppModule)</code> — kök modulu
        yükləyir və tətbiqi yaradır. Bu andan etibarən bütün modullar,
        controller-lər və servislər hazırdır.</p>
        <p><code>app.setGlobalPrefix('api/v1')</code> — bütün marşrutların
        qarşısına <code>/api/v1</code> əlavə edir.</p>
        <p><code>app.useGlobalPipes(new ValidationPipe({...}))</code> —
        validasiya qatı. <code>whitelist: true</code> DTO-da olmayan sahələri
        silir; <code>forbidNonWhitelisted: true</code> isə onları
        <em>xəta</em> sayır — səhv yazılmış parametrlər səssizcə udulmasın.</p>
        <p><code>app.useGlobalFilters(new AllExceptionsFilter())</code> —
        8-ci addımdaki filtri qoşur. Bu sətir olmasa, xətalar standart
        formatda gələrdi.</p>
        <p><code>SwaggerModule.setup('docs', app, ...)</code> — brauzerdə
        <code>/docs</code> ünvanını açır. Orada bütün endpoint-ləri görmək və
        «Try it out» düyməsi ilə sınamaq mümkündür.</p>
        <p><code>await app.listen(port)</code> — serveri həqiqətən başladır.
        <code>await</code> sözü «bu iş bitənə qədər gözlə» deməkdir.</p>
        <p>⚠️ <strong>Port məşğuldursa?</strong> <code>EADDRINUSE</code>
        xətası gəlir. O zaman <code>lsof -ti:4000 | xargs kill</code> ilə
        köhnə prosesi dayandırın.</p>""",
        fayllar=["src/main.ts"],
        c="""cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

echo "── main.ts yerindədirmi? ──"
ls -l src/main.ts

echo "── Build ──"
npm run build 2>&1 | tail -2
[ -f dist/main.js ] && echo "  ✓ dist/main.js yaradıldı" || echo "  ✗ dist/main.js YOXDUR"

echo
echo "── Köhnə prosesi təmizləyirik ──"
lsof -ti:${PORT:-4000} 2>/dev/null | xargs -r kill 2>/dev/null
sleep 1
echo "  port ${PORT:-4000} boşdur: $([ -z "$(lsof -ti:${PORT:-4000} 2>/dev/null)" ] && echo bəli || echo xeyr)"

echo
echo "── Server qalxır (arxa planda) ──"
PORT=${PORT:-4000} nohup npm run start:prod > /tmp/ders1a_server.log 2>&1 &
for i in $(seq 1 30); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' "${A:-http://localhost:4000/api/v1}/saglamliq" 2>/dev/null)" = "200" ] && break
  sleep 1
done
grep -E 'Mapped|BAŞLANGIC' /tmp/ders1a_server.log | sed 's/^/  /'

echo
echo "── 1) Kök ünvan ──"
curl -s "${A:-http://localhost:4000/api/v1}" | python3 -m json.tool | sed 's/^/  /'

echo
echo "── 2) Sağlamlıq ──"
curl -s "${A:-http://localhost:4000/api/v1}/saglamliq" | python3 -m json.tool | sed 's/^/  /'

echo
echo "── 3) Olmayan yol → vahid xəta formatı ──"
curl -s "${A:-http://localhost:4000/api/v1}/bele-yol-yoxdur" | python3 -m json.tool | sed 's/^/  /'

echo
echo "── 4) Swagger sənədləşdirmə ──"
echo "  /docs → HTTP $(curl -s -o /dev/null -w '%{http_code}' "${KOK:-http://localhost:4000}/docs")"

echo
echo "── Serveri dayandırırıq ──"
lsof -ti:${PORT:-4000} 2>/dev/null | xargs -r kill 2>/dev/null
echo "  ✓ dayandırıldı\"""",
        olmaz="""$ npm run start:prod
Error: Cannot find module '/.../dist/main.js'

   # ⚠️ main.ts yoxdursa (və ya build edilməyibsə) server heç qalxmır.
   # Bütün yazdığımız modullar, servislər, controller-lər — hamısı
   # «ölü» qalır. Kod var, amma işlədən yoxdur.

$ PORT=4000 npm run start:prod
Error: listen EADDRINUSE: address already in use :::4000

   # ⚠️ Port məşğuldur — köhnə bir server hələ işləyir. Həll:
   #   lsof -ti:4000 | xargs kill

   # main.ts olmasa həm də bunlar olmazdı:
   #   • /api/v1 prefiksi        → bütün ünvanlar səhv olardı
   #   • qlobal xəta formatı     → formatlar qarışıq olardı
   #   • Swagger sənədləşdirmə   → brauzerdə sınamaq mümkün olmazdı""",
        c_izah="""<p>Bu, dərsin <strong>yekun yoxlamasıdır</strong> — dörd fərqli
        şeyi sınayır:</p>
        <p><strong>1)</strong> Kök ünvan cavab verirmi? Bu, serverin
        qalxdığını göstərir.</p>
        <p><strong>2)</strong> Sağlamlıq nə deyir? <code>cedvel_sayi: 48</code>
        görməlisiniz — bu, bazanın da işlədiyini sübut edir.</p>
        <p><strong>3)</strong> Olmayan yol <em>vahid formatda</em> xəta
        verirmi? <code>xeta.kod: "TAPILMADI"</code> görməlisiniz. Əgər
        <code>statusCode</code> görsəniz, deməli filtr qoşulmayıb.</p>
        <p><strong>4)</strong> Swagger açılır? <code>/docs</code> ünvanını
        brauzerdə açıb bütün endpoint-ləri görə bilərsiniz.</p>""",
        sual=[
            ("Serveri necə dayandırım?",
             "İşlədiyi terminalda <code>Ctrl+C</code> basın. Arxa planda işləyirsə: <code>lsof -ti:4000 | xargs kill</code>."),
            ("`start:dev` ilə `start:prod` fərqi nədir?",
             "<code>start:dev</code> kodu dəyişdikcə avtomatik yenidən başladır — inkişaf üçün. <code>start:prod</code> yığılmış <code>dist</code> kodunu işlədir — istehsalat üçün, daha sürətli."),
            ("Portu necə dəyişim?",
             "<code>PORT=4100 npm run start:prod</code> — müvəqqəti. Həmişəlik üçün <code>.env</code>-də <code>PORT</code> sətrini dəyişin."),
            ("Swagger istehsalatda açıq qalmalıdırmı?",
             "Adətən xeyr — API strukturunu kənara göstərir. Sadəcə inkişaf mərhələsində açıq saxlamaq tövsiyə olunur."),
            ("`nohup` və `&` nə edir?",
             "<code>&</code> əmri arxa planda işlədir, <code>nohup</code> isə terminal bağlananda prosesin ölməməsini təmin edir."),
        ],
        d_izah="""<p><strong>Təbriklər — 1A dərsi tamamlandı!</strong> Sistemin
        vəziyyəti:</p>
        <p>✅ Baza bağlantısı işləyir və bütün layihəyə açıqdır<br>
        ✅ Xətalar vahid formatdadır<br>
        ✅ İki endpoint canlıdır: <code>/api/v1</code> və
        <code>/api/v1/saglamliq</code><br>
        ✅ Swagger sənədləşdirmə <code>/docs</code> ünvanındadır<br>
        ✅ Server <code>npm run start:prod</code> ilə qalxır</p>
        <p>Növbəti dərsdə (<strong>1B</strong>) bu təməlin üstündə davam
        edəcəyik: build və tip yoxlamasının dərin izahı, test yazmağı
        öyrənmək (Vitest), port və proses idarəsi, loq oxumaq və nasazlıq
        axtarmaq.</p>""",
    ),
]
