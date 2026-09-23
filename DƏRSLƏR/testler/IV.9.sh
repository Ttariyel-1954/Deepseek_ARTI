LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

curl -s "$A/ai/reseptler" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  resept sayı:', d['say'])
print()
for i, r in enumerate(d['reseptler'], 1):
    print('  %2d. %-22s ← %s' % (i, r['izah'], r['açar'][:46]))
print()
adlar = [r['izah'] for r in d['reseptler']]
o = adlar.index('Orta əmək haqqı')
u = adlar.index('Ən çox maaş alan 5 nəfər')
print('  «orta maaş» sırası :', o + 1)
print('  «ümumi maaş» sırası:', u + 1)
print('  ⚠️ xüsusi ümumidən ƏVVƏLdir:', o < u)
"
)
