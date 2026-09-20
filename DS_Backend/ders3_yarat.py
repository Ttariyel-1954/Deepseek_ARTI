# -*- coding: utf-8 -*-
"""DƏRSLƏR/DS_Backend-3.html dərsini yaradır.

Kodu BİRBAŞA sınaqdan keçmiş fayllardan oxuyur — bayt-dəqiqlik üçün.
Hədəf: >= 1700 sətir.
"""
from __future__ import annotations

import html
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent          # ~/Deepseek_ARTI
MENBE = Path("/tmp/bt4")                              # sınaqdan keçmiş nüsxə
CSS = (KOK / "DS_Baza/ders.css").read_text(encoding="utf-8").strip("\n")

H: list[str] = []
A = H.append

def e(m: str) -> str:
    return html.escape(str(m), quote=False)

def fayl(yol: str) -> str:
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

def fayl_yaz(yol: str) -> None:
    """mkdir -p + cat > bloku (mkdir MÜTLƏQDİR)."""
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
A('<title>DS Backend 3 — JWT autentifikasiya, rollar ve audit</title>')
A('<style>')
A(CSS)
A('</style>')
A('</head>')
A('<body>')
A('<div class="container">')
A('<header>')
A('  <div class="lesson-badge">DS_Backend · Hissə 3/4</div>')
A('  <h1>Backend 3 — JWT, rollar və audit</h1>')
A('  <p class="subtitle">Sistemi bağla, sonra açar paylaş — '
  'autentifikasiya, RBAC və hər dəyişikliyin izi</p>')
A('  <p class="meta">Layihə: <strong>Deepseek_ARTI</strong> · Blok: <code>DS_Backend</code> · '
  'NestJS 12 · Passport · JWT · bcrypt · 100 test</p>')
A('</header>')

# ── TOC ──
A('<div class="toc">')
A('  <h3>📚 Bu dərsdə nələr öyrənəcəksiniz</h3>')
A('  <ol>')
TOC = [
    "Backend-3 nə verir — xülasə",
    "Auth paketlərinin quraşdırılması",
    "Autentifikasiya nədir — session vs JWT",
    "JWT nədir — üç hissə",
    "Şifrə saxlama — heç vaxt düz mətn",
    "bcrypt — hash və compare",
    "LoginDto və QeydiyyatDto",
    "Rollar (RBAC) — dörd rol matrisi",
    "Dekoratorlar — @Roles, @Public, @CurrentUser",
    "JWT strategiyası",
    "JwtAuthGuard — qlobal «təhlükəsiz susmaya görə»",
    "RolesGuard — RBAC yoxlaması",
    "⚠️ REAL XƏTA: .env və modul yüklənmə sırası",
    "Auth servisi — login və timing attack qoruması",
    "Auth controller",
    "Auth modulu — registerAsync",
    "Audit interceptor",
    "app.module.ts — APP_GUARD sırası",
    "Endpoint-lərin qorunması",
    "Seed skripti",
    "Testlər — 38 unit + 62 e2e",
    "Backend-2 testlərinin yenilənməsi",
    "Xəta kitabçası",
    "Yoxlama siyahısı və növbəti dərs",
]
for i, t in enumerate(TOC, 1):
    A('    <li><a href="#b%d">%s</a></li>' % (i, t))
A('  </ol>')
A('</div>')

# ══════════════════ 1 ══════════════════
A('<h2 id="b1">1. Backend-3 nə verir — xülasə</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Backend-2-də API işləyirdi, lakin <strong>hər kəs hər şeyi edə bilirdi</strong>. "
     "İndi sistemi bağlayacağıq:</p>"
     "<table>"
     "<tr><th>#</th><th>Nə əlavə olunur</th><th>Nə üçün</th></tr>"
     "<tr><td>1</td><td><strong>JWT autentifikasiya</strong></td><td>Kim olduğunu bilmək</td></tr>"
     "<tr><td>2</td><td><strong>bcrypt şifrə hash</strong></td><td>Baza sızsa da şifrələr açılmasın</td></tr>"
     "<tr><td>3</td><td><strong>Rollar (RBAC)</strong></td><td>Hər kəs hər şeyi etməsin</td></tr>"
     "<tr><td>4</td><td><strong>Qlobal guard</strong></td><td>Yeni endpoint susmaya görə qorunsun</td></tr>"
     "<tr><td>5</td><td><strong>Audit interceptor</strong></td><td>Kim nəyi dəyişdi — iz qalsın</td></tr>"
     "<tr><td>6</td><td><strong>Seed skripti</strong></td><td>İstifadəçiləri tək əmrlə yaratmaq</td></tr>"
     "<tr><td>7</td><td><strong>100 test</strong></td><td>Təhlükəsizlik pozulmasın</td></tr>"
     "</table>")
blok("block-niye", "NİYƏ BU DƏRS ƏN VACİBDİR?",
     "<p>Backend-1 və -2 funksionallıq verdi. Backend-3 isə <strong>etimad</strong> verir. "
     "Bu olmasa:</p>"
     "<ul>"
     "<li>İstənilən şəxs bütün əməkdaşların maaşını görər;</li>"
     "<li>Kənar şəxs məlumatları silə bilər;</li>"
     "<li>Baza sızsa, bütün şifrələr açıq mətn kimi oxunar;</li>"
     "<li>'Bunu kim dəyişdi?' sualına cavab tapılmaz.</li>"
     "</ul>")
A('<div class="success-box">Bu dərsin sonunda API <strong>bağlı</strong> olacaq: '
  '24 endpoint, 4 rol, 100 test. Token olmadan heç nə işləməyəcək.</div>')

