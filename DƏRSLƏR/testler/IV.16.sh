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

echo "── POST /ai/cavab ──"
curl -s -X POST "$A/ai/cavab" -H "Authorization: Bearer $T" \
  -H 'Content-Type: application/json' \
  -d '{"sual":"Elmi dərəcə ilə bağlı sənədlər hansılardır?"}' | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  demo               :', d['demo'], '← açar olmadığı üçün')
print('  model              :', d['model'])
print('  token_sayi         :', d['token_sayi'], '(demo rejimdə hesablanmır)')
print('  istifadə olunan sənəd:', d.get('istifade_olunan_senedler'))
print()
print('  cavab:')
for l in str(d['cavab']).splitlines()[:6]: print('   ', l)
"
)
