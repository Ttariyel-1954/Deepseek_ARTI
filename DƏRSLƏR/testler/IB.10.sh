LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur — bu qovluq layihə deyil: $(pwd)"; exit 1; }

[ -f test/saglamliq.e2e-spec.ts ] \
  || { echo "  ✗ test/saglamliq.e2e-spec.ts yoxdur — ADDIM 16-nı işlədin"; exit 1; }
echo "  ✓ e2e test faylı yerindədir"

echo ""
echo "  → 1) E2E testləri işlədirik (npm run test:e2e)"
CIXIS=$(npm run test:e2e 2>&1)
KOD=$?
printf '%s\n' "$CIXIS" | tail -n 14 | sed 's/^/      /'
printf '      exit kodu: %s\n' "$KOD"
[ "$KOD" -eq 0 ] || { echo "  ✗ e2e testlər UĞURSUZ oldu (baza işləyirmi?)"; exit 1; }

echo ""
echo "  → 2) Nəticənin dəqiq yoxlanması"
printf '%s' "$CIXIS" | grep -q 'Tests  4 passed' \
  || { echo "      ✗ 'Tests 4 passed' gözlənilirdi"; exit 1; }
echo "      ✓ 4 test keçdi"
printf '%s' "$CIXIS" | grep -q 'Test Files  1 passed' \
  || { echo "      ✗ 'Test Files 1 passed' gözlənilirdi"; exit 1; }
echo "      ✓ 1 e2e faylı işlədi"

echo ""
echo "  → 3) Dörd testin adı (verbose)"
VERBOSE=$(npx vitest run --config vitest.config.e2e.ts --reporter=verbose 2>&1)
printf '%s\n' "$VERBOSE" | grep '✓' | sed 's/^/      /'
SATIR=$(printf '%s\n' "$VERBOSE" | grep -c '✓ test/saglamliq.e2e-spec.ts')
[ "$SATIR" -ge 4 ] || { echo "      ✗ 4 test adı gözlənilirdi, tapıldı: $SATIR"; exit 1; }
echo "      ✓ hər dörd test adı ilə görünür"

echo ""
echo "  → 4) SÜBUT: e2e testlər BAZADAN ASILIDIR"
echo "      DATABASE_URL-i qəsdən mövcud olmayan bazaya yönləndiririk."
echo "      Vahid testlər bu halda KEÇİRDİ (IB.9) — indi KEÇMƏMƏLİDİR:"
CIXIS2=$(env -u DATABASE_URL -u PGHOST \
  DATABASE_URL="postgresql://yoxdur:yoxdur@localhost:9999/yoxdur" \
  npx vitest run --config vitest.config.e2e.ts 2>&1)
KOD2=$?
printf '%s\n' "$CIXIS2" | tail -n 10 | sed 's/^/      /'
printf '      exit kodu: %s (0 OLMAMALIDIR)\n' "$KOD2"
[ "$KOD2" -ne 0 ] || { echo "  ✗ e2e testlər bazasız KEÇDİ — bu mümkün deyil!"; exit 1; }
printf '%s' "$CIXIS2" | grep -q 'failed' \
  || { echo "      ✗ uğursuzluq hesabatı gözlənilirdi"; exit 1; }
printf '%s' "$CIXIS2" | grep -q '3 passed' \
  || { echo "      ✗ digər 3 test keçməli idi (onlar bazaya toxunmur)"; exit 1; }
echo "      ✓ bazasız halda 1 test uğursuz oldu, 3-ü keçdi — gözlənilən nəticə"

echo ""
echo "  → 5) Test faylları build-ə düşürmü?"
npm run build >/dev/null 2>&1 || { echo "  ✗ build uğursuz"; exit 1; }
SAY=$(find dist -name '*spec*' | wc -l | tr -d ' ')
printf '      dist içində *spec* fayl sayı: %s\n' "$SAY"
[ "$SAY" -eq 0 ] || { echo "  ✗ testlər dist-ə düşüb!"; exit 1; }
echo "      ✓ heç bir test faylı build-ə düşməyib"

echo ""
echo "  → 6) YEKUN: hər şey bir yerdə"
printf '      tip yoxlaması: '
npx tsc --noEmit && echo "✓ təmiz"
printf '      vahid testlər: '
npx vitest run 2>&1 | grep 'Tests ' | sed 's/^ *//'
printf '      e2e testlər:   '
npx vitest run --config vitest.config.e2e.ts 2>&1 | grep 'Tests ' | sed 's/^ *//'

echo ""
echo "  ✓ IB.10 KEÇDİ — e2e testlər bütöv sistemi yoxlayır"
)
