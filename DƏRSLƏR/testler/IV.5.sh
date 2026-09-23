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

curl -s -X POST "$A/ai/rag" -H "Authorization: Bearer $T" \
  -H 'Content-Type: application/json' \
  -d '{"sual":"elm və təhsil haqqında sənəd"}' | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  sual    :', d['sual'])
print('  tapıldı :', d['tapildi'])
print()
for n in d['neticeler']:
    print('  bal %.6f | sənəd #%s | %s' % (n['oxsarlıq'], n['sened_id'], n['metn'][:46]))
ballar = [n['oxsarlıq'] for n in d['neticeler']]
print()
print('  azalan sıra   :', ballar == sorted(ballar, reverse=True))
print('  hamısı > 0    :', all(b > 0 for b in ballar))
print('  hamısı ≤ 1    :', all(b <= 1 for b in ballar))
"
)
