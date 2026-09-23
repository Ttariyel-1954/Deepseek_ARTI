LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── POST /ai/vektorlasdir ──"
for rol in admin muhendis maliyyeci baxici; do
  T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  printf '  %-10s → %s\n' "$rol" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/ai/vektorlasdir" -H "Authorization: Bearer $T")"
done
printf '  %-10s → %s\n' "tokensiz" "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/ai/vektorlasdir")"

echo "── baxicinin aldığı cavab ──"
T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"baxici@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
curl -s -X POST "$A/ai/vektorlasdir" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  kod  :', d['xeta']['kod']); print('  mesaj:', d['xeta']['mesaj'])"
)
