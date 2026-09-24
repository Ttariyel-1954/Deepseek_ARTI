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
  if [ "$GEL" = "$GOZ" ]; then printf '      [OK] %-48s → %s\n' "$AD" "$GEL"
  else printf '      [XX] %-48s → %s (gözlənilirdi %s)\n' "$AD" "$GEL" "$GOZ"; XETA=$((XETA+1)); fi
}

SEED='123456'
tok_al() {
  govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$1\",\"parol\":\"$SEED\"}" | jsonf "['access_token']" 2>/dev/null
}
rol_al() {
  govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$1\",\"parol\":\"$SEED\"}" | jsonf "['istifadeci']['rol']" 2>/dev/null
}

echo "  → 1) Dörd real istifadəçi ilə giriş"
for e in admin@arti.edu.az muhendis@arti.edu.az maliyyeci@arti.edu.az baxici@arti.edu.az; do
  K=$(kod -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "{\"email\":\"$e\",\"parol\":\"$SEED\"}")
  R=$(rol_al "$e")
  printf '      [%s] %-30s rol=%-10s (gözlənilən: %s)\n' \
    "$([ "$K" = "200" ] && echo OK || echo XX)" "$e" "$R" "${e%%@*}"
  [ "$K" = "200" ] || XETA=$((XETA+1))
  [ "$R" = "${e%%@*}" ] || { echo "      ✗ rol uyğun deyil!"; XETA=$((XETA+1)); }
done

echo ""
echo "  → 2) Rol matrisi (admin/muhendis/maliyyeci/baxici)"
T_ADMIN=$(tok_al admin@arti.edu.az)
T_MUH=$(tok_al muhendis@arti.edu.az)
T_MAL=$(tok_al maliyyeci@arti.edu.az)
T_BAX=$(tok_al baxici@arti.edu.az)
for t in "$T_ADMIN" "$T_MUH" "$T_MAL" "$T_BAX"; do
  [ -n "$t" ] || { echo "  ✗ token alınmadı"; exit 1; }
done

printf '      %-12s %-22s %-22s\n' 'İSTİFADƏÇİ' '/admin-yoxlama' '/muhendis-yoxlama'
for c in "admin:$T_ADMIN:200:200" "muhendis:$T_MUH:403:200" \
         "maliyyeci:$T_MAL:403:403" "baxici:$T_BAX:403:403"; do
  AD=${c%%:*}; REST=${c#*:}; T=${REST%%:*}; REST=${REST#*:}
  G1=${REST%%:*}; G2=${REST##*:}
  K1=$(kod -H "Authorization: Bearer $T" "$AUTH/admin-yoxlama")
  K2=$(kod -H "Authorization: Bearer $T" "$AUTH/muhendis-yoxlama")
  printf '      %-12s %-22s %-22s\n' "$AD" "$K1 (gözlənilir $G1)" "$K2 (gözlənilir $G2)"
  [ "$K1" = "$G1" ] || { echo "      ✗ $AD admin-yoxlama"; XETA=$((XETA+1)); }
  [ "$K2" = "$G2" ] || { echo "      ✗ $AD muhendis-yoxlama"; XETA=$((XETA+1)); }
done

echo ""
echo "  → 3) 403 gəlməlidir, 401 YOX (tanınan istifadəçi üçün)"
K=$(kod -H "Authorization: Bearer $T_BAX" "$AUTH/admin-yoxlama")
printf '      baxici /admin-yoxlama : %s\n' "$K"
[ "$K" = "403" ] && echo "      ✓ 403 — istifadəçi TANINIR, sadəcə icazəsi yoxdur" \
  || { echo "      ✗ 401 gəldi — istifadəçi «tanınmır» kimi cavab aldı"; XETA=$((XETA+1)); }

echo ""
echo "  → 4) İstifadəçi siyahısı yalnız admin üçündür"
gozle 'admin  /istifadeciler' 200 "$(kod -H "Authorization: Bearer $T_ADMIN" "$AUTH/istifadeciler")"
gozle 'muhendis /istifadeciler → 403' 403 "$(kod -H "Authorization: Bearer $T_MUH" "$AUTH/istifadeciler")"
gozle 'maliyyeci /istifadeciler → 403' 403 "$(kod -H "Authorization: Bearer $T_MAL" "$AUTH/istifadeciler")"
gozle 'baxici /istifadeciler → 403' 403 "$(kod -H "Authorization: Bearer $T_BAX" "$AUTH/istifadeciler")"

echo ""
echo "  → 5) Siyahıda parol_hash YOXDUR"
SIYAHI=$(govde -H "Authorization: Bearer $T_ADMIN" "$AUTH/istifadeciler")
printf '%s' "$SIYAHI" | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("      istifadəçi sayı :", len(d) if isinstance(d, list) else "?")
print("      parol_hash      :", "VAR — TƏHLÜKƏ!" if "parol_hash" in json.dumps(d) else "yoxdur ✓")
if isinstance(d, list) and d:
    print("      sahələr         :", ", ".join(sorted(d[0].keys())))
' 2>/dev/null
printf '%s' "$SIYAHI" | grep -q 'parol_hash' && { echo "      ✗ parol_hash SIZDI!"; XETA=$((XETA+1)); }

echo ""
echo "  → 6) Dörd real istifadəçi toxunulmazdır"
printf '      real istifadəçi sayı : %s\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE '%@arti.edu.az' AND email NOT LIKE 'test.3a.%';")"
printf '      hamısı aktiv         : %s\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE '%@arti.edu.az' AND email NOT LIKE 'test.3a.%' AND aktiv;")"
printf '      rollar               : %s\n' \
  "$(psql "$DBURL" -At -F'=' -c "SELECT rol, count(*) FROM kadrlar.istifadeciler WHERE email NOT LIKE 'test.3a.%' GROUP BY rol ORDER BY rol;" 2>/dev/null | tr '\n' ' ')"

echo ""
[ "$XETA" = "0" ] || { echo "  ✗ $XETA yoxlama uğursuz"; exit 1; }
echo "  ✓ IIIA.8 KEÇDİ — RBAC düzgün işləyir, 401 və 403 ayrılır"
)
