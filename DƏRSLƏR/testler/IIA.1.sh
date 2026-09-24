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

echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) DTO faylları"
catmadi=0
for f in src/emekdaslar/dto/emekdas-sorgu.dto.ts \
         src/emekdaslar/dto/emekdas-yarat.dto.ts \
         src/emekdaslar/dto/emekdas-yenile.dto.ts \
         skriptler/dto_yoxla.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ DTO faylları natamamdır — ADDIM 17-ni işlədin"; exit 1; }

echo ""
echo "  → 2) Qaydaların sayı"
IS=$(grep -c '@Is' src/emekdaslar/dto/*.ts | awk -F: '{s+=$2} END {print s}')
MSJ=$(grep -c 'message:' src/emekdaslar/dto/*.ts | awk -F: '{s+=$2} END {print s}')
printf '      @Is… dekoratoru      : %s\n' "$IS"
printf '      Azərbaycanca mesaj   : %s\n' "$MSJ"
[ "$IS" -ge 45 ] || { echo "  ✗ @Is dekoratorlarının sayı azdır: $IS"; exit 1; }
[ "$MSJ" -ge 30 ] || { echo "  ✗ Azərbaycanca mesajların sayı azdır: $MSJ"; exit 1; }
echo "      ✓ hər qaydanın öz mesajı var"

echo ""
echo "  → 3) Ağ siyahı (allowlist) varmı?"
grep -q 'SIRALANA_BILEN' src/emekdaslar/dto/emekdas-sorgu.dto.ts \
  || { echo "      ✗ sıralama ağ siyahısı yoxdur!"; exit 1; }
grep -q '@IsIn' src/emekdaslar/dto/emekdas-sorgu.dto.ts \
  || { echo "      ✗ @IsIn dekoratoru yoxdur!"; exit 1; }
echo "      ✓ sıralama yalnız icazəli sütunlarla məhdudlaşır"

echo ""
echo "  → 4) Tip yoxlaması"
npx tsc --noEmit || { echo "  ✗ tip xətası var"; exit 1; }
echo "      ✓ təmiz"

echo ""
echo "  → 5) REAL validasiya matrisi"
npx tsx skriptler/dto_yoxla.ts
CIXIS=$?
[ "$CIXIS" -eq 0 ] || { echo "  ✗ validasiya matrisi uğursuz oldu (exit $CIXIS)"; exit 1; }

echo ""
echo "  ✓ IIA.1 KEÇDİ — DTO-lar tamdır və 25 qayda işləyir"
)
