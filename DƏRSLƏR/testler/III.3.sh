LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  cavab sahələri :', ', '.join(d.keys()))
print('  token hissəsi  :', len(d['token'].split('.')), '(header.payload.signature)')
print('  token uzunluğu :', len(d['token']), 'simvol')
print('  istifadəçi     :', d['istifadeci']['ad_soyad'], '/', d['istifadeci']['rol'])
print('  bitme          :', d['bitme'])
print()
print('  token başlanğıcı:', d['token'][:32] + '…')
"
)
