LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── Tokensiz çağırışlar ──"
for yol in "" "/saglamliq"; do
  printf '  GET %-14s → %s\n' "/$yol" "$(curl -s -o /dev/null -w '%{http_code}' "$A$yol")"
done
printf '  POST %-13s → %s (pis cisim, 401 DEYİL, 400 olmalı)\n' "/auth/login" \
  "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/auth/login" \
      -H 'Content-Type: application/json' -d '{}')"

echo "── Kodda @Public() işarələnənlər ──"
grep -rn -A2 '@Public()' src/ --include=*.controller.ts | grep -E '@Public|@(Get|Post)' | sed 's/^/  /'
)
