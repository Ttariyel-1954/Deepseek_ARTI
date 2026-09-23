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
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "$TOKEN" | python3 -c "
import base64, json, sys, datetime
def ac(h):
    h += '=' * (-len(h) % 4); return json.loads(base64.urlsafe_b64decode(h))
y = ac(sys.stdin.read().strip().split('.')[1])
muddet = y['exp'] - y['iat']
print('  iat (verilib)  :', datetime.datetime.fromtimestamp(y['iat']))
print('  exp (bitir)    :', datetime.datetime.fromtimestamp(y['exp']))
print('  müddət         :', muddet, 'saniyə =', muddet/3600, 'saat')
print('  .env-dəki sətir:', open('.env').read().strip().splitlines()[-0] and [l for l in open('.env') if l.startswith('JWT_MUDDET')][0].strip())
"
)
