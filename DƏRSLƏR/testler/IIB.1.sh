LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur: $(pwd)"; exit 1; }
[ -f .env ] || { echo "  ✗ .env yoxdur"; exit 1; }
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
[ -n "$DBURL" ] || { echo "  ✗ .env-də DATABASE_URL yoxdur"; exit 1; }
say() { psql "$DBURL" -At -c "$1" 2>/dev/null | tr -d ' '; }

echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) Statistika faylları"
catmadi=0
for f in src/emekdaslar/statistika/dto/statistika-sorgu.dto.ts \
         src/emekdaslar/statistika/statistika.service.ts \
         src/emekdaslar/statistika/statistika.controller.ts \
         skriptler/statistika_yoxla.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ fayllar natamamdır — ADDIM 22-ni işlədin"; exit 1; }

echo ""
echo "  → 2) Prisma aqreqat metodları"
S=src/emekdaslar/statistika/statistika.service.ts
for m in 'groupBy' '_count' '_avg' '_sum' '_min' '_max' 'aggregate'; do
  N=$(grep -c "$m" "$S" || true)
  printf '      %-12s %s\n' "$m" "$N"
  [ "$N" -ge 1 ] || { echo "      ✗ $m istifadə olunmur!"; exit 1; }
done

echo ""
echo "  → 3) Baza funksiyaları və təhlükəsizlik"
grep -q 'queryRaw' "$S" || { echo "      ✗ queryRaw yoxdur!"; exit 1; }
printf '      $queryRaw çağırışı : %s\n' "$(grep -c 'queryRaw' "$S")"
grep -q 'queryRawUnsafe' "$S" && { echo "      ✗ TƏHLÜKƏLİ: queryRawUnsafe işlədilir!"; exit 1; }
echo "      ✓ queryRawUnsafe işlədilmir (SQL inyeksiyası qorunur)"
printf '      $transaction       : %s\n' "$(grep -c 'transaction' "$S")"

echo ""
echo "  → 4) Statistika endpoint-ləri"
printf '      endpoint sayı: %s\n' "$(grep -c '@Get' src/emekdaslar/statistika/statistika.controller.ts)"
for y in statistika statistika/merkezler statistika/vezifeler statistika/merkezler-tam; do
  grep -q "'$y'" src/emekdaslar/statistika/statistika.controller.ts \
    || { echo "      ✗ /$y yoxdur!"; exit 1; }
done
echo "      ✓ dörd endpoint mövcuddur"

echo ""
echo "  → 5) Tip yoxlaması"
npx tsc --noEmit || { echo "  ✗ tip xətası var"; exit 1; }
echo "      ✓ təmiz"

echo ""
echo "  → 6) CANLI statistika yoxlaması"
npx tsx skriptler/statistika_yoxla.ts
[ $? -eq 0 ] || { echo "  ✗ statistika probe uğursuz oldu"; exit 1; }

echo ""
echo "  ✓ IIB.1 KEÇDİ — statistika modulu tam işləyir"
)
