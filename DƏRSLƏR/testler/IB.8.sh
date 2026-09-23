LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur — bu qovluq layihə deyil: $(pwd)"; exit 1; }

echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) Konfiqurasiya faylları varmı?"
catmadi=0
for f in vitest.config.ts vitest.config.e2e.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ konfiqurasiya faylları natamamdır"; exit 1; }

echo ""
echo "  → 2) Vitest qurulubmu?"
V=$(npx vitest --version 2>&1 | tail -n 1)
printf '      %s\n' "$V"
printf '%s' "$V" | grep -q 'vitest/' || { echo "  ✗ vitest işləmir"; exit 1; }

echo ""
echo "  → 3) package.json skriptləri"
for s in test test:unit test:izle test:e2e; do
  D=$(npm pkg get "scripts.$s" 2>/dev/null)
  printf '      %-12s → %s\n' "$s" "$D"
  [ "$D" = '{}' ] && { echo "  ✗ '$s' skripti yoxdur"; exit 1; }
done
npm pkg get "scripts.test:e2e" 2>/dev/null | grep -q 'vitest.config.e2e.ts' \
  || { echo "  ✗ test:e2e skripti e2e konfiqurasiyasına işarə etmir"; exit 1; }
echo "      ✓ bütün dörd skript mövcuddur və düzgün əmrlərə işarə edir"

echo ""
echo "  → 4) Vahid konfiqurasiyası hansı testləri görür?"
ULIST=$(npx vitest list --config vitest.config.ts 2>&1)
USAY=$(printf '%s\n' "$ULIST" | grep -c . )
printf '%s\n' "$ULIST" | sed 's/^/      /'
printf '      cəmi: %s test\n' "$USAY"

echo ""
echo "  → 5) E2E konfiqurasiyası hansı testləri görür?"
ELIST=$(npx vitest list --config vitest.config.e2e.ts 2>&1)
ESAY=$(printf '%s\n' "$ELIST" | grep -c . )
printf '%s\n' "$ELIST" | sed 's/^/      /'
printf '      cəmi: %s test\n' "$ESAY"

echo ""
echo "  → 6) Ayrı-seçkilik yoxlaması"
printf '%s' "$ULIST" | grep -q 'e2e-spec' && { echo "      ✗ e2e testlər vahid dəstinə SIZIB!"; exit 1; }
echo "      ✓ vahid dəstində e2e test yoxdur"
printf '%s' "$ELIST" | grep -q 'service.spec' && { echo "      ✗ vahid testlər e2e dəstinə SIZIB!"; exit 1; }
echo "      ✓ e2e dəstində vahid test yoxdur"
printf '%s' "$ULIST" | grep -q 'vitest.saltsiz' && { echo "      ✗ müvəqqəti konfiqurasiya qalıb"; exit 1; }

[ "$USAY" -eq 3 ] || { echo "      ✗ vahid dəstində 3 test gözlənilirdi, alındı: $USAY"; exit 1; }
[ "$ESAY" -eq 4 ] || { echo "      ✗ e2e dəstində 4 test gözlənilirdi, alındı: $ESAY"; exit 1; }
echo "      ✓ vahid dəst: 3 test — e2e dəst: 4 test"

echo ""
echo "  → 7) Konfiqurasiya fayllarının vacib ayarları"
grep -q "include: \['src/\*\*/\*.spec.ts'\]" vitest.config.ts \
  || { echo "      ✗ vahid include ayarı gözlənilən deyil"; exit 1; }
echo "      ✓ vahid include: src/**/*.spec.ts"
grep -q 'fileParallelism: false' vitest.config.e2e.ts \
  || { echo "      ✗ e2e konfiqurasiyasında fileParallelism: false yoxdur"; exit 1; }
echo "      ✓ e2e fileParallelism: false (ardıcıl işləyir)"
grep -q 'testTimeout: 30_000' vitest.config.e2e.ts \
  || { echo "      ✗ e2e testTimeout ayarı yoxdur"; exit 1; }
echo "      ✓ e2e testTimeout: 30 saniyə"

echo ""
echo "  ✓ IB.8 KEÇDİ — iki konfiqurasiya düzgün ayrılıb"
)
