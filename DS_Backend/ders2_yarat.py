# -*- coding: utf-8 -*-
"""DƏRSLƏR/DS_Backend-2.html dərsini yaradır.

Kodu BİRBAŞA sınaqdan keçmiş fayllardan oxuyur — bayt-dəqiqlik üçün.
Hədəf: >= 1700 sətir.
"""
from __future__ import annotations

import html
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent          # ~/Deepseek_ARTI
MENBE = Path("/tmp/bt2")                              # sınaqdan keçmiş nüsxə
CSS = (KOK / "DS_Baza/ders.css").read_text(encoding="utf-8").strip("\n")

H: list[str] = []
A = H.append

def e(m: str) -> str:
    return html.escape(str(m), quote=False)

def fayl(yol: str) -> str:
    """Sınaqdan keçmiş faylın məzmununu qaytarır."""
    return (MENBE / yol).read_text(encoding="utf-8").rstrip("\n")

def blok(sinf: str, basliq: str, govde: str) -> None:
    A('<div class="block %s">' % sinf)
    A('  <span class="block-title">%s</span>' % basliq)
    A('  %s' % govde)
    A('</div>')

def kod(dil: str, govde: str) -> None:
    A('<pre data-lang="%s"><code>%s</code></pre>' % (dil, e(govde.strip("\n"))))

def bash(s: str) -> None: kod("bash", s)
def ts(s: str) -> None: kod("typescript", s)
def sql(s: str) -> None: kod("sql", s)
def cixis(s: str) -> None: kod("çıxış", s)
def json_(s: str) -> None: kod("json", s)

def addim(n: int, basliq: str) -> None:
    A('<h3><span class="step-num">%d</span> %s</h3>' % (n, basliq))

def yoxlama(n: int, basliq: str, govde: str) -> None:
    blok("block-yox", "YOXLAMA %d — %s" % (n, basliq), govde)

def fayl_yaz(yol: str, dil: str = "typescript") -> None:
    """«mkdir -p + cat > fayl <<'EOF'» bloku.

    mkdir -p MÜTLƏQDİR: cat > qovluq movcud olmadan fayl yarada bilmir.
    """
    qovluq = str(Path(yol).parent).replace(".", "")
    bash("mkdir -p ~/Deepseek_ARTI/DS_Backend/%s\n\n"
         "cat > ~/Deepseek_ARTI/DS_Backend/%s <<'EOF'\n%s\nEOF"
         % (qovluq, yol, fayl(yol)))

