LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── Node və npm ──"
echo "  node: $(node -v)   npm: $(npm -v)"

echo "── Konfiqurasiya faylları ──"
for f in package.json tsconfig.json tsconfig.build.json nest-cli.json .env .env.example prisma/schema.prisma; do
  [ -f "$f" ] && echo "  ✓ $f" || echo "  ✗ $f YOXDUR"
done

echo "── Əsas paketlər ──"
for p in @nestjs/core @nestjs/common @nestjs/config @prisma/client; do
  v=$(python3 -c "import json;print(json.load(open('node_modules/$p/package.json'))['version'])" 2>/dev/null)
  echo "  $p = ${v:-QURAŞDIRILMAYIB}"
done

echo "── npm skriptləri ──"
python3 -c "import json;[print('  '+k+' → '+v) for k,v in json.load(open('package.json'))['scripts'].items()]"
)
