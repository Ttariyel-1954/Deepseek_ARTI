#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DS_Backend-3.html faylına ADDIM-ADDIM YOXLAMA blokları əlavə edir.

Hər mərhələdən sonra İKİ yoxlama bloku düşür:
  1) LOKAL      — həmin addımda qurulan şey işləyirmi?
  2) TAM BACKEND — köhnə hissələr hələ də işləyirmi? (reqressiya)

Sonunda yeni bölmə: §25 — tam yoxlama skripti (yoxla_addim.sh).

İSTİFADƏ:
    cd ~/Deepseek_ARTI/DƏRSLƏR
    python3 ds3_yoxla_elave.py
"""
from __future__ import annotations

import html
import pathlib
import re
import sys

KOK = pathlib.Path(__file__).resolve().parent
DERS = KOK / "DS_Backend-3.html"
SKRIPT = KOK.parent / "DS_Backend" / "scripts" / "yoxla_addim.sh"


def esc(metn: str) -> str:
    """< > & simvollarını HTML üçün təhlükəsiz edir."""
    return html.escape(metn, quote=False)


def blok(n: str, ad: str, lokal: str, tam: str, gozle: str) -> str:
    """Bir addımın yoxlama blokunu qurur."""
    return (
        '<div class="block block-yox">\n'
        f'  <span class="block-title">✅ ADDIM {n} YOXLAMASI — {esc(ad)}</span>\n'
        '  <p><strong>1) LOKAL</strong> — bu addımda qurduğumuz şey işləyirmi?</p>\n'
        f'<pre><code>{esc(lokal.strip())}</code></pre>\n'
        '  <p><strong>2) TAM BACKEND</strong> — köhnə hissələr hələ də işləyirmi? '
        '(reqressiya yoxlaması)</p>\n'
        f'<pre><code>{esc(tam.strip())}</code></pre>\n'
        f'  <p><strong>Gözlənilən nəticə:</strong> {gozle}</p>\n'
        '</div>\n'
    )


# ── HƏR ADDIMIN YOXLAMA MƏZMUNU ───────────────────────────────────────
# (anchor_h2_id, addım_nömrəsi, başlıq, LOKAL, TAM, GÖZLƏNİLƏN)

BLOKLAR = []

# ── ADDIM 2 — Paketlər ────────────────────────────────────────────────
BLOKLAR.append(("b3", "2", "Auth paketləri + tam reqressiya", r"""
cd ~/Deepseek_ARTI/DS_Backend

# 5 paketin versiyası
# ⚠️ 'node -p "require(...)"' İŞLƏMİR — bəzi paketlər 'exports' xəritəsi ilə
#    './package.json'-u bağlayır. Faylı BİRBAŞA oxuyuruq.
for p in @nestjs/jwt @nestjs/passport passport passport-jwt bcryptjs; do
  v=$(python3 -c "import json;print(json.load(open('node_modules/$p/package.json'))['version'])")
  printf '%-20s %s\n' "$p" "$v"
done
""", r"""
# Köhnə paketlər yerindədir?
for p in @nestjs/core @prisma/client exceljs class-validator pg; do
  v=$(python3 -c "import json;print(json.load(open('node_modules/$p/package.json'))['version'])")
  printf '%-20s %s\n' "$p" "$v"
done

# Bütün layihə hələ də qurulur?  ← ƏSAS REQRESSİYA YOXLAMASI
npm run build && echo "✅ BUILD OK"
""", "5 paket versiya verir (<code>12.0.2</code>, <code>12.0.0</code>, "
     "<code>0.7.0</code>, <code>4.0.1</code>, <code>3.0.3</code>); köhnə 5 paket də "
     "yerindədir; build <code>exit 0</code>. Build sınırsa — yeni paket köhnə kodu pozub."))

# ── ADDIM 4 — JWT strukturu ───────────────────────────────────────────
BLOKLAR.append(("b5", "4", "JWT token üç hissədən ibarətdir", r"""
# Nümunə token yarat
node -e '
  const c = Buffer.from(JSON.stringify({alg:"HS256",typ:"JWT"})).toString("base64url");
  const p = Buffer.from(JSON.stringify({sub:2,email:"admin@arti.edu.az",rol:"admin",exp:9999999999})).toString("base64url");
  console.log(c + "." + p + ".imza");
' > /tmp/numune_token.txt

N=$(cat /tmp/numune_token.txt)
echo "Hissə sayı: $(echo "$N" | awk -F. '{print NF}')"

# Header-i aç (1-ci hissə)
echo "$N" | cut -d. -f1 | python3 -c "
import sys,base64,json
s=sys.stdin.read().strip(); s+='='*(-len(s)%4)
print('HEADER :', json.loads(base64.urlsafe_b64decode(s)))
"

# Payload-u aç (2-ci hissə)
echo "$N" | cut -d. -f2 | python3 -c "
import sys,base64,json
s=sys.stdin.read().strip(); s+='='*(-len(s)%4)
print('PAYLOAD:', json.loads(base64.urlsafe_b64decode(s)))
"
""", r"""
# Strategiya və modul faylları yerindədir?
ls -1 src/auth/strategies/jwt.strategy.ts src/auth/auth.module.ts

# Build hələ də keçir?
npm run build && echo "✅ BUILD OK"
""", "<code>Hissə sayı: 3</code>; header <code>{'alg': 'HS256', 'typ': 'JWT'}</code>; "
     "payload-da <code>sub</code>, <code>email</code>, <code>rol</code>, <code>exp</code> "
     "sahələri görünür. Payload <strong>base64</strong>-dür — şifrəli DEYİL, "
     "imza ilə qorunur."))

# ── ADDIM 6 — bcrypt ──────────────────────────────────────────────────
BLOKLAR.append(("b7", "6", "bcrypt hash və compare", r"""
node -e '
  const b = require("bcryptjs");
  const h = b.hashSync("123456", 10);
  console.log("Hash       :", h);
  console.log("Uzunluq    :", h.length);
  console.log("Doğru şifrə:", b.compareSync("123456", h));
  console.log("Səhv şifrə :", b.compareSync("654321", h));
  console.log("İki hash eynidir?:", h === b.hashSync("123456", 10));
