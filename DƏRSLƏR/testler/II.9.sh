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

echo "── Şöbəsi olan mərkəzlər ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT m.id || ' | ' || m.ad || ' | şöbə: ' || count(s.id)
  FROM struktur.merkezler m
  JOIN struktur.shobeler s ON s.merkez_id = m.id
  GROUP BY m.id, m.ad ORDER BY m.id LIMIT 3" | sed 's/^/  /'

ID=$(psql -U arti_user -d arti_baza -tA -c "
  SELECT m.id FROM struktur.merkezler m
  JOIN struktur.shobeler s ON s.merkez_id = m.id
  GROUP BY m.id ORDER BY m.id LIMIT 1")

echo "── $ID nömrəli mərkəzi silmək cəhdi ──"
curl -s -X DELETE "$A/struktur/merkezler/$ID" -H "$H" | python3 -m json.tool

echo "── Mərkəz hələ də yerindədir? ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  ✓ ' || ad || ' — silinmədi' FROM struktur.merkezler WHERE id = $ID"
)
