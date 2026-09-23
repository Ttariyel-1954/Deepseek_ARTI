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

echo "── @Roles('admin','muhendis') — POST /struktur/merkezler ──"
for rol in admin muhendis maliyyeci baxici; do
  T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  KOD=$(curl -s -o /tmp/_m.json -w '%{http_code}' -X POST "$A/struktur/merkezler" \
    -H "Authorization: Bearer $T" -H 'Content-Type: application/json' \
    -d "{\"ad\":\"RBAC testi — $rol\",\"tip\":\"merkez\"}")
  printf '  %-10s → %s\n' "$rol" "$KOD"
  if [ "$KOD" = "201" ]; then
    ID=$(python3 -c "import json;print(json.load(open('/tmp/_m.json'))['id'])")
    curl -s -o /dev/null -X DELETE "$A/struktur/merkezler/$ID" -H "Authorization: Bearer $TOKEN"
  fi
done
rm -f /tmp/_m.json

echo "── Controller-də dekorator ──"
grep -n -B2 "'merkezler')" src/struktur/struktur.controller.ts | head -8 | sed 's/^/  /'
)
