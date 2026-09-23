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

CAVAB=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}')
TOKEN=$(printf '%s' "$CAVAB" | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── 1) Login cavabında ──"
printf '%s' "$CAVAB" | grep -q 'parol_hash' && echo "  ✗ parol_hash SIZIB!" || echo "  ✓ parol_hash yoxdur"
printf '%s' "$CAVAB" | grep -q '\$2[aby]\$' && echo "  ✗ bcrypt hash-i SIZIB!" || echo "  ✓ bcrypt izi yoxdur"

echo "── 2) Tokenin içində ──"
printf '%s' "$TOKEN" | grep -q 'parol_hash' && echo "  ✗ SIZIB!" || echo "  ✓ parol_hash yoxdur"
printf '%s' "$TOKEN" | grep -q '\$2[aby]\$' && echo "  ✗ bcrypt izi SIZIB!" || echo "  ✓ bcrypt izi yoxdur"

echo "── 3) Bazada şifrə NECƏ saxlanılır ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  ' || email || ' → ' || left(parol_hash, 7) || '… (' || length(parol_hash) || ' simvol)'
  FROM kadrlar.istifadeciler ORDER BY id" 
echo "  (bcrypt hash-i geri açıla bilmir — yalnız müqayisə olunur)"
)
