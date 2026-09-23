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
  -d '{"email":"maliyyeci@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── maliyyeci → POST /struktur/merkezler ──"
curl -s -X POST "$A/struktur/merkezler" -H "Authorization: Bearer $T" \
  -H 'Content-Type: application/json' -d '{"ad":"olmayacaq","tip":"merkez"}' | python3 -m json.tool

echo "── maliyyeci → GET /auth/istifadeciler ──"
curl -s "$A/auth/istifadeciler" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  ugur :', d['ugur'])
print('  kod  :', d['xeta']['kod'])
print('  mesaj:', d['xeta']['mesaj'])
"
)
