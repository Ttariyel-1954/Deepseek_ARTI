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
H="Authorization: Bearer $TOKEN"

echo "── limit=20 (icazəli) ──"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$A/struktur/merkezler?limit=20" -H "$H"

echo "── limit=500 (həddi aşır) ──"
curl -s "$A/struktur/merkezler?limit=500" -H "$H" | python3 -m json.tool

echo "── limit=abc (rəqəm deyil) ──"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$A/struktur/merkezler?limit=abc" -H "$H"
)
