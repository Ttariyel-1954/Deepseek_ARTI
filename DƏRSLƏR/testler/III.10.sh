LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"baxici@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── 1) Həqiqi token (baxici) ──"
printf '  /auth/profil            → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H "$H")"

SAXTA=$(printf '%s' "$TOKEN" | python3 -c "
import base64, json, sys
b, y, i = sys.stdin.read().strip().split('.')
def ac(h):
    h += '=' * (-len(h) % 4); return json.loads(base64.urlsafe_b64decode(h))
def kodla(o):
    return base64.urlsafe_b64encode(json.dumps(o).encode()).decode().rstrip('=')
yeni = ac(y); yeni['rol'] = 'admin'
print(b + '.' + kodla(yeni) + '.' + i)")

echo "── 2) Yükü dəyişilmiş token (rol → admin) ──"
printf '  /auth/profil            → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H "Authorization: Bearer $SAXTA")"
printf '  /auth/istifadeciler     → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/istifadeciler" -H "Authorization: Bearer $SAXTA")"

echo "── 3) Cavab ──"
curl -s "$A/auth/profil" -H "Authorization: Bearer $SAXTA" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  kod  :', d['xeta']['kod']); print('  mesaj:', d['xeta']['mesaj'])"

echo "── 4) Tamamilə uydurma token ──"
printf '  uydurma.token.imza      → %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/auth/profil" -H 'Authorization: Bearer uydurma.token.imza')"
)
