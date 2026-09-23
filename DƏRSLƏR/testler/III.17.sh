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

temizle() {
  psql -U arti_user -d arti_baza -q -c \
    "DELETE FROM kadrlar.istifadeciler WHERE email = 'yoxlama@arti.edu.az'" 2>/dev/null
}
trap temizle EXIT

ADMIN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
BAXICI=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"baxici@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

CISIM='{"email":"yoxlama@arti.edu.az","parol":"yoxlama2026","ad_soyad":"Yoxlama Istifadeci","rol":"baxici"}'

echo "── baxici cəhd edir ──"
printf '  HTTP %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/auth/qeydiyyat" \
  -H "Authorization: Bearer $BAXICI" -H 'Content-Type: application/json' -d "$CISIM")"

echo "── admin cəhd edir ──"
curl -s -X POST "$A/auth/qeydiyyat" -H "Authorization: Bearer $ADMIN" \
  -H 'Content-Type: application/json' -d "$CISIM" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  yaradıldı:', d.get('email'), '| rol:', d.get('rol'), '| id:', d.get('id'))
print('  parol_hash cavabda varmı?', 'BƏLİ ⚠️' if 'parol_hash' in json.dumps(d) else 'xeyr ✓')
"

echo "── Eyni e-poçtla təkrar → 409 ──"
printf '  HTTP %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/auth/qeydiyyat" \
  -H "Authorization: Bearer $ADMIN" -H 'Content-Type: application/json' -d "$CISIM")"

echo "── Yeni istifadəçi giriş edə bilir? ──"
printf '  login → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/auth/login" \
  -H 'Content-Type: application/json' -d '{"email":"yoxlama@arti.edu.az","parol":"yoxlama2026"}')"
)
