LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur: $(pwd)"; exit 1; }
[ -f .env ] || { echo "  ✗ .env yoxdur — DATABASE_URL tapılmır"; exit 1; }
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
[ -n "$DBURL" ] || { echo "  ✗ .env-də DATABASE_URL yoxdur"; exit 1; }
say()  { psql "$DBURL" -At -c "$1" 2>/dev/null | tr -d ' '; }

[ -f skriptler/crud_yoxla.sh ] \
  || { echo "  ✗ skriptler/crud_yoxla.sh yoxdur — ADDIM 21-i işlədin"; exit 1; }

echo ""
echo "  → 1) Skriptin sintaksisi"
bash -n skriptler/crud_yoxla.sh || { echo "  ✗ bash sintaksisi səhvdir"; exit 1; }
printf '      ✓ düzgündür (%s sətir, %s yoxlama)\n' \
  "$(wc -l < skriptler/crud_yoxla.sh | tr -d ' ')" \
  "$(grep -c '^sorqu ' skriptler/crud_yoxla.sh)"

echo ""
echo "  → 2) Bazanın vəziyyəti (əvvəl)"
EVVEL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      əməkdaş sayı: %s\n' "$EVVEL"

echo ""
echo "  → 3) Skript işlədilir (istifadəçinin əmri ilə)"
bash skriptler/crud_yoxla.sh
CIXIS=$?
echo ""
printf '      skriptin çıxış kodu: %s\n' "$CIXIS"
[ "$CIXIS" -eq 0 ] || { echo "  ✗ CRUD skripti uğursuz oldu"; exit 1; }

echo ""
echo "  → 4) Simmetriya yoxlaması"
SONRA=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
ZIBIL=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'test.crud.%@arti.edu.az';")
printf '      əvvəl: %s   sonra: %s   test zibili: %s\n' "$EVVEL" "$SONRA" "$ZIBIL"
[ "$EVVEL" = "$SONRA" ] || { echo "  ✗ sətir sayı dəyişdi!"; exit 1; }
[ "$ZIBIL" = "0" ] || { echo "  ✗ test zibili qaldı: $ZIBIL"; exit 1; }
echo "      ✓ baza tam əvvəlki vəziyyətindədir"

echo ""
echo "  → 5) Səhv port → skript aydın xəta verirmi?"
python3 -m http.server 4187 --bind 127.0.0.1 >/dev/null 2>&1 &
TUTAN=$!
sleep 1.5
CIXIS2=$(PORT=4187 bash skriptler/crud_yoxla.sh 2>&1)
KOD2=$?
kill $TUTAN 2>/dev/null
wait $TUTAN 2>/dev/null
printf '%s\n' "$CIXIS2" | head -3 | sed 's/^/      /'
printf '      exit kodu: %s\n' "$KOD2"
[ "$KOD2" -ne 0 ] || { echo "  ✗ məşğul portda skript uğurlu oldu — bu mümkün deyil"; exit 1; }
echo "      ✓ məşğul portu tanıdı və dayandı"

echo ""
echo "  → 6) YEKUN: bütün yoxlama alətləri bir yerdə"
printf '      a) tip yoxlaması   : '
npx tsc --noEmit && echo "✓ təmiz"
printf '      b) DTO matrisi     : '
npx tsx skriptler/dto_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      c) mapper          : '
npx tsx skriptler/mapper_yoxla.ts 2>&1 | grep -c 'JSON.stringify İŞLƏDİ' >/dev/null && echo "✓ işləyir"
printf '      d) servis yoxlaması: '
npx tsx skriptler/servis_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'

echo ""
echo "  → 7) Son vəziyyət"
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      bazada əməkdaş: %s\n' "$TOTAL"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }

echo ""
echo "  ✓ IIA.10 KEÇDİ — Dərs 2A-nın bütün nəticələri təsdiqləndi"
)
