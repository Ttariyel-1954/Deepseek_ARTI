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

EVVEL=$(say "SELECT count(*) FROM kadrlar.istifadeciler;")
echo "  → 0) Başlanğıc: $EVVEL istifadəçi"

T_ADMIN=$(govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' | jsonf "['access_token']" 2>/dev/null)
[ -n "$T_ADMIN" ] || { echo "  ✗ admin tokeni alınmadı"; exit 1; }

kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$GOVDE" >/dev/null
ID=$(say "SELECT id FROM kadrlar.istifadeciler WHERE email = '$TE';")
[ -n "$ID" ] || { echo "  ✗ test istifadəçisi yaradılmadı"; exit 1; }
printf '      test istifadəçisi : id=%s, %s\n' "$ID" "$TE"
TOKEN_BAXICI=$(def_giris_token)
printf '      köhnə token alındı : %s simvol (rol=baxici)\n' "${#TOKEN_BAXICI}"

echo ""
echo "  → 1) İstifadəçi siyahısı (admin)"
gozle 'GET /auth/istifadeciler' 200 "$(kod -H "Authorization: Bearer $T_ADMIN" "$AUTH/istifadeciler")"
printf '      siyahıda test ist.: %s\n' \
  "$(govde -H "Authorization: Bearer $T_ADMIN" "$AUTH/istifadeciler" | grep -c "$TE")"

echo ""
echo "  → 2) Rol dəyişmə: baxici → muhendis"
gozle "PATCH /istifadeci/$ID/rol (baxici→muhendis)" 200 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/rol" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"rol":"muhendis"}')"
printf '      bazada yeni rol    : %s\n' "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE id = $ID;")"
[ "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE id = $ID;")" = "muhendis" ] \
  || { echo "      ✗ rol bazada dəyişmədi"; XETA=$((XETA+1)); }

echo ""
echo "  → 3) YENİ ROL DƏRHAL İŞLƏYİR (yeni token ilə)"
T_YENI=$(def_giris_token)
gozle 'YENİ token /muhendis-yoxlama' 200 "$(kod -H "Authorization: Bearer $T_YENI" "$AUTH/muhendis-yoxlama")"
gozle 'YENİ token /admin-yoxlama → 403' 403 "$(kod -H "Authorization: Bearer $T_YENI" "$AUTH/admin-yoxlama")"
printf '      ⚠️ KÖHNƏ token hələ də «baxici» deyir — JWT LƏĞV EDİLƏ BİLMİR:\n'
gozle 'KÖHNƏ token /muhendis-yoxlama → 403' 403 \
  "$(kod -H "Authorization: Bearer $TOKEN_BAXICI" "$AUTH/muhendis-yoxlama")"
gozle 'KÖHNƏ token /me → 200 (hələ etibarlıdır!)' 200 \
  "$(kod -H "Authorization: Bearer $TOKEN_BAXICI" "$AUTH/me")"

echo ""
echo "  → 4) Yanlış rol adı və id rədd edilir"
gozle 'PATCH rol=superadmin' 400 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/rol" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"rol":"superadmin"}')"
gozle 'PATCH rol boş gövdə' 400 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/rol" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{}')"
gozle 'PATCH mövcud olmayan id → 404 (500 YOX)' 404 \
  "$(kod -X PATCH "$AUTH/istifadeci/999999/rol" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"rol":"baxici"}')"

echo ""
echo "  → 5) Deaktiv etmə: aktiv=false → giriş 401"
gozle "PATCH /istifadeci/$ID/aktivlik (false)" 200 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/aktivlik" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"aktiv":false}')"
printf '      bazada aktiv       : %s\n' "$(say "SELECT aktiv FROM kadrlar.istifadeciler WHERE id = $ID;")"
gozle 'deaktiv hesabla giriş → 403' 403 "$(def_giris_kod)"
gozle 'səhv tip (aktiv="beli") → 400' 400 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/aktivlik" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"aktiv":"beli"}')"

echo ""
echo "  → 6) Yenidən aktiv etmə"
gozle "PATCH /istifadeci/$ID/aktivlik (true)" 200 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/aktivlik" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"aktiv":true}')"
gozle 'yenidən giriş → 200' 200 "$(def_giris_kod)"

echo ""
echo "  → 7) Qeyri-admin rol dəyişə BİLMƏZ"
T_MUH=$(govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' \
  -d '{"email":"muhendis@arti.edu.az","parol":"123456"}' | jsonf "['access_token']")
gozle 'muhendis PATCH rol → 403' 403 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/rol" -H "Authorization: Bearer $T_MUH" \
     -H 'Content-Type: application/json' -d '{"rol":"admin"}')"
printf '      rol dəyişməyib    : %s (muhendis olmalıdır)\n' \
  "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE id = $ID;")"
[ "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE id = $ID;")" = "muhendis" ] \
  || { echo "      ✗ İCAZƏSİZ DƏYİŞİKLİK BAŞ VERDİ!"; XETA=$((XETA+1)); }

echo ""
echo "  → 8) Təmizlik"
psql "$DBURL" -At -c "DELETE FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%@arti.edu.az';" >/dev/null 2>&1
SONRA=$(say "SELECT count(*) FROM kadrlar.istifadeciler;")
printf '      istifadəçi sayı : %s → %s\n' "$EVVEL" "$SONRA"
[ "$SONRA" = "$EVVEL" ] || { echo "      ✗ test iz qoydu!"; XETA=$((XETA+1)); }
printf '      qalan test ist. : %s (0 olmalıdır)\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%';")"
printf '      real istifadəçi : %s (4 olmalıdır)\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE '%@arti.edu.az' AND email NOT LIKE 'test.3a.%';")"

echo ""
[ "$XETA" = "0" ] || { echo "  ✗ $XETA yoxlama uğursuz"; exit 1; }
echo "  ✓ IIIA.9 KEÇDİ — admin idarəsi işləyir və test iz qoymur"
)
