LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur — bu qovluq layihə deyil: $(pwd)"; exit 1; }

echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) Köhnə dist/ qovluğunu silirik (sıfırdan build yoxlaması)"
rm -rf dist
printf '      dist/ əvvəlcə → %s\n' "$([ -d dist ] && echo 'VAR' || echo 'yoxdur (silindi)')"

echo ""
echo "  → 2) npm run build"
npm run build
KOD=$?
printf '      exit kodu: %s\n' "$KOD"
[ "$KOD" -eq 0 ] || { echo "  ✗ BUILD UĞURSUZ — xəta mesajına baxın"; exit 1; }

echo ""
echo "  → 3) dist/ içində nə var?"
ls dist | sed 's/^/      /'

echo ""
echo "  → 4) vacib fayllar yerindədirmi?"
catmadi=0
for f in dist/main.js dist/app.module.js dist/prisma/prisma.service.js \
         dist/prisma/prisma.module.js \
         dist/saglamliq/saglamliq.service.js \
         dist/saglamliq/saglamliq.controller.js \
         dist/saglamliq/saglamliq.module.js \
         dist/common/filters/all-exceptions.filter.js \
         dist/generated/prisma/client.js; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ build nəticəsi natamamdır"; exit 1; }

echo ""
printf '  → cəmi .js fayl: %s\n' "$(find dist -name '*.js' | wc -l | tr -d ' ')"
printf '  → dist/main.js ölçüsü: %s bayt\n' "$(wc -c < dist/main.js | tr -d ' ')"

echo ""
echo "  ✓ IB.1 KEÇDİ — build sıfırdan işləyir və dist/main.js yaranır"
)
