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

BAXICI=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"baxici@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── baxici mərkəz silməyə çalışır (403 olacaq) ──"
printf '  HTTP %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$A/struktur/merkezler/1" \
  -H "Authorization: Bearer $BAXICI")"

sleep 1
echo "── Jurnalda bu cəhd görünürmü? ──"
psql -U arti_user -d arti_baza -c "
  SELECT cedvel_adi, emeliyyat, istifadeci, qeyd, vaxt::timestamp(0)
  FROM audit.audit_log
  WHERE istifadeci = 'baxici@arti.edu.az'
  ORDER BY id DESC LIMIT 3" | sed 's/^/  /'

echo "── XƏTA qeydi olan cəhdlərin sayı ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  ' || count(*) || ' uğursuz cəhd jurnala yazılıb'
  FROM audit.audit_log WHERE qeyd LIKE 'XƏTA%'"
)
