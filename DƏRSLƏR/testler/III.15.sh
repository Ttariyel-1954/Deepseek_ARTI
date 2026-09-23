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

echo "── admin hər qorunan endpointə girir ──"
for yol in /struktur/merkezler /struktur/merkezler/statistika \
           /kadrlar/emekdaslar /kadrlar/emekdaslar/icmal \
           /auth/profil /auth/istifadeciler \
           /ai/statistika /ai/reseptler /ixrac/merkezler.xlsx \
           /tehsil/istirakciler /tehsil/statistika; do
  printf '  %-32s → %s\n' "$yol" "$(curl -s -o /dev/null -w '%{http_code}' "$A$yol" -H "$H")"
done

echo "── Guard-daki super-rol qaydası ──"
grep -n "admin' === \|super\|=== 'admin'" src/auth/guards/roles.guard.ts | sed 's/^/  /'
)
