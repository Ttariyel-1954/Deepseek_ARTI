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

[ -f src/emekdaslar/dto/emekdas-cavab.dto.ts ] \
  || { echo "  ✗ emekdas-cavab.dto.ts yoxdur — ADDIM 18-i işlədin"; exit 1; }
[ -f skriptler/mapper_yoxla.ts ] \
  || { echo "  ✗ skriptler/mapper_yoxla.ts yoxdur"; exit 1; }
echo "  ✓ mapper faylları yerindədir"

echo ""
echo "  → 1) Mapper-in vacib hissələri"
grep -q 'String(e.id)' src/emekdaslar/dto/emekdas-cavab.dto.ts \
  || { echo "      ✗ id BigInt-dən mətnə çevrilmir!"; exit 1; }
echo "      ✓ id → String()"
grep -q 'toFixed(2)' src/emekdaslar/dto/emekdas-cavab.dto.ts \
  || { echo "      ✗ maas toFixed(2) ilə formatlanmır!"; exit 1; }
echo "      ✓ maas → toFixed(2)"
grep -q 'slice(0, 10)' src/emekdaslar/dto/emekdas-cavab.dto.ts \
  || { echo "      ✗ tarixlər yalnız günə kəsilmir!"; exit 1; }
echo "      ✓ tarixlər → YYYY-MM-DD"
grep -q 'as const' src/emekdaslar/dto/emekdas-cavab.dto.ts \
  || { echo "      ✗ EMEKDAS_SECIM-də as const yoxdur!"; exit 1; }
echo "      ✓ select sabiti as const ilə"

echo ""
echo "  → 2) select (include yox) işlədilir?"
N=$(grep -c 'select: EMEKDAS_SECIM' src/emekdaslar/emekdaslar.service.ts || true)
printf '      select: EMEKDAS_SECIM → %s yerdə
' "$N"
[ "$N" -ge 4 ] || { echo "      ✗ servis select işlətmir (include ola bilər)!"; exit 1; }
grep -q 'include:' src/emekdaslar/emekdaslar.service.ts \
  && { echo "      ✗ servisdə include istifadə olunur — select gözlənilirdi!"; exit 1; }
echo "      ✓ yalnız select işlədilir (include yox)"

echo ""
echo "  → 3) CANLI sübut: problem və həll yan-yana"
npx tsx skriptler/mapper_yoxla.ts
CIXIS=$?
[ "$CIXIS" -eq 0 ] || { echo "  ✗ mapper skripti uğursuz oldu"; exit 1; }

echo ""
echo "  → 4) Bazadaki real sütun tipləri"
psql "$DBURL" -At -c "
SELECT '      ' || column_name || ' → ' || data_type
  FROM information_schema.columns
 WHERE table_schema='kadrlar' AND table_name='emekdaslar'
   AND column_name IN ('id','maas','dogum_tarixi','yaradilma')
 ORDER BY ordinal_position;" 2>/dev/null

echo ""
echo "  ✓ IIA.2 KEÇDİ — BigInt/Decimal problemi həll olunub"
)
