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

echo "── Cavab başlıqları ──"
curl -s -o /dev/null -D - "$A/ixrac/merkezler.xlsx" -H "Authorization: Bearer $T" \
  | grep -iE '^HTTP|content-type|content-disposition|content-length' | tr -d '\r' | sed 's/^/  /'

echo "── Dörd rolun hamısı yükləyə bilir? ──"
for rol in admin muhendis maliyyeci baxici; do
  RT=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  printf '  %-10s → %s\n' "$rol" "$(curl -s -o /dev/null -w '%{http_code}' "$A/ixrac/merkezler.xlsx" -H "Authorization: Bearer $RT")"
done
)
