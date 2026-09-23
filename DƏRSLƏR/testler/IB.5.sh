LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur — bu qovluq layihə deyil: $(pwd)"; exit 1; }

PORT="${PORT:-4000}"
LOQ="/tmp/arti_ib5_${PORT}.log"

echo "  → Port: $PORT"

[ -f dist/main.js ] || { echo "  ✗ dist/main.js yoxdur — əvvəlcə build edin (IB.1)"; exit 1; }
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "  ✗ $PORT portu məşğuldur"; exit 1
fi

PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
temizle() { kill "$PID" 2>/dev/null; wait "$PID" 2>/dev/null; true; }
trap temizle EXIT INT TERM

hazir=0
i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  curl -fsS "http://localhost:$PORT/api/v1" -o /dev/null 2>/dev/null && { hazir=1; break; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.5
done
[ "$hazir" = "1" ] || { echo "  ✗ server cavab vermədi"; tail -n 20 "$LOQ" | sed 's/^/      /'; exit 1; }
printf '  ✓ server hazırdır (%s cəhddən sonra)\n' "$i"

kod() { curl -s -o /dev/null -w '%{http_code}' "http://localhost:$PORT$1"; }

echo ""
echo "  → Yolların status kodları"
XETA=0
yoxla() {
  N=$(kod "$1")
  if [ "$N" = "$2" ]; then
    printf '      ✓ %-24s → %s\n' "$1" "$N"
  else
    printf '      ✗ %-24s → %s  (gözlənilirdi: %s)\n' "$1" "$N" "$2"
    XETA=1
  fi
}
yoxla "/api/v1"                 200
yoxla "/api/v1/saglamliq"       200
yoxla "/docs"                   200
yoxla "/saglamliq"              404
yoxla "/"                       404
yoxla "/api/saglamliq"          404
yoxla "/api/v2/saglamliq"       404

echo ""
[ "$XETA" -eq 0 ] || { echo "  ✗ bəzi yollar gözlənilən statusu qaytarmadı"; exit 1; }

echo "  → Kök endpoint-in cavabı:"
curl -s "http://localhost:$PORT/api/v1" | sed 's/^/      /'
echo ""
printf '%s' "$(curl -s "http://localhost:$PORT/api/v1")" | grep -q '/api/v1' \
  || { echo "  ✗ /api/v1 cavabında prefiks məlumatı yoxdur"; exit 1; }
echo "      ✓ cavabda prefiks məlumatı var"

echo ""
echo "  ✓ IB.5 KEÇDİ — prefiks işləyir, prefikssiz yollar 404 qaytarır"
)
