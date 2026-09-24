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
LOQ="/tmp/arti_iib_${PORT}.log"
API="http://localhost:$PORT/api/v1"
EM="$API/emekdaslar"

npm run build >/tmp/arti_iib_build.log 2>&1 \
  || { echo "  ✗ build uğursuz"; tail -n 20 /tmp/arti_iib_build.log | sed 's/^/      /'; exit 1; }

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "  ✗ $PORT portu məşğuldur"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | sed 's/^/      /'
  exit 1
fi

PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
temizle() {
  [ -n "$PID" ] && kill "$PID" 2>/dev/null
  [ -n "$PID" ] && wait "$PID" 2>/dev/null
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
[ "$hazir" = "1" ] || { echo "  ✗ server qalxmadı"; tail -n 20 "$LOQ" | sed 's/^/      /'; exit 1; }
printf '  ✓ server hazırdır (%s cəhd)\n' "$i"

kod()  { curl -s -o /dev/null -w '%{http_code}' "$@"; }
govde(){ curl -s "$@"; }

EPOX=$(date +%s)
P="iib7.${EPOX}"
IDLER=""
temizle2() {
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iib7.%@arti.edu.az';" >/dev/null
  temizle
}
trap temizle2 EXIT INT TERM

echo ""
echo "  → 1) Üç test əməkdaşı yaradılır"
KOD=$(curl -s -o /tmp/iib7.json -w '%{http_code}' -X POST "$EM/toplu/yarat" \
  -H 'Content-Type: application/json' \
  -d "{\"emekdaslar\":[
    {\"ad\":\"Faiz1\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.1@arti.edu.az\",\"maas\":1000},
    {\"ad\":\"Faiz2\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.2@arti.edu.az\",\"maas\":2000},
    {\"ad\":\"Faiz3\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.3@arti.edu.az\",\"maas\":3000}]}")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "201" ] || { echo "  ✗ 201 gözlənilirdi"; exit 1; }
IDLER=$(python3 -c "import json;print(','.join(json.load(open('/tmp/iib7.json'))['idler']))")
printf '      ID-lər: %s\n' "$IDLER"

oxu() {
  say "SELECT string_agg(maas::text, ',' ORDER BY id) FROM kadrlar.emekdaslar WHERE id IN ($IDLER);"
}

EVVEL=$(oxu)
printf '      başlanğıc maaşlar: %s\n' "$EVVEL"
[ "$EVVEL" = "1000.00,2000.00,3000.00" ] || { echo "  ✗ başlanğıc maaşlar gözlənilən deyil: $EVVEL"; exit 1; }

echo ""
echo "  → 2) +10% tətbiq edilir"
KOD=$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":10,\"idler\":[$IDLER]}")
printf '      status: %s\n' "$KOD"
ARTMIS=$(oxu)
printf '      +10%% sonra: %s\n' "$ARTMIS"
[ "$ARTMIS" = "1100.00,2200.00,3300.00" ] || { echo "  ✗ 10% artım səhvdir: $ARTMIS"; exit 1; }
echo "      ✓ hər maaş dəqiq 10% artdı"

echo ""
echo "  → 3) −10% tətbiq edilir (FAİZ TƏLƏSİ)"
KOD=$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":-10,\"idler\":[$IDLER]}")
printf '      status: %s\n' "$KOD"
TELEDEN=$(oxu)
printf '      −10%% sonra: %s\n' "$TELEDEN"
printf '      başlanğıc : %s\n' "$EVVEL"
[ "$TELEDEN" != "$EVVEL" ] || { echo "  ✗ gözlənilməz: dəyərlər bərpa olundu — riyaziyyat səhvdir!"; exit 1; }
[ "$TELEDEN" = "990.00,1980.00,2970.00" ] || { echo "  ✗ gözlənilən 990/1980/2970, alındı: $TELEDEN"; exit 1; }
echo "      ✓ SÜBUT: +10% sonra −10% əvvəlki dəyəri QAYTARMADI"
echo "        riyazi izah: 3000 × 1.1 = 3300,  3300 × 0.9 = 2970 ≠ 3000"
python3 -c "
print('        itki: 1000→990 (10), 2000→1980 (20), 3000→2970 (30) = cəmi 60 AZN')
"

echo ""
echo "  → 4) İtki KÜMÜLATİVDİR — düzəliş onu geri qaytarmır"
KOD=$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":10,\"idler\":[$IDLER]}")
GERI_ARTMIS=$(oxu)
printf '      itkidən sonra +10%%: %s\n' "$GERI_ARTMIS"
[ "$GERI_ARTMIS" = "1089.00,2178.00,3267.00" ] || { echo "  ✗ gözlənilən 1089/2178/3267, alındı: $GERI_ARTMIS"; exit 1; }
echo "      ✓ düzəliş itkini geri qaytarmır — 1089 ≠ 1100"