'
""", r"""
export PGPASSWORD=arti_secret_2025

# Bazadakı hash həqiqətən '123456'-dır?
HASH=$(psql -U arti_user -w -d arti_baza -tAc \
  "SELECT parol_hash FROM kadrlar.istifadeciler WHERE email='admin@arti.edu.az'")

node -e "console.log('Bazadakı şifrə 123456-dır →',
  require('bcryptjs').compareSync('123456', process.argv[1]))" "$HASH"

# ⚠️ Sütun adı 'parol_hash'-dır, 'parol' DEYİL
psql -U arti_user -w -d arti_baza -c "\d kadrlar.istifadeciler" | grep -i parol
""", "Hash 60 simvol, <code>$2b$</code> ilə başlayır; doğru şifrə "
     "<code>true</code>, səhv <code>false</code>; iki hash <strong>fərqlidir</strong> "
     "(<code>false</code>) — duz işləyir. Bazada <code>true</code>. "
     "Sütun <code>parol_hash</code>-dır; <code>parol</code> yazsanız "
     "<code>column \"parol\" does not exist</code> alacaqsınız."))

# ── ADDIM 7 — DTO ─────────────────────────────────────────────────────
BLOKLAR.append(("b8", "7", "DTO validasiya qaydaları", r"""
ls -1 src/auth/dto/

echo "── LoginDto ──"
grep -nE '@IsEmail|@MinLength|@MaxLength|email!|parol!' src/auth/dto/login.dto.ts

echo "── QeydiyyatDto ──"
grep -nE '@IsEmail|@MinLength|@IsIn|@IsOptional|ROLLAR|ad_soyad' \
  src/auth/dto/qeydiyyat.dto.ts
""", r"""
API=http://localhost:4000/api/v1

# Bütün DTO-lar yerindədir?
find src -name '*.dto.ts' | sort

# Validasiya REAL işləyir? (server işləməlidir)
curl -s -o /dev/null -w 'parol=123  → %{http_code}\n' -X POST "$API/auth/login" \
  -H 'Content-Type: application/json' -d '{"email":"admin@arti.edu.az","parol":"123"}'

curl -s -o /dev/null -w 'email=pis  → %{http_code}\n' -X POST "$API/auth/login" \
  -H 'Content-Type: application/json' -d '{"email":"pis","parol":"123456"}'

curl -s -o /dev/null -w 'düzgün     → %{http_code}\n' -X POST "$API/auth/login" \
  -H 'Content-Type: application/json' -d '{"email":"admin@arti.edu.az","parol":"123456"}'
""", "<code>find</code> 8 DTO faylı verir; LoginDto-da <code>@IsEmail</code> və "
     "<code>@MinLength(6)</code>, QeydiyyatDto-da <code>@MinLength(8)</code> və "
     "<code>@IsIn(ROLLAR)</code> var; kodlar <code>400</code>, <code>400</code>, "
     "<code>200</code>. Üçüncüsü də 400 verirsə — <code>ValidationPipe</code> "
     "<code>main.ts</code>-də qeydiyyatdan keçməyib."))

# ── ADDIM 9 — Dekoratorlar ────────────────────────────────────────────
BLOKLAR.append(("b10", "9", "Dekoratorlar və build", r"""
ls -1 src/auth/decorators/

