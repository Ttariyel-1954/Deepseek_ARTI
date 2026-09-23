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

echo "── İki fayl ──"
for f in merkezler emekdaslar; do
  AD=$(curl -s -o /dev/null -D - "$A/ixrac/$f.xlsx" -H "Authorization: Bearer $T" \
    | grep -i 'content-disposition' | tr -d '\r' | sed 's/.*filename="//; s/"//')
  curl -s -o /tmp/yoxla.xlsx "$A/ixrac/$f.xlsx" -H "Authorization: Bearer $T"
  echo "  $f.xlsx → $(wc -c < /tmp/yoxla.xlsx | tr -d ' ') bayt | fayl adı: $AD"
done
rm -f /tmp/yoxla.xlsx

echo "── Server diskdə fayl saxlayırmı? ──"
echo "  /tmp-də artıq .xlsx: $(ls /tmp/*.xlsx 2>/dev/null | wc -l | tr -d ' ')"
echo "  layihədə: $(find . -name '*.xlsx' -not -path './node_modules/*' 2>/dev/null | wc -l | tr -d ' ')"
echo "  → fayl yalnız yaddaşda qurulur (Buffer), diskə yazılmır"

echo "── Content-Disposition necə qurulur? ──"
grep -n 'Content-Disposition\|attachment\|toISOString' src/ixrac/ixrac.controller.ts | sed 's/^/  /'
)
