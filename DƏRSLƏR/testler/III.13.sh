LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

ADMIN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

# Yoxlama üçün boş mərkəz yaradırıq
ID=$(curl -s -X POST "$A/struktur/merkezler" -H "Authorization: Bearer $ADMIN" \
  -H 'Content-Type: application/json' -d '{"ad":"Silme testi","tip":"merkez"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")
echo "  Yoxlama mərkəzi yaradıldı: id=$ID"

echo "── @Roles('admin') — DELETE /struktur/merkezler/$ID ──"
for rol in muhendis maliyyeci baxici; do
  T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  printf '  %-10s → %s\n' "$rol" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$A/struktur/merkezler/$ID" -H "Authorization: Bearer $T")"
done

echo "── admin → 200 ──"
curl -s -X DELETE "$A/struktur/merkezler/$ID" -H "Authorization: Bearer $ADMIN" \
  | python3 -c "import json,sys;print('  silindi:', json.load(sys.stdin)['ad'])"
)
