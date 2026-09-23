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

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── Əvvəl ──"
psql -U arti_user -d arti_baza -tA -c \
  "SELECT '  ai.embeddingler: ' || count(*) || ' sətir' FROM ai.embeddingler"

echo "── POST /ai/vektorlasdir ──"
curl -s -X POST "$A/ai/vektorlasdir" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  baxılan sənəd:', d.get('baxildi'), '| yazılan:', d.get('yazildi'))"

echo "── Sonra ──"
psql -U arti_user -d arti_baza -tA -c \
  "SELECT '  ai.embeddingler: ' || count(*) || ' sətir' FROM ai.embeddingler"

echo "── Hansı cədvəllər vektorlaşdırılıb? ──"
psql -U arti_user -d arti_baza -c \
  "SELECT cedvel_adi, count(*) AS sayi, min(jsonb_array_length(vektor)) AS olcu
   FROM ai.embeddingler GROUP BY cedvel_adi" | sed 's/^/  /'
)
