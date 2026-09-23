LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── 1) Olmayan endpoint → 404 ──"
curl -s "$A/bele-bir-yol-yoxdur" | python3 -m json.tool

echo "── 2) Cavabın 4 sahəsi ──"
curl -s "$A/bele-bir-yol-yoxdur" | python3 -c "
import json,sys
d = json.load(sys.stdin)
for a in ('ugur','xeta','yol','vaxt'):
    print('  %-6s → %s' % (a, 'var' if a in d else 'YOXDUR'))
print('  xeta.kod  →', d['xeta']['kod'])
print('  xeta.mesaj→', d['xeta']['mesaj'])
"

echo "── 3) Status kodlarının oxunaqlı xəritəsi ──"
grep -E "^  [0-9]{3}:" src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'
)
