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
  if [ "$GEL" = "$GOZ" ]; then
    printf '      [OK] %-44s → %s\n' "$AD" "$GEL"
  else
    printf '      [XX] %-44s → %s (gözlənilirdi %s)\n' "$AD" "$GEL" "$GOZ"; XETA=$((XETA+1))
  fi
}

echo "  → 1) Sağlamlıq yoxlaması (açıq)"
gozle 'GET /auth/yoxlama (açıq)' 200 "$(kod "$AUTH/yoxlama")"
govde "$AUTH/yoxlama" | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("      auth          :", d.get("auth"))
print("      sirr_uzunlugu :", d.get("sirr_uzunlugu"), "(DƏYƏR YOX — yalnız uzunluq)")
print("      muddet        :", d.get("muddet"))
' 2>/dev/null

echo ""
echo "  → 2) Qeydiyyat — uğurlu hal (201)"
gozle 'POST /auth/qeydiyyat (güclü parol)' 201 "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$GOVDE")"
printf '      bazada yeni sətir : %s\n' "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email = '$TE';")"
printf '      rolu              : %s (standart «baxici» olmalıdır)\n' \
  "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE email = '$TE';")"
[ "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE email = '$TE';")" = "baxici" ] \
  || { echo "      ✗ standart rol «baxici» deyil!"; XETA=$((XETA+1)); }

echo ""
echo "  → 3) Qeydiyyat — rədd halları"
gozle 'POST zəif parol (123456)' 400 \
  "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$G_Z1")"
gozle 'POST rol inyeksiyası (rol=admin)' 400 \
  "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$G_Z2")"
gozle 'POST mövcud e-poçt (409 konflikt)' 409 \
  "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$GOVDE")"
gozle 'POST səhv e-poçt formatı' 400 \
  "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$G_SAHVE")"
gozle 'POST boş gövdə' 400 "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d '{}')"
gozle 'POST qısa ad_soyad' 400 \
  "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$G_Z3")"

echo ""
echo "  → 4) Rol inyeksiyası cəhdi BAZAYA düşmədi"
printf '      test.3a.z2 bazada : %s (0 olmalıdır)\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email = 'test.3a.z2.$EPOK@arti.edu.az';")"
printf '      admin rolunda test: %s (0 olmalıdır)\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%' AND rol = 'admin';")"
[ "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%' AND rol <> 'baxici';")" = "0" ] \
  || { echo "      ✗ test istifadəçisi «baxici»-dən başqa rola malikdir!"; XETA=$((XETA+1)); }

echo ""
echo "  → 5) Giriş — 401 və 200"
gozle 'POST giriş səhv parol (401)' 401 \
  "$(kod -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "$G_SEHV_PAROL")"
gozle 'POST giriş mövcud olmayan e-poçt' 401 \
  "$(kod -X POST "$AUTH/giris" -H 'Content-Type: application/json' \
     -d '{"email":"yoxdur.3a@arti.edu.az","parol":"YanlisParol123!"}')"
gozle 'POST giriş düzgün parol (200)' 200 "$(def_giris_kod)"

echo ""
echo "  → 6) Giriş cavabının quruluşu"
CAVAB=$(govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "$GIRIS_GOVDE")
printf '%s' "$CAVAB" | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("      ugur          :", d.get("ugur"))
print("      token_novu    :", d.get("token_novu"))
print("      muddet_saniye :", d.get("muddet_saniye"))
print("      bitme_vaxti   :", d.get("bitme_vaxti"))
t = d.get("access_token", "")
print("      token hissəsi :", len(t.split(".")))
hamisi = json.dumps(d)
print("      parol_hash    :", "VAR — TƏHLÜKƏ!" if "parol_hash" in hamisi else "yoxdur ✓")
' 2>/dev/null

echo ""
echo "  → 7) Səhv parol ilə düzgün parolun cavab QURULUŞU eynidir (enumeration)"
S1=$(govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "{\"email\":\"$TE\",\"parol\":\"Yanlis1!\"}" | python3 -c 'import sys,json;print(json.load(sys.stdin)["xeta"]["kod"])' 2>/dev/null)
S2=$(govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d '{"email":"yoxdur.3a@arti.edu.az","parol":"Yanlis1!"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["xeta"]["kod"])' 2>/dev/null)
printf '      mövcud e-poçt + səhv parol : %s\n' "$S1"
printf '      mövcud olmayan e-poçt      : %s\n' "$S2"
[ "$S1" = "$S2" ] && echo "      ✓ hər ikisi eyni kodu verir — e-poçt siyahısı sızmır" \
  || { echo "      ✗ fərqli kodlar — enumeration mümkündür"; XETA=$((XETA+1)); }

echo ""
[ "$XETA" = "0" ] || { echo "  ✗ $XETA yoxlama uğursuz"; exit 1; }
echo "  ✓ IIIA.6 KEÇDİ — açıq endpoint-lər və validasiya düzgün işləyir"
)
