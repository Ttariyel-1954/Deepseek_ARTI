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

yoxla() {
  printf '  %-26s → %s\n' "$1" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/ai/rag" -H "$H" \
        -H 'Content-Type: application/json' -d "$2")"
}

echo "── 1) Limit göstərilməyib (default 3) ──"
curl -s -X POST "$A/ai/rag" -H "$H" -H 'Content-Type: application/json' \
  -d '{"sual":"elm və təhsil haqqında"}' | python3 -c "
import json,sys; print('  tapıldı:', json.load(sys.stdin)['tapildi'])"

echo "── 2) limit=1 ──"
curl -s -X POST "$A/ai/rag" -H "$H" -H 'Content-Type: application/json' \
  -d '{"sual":"elm və təhsil haqqında","limit":1}' | python3 -c "
import json,sys; print('  tapıldı:', json.load(sys.stdin)['tapildi'])"

echo "── 3) Hədd yoxlaması ──"
yoxla "limit=10 (icazəli)"  '{"sual":"elm və təhsil","limit":10}'
yoxla "limit=11 (həddi aşır)" '{"sual":"elm və təhsil","limit":11}'
yoxla "limit=0 (mənfi hədd)" '{"sual":"elm və təhsil","limit":0}'
)
