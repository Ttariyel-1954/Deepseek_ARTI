LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
echo "GET /saglamliq → $kod"
if [ "$kod" != "200" ]; then
  echo "⚠️ Server işləmir. Ayrı terminalda işlədin:"
  echo "   cd $LAYIHE && PORT=4000 npm run start:prod"
  exit 1
fi

echo "── Serverin cavabı ──"
curl -s "$A/saglamliq" | python3 -m json.tool

echo "── Bazadakı real cədvəl sayı ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT count(*) FROM pg_class c
  JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE c.relkind = 'r'
    AND n.nspname NOT IN ('pg_catalog','information_schema')" | sed 's/^/  /'
)
