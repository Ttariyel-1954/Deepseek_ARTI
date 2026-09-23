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

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

for cift in "merkezler:struktur.merkezler" "emekdaslar:kadrlar.emekdaslar"; do
  FAYL=$(echo "$cift" | cut -d: -f1); CEDVEL=$(echo "$cift" | cut -d: -f2)
  curl -s -o /tmp/yoxla.xlsx "$A/ixrac/$FAYL.xlsx" -H "Authorization: Bearer $T"
  DB=$(psql -U arti_user -d arti_baza -tA -c "SELECT count(*) FROM $CEDVEL" | tr -d ' ')
  XL=$(unzip -p /tmp/yoxla.xlsx xl/worksheets/sheet1.xml | grep -o '<row ' | wc -l | tr -d ' ')
  echo "── $FAYL ──"
  echo "  bazada      : $DB sətir"
  echo "  Excel-də    : $XL sətir (başlıq daxil)"
  echo "  gözlənilən  : $((DB + 1))  →  $([ "$XL" = "$((DB + 1))" ] && echo '✓ uyğundur' || echo '✗ UYĞUN DEYİL')"
  echo "  başlıq sətri: $(unzip -p /tmp/yoxla.xlsx xl/sharedStrings.xml 2>/dev/null | grep -o '<t>[^<]*</t>' | head -1 | sed 's/<[^>]*>//g')"
done
rm -f /tmp/yoxla.xlsx
)