say "UPDATE kadrlar.emekdaslar SET maas = maas / 1.1 WHERE id IN ($IDLER);" >/dev/null
GERI_SAKIT=$(oxu)
printf '      ÷1.1 ilə sakitləşdirdik: %s\n' "$GERI_SAKIT"
[ "$GERI_SAKIT" = "990.00,1980.00,2970.00" ] || { echo "  ✗ gözlənilən 990/1980/2970, alındı: $GERI_SAKIT"; exit 1; }
echo "      ✓ ÷1.1 ×1.1-i DƏQİQ geri qaytarır (amma itki artıq olub)"

echo ""
echo "  → 4b) TƏMİZ SÜBUT: ×1.1 sonra ÷1.1 → dəqiq bərpa"
ID3=$(say "SELECT id FROM kadrlar.emekdaslar WHERE email='$P.3@arti.edu.az';")
say "UPDATE kadrlar.emekdaslar SET maas = 3000 WHERE id = $ID3;" >/dev/null
ONCE=$(say "SELECT maas FROM kadrlar.emekdaslar WHERE id = $ID3;")
kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":10,\"idler\":[$ID3]}" >/dev/null
ORTADA=$(say "SELECT maas FROM kadrlar.emekdaslar WHERE id = $ID3;")
say "UPDATE kadrlar.emekdaslar SET maas = maas / 1.1 WHERE id = $ID3;" >/dev/null
SON=$(say "SELECT maas FROM kadrlar.emekdaslar WHERE id = $ID3;")
printf '      %s --(x1.1)--> %s --(/1.1)--> %s\n' "$ONCE" "$ORTADA" "$SON"
[ "$ONCE" = "$SON" ] || { echo "  ✗ bölmə dəqiq bərpa etmədi!"; exit 1; }
echo "      ✓ bölmə DƏQİQ tərs əməliyyatdır; faiz isə YOX"

echo ""
echo "  → 5) Sıfırlama riski — faiz = -100 qadağandır"
ONCE5=$(oxu)
printf '      cəhddən ƏVVƏL: %s\n' "$ONCE5"
KOD=$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":-100,\"idler\":[$IDLER]}")
printf '      faiz=-100 → %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi — sıfırlama riski!"; exit 1; }
SON5=$(oxu)
printf '      cəhddən SONRA: %s\n' "$SON5"
[ "$ONCE5" = "$SON5" ] || { echo "  ✗ maaşlar dəyişdi: $ONCE5 → $SON5"; exit 1; }
echo "      ✓ -100 rədd edildi, maaşlar TOXUNULMAZ qaldı (əmsal 0 olardı)"
python3 -c "
print('        izah: 1 + (-100/100) = 0  →  bütün maaşlar 0.00 olardı')
"

echo ""
echo "  → 6) Təmizlik"
say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE '$P.%';" >/dev/null
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      bazada əməkdaş: %s\n' "$TOTAL"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }

echo ""
echo "  ✓ IIB.7 KEÇDİ — faiz tələsi sübut olundu, düzgün bərpa yolu göstərildi"
)