echo "── Metadata açarları ──"
grep -n 'ACARI' src/auth/decorators/*.ts

echo "── TS1272 qoruması: 'import type' ──"
grep -rn 'import type' src/auth/ | head
""", r"""
# Dekoratorlar düzgün kompilyasiya olunur?
npm run build && echo "✅ BUILD OK"

# Nəticə faylları
ls -1 dist/auth/decorators/
""", "3 dekorator faylı; <code>PUBLIC_ACARI = 'publicdir'</code>, "
     "<code>ROLLAR_ACARI = 'rollar'</code>; <code>import type</code> ən azı "
     "<code>auth.controller.ts</code>-də var; build <code>exit 0</code> və "
     "<code>dist/auth/decorators/</code> yaranır."))

# ── ADDIM 10 — JwtStrategy ────────────────────────────────────────────
BLOKLAR.append(("b11", "10", "JwtStrategy quruldu", r"""
grep -nE 'fromAuthHeaderAsBearerToken|secretOrKey|ignoreExpiration|PassportStrategy' \
  src/auth/strategies/jwt.strategy.ts

echo "── validate() bazadan oxuyur? ──"
grep -nE 'kadrlar.istifadeciler|aktiv|UnauthorizedException|payload.sub' \
  src/auth/strategies/jwt.strategy.ts
""", r"""
npm run build && echo "✅ BUILD OK"

# Strategiya AuthModule-da qeydiyyatdadır?
grep -n 'JwtStrategy' src/auth/auth.module.ts

# Sınıq olsa server belə xəta verər:
#   Unknown authentication strategy "jwt"
""", "<code>ExtractJwt.fromAuthHeaderAsBearerToken()</code>, "
     "<code>ignoreExpiration: false</code>, "
     "<code>secretOrKey: config.get('JWT_SECRET')</code>, "
     "<code>PassportStrategy(Strategy, 'jwt')</code> görünür; "
     "<code>validate()</code> <code>kadrlar.istifadeciler</code>-dən oxuyur və "
     "<code>aktiv=false</code> olduqda <code>UnauthorizedException</code> atır."))

# ── ADDIM 11 — JwtAuthGuard (İLK CANLI YOXLAMA) ───────────────────────
BLOKLAR.append(("b12", "11", "JwtAuthGuard — tokensiz 401 (İLK CANLI YOXLAMA)", r"""
API=http://localhost:4000/api/v1

# ── Qorunan endpoint-lər TOKENSİZ 401 verməlidir ──
for yol in struktur/merkezler kadrlar/emekdaslar hesabatlar/icmal auth/profil; do
  printf '%-24s %s\n' "$yol" "$(curl -s -o /dev/null -w '%{http_code}' "$API/$yol")"
done

# POST da 401 verməlidir (body yoxdur — guard body-dən ƏVVƏL işləyir)
curl -s -o /dev/null -w 'POST merkezler           %{http_code}\n' \
  -X POST "$API/struktur/merkezler" \
  -H 'Content-Type: application/json' -d '{"ad":"test"}'

# ── @Public() istisnaları AÇIQ olmalıdır ──
curl -s -o /dev/null -w 'GET /saglamliq           %{http_code}\n' "$API/saglamliq"
curl -s "$API/saglamliq"; echo
""", r"""
# ══════════════════════════════════════════════════════════════
#  TOKEN AL və YADDA SAXLA — bundan sonra hər yerdə istifadə olunur
# ══════════════════════════════════════════════════════════════
TOKEN=$(curl -s -X POST "$API/auth/login" \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "$TOKEN" > /tmp/arti_token.txt      # ← YADDA SAXLA
echo "Token: ${TOKEN:0:40}..."

# ── Sonra fayldan OXU ──
TOKEN=$(cat /tmp/arti_token.txt)
echo "Fayldan oxundu: ${#TOKEN} simvol"

# ── Token ilə 200 gəlməlidir ──
curl -s -o /dev/null -w 'token ilə merkezler     %{http_code}\n' \
  -H "Authorization: Bearer $TOKEN" "$API/struktur/merkezler"

# ── Səhv token 401 verməlidir ──
curl -s -o /dev/null -w 'səhv token               %{http_code}\n' \
  -H "Authorization: Bearer sehv.token.deyeri" "$API/struktur/merkezler"

# ── Qlobal prefiks unudulmayıb ──
curl -s -o /dev/null -w 'prefikssiz yol           %{http_code}\n' \
  http://localhost:4000/struktur/merkezler
""", "4 qorunan yol <code>401</code>, POST <code>401</code>, "
     "<code>saglamliq</code> <code>200</code>; token ~195 simvol; token ilə "
     "<code>200</code>; səhv token <code>401</code>; prefikssiz yol "
     "<code>404</code>. Token 401 verirsə — 13-cü addıma bax (açar uyğunsuzluğu)."))

# ── ADDIM 12 — RolesGuard ─────────────────────────────────────────────
BLOKLAR.append(("b13", "12", "RolesGuard — rol matrisi", r"""
API=http://localhost:4000/api/v1
mkdir -p /tmp/arti_tokenlar

# Hər rol üçün token al və AYRICA fayla yaz
for rol in admin muhendis maliyyeci baxici; do
  T=$(curl -s -X POST "$API/auth/login" \
    -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin).get('token',''))")
  echo "$T" > "/tmp/arti_tokenlar/$rol.txt"
  printf '%-10s %s simvol\n' "$rol" "${#T}"
done
""", r"""
# ── Oxuma (GET) hamı üçün AÇIQDIR ──
for rol in admin muhendis maliyyeci baxici; do
  T=$(cat /tmp/arti_tokenlar/$rol.txt)
  printf '%-10s GET merkezler      %s\n' "$rol" \
    "$(curl -s -o /dev/null -w '%{http_code}' \
       -H "Authorization: Bearer $T" "$API/struktur/merkezler")"
done

# ── /auth/istifadeciler YALNIZ admin ──
for rol in admin muhendis maliyyeci baxici; do
  T=$(cat /tmp/arti_tokenlar/$rol.txt)
  printf '%-10s GET istifadeciler %s\n' "$rol" \
    "$(curl -s -o /dev/null -w '%{http_code}' \
       -H "Authorization: Bearer $T" "$API/auth/istifadeciler")"
done

# ── Rol tələb olunmayan endpoint hamıya açıqdır ──
T=$(cat /tmp/arti_tokenlar/baxici.txt)
curl -s -o /dev/null -w 'baxici GET ai/statistika %{http_code}\n' \
  -H "Authorization: Bearer $T" "$API/ai/statistika"
""", "4 rol token alır (hər biri ~195 simvol); GET üçün hamısı <code>200</code>; "
     "<code>/auth/istifadeciler</code> üçün admin <code>200</code>, digər üç rol "
     "<code>403</code>. 403 yerinə 401 gəlsə — guard sırası tərsdir (18-ci addım)."))

# ── ADDIM 13 — Açar uyğunluğu (real xəta) ─────────────────────────────
BLOKLAR.append(("b14", "13", "JWT açarı uyğundur? (real xəta yoxlaması)", r"""
# Tokeni AÇ və müddətini yoxla
TOKEN=$(cat /tmp/arti_token.txt)

echo "$TOKEN" | cut -d. -f2 | python3 -c "
import sys,base64,json,datetime
s=sys.stdin.read().strip(); s+='='*(-len(s)%4)
p=json.loads(base64.urlsafe_b64decode(s))
print('sub    :', p['sub'])
print('email  :', p['email'])
print('rol    :', p['rol'])
print('verilib:', datetime.datetime.fromtimestamp(p['iat']))
print('bitir  :', datetime.datetime.fromtimestamp(p['exp']))
print('müddət :', (p['exp']-p['iat'])//3600, 'saat')
"
""", r"""
# ── .env-dəki açar ──
grep JWT_SECRET .env
grep JWT_MUDDET .env

# ── ⚠️ ŞƏRHLƏRİ ÇIXARIB koda bax (şərhlərdə 'register()' sözü keçir) ──
grep -v '^[[:space:]]*\*' src/auth/auth.module.ts \
  | grep -v '^[[:space:]]*//' \
  | grep -v '^[[:space:]]*/\*' \
  | grep -n 'JwtModule'

