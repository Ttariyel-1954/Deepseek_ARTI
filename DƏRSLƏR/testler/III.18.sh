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
H="Authorization: Bearer $T"

say() { psql -U arti_user -d arti_baza -tA -c "SELECT count(*) FROM audit.audit_log" | tr -d ' '; }

echo "── 3 × GET ──"
E=$(say)
for i in 1 2 3; do curl -s -o /dev/null "$A/struktur/merkezler" -H "$H"; done
S=$(say)
echo "  əvvəl: $E   sonra: $S   fərq: $((S - E))   (gözlənilən: 0)"

echo "── 1 × POST + 1 × DELETE ──"
E=$(say)
ID=$(curl -s -X POST "$A/struktur/merkezler" -H "$H" -H 'Content-Type: application/json' \
  -d '{"ad":"Audit testi","tip":"merkez"}' | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")
curl -s -o /dev/null -X DELETE "$A/struktur/merkezler/$ID" -H "$H"
S=$(say)
echo "  əvvəl: $E   sonra: $S   fərq: $((S - E))   (gözlənilən: 2)"

echo "── Son 3 jurnal sətri ──"
psql -U arti_user -d arti_baza -c "
  SELECT cedvel_adi, emeliyyat, setir_id, istifadeci, qeyd
  FROM audit.audit_log ORDER BY id DESC LIMIT 3" | sed 's/^/  /'
)
