LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache
A="${A:-http://localhost:4000/api/v1}"
PORT="${PORT:-4000}"

echo "── Build ──"
npm run build 2>&1 | tail -2 | sed 's/^/  /'
[ -f dist/main.js ] || { echo "  ✗ dist/main.js yoxdur"; exit 1; }

echo
echo "── Köhnə proses təmizlənir ──"
lsof -ti:$PORT 2>/dev/null | xargs -r kill 2>/dev/null
sleep 1

echo "── Server qalxır (port $PORT) ──"
PORT=$PORT nohup npm run start:prod > /tmp/ders1a_ia10.log 2>&1 &
for i in $(seq 1 30); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)" = "200" ] && break
  sleep 1
done

echo "  Marşrutlar:"
grep 'Mapped' /tmp/ders1a_ia10.log | sed 's/.*Mapped //' | sed 's/^/    /'

echo
echo "── 1) Kök ünvan ──"
curl -s "$A" | python3 -m json.tool | sed 's/^/  /'

echo
echo "── 2) Sağlamlıq ──"
curl -s "$A/saglamliq" | python3 -m json.tool | sed 's/^/  /'

echo
echo "── 3) Olmayan yol → vahid xəta formatı ──"
curl -s "$A/bele-yol-yoxdur" | python3 -m json.tool | sed 's/^/  /'

echo
echo "── 4) Swagger ──"
kok="${A%/api/v1}"
echo "  $kok/docs      → HTTP $(curl -s -o /dev/null -w '%{http_code}' "$kok/docs")"
echo "  $kok/docs-json → HTTP $(curl -s -o /dev/null -w '%{http_code}' "$kok/docs-json")"

echo
echo "── Server dayandırılır ──"
lsof -ti:$PORT 2>/dev/null | xargs -r kill 2>/dev/null
echo "  ✓ dayandırıldı"
)