# ── ƏSAS: token 401 YOX, 200 verməlidir ──
curl -s -o /dev/null -w 'token ilə merkezler  %{http_code}\n' \
  -H "Authorization: Bearer $(cat /tmp/arti_token.txt)" \
  http://localhost:4000/api/v1/struktur/merkezler

# ── Bütün əsas endpoint-lər də 200 olmalıdır ──
for yol in struktur/merkezler struktur/merkezler/statistika \
           kadrlar/emekdaslar hesabatlar/icmal ai/statistika; do
  printf '%-34s %s\n' "$yol" \
    "$(curl -s -o /dev/null -w '%{http_code}' \
       -H "Authorization: Bearer $(cat /tmp/arti_token.txt)" \
       "http://localhost:4000/api/v1/$yol")"
done
""", "<code>müddət: 8 saat</code>; <code>.env</code>-də <code>JWT_SECRET</code> "
     "boş deyil; kodda <strong>yalnız</strong> <code>JwtModule.registerAsync(</code> "
     "var, <code>JwtModule.register(</code> YOX; bütün endpoint-lər "
     "<code>200</code>. Əgər token düzgün imzalanmış görünür, amma hər şey "
     "<code>401</code> verirsə — <code>register()</code> <code>.env</code>-dən "
     "əvvəl işləyib və fallback açar istifadə edilib."))

# ── ADDIM 14 — Auth servisi ───────────────────────────────────────────
BLOKLAR.append(("b15", "14", "Login, timing attack və validasiya", r"""
API=http://localhost:4000/api/v1

# ── Düzgün giriş ──
curl -s -X POST "$API/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' | python3 -m json.tool

# ── ⚠️ parol_hash SIZMIR — bu əmr '0' çap etməlidir ──
curl -s -X POST "$API/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' | grep -c 'parol_hash'
""", r"""
# ── TIMING ATTACK: iki FƏRQLİ səbəb EYNİ mesaj verməlidir ──
for e in yoxdur@arti.edu.az admin@arti.edu.az; do
  printf '%-22s ' "$e"
  curl -s -X POST "$API/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$e\",\"parol\":\"sehv-sifre-2026\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['xeta']['mesaj'])"
done

# ── 4 rolun HAMISI giriş edə bilir ──
# ⚠️ JSON cismi MÜTLƏQ dəyişənə yazılmalıdır:
#    "$(curl ... -d "{\"a\":\"$x\",\"b\":\"$y\"}")" — bash bu halda
#    cismi Vergülə görə parçalayır (brace expansion) və 400 alınır.
for rol in admin muhendis maliyyeci baxici; do
  cisim="{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}"
  printf '%-10s %s\n' "$rol" "$(curl -s -o /dev/null -w '%{http_code}' \
    -X POST "$API/auth/login" -H 'Content-Type: application/json' -d "$cisim")"
done

# ── Validasiya sərhədləri ──
for c in '{"email":"admin@arti.edu.az","parol":"123"}' \
         '{"email":"pis","parol":"123456"}' \
         '{}' ; do
  printf '%-52s %s\n' "$c" "$(curl -s -o /dev/null -w '%{http_code}' \
    -X POST "$API/auth/login" -H 'Content-Type: application/json' -d "$c")"
done
""", "Cavabda <code>token</code>, <code>istifadeci</code>, <code>bitme</code> var; "
     "<code>grep -c 'parol_hash'</code> → <code>0</code>; iki fərqli səbəb eyni "
     "mesaj verir: <em>«E-poçt və ya şifrə yanlışdır»</em>; 4 rol "
     "<code>200</code>; üç səhv sorğu <code>400</code>."))

# ── ADDIM 15 — Auth controller ────────────────────────────────────────
BLOKLAR.append(("b16", "15", "Auth controller-in 4 endpoint-i", r"""
API=http://localhost:4000/api/v1
TOKEN=$(cat /tmp/arti_token.txt)

# 1) LOGIN — 200 (201 DEYİL! @HttpCode(HttpStatus.OK) işləyir?)
curl -s -o /dev/null -w 'POST login              %{http_code}\n' \
  -X POST "$API/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}'

# 2) PROFIL — cari istifadəçi
curl -s -H "Authorization: Bearer $TOKEN" "$API/auth/profil" | python3 -m json.tool
""", r"""
# 3) İSTİFADECİLER — yalnız admin
for rol in admin muhendis maliyyeci baxici; do
  T=$(cat /tmp/arti_tokenlar/$rol.txt)
  printf '%-10s GET istifadeciler %s\n' "$rol" \
    "$(curl -s -o /dev/null -w '%{http_code}' \
       -H "Authorization: Bearer $T" "$API/auth/istifadeciler")"
done

# 4) QEYDİYYAT — yalnız admin
curl -s -o /dev/null -w 'baxici POST qeydiyyat %{http_code}\n' \
  -X POST "$API/auth/qeydiyyat" -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $(cat /tmp/arti_tokenlar/baxici.txt)" \
  -d '{"email":"test@arti.edu.az","parol":"12345678","ad_soyad":"Test Testov"}'

