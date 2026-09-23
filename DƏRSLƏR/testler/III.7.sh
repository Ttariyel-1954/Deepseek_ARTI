LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── Mövcud e-poçt + səhv şifrə ──"
curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"sehv-parol-2026"}' | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  mesaj :', d['xeta']['mesaj'])"

echo "── Mövcud OLMAYAN e-poçt + səhv şifrə ──"
curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"yoxdur@arti.edu.az","parol":"sehv-parol-2026"}' | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  mesaj :', d['xeta']['mesaj'])"

echo "── Cavab vaxtları (fərq kiçik olmalıdır) ──"
for e in admin@arti.edu.az yoxdur@arti.edu.az; do
  t=$( { /usr/bin/time -p curl -s -o /dev/null -X POST "$A/auth/login" \
        -H 'Content-Type: application/json' \
        -d "{\"email\":\"$e\",\"parol\":\"sehv-parol-2026\"}"; } 2>&1 | awk '/real/{print $2}')
  printf '  %-22s %s san\n' "$e" "$t"
done

echo "── Saxta hash harada istifadə olunur? ──"
grep -n 'fake\|saxta\|DUMMY\|compare' src/auth/auth.service.ts | head -5 | sed 's/^/  /'
)
