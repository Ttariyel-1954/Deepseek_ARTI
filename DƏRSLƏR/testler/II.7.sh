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

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── API cavabı ──"
curl -s "$A/struktur/merkezler/statistika" -H "$H" | python3 -c "
import json,sys
for s in json.load(sys.stdin):
    print('  %-38s şöbə: %-3s əməkdaş: %s' % (s['ad'], s['shobe_sayi'], s['emekdas_sayi']))
"

echo "── Bazadan yoxlama (eyni rəqəmlər olmalıdır) ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT m.ad || ' → şöbə: ' || count(DISTINCT s.id) || ' əməkdaş: ' || count(DISTINCT e.id)
  FROM struktur.merkezler m
  LEFT JOIN struktur.shobeler s ON s.merkez_id = m.id
  LEFT JOIN kadrlar.emekdaslar e ON e.merkez_id = m.id
  GROUP BY m.ad ORDER BY m.ad" | sed 's/^/  /'
)