# Profil tokensiz 401
curl -s -o /dev/null -w 'profil tokensiz        %{http_code}\n' "$API/auth/profil"
""", "<code>login</code> <code>200</code> (201 olsa — <code>@HttpCode</code> "
     "unudulub); <code>profil</code> admin məlumatını qaytarır "
     "(<code>email</code>, <code>rol</code>); <code>istifadeciler</code> admin "
     "<code>200</code>, digərləri <code>403</code>; <code>qeydiyyat</code> baxici "
     "üçün <code>403</code>; tokensiz profil <code>401</code>."))

# ── ADDIM 16 — AuthModule ─────────────────────────────────────────────
BLOKLAR.append(("b17", "16", "AuthModule — registerAsync", r"""
echo "── .env ──"
grep -E 'JWT_SECRET|JWT_MUDDET' .env

echo "── Modul ──"
grep -nE 'registerAsync|register\(|ConfigService|secret' src/auth/auth.module.ts
""", r"""
# ── Şərhləri çıxarıb koda bax ──
grep -v '^[[:space:]]*\*' src/auth/auth.module.ts \
  | grep -v '^[[:space:]]*//' \
  | grep -v '^[[:space:]]*/\*' \
  | grep -n 'JwtModule'

npm run build && echo "✅ BUILD OK"
""", "<code>.env</code>-də <code>JWT_SECRET</code> boş deyil (boşdursa "
     "<code>registerAsync</code> da kömək etmir); kodda "
     "<code>JwtModule.registerAsync(</code> var, "
     "<code>JwtModule.register(</code> YOX; build <code>exit 0</code>."))

# ── ADDIM 17 — Audit ──────────────────────────────────────────────────
BLOKLAR.append(("b18", "17", "Audit interceptor jurnal yazır", r"""
API=http://localhost:4000/api/v1
TOKEN=$(cat /tmp/arti_token.txt)
export PGPASSWORD=arti_secret_2025
PSQL="psql -U arti_user -w -d arti_baza -tAc"

# ── ƏVVƏL: neçə qeyd var? ──
EVVEL=$($PSQL "SELECT count(*)::int FROM audit.audit_log")
echo "Əvvəl: $EVVEL"

# ── POST et (jurnala YAZILMALIDIR) ──
ID=$(curl -s -X POST "$API/struktur/merkezler" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d "{\"ad\":\"Audit Test $(date +%s)\"}" \
  | python3 -c "import json,sys;print(json.load(sys.stdin).get('id',''))")
echo "Yaradılan merkez: $ID"

# ── 3 dəfə GET et (jurnala YAZILMAMALIDIR) ──
for yol in struktur/merkezler kadrlar/emekdaslar hesabatlar/icmal; do
  curl -s -o /dev/null -H "Authorization: Bearer $TOKEN" "$API/$yol"
done
""", r"""
sleep 1
SONRA=$($PSQL "SELECT count(*)::int FROM audit.audit_log")
echo "Sonra: $SONRA    (POST +1, üç GET +0 olmalıdır)"

# ── Son 3 qeyd ──
$PSQL "SELECT cedvel_adi || ' | ' || emeliyyat || ' | ' ||
              COALESCE(istifadeci,'?') || ' | ' || COALESCE(qeyd,'')
         FROM audit.audit_log ORDER BY id DESC LIMIT 3"

# ── Sütun adları (⚠️ 'emeliyyat', 'əməliyyat' DEYİL) ──
$PSQL "SELECT string_agg(column_name, ', ')
         FROM information_schema.columns
        WHERE table_schema='audit' AND table_name='audit_log'"

# ── Təmizlik ──
curl -s -o /dev/null -X DELETE "$API/struktur/merkezler/$ID" \
  -H "Authorization: Bearer $TOKEN"
echo "Test merkezi silindi: $ID"
""", "<code>Sonra = Əvvəl + 1</code> — yalnız POST yazılıb, üç GET yazılmayıb. "
     "Sonuncu qeyd: <code>struktur.merkezler | POST | admin@arti.edu.az | "
     "Ugurlu | Nms</code>. Sütunlar: <code>id, cedvel_adi, emeliyyat, setir_id, "
     "istifadeci, vaxt, qeyd</code>. GET də yazılırsa — "
     "<code>IZLENEN_METODLAR</code> səhvdir."))

# ── ADDIM 18 — app.module ─────────────────────────────────────────────
BLOKLAR.append(("b19", "18", "app.module.ts — APP_GUARD sırası", r"""
echo "── Guard sırası (sətir nömrələri ARTAN olmalıdır) ──"
grep -n 'APP_GUARD\|APP_INTERCEPTOR\|JwtAuthGuard\|RolesGuard\|AuditInterceptor' \
  src/app.module.ts
""", r"""
# ── Bütün modullar import olunub? ──
for m in PrismaModule SaglamliqModule AuthModule StrukturModule \
         KadrlarModule HesabatlarModule AiModule IxracModule; do
  printf '%-20s %s\n' "$m" "$(grep -c "$m" src/app.module.ts)"
done

npm run build && echo "✅ BUILD OK"

# ── ⚠️ Sıra REAL işləyir? 401 guard 403-dən ƏVVƏL olmalıdır ──
curl -s -o /dev/null -w 'tokensiz istifadeciler %{http_code}\n' \
  http://localhost:4000/api/v1/auth/istifadeciler
""", "<code>JwtAuthGuard</code> sətri <code>RolesGuard</code>-dan əvvəl, o da "
     "<code>AuditInterceptor</code>-dan əvvəl gəlir; 8 modul import olunub; build "
     "<code>exit 0</code>. Tokensiz <code>/auth/istifadeciler</code> "
     "<code>401</code> verməlidir — <code>403</code> verirsə, "
     "<code>RolesGuard</code> <code>JwtAuthGuard</code>-dan əvvəl qeydiyyatdadır."))

# ── ADDIM 19 — RBAC matrisi ───────────────────────────────────────────
BLOKLAR.append(("b20", "19", "RBAC matrisi — 4 rol × əməliyyat", r"""
API=http://localhost:4000/api/v1
mkdir -p /tmp/arti_tokenlar

