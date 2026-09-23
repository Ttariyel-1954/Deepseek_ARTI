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

echo "── 1) POST /struktur/merkezler ──"
YENI=$(curl -s -X POST "$A/struktur/merkezler" -H "$H" -H 'Content-Type: application/json' \
  -d '{"ad":"Test Mərkəzi","tip":"merkez","tesvir":"Yoxlama üçün"}')
ID=$(printf '%s' "$YENI" | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")
echo "$YENI" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  id:', d['id'], '| ad:', d['ad'], '| tip:', d['tip'])"

echo "── 2) GET ilə oxu ──"
curl -s "$A/struktur/merkezler/$ID" -H "$H" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  oxundu:', d['ad'], '| aktiv:', d['aktiv'])"

echo "── 3) Eyni adla təkrar yaratmaq → 409 ──"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" -X POST "$A/struktur/merkezler" \
  -H "$H" -H 'Content-Type: application/json' -d '{"ad":"Test Mərkəzi","tip":"merkez"}'

echo "── 4) DELETE ──"
curl -s -X DELETE "$A/struktur/merkezler/$ID" -H "$H" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  silindi:', d['ad'])"

echo "── 5) Silindikdən sonra oxumaq → 404 ──"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$A/struktur/merkezler/$ID" -H "$H"
)
