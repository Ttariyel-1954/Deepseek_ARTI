LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur — bu qovluq layihə deyil: $(pwd)"; exit 1; }

[ -f src/saglamliq/saglamliq.service.spec.ts ] \
  || { echo "  ✗ src/saglamliq/saglamliq.service.spec.ts yoxdur — ADDIM 15-i işlədin"; exit 1; }
echo "  ✓ test faylı yerindədir"

echo ""
echo "  → 1) Vahid testləri işlədirik"
CIXIS=$(npx vitest run 2>&1)
KOD=$?
printf '%s\n' "$CIXIS" | tail -n 12 | sed 's/^/      /'
printf '      exit kodu: %s\n' "$KOD"
[ "$KOD" -eq 0 ] || { echo "  ✗ vahid testlər UĞURSUZ oldu"; exit 1; }

echo ""
echo "  → 2) Nəticənin dəqiq yoxlanması"
printf '%s' "$CIXIS" | grep -q 'Tests  3 passed' \
  || { echo "      ✗ 'Tests 3 passed' gözlənilirdi"; exit 1; }
echo "      ✓ 3 test keçdi"
printf '%s' "$CIXIS" | grep -q 'Test Files  1 passed' \
  || { echo "      ✗ 'Test Files 1 passed' gözlənilirdi"; exit 1; }
echo "      ✓ 1 test faylı işlədi (yalnız vahid faylı)"
printf '%s' "$CIXIS" | grep -q 'e2e-spec' \
  && { echo "      ✗ e2e testlər də işlədi — konfiqurasiya səhvdir"; exit 1; }
echo "      ✓ e2e testlər qarışmadı"

echo ""
echo "  → 3) Üç testin adı çıxışda görünürmü?"
VERBOSE=$(npx vitest run --reporter=verbose 2>&1)
printf '%s\n' "$VERBOSE" | grep '✓' | sed 's/^/      /'
SATIR=$(printf '%s\n' "$VERBOSE" | grep -c '✓ src/saglamliq')
[ "$SATIR" -ge 3 ] || { echo "      ✗ 3 test adı gözlənilirdi, tapıldı: $SATIR"; exit 1; }
echo "      ✓ hər üç test adı ilə görünür"

echo ""
echo "  → 4) SÜBUT: vahid testlər BAZADAN ASILI DEYİL"
echo "      DATABASE_URL-i qəsdən mövcud olmayan bazaya yönləndiririk"
echo "      (localhost:9999 — orada heç nə yoxdur)"
CIXIS2=$(env -u DATABASE_URL -u PGHOST \
  DATABASE_URL="postgresql://yoxdur:yoxdur@localhost:9999/yoxdur" \
  npx vitest run 2>&1)
KOD2=$?
printf '%s\n' "$CIXIS2" | tail -n 8 | sed 's/^/      /'
printf '      exit kodu: %s\n' "$KOD2"
[ "$KOD2" -eq 0 ] || { echo "  ✗ vahid testlər bazadan ASILIDIR — təcrid pozulub!"; exit 1; }
printf '%s' "$CIXIS2" | grep -q 'Tests  3 passed' \
  || { echo "      ✗ bazasız halda 3 test keçmədi"; exit 1; }
echo "      ✓ bazasız halda da 3/3 keçdi — saxta PrismaService işləyir"

echo ""
echo "  → 5) Test təmizliyi: müvəqqəti fayllar qalmayıb?"
for f in src/saglamliq/_muveqqeti.spec.ts src/_ib2_tip.ts src/_tip_yoxlamasi.ts; do
  [ -f "$f" ] && { echo "      ✗ $f QALIB"; exit 1; }
done
echo "      ✓ müvəqqəti fayl yoxdur"

echo ""
echo "  ✓ IB.9 KEÇDİ — vahid testlər keçir və bazadan asılı deyil"
)
