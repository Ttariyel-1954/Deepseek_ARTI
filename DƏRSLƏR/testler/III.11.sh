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

# ⚠️ Skript nə olursa olsun istifadəçini AKTİV saxlayır
geri_qaytar() {
  psql -U arti_user -d arti_baza -q -c \
    "UPDATE kadrlar.istifadeciler SET aktiv = true WHERE email = 'baxici@arti.edu.az'" 2>/dev/null
}
trap geri_qaytar EXIT

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"baxici@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── 1) İstifadəçi aktivdir ──"
printf '  /auth/profil → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H "$H")"

echo "── 2) İstifadəçi deaktiv edilir (token DƏYİŞMİR) ──"
psql -U arti_user -d arti_baza -q -c \
  "UPDATE kadrlar.istifadeciler SET aktiv = false WHERE email = 'baxici@arti.edu.az'"
printf '  /auth/profil → %s  (eyni tokenlə!)\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H "$H")"
curl -s "$A/auth/profil" -H "$H" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  mesaj :', d['xeta']['mesaj'])"

echo "── 3) İstifadəçi yenidən aktiv edilir ──"
geri_qaytar
printf '  /auth/profil → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H "$H")"

echo "── Strategiyanın yoxlaması ──"
grep -n 'aktiv\|findUnique\|queryRaw\|Unauthorized' src/auth/strategies/jwt.strategy.ts | head -6 | sed 's/^/  /'
)