# ══════════════════ 2 ══════════════════
A('<h2 id="b2">2. Auth paketlərinin quraşdırılması</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Autentifikasiya üçün lazım olan 5 paketi quraşdıracağıq.</p>")
bash("""
cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST

npm install \\
  @nestjs/jwt@^12.0.0 \\
  @nestjs/passport@^12.0.0 \\
  passport@^0.7.0 \\
  passport-jwt@^4.0.1 \\
  bcryptjs@^3.0.0

npm install -D @types/passport-jwt@^4.0.1 @types/bcryptjs@^2.4.6
""")
blok("block-izah", "İZAH — hər paket nə edir?",
     "<table>"
     "<tr><th>Paket</th><th>Nə edir</th><th>Olmazsa</th></tr>"
     "<tr><td><code>@nestjs/jwt</code></td><td>Token imzalayır və yoxlayır</td>"
     "<td>Özümüz HMAC yazmalı olardıq</td></tr>"
     "<tr><td><code>@nestjs/passport</code></td><td>Passport-u NestJS-ə bağlayır</td>"
     "<td><code>PassportStrategy</code> tapılmır</td></tr>"
     "<tr><td><code>passport</code></td><td>Autentifikasiya çərçivəsi</td>"
     "<td>Strategiya işləmir</td></tr>"
     "<tr><td><code>passport-jwt</code></td><td>JWT strategiyası</td>"
     "<td>Bearer token oxunmur</td></tr>"
     "<tr><td><code>bcryptjs</code></td><td>Şifrə hash-ləyir</td>"
     "<td>Şifrələr açıq saxlanılardı</td></tr>"
     "</table>")
blok("block-ipucu", "💡 NİYƏ «bcryptjs», «bcrypt» YOX?",
     "<table>"
     "<tr><th>Paket</th><th>Nədir</th><th>Quraşdırma</th></tr>"
     "<tr><td><code>bcrypt</code></td><td>Native C++ modulu</td><td>Kompilyator tələb edir</td></tr>"
     "<tr><td><code>bcryptjs</code></td><td>Təmiz JavaScript</td><td>Hər yerdə işləyir ✅</td></tr>"
     "</table>"
     "<p>Native modul Docker-də və ARM-da problem yaradır. "
     "<code>bcryptjs</code> bir qədər yavaşdır, lakin <strong>hər platformada</strong> işləyir.</p>")
yoxlama(2, "Paketlər quraşdırıldı?",
        "<pre><code>for p in @nestjs/jwt @nestjs/passport passport passport-jwt bcryptjs; do\n"
        "  echo \"$p: $(node -p \"require('$p/package.json').version\")\"\n"
        "done\n\n"
        "@nestjs/jwt: 12.0.2\n@nestjs/passport: 12.0.0\n"
        "passport: 0.7.0\npassport-jwt: 4.0.1\nbcryptjs: 3.0.3</code></pre>")

# ══════════════════ 3 ══════════════════
A('<h2 id="b3">3. Autentifikasiya nədir — session vs JWT</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>İki yanaşmanı müqayisə edib JWT-ni seçmə səbəbini anlayacağıq.</p>")
A('<table>')
A('  <tr><th></th><th>Session (köhnə yol)</th><th>JWT (müasir)</th></tr>')
A('  <tr><td><strong>Harada saxlanılır</strong></td><td>Serverin yaddaşında / bazada</td>'
  '<td>Tokenin ÖZÜNDƏ (imzalı)</td></tr>')
A('  <tr><td><strong>Yoxlama</strong></td><td>Bazaya sorğu</td><td>İmza riyazi yoxlanılır</td></tr>')
A('  <tr><td><strong>Ölçəklənmə</strong></td><td>Çətin — hər server öz yaddaşını saxlayır</td>'
  '<td>Asan — istənilən server yoxlaya bilər</td></tr>')
A('  <tr><td><strong>Ləğv etmə</strong></td><td>Asan — session silinir</td>'
  '<td>Çətin — token bitənə qədər qüvvədədir</td></tr>')
A('  <tr><td><strong>Mobil tətbiq</strong></td><td>Çətin (cookie)</td><td>Asan (header)</td></tr>')
A('  <tr><td><strong>Ölçü</strong></td><td>Kiçik (session id)</td><td>Böyük (~200 simvol)</td></tr>')
A('</table>')
blok("block-izah", "İZAH — bizim seçim",
     "<p>ARTİ ERP üçün JWT seçirik, çünki:</p>"
     "<ul>"
     "<li>Frontend (Next.js) və backend (NestJS) <strong>ayrı</strong> portlardadır;</li>"
     "<li>Gələcəkdə mobil tətbiq və R Shiny paneli də qoşulacaq;</li>"
     "<li>Bir neçə server ola bilər (yük balanslaşdırması);</li>"
     "<li>Token müddəti qısadır (8 saat) — ləğv etmə problemi azalır.</li>"
     "</ul>")
blok("block-olmaz", "OLMASA NƏ OLAR — heç bir autentifikasiya",
     "<p>API tam açıq olar. Kənar şəxs bütün məlumatı oxuya, silə, dəyişə bilər:</p>")
bash("""
# Tokensiz məlumat çəkmək — bu İŞLƏMƏMƏLİDİR
curl -s http://localhost:4000/api/v1/kadrlar/emekdaslar | head -c 120
""")
cixis("""
# Autentifikasiya OLSA:
{ "ugur": false,
  "xeta": { "kod": "AUTENTIFIKASIYA_LAZIM",
            "mesaj": "Unauthorized" } }
""")
blok("block-evez", "ƏVƏZİNDƏ — digər yanaşmalar",
     "<table>"
     "<tr><th>Yanaşma</th><th>Üstünlük</th><th>Çatışmazlıq</th></tr>"
     "<tr><td>Session + Redis</td><td>Ani ləğv etmə</td><td>Əlavə infrastruktur</td></tr>"
     "<tr><td>OAuth 2.0 (Google)</td><td>Şifrə idarəsi yox</td><td>Xarici asılılıq, dövlət qurumu üçün uyğun deyil</td></tr>"
     "<tr><td>API açarı</td><td>Sadə</td><td>İstifadəçi anlayışı yox, ləğv çətindir</td></tr>"
     "<tr><td><strong>JWT + refresh token</strong></td><td>Balanslı</td><td>İki token idarəsi</td></tr>"
     "</table>"
     "<p>Biz <strong>sadə JWT</strong> ilə başlayırıq. Refresh token gələcək mərhələdədir.</p>")

# ══════════════════ 4 ══════════════════
A('<h2 id="b4">4. JWT nədir — üç hissə</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>JWT-nin strukturunu açacağıq. Bu, diaqnostika üçün vacibdir.</p>")
A('<pre data-lang="sxem"><code>eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImVtYWlsIjoi'
  'YWRtaW5AYXJ0aS5lZHUuYXoiLCJyb2wiOiJhZG1pbiIsImlhdCI6MTc4OTgyODc3NiwiZXhwIjoxNzg5ODU3NTc2fQ'
  '.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c\n'
  '└──────────── HEADER ────────────┘ └──────────── PAYLOAD ────────────┘ '
  '└─────────── İMZA ──────────┘</code></pre>')
blok("block-izah", "İZAH — hər hissə nədir?",
     "<table>"
     "<tr><th>Hissə</th><th>Nə saxlayır</th><th>Şifrəlidir?</th></tr>"
     "<tr><td><strong>Header</strong></td><td>Alqoritm (HS256) və tip (JWT)</td><td>❌ Base64 — hər kəs oxuyur</td></tr>"
     "<tr><td><strong>Payload</strong></td><td>İstifadəçi id, email, rol, vaxtlar</td><td>❌ Base64 — hər kəs oxuyur</td></tr>"
     "<tr><td><strong>İmza</strong></td><td>Header+Payload+gizli açarın HMAC-ı</td><td>✅ Riyazi qorunma</td></tr>"
     "</table>")
blok("block-xeber", "⚠️ JWT ŞİFRƏLƏNMİR — YALNIZ İMZALANIR",
     "<p>Tokeni istənilən şəxs <code>base64 -d</code> ilə aça bilər. "
     "İmza yalnız <strong>dəyişdirilmədiyini</strong> sübut edir, gizli olduğunu yox.</p>"
     "<p><strong>Nəticə:</strong> JWT payload-a <em>heç vaxt</em> həssas məlumat qoymayın "
     "(şifrə, FIN kod, maaş). Yalnız <strong>identifikasiya</strong> üçün lazım olanı.</p>")
addim(1, "Tokeni aç")
bash("""
# Tokeni 3 hisseye böl ve payload-i oxu
TOKEN='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImVtYWlsIjoiYWRtaW5AYXJ0aS5lZHUuYXoiLCJyb2wiOiJhZG1pbiIsImlhdCI6MTc4OTgyODc3NiwiZXhwIjoxNzg5ODU3NTc2fQ.xxx'

echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | python3 -m json.tool
""")
json_("""{
  "sub": 2,
  "email": "admin@arti.edu.az",
  "rol": "admin",
  "iat": 1789828776,
  "exp": 1789857576
}""")
blok("block-izah", "İZAH — payload sahələri",
     "<table>"
     "<tr><th>Sahə</th><th>Mənası</th><th>Nümunə</th></tr>"
     "<tr><td><code>sub</code></td><td>Subject — istifadəçi id</td><td><code>2</code></td></tr>"
     "<tr><td><code>email</code></td><td>İstifadəçi e-poçtu</td><td><code>admin@...</code></td></tr>"
     "<tr><td><code>rol</code></td><td>RBAC rolu</td><td><code>admin</code></td></tr>"
     "<tr><td><code>iat</code></td><td>Issued at — nə vaxt verildi</td><td>Unix vaxt</td></tr>"
     "<tr><td><code>exp</code></td><td>Expiration — nə vaxt bitir</td><td>Unix vaxt</td></tr>"
     "</table>"
     "<p><code>iat</code> və <code>exp</code> avtomatik əlavə olunur — biz yazmırıq.</p>")
blok("block-ipucu", "💡 TOKEN MÜDDƏTİNİ YOXLAMAQ",
     "<pre><code>node -e \"\n"
     "const t = process.argv[1];\n"
     "const p = JSON.parse(Buffer.from(t.split('.')[1], 'base64').toString());\n"
     "console.log('Bitir:', new Date(p.exp * 1000).toLocaleString('az'));\n"
     "console.log('Qaldi:', Math.round((p.exp * 1000 - Date.now()) / 60000), 'deqiqe');\n"
     "\" \"$TOKEN\"</code></pre>")

# ══════════════════ 5 ══════════════════
A('<h2 id="b5">5. Şifrə saxlama — heç vaxt düz mətn</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Şifrələrin bazada necə saxlandığını görəcəyik.</p>")
blok("block-xeber", "⚠️ ƏN BÖYÜK TƏHLÜKƏSİZLİK SƏHVİ",
     "<p>Şifrəni düz mətn kimi saxlamaq:</p>"
     "<table>"
     "<tr><th>Cədvəl</th><th>email</th><th>parol</th></tr>"
     "<tr><td>❌ SƏHV</td><td>admin@arti.edu.az</td><td><strong>123456</strong></td></tr>"
     "<tr><td>✅ DOĞRU</td><td>admin@arti.edu.az</td><td><code>$2b$10$oIesQsaJ4ahBc...</code></td></tr>"
     "</table>"
     "<p>Düz mətn saxlanılsa, baza sızması <strong>bütün istifadəçilərin</strong> "
     "şifrəsini açıq verir. İnsanlar isə eyni şifrəni hər yerdə işlədir.</p>")
blok("block-izah", "İZAH — hash nədir?",
     "<p><strong>Hash</strong> — geri qaytarıla bilməyən çevrilmədir:</p>"
     "<pre data-lang=\"sxem\"><code>\"123456\"  --hash-->  \"$2b$10$oIesQsaJ4ahBc...\"\n"
     "                          |\n"
     "                          +-- GERI QAYTARMAQ MÜMKÜN DEYİL</code></pre>"
     "<p>Yoxlama isə belədir: istifadəçi şifrəni yazır → hash-lənir → "
     "bazadakı hash ilə <strong>müqayisə</strong> olunur.</p>")
blok("block-evez", "ƏVƏZİNDƏ — digər alqoritmlər",
     "<table>"
     "<tr><th>Alqoritm</th><th>Sürət</th><th>Vəziyyət</th></tr>"
     "<tr><td>MD5</td><td>Çox sürətli</td><td>❌ <strong>QADAĞAN</strong> — GPU ilə saniyədə milyard</td></tr>"
     "<tr><td>SHA-256</td><td>Sürətli</td><td>❌ Şifrə üçün yararsız — çox sürətli</td></tr>"
     "<tr><td>bcrypt</td><td>Yavaş (tənzimlənən)</td><td>✅ Standart</td></tr>"
     "<tr><td>Argon2</td><td>Yavaş</td><td>✅ Ən müasir (2015)</td></tr>"
     "<tr><td>scrypt</td><td>Yavaş, yaddaş tələb edir</td><td>✅ Yaxşı</td></tr>"
     "</table>"
     "<p><strong>Məntiq tərsdir:</strong> parol hash-i üçün <em>yavaş</em> olmaq "
     "<strong>üstünlükdür</strong>. Sürətli alqoritm hücumçuya da kömək edir.</p>")

# ══════════════════ 6 ══════════════════
A('<h2 id="b6">6. bcrypt — hash və compare</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>bcrypt-in iki funksiyasını öyrənəcəyik: <code>hash()</code> və <code>compare()</code>.</p>")
addim(1, "Hash yaratmaq")
ts("""
import * as bcrypt from 'bcryptjs';

const BCRYPT_RAUND = 10;                       // "cost" — 2^10 = 1024 raund

const hash = await bcrypt.hash('123456', BCRYPT_RAUND);
// '$2b$10$oIesQsaJ4ahBc0vjhaRpN.x7k8YqZ...'
//   │   │  └──────────── duz (salt), 22 simvol
//   │   └── cost = 10
//   └── alqoritm versiyasi (2b = bcrypt)
""")
blok("block-izah", "İZAH — hash-in hissələri",
     "<table>"
     "<tr><th>Hissə</th><th>Uzunluq</th><th>Nədir</th></tr>"
     "<tr><td><code>$2b$</code></td><td>4</td><td>Alqoritm versiyası</td></tr>"
     "<tr><td><code>10$</code></td><td>3</td><td>Cost faktoru</td></tr>"
     "<tr><td><em>duz</em></td><td>22</td><td>Təsadüfi salt</td></tr>"
     "<tr><td><em>hash</em></td><td>31</td><td>Əsl hash dəyəri</td></tr>"
     "</table>"
     "<p><strong>CƏMİ: 60 simvol</strong>. Duz hash-in İÇİNDƏDİR — ona görə ayrıca "
     "sütun lazım deyil.</p>")
blok("block-ipucu", "💡 SALT (DUZ) NƏ ÜÇÜNDÜR?",
     "<p>Duz olmasa, eyni şifrəli iki istifadəçinin hash-i eyni olar:</p>"
     "<table>"
     "<tr><th></th><th>Duzsuz</th><th>Duzlu</th></tr>"
     "<tr><td>admin şifrəsi <code>123456</code></td><td><code>e10adc39...</code></td>"
     "<td><code>$2b$10$oIes...</code></td></tr>"
     "<tr><td>user şifrəsi <code>123456</code></td><td><code>e10adc39...</code> ⚠️ EYNİ</td>"
     "<td><code>$2b$10$Xk2p...</code> ✅ FƏRQLİ</td></tr>"
     "</table>"
     "<p>Duzsuz halda hücumçu bir hash-i sındırıb <strong>bütün</strong> eyni şifrəliləri tapır. "
     "Duzlu halda hər biri ayrıca sındırılmalıdır.</p>")
addim(2, "Şifrəni yoxlamaq")
ts("""
const duzdur = await bcrypt.compare('123456', hash);
// true

const sehvdir = await bcrypt.compare('654321', hash);
// false
""")
blok("block-olmaz", "OLMASA NƏ OLAR — hash-ləri müqayisə etmək",
     "<p>Sadəlövh yanaşma:</p>")
ts("""
// SEHV!
if (await bcrypt.hash(gelenParol, 10) === bazadakiHash) { ... }
""")
blok("block-izah", "İZAH — niyə bu işləmir?",
     "<p>bcrypt hər dəfə <strong>yeni təsadüfi duz</strong> yaradır. Eyni şifrə üçün "
     "hər dəfə fərqli hash alınır:</p>")
bash("""
node -e "
const b = require('bcryptjs');
console.log(b.hashSync('123456', 10));
console.log(b.hashSync('123456', 10));
console.log(b.hashSync('123456', 10));
"
""")
cixis("""
$2b$10$oIesQsaJ4ahBc0vjhaRpN.x7k8YqZ...
$2b$10$Xk2pLmN9vRtYuIoP3aSdF.e5wQ1zX...
$2b$10$Zq7wErT5yUiOpAsD2fGhJ.k9lMnBv...
                   ^^^ HAMISI FERQLIDIR
""")
blok("block-xeber", "⚠️ BCRYPT ASİNXRONDUR",
     "<p><code>bcrypt.hash()</code> və <code>compare()</code> <strong>Promise</strong> qaytarır. "
     "<code>await</code> unudulsa, dəyər əvəzinə Promise alınır:</p>")
ts("""
// SEHV — await yoxdur
const hash = bcrypt.hash('123456', 10);
// Promise { <pending> }  →  bazaya "Promise" yazilar!

// DOĞRU
const hash = await bcrypt.hash('123456', 10);
""")
addim(3, "Cost faktorunu seçmək")
A('<table>')
A('  <tr><th>Cost</th><th>Raund</th><th>Vaxt</th><th>Nə vaxt</th></tr>')
A('  <tr><td>8</td><td>256</td><td>~10 ms</td><td>Testlər</td></tr>')
A('  <tr><td><strong>10</strong></td><td>1024</td><td>~50 ms</td><td><strong>Standart — bizim seçim</strong></td></tr>')
A('  <tr><td>12</td><td>4096</td><td>~200 ms</td><td>Yüksək təhlükəsizlik</td></tr>')
A('  <tr><td>14</td><td>16384</td><td>~800 ms</td><td>Çox yavaş — istifadəçi gözləyir</td></tr>')
A('</table>')
blok("block-ipucu", "💡 COST-U NECƏ SEÇMƏK?",
     "<p>Qayda: <strong>login 200-500 ms çəkməlidir</strong>. Cost-u hər il bir addım "
     "artırmaq tövsiyə olunur (kompüterlər sürətlənir).</p>"
     "<p><code>10</code> bu gün balanslı seçimdir: hücumçu üçün yavaş, "
     "istifadəçi üçün hiss olunmaz.</p>")

# ══════════════════ 7 ══════════════════
A('<h2 id="b7">7. LoginDto və QeydiyyatDto</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>İki DTO yaradacağıq: giriş və qeydiyyat üçün.</p>")
addim(1, "LoginDto")
fayl_yaz("src/auth/dto/login.dto.ts")
blok("block-izah", "İZAH — login DTO-nun qaydaları",
     "<table>"
     "<tr><th>Sahə</th><th>Qayda</th><th>Nə üçün</th></tr>"
     "<tr><td><code>email</code></td><td><code>@IsEmail()</code></td>"
     "<td>Yanlış formatla bazaya sorğu göndərməyək</td></tr>"
     "<tr><td><code>parol</code></td><td><code>@MinLength(6)</code></td>"
     "<td>Çox qısa şifrə bazada ola bilməz</td></tr>"
     "</table>")
blok("block-xeber", "⚠️ LOGIN-DƏ MÜRƏKKƏB QAYDA YAZMAYIN",
     "<p>Login DTO-da <code>@Matches</code> kimi sərt qaydalar <strong>olmamalıdır</strong>:</p>"
     "<ul>"
     "<li>Əgər qayda dəyişsə, köhnə şifrəli istifadəçilər giriş edə bilməz;</li>"
     "<li>'Şifrə böyük hərf tələb edir' mesajı hücumçuya şifrə <strong>qaydasını</strong> deyir;</li>"
     "<li>Login sadəcə <em>müqayisədir</em> — qayda qeydiyyatda yoxlanılır.</li>"
     "</ul>"
     "<p><strong>Qayda:</strong> login yumşaq, qeydiyyat sərt olmalıdır.</p>")
addim(2, "QeydiyyatDto")
fayl_yaz("src/auth/dto/qeydiyyat.dto.ts")
blok("block-izah", "İZAH — ROLLAR sabiti",
     "<p><code>ROLLAR</code> massivi həm validasiyada, həm tip kimi işlədilir:</p>")
ts("""
export const ROLLAR = ['admin', 'muhendis', 'maliyyeci', 'baxici'] as const;
export type Rol = (typeof ROLLAR)[number];

// Rol = 'admin' | 'muhendis' | 'maliyyeci' | 'baxici'
""")
blok("block-ipucu", "💡 «as const» NƏ EDİR?",
     "<p><code>as const</code> olmasa, TypeScript <code>string[]</code> kimi görür və "
     "<code>Rol</code> tipi sadəcə <code>string</code> olar — yəni <strong>yazı səhvini "
     "tutmur</strong>:</p>"
     "<table>"
     "<tr><th></th><th>Tip</th><th>Yazı səhvi tutulur?</th></tr>"
     "<tr><td><code>as const</code> olmadan</td><td><code>string</code></td><td>❌ <code>'admn'</code> keçir</td></tr>"
     "<tr><td><code>as const</code> ilə</td><td><code>'admin' | ...</code></td><td>✅ Kompilyasiya xətası</td></tr>"
     "</table>")

# ══════════════════ 8 ══════════════════
A('<h2 id="b8">8. Rollar (RBAC) — dörd rol matrisi</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Dörd rolu və hər birinin nə edə biləcəyini müəyyənləşdirəcəyik.</p>")
A('<table>')
A('  <tr><th>Rol</th><th>Nə edir</th><th>Oxu</th><th>Yarat/Yenilə</th><th>Sil</th>'
  '<th>İstifadəçi idarəsi</th></tr>')
ROLLAR = [
    ("<code>admin</code>", "Sistem administratoru", "✅", "✅", "✅", "✅"),
    ("<code>muhendis</code>", "Mühəndis / metodist", "✅", "✅", "❌", "❌"),
    ("<code>maliyyeci</code>", "Maliyyə işçisi", "✅", "❌", "❌", "❌"),
    ("<code>baxici</code>", "Yalnız oxuma", "✅", "❌", "❌", "❌"),
]
for r in ROLLAR:
    A('  <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % r)
A('</table>')
blok("block-izah", "İZAH — «admin» super-roldur",
     "<p><code>RolesGuard</code>-da xüsusi qayda var:</p>")
ts("""
// admin HER SEYE icazelidir — super-rol
if (istifadeci.rol === 'admin') return true;
""")
blok("block-niye", "NİYƏ BELƏ?",
     "<p>Əks halda hər yeni endpoint-də <code>@Roles('admin', ...)</code> yazmaq lazım gələrdi "
     "və biri mütləq unudulardı. Super-rol bu riski aradan qaldırır.</p>"
     "<p><strong>Alternativ:</strong> super-rolu tam çıxarıb hər yerdə açıq yazmaq — "
     "daha sərt, lakin daha çox yazı tələb edir.</p>")
blok("block-evez", "ƏVƏZİNDƏ — icazə (permission) modeli",
     "<table>"
     "<tr><th>Model</th><th>Nümunə</th><th>Çeviklik</th></tr>"
     "<tr><td><strong>RBAC</strong> (bizim)</td><td>Rol → icazələr</td><td>Orta</td></tr>"
     "<tr><td>ABAC</td><td>Atribut əsaslı (<code>şöbə = öz şöbəsi</code>)</td><td>Yüksək</td></tr>"
     "<tr><td>ACL</td><td>Hər obyektə ayrıca icazə</td><td>Çox yüksək, idarəsi çətin</td></tr>"
     "</table>"
     "<p>4 rollu dövlət qurumu üçün RBAC tamamilə kifayətdir.</p>")

# ══════════════════ 9 ══════════════════
A('<h2 id="b9">9. Dekoratorlar — @Roles, @Public, @CurrentUser</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Üç dekorator yaradacağıq — guard-lar və controller-lər onları oxuyacaq.</p>")
addim(1, "@Roles — icazəli rollar")
fayl_yaz("src/auth/decorators/roles.decorator.ts")
blok("block-izah", "İZAH — SetMetadata nə edir?",
     "<p><code>SetMetadata(acar, deyer)</code> metadatanı funksiyaya <strong>yapışdırır</strong>. "
     "Guard isə <code>Reflector</code> vasitəsilə onu oxuyur:</p>"
     "<pre data-lang=\"sxem\"><code>@Roles('admin','muhendis')   -->   metadata: { rollar: ['admin','muhendis'] }\n"
     "                                              |\n"
     "              RolesGuard &lt;-- Reflector.getAllAndOverride()</code></pre>")
addim(2, "@Public — autentifikasiyadan azad")
fayl_yaz("src/auth/decorators/public.decorator.ts")
blok("block-niye", "NİYƏ @Public LAZIMDIR?",
     "<p>Qlobal guard <strong>hər şeyi</strong> qoruyur. Lakin bəzi endpoint-lər "
     "tokensiz işləməlidir:</p>"
     "<table>"
     "<tr><th>Endpoint</th><th>Nə üçün açıq</th></tr>"
     "<tr><td><code>POST /auth/login</code></td><td>Token almaq üçün — paradoks</td></tr>"
     "<tr><td><code>GET /saglamliq</code></td><td>Monitorinq sistemi token bilmir</td></tr>"
     "<tr><td><code>GET /</code></td><td>API məlumatı</td></tr>"
     "</table>")
addim(3, "@CurrentUser — istifadəçini controller-ə ötür")
fayl_yaz("src/auth/decorators/current-user.decorator.ts")
blok("block-izah", "İZAH — bu dekorator nə qənaət edir?",
     "<p>Olmadan hər controller-də belə yazmalı olardıq:</p>")
ts("""
@Get('profil')
profil(@Req() sorqu: Request) {
  const istifadeci = sorqu.user as CariIstifadeci;
  return istifadeci;
}
""")
blok("block-izah", "İZAH — @CurrentUser ilə",
     "<p>İndi isə birbaşa:</p>")
ts("""
@Get('profil')
profil(@CurrentUser() istifadeci: CariIstifadeci) {
  return istifadeci;
}

// Ve ya yalniz bir sahe:
@Get('profil')
email(@CurrentUser('email') email: string) {
  return { email };
}
""")
blok("block-ipucu", "💡 `createParamDecorator` NƏ EDİR?",
     "<p>NestJS-in xüsusi parametr dekoratoru yaratmağa imkan verir. "
     "<code>ctx.switchToHttp().getRequest()</code> ilə sorğuya çatırıq — "
     "orada <code>user</code> sahəsini <strong>JwtStrategy.validate()</strong> qoyub.</p>")

# ══════════════════ 10 ══════════════════
A('<h2 id="b10">10. JWT strategiyası</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Tokeni oxuyub istifadəçini tapan strategiyanı yazacağıq.</p>")
fayl_yaz("src/auth/strategies/jwt.strategy.ts")
blok("block-izah", "İZAH — üç addım",
     "<table>"
     "<tr><th>Addım</th><th>Kod</th><th>Nə edir</th></tr>"
     "<tr><td>1. Tokeni götür</td><td><code>ExtractJwt.fromAuthHeaderAsBearerToken()</code></td>"
     "<td><code>Authorization: Bearer xxx</code> header-indən oxuyur</td></tr>"
     "<tr><td>2. İmzanı yoxla</td><td><code>secretOrKey</code></td>"
     "<td>Token dəyişdirilibsə rədd edir</td></tr>"
     "<tr><td>3. İstifadəçini tap</td><td><code>validate(payload)</code></td>"
     "<td>Bazadan oxuyur, <code>request.user</code>-ə yazır</td></tr>"
     "</table>")
blok("block-xeber", "⚠️ validate() İÇİNDƏ BAZAYA BAXMAQ VACİBDİR",
     "<p>Token 8 saat qüvvədədir. Bu müddətdə istifadəçi:</p>"
     "<ul>"
     "<li>Silinə bilər;</li>"
     "<li>Deaktiv edilə bilər;</li>"
     "<li>Rolu dəyişdirilə bilər.</li>"
     "</ul>"
     "<p>Yalnız token payload-ına güvənsək, silinmiş istifadəçi 8 saat işləməyə davam edər. "
     "Ona görə <code>validate()</code>-də bazadan <strong>təzə məlumat</strong> oxuyuruq.</p>")
blok("block-olmaz", "OLMASA NƏ OLAR — bazaya baxmasaq",
     "<table>"
     "<tr><th>Hadisə</th><th>Bazaya baxmadan</th><th>Bazaya baxaraq</th></tr>"
     "<tr><td>İstifadəçi silindi</td><td>Token 8 saat işləyir ⚠️</td><td>Dərhal 401 ✅</td></tr>"
     "<tr><td>Deaktiv edildi</td><td>İşləyir ⚠️</td><td>Dərhal 401 ✅</td></tr>"
     "<tr><td>Rol dəyişdi</td><td>Köhnə rol qüvvədə ⚠️</td><td>Yeni rol dərhal qüvvədə ✅</td></tr>"
     "</table>"
     "<p><strong>Qiymət:</strong> hər sorğuda bir SQL. Lakin bu, "
     "<code>id</code> üzrə indeksli sadə sorğudur — mikrosaniyələr.</p>")
blok("block-evez", "ƏVƏZİNDƏ — keşləmə",
     "<p>Performans üçün istifadəçini Redis-də 60 saniyə keşləmək olar. "
     "Lakin 14 istifadəçi üçün bu lazımsızdır — <strong>vaxtından əvvəl "
     "optimallaşdırma</strong> etməyin.</p>")

# ══════════════════ 11 ══════════════════
A('<h2 id="b11">11. JwtAuthGuard — qlobal «təhlükəsiz susmaya görə»</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Qlobal guard yaradacağıq: hər şey qorunur, <code>@Public()</code> istisnadır.</p>")
fayl_yaz("src/auth/guards/jwt-auth.guard.ts")
blok("block-niye", "NİYƏ QLOBAL? — İKİ YANAŞMA",
     "<table>"
     "<tr><th></th><th>Endpoint-ə görə</th><th>Qlobal (bizim)</th></tr>"
     "<tr><td>Necə işləyir</td><td>Hər controller-də <code>@UseGuards()</code></td>"
     "<td>Bir dəfə <code>APP_GUARD</code></td></tr>"
     "<tr><td>Yeni endpoint</td><td><strong>Susmaya görə AÇIQ</strong> ⚠️</td>"
     "<td><strong>Susmaya görə QORUNUR</strong> ✅</td></tr>"
     "<tr><td>Unutma riski</td><td>Yüksək</td><td>Yoxdur</td></tr>"
     "<tr><td>Açıq endpoint</td><td>Heç nə yazmaq lazım deyil</td><td><code>@Public()</code></td></tr>"
     "</table>")
blok("block-olmaz", "OLMASA NƏ OLAR — «susmaya görə açıq» faciəsi",
     "<p>Endpoint-ə görə yanaşmada tipik hadisə:</p>"
     "<ol>"
     "<li>Developer <code>GET /kadrlar/emekdaslar</code> yaradır;</li>"
     "<li><code>@UseGuards(JwtAuthGuard)</code> yazmağı <strong>unudur</strong>;</li>"
     "<li>Testlər keçir (testdə token göndərilir, lakin guard yoxdur — fərq görünmür);</li>"
     "<li>İstehsalata çıxır → <strong>bütün maaşlar açıq</strong>.</li>"
     "</ol>"
     "<p>Qlobal guard bu ssenarini <strong>mümkünsüz</strong> edir.</p>")
blok("block-izah", "İZAH — getAllAndOverride nə edir?",
     "<p>Metadatanı iki yerdə axtarır: <strong>metodda</strong> və <strong>sinifdə</strong>:</p>")
ts("""
const publicdir = this.reflector.getAllAndOverride<boolean>(PUBLIC_ACARI, [
  context.getHandler(),     // metod:  @Get('login')
  context.getClass(),       // sinif:  @Controller('auth')
]);
""")
blok("block-ipucu", "💡 BÜTÜN CONTROLLER-İ AÇMAQ",
     "<p><code>@Public()</code>-i sinifə qoysaq, controller-in bütün endpoint-ləri açıq olar:</p>")
ts("""
@Public()                    // butun controller PUBLIC
@Controller('ictimai')
export class IctimaiController { ... }
""")

# ══════════════════ 12 ══════════════════
A('<h2 id="b12">12. RolesGuard — RBAC yoxlaması</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>İkinci qlobal guard — rol yoxlaması.</p>")
fayl_yaz("src/auth/guards/roles.guard.ts")
blok("block-izah", "İZAH — məntiq axını",
     "<pre data-lang=\"sxem\"><code>Sorqu gəlir\n"
     "   |\n"
     "   +-- JwtAuthGuard -----> token varmi?  --X--> 401\n"
     "   |                      duzdurmu?      --X--> 401\n"
     "   |                      user = {...}\n"
     "   v\n"
     "   +-- RolesGuard -------> @Roles var?   --X--> BURAX (her kes)\n"
     "   |                      rol = admin?   --B--> BURAX (super-rol)\n"
     "   |                      rolu uygundur? --X--> 403\n"
     "   v\n"
     "Controller metodu</code></pre>")
blok("block-xeber", "⚠️ GUARD-LARIN SIRASI VACİBDİR",
     "<p><code>RolesGuard</code> <code>JwtAuthGuard</code>-dan <strong>SONRA</strong> "
     "işləməlidir — çünki <code>request.user</code>-i o yaradır.</p>"
     "<p>Sıra <code>app.module.ts</code>-dəki <code>providers</code> massivinin "
     "sırası ilə müəyyən olunur:</p>")
ts("""
providers: [
  { provide: APP_GUARD, useClass: JwtAuthGuard },   // 1-ci
  { provide: APP_GUARD, useClass: RolesGuard },     // 2-ci
]
""")
blok("block-olmaz", "OLMASA NƏ OLAR — sıra tərs olsa",
     "<p><code>RolesGuard</code> birinci işləsə, <code>request.user</code> hələ "
     "<code>undefined</code> olar:</p>"
     "<pre><code>403 Forbidden: İstifadəçi rolu müəyyən deyil</code></pre>"
     "<p>Hətta <strong>düzgün token</strong> göndərsəniz belə.</p>")
blok("block-ipucu", "💡 `includes` vs `some`",
     "<p>Rollar massivini yoxlayarkən:</p>"
     "<table>"
     "<tr><th>Kod</th><th>Nəticə</th></tr>"
     "<tr><td><code>teleb.includes(rol)</code></td><td>✅ Düzgün — massivdə axtarır</td></tr>"
     "<tr><td><code>rol in teleb</code></td><td>❌ Səhv — indeksləri yoxlayır</td></tr>"
     "<tr><td><code>teleb.indexOf(rol) &gt;= 0</code></td><td>✅ Düzgün, lakin uzun</td></tr>"
     "</table>")

# ══════════════════ 13 ══════════════════
A('<h2 id="b13">13. ⚠️ REAL XƏTA: .env və modul yüklənmə sırası</h2>')
blok("block-xeber", "⚠️ BU XƏTA BU DƏRSDƏ REAL OLARAQ BAŞ VERDİ",
     "<p>İlk buraxılışda <code>JwtModule.register()</code> yazdım. Nəticə: "
     "<strong>login işləyirdi, amma heç bir token qəbul olunmurdu</strong> — hər sorğu 401.</p>")
cixis("""
$ curl -X POST .../auth/login -d '{"email":"admin@arti.edu.az","parol":"123456"}'
{"token":"eyJhbGciOiJIUzI1NiIs...","istifadeci":{...}}      <-- TOKEN GELIR

$ curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." .../struktur/merkezler
{"ugur":false,"xeta":{"kod":"AUTENTIFIKASIYA_LAZIM",...}}  <-- AMMA 401!
""")
blok("block-izah", "İZAH — səbəb: İKİ FƏRQLİ AÇAR",
     "<p>İki yerdə <code>process.env.JWT_SECRET</code> oxunurdu, lakin "
     "<strong>fərqli vaxtlarda</strong>:</p>"
     "<table>"
     "<tr><th>Harada</th><th>Nə vaxt işləyir</th><th>Oxunan açar</th></tr>"
     "<tr><td><code>JwtModule.register({...})</code></td>"
     "<td>Modul <strong>yüklənəndə</strong> (import zamanı)</td>"
     "<td>❌ <code>undefined</code> → fallback</td></tr>"
     "<tr><td><code>JwtStrategy</code> konstruktoru</td>"
     "<td>DI <strong>yaradılanda</strong> (ConfigModule hazır)</td>"
     "<td>✅ real açar</td></tr>"
     "</table>"
     "<p>Nəticə: token <strong>bir açarla imzalanır</strong>, "
     "<strong>başqa açarla yoxlanılır</strong> → 401.</p>")
blok("block-yox", "SÜBUT — diaqnostika",
     "<pre><code>$ node -e \"\n"
     "console.log('.env yuklenmeden:', process.env.JWT_SECRET ?? '(yoxdur)');\n"
     "require('dotenv').config({ path: '.env' });\n"
     "console.log('.env yuklendikden sonra:', process.env.JWT_SECRET);\n"
     "\"\n\n"
     ".env yuklenmeden: (yoxdur)\n"
     ".env yuklendikden sonra: deepseek-arti-gizli-acar-2026</code></pre>")
blok("block-olmaz", "HƏLL — üç variant",
     "<table>"
     "<tr><th>#</th><th>Həll</th><th>Qiymətləndirmə</th></tr>"
     "<tr><td>1</td><td><code>main.ts</code>-ə <code>import 'dotenv/config'</code></td>"
     "<td>İşləyir, lakin kövrəkdir</td></tr>"
     "<tr><td>2</td><td><code>JwtModule.registerAsync()</code> + <code>ConfigService</code></td>"
     "<td>✅ <strong>Düzgün yol</strong> — NestJS standartı</td></tr>"
     "<tr><td>3</td><td>Açarı kodda sabit yazmaq</td>"
     "<td>❌ <strong>QADAĞAN</strong> — açar repoya düşər</td></tr>"
     "</table>")
addim(1, "Düzgün həll")
fayl_yaz("src/auth/auth.module.ts")
blok("block-izah", "İZAH — register vs registerAsync",
     "<table>"
     "<tr><th></th><th><code>register()</code></th><th><code>registerAsync()</code></th></tr>"
     "<tr><td>Nə vaxt işləyir</td><td>Dərhal, import zamanı</td><td>Modul hazır olanda</td></tr>"
     "<tr><td><code>.env</code> yüklənib?</td><td>❌ Yox</td><td>✅ Bəli</td></tr>"
     "<tr><td><code>ConfigService</code></td><td>Yoxdur</td><td>✅ Var</td></tr>"
     "<tr><td>Tövsiyə</td><td>Sabit dəyərlər üçün</td><td>✅ <strong>Mühit dəyişənləri üçün</strong></td></tr>"
     "</table>")
blok("block-ipucu", "💡 ÜMUMİ QAYDA",
     "<p><strong>Mühit dəyişəni oxuyursunuzsa — <code>registerAsync</code> işlədin.</strong></p>"
     "<p>Eyni qayda <code>TypeOrmModule</code>, <code>CacheModule</code>, "
     "<code>MailerModule</code> və digər <code>register()</code> API-li modullara da aiddir.</p>")
yoxlama(13, "Açarlar uyğundur?",
        "<pre><code># Login\ncurl -s -X POST .../auth/login -d '{...}' | python3 -c \"import json,sys;print(json.load(sys.stdin)['token'])\"\n\n"
        "# Hemin token ile sorqu\n"
        "curl -s -H \"Authorization: Bearer &lt;TOKEN&gt;\" .../struktur/merkezler | head -c 80\n\n"
        "# Gozlenilen: melumat gelir (401 YOX)</code></pre>")

# ══════════════════ 14 ══════════════════
A('<h2 id="b14">14. Auth servisi — login və timing attack qoruması</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Biznes məntiqini yazacağıq: login, qeydiyyat, şifrə dəyişmə.</p>")
fayl_yaz("src/auth/auth.service.ts")
blok("block-izah", "İZAH — iki təhlükəsizlik qərarı",
     "<p><strong>1. Timing attack qoruması:</strong></p>")
ts("""
const hash = istifadeci?.parol_hash ?? SAXTA_HASH;
const duzdur = await bcrypt.compare(dto.parol, hash);

if (!istifadeci || !duzdur) {
  throw new UnauthorizedException('E-poçt və ya şifrə yanlışdır');
}
""")
blok("block-olmaz", "OLMASA NƏ OLAR — sadəlövh yanaşma",
     "<p>Əvvəlcə istifadəçini yoxlasaq:</p>")
ts("""
const istifadeci = await tap(email);
if (!istifadeci) throw new UnauthorizedException('İstifadəçi tapılmadı');

const duzdur = await bcrypt.compare(parol, istifadeci.parol_hash);
if (!duzdur) throw new UnauthorizedException('Şifrə yanlışdır');
""")
A('<table>')
A('  <tr><th>Sorğu</th><th>Vaxt</th><th>Hücumçu nə öyrənir</th></tr>')
A('  <tr><td>Mövcud olmayan e-poçt</td><td>~5 ms</td><td>Bu e-poçt <strong>yoxdur</strong></td></tr>')
A('  <tr><td>Mövcud e-poçt</td><td>~50 ms</td><td>Bu e-poçt <strong>var</strong> (bcrypt hesablandı)</td></tr>')
A('</table>')
blok("block-izah", "İZAH — bizim yanaşma",
     "<p>İstifadəçi tapılmasa da <strong>saxta hash</strong> ilə bcrypt müqayisəsi aparırıq. "
     "Nəticədə hər iki halda vaxt eyni olur (~50 ms) və hücumçu fərqi görmür.</p>")
blok("block-ipucu", "💡 İKİNCİ QƏRAR — EYNI XƏTA MESAJI",
     "<table>"
     "<tr><th></th><th>Mesaj</th><th>Nəticə</th></tr>"
     "<tr><td>❌ Fərqli</td><td>'İstifadəçi tapılmadı' / 'Şifrə yanlışdır'</td>"
     "<td>E-poçt siyahısı öyrənilir</td></tr>"
     "<tr><td>✅ Eyni</td><td>'E-poçt və ya şifrə yanlışdır'</td>"
     "<td>Heç nə öyrənilmir</td></tr>"
     "</table>"
     "<p>Bu, <strong>user enumeration</strong> hücumunun qarşısını alır.</p>")

# ══════════════════ 15 ══════════════════
A('<h2 id="b15">15. Auth controller</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Dörd endpoint: login, profil, qeydiyyat, istifadəçi siyahısı.</p>")
fayl_yaz("src/auth/auth.controller.ts")
blok("block-izah", "İZAH — endpoint-lər",
     "<table>"
     "<tr><th>Metod</th><th>Yol</th><th>İcazə</th><th>Nə edir</th></tr>"
     "<tr><td>POST</td><td><code>/auth/login</code></td><td><code>@Public()</code></td>"
     "<td>Token alır</td></tr>"
     "<tr><td>GET</td><td><code>/auth/profil</code></td><td>İstənilən token</td>"
     "<td>Öz profilini göstərir</td></tr>"
     "<tr><td>POST</td><td><code>/auth/qeydiyyat</code></td><td><code>@Roles('admin')</code></td>"
     "<td>Yeni istifadəçi yaradır</td></tr>"
     "<tr><td>GET</td><td><code>/auth/istifadeciler</code></td><td><code>@Roles('admin')</code></td>"
     "<td>Hamısını siyahılayır</td></tr>"
     "</table>")
blok("block-xeber", "⚠️ LOGIN-DƏ 200, 201 DEYİL",
     "<p><code>@Post()</code> susmaya görə <strong>201 Created</strong> qaytarır. "
     "Login heç nə <em>yaratmır</em> — ona görə:</p>")
ts("""
@Post('login')
@HttpCode(HttpStatus.OK)      // 200 — 201 YOX
login(@Body() dto: LoginDto) { ... }
""")
blok("block-ipucu", "💡 NİYƏ CAVAB TİPİ AÇIQ YAZILIR?",
     "<p><code>login(): Promise&lt;LoginCavabi&gt;</code> — TypeScript tipi "
     "sənədləşmə rolunu oynayır. Frontend komandası <code>/docs</code>-da "
     "dəqiq cavab strukturunu görür.</p>")

# ══════════════════ 16 ══════════════════
A('<h2 id="b16">16. Auth modulu — registerAsync</h2>')
blok("block-ne", "NƏ EDƏCƏYƏK",
     "<p>Modulu yığacağıq. (Fayl artıq §13-də yazıldı.)</p>")
fayl_yaz("src/auth/auth.module.ts")
blok("block-izah", "İZAH — modulun hissələri",
     "<table>"
     "<tr><th>Hissə</th><th>Nə üçün</th></tr>"
     "<tr><td><code>PassportModule</code></td><td>Strategiyaları qeydiyyatdan keçirir</td></tr>"
     "<tr><td><code>JwtModule.registerAsync</code></td><td>Token imzalama və yoxlama</td></tr>"
     "<tr><td><code>providers: [AuthService, JwtStrategy]</code></td>"
     "<td>Passport <code>JwtStrategy</code>-ni avtomatik tapır</td></tr>"
     "</table>")
blok("block-xeber", "⚠️ JwtStrategy-Nİ PROVIDERS-A ƏLAVƏ ETMƏK VACİBDİR",
     "<p>Əlavə etməsəniz, Passport strategiyanı tanımır:</p>"
     "<pre><code>Error: Unknown authentication strategy \"jwt\"</code></pre>"
     "<p>Bu, ən çaşdırıcı xətalardan biridir — çünki kod düzgün görünür.</p>")

# ══════════════════ 17 ══════════════════
A('<h2 id="b17">17. Audit interceptor</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Hər yazma əməliyyatını <code>audit.audit_log</code> cədvəlinə yazacağıq.</p>")
fayl_yaz("src/common/interceptors/audit.interceptor.ts")
blok("block-niye", "NİYƏ AUDIT LAZIMDIR?",
     "<table>"
     "<tr><th>Sual</th><th>Audit olmadan</th></tr>"
     "<tr><td>'Bu maaşı kim dəyişdi?'</td><td>Bilinmir</td></tr>"
     "<tr><td>'Bu mərkəzi kim sildi?'</td><td>Bilinmir</td></tr>"
     "<tr><td>'Dünən nə dəyişdi?'</td><td>Bilinmir</td></tr>"
     "<tr><td>'Şübhəli fəaliyyət varmı?'</td><td>Bilinmir</td></tr>"
     "</table>"
     "<p>Dövlət qurumunda audit <strong>tələbdir</strong>, seçim deyil.</p>")
blok("block-izah", "İZAH — interceptor necə işləyir?",
     "<pre data-lang=\"sxem\"><code>Sorqu --> Interceptor.before --> Controller --> Service\n"
     "                            |                              |\n"
     "                            |                              v\n"
     "                            +----- Interceptor.after &lt;---- Cavab\n"
     "                                       |\n"
     "                                       v\n"
     "                              audit_log-a YAZ</code></pre>")
ts("""
return novbeti.handle().pipe(
  tap({
    next:  () => this.yaz(..., null),              // ugurlu
    error: (x) => this.yaz(..., x.message),        // xetali
  }),
);
""")
blok("block-ipucu", "💡 YALNIZ YAZMA ƏMƏLİYYATLARI",
     "<p><code>GET</code> sorğuları jurnala yazılmır — əks halda cədvəl sürətlə böyüyər:</p>")
ts("""
const IZLENEN_METODLAR = ['POST', 'PATCH', 'PUT', 'DELETE'];

if (!IZLENEN_METODLAR.includes(metod)) {
  return novbeti.handle();      // oxuma — kec, yazma
}
""")
blok("block-xeber", "⚠️ AUDIT XƏTASI ƏSAS ƏMƏLİYYATI POZMAMALIDIR",
     "<p>Audit yazıla bilməz (baza yüklənib, cədvəl silinib). "
     "Bu halda <strong>əsas əməliyyat uğursuz olmamalıdır</strong>:</p>")
ts("""
try {
  await this.prisma.$executeRaw`INSERT INTO audit.audit_log ...`;
} catch (x) {
  // Audit yazilmamasi esas emeliyyati POZMASIN
  this.log.error(`Audit yazilmadi: ${(x as Error).message}`);
}
""")
blok("block-olmaz", "OLMASA NƏ OLAR — try/catch olmasa",
     "<p>Audit cədvəli dolubsa, istifadəçi məlumat <strong>əlavə edə bilməz</strong> — "
     "səbəbi isə anlaşılmaz olar. Audit <em>köməkçi</em> funksiyadır, "
     "<strong>əsas işi bloklamamalıdır</strong>.</p>")
addim(1, "Cədvəl adını düzgün çıxarmaq")
blok("block-izah", "İZAH — cedvelAdi()",
     "<p>İlk versiyada nəticə <code>api.v1.struktur.merkezler</code> olurdu — "
     "qlobal prefiks də daxil. Düzəldilmiş variant:</p>")
ts("""
private cedvelAdi(yol: string): string {
  return yol
    .replace(/^\\/api\\/v\\d+\\//, '')     // qlobal prefiksi sil
    .replace(/^\\//, '')
    .replace(/\\/:[^/]+.*$/, '')          // :id kimi parametrleri sil
    .replace(/\\/+$/, '')
    .replace(/\\//g, '.') || 'namelum';
}

// /api/v1/struktur/merkezler/:id  ->  struktur.merkezler
""")

# ══════════════════ 18 ══════════════════
A('<h2 id="b18">18. app.module.ts — APP_GUARD sırası</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Qlobal guard və interceptor-u qeyd edəcəyik.</p>")
fayl_yaz("src/app.module.ts")
blok("block-izah", "İZAH — APP_GUARD nədir?",
     "<p><code>@UseGuards()</code> hər controller-də təkrar yazılır. "
     "<code>APP_GUARD</code> isə qlobal qeydiyyatdır:</p>"
     "<table>"
     "<tr><th>Token</th><th>Nə üçün</th></tr>"
     "<tr><td><code>APP_GUARD</code></td><td>Qlobal guard</td></tr>"
     "<tr><td><code>APP_INTERCEPTOR</code></td><td>Qlobal interceptor</td></tr>"
     "<tr><td><code>APP_PIPE</code></td><td>Qlobal pipe</td></tr>"
     "<tr><td><code>APP_FILTER</code></td><td>Qlobal xəta filtri</td></tr>"
     "</table>")
blok("block-xeber", "⚠️ SIRA MÜTLƏQDİR",
     "<pre data-lang=\"sxem\"><code>1. JwtAuthGuard    ->  request.user = {...}\n"
     "2. RolesGuard      ->  request.user.rol yoxlanilir</code></pre>"
     "<p>Massivdəki sıra icra sırasıdır. Tərs olsa — 403.</p>")
blok("block-ipucu", "💡 main.ts-DƏ ALLEXCEPTIONSFILTER",
     "<p>Qeyd: <code>AllExceptionsFilter</code> <code>main.ts</code>-də "
     "<code>app.useGlobalFilters()</code> ilə qoşulub, "
     "<code>APP_FILTER</code> ilə yox. Səbəb: filtr <code>APP_GUARD</code>-dan "
     "əvvəl işləməlidir ki, guard-ın atdığı 401 də düzgün formatda qaytarılsın.</p>")

# ══════════════════ 19 ══════════════════
A('<h2 id="b19">19. Endpoint-lərin qorunması</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Mövcud endpoint-lərə rol tələbləri əlavə edəcəyik.</p>")
fayl_yaz("src/struktur/struktur.controller.ts")
blok("block-izah", "İZAH — rol paylanması",
     "<table>"
     "<tr><th>Endpoint</th><th>Rol</th><th>Nə üçün</th></tr>"
     "<tr><td><code>GET /struktur/merkezler</code></td><td>hamı (token ilə)</td>"
     "<td>Oxumaq zərərsizdir</td></tr>"
     "<tr><td><code>POST /struktur/merkezler</code></td><td><code>admin, muhendis</code></td>"
     "<td>Struktur dəyişikliyi məsuliyyət tələb edir</td></tr>"
     "<tr><td><code>PATCH /struktur/merkezler/:id</code></td><td><code>admin, muhendis</code></td>"
     "<td>Eyni</td></tr>"
     "<tr><td><code>DELETE /struktur/merkezler/:id</code></td><td><code>admin</code></td>"
     "<td>Silmə <strong>geri qaytarılmır</strong> — yalnız admin</td></tr>"
     "</table>")
blok("block-niye", "NİYƏ SİLMƏ YALNIZ ADMIN?",
     "<p>Silmə əməliyyatı:</p>"
     "<ul>"
     "<li>Bağlı məlumatı da məhv edə bilər;</li>"
     "<li>Geri qaytarma yoxdur (hard delete);</li>"
     "<li>Audit jurnalında iz qalsa da, məlumat bərpa olunmur.</li>"
     "</ul>"
     "<p>Buna görə ən dar icazə — yalnız <code>admin</code>.</p>")
addim(1, "Saglamliq endpoint-lərini aç")
fayl_yaz("src/saglamliq/saglamliq.controller.ts")
blok("block-ipucu", "💡 @Public() YADDA SAXLAYIN",
     "<p>Qlobal guard əlavə edəndə <strong>monitorinq endpoint-ləri dərhal 401 verir</strong>. "
     "Docker, Kubernetes, UptimeRobot — hamısı token bilmir.</p>")

# ══════════════════ 20 ══════════════════
A('<h2 id="b20">20. Seed skripti</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>İstifadəçiləri yaradan skript yazacağıq.</p>")
blok("block-niye", "NİYƏ LAZIMDIR",
     "<p>Şifrələr bcrypt ilə hash-lənməlidir — əl ilə SQL yazmaq mümkün deyil. "
     "Skript isə:</p>"
     "<ul>"
     "<li>Hash-ləyir;</li>"
     "<li>İdempotentdir — ikinci dəfə işlətsəniz dublikat yaratmır;</li>"
     "<li>Yeni mühitdə (test, istehsalat) eyni istifadəçiləri yaradır.</li>"
     "</ul>")
fayl_yaz("scripts/seed-auth.ts")
blok("block-izah", "İZAH — ON CONFLICT nə edir?",
     "<p><code>INSERT ... ON CONFLICT (email) DO UPDATE</code> — "
     "PostgreSQL-in <strong>upsert</strong> əmri:</p>"
     "<table>"
     "<tr><th>Vəziyyət</th><th>Nə olur</th></tr>"
     "<tr><td>E-poçt yoxdur</td><td>Yeni sətir yaranır</td></tr>"
     "<tr><td>E-poçt var</td><td>Şifrə və rol <strong>yenilənir</strong></td></tr>"
     "</table>"
     "<p>Beləliklə skript <strong>neçə dəfə işlətsəniz də</strong> eyni nəticəni verir.</p>")
bash("""
cd ~/Deepseek_ARTI/DS_Backend

# package.json-a skript elave et
npm pkg set scripts.seed:auth="tsx scripts/seed-auth.ts"

# Icra et
npm run seed:auth
""")
cixis("""
════ İstifadəçilər yaradılır ════

  ✓ id= 2  admin@arti.edu.az        admin      şifrə: 123456
  ✓ id= 3  muhendis@arti.edu.az     muhendis   şifrə: 123456
  ✓ id= 4  maliyyeci@arti.edu.az    maliyyeci  şifrə: 123456
  ✓ id= 5  baxici@arti.edu.az       baxici     şifrə: 123456

════ CƏMİ: 4 istifadəçi ════
""")
blok("block-xeber", "⚠️ İSTEHSALATDA ŞİFRƏLƏRİ DƏYİŞİN",
     "<p><code>123456</code> yalnız inkişaf üçündür. İstehsalata çıxmazdan əvvəl:</p>"
     "<ul>"
     "<li>Hər istifadəçiyə <strong>fərqli</strong> və güclü şifrə verin;</li>"
     "<li>Skripti repodan çıxarın və ya şifrələri mühit dəyişənindən oxuyun;</li>"
     "<li>İlk girişdə şifrə dəyişmə məcburiyyəti qoyun.</li>"
     "</ul>")

# ══════════════════ 21 ══════════════════
A('<h2 id="b21">21. Testlər — 38 unit + 62 e2e</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Təhlükəsizlik qatını test edəcəyik. Bu dərsdə testlər "
     "<strong>funksionallıqdan daha vacibdir</strong>.</p>")
addim(1, "Auth servisi testləri")
fayl_yaz("src/auth/auth.service.spec.ts")
blok("block-izah", "İZAH — ən vacib testlər",
     "<table>"
     "<tr><th>Test</th><th>Nə sübut edir</th></tr>"
     "<tr><td>cavabda <code>parol_hash</code> yoxdur</td>"
     "<td>Şifrə hash-ı API-dən sız mır</td></tr>"
     "<tr><td>mövcud olmayan email → <strong>eyni</strong> mesaj</td>"
     "<td>User enumeration mümkün deyil</td></tr>"
     "<tr><td>bcrypt müqayisəsi hər halda aparılır</td>"
     "<td>Timing attack mümkün deyil</td></tr>"
     "<tr><td>INSERT-ə düz mətn şifrə getmir</td>"
     "<td>Şifrə HƏMİŞƏ hash-lənir</td></tr>"
     "</table>")
blok("block-xeber", "⚠️ bcryptjs-i MOCK ETMƏK LAZIM GƏLDİ",
     "<p>İlk versiyada <code>vi.spyOn(bcrypt, 'compare')</code> yazdım — xəta verdi:</p>"
     "<pre><code>TypeError: Cannot redefine property: compare</code></pre>"
     "<p><strong>Səbəb:</strong> ESM namespace dondurulmuşdur (frozen) — "
     "<code>spyOn</code> onu dəyişə bilmir.</p>"
     "<p><strong>Həll:</strong> <code>vi.mock</code> ilə modulu yüklənərkən əvəz et:</p>")
ts("""
vi.mock('bcryptjs', async () => {
  const real = await vi.importActual<typeof import('bcryptjs')>('bcryptjs');
  return {
    ...real,                              // real funksiyalari saxla
    compare: vi.fn(real.compare),         // ...amma izlenen variantla
    hash: vi.fn(real.hash),
  };
});
""")
addim(2, "e2e testləri")
fayl_yaz("test/backend3.e2e-spec.ts")
blok("block-izah", "İZAH — e2e test qrupları",
     "<table>"
     "<tr><th>Qrup</th><th>Test</th><th>Nə yoxlanılır</th></tr>"
     "<tr><td>POST /auth/login</td><td>5</td><td>Token, səhv şifrə, validasiya</td></tr>"
     "<tr><td>Token yoxlaması</td><td>4</td><td>Tokensiz, səhv token, prefikssiz</td></tr>"
     "<tr><td>@Public() endpoint-lər</td><td>3</td><td>Token olmadan işləyir</td></tr>"
     "<tr><td>GET /auth/profil</td><td>1</td><td>Cari istifadəçi</td></tr>"
     "<tr><td><strong>RBAC matrisi</strong></td><td>8</td><td>Hər rol üçün icazə</td></tr>"
     "<tr><td>POST /auth/qeydiyyat</td><td>5</td><td>Yaratma, giriş, icazə</td></tr>"
     "<tr><td>Audit jurnalı</td><td>2</td><td>Yazma qeyd olunur, oxuma yox</td></tr>"
     "<tr><td>Xəta formatları</td><td>3</td><td>401, 403, parol sızması</td></tr>"
     "</table>")
blok("block-ipucu", "💡 TEST TƏMİZLİYİ",
     "<p>Test yaratdığı məlumatı <strong>sil məlidir</strong>, əks halda "
     "hər buraxılış bazanı böyüdür. Biz <code>afterAll</code>-da təmizləyirik:</p>")
ts("""
afterAll(async () => {
  // 1) Yaradilan merkezleri sil
  for (const id of YARADILANLAR) {
    await request(app.getHttpServer())
      .delete(`/api/v1/struktur/merkezler/${id}`)
      .set('Authorization', `Bearer ${tokenlar.admin}`);
  }

  // 2) Test istifadecilerini sil (qeydiyyat endpoint-i onlari saxlayir)
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  await pool.query("DELETE FROM kadrlar.istifadeciler WHERE email LIKE 'e2e%'");
  await pool.end();

  await app.close();
});
""")
blok("block-olmaz", "OLMASA NƏ OLAR — təmizləmə olmasa",
     "<p>E2E testləri 4 buraxılışda bazaya <strong>80 istifadəçi</strong> əlavə etdi. "
     "Nəticədə:</p>"
     "<ul>"
     "<li><code>/auth/istifadeciler</code> siyahısı oxunmaz olur;</li>"
     "<li>Sayğac testləri pozulur;</li>"
     "<li>İstehsalat bazasında zibil qalır.</li>"
     "</ul>")
bash("""
cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST

npm test                                         # 38 unit
npx vitest run --config vitest.config.e2e.ts     # 62 e2e
""")
cixis("""
 ✓ src/common/dto/sehife.dto.spec.ts (8 tests)
 ✓ src/struktur/struktur.service.spec.ts (17 tests)
 ✓ src/auth/auth.service.spec.ts (13 tests)
 Test Files  3 passed (3)
      Tests  38 passed (38)

 ✓ test/backend2.e2e-spec.ts (30 tests)
 ✓ test/backend3.e2e-spec.ts (32 tests)
 Test Files  2 passed (2)
      Tests  62 passed (62)
""")

# ══════════════════ 22 ══════════════════
A('<h2 id="b22">22. Backend-2 testlərinin yenilənməsi</h2>')
blok("block-xeber", "⚠️ BACKEND-3 KÖHNƏ TESTLƏRİ POZUR",
     "<p>Qlobal guard əlavə olanda Backend-2-nin <strong>30 e2e testi</strong> "
     "dərhal uğursuz oldu — hamısı 401 qaytarmağa başladı:</p>")
cixis("""
 FAIL  test/backend2.e2e-spec.ts > GET /struktur/merkezler
       > sehifelenmis siyahi qaytarir
 Error: expected 200 "OK", got 401 "Unauthorized"
""")
blok("block-izah", "İZAH — bu, GÖZLƏNİLƏN nəticədir",
     "<p>Testlər <strong>qırılmadı</strong> — davranış dəyişdi. "
     "Əvvəl API açıq idi, indi bağlıdır.</p>"
     "<p>Bu, <strong>yaxşı əlamətdir</strong>: testlər real dəyişikliyi tutdu. "
     "Əgər testlər yenə yaşıl qalsaydı, deməli heç nə yoxlamırdılar.</p>")
blok("block-ne", "HƏLL — testlərə token əlavə et",
     "<p>Hər test faylında <code>beforeAll</code>-da token alırıq və "
     "bütün sorğulara header əlavə edirik:</p>")
ts("""
describe('Backend-2 (e2e)', () => {
  let app: INestApplication<App>;
  let token = '';

  const api = () =>
    request(app.getHttpServer()).set('Authorization', `Bearer ${token}`);
  const publicApi = () => request(app.getHttpServer());

  beforeAll(async () => {
    // ... app yaradilir ...

    const girish = await publicApi()
      .post('/api/v1/auth/login')
      .send({ email: 'admin@arti.edu.az', parol: '123456' });

    token = girish.body?.token ?? '';
    expect(token).toBeTruthy();
  });
""")
blok("block-xeber", "⚠️ api() FUNKSİYASINI YANLIŞ YAZMAQ — REAL XƏTA",
     "<p>İlk cəhddə belə yazdım:</p>")
ts("""
// SEHV — sonsuz rekursiya!
const api = () => api().set('Authorization', `Bearer ${token}`);
// RangeError: Maximum call stack size exceeded
""")
blok("block-izah", "İZAH — nə baş verdi?",
     "<p>Kütləvi əvəzləmə (`request(app.getHttpServer())` → `api()`) "
     "funksiyanın <strong>öz gövdəsini</strong> də dəyişdi. Nəticədə "
     "<code>api()</code> özünü çağırır.</p>")
ts("""
// DOĞRU
const api = () =>
  request(app.getHttpServer()).set('Authorization', `Bearer ${token}`);
""")
blok("block-ipucu", "💡 DƏRS",
     "<p>Kütləvi əvəzləmə (find &amp; replace) edərkən <strong>həmişə</strong> "
     "nəticəni yoxlayın — xüsusən funksiya təriflərini.</p>"
     "<p>Komanda: <code>grep -n 'const api' fayl.ts</code> — tərifi dərhal göstərir.</p>")

# ══════════════════ 23 ══════════════════
A('<h2 id="b23">23. Xəta kitabçası</h2>')
blok("block-ne", "NƏ EDƏCƏYİK",
     "<p>Bu dərsdə rast gəlinən xətaları toplayacağıq.</p>")
A('<table>')
A('  <tr><th>Xəta</th><th>Səbəb</th><th>Həll</th></tr>')
XETALAR = [
    ("Login işləyir, amma <strong>hər token 401</strong> verir",
     "<code>JwtModule.register()</code> <code>.env</code>-dən əvvəl işləyir — "
     "fərqli açarlar",
     "<code>registerAsync()</code> + <code>ConfigService</code> işlədin"),
    ("<code>Unknown authentication strategy \"jwt\"</code>",
     "<code>JwtStrategy</code> <code>providers</code>-dadır?",
     "<code>AuthModule</code>-un <code>providers</code>-ına əlavə edin"),
    ("<code>TypeError: Cannot redefine property: compare</code>",
     "ESM namespace dondurulub — <code>vi.spyOn</code> işləmir",
     "<code>vi.mock('bcryptjs', ...)</code> işlədin"),
    ("<code>RangeError: Maximum call stack size exceeded</code>",
     "Test köməkçisi özünü çağırır",
     "<code>api()</code> gövdəsində <code>request(app.getHttpServer())</code> yazın"),
    ("403 bütün endpoint-lərdə (token düzgün olsa da)",
     "Guard sırası tərsdir",
     "<code>JwtAuthGuard</code> <code>RolesGuard</code>-dan əvvəl olmalıdır"),
    ("Monitorinq endpoint-i 401 verir",
     "<code>@Public()</code> unudulub",
     "<code>/saglamliq</code>-a <code>@Public()</code> əlavə edin"),
    ("<code>pbkdf2</code> / <code>bcrypt</code> native xətası",
     "<code>bcrypt</code> paketi (C++) işlədilib",
     "<code>npm uninstall bcrypt &amp;&amp; npm i bcryptjs</code>"),
    ("Bazada <code>Promise { &lt;pending&gt; }</code> yazılıb",
     "<code>await bcrypt.hash()</code> unudulub",
     "<code>await</code> əlavə edin"),
    ("<code>@CurrentUser()</code> <code>undefined</code> qaytarır",
     "Guard işləməyib və ya sıra tərsdir",
     "<code>JwtStrategy</code> qeydiyyatını yoxlayın"),
    ("Audit cədvəlində <code>api.v1.struktur.merkezler</code>",
     "Qlobal prefiks təmizlənmir",
     "<code>cedvelAdi()</code>-də <code>replace(/^\\/api\\/v\\d+\\//, '')</code>"),
    ("E2E testləri bazada zibil qoyur",
     "<code>afterAll</code>-da təmizləmə yoxdur",
     "Yaradılan sətirləri silin"),
    ("<code>Do not know how to serialize a BigInt</code>",
     "<code>count(*)::int</code> cast yoxdur",
     "SQL-də cast edin"),
]
for x, s2, h in XETALAR:
    A('  <tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (x, s2, h))
A('</table>')
blok("block-ipucu", "💡 401 vs 403 — FƏRQİ",
     "<table>"
     "<tr><th>Kod</th><th>Mənası</th><th>Nə etməli</th></tr>"
     "<tr><td><strong>401</strong> Unauthorized</td><td>'Sən kimsən?' — token yoxdur/səhvdir</td>"
     "<td>Yenidən login ol</td></tr>"
     "<tr><td><strong>403</strong> Forbidden</td><td>'Sən kimsən, bilirəm — amma icazən yoxdur'</td>"
     "<td>Admin-dən icazə istə</td></tr>"
     "</table>"
     "<p>Frontend bu fərqi bilməlidir: 401 → login səhifəsinə yönləndir; "
     "403 → 'icazəniz yoxdur' mesajı göstər.</p>")

# ══════════════════ 24 ══════════════════
A('<h2 id="b24">24. Yoxlama siyahısı və növbəti dərs</h2>')
A('<div class="block block-yox">')
A('  <span class="block-title">YOXLAMA — BACKEND-3 HAZIRDIR?</span>')
A('  <table>')
A('    <tr><th>#</th><th>Yoxlama</th><th>Əmr / Gözlənilən</th></tr>')
SON = [
    ("Auth paketləri (5)", "<code>ls node_modules/@nestjs/jwt</code>"),
    ("Auth qovluqları (4)", "<code>ls src/auth/</code>"),
    ("JWT strategiyası", "<code>ls src/auth/strategies/jwt.strategy.ts</code>"),
    ("2 guard", "<code>ls src/auth/guards/</code>"),
    ("3 dekorator", "<code>ls src/auth/decorators/</code>"),
    ("Audit interceptor", "<code>ls src/common/interceptors/</code>"),
    ("Seed skripti", "<code>ls scripts/seed-auth.ts</code>"),
    ("Seed işləyir", "<code>npm run seed:auth</code> → 4 istifadəçi"),
    ("Build keçir", "<code>npm run build</code> → exit 0"),
    ("Unit testlər", "<code>npm test</code> → 38 passed"),
    ("e2e testlər", "<code>npx vitest run --config vitest.config.e2e.ts</code> → 62 passed"),
    ("24 marshrut", "server logunda <code>Mapped</code> sayı"),
    ("Tokensiz 401", "<code>curl .../struktur/merkezler</code> → 401"),
    ("Login token verir", "<code>curl -X POST .../auth/login</code> → <code>token</code>"),
    ("Token ilə 200", "<code>curl -H 'Authorization: Bearer ...'</code> → 200"),
    ("Səhv şifrə 401", "eyni mesaj verməlidir"),
    ("baxici yarada bilmir", "<code>POST /merkezler</code> → 403"),
    ("muhendis silə bilmir", "<code>DELETE /merkezler/:id</code> → 403"),
    ("admin hər şeyi edir", "super-rol işləyir"),
    ("Audit jurnalı dolur", "<code>curl .../hesabatlar/audit</code>"),
    ("<code>parol_hash</code> sızmır", "cavabda <code>$2b$</code> yoxdur"),
    ("Swagger-də Authorize", "<code>open localhost:4000/docs</code>"),
]
for i, (y, g) in enumerate(SON, 1):
    A('    <tr><td>%d</td><td>%s</td><td>%s</td></tr>' % (i, y, g))
A('  </table>')
A('</div>')

blok("block-ne", "NƏ GƏLİR — Backend-4",
     "<table>"
     "<tr><th>#</th><th>Mövzu</th></tr>"
     "<tr><td>1</td><td><strong>AI qatı</strong> — DeepSeek API inteqrasiyası</td></tr>"
     "<tr><td>2</td><td><strong>RAG</strong> — <code>ai.embeddingler</code>, vektor axtarış</td></tr>"
     "<tr><td>3</td><td><strong>Məlumat üzrə sual</strong> — təbii dil → SQL</td></tr>"
     "<tr><td>4</td><td><strong>Excel/PDF ixracı</strong></td></tr>"
     "<tr><td>5</td><td><strong>Docker + docker-compose</strong></td></tr>"
     "<tr><td>6</td><td><strong>GitHub Actions CI/CD</strong></td></tr>"
     "<tr><td>7</td><td><strong>İstehsalat yerləşdirmə</strong> + ehtiyat nüsxə</td></tr>"
     "</table>")
A('<div class="success-box">'
  '<strong>Backend-3 tamamlandı.</strong> API artıq <strong>bağlıdır</strong>: '
  'JWT token tələb olunur, 4 rol fərqlənir, hər dəyişiklik audit jurnalına düşür. '
  '<strong>24 endpoint · 4 rol · 100 test.</strong>'
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
hedef = KOK / "DƏRSLƏR/DS_Backend-3.html"
hedef.write_text(metn, encoding="utf-8")
print("  yazıldı: %s" % hedef)
print("  sətir sayı: %d" % len(metn.splitlines()))
print("  həcm: %.1f KB" % (len(metn.encode()) / 1024))
print("  bölmə: %d" % metn.count('<h2 id="b'))
print("  kod bloku: %d" % metn.count('<pre data-lang='))
