LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── Siyahıdan bir kadr ──"
curl -s "$A/kadrlar/emekdaslar?limit=2" -H "$H" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  cemi:', d['cemi'])
for s in d['setirler']:
    print('  %s %s | %s | maas: %s (%s)' % (s['ad'], s['soyad'],
          s.get('merkez'), s.get('maas'), type(s.get('maas')).__name__))
"

echo "── JOIN ilə tam profil ──"
ID=$(curl -s "$A/kadrlar/emekdaslar?limit=1" -H "$H" | python3 -c "
import json,sys;print(json.load(sys.stdin)['setirler'][0]['id'])")
curl -s "$A/kadrlar/emekdaslar/$ID" -H "$H" | python3 -c "
import json,sys
d = json.load(sys.stdin)
for k, v in d.items():
    if isinstance(v, list):
        print('  %-14s → %d qeyd' % (k, len(v)))
    else:
        print('  %-14s → %s' % (k, v))
"

echo "── İcmal endpointi ──"
curl -s "$A/kadrlar/emekdaslar/icmal" -H "$H" | python3 -m json.tool | head -14
)
