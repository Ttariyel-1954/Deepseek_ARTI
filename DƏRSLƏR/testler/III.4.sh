LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
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
)
