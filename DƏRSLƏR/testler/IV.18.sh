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

curl -s -o /tmp/yoxla.xlsx "$A/ixrac/merkezler.xlsx" -H "Authorization: Bearer $T"

echo "── Bayt yoxlaması ──"
echo "  ilk 4 bayt (hex): $(xxd -p -l 4 /tmp/yoxla.xlsx)"
echo "  PK imzası       : $(xxd -p -l 2 /tmp/yoxla.xlsx | tr 'A-Z' 'a-z')  (504b olmalıdır)"

echo "── file əmri ──"
file -b /tmp/yoxla.xlsx | sed 's/^/  /'

echo "── ZIP içində nə var? ──"
unzip -l /tmp/yoxla.xlsx | head -8 | sed 's/^/  /'

echo "── Səhv import olsaydı nə olardı? ──"
grep -n "^import ExcelJS" src/ixrac/excel.service.ts | sed 's/^/  düzgün: /'
echo "  səhv  : import * as ExcelJS  →  ExcelJS.Workbook is not a constructor"
rm -f /tmp/yoxla.xlsx
)