# ══════════════════════════════════════════════════════════════════
A('<!DOCTYPE html>')
A('<html lang="az">')
A('<head>')
A('<meta charset="UTF-8">')
A('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
A('<title>DS Backend 2 — DTO, validasiya, tam CRUD ve modullar</title>')
A('<style>')
A(CSS)
A('</style>')
A('</head>')
A('<body>')
A('<div class="container">')
A('<header>')
A('  <div class="lesson-badge">DS_Backend · Hissə 2/4</div>')
A('  <h1>Backend 2 — DTO, validasiya ve tam CRUD</h1>')
A('  <p class="subtitle">Məlumatı qəbul etməzdən əvvəl yoxla, sonra yaz — '
  'vahid xəta formatı və SQL injection qoruması ilə</p>')
A('  <p class="meta">Layihə: <strong>Deepseek_ARTI</strong> · Blok: <code>DS_Backend</code> · '
  'NestJS 12 · Prisma 7 · class-validator 0.14 · Vitest 4</p>')
A('</header>')

# ── TOC ──
A('<div class="toc">')
A('  <h3>📚 Bu dərsdə nələr öyrənəcəksiniz</h3>')
A('  <ol>')
TOC = [
    "Backend-2 nə verir — xülasə",
    "Mövcud vəziyyət — Backend-1-dən sonra",
    "DTO nədir və niyə bu qədər vacibdir",
    "class-validator — bütün dekoratorlar",
    "SehifeDto — ümumi səhifələmə DTO-su",
    "ValidationPipe — dörd konfiqurasiya",
    "CreateMerkezDto — validasiya qaydaları",
    "UpdateMerkezDto — PartialType",
    "Filtr DTO-ları — miras zənciri",
    "Vahid xəta formatı — exception filter",
    "SQL injection qoruması — ağ siyahı prinsipi",
    "Tam CRUD servisi",
    "Tam CRUD controller",
    "Kadrlar modulu — filtr qurucusu",
    "Kadrlar — axtarış, səhifələmə, sıralama",
    "Hesabat modulu — view və funksiyalar",
    "Sağlamlıq endpoint-i",
    "app.module.ts — modul qeydiyyatı",
    "Unit testlər — DTO və servis",
    "e2e testlər — 30 test",
    "Xəta kitabçası",
    "Yoxlama siyahısı və növbəti dərs",
]
for i, t in enumerate(TOC, 1):
    A('    <li><a href="#b%d">%s</a></li>' % (i, t))
A('  </ol>')
A('</div>')

# ══════════════════ 1 ══════════════════
A('<h2 id="b1">1. Backend-2 nə verir — xülasə</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Backend-1-də server işə düşdü və <strong>oxuma</strong> endpoint-i quruldu. "
     "Backend-2-də sistem <strong>real tətbiqə</strong> çevrilir:</p>"
     "<table>"
     "<tr><th>#</th><th>Nə əlavə olunur</th><th>Nə üçün</th></tr>"
     "<tr><td>1</td><td><strong>DTO + validasiya</strong></td><td>Zibil məlumat bazaya düşməsin</td></tr>"
     "<tr><td>2</td><td><strong>Tam CRUD</strong> (POST/PATCH/DELETE)</td><td>Məlumatı idarə etmək</td></tr>"
     "<tr><td>3</td><td><strong>Vahid xəta formatı</strong></td><td>Frontend bir format bilsin</td></tr>"
     "<tr><td>4</td><td><strong>Səhifələmə + filtr + sıralama</strong></td><td>10 000 sətir bir səhifəyə sığmaz</td></tr>"
     "<tr><td>5</td><td><strong>SQL injection qoruması</strong></td><td>İstifadəçi bazanı silə bilməsin</td></tr>"
     "<tr><td>6</td><td><strong>Kadrlar modulu</strong></td><td>5 cədvəlli birləşmə, axtarış</td></tr>"
     "<tr><td>7</td><td><strong>Hesabat modulu</strong></td><td>View və funksiyaları API-yə çıxarmaq</td></tr>"
     "<tr><td>8</td><td><strong>55 test</strong></td><td>Dəyişiklik köhnə funksiyanı pozmasın</td></tr>"
     "</table>")
blok("block-niye", "NİYƏ BU DƏRS KRİTİKDİR?",
     "<p>Backend-1 'işləyən skelet' idi. Bu dərsdə isə <strong>təhlükəsizlik</strong> "
     "və <strong>etibarlılıq</strong> qatı qurulur. Bu iki şey olmasa:</p>"
     "<ul>"
     "<li>İstifadəçi <code>{\"ad\": null}</code> göndərər → baza xəta verər;</li>"
     "<li>İstifadəçi <code>{\"rol\": \"admin\"}</code> göndərər → özünə admin hüququ verər;</li>"
     "<li>İstifadəçi <code>?siralama_sah=ad;DROP TABLE</code> yazsa → baza silinər;</li>"
     "<li>10 000 əməkdaş bir JSON-da gələr → brauzer donar.</li>"
     "</ul>")
A('<div class="success-box">Bu dərsin sonunda API <strong>təhlükəsiz</strong> və '
  '<strong>proqramlaşdırıla bilən</strong> olacaq: 18 endpoint, 55 test.</div>')

# ══════════════════ 2 ══════════════════
A('<h2 id="b2">2. Mövcud vəziyyət — Backend-1-dən sonra</h2>')
blok("block-ne", "NƏ EDƏCƏYİK", "<p>Başlamazdan əvvəl nəyin olduğunu yoxlayacağıq.</p>")
bash("""
cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST

pwd && ls package.json          # dogru qovluqdayiqmi?
ls src/
npm test                        # Backend-1 testleri kecirmi?
""")
cixis("""
src/
app.controller.spec.ts
app.controller.ts
app.module.ts
app.service.ts
main.ts
prisma/
struktur/

 ✓ src/struktur/struktur.service.spec.ts (4 tests)
 Test Files  2 passed (2)
      Tests  5 passed (5)
""")
blok("block-xeber", "⚠️ NƏYİ DƏYİŞƏCƏYİK",
     "<p>Bu dərsdə <strong>default NestJS faylları silinəcək</strong>:</p>"
     "<table>"
     "<tr><th>Fayl</th><th>Nə olacaq</th><th>Səbəb</th></tr>"
     "<tr><td><code>app.controller.ts</code></td><td>silinir</td><td>Real controller-lər var</td></tr>"
     "<tr><td><code>app.service.ts</code></td><td>silinir</td><td>Real servislər var</td></tr>"
     "<tr><td><code>app.controller.spec.ts</code></td><td>silinir</td><td>'Hello World' testi lazımsız</td></tr>"
     "<tr><td><code>test/app.e2e-spec.ts</code></td><td>silinir</td><td>Real e2e testi ilə əvəzlənir</td></tr>"
     "</table>"
     "<p><strong>Diqqət:</strong> <code>app.module.ts</code>-dən <code>AppController</code> "
     "çıxarılsa və <code>app.controller.ts</code> qalsa, heç bir xəta çıxmaz — "
     "sadəcə <code>GET /</code> <strong>404</strong> qaytarar.</p>")
blok("block-izah", "İZAH — bu fayllar hardan gəldi?",
     "<p>Onları <code>nest new</code> əmri yaradıb — 'salam dünya' nümunəsi kimi. "
     "Real layihədə onların yeri yoxdur.</p>")
bash("""
cd ~/Deepseek_ARTI/DS_Backend
rm -f src/app.controller.ts src/app.service.ts src/app.controller.spec.ts
rm -f test/app.e2e-spec.ts
""")
yoxlama(2, "Təmizlik",
        "<pre><code>ls src/\n# app.module.ts  main.ts  prisma/  struktur/</code></pre>")

# ══════════════════ 3 ══════════════════
A('<h2 id="b3">3. DTO nədir və niyə bu qədər vacibdir</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p><strong>DTO</strong> (Data Transfer Object) — şəbəkədən gələn məlumatın "
     "<strong>formasını və qaydalarını</strong> təyin edən sinifdir.</p>")
blok("block-niye", "NİYƏ LAZIMDIR",
     "<p>DTO olmasa, istifadəçinin göndərdiyi <strong>hər şey</strong> birbaşa bazaya gedər:</p>")
json_("""{
  "ad": null,
  "email": "bu-email-deyil",
  "maas": -5000,
  "rol": "admin",
  "aktiv": "beli"
}""")
blok("block-olmaz", "OLMASA NƏ OLAR — real nəticələr",
     "<table>"
     "<tr><th>Göndərilən</th><th>DTO olmadan</th><th>Nəticə</th></tr>"
     "<tr><td><code>\"ad\": null</code></td><td>Baza <code>NOT NULL</code> pozuntusu</td><td>500 xətası</td></tr>"
     "<tr><td><code>\"email\": \"bu-email-deyil\"</code></td><td>Bazaya yazılır</td><td>E-poçt göndərilə bilmir</td></tr>"
     "<tr><td><code>\"maas\": -5000</code></td><td>Mənfi maaş</td><td>Hesabat səhv olur</td></tr>"
     "<tr><td><code>\"rol\": \"admin\"</code></td><td><strong>Yazılır!</strong></td><td>İstifadəçi özünə admin edir</td></tr>"
     "<tr><td><code>\"aktiv\": \"beli\"</code></td><td>Tip xətası</td><td>500 xətası</td></tr>"
     "</table>")
blok("block-izah", "İZAH — DTO harada dayanır?",
     "<pre data-lang=\"sxem\"><code>Brauzer\n"
     "   |  JSON gonderir\n"
     "   v\n"
     "ValidationPipe   &lt;-- DTO burada yoxlanilir\n"
     "   |  temiz melumat\n"
     "   v\n"
     "Controller  ->  Service  ->  Baza</code></pre>"
     "<p>Yoxlama <strong>controller-ə çatmazdan əvvəl</strong> baş verir. "
     "Servis heç vaxt pis məlumat görmür.</p>")
blok("block-evez", "ƏVƏZİNDƏ — DTO-suz yanaşmalar",
     "<table>"
     "<tr><th>Yol</th><th>Üstünlük</th><th>Çatışmazlıq</th></tr>"
     "<tr><td>Manual <code>if</code> yoxlamaları</td><td>Asılılıq yoxdur</td><td>Hər endpoint-də təkrar, unudulur</td></tr>"
     "<tr><td>Zod / Joi sxemləri</td><td>TypeScript tipləri çıxarılır</td><td>NestJS pipe-ları ilə əlavə inteqrasiya</td></tr>"
     "<tr><td>Baza səviyyəsində <code>CHECK</code></td><td>Ən etibarlı</td><td>İstifadəçiyə aydın mesaj gəlmir</td></tr>"
     "<tr><td><strong>class-validator DTO</strong></td><td>Deklarativ, Swagger inteqrasiyası</td><td>Sinif yazmaq lazımdır</td></tr>"
     "</table>"
     "<p>Ən yaxşı yanaşma — <strong>hər üç qat</strong>: DTO (mesaj), servis (məntiq), "
     "baza (son sədd).</p>")

# ══════════════════ 4 ══════════════════
A('<h2 id="b4">4. class-validator — bütün dekoratorlar</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Ən çox işlənən validasiya dekoratorlarını öyrənəcəyik.</p>")
A('<table>')
A('  <tr><th>Dekorator</th><th>Nə yoxlayır</th><th>Nümunə</th></tr>')
DEK = [
    ("@IsString()", "Mətn tipi", "<code>'salam'</code>"),
    ("@IsInt()", "Tam ədəd", "<code>5</code>"),
    ("@IsNumber()", "İstənilən ədəd", "<code>5.5</code>"),
    ("@IsBoolean()", "Doğru/yalan", "<code>true</code>"),
    ("@IsEmail()", "E-poçt formatı", "<code>a@b.az</code>"),
    ("@IsOptional()", "Buraxıla bilər", "—"),
    ("@MinLength(3)", "Minimum uzunluq", "<code>'abc'</code>"),
    ("@MaxLength(200)", "Maksimum uzunluq", "<code>'...'</code>"),
    ("@Min(1)", "Minimum dəyər", "<code>1</code>"),
    ("@Max(100)", "Maksimum dəyər", "<code>100</code>"),
    ("@IsIn([...])", "Siyahıdan biri", "<code>'asc'</code>"),
    ("@Matches(/regex/)", "Regex uyğunluğu", "<code>+994...</code>"),
    ("@IsDateString()", "ISO tarix", "<code>2026-09-19</code>"),
    ("@IsArray()", "Massiv", "<code>[1,2]</code>"),
    ("@IsEnum(Tip)", "Enum dəyəri", "<code>Tip.MERKEZ</code>"),
]
for d, n, x in DEK:
    A('  <tr><td><code>%s</code></td><td>%s</td><td>%s</td></tr>' % (d, n, x))
A('</table>')
blok("block-izah", "İZAH — xəta mesajı necə yazılır?",
     "<p>Hər dekorator ikinci arqument kimi <strong>mesaj</strong> qəbul edir:</p>")
ts("""
@MinLength(3)                                     // standart ingilis mesaji
@MinLength(3, { message: 'Ad ən azı 3 simvol olmalıdır' })   // oz mesajimiz
""")
blok("block-ipucu", "💡 NİYƏ AZƏRBAYCAN DİLİNDƏ MESAJ?",
     "<p>Standart mesaj <code>\"ad must be longer than or equal to 3 characters\"</code> "
     "olur. Frontend bunu <strong>olduğu kimi</strong> istifadəçiyə göstərir. "
     "Azərbaycan dilində yazsaq, tərcümə qatı lazım gəlmir.</p>")
blok("block-xeber", "⚠️ @Type(() => Number) UNUDULSA",
     "<p>URL parametrləri <strong>həmişə mətn</strong> kimi gəlir: "
     "<code>?limit=20</code> → <code>limit = '20'</code>.</p>"
     "<p><code>@IsInt()</code> mətn üzərində işləmir. Çevirmə üçün "
     "<code>@Type(() => Number)</code> lazımdır:</p>")
ts("""
// SEHV — '20' gelir, @IsInt() uğursuz olur
@IsOptional()
@IsInt()
limit: number = 20;

// DOĞRU — evvelce reqeme cevir, sonra yoxla
@IsOptional()
@Type(() => Number)      // <- BU MÜTLƏQDİR
@IsInt()
limit: number = 20;
""")
blok("block-olmaz", "OLMASA NƏ OLAR — @Type olmadan",
     "<pre><code>$ curl 'http://localhost:4000/api/v1/struktur/merkezler?limit=3'\n"
     "{\n"
     "  \"ugur\": false,\n"
     "  \"xeta\": {\n"
     "    \"kod\": \"YANLIS_SORGU\",\n"
     "    \"mesaj\": \"Validasiya xetasi\",\n"
     "    \"detallar\": [\"limit tam eded olmalidir\"]\n"
     "  }\n"
     "}</code></pre>"
     "<p>Hal buki <code>limit=3</code> tamamilə düzgündür — sadəcə çevrilməyib.</p>")

# ══════════════════ 5 ══════════════════
A('<h2 id="b5">5. SehifeDto — ümumi səhifələmə DTO-su</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Bütün siyahı endpoint-ləri üçün <strong>ortaq</strong> DTO yaradacağıq: "
     "səhifələmə, axtarış, sıralama.</p>")
blok("block-niye", "NİYƏ ORTAQ?",
     "<p>11 modulun hər birində eyni 5 sahəni təkrar yazmaq lazım gəlməsin. "
     "<code>extends SehifeDto</code> kifayət edir.</p>")
fayl_yaz("src/common/dto/sehife.dto.ts")
blok("block-izah", "İZAH — əsas məqamlar",
     "<table>"
     "<tr><th>Kod</th><th>Nə edir</th></tr>"
     "<tr><td><code>@Type(() => Number)</code></td><td>URL mətnini rəqəmə çevirir</td></tr>"
     "<tr><td><code>@Max(100)</code></td><td>Bir sorğuda 100-dən çox sətir gəlməsin</td></tr>"
     "<tr><td><code>= 1</code> (default)</td><td>Parametr verilməzsə işləyən dəyər</td></tr>"
     "<tr><td><code>get offset()</code></td><td>Hesablanmış xassə — SQL OFFSET üçün</td></tr>"
     "<tr><td><code>Sehifelenmis&lt;T&gt;</code></td><td>Ümumi cavab formatı (generic)</td></tr>"
     "</table>")
blok("block-izah", "İZAH — nə üçün limit məhdudlaşdırılır?",
     "<p>Təsəvvül edin bazada 500 000 əməkdaş var və kimsə yazır "
     "<code>?limit=1000000</code>. Nəticə:</p>"
     "<ul>"
     "<li>PostgreSQL milyon sətir hazırlayır — yaddaş dolur;</li>"
     "<li>Node.js hamısını JSON-a çevirir — bir neçə saniyə bloklanır;</li>"
     "<li>Şəbəkə 200 MB ötürür — brauzer donur.</li>"
     "</ul>"
     "<p><code>@Max(100)</code> bunun qarşısını <strong>bir sətirlə</strong> alır.</p>")
blok("block-evez", "ƏVƏZİNDƏ — offset yerinə cursor",
     "<table>"
     "<tr><th>Üsul</th><th>Üstünlük</th><th>Çatışmazlıq</th></tr>"
     "<tr><td><strong>OFFSET/LIMIT</strong></td><td>Sadə, səhifə nömrəsi var</td><td>Böyük offset yavaşdır</td></tr>"
     "<tr><td>Keyset (cursor)</td><td>Çox sürətli</td><td>Səhifə nömrəsi yoxdur</td></tr>"
     "</table>"
     "<p>10 000 sətrə qədər <code>OFFSET</code> tamamilə kifayətdir. "
     "Milyonlarla sətirdə cursor-a keçin.</p>")

# ══════════════════ 6 ══════════════════
A('<h2 id="b6">6. ValidationPipe — dörd konfiqurasiya</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p><code>main.ts</code>-də validasiyanı <strong>sərtləşdirəcəyik</strong>.</p>")
fayl_yaz("src/main.ts")
blok("block-izah", "İZAH — hər seçim nə edir?",
     "<table>"
     "<tr><th>Seçim</th><th>Nə edir</th><th>Olmazsa</th></tr>"
     "<tr><td><code>whitelist: true</code></td><td>DTO-da olmayan sahələri silir</td>"
     "<td>Artıq sahələr servisə çatır</td></tr>"
     "<tr><td><code>forbidNonWhitelisted: true</code></td><td>...və <strong>400 xəta verir</strong></td>"
     "<td>Səhv yazılmış sahə sükutla itir</td></tr>"
     "<tr><td><code>transform: true</code></td><td>DTO sinfinə çevirir, default-ları işlədir</td>"
     "<td><code>@Type()</code> işləmir</td></tr>"
     "<tr><td><code>enableImplicitConversion: false</code></td><td>Yalnız açıq <code>@Type()</code> çevirir</td>"
     "<td>Gözlənilməz çevrilmələr (<code>'abc'</code> → <code>NaN</code>)</td></tr>"
     "</table>")
blok("block-xeber", "⚠️ whitelist vs forbidNonWhitelisted",
     "<p>Bu iki seçim <strong>bir yerdə</strong> işlədilməlidir:</p>"
     "<table>"
     "<tr><th>whitelist</th><th>forbidNonWhitelisted</th><th>Nəticə</th></tr>"
     "<tr><td>false</td><td>false</td><td>Hər şey keçir ❌</td></tr>"
     "<tr><td>true</td><td>false</td><td>Artıqlar sükutla silinir ⚠️</td></tr>"
     "<tr><td>true</td><td>true</td><td>400 xəta — istifadəçi səhvini bilir ✅</td></tr>"
     "</table>"
     "<p><strong>Mass assignment hücumu:</strong> istifadəçi "
     "<code>{\"ad\": \"X\", \"rol\": \"admin\"}</code> göndərir. "
     "<code>forbidNonWhitelisted</code> olmasa, xəta çıxmaz və istifadəçi "
     "düşünər ki, hər şey qaydasındadır.</p>")
yoxlama(6, "Validasiya işləyir?",
        "<pre><code>$ curl -X POST .../struktur/merkezler \\\n"
        "    -H 'Content-Type: application/json' \\\n"
        "    -d '{\"ad\":\"Test\",\"rol\":\"admin\"}'\n\n"
        "{ \"ugur\": false,\n"
        "  \"xeta\": { \"kod\": \"YANLIS_SORGU\",\n"
        "            \"detallar\": [\"property rol should not exist\"] } }</code></pre>")

# ══════════════════ 7 ══════════════════
A('<h2 id="b7">7. CreateMerkezDto — validasiya qaydaları</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Yeni mərkəz yaratmaq üçün DTO yazacağıq — 8 sahə, hər biri öz qaydası ilə.</p>")
fayl_yaz("src/struktur/dto/create-merkez.dto.ts")
blok("block-izah", "İZAH — hər sahənin qaydası",
     "<table>"
     "<tr><th>Sahə</th><th>Qayda</th><th>Nə üçün</th></tr>"
     "<tr><td><code>ad</code></td><td><code>@MinLength(3)</code> + <code>@MaxLength(200)</code></td>"
     "<td>'A' adlı mərkəz olmaz; 200 simvol ekranda sığmaz</td></tr>"
     "<tr><td><code>tip</code></td><td><code>@IsIn([...])</code></td>"
     "<td>Yalnız 4 icazəli tip — sərbəst mətn yox</td></tr>"
     "<tr><td><code>telefon</code></td><td><code>@Matches(/^\\+?[0-9\\s()-]{7,25}$/)</code></td>"
     "<td>Rəsmi format: <code>+994 12 599 08 08</code></td></tr>"
     "<tr><td><code>email</code></td><td><code>@IsEmail()</code></td>"
     "<td>Yanlış e-poçtla bildiriş göndərilə bilmir</td></tr>"
     "<tr><td><code>yaradilma_tarixi</code></td><td><code>@Matches(/^\\d{4}-\\d{2}-\\d{2}$/)</code></td>"
     "<td>ISO format — <code>15.02.2024</code> qəbul edilmir</td></tr>"
     "<tr><td><code>aktiv</code></td><td><code>@IsBoolean()</code></td>"
     "<td><code>'beli'</code> yox, <code>true</code></td></tr>"
     "</table>")
blok("block-xeber", "⚠️ @IsOptional() MÜTLƏQ DEYİL, AMMA...",
     "<p><code>@IsOptional()</code> olmasa, sahə <strong>məcburi</strong> olur. "
     "DTO-da isə yalnız <code>ad</code> məcburi olmalıdır (bazada da <code>NOT NULL</code>).</p>"
     "<table>"
     "<tr><th>Sahə</th><th>Bazada</th><th>DTO-da</th></tr>"
     "<tr><td><code>ad</code></td><td>NOT NULL</td><td>məcburi ✅</td></tr>"
     "<tr><td>digərləri</td><td>NULL ola bilər</td><td><code>@IsOptional()</code> ✅</td></tr>"
     "</table>")
blok("block-ipucu", "💡 TİP İŞARƏSİ — «!» NƏ DEMƏKDİR?",
     "<p><code>ad!: string;</code> — <code>!</code> TypeScript-ə deyir: "
     "'bu sahə konstruktorda təyin olunmasa da, narahat olma'.</p>"
     "<p>DTO sinfi heç vaxt <code>new</code> ilə yaradılmır — "
     "<code>ValidationPipe</code> JSON-u çevirir və sahələri doldurur. "
     "<code>!</code> olmasa TypeScript <code>strictPropertyInitialization</code> xətası verər.</p>")

# ══════════════════ 8 ══════════════════
A('<h2 id="b8">8. UpdateMerkezDto — PartialType</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Yeniləmə üçün DTO. Bütün sahələr <strong>opsional</strong> olmalıdır — "
     "istifadəçi yalnız telefonu dəyişmək istəyə bilər.</p>")
fayl_yaz("src/struktur/dto/update-merkez.dto.ts")
blok("block-izah", "İZAH — PartialType nə edir?",
     "<p><code>PartialType(CreateMerkezDto)</code> <strong>avtomatik</strong> "
     "yeni sinif yaradır:</p>"
     "<table>"
     "<tr><th>CreateMerkezDto</th><th>UpdateMerkezDto</th></tr>"
     "<tr><td><code>@MinLength(3) ad: string</code></td><td><code>@IsOptional() @MinLength(3) ad?: string</code></td></tr>"
     "<tr><td><code>@IsEmail() email?: string</code></td><td><code>@IsOptional() @IsEmail() email?: string</code></td></tr>"
     "</table>"
     "<p>Yəni <strong>bütün qaydalar saxlanılır</strong>, sadəcə hər sahə "
     "opsional olur.</p>")
blok("block-olmaz", "OLMASA NƏ OLAR — DTO təkrar yazılsa",
     "<p>8 sahəni iki dəfə yazmalı olardıq. Sonra <code>CreateMerkezDto</code>-da "
     "bir qayda dəyişsək, <code>UpdateMerkezDto</code>-nu da yeniləməli olardıq — "
     "və mütləq biri unudulardı.</p>"
     "<p><strong>Prinsip:</strong> bir məlumat, bir yer.</p>")
blok("block-evez", "ƏVƏZİNDƏ — OmitType / PickType",
     "<table>"
     "<tr><th>Alət</th><th>Nə edir</th><th>Nə vaxt</th></tr>"
     "<tr><td><code>PartialType(X)</code></td><td>Hamısı opsional</td><td>PATCH</td></tr>"
     "<tr><td><code>OmitType(X, ['ad'])</code></td><td>'ad' sahəsini çıxarır</td><td>Ad dəyişməz olmalıdır</td></tr>"
     "<tr><td><code>PickType(X, ['ad'])</code></td><td>Yalnız 'ad' qalır</td><td>Xüsusi endpoint</td></tr>"
     "<tr><td><code>IntersectionType(A, B)</code></td><td>İki DTO-nu birləşdirir</td><td>Mürəkkəb sxemlər</td></tr>"
     "</table>")

# ══════════════════ 9 ══════════════════
A('<h2 id="b9">9. Filtr DTO-ları — miras zənciri</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Hər modul üçün öz filtrini <code>SehifeDto</code>-dan miras alaraq yaradacağıq.</p>")
A('<pre data-lang="sxem"><code>SehifeDto          sehife, limit, axtar, siralama, siralama_sah\n'
  '   |\n'
  '   +-- MerkezFiltrDto      + tip, aktiv\n'
  '   +-- EmekdasFiltrDto     + merkez_id, shobe_id, vezife_id, min_maas, max_maas\n'
  '   +-- ... (gelecek modullar)</code></pre>')
fayl_yaz("src/struktur/dto/merkez-filtr.dto.ts")
blok("block-izah", "İZAH — miras nə verir?",
     "<table>"
     "<tr><th>Fayda</th><th>İzah</th></tr>"
     "<tr><td>Kod təkrarı yox</td><td>5 ortaq sahə bir dəfə yazılır</td></tr>"
     "<tr><td>Vahid davranış</td><td>Bütün modullarda <code>limit</code> 100-dür</td></tr>"
     "<tr><td>Swagger bütöv</td><td>Bütün parametrlər sənəddə görünür</td></tr>"
     "</table>")
blok("block-ipucu", "💡 Swagger-DƏ MİRAS GÖRÜNÜR",
     "<p><code>/docs</code> səhifəsində <code>MerkezFiltrDto</code> açılanda "
     "<strong>həm öz sahələri, həm də valideyndən gələnlər</strong> görünür. "
     "Frontend komandası bütün parametrləri bir yerdə görür.</p>")

# ══════════════════ 10 ══════════════════
A('<h2 id="b10">10. Vahid xəta formatı — exception filter</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Bütün xətaları <strong>eyni formatda</strong> qaytaran filtr yazacağıq.</p>")
blok("block-niye", "NİYƏ LAZIMDIR",
     "<p>NestJS standart formatı belədir:</p>")
json_("""{
  "statusCode": 404,
  "message": "Merkez tapilmadi: id=999",
  "error": "Not Found"
}""")
blok("block-olmaz", "OLMASA NƏ OLAR — frontend nə çəkər?",
     "<p>Frontend hər endpoint üçün <strong>fərqli</strong> format gözləyir. "
     "Validasiya xətasında <code>message</code> <strong>massiv</strong> olur, "
     "digərlərində <strong>mətn</strong>:</p>")
json_("""// Validasiya xetasi
{ "statusCode": 400, "message": ["ad must be longer..."], "error": "Bad Request" }

// Tapilmadi
{ "statusCode": 404, "message": "Merkez tapilmadi: id=999", "error": "Not Found" }""")
blok("block-izah", "İZAH — yeni format",
     "<p>Biz <strong>həmişə eyni</strong> quruluş qaytarırıq:</p>")
json_("""{
  "ugur": false,
  "xeta": {
    "kod": "TAPILMADI",
    "mesaj": "Merkez tapilmadi: id=999"
  },
  "yol": "/api/v1/struktur/merkezler/999",
  "vaxt": "2026-09-19T18:40:31.123Z"
}""")
blok("block-ipucu", "💡 NƏ ÜÇÜN «kod» SAHƏSİ?",
     "<p><code>mesaj</code> azərbaycan dilindədir və dəyişə bilər. "
     "<code>kod</code> isə <strong>maşın oxuyan</strong> sabit dəyərdir:</p>"
     "<table>"
     "<tr><th>kod</th><th>HTTP</th><th>Frontend nə edir</th></tr>"
     "<tr><td><code>YANLIS_SORGU</code></td><td>400</td><td>Formada səhvləri göstərir</td></tr>"
     "<tr><td><code>AUTENTIFIKASIYA_LAZIM</code></td><td>401</td><td>Login səhifəsinə yönləndirir</td></tr>"
     "<tr><td><code>ICAZE_YOXDUR</code></td><td>403</td><td>'İcazəniz yoxdur' mesajı</td></tr>"
     "<tr><td><code>TAPILMADI</code></td><td>404</td><td>'Tapılmadı' səhifəsi</td></tr>"
     "<tr><td><code>TOQQUSMA</code></td><td>409</td><td>'Bu ad artıq var' xəbərdarlığı</td></tr>"
     "</table>")
addim(1, "Fil tri yaz")
fayl_yaz("src/common/filters/all-exceptions.filter.ts")
blok("block-izah", "İZAH — filtrin məntiqi",
     "<table>"
     "<tr><th>Addım</th><th>Nə edir</th></tr>"
     "<tr><td><code>@Catch()</code></td><td><strong>Bütün</strong> xətaları tutur (boş arqument = hamısı)</td></tr>"
     "<tr><td><code>switchToHttp()</code></td><td>HTTP kontekstinə keçir</td></tr>"
     "<tr><td><code>xeta instanceof HttpException</code></td><td>NestJS xətasıdırsa statusu götürür</td></tr>"
     "<tr><td><code>Array.isArray(mesaj)</code></td><td>Validasiya xətasını ayırd edir</td></tr>"
     "<tr><td><code>this.log.error(...)</code></td><td>Gözlənilməz xətanı server jurnalına yazır</td></tr>"
     "</table>")
blok("block-xeber", "⚠️ 500 XƏTASI İSTİFADƏÇİYƏ GÖSTƏRİLMİR",
     "<p><code>HttpException</code> olmayan xəta (məsələn SQL xətası) "
     "<strong>500</strong> kimi qaytarılır və mesajı gizlədilir:</p>"
     "<pre><code>{ \"kod\": \"DAXILI_XETA\", \"mesaj\": \"Daxili server xetasi\" }</code></pre>"
     "<p>Əsl mesaj <strong>yalnız server jurnalında</strong> olur. Səbəb: "
     "texniki detallar (<code>relation \"x\" does not exist</code>) "
     "hücumçuya bazanın strukturu haqqında məlumat verir.</p>")
addim(2, "Filtri qeyd et")
bash("""
# main.ts-de artiq var:
app.useGlobalFilters(new AllExceptionsFilter());
""")
yoxlama(10, "Xəta formatı",
        "<pre><code>$ curl -s .../struktur/merkezler/999999 | python3 -m json.tool\n\n"
        "{\n"
        "  \"ugur\": false,\n"
        "  \"xeta\": { \"kod\": \"TAPILMADI\", \"mesaj\": \"Merkez tapilmadi: id=999999\" },\n"
        "  \"yol\": \"/api/v1/struktur/merkezler/999999\",\n"
        "  \"vaxt\": \"2026-09-19T18:40:31.123Z\"\n"
        "}</code></pre>")

# ══════════════════ 11 ══════════════════
A('<h2 id="b11">11. SQL injection qoruması — ağ siyahı prinsipi</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Sıralama sütunu SQL-ə <strong>birbaşa yazılır</strong> — çünki "
     "sütun adını parametr kimi ötürmək mümkün deyil. Bunu təhlükəsiz edəcəyik.</p>")
blok("block-niye", "NİYƏ TƏHLÜKƏLİDİR?",
     "<p>Prisma <code>${...}</code> ifadəsini <strong>dəyər</strong> kimi ötürür, "
     "lakin sütun adı dəyər deyil:</p>")
sql("""
-- Bu ISLEMIR (parametr kimi):
SELECT * FROM merkezler WHERE id = $1;

-- Bu ISLEMIR (sutun adi parametr ola bilmez):
SELECT * FROM merkezler ORDER BY $1;   -- 'id' yox, sabit metn kimi baxis
""")
blok("block-olmaz", "OLMASA NƏ OLAR — real hücum",
     "<p>Sadəlövh yanaşma:</p>")
ts("""
// TEHLUKELI!
const sql = `SELECT * FROM merkezler ORDER BY ${dto.siralama_sah}`;
await this.prisma.$queryRawUnsafe(sql);
""")
cixis("""
$ curl '.../merkezler?siralama_sah=id;DROP TABLE struktur.shobeler--'

# PostgreSQL bunu BIR sorğu kimi icra edir:
SELECT * FROM merkezler ORDER BY id;
DROP TABLE struktur.shobeler;--   <-- BAZA SILINDI
""")
blok("block-izah", "İZAH — AĞ SİYAHI (WHITELIST) PRİNSİPİ",
     "<p><strong>Qara siyahı</strong> (qadağan olunanları saymaq) həmişə uduzur — "
     "hücumçu yeni variant tapır.</p>"
     "<p><strong>Ağ siyahı</strong> (yalnız icazəliləri saymaq) isə qırılmazdır:</p>")
ts("""
/** YALNIZ bu sutunlar uzre siralama olar */
const SIRALAMA_ICAZELI = ['id', 'ad', 'tip', 'unvan'] as const;

private sutunYoxla(sutun?: string): string {
  if (!sutun) return 'id';                              // susmaya gore
  if (!SIRALAMA_ICAZELI.includes(sutun as never)) {
    throw new BadRequestException(
      `Bu sutun uzre siralama mumkun deyil: "${sutun}". ` +
      `Icazeli sutunlar: ${SIRALAMA_ICAZELI.join(', ')}`,
    );
  }
  return sutun;                                          // artiq tehlukesiz
}
""")
blok("block-ipucu", "💡 NİYƏ SÜKUTLA «id»-YƏ DÜŞMÜRÜK?",
     "<p>Alternativ: yanlış sütun gəlsə, <code>'id'</code> istifadə et — xəta vermə. "
     "Bu <strong>pisdir</strong>:</p>"
     "<ul>"
     "<li>İstifadəçi <code>?siralama_sah=maass</code> (yazı səhvi) yazır;</li>"
     "<li>API 200 qaytarır, sıralama isə <code>id</code> üzrə olur;</li>"
     "<li>İstifadəçi düşünür ki, sıralama işləyir — <strong>səhvi tapmır</strong>.</li>"
     "</ul>"
     "<p><strong>Açıq xəta</strong> — ən yaxşı sənədləşmədir: mesajda icazəli "
     "sütunların siyahısı var.</p>")
addim(1, "Hücumu sına")
bash("""
B=http://localhost:4000/api/v1/struktur/merkezler

# Duzgun siralama
curl -s "$B?siralama_sah=ad&limit=2" | head -c 100

# Hucum cehdi
curl -s "$B?siralama_sah=id;DROP%20TABLE%20struktur.shobeler--" | python3 -m json.tool
""")
cixis("""
[{"id":1,"ad":"Elmi katiblik",...}]

{
  "ugur": false,
  "xeta": {
    "kod": "YANLIS_SORGU",
    "mesaj": "Bu sutun uzre siralama mumkun deyil: \"id;DROP TABLE struktur.shobeler--\". Icazeli sutunlar: id, ad, tip, unvan"
  },
  "yol": "/api/v1/struktur/merkezler?siralama_sah=...",
  "vaxt": "2026-09-19T18:41:30.000Z"
}
""")
yoxlama(11, "Cədvəl yerindədir?",
        "<pre><code>psql -U arti_user -d arti_baza -c \"SELECT count(*) FROM struktur.shobeler;\"\n"
        "#  count\n# -------\n#     36    &lt;-- toxunulmadi</code></pre>")

# ══════════════════ 12 ══════════════════
A('<h2 id="b12">12. Tam CRUD servisi</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Servisi tam CRUD + səhifələmə + filtr ilə yenidən yazacağıq: "
     "<strong>6 metod</strong>.</p>")
A('<table>')
A('  <tr><th>Metod</th><th>HTTP</th><th>Nə edir</th></tr>')
A('  <tr><td><code>merkezler(dto)</code></td><td>GET</td><td>Səhifələnmiş, filtreli, sıralanmış siyahı</td></tr>')
A('  <tr><td><code>merkez(id)</code></td><td>GET</td><td>Bir mərkəz — yoxdursa 404</td></tr>')
A('  <tr><td><code>yarat(dto)</code></td><td>POST</td><td>Yeni mərkəz — ad tutulubsa 409</td></tr>')
A('  <tr><td><code>yenile(id, dto)</code></td><td>PATCH</td><td>Qismən yenilə</td></tr>')
A('  <tr><td><code>sil(id)</code></td><td>DELETE</td><td>Sil — bağlı şöbə varsa 409</td></tr>')
A('  <tr><td><code>merkezStatistikasi()</code></td><td>GET</td><td>Mərkəz üzrə şöbə və əməkdaş sayı</td></tr>')
A('</table>')
fayl_yaz("src/struktur/struktur.service.ts")
blok("block-izah", "İZAH — ən vacib üç məqam",
     "<p><strong>1. Eyni ad yoxlaması:</strong></p>")
ts("""
private async adYoxla(ad: string, xaricId?: number): Promise<void> {
  const setirler = await this.prisma.$queryRaw<{ id: number }[]>`
    SELECT id::int FROM struktur.merkezler
     WHERE lower(ad) = lower(${ad})
       AND (${xaricId ?? null}::int IS NULL OR id <> ${xaricId ?? null})`;
  if (setirler.length) throw new ConflictException(...);
}
""")
blok("block-ipucu", "💡 `xaricId` NƏ ÜÇÜNDÜR?",
     "<p>Yeniləmə zamanı <strong>özünü</strong> konflikt saymamaq üçün. "
     "Mərkəzin adını dəyişmədən telefonunu yeniləyirsinizsə, "
     "<code>adYoxla</code> həmin sətri tapıb 'artıq var' deyərdi. "
     "<code>id &lt;&gt; xaricId</code> bunun qarşısını alır.</p>")
blok("block-izah", "İZAH — silmə qaydası",
     "<p>Xarici açar (<code>shobeler.merkez_id → merkezler.id</code>) "
     "mərkəzi silməyə <strong>icazə vermir</strong>:</p>")
cixis("""
ERROR: update or delete on table "merkezler" violates foreign key
       constraint "shobeler_merkez_id_fkey" on table "shobeler"
""")
blok("block-olmaz", "OLMASA NƏ OLAR — yoxlama olmadan",
     "<p>İstifadəçi PostgreSQL xətası görərdi:</p>"
     "<pre><code>{ \"statusCode\": 500, \"message\": \"Internal server error\" }</code></pre>"
     "<p>Səbəbi bilməzdi. Biz isə <strong>əvvəlcədən</strong> yoxlayırıq və "
     "aydın mesaj veririk:</p>")
json_("""{
  "ugur": false,
  "xeta": {
    "kod": "TOQQUSMA",
    "mesaj": "Bu merkeze 7 shobe baglidir — evvelce onlari kocurun"
  }
}""")
blok("block-evez", "ƏVƏZİNDƏ — soft delete",
     "<p>Silmək yerinə <code>aktiv = false</code> etmək:</p>"
     "<table>"
     "<tr><th>Yanaşma</th><th>Üstünlük</th><th>Çatışmazlıq</th></tr>"
     "<tr><td><strong>Hard delete</strong> (bizim)</td><td>Sadə, yer az</td><td>Geri qaytarmaq olmur</td></tr>"
     "<tr><td>Soft delete</td><td>Tarixçə qalır, geri qaytarıla bilər</td><td>Hər sorğuda <code>WHERE aktiv</code></td></tr>"
     "</table>"
     "<p>Kadr və maliyyə məlumatlarında soft delete daha doğrudur — "
     "sənəd tarixçəsi pozulmamalıdır.</p>")

# ══════════════════ 13 ══════════════════
A('<h2 id="b13">13. Tam CRUD controller</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Controller-i 6 endpoint ilə yazacağıq.</p>")
fayl_yaz("src/struktur/struktur.controller.ts")
blok("block-izah", "İZAH — HTTP kodları",
     "<table>"
     "<tr><th>Metod</th><th>Uğurlu kod</th><th>Nə qaytarır</th></tr>"
     "<tr><td><code>GET</code></td><td>200</td><td>Məlumat</td></tr>"
     "<tr><td><code>POST</code></td><td><strong>201</strong></td><td>Yaradılmış obyekt</td></tr>"
     "<tr><td><code>PATCH</code></td><td>200</td><td>Yenilənmiş obyekt</td></tr>"
     "<tr><td><code>DELETE</code></td><td><strong>200</strong> (bizdə)</td><td>Təsdiq</td></tr>"
     "</table>")
blok("block-xeber", "⚠️ DELETE STANDART OLARAQ 200 QAYTARIR — 204 DEYİL",
     "<p>NestJS <code>@Delete()</code> üçün susmaya görə <strong>200</strong> verir. "
     "Əgər <strong>204 No Content</strong> istəyirsinizsə:</p>")
ts("""
@Delete(':id')
@HttpCode(HttpStatus.NO_CONTENT)     // 204 — cavab govdesi olmaz
sil(@Param('id', ParseIntPipe) id: number) {
  return this.struktur.sil(id);
}
""")
blok("block-ipucu", "💡 HANSI SEÇİLMƏLİ?",
     "<table>"
     "<tr><th>Kod</th><th>Nə vaxt</th></tr>"
     "<tr><td>204 No Content</td><td>Silmə uğurludur, əlavə məlumat lazım deyil</td></tr>"
     "<tr><td>200 + gövdə</td><td>Frontend silinən obyekti <strong>siyahıdan çıxarmalıdır</strong></td></tr>"
     "</table>"
     "<p>Biz 200 qaytarırıq — frontend <code>id</code>-ni alıb siyahıdan dərhal silə bilir.</p>")
blok("block-izah", "İZAH — @ApiResponse nə üçündür?",
     "<p>Swagger sənədində <strong>hansı xətaların mümkün olduğunu</strong> göstərir. "
     "Frontend komandası kod oxumadan bilir:</p>")
ts("""
@Post()
@ApiResponse({ status: 201, description: 'Yaradildi' })
@ApiResponse({ status: 409, description: 'Bu adla merkez artiq var' })
yarat(@Body() dto: CreateMerkezDto): Promise<Merkez> { ... }
""")

# ══════════════════ 14 ══════════════════
A('<h2 id="b14">14. Kadrlar modulu — filtr qurucusu</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Ən böyük modulu quracağıq: <strong>6 cədvəlli birləşmə</strong>, "
     "9 filtr sahəsi, axtarış və səhifələmə.</p>")
fayl_yaz("src/kadrlar/dto/emekdas-filtr.dto.ts")
blok("block-izah", "İZAH — filtr sahələri",
     "<table>"
     "<tr><th>Sahə</th><th>SQL</th><th>Nə üçün</th></tr>"
     "<tr><td><code>merkez_id</code></td><td><code>e.merkez_id = $n</code></td><td>Mərkəz üzrə</td></tr>"
     "<tr><td><code>shobe_id</code></td><td><code>e.shobe_id = $n</code></td><td>Şöbə üzrə</td></tr>"
     "<tr><td><code>vezife_id</code></td><td><code>e.vezife_id = $n</code></td><td>Vəzifə üzrə</td></tr>"
     "<tr><td><code>elmi_derece_id</code></td><td><code>e.elmi_derece_id = $n</code></td><td>Elmi dərəcə üzrə</td></tr>"
     "<tr><td><code>aktiv</code></td><td><code>e.aktiv = $n</code></td><td>İşdən çıxanları gizlət</td></tr>"
     "<tr><td><code>min_maas</code></td><td><code>e.maas &gt;= $n</code></td><td>Aralıq filtri</td></tr>"
     "<tr><td><code>max_maas</code></td><td><code>e.maas &lt;= $n</code></td><td>Aralıq filtri</td></tr>"
     "</table>")
blok("block-ne", "NƏ EDƏCƏYİK — filtr qurucusu",
     "<p>Filtri <strong>dinamik SQL</strong>-ə çevirəcəyik. Bu, ən mürəkkəb hissədir.</p>")
addim(1, "Servisi yaz")
fayl_yaz("src/kadrlar/kadrlar.service.ts")
blok("block-izah", "İZAH — filtr qurucusunun məntiqi",
     "<p>Metod iki şey qaytarır: <strong>WHERE hissəsi</strong> və "
     "<strong>parametrlər massivi</strong>:</p>")
ts("""
private sertQur(dto: EmekdasFiltrDto) {
  const sertler: string[] = [];
  const parametrler: unknown[] = [];
  let n = 1;                       // parametr saygaci

  if (dto.axtar) {
    sertler.push(`(e.ad ILIKE $${n} OR e.soyad ILIKE $${n} OR ...)`);
    parametrler.push(`%${dto.axtar}%`);
    n++;                           // novbeti parametr ucun artir
  }
  ...
  return { where: sertler.length ? `WHERE ${sertler.join(' AND ')}` : '',
           parametrler };
}
""")
blok("block-ipucu", "💡 NİYƏ «$1, $2, …» SAYĞACI?",
     "<p>PostgreSQL parametrləri <strong>mövqeyə görə</strong> oxuyur: "
     "<code>$1</code> birinci, <code>$2</code> ikinci.</p>"
     "<p>Filtr dinamik olduğu üçün parametr sayı dəyişir:</p>"
     "<table>"
     "<tr><th>Sorğu</th><th>Parametrlər</th></tr>"
     "<tr><td><code>?axtar=elmi</code></td><td><code>$1</code> = <code>%elmi%</code></td></tr>"
     "<tr><td><code>?axtar=elmi&amp;merkez_id=2</code></td><td><code>$1</code> = <code>%elmi%</code>, <code>$2</code> = <code>2</code></td></tr>"
     "<tr><td><code>?merkez_id=2</code></td><td><code>$1</code> = <code>2</code></td></tr>"
     "</table>"
     "<p>Sayğac (<code>n</code>) hər əlavə olunan parametrlə artır və "
     "<code>$n</code> düzgün nömrəni alır.</p>")
blok("block-xeber", "⚠️ SƏHV PARAMETR NÖMRƏSİ — ƏN ÇOX EDİLƏN XƏTA",
     "<p>Sayğacı artırmağı unutsanız, iki filtr eyni parametri oxuyar:</p>")
sql("""
-- SEHV: her ikisi $1 oxuyur
WHERE ad ILIKE $1 AND merkez_id = $1
-- Netice: "operator does not exist: integer ~~ text"

-- DOĞRU
WHERE ad ILIKE $1 AND merkez_id = $2
""")
blok("block-izah", "İZAH — eyni filtri SAYMAQ və SEÇMƏK üçün",
     "<p><code>sertQur()</code> iki yerdə işlədilir:</p>")
ts("""
// 1) Setirleri sec
const setirler = await this.prisma.$queryRawUnsafe(
  `SELECT ${SAHELER} ${BIRLESME} ${where}
    ORDER BY ${sutun} ${istiqamet}
    LIMIT $${parametrler.length + 1} OFFSET $${parametrler.length + 2}`,
  ...parametrler, dto.limit, dto.offset,
);

// 2) UMRI sayi hesabla — EYNI filtre ile
const cem = await this.prisma.$queryRawUnsafe(
  `SELECT count(*)::int AS cem ${BIRLESME} ${where}`,
  ...parametrler,
);
""")
blok("block-olmaz", "OLMASA NƏ OLAR — say ayrı hesablansa",
     "<p>Filtrsiz <code>count(*)</code> götürsək, meta səhv olar:</p>"
     "<pre><code>?merkez_id=10    ->  data: 3 setir,  meta.cem: 14   ❌\n"
     "                    'Sehife 1/1' gosteriler, halbuki 1 sehifedir</code></pre>"
     "<p><strong>Qayda:</strong> <code>count</code> və <code>select</code> "
     "həmişə <strong>eyni</strong> filtri işlətməlidir.</p>")

# ══════════════════ 15 ══════════════════
A('<h2 id="b15">15. Kadrlar — axtarış, səhifələmə, sıralama</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Controller və modulu yazıb canlı sınayacağıq.</p>")
fayl_yaz("src/kadrlar/kadrlar.controller.ts")
fayl_yaz("src/kadrlar/kadrlar.module.ts")
blok("block-izah", "İZAH — tam profil nə qaytarır?",
     "<p><code>SELECT</code> hissəsi <strong>6 cədvəli</strong> birləşdirir:</p>")
sql("""
SELECT e.id::int                                   AS id,
       e.soyad || ' ' || e.ad || ' ' || e.ata_adi AS tam_adi,
       v.ad                                        AS vezife,
       s.ad                                        AS shobe,
       m.ad                                        AS merkez,
       c.ad                                        AS cins,
       d.ad                                        AS elmi_derece,
       a.ad                                        AS elmi_ad,
       e.email, e.telefon,
       e.ise_baslama::text                         AS ise_baslama,
       e.maas::float8                              AS maas,
       e.aktiv
  FROM kadrlar.emekdaslar e
  LEFT JOIN struktur.vezifeler   v ON v.id = e.vezife_id
  LEFT JOIN struktur.shobeler    s ON s.id = e.shobe_id
  LEFT JOIN struktur.merkezler   m ON m.id = e.merkez_id
  LEFT JOIN ortaq.cinsiyyet      c ON c.id = e.cinsiyyet_id
  LEFT JOIN ortaq.elmi_dereceler d ON d.id = e.elmi_derece_id
  LEFT JOIN ortaq.elmi_adlar     a ON a.id = e.elmi_ad_id
""")
blok("block-xeber", "⚠️ LEFT JOIN vs INNER JOIN",
     "<table>"
     "<tr><th>Növ</th><th>Nəticə</th></tr>"
     "<tr><td><code>JOIN</code> (INNER)</td><td>Uyğunluq yoxdursa sətir <strong>itir</strong></td></tr>"
     "<tr><td><code>LEFT JOIN</code></td><td>Uyğunluq yoxdursa <code>NULL</code> qaytarır</td></tr>"
     "</table>"
     "<p>Şöbəsi təyin olunmamış əməkdaş <code>JOIN</code> ilə siyahıdan "
     "<strong>tamamilə yox olar</strong>. Axtarış nəticəsində 'itkin əməkdaş' "
     "problemi belə yaranır.</p>")

addim(1, "Modulu qeyd et")
fayl_yaz("src/app.module.ts")
blok("block-xeber", "⚠️ MODULU QEYD ETMƏK UNUDULSA",
     "<p>Server işləyər, lakin endpoint <strong>404</strong> qaytarar. "
     "Xəta mesajı yoxdur — ən bezdirici haldır.</p>"
     "<p><strong>Qayda:</strong> yeni modul yaratdıqdan sonra "
     "<code>app.module.ts</code>-ə 2 sətir əlavə et:</p>")
ts("""
import { YeniModule } from './yeni/yeni.module.js';   // 1) import

@Module({
  imports: [
    ...
    YeniModule,                                        // 2) siyahiya
  ],
})
""")

addim(2, "Serveri işə sal və sına")
bash("""
cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST
npm run build
npm run start:dev
""")
bash("""
K=http://localhost:4000/api/v1/kadrlar/emekdaslar

# Sehifeleme
curl -s "$K?limit=3" | python3 -m json.tool | head -12

# Axtaris
curl -s "$K?axtar=elnur" | python3 -c "
import json,sys; d=json.load(sys.stdin)
for r in d['data']: print(r['tam_adi'], '|', r['email'])"

# Filtr: merkez + maas araligi + siralama
curl -s "$K?merkez_id=10&min_maas=1000&siralama=desc&siralama_sah=maas" \\
  | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('cem:', d['meta']['cem'])
for r in d['data']: print('  %-24s %8.2f' % (r['tam_adi'], r['maas']))"
""")
cixis("""
{ "data": [ { "id": 1, "tam_adi": "Əliyev Elnur Qəzənfər",
              "vezife": "Direktor", "merkez": "Elmi katiblik",
              "maas": 3500, ... } ],
  "meta": { "sehife": 1, "limit": 3, "cem": 14, "sehife_sayi": 5 } }

Əliyev Elnur Qəzənfər | elnur.eliyev@arti.edu.az

cem: 3
  İsmayılov Tural Mübariz     1900.00
  Əliyeva Sevinc Kamran       1400.00
  Rzayeva Günel Azər          1100.00
""")
yoxlama(15, "Kadrlar modulu",
        "<pre><code>curl -s http://localhost:4000/api/v1/kadrlar/emekdaslar/icmal\n\n"
        "{ \"merkez_uzre\": [ { \"merkez\": \"Elmi katiblik\",\n"
        "                      \"emekdas\": 2, \"orta_maas\": 2850, \"fond\": 5700 } ],\n"
        "  \"umumi_fond\": 33000, \"aktiv_say\": 14 }</code></pre>")

# ══════════════════ 16 ══════════════════
A('<h2 id="b16">16. Hesabat modulu — view və funksiyalar</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Bazada hazır olan <strong>8 view</strong> və <strong>10 funksiyanı</strong> "
     "API-yə çıxaracağıq.</p>")
blok("block-niye", "NİYƏ VIEW-LARI İSTİFADƏ EDİRİK?",
     "<p>Bazada artıq hazır JOIN-lar var. Onları yenidən yazmaq:</p>"
     "<ul>"
     "<li>Kod təkrarı yaradır;</li>"
     "<li>İki yerdə məntiq — biri dəyişsə, digəri köhnələr;</li>"
     "<li>Optimallaşdırma imkanı itir.</li>"
     "</ul>")
fayl_yaz("src/hesabatlar/hesabatlar.service.ts")
blok("block-izah", "İZAH — hesabat metodları",
     "<table>"
     "<tr><th>Metod</th><th>Mənbə</th><th>Nə qaytarır</th></tr>"
     "<tr><td><code>umumiIcmal()</code></td><td>4 sorğu</td><td>Dashboard üçün əsas rəqəmlər</td></tr>"
     "<tr><td><code>gorunusler()</code></td><td><code>information_schema.views</code></td><td>8 view-un siyahısı</td></tr>"
     "<tr><td><code>merkezShobe()</code></td><td><code>struktur.v_merkez_shobe_sayi</code></td><td>Mərkəz üzrə şöbə sayı</td></tr>"
     "<tr><td><code>emekdasTam()</code></td><td><code>kadrlar.v_emekdas_tam</code></td><td>5 cədvəlli profil</td></tr>"
     "<tr><td><code>budceIstifadesi()</code></td><td><code>maliyye.v_budce_istifadesi</code></td><td>Plan / xərclənmiş / qalıq</td></tr>"
     "<tr><td><code>telimQruplari()</code></td><td><code>tehsil.v_telim_qrup_istirakci_sayi</code></td><td>Qrup + iştirakçı sayı</td></tr>"
     "<tr><td><code>funksiyalar()</code></td><td>4 funksiya</td><td>Fond, orta bal, büdcə cəmi</td></tr>"
     "<tr><td><code>budceIcmali()</code></td><td><code>GROUP BY ROLLUP</code></td><td>İl üzrə + CƏMİ sətri</td></tr>"
     "<tr><td><code>sonAudit()</code></td><td><code>audit.audit_log</code></td><td>Son dəyişikliklər</td></tr>"
     "</table>")
blok("block-ipucu", "💡 FUNKSİYANI SQL-DƏ ÇAĞIRMAQ",
     "<p>Bazadaxili funksiyalar adi sütun kimi çağırılır:</p>")
sql("""
SELECT kadrlar.fn_maas_fondu()::float8              AS maas_fondu,
       tehsil.fn_sertifikasiya_ortalamasi()::float8 AS orta_bal,
       maliyye.fn_budce_il_cemi(2026)::float8       AS budce_2026;
""")
blok("block-xeber", "⚠️ FUNKSİYA NƏTİCƏSİ CAST EDİLMƏLİDİR",
     "<p><code>numeric</code> qaytaran funksiya JavaScript-də "
     "<strong>sətir</strong> olur:</p>"
     "<pre><code>\"maas_fondu\": \"33000.00\"     ❌ setir</code></pre>"
     "<p><code>::float8</code> əlavə etməsək, frontend toplama əvəzinə "
     "<strong>birləşdirmə</strong> edər: <code>\"33000.00\" + 1000 = \"33000.001000\"</code>.</p>")
fayl_yaz("src/hesabatlar/hesabatlar.controller.ts")
fayl_yaz("src/hesabatlar/hesabatlar.module.ts")
blok("block-izah", "İZAH — ROLLUP nə verir?",
     "<p>Adi <code>GROUP BY</code> yalnız qrupları göstərir. "
     "<code>ROLLUP</code> isə <strong>əlavə yekun sətri</strong> əlavə edir:</p>")
cixis("""
  il  | setir |   mebleg
------+-------+-------------
 2024 |     1 |  3900000.00
 2025 |     3 |  4585000.00
 2026 |     3 |  4970000.00
 2027 |     3 |  5350000.00
 CƏMİ |    10 | 18805000.00     <-- ROLLUP bunu OZU elave edir
""")
blok("block-olmaz", "OLMASA NƏ OLAR — yekun əl ilə hesablansa",
     "<p>İki ayrı sorğu yazıb nəticələri birləşdirməli olardıq. "
     "Üstəlik <strong>tarix filtri</strong> əlavə etsək, yekun da "
     "həmin filtrlə hesablanmalıdır — əl ilə etsək, unudular.</p>")

yoxlama(16, "Hesabat endpoint-ləri",
        "<pre><code>curl -s http://localhost:4000/api/v1/hesabatlar/icmal\n\n"
        "{\n"
        "  \"cedvel_sayi\": 48,\n"
        "  \"gorunus_sayi\": 8,\n"
        "  \"aktiv_emekdas\": 14,\n"
        "  \"emek_haqqi_fondu\": 33000,\n"
        "  \"davam_eden_layihe\": 6\n"
        "}</code></pre>")

# ══════════════════ 17 ══════════════════
A('<h2 id="b17">17. Sağlamlıq endpoint-i</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Serverin və bazanın <strong>işlək olduğunu</strong> yoxlayan endpoint "
     "yaradacağıq.</p>")
blok("block-niye", "NİYƏ LAZIMDIR",
     "<table>"
     "<tr><th>İstifadəçi</th><th>Nə üçün</th></tr>"
     "<tr><td>İnkişafçı</td><td>'Server işləyir, baza qoşulub?' — bir sorğu ilə</td></tr>"
     "<tr><td>Docker / Kubernetes</td><td>Konteinera <strong>canlıdır</strong> siqnalı</td></tr>"
     "<tr><td>Monitorinq (UptimeRobot)</td><td>Hər 5 dəqiqədə yoxlayır</td></tr>"
     "<tr><td>Nginx</td><td>Yük balanslaşdırması üçün</td></tr>"
     "</table>")
blok("block-hara", "HARA", "<p><code>src/saglamliq/</code></p>")
fayl_yaz("src/saglamliq/saglamliq.controller.ts")
fayl_yaz("src/saglamliq/saglamliq.module.ts")
blok("block-izah", "İZAH — nə üçün bazaya sorğu göndəririk?",
     "<p>Sadəcə <code>{ status: 'ok' }</code> qaytarmaq <strong>kifayət deyil</strong>. "
     "Server işləyə bilər, lakin baza bağlı ola bilər.</p>"
     "<p>Buna görə <code>information_schema</code>-dan real sorğu göndəririk. "
     "Baza cavab verməzsə, endpoint <strong>500</strong> qaytarır — "
     "monitorinq dərhal xəbər tutur.</p>")
blok("block-ipucu", "💡 «gecikme_ms» NƏ ÜÇÜNDÜR?",
     "<p>Sorğunun nə qədər vaxt aldığını göstərir. Adətən 1-5 ms olur. "
     "Əgər <strong>500 ms</strong>-dən çoxdursa — baza yüklənib və ya "
     "şəbəkədə problem var. Bu, erkən xəbərdarlıq siqnalıdır.</p>")
yoxlama(17, "Sağlamlıq",
        "<pre><code>curl -s http://localhost:4000/api/v1/saglamliq | python3 -m json.tool\n\n"
        "{\n"
        "  \"status\": \"saglam\",\n"
        "  \"baza\": { \"qosulub\": true, \"cedvel_sayi\": 48, \"gecikme_ms\": 2 },\n"
        "  \"versiya\": \"0.0.1\",\n"
        "  \"vaxt\": \"2026-09-19T18:41:00.000Z\"\n"
        "}</code></pre>")

# ══════════════════ 18 ══════════════════
A('<h2 id="b18">18. app.module.ts — modul qeydiyyatı</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Bütün modulları bir yerə yığacağıq.</p>")
bash("""
cat > ~/Deepseek_ARTI/DS_Backend/src/app.module.ts <<'EOF'
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module.js';
import { SaglamliqModule } from './saglamliq/saglamliq.module.js';
import { StrukturModule } from './struktur/struktur.module.js';
import { KadrlarModule } from './kadrlar/kadrlar.module.js';
import { HesabatlarModule } from './hesabatlar/hesabatlar.module.js';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    SaglamliqModule,
    StrukturModule,
    KadrlarModule,
    HesabatlarModule,
  ],
})
export class AppModule {}
EOF
""")
A('<table>')
A('  <tr><th>Modul</th><th>Endpoint sayı</th><th>Nə edir</th></tr>')
A('  <tr><td><code>SaglamliqModule</code></td><td>2</td><td>Sağlamlıq + kök</td></tr>')
A('  <tr><td><code>StrukturModule</code></td><td>6</td><td>Mərkəzlər — tam CRUD</td></tr>')
A('  <tr><td><code>KadrlarModule</code></td><td>3</td><td>Əməkdaşlar — filtr, axtarış</td></tr>')
A('  <tr><td><code>HesabatlarModule</code></td><td>9</td><td>View və funksiyalar</td></tr>')
A('  <tr><td><strong>CƏMİ</strong></td><td><strong>20</strong></td><td></td></tr>')
A('</table>')
yoxlama(18, "Bütün marshrutlar",
        "<pre><code>grep 'Mapped' server.log | wc -l\n# 20</code></pre>")

# ══════════════════ 19 ══════════════════
A('<h2 id="b19">19. Unit testlər — DTO və servis</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>İki qat üçün test yazacağıq: <strong>DTO validasiyası</strong> və "
     "<strong>servis məntiqi</strong>.</p>")
blok("block-niye", "NİYƏ İKİ QAT?",
     "<table>"
     "<tr><th>Qat</th><th>Nə yoxlanılır</th><th>Sürət</th></tr>"
     "<tr><td>DTO</td><td>Qaydalar düzgün işləyirmi?</td><td>Çox sürətli</td></tr>"
     "<tr><td>Servis</td><td>SQL qurulması, xəta atılması</td><td>Sürətli (saxta Prisma)</td></tr>"
     "<tr><td>e2e</td><td>Bütün zəncir — HTTP-dən bazaya</td><td>Yavaş</td></tr>"
     "</table>"
     "<p>Aşağı qat sınsa, yuxarı qatı işlətməyə ehtiyac yoxdur — "
     "xətanı <strong>dərhal</strong> görürsünüz.</p>")
addim(1, "DTO testi")
fayl_yaz("src/common/dto/sehife.dto.spec.ts")
blok("block-izah", "İZAH — DTO-nu HTTP olmadan necə yoxlamaq?",
     "<p>İki funksiya kifayətdir:</p>")
ts("""
import { plainToInstance } from 'class-transformer';
import { validate } from 'class-validator';

const dto = plainToInstance(SehifeDto, { limit: 101 });  // JSON -> sinif
const xetalar = await validate(dto);                      // qaydalari yoxla
// xetalar -> ValidationError[] massivi
""")
blok("block-ipucu", "💡 `plainToInstance` `new`-DAN NƏ İLƏ FƏRQLƏNİR?",
     "<p><code>new SehifeDto()</code> yalnız default dəyərləri qoyur — "
     "<code>@Type()</code> çevrilməsi <strong>işləmir</strong>.</p>"
     "<p><code>plainToInstance</code> isə <code>ValidationPipe</code>-un "
     "etdiyi işi təkrarlayır: tip çevrilməsi + sinifə yığılma.</p>")
addim(2, "Servis testi")
fayl_yaz("src/struktur/struktur.service.spec.ts")
blok("block-izah", "İZAH — nə üçün `$queryRawUnsafe` ayrıca mock edilir?",
     "<p><code>merkezler()</code> <strong>iki</strong> fərqli metod işlədir:</p>"
     "<table>"
     "<tr><th>Metod</th><th>Nə üçün</th></tr>"
     "<tr><td><code>$queryRawUnsafe</code></td><td>Dinamik sütun adı lazım olduqda</td></tr>"
     "<tr><td><code>$queryRaw</code></td><td>Sabit SQL (template literal)</td></tr>"
     "<tr><td><code>$executeRaw</code></td><td>Yazma əməliyyatları</td></tr>"
     "</table>"
     "<p>Mock-da hər üçünü ayrıca yaratmalıyıq.</p>")
blok("block-xeber", "⚠️ SQL INJECTION TESTİ ƏN VACİB TESTDİR",
     "<p>Təhlükəsizlik testi funksional testdən <strong>daha vacibdir</strong> — "
     "çünki səhv nəticəsi geri qaytarıla bilmir:</p>")
ts("""
it('icazesiz sutun BadRequestException atir', async () => {
  await expect(service.merkezler(filtr({ siralama_sah: 'DROP TABLE' })))
    .rejects.toThrow(BadRequestException);
  expect(prisma.$queryRawUnsafe).not.toHaveBeenCalled();   // SQL HEÇ QURULMADI
});

it('SQL fragment sizişi bloklanir', async () => {
  for (const hucum of ['ad; DROP TABLE', '1=1 --', 'ad) UNION SELECT']) {
    await expect(service.merkezler(filtr({ siralama_sah: hucum })))
      .rejects.toThrow(BadRequestException);
  }
});
""")
blok("block-ipucu", "💡 `not.toHaveBeenCalled()` NƏ SÜBUT EDİR?",
     "<p>Xəta atmaqla yanaşı, funksiyanın <strong>heç çağırılmadığını</strong> "
     "yoxlayırıq. Yəni pis SQL <strong>bazaya heç getmədi</strong> — "
     "yoxlama <em>ondan əvvəl</em> baş verdi.</p>")
bash("""
cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST
npm test
""")
cixis("""
 ✓ src/common/dto/sehife.dto.spec.ts (8 tests) 4ms
 ✓ src/struktur/struktur.service.spec.ts (17 tests) 4ms

 Test Files  2 passed (2)
      Tests  25 passed (25)
""")

# ══════════════════ 20 ══════════════════
A('<h2 id="b20">20. e2e testlər — 30 test</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Bütün HTTP qatını <strong>real server</strong> kimi sınayacağıq: "
     "validasiya, filtr, CRUD, xəta formatları.</p>")
blok("block-niye", "NİYƏ e2e LAZIMDIR?",
     "<p>Unit testlər servisi ayrıca yoxlayır, lakin <strong>zənciri</strong> yox: "
     "ValidationPipe + guard + filter + controller + service.</p>"
     "<table>"
     "<tr><th>Yalnız unit test olsa</th><th>e2e də olsa</th></tr>"
     "<tr><td>Pipe səhv qoşulub — bilinməz</td><td>Dərhal görünər</td></tr>"
     "<tr><td>Global prefiks unudulub — bilinməz</td><td>404 testi tutar</td></tr>"
     "<tr><td>Xəta formatı dəyişib — bilinməz</td><td>Format testi tutar</td></tr>"
     "</table>")
addim(1, "e2e konfiqurasiyası")
blok("block-xeber", "⚠️ EXCLUDE SƏTRİ VACİBDİR",
     "<p><code>vitest.config.ts</code>-də e2e testləri "
     "<strong>xaric edilməlidir</strong>, əks halda <code>npm test</code> "
     "server tələb edən testləri də götürür və uğursuz olur:</p>")
ts("""
// vitest.config.ts  (unit testler)
export default defineConfig({
  test: {
    include: ['**/*.spec.ts'],
    exclude: ['**/*.e2e-spec.ts', 'node_modules/**'],   // <- VACIB
  },
});
""")
blok("block-izah", "İZAH — iki ayrı konfiqurasiya",
     "<table>"
     "<tr><th>Fayl</th><th>Nə götürür</th><th>Əmr</th></tr>"
     "<tr><td><code>vitest.config.ts</code></td><td><code>*.spec.ts</code></td><td><code>npm test</code></td></tr>"
     "<tr><td><code>vitest.config.e2e.ts</code></td><td><code>*.e2e-spec.ts</code></td><td><code>npx vitest run --config vitest.config.e2e.ts</code></td></tr>"
     "</table>")
addim(2, "e2e testini yaz")
fayl_yaz("test/backend2.e2e-spec.ts")
blok("block-izah", "İZAH — main.ts ilə EYNİ konfiqurasiya",
     "<p>Bu, e2e testlərinin <strong>ən vacib qaydasıdır</strong>:</p>")
ts("""
app.setGlobalPrefix('api/v1');
app.useGlobalPipes(new ValidationPipe({
  whitelist: true, forbidNonWhitelisted: true, transform: true,
}));
app.useGlobalFilters(new AllExceptionsFilter());
""")
blok("block-olmaz", "OLMASA NƏ OLAR — konfiqurasiya təkrarlanmasa",
     "<p>Test yaşıl olar, istehsalatda isə <strong>404</strong> gələr:</p>"
     "<table>"
     "<tr><th>Test konfiqurasiyası</th><th>Real server</th><th>Nəticə</th></tr>"
     "<tr><td>prefiks yox</td><td><code>/api/v1</code></td><td>Test <code>/struktur/...</code> yoxlayır, real isə <code>/api/v1/...</code> gözləyir</td></tr>"
     "<tr><td>filter yox</td><td>filter var</td><td>Xəta formatı testdə fərqli</td></tr>"
     "</table>"
     "<p>Test <strong>real davranışı</strong> yoxlamalıdır, ideal variantı yox.</p>")
addim(3, "Testləri işlət")
bash("""
cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST
npx vitest run --config vitest.config.e2e.ts
""")
cixis("""
 ✓ test/backend2.e2e-spec.ts (30 tests) 189ms

 Test Files  1 passed (1)
      Tests  30 passed (30)
""")
blok("block-izah", "İZAH — 30 test nə yoxlayır?",
     "<table>"
     "<tr><th>Qrup</th><th>Test</th><th>Nə yoxlanılır</th></tr>"
     "<tr><td>Sağlamlıq</td><td>3</td><td>Prefiks, baza qoşulması, kök endpoint</td></tr>"
     "<tr><td>Struktur GET</td><td>7</td><td>Səhifələmə, axtarış, 400/404</td></tr>"
     "<tr><td>Struktur CRUD</td><td>8</td><td>POST/PATCH/DELETE, 409, mass assignment</td></tr>"
     "<tr><td>Kadrlar</td><td>6</td><td>Filtr, sıralama, injection, icmal</td></tr>"
     "<tr><td>Hesabatlar</td><td>4</td><td>View, ROLLUP, funksiyalar</td></tr>"
     "<tr><td>Xəta formatı</td><td>2</td><td>404 və 400 formatları</td></tr>"
     "</table>")
blok("block-ipucu", "💡 TEST SAYĞACI",
     "<pre><code>npm test                                   # 25 unit\n"
     "npx vitest run --config vitest.config.e2e.ts   # 30 e2e\n"
     "# CƏMİ: 55 test</code></pre>")

# ══════════════════ 21 ══════════════════
A('<h2 id="b21">21. Xəta kitabçası</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Bu dərsdə rast gəlinən xətaları və həllini toplayacağıq.</p>")
A('<table>')
A('  <tr><th>Xəta</th><th>Səbəb</th><th>Həll</th></tr>')
XETALAR = [
    ("<code>property rol should not exist</code>",
     "<code>forbidNonWhitelisted: true</code> işləyir (yaxşı haldır!)",
     "DTO-ya sahə əlavə edin və ya göndərilən JSON-u düzəldin"),
    ("<code>limit must be an integer number</code>",
     "<code>@Type(() =&gt; Number)</code> yoxdur",
     "Dekoratoru əlavə edin — URL mətni rəqəmə çevrilmir"),
    ("<code>merkezler is not a function</code>",
     "Servis metodu adı dəyişib, controller köhnə qalıb",
     "<code>npm run build</code> — TypeScript göstərəcək"),
    ("<code>404</code> bütün endpoint-lərə",
     "Modul <code>app.module.ts</code>-də qeydiyyatsızdır",
     "<code>imports</code> siyahısına əlavə edin"),
    ("<code>operator does not exist: integer ~~ text</code>",
     "Filtr sayğacı səhv — iki şərt eyni <code>$n</code>-i oxuyur",
     "Hər parametrdən sonra <code>n++</code> edin"),
    ("<code>relation \"struktur.shobeler\" does not exist</code>",
     "Qlobal <code>DATABASE_URL</code> səhv bazaya aparır",
     "<code>unset DATABASE_URL PGHOST</code>"),
    ("<code>Cannot find module './dto/...</code>",
     "Backend import-da <code>.js</code> yoxdur",
     "Bütün nisbi importlara <code>.js</code> əlavə edin"),
    ("<code>Do not know how to serialize a BigInt</code>",
     "<code>count(*)::int</code> cast yoxdur",
     "Bütün <code>count</code> və <code>id</code>-lərə cast edin"),
    ("<code>numeric</code> sətir kimi gəlir (<code>\"33000.00\"</code>)",
     "<code>::float8</code> cast yoxdur",
     "Funksiya və view nəticələrini cast edin"),
    ("<code>The \"path\" argument must be of type string</code>",
     "<code>.env</code> faylı yoxdur",
     "<code>cp .env.example .env</code>"),
    ("<code>EADDRINUSE :::4000</code>",
     "Port tutulub",
     "<code>lsof -ti :4000 | xargs kill -9</code>"),
    ("<code>Cannot find module vitest/config</code>",
     "Dev asılılıqlar qurulmayıb",
     "<code>npm install -D vitest</code>"),
    ("e2e testləri <code>npm test</code>-də uğursuz olur",
     "<code>exclude</code> sətri yoxdur",
     "<code>vitest.config.ts</code>-ə <code>exclude</code> əlavə edin"),
    ("<code>Hello World!</code> testi 404 verir",
     "<code>AppController</code> <code>app.module.ts</code>-dən çıxarılıb",
     "Faylları silin — bu dərsdə real controller-lər var"),
]
for x, s2, h in XETALAR:
    A('  <tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (x, s2, h))
A('</table>')
blok("block-ipucu", "💡 SWAGGER-DƏN DİAQNOSTİKA",
     "<p><code>/docs</code> səhifəsi <strong>ən sürətli diaqnostika alətidir</strong>:</p>"
     "<table>"
     "<tr><th>Swagger-də görünür</th><th>Nəticə</th></tr>"
     "<tr><td>Endpoint yoxdur</td><td>Modul qeydiyyatsız</td></tr>"
     "<tr><td>Parametr yoxdur</td><td>DTO-da dekorator çatışmır</td></tr>"
     "<tr><td>Sxem boşdur</td><td><code>@ApiProperty</code> yoxdur</td></tr>"
     "</table>")

# ══════════════════ 22 ══════════════════
A('<h2 id="b22">22. Yoxlama siyahısı və növbəti dərs</h2>')
A('<div class="block block-yox">')
A('  <span class="block-title">YOXLAMA — BACKEND-2 HAZIRDIR?</span>')
A('  <table>')
A('    <tr><th>#</th><th>Yoxlama</th><th>Əmr / Gözlənilən</th></tr>')
SON = [
    ("Default fayllar silinib", "<code>ls src/app.controller.ts</code> → yoxdur"),
    ("SehifeDto var", "<code>ls src/common/dto/sehife.dto.ts</code>"),
    ("Xəta filtri var", "<code>ls src/common/filters/</code>"),
    ("Struktur DTO-ları (3)", "<code>ls src/struktur/dto/</code>"),
    ("Kadrlar modulu", "<code>ls src/kadrlar/</code>"),
    ("Hesabat modulu", "<code>ls src/hesabatlar/</code>"),
    ("Sağlamlıq modulu", "<code>ls src/saglamliq/</code>"),
    ("Modullar qeydiyyatda", "<code>grep -c Module src/app.module.ts</code> → 5"),
    ("Build keçir", "<code>npm run build</code> → exit 0"),
    ("Unit testlər", "<code>npm test</code> → 25 passed"),
    ("e2e testlər", "<code>npx vitest run --config vitest.config.e2e.ts</code> → 30 passed"),
    ("20 marshrut", "server logunda <code>Mapped</code> sayı"),
    ("Sağlamlıq işləyir", "<code>curl .../saglamliq</code> → <code>status: saglam</code>"),
    ("Səhifələmə", "<code>curl '...merkezler?limit=3'</code> → <code>meta.sehife_sayi</code>"),
    ("Validasiya 400 verir", "<code>curl -X POST ... -d '{\"ad\":\"AB\"}'</code>"),
    ("Mass assignment bloklanır", "<code>-d '{\"ad\":\"Test\",\"rol\":\"admin\"}'</code> → 400"),
    ("Dublikat 409 verir", "eyni adla iki POST"),
    ("SQL injection bloklanır", "<code>?siralama_sah=DROP%20TABLE</code> → 400"),
    ("Xəta formatı vahiddir", "cavabda <code>ugur</code>, <code>xeta.kod</code>, <code>yol</code>, <code>vaxt</code>"),
    ("Swagger açılır", "<code>open localhost:4000/docs</code>"),
]
for i, (y, g) in enumerate(SON, 1):
    A('    <tr><td>%d</td><td>%s</td><td>%s</td></tr>' % (i, y, g))
A('  </table>')
A('</div>')

blok("block-ne", "NƏ GƏLİR — Backend-3",
     "<table>"
     "<tr><th>#</th><th>Mövzu</th></tr>"
     "<tr><td>1</td><td><strong>JWT autentifikasiya</strong> — login, token</td></tr>"
     "<tr><td>2</td><td><strong>Rollar (RBAC)</strong> — admin, mühendis, maliyyəçi, baxıcı</td></tr>"
     "<tr><td>3</td><td><strong>Guard-lar</strong> — <code>@UseGuards</code>, <code>@Roles</code></td></tr>"
     "<tr><td>4</td><td><strong>Şifrə hash</strong> — bcrypt</td></tr>"
     "<tr><td>5</td><td><strong>İstifadəçi idarəsi</strong> — <code>kadrlar.istifadeciler</code></td></tr>"
     "<tr><td>6</td><td><strong>Səviyyəli icazə</strong> — öz məlumatını görmək</td></tr>"
     "<tr><td>7</td><td><strong>Audit interceptor</strong> — kim nəyi dəyişdi</td></tr>"
     "</table>")
A('<div class="success-box">'
  '<strong>Backend-2 tamamlandı.</strong> API artıq təhlükəsiz və '
  'proqramlaşdırıla biləndir: <strong>20 endpoint</strong>, '
  '<strong>55 test</strong>, vahid xəta formatı, SQL injection qoruması.'
  '</div>')

A('</div>')
A('<script>')
A("""  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('pre').forEach(function (pre) {
      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.textContent = '📋 KOPYALA';
      btn.addEventListener('click', async function (ev) {
        ev.preventDefault();
        var kod = pre.querySelector('code');
        var metn = kod ? kod.textContent : pre.textContent;
        try {
          await navigator.clipboard.writeText(metn);
          btn.textContent = '✅ KOPYALANDI';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = '📋 KOPYALA';
            btn.classList.remove('copied');
          }, 2000);
        } catch (err) {
          var ta = document.createElement('textarea');
          ta.value = metn;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          btn.textContent = '✅ KOPYALANDI';
          setTimeout(function () { btn.textContent = '📋 KOPYALA'; }, 2000);
        }
      });
      pre.insertBefore(btn, pre.firstChild);
    });
  });""")
A('</script>')
A('</body>')
A('</html>')

metn = "\n".join(H)
hedef = KOK / "DƏRSLƏR/DS_Backend-2.html"
hedef.write_text(metn, encoding="utf-8")
print("  yazıldı: %s" % hedef)
print("  sətir sayı: %d" % len(metn.splitlines()))
print("  həcm: %.1f KB" % (len(metn.encode()) / 1024))
print("  bölmə: %d" % metn.count('<h2 id="b'))
print("  kod bloku: %d" % metn.count('<pre data-lang='))
