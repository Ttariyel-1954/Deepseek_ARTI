LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"

CISIM='{"sual":"Banana qiyməti nə qədərdir?"}'
echo "── HTTP kodu ──"
printf '  %s (500 DEYİL)\n' "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/ai/sual" -H "$H" -H 'Content-Type: application/json' -d "$CISIM")"

echo "── Cavab ──"
curl -s -X POST "$A/ai/sual" -H "$H" -H 'Content-Type: application/json' -d "$CISIM" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  uygun_resept:', d['uygun_resept'])
print('  sətir sayı  :', d['setir_sayi'])
print('  izah (dəstəklənən suallar):')
for x in d['izah'].split('; '): print('     -', x)
"
)