# Hər rol üçün token
for rol in admin muhendis maliyyeci baxici; do
  curl -s -X POST "$API/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])" \
    > "/tmp/arti_tokenlar/$rol.txt"
done

# ── POST /struktur/merkezler  (admin, muhendis → 201; digərləri → 403) ──
for rol in admin muhendis maliyyeci baxici; do
  T=$(cat /tmp/arti_tokenlar/$rol.txt)
  cisim="{\"ad\":\"RBAC $rol $(date +%s)\"}"
  printf '%-10s POST merkezler  %s\n' "$rol" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$API/struktur/merkezler" \
       -H "Authorization: Bearer $T" \
       -H 'Content-Type: application/json' -d "$cisim")"
done
""", r"""
# ── DELETE /struktur/merkezler/:id  (yalnız admin → 200) ──
ID=$(psql -U arti_user -w -d arti_baza -tAc \
  "SELECT id FROM struktur.merkezler WHERE ad LIKE 'RBAC %' ORDER BY id DESC LIMIT 1")
export PGPASSWORD=arti_secret_2025

for rol in muhendis maliyyeci admin; do
  printf '%-10s DELETE merkez %-5s %s\n' "$rol" "$ID" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$API/struktur/merkezler/$ID" \
       -H "Authorization: Bearer $(cat /tmp/arti_tokenlar/$rol.txt)")"
done

# ── ⚠️ BAĞLI mərkəz 409 verməlidir (500 DEYİL) ──
curl -s -o /dev/null -w 'DELETE merkez 1 (bağlı)  %{http_code}\n' \
  -X DELETE "$API/struktur/merkezler/1" \
  -H "Authorization: Bearer $(cat /tmp/arti_tokenlar/admin.txt)"

# ── Test mərkəzlərini təmizlə (API ilə — FK qorunur) ──
psql -U arti_user -w -d arti_baza -tAc \
  "SELECT id FROM struktur.merkezler WHERE ad LIKE 'RBAC %' OR ad LIKE 'Audit %'" \
| while read -r i; do
    [ -n "$i" ] && curl -s -o /dev/null -X DELETE "$API/struktur/merkezler/$i" \
      -H "Authorization: Bearer $(cat /tmp/arti_tokenlar/admin.txt)"
    echo "təmizləndi: $i"
  done
""", "POST: admin <code>201</code>, muhendis <code>201</code>, maliyyeci "
     "<code>403</code>, baxici <code>403</code>. DELETE: muhendis "
     "<code>403</code>, maliyyeci <code>403</code>, admin <code>200</code>. "
     "Bağlı mərkəz <code>409</code> — <strong>500 olsa</strong>, "
     "<code>sil()</code> bütün FK-ları yoxlamır "
     "(<code>shobeler</code>, <code>emekdaslar</code>, <code>rehberlik</code>)."))

# ── ADDIM 20 — Seed ───────────────────────────────────────────────────
BLOKLAR.append(("b21", "20", "Seed skripti — idempotentlik", r"""
grep -n 'seed:auth' package.json
grep -nE 'ON CONFLICT|bcrypt.hash|DATABASE_URL' scripts/seed-auth.ts

# ── Seed-i işə sal ──
npm run seed:auth
""", r"""
export PGPASSWORD=arti_secret_2025
PSQL="psql -U arti_user -w -d arti_baza -tAc"

# ── ⚠️ İKİNCİ DƏFƏ işə sal — say DƏYİŞMƏMƏLİDİR ──
npm run seed:auth
echo "İstifadəçi sayı: $($PSQL 'SELECT count(*)::int FROM kadrlar.istifadeciler')"

# ── Rollar üzrə bölgü ──
$PSQL "SELECT rol || ': ' || count(*)::int
         FROM kadrlar.istifadeciler GROUP BY rol ORDER BY rol"

# ── Seed-dən sonra giriş işləyir ──
curl -s -o /dev/null -w 'admin girişi  %{http_code}\n' \
  -X POST http://localhost:4000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}'

# ── ⚠️ 'tsx' yoxdursa: npm install -D tsx@^4.19.0 ──
""", "İki işə salmadan sonra da <strong>4</strong> istifadəçi (artıbsa — "
     "<code>ON CONFLICT</code> yoxdur); hər roldan <code>1</code>; giriş "
     "<code>200</code>. <code>tsx: command not found</code> alsanız — "
     "<code>npm install -D tsx@^4.19.0</code>."))

# ── ADDIM 21 — Testlər ────────────────────────────────────────────────
BLOKLAR.append(("b22", "21", "Bütün testlər (unit + e2e)", r"""
# ── Unit testlər (e2e konfiqurasiyadan XARİC edilib) ──
npm test

# ── e2e testlər ──
npx vitest run --config vitest.config.e2e.ts
""", r"""
# ── Yalnız auth testləri ──
npx vitest run src/auth/auth.service.spec.ts
npx vitest run --config vitest.config.e2e.ts test/backend3.e2e-spec.ts

# ── Build ──
npm run build && echo "✅ BUILD OK"

# ── Yekun gözlənti ──
echo "78 unit + 91 e2e = 169 test"
""", "<code>Tests 78 passed (78)</code> və <code>Tests 91 passed (91)</code>; "
     "build <code>exit 0</code>. e2e testləri unit konfiqurasiyasında da işə "
     "düşürsə — <code>vitest.config.ts</code>-də <code>exclude</code>-a "
     "<code>e2e-spec</code> əlavə edin."))

# ── ADDIM 22 — Backend-2 testləri ─────────────────────────────────────
BLOKLAR.append(("b23", "22", "Backend-2 testləri token ilə yeniləndimi", r"""
echo "── Token köməkçisi varmı? ──"
grep -nE 'const api|Bearer|auth/login|let token' test/backend2.e2e-spec.ts | head

