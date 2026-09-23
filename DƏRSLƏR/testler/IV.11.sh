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
H="Authorization: Bearer $T"

for s in "Orta maaş nə qədərdir?" "Ən çox maaş alan kimdir?"; do
  echo "── «$s» ──"
  curl -s -X POST "$A/ai/sual" -H "$H" -H 'Content-Type: application/json' \
    -d "{\"sual\":\"$s\"}" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  izah  :', d['izah'])
print('  nəticə:', json.dumps(d['setirler'][:2], ensure_ascii=False))
"
done

echo "── ✅ «Orta maaş» XÜSUSİ reseptə düşməlidir, ümumi «maaş»-a YOX ──"
)
