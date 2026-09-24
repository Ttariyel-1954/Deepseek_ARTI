LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur: $(pwd)"; exit 1; }
[ -f .env ] || { echo "  ✗ .env yoxdur"; exit 1; }
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
[ -n "$DBURL" ] || { echo "  ✗ .env-də DATABASE_URL yoxdur"; exit 1; }
say() { psql "$DBURL" -At -c "$1" 2>/dev/null | tr -d ' '; }

PORT="${PORT:-4000}"
LOQ="/tmp/arti_iiia_${PORT}.log"
API="http://localhost:$PORT/api/v1"
AUTH="$API/auth"

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "  ✗ $PORT portu məşğuldur — əvvəlcə həmin serveri dayandırın"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | awk '{ print "      " $0 }'
  exit 1
fi

npm run build >/tmp/arti_iiia_build.log 2>&1 \
  || { echo "  ✗ build uğursuz"; tail -n 25 /tmp/arti_iiia_build.log | awk '{ print "      " $0 }'; exit 1; }
echo "  ✓ build uğurlu"

PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
temizle() {
  [ -n "$PID" ] && kill "$PID" 2>/dev/null
  [ -n "$PID" ] && wait "$PID" 2>/dev/null
  psql "$DBURL" -At -c "DELETE FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%@arti.edu.az';" >/dev/null 2>&1
  true
}
trap temizle EXIT INT TERM

