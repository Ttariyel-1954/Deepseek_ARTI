LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur — bu qovluq layihə deyil: $(pwd)"; exit 1; }

[ -f skriptler/servis_yoxla.sh ] || { echo "  ✗ skriptler/servis_yoxla.sh yoxdur — ADDIM 13-ü işlədin"; exit 1; }
echo "  ✓ servis_yoxla.sh yerindədir"

PORT="${PORT:-4000}"
echo "  → İstifadə olunan port: $PORT"

echo ""
echo "  → 1) Portun BOŞ olduğunu yoxlayırıq"
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "      ✗ $PORT portu artıq məşğuldur — test başlaya bilməz"
  exit 1
fi
echo "      ✓ boşdur"

echo ""
echo "  → 2) Portu SÜNİ olaraq tuturuq (python http.server)"
python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
TUTAN=$!
temizle() {
  kill "$TUTAN" 2>/dev/null
  wait "$TUTAN" 2>/dev/null
  true
}
trap temizle EXIT INT TERM
sleep 1.5

if ! lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "      ✗ süni tutucu qalxa bilmədi"
  exit 1
fi
echo "      ✓ port indi məşğuldur:"
lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | sed 's/^/          /'

echo ""
echo "  → 3) servis_yoxla.sh MƏŞĞUL portla — rədd etməlidir"
CIXIS=$(PORT="$PORT" bash skriptler/servis_yoxla.sh 2>&1)
KOD=$?
printf '%s\n' "$CIXIS" | sed 's/^/      /'
printf '      exit kodu: %s\n' "$KOD"

[ "$KOD" -eq 1 ] || { echo "  ✗ skript məşğul portu TANIMADI (exit 0 verdi)"; exit 1; }
echo "      ✓ exit 1 qaytardı"

printf '%s' "$CIXIS" | grep -q 'MƏŞĞUL' || { echo "  ✗ xəbərdarlıq mətni yoxdur"; exit 1; }
echo "      ✓ problemi aydın Azərbaycanca bildirdi"

printf '%s' "$CIXIS" | grep -q "$TUTAN" || { echo "  ✗ tutan prosesin PID-i göstərilmədi"; exit 1; }
echo "      ✓ tutan prosesin PID-ini ($TUTAN) göstərdi"

printf '%s' "$CIXIS" | grep -q 'Server hazırdır' && { echo "  ✗ skript serveri qaldırmağa cəhd ETDİ!"; exit 1; }
echo "      ✓ serveri qaldırmağa cəhd belə etmədi"

echo ""
echo "  → 4) Süni tutucunu dayandırırıq"
kill "$TUTAN" 2>/dev/null
wait "$TUTAN" 2>/dev/null
sleep 1.5
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "      ✗ port hələ məşğuldur"; exit 1
fi
echo "      ✓ port boşdur"

echo ""
echo "  → 5) servis_yoxla.sh BOŞ portla — işləməlidir"
PORT="$PORT" bash skriptler/servis_yoxla.sh
KOD=$?
printf '      exit kodu: %s\n' "$KOD"
[ "$KOD" -eq 0 ] || { echo "  ✗ skript boş portda uğursuz oldu"; exit 1; }
echo "      ✓ exit 0 qaytardı"

echo ""
echo "  → 6) Skript bitdikdən sonra port BOŞ qalmalıdır (trap təmizliyi)"
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "      ✗ port məşğul qaldı — trap təmizliyi işləmədi"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | sed 's/^/          /'
  exit 1
fi
echo "      ✓ port boşdur — arxada asılı proses qalmadı"

echo ""
echo "  ✓ IB.7 KEÇDİ — port idarəsi və təmizlik zəmanətlidir"
)
