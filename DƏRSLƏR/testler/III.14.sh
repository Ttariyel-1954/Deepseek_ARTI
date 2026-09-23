LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── GET /auth/istifadeciler ──"
for rol in admin muhendis maliyyeci baxici; do
  T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  KOD=$(curl -s -o /tmp/_u.json -w '%{http_code}' "$A/auth/istifadeciler" -H "Authorization: Bearer $T")
  EK=""
  [ "$KOD" = "200" ] && EK="($(python3 -c "import json;print(len(json.load(open('/tmp/_u.json'))))") istifadəçi)"
  printf '  %-10s → %s %s\n' "$rol" "$KOD" "$EK"
done
rm -f /tmp/_u.json

echo "── Admin görən məlumat ──"
T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
curl -s "$A/auth/istifadeciler" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
for u in json.load(sys.stdin):
    print('  %-24s %-10s %s' % (u['email'], u['rol'], u['ad_soyad']))
"
)
