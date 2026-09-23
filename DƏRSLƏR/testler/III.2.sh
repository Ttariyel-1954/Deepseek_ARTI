LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

yoxla() {
  printf '  %-46s → %s\n' "$1" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/auth/login" \
        -H 'Content-Type: application/json' -d "$2")"
}

yoxla "düzgün e-poçt + düzgün şifrə"  '{"email":"admin@arti.edu.az","parol":"123456"}'
yoxla "pis e-poçt formatı"            '{"email":"admin","parol":"123456"}'
yoxla "şifrə 3 simvol"                '{"email":"admin@arti.edu.az","parol":"123"}'
yoxla "boş cisim"                     '{}'
yoxla "e-poçt yoxdur, şifrə var"      '{"parol":"123456"}'

echo "── Detallı mesaj (pis e-poçt) ──"
curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin","parol":"123456"}' | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  mesaj :', d['xeta']['mesaj'])
for x in d['xeta'].get('detallar', []): print('  detal :', x)
"
)