echo "── ⚠️ Sonsuz rekursiya yoxlaması (BOŞ çıxmalıdır) ──"
grep -n 'const api = () =>[[:space:]]*api()' test/backend2.e2e-spec.ts
echo "(boş = yaxşı)"
""", r"""
# ── Backend-2 testləri hələ də keçir? ──
npx vitest run --config vitest.config.e2e.ts test/backend2.e2e-spec.ts

# ── Üç e2e faylının hamısı ──
ls -1 test/*.e2e-spec.ts
npx vitest run --config vitest.config.e2e.ts
""", "<code>Test Files 1 passed</code>, <code>Tests 31 passed</code>; "
     "<code>const api = () => api()</code> axtarışı <strong>heç nə "
     "tapmamalıdır</strong> — tapsa, köməkçi özünü çağırır və "
     "<code>RangeError: Maximum call stack size exceeded</code> alacaqsınız."))


# ── YENİ BÖLMƏ: §25 — tam yoxlama skripti ─────────────────────────────
def yeni_bolme() -> str:
    if not SKRIPT.exists():
        sys.exit(f"XƏTA: skript tapılmadı: {SKRIPT}")
    kod = SKRIPT.read_text(encoding="utf-8")
    setir = kod.count("\n") + 1
    return f'''<h2 id="b25">25. Addım-addım yoxlama skripti — tam kod</h2>
<div class="block block-ne">
  <span class="block-title">NƏ EDƏCƏYİK</span>
  <p>Bütün 19 addımın yoxlamasını bir skriptə yığacağıq. Skript hər addımda
  <strong>iki</strong> şeyi yoxlayır: <strong>LOKAL</strong> (həmin addım düzgün
  quruldu?) və <strong>TAM BACKEND</strong> (köhnə hissələr hələ də işləyir?).</p>
</div>
<div class="block block-izah">
  <span class="block-title">İZAH — skriptin quruluşu</span>
  <table>
    <tr><th>Hissə</th><th>Nə edir</th></tr>
    <tr><td><code>yoxla()</code></td><td>Gözlənilən ilə faktiki nəticəni tutuşdurur, sayır</td></tr>
    <tr><td><code>token_al()</code></td><td>Login edib tokeni <code>/tmp/arti_token.txt</code>-ə <strong>yazır</strong></td></tr>
    <tr><td><code>token_oxu()</code></td><td>Tokeni fayldan <strong>oxuyur</strong></td></tr>
    <tr><td><code>kod()</code></td><td>Endpoint-ə sorğu göndərib HTTP kodunu qaytarır</td></tr>
    <tr><td><code>addim_N()</code></td><td>Bir addımın bütün yoxlamaları</td></tr>
  </table>
</div>
<div class="block block-ipucu">
  <span class="block-title">💡 İSTİFADƏ QAYDALARI</span>
  <pre><code>cd ~/Deepseek_ARTI/DS_Backend

# Server AYRI terminalda işləməlidir (canlı yoxlamalar üçün)
npm run start:dev

# Bütün addımlar
bash scripts/yoxla_addim.sh

# Yalnız bir addım
bash scripts/yoxla_addim.sh 13

# Addım aralığı
bash scripts/yoxla_addim.sh 7 12

# Addımların siyahısı
bash scripts/yoxla_addim.sh siyahi

# Başqa portda işləyirsə
API=http://localhost:4001/api/v1 bash scripts/yoxla_addim.sh</code></pre>
  <p><strong>Çıxış kodu:</strong> <code>0</code> — hər şey keçdi;
  <code>1</code> — ən azı bir yoxlama uğursuz. CI-da birbaşa istifadə edə bilərsiniz.</p>
</div>
<div class="block block-xeber">
  <span class="block-title">⚠️ DİQQƏT — server işləmirsə</span>
  <p>11, 12, 13, 14, 15, 17, 19, 20 nömrəli addımlar <strong>canlı server</strong>
  tələb edir. Server yoxdursa skript onları <em>atlandı</em> kimi işarələyir və
  yalançı xəta vermir. Fayl və baza yoxlamaları (1, 2, 4, 6, 7, 9, 10, 16, 18, 21, 22)
  serversiz də işləyir.</p>
</div>
<div class="block block-yox">
  <span class="block-title">✅ YOXLAMA 25 — Skript işləyir?</span>
  <pre><code>cd ~/Deepseek_ARTI/DS_Backend

# 1) Sintaksis
bash -n scripts/yoxla_addim.sh &amp;&amp; echo "✅ SINTAKSIS OK"

# 2) Addımların siyahısı
bash scripts/yoxla_addim.sh siyahi

# 3) Tam işə salma (server işləməlidir)
bash scripts/yoxla_addim.sh

# Gözlənilən son sətirlər:
#   NƏTİCƏ:  209 keçdi
#   ✅ BÜTÜN YOXLAMALAR KEÇDİ</code></pre>
</div>
<div class="block block-izah">
  <span class="block-title">📄 scripts/yoxla_addim.sh — TAM KOD ({setir} sətir)</span>
  <pre><code>{esc(kod)}</code></pre>
</div>
'''


# ── KÖMƏKÇİ: TOC və başlıqları yenilə ────────────────────────────────
def metni_cevir(metn: str) -> str:
    # Köhnəlmiş test saylarını düzəlt
    metn = metn.replace(
        'NestJS 12 · Passport · JWT · bcrypt · 100 test',
        'NestJS 12 · Passport · JWT · bcrypt · 169 test',
    )
    metn = metn.replace(
        '<h2 id="b21">21. Testlər — 38 unit + 62 e2e</h2>',
        '<h2 id="b21">21. Testlər — 78 unit + 91 e2e</h2>',
    )
    metn = metn.replace(
        '<li><a href="#b21">Testlər — 38 unit + 62 e2e</a></li>',
        '<li><a href="#b21">Testlər — 78 unit + 91 e2e</a></li>',
    )
    metn = metn.replace(
        '<li><a href="#b24">Yoxlama siyahısı və növbəti dərs</a></li>',
        '<li><a href="#b24">Yoxlama siyahısı və növbəti dərs</a></li>\n'
        '    <li><a href="#b25">Addım-addım yoxlama skripti — tam kod</a></li>',
    )
    metn = metn.replace(
        '<tr><td>10</td><td>Unit testlər</td><td><code>npm test</code> → 38 passed</td></tr>',
        '<tr><td>10</td><td>Unit testlər</td><td><code>npm test</code> → 78 passed</td></tr>',
    )
    metn = metn.replace(
        '<tr><td>11</td><td>e2e testlər</td>'
        '<td><code>npx vitest run --config vitest.config.e2e.ts</code> → 62 passed</td></tr>',
        '<tr><td>11</td><td>e2e testlər</td>'
        '<td><code>npx vitest run --config vitest.config.e2e.ts</code> → 91 passed</td></tr>',
    )
    metn = metn.replace(
        '<tr><td>12</td><td>24 marshrut</td>',
        '<tr><td>12</td><td>35 marshrut</td>',
    )
    metn = metn.replace(
        '<strong>24 endpoint · 4 rol · 100 test.</strong>',
        '<strong>35 endpoint · 4 rol · 169 test · 209 avtomatik yoxlama.</strong>',
    )

    # ── Köhnə YOXLAMA 2 blokundaki sınıq əmri düzəlt ──
    # 'node -p "require(...)"' @nestjs/jwt, @nestjs/passport və bcryptjs üçün
    # ERR_PACKAGE_PATH_NOT_EXPORTED verir — faylı birbaşa oxuyuruq.
    köhnə = (
        'for p in @nestjs/jwt @nestjs/passport passport passport-jwt bcryptjs; do\n'
        '  echo "$p: $(node -p "require(\'$p/package.json\').version")"\n'
        'done'
    )
    yeni = (
        'for p in @nestjs/jwt @nestjs/passport passport passport-jwt bcryptjs; do\n'
        '  v=$(python3 -c "import json;print(json.load(open(\'node_modules/$p/package.json\'))[\'version\'])")  \n'.rstrip(" \n") + "\n"
        '  echo "$p: $v"\n'
        'done'
    )
    if köhnə not in metn:
        sys.exit("XƏTA: köhnə YOXLAMA 2 bloku tapılmadı")
    metn = metn.replace(köhnə, yeni)

    # ── Gözlənilən çıxışı KOD BLOKUNUN İÇİNDƏN çıxar ──
    # Kopyala düyməsi hər şeyi götürür; çıxış sətirləri əmr kimi icra olunur.
    köhnə2 = (
        'done\n'
        '\n'
        '@nestjs/jwt: 12.0.2\n'
        '@nestjs/passport: 12.0.0\n'
        'passport: 0.7.0\n'
        'passport-jwt: 4.0.1\n'
        'bcryptjs: 3.0.3</code></pre>'
    )
    yeni2 = (
        'done</code></pre>\n'
        '  <p><strong>Gözlənilən nəticə:</strong> '
        '<code>@nestjs/jwt: 12.0.2</code>, '
        '<code>@nestjs/passport: 12.0.0</code>, '
        '<code>passport: 0.7.0</code>, '
        '<code>passport-jwt: 4.0.1</code>, '
        '<code>bcryptjs: 3.0.3</code></p>'
    )
    if metn.count(köhnə2) != 1:
        sys.exit(f"XƏTA: gözlənilən çıxış bloku {metn.count(köhnə2)} dəfə tapıldı")
    metn = metn.replace(köhnə2, yeni2)

    return metn


def main() -> None:
    if not DERS.exists():
        sys.exit(f"XƏTA: dərs tapılmadı: {DERS}")

    metn = DERS.read_text(encoding="utf-8")
    evvelki_setir = metn.count("\n") + 1

    if 'id="b25"' in metn:
        sys.exit("XƏTA: §25 artıq əlavə olunub — əvvəlcə geri qaytarın.")

    # ── 1) Blokları düzgün yerə əlavə et ──
    for anchor, n, ad, lokal, tam, gozle in BLOKLAR:
        nişan = f'<h2 id="{anchor}">'
        say = metn.count(nişan)
        if say != 1:
            sys.exit(f"XƏTA: '{nişan}' {say} dəfə tapıldı (1 olmalıdır)")
        metn = metn.replace(nişan, blok(n, ad, lokal, tam, gozle) + nişan, 1)

    # ── 2) §25-i container-in sonuna əlavə et ──
    son = '</div>\n<script>'
    if metn.count(son) != 1:
        sys.exit(f"XƏTA: container sonu {metn.count(son)} dəfə tapıldı")
    metn = metn.replace(son, yeni_bolme() + son, 1)

    # ── 3) Köhnə sayları düzəlt ──
    metn = metni_cevir(metn)

    DERS.write_text(metn, encoding="utf-8")

    yeni_setir = metn.count("\n") + 1
    print(f"✅ {DERS.name}")
    print(f"   Əvvəl : {evvelki_setir} sətir")
    print(f"   Sonra : {yeni_setir} sətir  (+{yeni_setir - evvelki_setir})")
    print(f"   Blok  : {len(BLOKLAR)} addım yoxlaması + §25")


if __name__ == "__main__":
    main()
