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

echo "── GET /tehsil/statistika ──"
curl -s "$A/tehsil/statistika" -H "Authorization: Bearer $T" | python3 -m json.tool

echo "── Uyğunsuz pasportların siyahısı ──"
for id in 1 2 3 4 5 6 7 8 9 10; do
  curl -s "$A/tehsil/istirakciler/$id/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
d = json.load(sys.stdin)
if not d['etibarlidir']:
    print('  ✗ %-20s %-14s %s' % (d['sahib']['tam_ad'], d['pasport_no'], d['uygunsuzluq'][:52]))
"
done
)
