# -*- coding: utf-8 -*-
"""DƏRS 3 — yekun test skriptləri (III.1–III.20)."""

DERSLER = [
    dict(
        rumuz="III",
        ad="Dərs 3 — Autentifikasiya, rollar və audit",
        qisa="JWT açarı, login və qeydiyyat DTO-ları, üç dekorator "
             "(<code>@Public</code>, <code>@Roles</code>, "
             "<code>@CurrentUser</code>), <code>JwtStrategy</code>, iki guard, "
             "<code>AuthService</code> və timing attack qoruması, "
             "<code>AuthModule</code>, <code>AuditInterceptor</code>, seed "
             "skripti və RBAC matrisi.",
        testler=[
            dict(
                no="III.1",
                ad="Auth paketləri və JWT açarı",
                giris=(
                    "Bu test Dərs 3-ün birinci addımını yoxlayır: "
                    "autentifikasiya üçün lazım olan paketlərin quraşdırılmasını "
                    "və JWT açarının <code>.env</code> faylında saxlanmasını. "
                    "Açar koda yazılsaydı, kodu görən hər kəs istənilən "
                    "istifadəçi üçün token imzalaya bilərdi. Skript açarın "
                    "uzunluğunu göstərir, dəyərini isə <em>çap etmir</em>."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── Auth paketləri ──"
for p in @nestjs/jwt @nestjs/passport passport passport-jwt bcryptjs; do
  v=$(python3 -c "import json;print(json.load(open('node_modules/$p/package.json'))['version'])" 2>/dev/null)
  echo "  %-20s %s" | sed "s/%-20s/$p/" | sed "s/%s/${v:-YOXDUR}/"
done

echo "── JWT ayarları (.env) ──"
for a in JWT_SECRET JWT_MUDDET; do
  d=$(grep "^$a=" .env | sed "s/^$a=//; s/\"//g")
  echo "  $a → ${#d} simvol (dəyər göstərilmir)"
done

echo "── Açar koda hardcode yazılıbmı? ──"
if grep -rn 'JWT_SECRET' src/ --include=*.ts | grep -qv 'configService\|config\.get\|ConfigService'; then
  echo "  ⚠️ koda yazılmış istinad var — yoxlayın"
else
  echo "  ✓ açar yalnız ConfigService ilə oxunur, koda yazılmayıb"
fi

echo "── .env git-ə düşürmü? ──"
grep -q '^\.env$' .gitignore && echo "  ✓ .env .gitignore-dadır" || echo "  ✗ .env git-ə düşə bilər!"
''',
            ),
            dict(
                no="III.2",
                ad="Login DTO validasiyası",
                giris=(
                    "Bu test Dərs 3-ün ikinci addımını yoxlayır: "
                    "<code>LoginDto</code>-nun yanlış girişi bazaya çatmadan "
                    "rədd etməsini. E-poçt formatı və şifrənin minimum uzunluğu "
                    "yoxlanılır. Validasiya olmasaydı hər sorğu bazaya gedərdi "
                    "və boş şifrə ilə cəhdlər hesablama yükü yaradardı."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

yoxla() {
  printf '  %-46s → %s\n' "$1" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/auth/login" \
        -H 'Content-Type: application/json' -d "$2")"
}

yoxla "düzgün e-poçt + düzgün şifrə"  '{"email":"admin@arti.edu.az","parol":"123456"}'
yoxla "pis e-poçt formatı"            '{"email":"admin","parol":"123456"}'
yoxla "şifrə 3 simvol"                '{"email":"admin@arti.edu.az","parol":"123"}'
yoxla "boş cisim"                     '{}'
yoxla "e-poçt yoxdur, şifrə var"      '{"parol":"123456"}'

echo "── Detallı mesaj (pis e-poçt) ──"
curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin","parol":"123456"}' | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  mesaj :', d['xeta']['mesaj'])
for x in d['xeta'].get('detallar', []): print('  detal :', x)
"
''',
            ),
            dict(
                no="III.3",
                ad="Uğurlu giriş — token və müddət",
                giris=(
                    "Bu test Dərs 3-ün altıncı addımını yoxlayır: login "
                    "cavabının formasını. Cavabda token, istifadəçi məlumatı və "
                    "müddət olmalıdır. Token üç nöqtə ilə ayrılmış üç hissədən "
                    "ibarətdir — bu, onun JWT olduğunu göstərir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  cavab sahələri :', ', '.join(d.keys()))
print('  token hissəsi  :', len(d['token'].split('.')), '(header.payload.signature)')
print('  token uzunluğu :', len(d['token']), 'simvol')
print('  istifadəçi     :', d['istifadeci']['ad_soyad'], '/', d['istifadeci']['rol'])
print('  bitme          :', d['bitme'])
print()
print('  token başlanğıcı:', d['token'][:32] + '…')
"
''',
            ),
            dict(
                no="III.4",
                ad="Tokenin içi — yük (payload) açılır",
                giris=(
                    "Bu test tokenin içində nə olduğunu göstərir: JWT gizli "
                    "deyil, sadəcə base64 ilə kodlanmışdır — hər kəs oxuya "
                    "bilər, amma <em>dəyişə</em> bilməz, çünki imza var. "
                    "Yükdə istifadəçinin kimliyi, rolu və vaxtları olur. "
                    "Skript yükü açıb göstərir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"muhendis@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "$TOKEN" | python3 -c "
import base64, json, sys
token = sys.stdin.read().strip()
def ac(h):
    h += '=' * (-len(h) % 4)
    return json.loads(base64.urlsafe_b64decode(h))
b, y, i = token.split('.')
print('── BAŞLIQ (header) ──')
for k, v in ac(b).items(): print('  %-6s %s' % (k, v))
print('── YÜK (payload) ──')
for k, v in ac(y).items(): print('  %-6s %s' % (k, v))
print('── İMZA ──')
print('  ', i[:40] + '…')
"
''',
            ),
            dict(
                no="III.5",
                ad="Token müddəti — exp minus iat",
                giris=(
                    "Bu test tokenin nə qədər yaşadığını hesablayır: "
                    "<code>exp</code> (bitmə) minus <code>iat</code> (verilmə) "
                    "= 8 saat = 28800 saniyə. Müddət sonsuz olsaydı, oğurlanmış "
                    "token əbədi işləyərdi. Skript rəqəmi həm saniyə, həm saat "
                    "kimi göstərir və tokenin bitmə vaxtını insan oxunaqlı edir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "$TOKEN" | python3 -c "
import base64, json, sys, datetime
def ac(h):
    h += '=' * (-len(h) % 4); return json.loads(base64.urlsafe_b64decode(h))
y = ac(sys.stdin.read().strip().split('.')[1])
muddet = y['exp'] - y['iat']
print('  iat (verilib)  :', datetime.datetime.fromtimestamp(y['iat']))
print('  exp (bitir)    :', datetime.datetime.fromtimestamp(y['exp']))
print('  müddət         :', muddet, 'saniyə =', muddet/3600, 'saat')
print('  .env-dəki sətir:', open('.env').read().strip().splitlines()[-0] and [l for l in open('.env') if l.startswith('JWT_MUDDET')][0].strip())
"
''',
            ),
            dict(
                no="III.6",
                ad="⚠️ Şifrə hash-i heç yerdə sızmır",
                giris=(
                    "Bu test Dərs 3-ün ən vacib təhlükəsizlik yoxlamasıdır: "
                    "şifrənin hash-i nə login cavabında, nə tokenin içində "
                    "görünməməlidir. Hash sızsa, hücumçu onu özü ilə aparıb "
                    "offline sındırmağa çalışa bilər. Skript tokeni açıb bütün "
                    "mətn içində bcrypt izi axtarır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

CAVAB=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}')
TOKEN=$(printf '%s' "$CAVAB" | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── 1) Login cavabında ──"
printf '%s' "$CAVAB" | grep -q 'parol_hash' && echo "  ✗ parol_hash SIZIB!" || echo "  ✓ parol_hash yoxdur"
printf '%s' "$CAVAB" | grep -q '\$2[aby]\$' && echo "  ✗ bcrypt hash-i SIZIB!" || echo "  ✓ bcrypt izi yoxdur"

echo "── 2) Tokenin içində ──"
printf '%s' "$TOKEN" | grep -q 'parol_hash' && echo "  ✗ SIZIB!" || echo "  ✓ parol_hash yoxdur"
printf '%s' "$TOKEN" | grep -q '\$2[aby]\$' && echo "  ✗ bcrypt izi SIZIB!" || echo "  ✓ bcrypt izi yoxdur"

echo "── 3) Bazada şifrə NECƏ saxlanılır ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  ' || email || ' → ' || left(parol_hash, 7) || '… (' || length(parol_hash) || ' simvol)'
  FROM kadrlar.istifadeciler ORDER BY id" 
echo "  (bcrypt hash-i geri açıla bilmir — yalnız müqayisə olunur)"
''',
            ),
            dict(
                no="III.7",
                ad="⚠️ Timing attack qoruması — eyni mesaj",
                giris=(
                    "Bu test Dərs 3-ün altıncı addımındaki <em>timing attack</em> "
                    "qorumasını yoxlayır. «Belə e-poçt yoxdur» deyilsəydi, "
                    "hücumçu hansı e-poçtların sistemdə olduğunu öyrənərdi. "
                    "Ona görə hər iki hal eyni mesajı qaytarır və hər iki halda "
                    "hash müqayisəsi aparılır ki, cavab vaxtı da fərqlənməsin."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── Mövcud e-poçt + səhv şifrə ──"
curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"sehv-parol-2026"}' | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  mesaj :', d['xeta']['mesaj'])"

echo "── Mövcud OLMAYAN e-poçt + səhv şifrə ──"
curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"yoxdur@arti.edu.az","parol":"sehv-parol-2026"}' | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  mesaj :', d['xeta']['mesaj'])"

echo "── Cavab vaxtları (fərq kiçik olmalıdır) ──"
for e in admin@arti.edu.az yoxdur@arti.edu.az; do
  t=$( { /usr/bin/time -p curl -s -o /dev/null -X POST "$A/auth/login" \
        -H 'Content-Type: application/json' \
        -d "{\"email\":\"$e\",\"parol\":\"sehv-parol-2026\"}"; } 2>&1 | awk '/real/{print $2}')
  printf '  %-22s %s san\n' "$e" "$t"
done

echo "── Saxta hash harada istifadə olunur? ──"
grep -n 'fake\|saxta\|DUMMY\|compare' src/auth/auth.service.ts | head -5 | sed 's/^/  /'
''',
            ),
            dict(
                no="III.8",
                ad="@Public() — açıq endpointlər",
                giris=(
                    "Bu test Dərs 3-ün üçüncü və səkkizinci addımını yoxlayır: "
                    "hansı endpoint-lərin autentifikasiya tələb etmədiyini. "
                    "Sistem bağlıdır — <code>@Public()</code> ilə işarələnənlər "
                    "istisnadır. Skript onları həm canlı yoxlayır, həm də "
                    "koddan tapır ki, uyğunsuzluq olmasın."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── Tokensiz çağırışlar ──"
for yol in "" "/saglamliq"; do
  printf '  GET %-14s → %s\n' "/$yol" "$(curl -s -o /dev/null -w '%{http_code}' "$A$yol")"
done
printf '  POST %-13s → %s (pis cisim, 401 DEYİL, 400 olmalı)\n' "/auth/login" \
  "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/auth/login" \
      -H 'Content-Type: application/json' -d '{}')"

echo "── Kodda @Public() işarələnənlər ──"
grep -rn -A2 '@Public()' src/ --include=*.controller.ts | grep -E '@Public|@(Get|Post)' | sed 's/^/  /'
''',
            ),
            dict(
                no="III.9",
                ad="Qorunan endpoint — tokensiz 401",
                giris=(
                    "Bu test Dərs 3-ün beşinci addımını yoxlayır: "
                    "<code>JwtAuthGuard</code>-ın hər qorunan endpointi "
                    "bağlamasını. Sekiz endpoint tokensiz yoxlanılır və "
                    "<strong>hamısı 401</strong> verməlidir. Guard qeyd "
                    "olunmasaydı bütün bu məlumat açıq olardı."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── Tokensiz GET sorğuları (hamısı 401 olmalıdır) ──"
for yol in /struktur/merkezler /struktur/merkezler/1 /struktur/merkezler/statistika \
           /kadrlar/emekdaslar /kadrlar/emekdaslar/1 /kadrlar/emekdaslar/icmal \
           /auth/profil /auth/istifadeciler; do
  printf '  %-34s → %s\n' "$yol" "$(curl -s -o /dev/null -w '%{http_code}' "$A$yol")"
done

echo "── Birinin cavabı ──"
curl -s "$A/struktur/merkezler" | python3 -m json.tool
''',
            ),
            dict(
                no="III.10",
                ad="Saxta token — imza yoxlanılır",
                giris=(
                    "Bu test tokenin <em>imzalandığını</em> sübut edir: yükü "
                    "dəyişib yenidən göndərsək server imzanı uyğunsuz tapır. "
                    "JWT-nin yükü sadəcə base64-dir, ona görə hər kəs oxuya "
                    "bilər — amma dəyişə bilməz. Bu, autentifikasiyanın təməl "
                    "prinsipidir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"baxici@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── 1) Həqiqi token (baxici) ──"
printf '  /auth/profil            → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H "$H")"

SAXTA=$(printf '%s' "$TOKEN" | python3 -c "
import base64, json, sys
b, y, i = sys.stdin.read().strip().split('.')
def ac(h):
    h += '=' * (-len(h) % 4); return json.loads(base64.urlsafe_b64decode(h))
def kodla(o):
    return base64.urlsafe_b64encode(json.dumps(o).encode()).decode().rstrip('=')
yeni = ac(y); yeni['rol'] = 'admin'
print(b + '.' + kodla(yeni) + '.' + i)")

echo "── 2) Yükü dəyişilmiş token (rol → admin) ──"
printf '  /auth/profil            → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H "Authorization: Bearer $SAXTA")"
printf '  /auth/istifadeciler     → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/istifadeciler" -H "Authorization: Bearer $SAXTA")"

echo "── 3) Cavab ──"
curl -s "$A/auth/profil" -H "Authorization: Bearer $SAXTA" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  kod  :', d['xeta']['kod']); print('  mesaj:', d['xeta']['mesaj'])"

echo "── 4) Tamamilə uydurma token ──"
printf '  uydurma.token.imza      → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H 'Authorization: Bearer uydurma.token.imza')"
''',
            ),
            dict(
                no="III.11",
                ad="⚠️ JwtStrategy tokeni BAZADAN yoxlayır",
                giris=(
                    "Bu test Dərs 3-ün dördüncü addımını yoxlayır: strategiyanın "
                    "tokeni sadəcə imzasına görə deyil, <em>bazadan</em> da "
                    "yoxladığını. İstifadəçi işdən çıxarılsa və ya deaktiv "
                    "edilsə, onun mövcud tokeni dərhal işləməyəcək. Skript "
                    "müvəqqəti olaraq istifadəçini deaktiv edir, yoxlayır və "
                    "hər halda geri qaytarır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

# ⚠️ Skript nə olursa olsun istifadəçini AKTİV saxlayır
geri_qaytar() {
  psql -U arti_user -d arti_baza -q -c \
    "UPDATE kadrlar.istifadeciler SET aktiv = true WHERE email = 'baxici@arti.edu.az'" 2>/dev/null
}
trap geri_qaytar EXIT

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"baxici@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── 1) İstifadəçi aktivdir ──"
printf '  /auth/profil → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H "$H")"

echo "── 2) İstifadəçi deaktiv edilir (token DƏYİŞMİR) ──"
psql -U arti_user -d arti_baza -q -c \
  "UPDATE kadrlar.istifadeciler SET aktiv = false WHERE email = 'baxici@arti.edu.az'"
printf '  /auth/profil → %s  (eyni tokenlə!)\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H "$H")"
curl -s "$A/auth/profil" -H "$H" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  mesaj :', d['xeta']['mesaj'])"

echo "── 3) İstifadəçi yenidən aktiv edilir ──"
geri_qaytar
printf '  /auth/profil → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H "$H")"

echo "── Strategiyanın yoxlaması ──"
grep -n 'aktiv\|findUnique\|queryRaw\|Unauthorized' src/auth/strategies/jwt.strategy.ts | head -6 | sed 's/^/  /'
''',
            ),
            dict(
                no="III.12",
                ad="RBAC matrisi — POST /struktur/merkezler",
                giris=(
                    "Bu test Dərs 3-ün beşinci addımını yoxlayır: "
                    "<code>RolesGuard</code>-ın dörd rolu ayırd etməsini. "
                    "<code>admin</code> və <code>muhendis</code> mərkəz yarada "
                    "bilir, <code>maliyyeci</code> və <code>baxici</code> isə "
                    "<strong>403</strong> alır. Skript hər cəhddən sonra "
                    "yaradılanı silir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── @Roles('admin','muhendis') — POST /struktur/merkezler ──"
for rol in admin muhendis maliyyeci baxici; do
  T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  KOD=$(curl -s -o /tmp/_m.json -w '%{http_code}' -X POST "$A/struktur/merkezler" \
    -H "Authorization: Bearer $T" -H 'Content-Type: application/json' \
    -d "{\"ad\":\"RBAC testi — $rol\",\"tip\":\"merkez\"}")
  printf '  %-10s → %s\n' "$rol" "$KOD"
  if [ "$KOD" = "201" ]; then
    ID=$(python3 -c "import json;print(json.load(open('/tmp/_m.json'))['id'])")
    curl -s -o /dev/null -X DELETE "$A/struktur/merkezler/$ID" -H "Authorization: Bearer $TOKEN"
  fi
done
rm -f /tmp/_m.json

echo "── Controller-də dekorator ──"
grep -n -B2 "'merkezler')" src/struktur/struktur.controller.ts | head -8 | sed 's/^/  /'
''',
            ),
            dict(
                no="III.13",
                ad="RBAC — DELETE yalnız admin",
                giris=(
                    "Bu test ən sərt qaydayı yoxlayır: silmə əməliyyatı yalnız "
                    "<code>admin</code> roluna açıqdır. <code>muhendis</code> "
                    "yarada bilir, amma silə bilmir — bu, qəsdən belə "
                    "qurulub, çünki silmə geri qaytarıla bilməyən əməliyyatdır. "
                    "Skript hər rolun cavabını göstərir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

ADMIN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

# Yoxlama üçün boş mərkəz yaradırıq
ID=$(curl -s -X POST "$A/struktur/merkezler" -H "Authorization: Bearer $ADMIN" \
  -H 'Content-Type: application/json' -d '{"ad":"Silme testi","tip":"merkez"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")
echo "  Yoxlama mərkəzi yaradıldı: id=$ID"

echo "── @Roles('admin') — DELETE /struktur/merkezler/$ID ──"
for rol in muhendis maliyyeci baxici; do
  T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  printf '  %-10s → %s\n' "$rol" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$A/struktur/merkezler/$ID" -H "Authorization: Bearer $T")"
done

echo "── admin → 200 ──"
curl -s -X DELETE "$A/struktur/merkezler/$ID" -H "Authorization: Bearer $ADMIN" \
  | python3 -c "import json,sys;print('  silindi:', json.load(sys.stdin)['ad'])"
''',
            ),
            dict(
                no="III.14",
                ad="RBAC — istifadəçi siyahısı yalnız admin",
                giris=(
                    "Bu test <code>GET /auth/istifadeciler</code> endpointinin "
                    "yalnız <code>admin</code> üçün açıq olduğunu yoxlayır. "
                    "İstifadəçi siyahısı həssas məlumatdır — kimin sistemdə "
                    "olduğunu bilmək kifayət edir ki, hücumçu hədəf seçsin. "
                    "Digər üç rol <strong>403</strong> almalıdır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── GET /auth/istifadeciler ──"
for rol in admin muhendis maliyyeci baxici; do
  T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  KOD=$(curl -s -o /tmp/_u.json -w '%{http_code}' "$A/auth/istifadeciler" -H "Authorization: Bearer $T")
  EK=""
  [ "$KOD" = "200" ] && EK="($(python3 -c "import json;print(len(json.load(open('/tmp/_u.json'))))") istifadəçi)"
  printf '  %-10s → %s %s\n' "$rol" "$KOD" "$EK"
done
rm -f /tmp/_u.json

echo "── Admin görən məlumat ──"
T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
curl -s "$A/auth/istifadeciler" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
for u in json.load(sys.stdin):
    print('  %-24s %-10s %s' % (u['email'], u['rol'], u['ad_soyad']))
"
''',
            ),
            dict(
                no="III.15",
                ad="admin super-rolu",
                giris=(
                    "Bu test <code>RolesGuard</code>-daki xüsusi qaydayı "
                    "yoxlayır: <code>admin</code> hər endpointə girə bilir, "
                    "hətta dekoratorda adı çəkilməsə də. Bu, super-rol "
                    "prinsipidir və inzibatçının hər yeri düzəldə bilməsini "
                    "təmin edir. Skript admini bütün qorunan endpoint-lərdə "
                    "sınayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"

echo "── admin hər qorunan endpointə girir ──"
for yol in /struktur/merkezler /struktur/merkezler/statistika \
           /kadrlar/emekdaslar /kadrlar/emekdaslar/icmal \
           /auth/profil /auth/istifadeciler \
           /ai/statistika /ai/reseptler /ixrac/merkezler.xlsx \
           /tehsil/istirakciler /tehsil/statistika; do
  printf '  %-32s → %s\n' "$yol" "$(curl -s -o /dev/null -w '%{http_code}' "$A$yol" -H "$H")"
done

echo "── Guard-daki super-rol qaydası ──"
grep -n "admin' === \|super\|=== 'admin'" src/auth/guards/roles.guard.ts | sed 's/^/  /'
''',
            ),
            dict(
                no="III.16",
                ad="403 cavabının strukturu",
                giris=(
                    "Bu test icazəsiz cəhdin cavabının nə qədər <em>açıqlayıcı</em> "
                    "olduğunu yoxlayır: kod <code>ICAZE_YOXDUR</code> və mesajda "
                    "hansı rolun lazım olduğu yazılır. Bu, təhlükəsizliyi "
                    "zəiflətmir, əksinə inkişaf etdiricini düzgün yola "
                    "yönəldir. Skript 403-ün tam strukturunu göstərir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"maliyyeci@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── maliyyeci → POST /struktur/merkezler ──"
curl -s -X POST "$A/struktur/merkezler" -H "Authorization: Bearer $T" \
  -H 'Content-Type: application/json' -d '{"ad":"olmayacaq","tip":"merkez"}' | python3 -m json.tool

echo "── maliyyeci → GET /auth/istifadeciler ──"
curl -s "$A/auth/istifadeciler" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  ugur :', d['ugur'])
print('  kod  :', d['xeta']['kod'])
print('  mesaj:', d['xeta']['mesaj'])
"
''',
            ),
            dict(
                no="III.17",
                ad="Qeydiyyat — kim istifadəçi yarada bilər",
                giris=(
                    "Bu test Dərs 3-ün yeddinci addımını yoxlayır: "
                    "<code>POST /auth/qeydiyyat</code> endpointinin rol "
                    "qorumasını. Yeni istifadəçi yaratmaq hüququ yalnız "
                    "<code>admin</code>-də olmalıdır — <code>baxici</code> özünə "
                    "yüksək rol verə bilməməlidir. Skript yaratdığı istifadəçini "
                    "sonda silir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

temizle() {
  psql -U arti_user -d arti_baza -q -c \
    "DELETE FROM kadrlar.istifadeciler WHERE email = 'yoxlama@arti.edu.az'" 2>/dev/null
}
trap temizle EXIT

ADMIN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
BAXICI=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"baxici@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

CISIM='{"email":"yoxlama@arti.edu.az","parol":"yoxlama2026","ad_soyad":"Yoxlama Istifadeci","rol":"baxici"}'

echo "── baxici cəhd edir ──"
printf '  HTTP %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/auth/qeydiyyat" \
  -H "Authorization: Bearer $BAXICI" -H 'Content-Type: application/json' -d "$CISIM")"

echo "── admin cəhd edir ──"
curl -s -X POST "$A/auth/qeydiyyat" -H "Authorization: Bearer $ADMIN" \
  -H 'Content-Type: application/json' -d "$CISIM" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  yaradıldı:', d.get('email'), '| rol:', d.get('rol'), '| id:', d.get('id'))
print('  parol_hash cavabda varmı?', 'BƏLİ ⚠️' if 'parol_hash' in json.dumps(d) else 'xeyr ✓')
"

echo "── Eyni e-poçtla təkrar → 409 ──"
printf '  HTTP %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/auth/qeydiyyat" \
  -H "Authorization: Bearer $ADMIN" -H 'Content-Type: application/json' -d "$CISIM")"

echo "── Yeni istifadəçi giriş edə bilir? ──"
printf '  login → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/auth/login" \
  -H 'Content-Type: application/json' -d '{"email":"yoxlama@arti.edu.az","parol":"yoxlama2026"}')"
''',
            ),
            dict(
                no="III.18",
                ad="AuditInterceptor — yazma +1, oxuma +0",
                giris=(
                    "Bu test Dərs 3-ün doqquzuncu addımını yoxlayır: audit "
                    "jurnalının yalnız <em>yazma</em> əməliyyatlarını yazmasını. "
                    "Hər GET sorğusunu yazsaq jurnal bir gündə milyon sətir "
                    "olar və içindən heç nə tapmaq mümkün olmaz. Skript əvvəl "
                    "və sonra sayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"

say() { psql -U arti_user -d arti_baza -tA -c "SELECT count(*) FROM audit.audit_log" | tr -d ' '; }

echo "── 3 × GET ──"
E=$(say)
for i in 1 2 3; do curl -s -o /dev/null "$A/struktur/merkezler" -H "$H"; done
S=$(say)
echo "  əvvəl: $E   sonra: $S   fərq: $((S - E))   (gözlənilən: 0)"

echo "── 1 × POST + 1 × DELETE ──"
E=$(say)
ID=$(curl -s -X POST "$A/struktur/merkezler" -H "$H" -H 'Content-Type: application/json' \
  -d '{"ad":"Audit testi","tip":"merkez"}' | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")
curl -s -o /dev/null -X DELETE "$A/struktur/merkezler/$ID" -H "$H"
S=$(say)
echo "  əvvəl: $E   sonra: $S   fərq: $((S - E))   (gözlənilən: 2)"

echo "── Son 3 jurnal sətri ──"
psql -U arti_user -d arti_baza -c "
  SELECT cedvel_adi, emeliyyat, setir_id, istifadeci, qeyd
  FROM audit.audit_log ORDER BY id DESC LIMIT 3" | sed 's/^/  /'
''',
            ),
            dict(
                no="III.19",
                ad="⚠️ Uğursuz cəhd də jurnala yazılır",
                giris=(
                    "Bu test auditin ən dəyərli xüsusiyyətini yoxlayır: uğursuz "
                    "cəhdlərin də qeydə alınmasını. Kimsə icazəsiz silməyə "
                    "çalışsa, bu cəhd jurnalda <code>XƏTA</code> qeydi ilə "
                    "qalmalıdır. Yalnız uğurlu əməliyyatları yazsaq, "
                    "təhlükəsizlik pozuntuları görünməz qalardı."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

BAXICI=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"baxici@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── baxici mərkəz silməyə çalışır (403 olacaq) ──"
printf '  HTTP %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$A/struktur/merkezler/1" \
  -H "Authorization: Bearer $BAXICI")"

sleep 1
echo "── Jurnalda bu cəhd görünürmü? ──"
psql -U arti_user -d arti_baza -c "
  SELECT cedvel_adi, emeliyyat, istifadeci, qeyd, vaxt::timestamp(0)
  FROM audit.audit_log
  WHERE istifadeci = 'baxici@arti.edu.az'
  ORDER BY id DESC LIMIT 3" | sed 's/^/  /'

echo "── XƏTA qeydi olan cəhdlərin sayı ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  ' || count(*) || ' uğursuz cəhd jurnala yazılıb'
  FROM audit.audit_log WHERE qeyd LIKE 'XƏTA%'"
''',
            ),
            dict(
                no="III.20",
                ad="Seed skriptinin idempotentliyi",
                giris=(
                    "Bu test Dərs 3-ün on birinci addımını yoxlayır: seed "
                    "skriptinin təkrar işlədilə bilməsini. Skript iki dəfə "
                    "işlədilsə də sistemdə <strong>4</strong> istifadəçi "
                    "qalmalıdır — dublikat yaranmamalıdır. İdempotentlik "
                    "olmasaydı hər işə salmada yeni sətirlər yığılardı."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
export npm_config_cache=/tmp/npmcache

say() {
  echo "  istifadəçi: $(psql -U arti_user -d arti_baza -tA -c 'SELECT count(*) FROM kadrlar.istifadeciler' | tr -d ' ')  |  bcrypt hash-li: $(psql -U arti_user -d arti_baza -tA -c "SELECT count(*) FROM kadrlar.istifadeciler WHERE parol_hash LIKE '\$2%'" | tr -d ' ')"
}

echo "── Əvvəl ──"; say

echo "── 1-ci işə salma ──"
npm run seed:auth 2>&1 | tail -3 | sed 's/^/  /'
say

echo "── 2-ci işə salma (idempotent olmalıdır) ──"
npm run seed:auth 2>&1 | tail -3 | sed 's/^/  /'
say

echo "── Rollar üzrə ──"
psql -U arti_user -d arti_baza -c "
  SELECT rol, count(*) AS sayi FROM kadrlar.istifadeciler GROUP BY rol ORDER BY rol" | sed 's/^/  /'

echo "── Seed skriptində idempotentlik ──"
grep -nE 'upsert|ON CONFLICT|update:|create:' scripts/seed-auth.ts | head -6 | sed 's/^/  /'
''',
            ),
        ],
    ),
]
