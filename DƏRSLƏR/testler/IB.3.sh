LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur — bu qovluq layihə deyil: $(pwd)"; exit 1; }

echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) Təzə build"
npm run build >/dev/null 2>&1 || { echo "  ✗ build uğursuz oldu"; exit 1; }
echo "      ✓ build tamamlandı"

echo ""
echo "  → 2) Gözlənilən fayllar (rootDir düzgün işləyirmi?)"
catmadi=0
for f in dist/main.js dist/app.module.js \
         dist/prisma/prisma.service.js dist/prisma/prisma.module.js \
         dist/saglamliq/saglamliq.service.js \
         dist/saglamliq/saglamliq.controller.js \
         dist/saglamliq/saglamliq.module.js \
         dist/common/filters/all-exceptions.filter.js; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ dist strukturu natamamdır"; exit 1; }

echo ""
echo "  → 3) YANLIŞ yol olmamalıdır: dist/src/main.js"
if [ -f dist/src/main.js ]; then
  echo "      ✗ dist/src/main.js VAR — rootDir işləmir!"
  exit 1
fi
echo "      ✓ dist/src/main.js yoxdur (rootDir düzgündür)"

echo ""
echo "  → 4) Test faylları dist-ə DÜŞMƏMƏLİDİR"
SAY=$(find dist -name '*spec*' | wc -l | tr -d ' ')
find dist -name '*spec*' | sed 's/^/      /'
printf '      tapılan *spec* fayl sayı: %s\n' "$SAY"
[ "$SAY" -eq 0 ] || { echo "  ✗ testlər build-ə düşüb — exclude işləmir!"; exit 1; }
echo "      ✓ heç bir test faylı dist-ə düşməyib"

echo ""
echo "  → 5) deleteOutDir yoxlaması"
mkdir -p dist
echo "kohne" > dist/kohne_fayl.js
printf '      dist/kohne_fayl.js (build-dən əvvəl) → %s\n' "$([ -f dist/kohne_fayl.js ] && echo VAR || echo yoxdur)"
npm run build >/dev/null 2>&1
printf '      dist/kohne_fayl.js (build-dən sonra) → %s\n' "$([ -f dist/kohne_fayl.js ] && echo 'HƏLƏ DURUR' || echo silindi)"
[ -f dist/kohne_fayl.js ] && { echo "  ✗ deleteOutDir işləmədi"; exit 1; }
echo "      ✓ saxta köhnə fayl build zamanı silindi"

echo ""
echo "  ✓ IB.3 KEÇDİ — dist strukturu və deleteOutDir düzgündür"
)