hazir=0
i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  curl -fsS "$API/saglamliq" -o /dev/null 2>/dev/null && { hazir=1; break; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.5
done
[ "$hazir" = "1" ] || { echo "  ✗ server qalxmadı"; tail -n 25 "$LOQ" | awk '{ print "      " $0 }'; exit 1; }
printf '  ✓ server hazırdır (%s cəhd)\n' "$i"

kod()   { curl -s -o /dev/null -w '%{http_code}' "$@"; }
govde() { curl -s "$@"; }
jsonf() { python3 -c 'import sys,json; d=json.load(sys.stdin); print(eval("d"+sys.argv[1]))' "$1"; }

EPOK=$(date +%s)
TE="test.3a.${EPOK}@arti.edu.az"
PAROL='GucluParol123!'
GOVDE="{\"email\":\"$TE\",\"parol\":\"$PAROL\",\"ad_soyad\":\"Test Istifadeci\"}"
# ⚠️ Giriş DTO-su YALNIZ email + parol qəbul edir! `ad_soyad` göndərsək
#    `forbidNonWhitelisted` onu 400 ilə rədd edər.
GIRIS_GOVDE="{\"email\":\"$TE\",\"parol\":\"$PAROL\"}"
def_giris_kod() { kod -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "$GIRIS_GOVDE"; }
def_giris_token() { govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "$GIRIS_GOVDE" | jsonf "['access_token']"; }

# ⚠️⚠️ NİYƏ AYRICA DƏYİŞƏNLƏR? — bash 3.2-nin ÇOX MƏKRİ XƏTASI!
#
#   gozle '...' 400 "$(kod ... -d "{\"email\":\"$TE\"}")"
#                    └──────────── İÇ-İÇƏ dırnaqlar ────────────┘
#
# macOS-un bash 3.2-si bu formada gövdəni SƏHV parse edir: `\"` ilə
# qorunan dırnaqlar itir və `{...}` qalin mötərizə genişlənməsinə
# (brace expansion) düşür — nəticədə serverə YARIMÇIQ JSON gedir və
# gözlənilməz 400 qayıdır. Gövdəni DƏYİŞƏNDƏ saxlasaq, problem yox olur.
G_Z1="{\"email\":\"test.3a.z1.$EPOK@arti.edu.az\",\"parol\":\"123456\",\"ad_soyad\":\"Test Ad\"}"
G_Z2="{\"email\":\"test.3a.z2.$EPOK@arti.edu.az\",\"parol\":\"$PAROL\",\"ad_soyad\":\"Test Ad\",\"rol\":\"admin\"}"
G_Z3="{\"email\":\"test.3a.z3.$EPOK@arti.edu.az\",\"parol\":\"$PAROL\",\"ad_soyad\":\"A\"}"
G_SAHVE="{\"email\":\"bu-e-poct-deyil\",\"parol\":\"$PAROL\",\"ad_soyad\":\"Test Ad\"}"
G_SEHV_PAROL="{\"email\":\"$TE\",\"parol\":\"YanlisParol123!\"}"

XETA=0
gozle() {
  AD="$1"; GOZ="$2"; GEL="$3"
  if [ "$GEL" = "$GOZ" ]; then printf '      [OK] %-46s → %s\n' "$AD" "$GEL"
  else printf '      [XX] %-46s → %s (gözlənilirdi %s)\n' "$AD" "$GEL" "$GOZ"; XETA=$((XETA+1)); fi
}

kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$GOVDE" >/dev/null
TOKEN=$(def_giris_token)
[ -n "$TOKEN" ] || { echo "  ✗ token alınmadı"; exit 1; }
printf '  token alındı: %s simvol, %s hissə\n\n' "${#TOKEN}" "$(printf '%s' "$TOKEN" | awk -F. '{print NF}')"

echo "  → 1) Token OLMADAN qorunan endpoint-lər → 401"
for yol in me admin-yoxlama muhendis-yoxlama istifadeciler; do
  gozle "GET /$yol (token yox)" 401 "$(kod "$AUTH/$yol")"
done
gozle 'PATCH rol (token yox)' 401 "$(kod -X PATCH "$AUTH/istifadeci/1/rol" -H 'Content-Type: application/json' -d '{"rol":"admin"}')"

echo ""
echo "  → 2) Səhv token başlığı → 401"
gozle 'Authorization: Bearer bu-token-deyil' 401 "$(kod -H 'Authorization: Bearer bu-token-deyil' "$AUTH/me")"
gozle 'Authorization: Bearer (boş)' 401 "$(kod -H 'Authorization: Bearer ' "$AUTH/me")"
gozle 'Authorization: Basic dXNlcjpwYXNz' 401 "$(kod -H 'Authorization: Basic dXNlcjpwYXNz' "$AUTH/me")"
gozle 'Authorization olmadan (başqa başlıq)' 401 "$(kod -H 'X-Test: 1' "$AUTH/me")"
gozle 'Bearer sözü olmadan' 401 "$(kod -H "Authorization: $TOKEN" "$AUTH/me")"

echo ""
echo "  → 3) Düzgün token → 200"
gozle 'GET /me (düzgün token)' 200 "$(kod -H "Authorization: Bearer $TOKEN" "$AUTH/me")"
govde -H "Authorization: Bearer $TOKEN" "$AUTH/me" | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("      sub           :", d.get("sub"))
print("      email         :", d.get("email"))
print("      rol           :", d.get("rol"))
print("      token_verildi :", d.get("token_verildi"))
print("      token_bitir   :", d.get("token_bitir"))
' 2>/dev/null
gozle 'GET /muhendis-yoxlama (baxici → 403)' 403 "$(kod -H "Authorization: Bearer $TOKEN" "$AUTH/muhendis-yoxlama")"

echo ""
echo "  → 4) 401 və 403 cavablarının KODLARI fərqlidir"
K401=$(govde "$AUTH/me" | python3 -c 'import sys,json;print(json.load(sys.stdin)["xeta"]["kod"])' 2>/dev/null)
K403=$(govde -H "Authorization: Bearer $TOKEN" "$AUTH/admin-yoxlama" | python3 -c 'import sys,json;print(json.load(sys.stdin)["xeta"]["kod"])' 2>/dev/null)
printf '      401 kodu : %s\n' "$K401"
printf '      403 kodu : %s\n' "$K403"
[ "$K401" != "$K403" ] && echo "      ✓ frontend 401 və 403-ü AYIRD EDƏ BİLİR" \
  || { echo "      ✗ kodlar eynidir — frontend ayırd edə bilməz"; XETA=$((XETA+1)); }

echo ""
echo "  → 5) SAXTALAŞDIRMA: payload dəyişdirilir, imza saxlanılır"
cat > /tmp/iiia7_saxta.py <<'PYSUB7'
import base64, json, sys
h, p, s = sys.argv[1].split('.')
def ac(x): return json.loads(base64.urlsafe_b64decode(x + '=' * (-len(x) % 4)))
def bag(d): return base64.urlsafe_b64encode(json.dumps(d, separators=(',', ':')).encode()).rstrip(b'=').decode()
yuk = ac(p)
print('      orijinal rol :', yuk.get('rol'), file=sys.stderr)
yuk['rol'] = 'admin'
print('%s.%s.%s' % (h, bag(yuk), s))
PYSUB7
SAXTA=$(python3 /tmp/iiia7_saxta.py "$TOKEN" 2>/dev/null)
printf '      saxta token uzunluğu : %s (orijinal %s)\n' "${#SAXTA}" "${#TOKEN}"
[ "${#SAXTA}" -gt 0 ] || { echo "  ✗ saxta token yaradıla bilmədi"; exit 1; }
gozle 'saxta token (rol=admin) → 401' 401 "$(kod -H "Authorization: Bearer $SAXTA" "$AUTH/admin-yoxlama")"
gozle 'saxta token /me → 401' 401 "$(kod -H "Authorization: Bearer $SAXTA" "$AUTH/me")"
rm -f /tmp/iiia7_saxta.py

echo ""
echo "  → 6) İmzasız / pozulmuş tokenlər"
H=$(printf '%s' "$TOKEN" | cut -d. -f1)
P=$(printf '%s' "$TOKEN" | cut -d. -f2)
gozle 'yalnız 2 hissə' 401 "$(kod -H "Authorization: Bearer $H.$P" "$AUTH/me")"
gozle '4 hissə' 401 "$(kod -H "Authorization: Bearer $TOKEN.artiq" "$AUTH/me")"
gozle 'imza tamamilə dəyişdirilib' 401 \
  "$(kod -H "Authorization: Bearer $H.$P.${H}${P}" "$AUTH/me")"

echo ""
[ "$XETA" = "0" ] || { echo "  ✗ $XETA yoxlama uğursuz"; exit 1; }
echo "  ✓ IIIA.7 KEÇDİ — token qoruması və saxtalaşdırma müdafiəsi işləyir"
)
