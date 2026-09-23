LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

echo "── Sxemanın əsas blokları ──"
grep -nE '^(generator|datasource)|^  (provider|output|url|schemas)' \
  prisma/schema.prisma | head -8 | sed 's/^/  /'

echo
echo "── Bazadan nə oxundu? ──"
echo "  model sayı : $(grep -c '^model ' prisma/schema.prisma)"
echo "  @@schema    : $(grep -c '@@schema' prisma/schema.prisma)"
echo "  sətir sayı : $(wc -l < prisma/schema.prisma | tr -d ' ')"

echo
echo "── İlk model nümunə ──"
sed -n '/^model merkezler /,/^}/p' prisma/schema.prisma | head -12 | sed 's/^/  /'

echo
echo "── Sxema etibarlıdırmı? ──"
npx prisma validate 2>&1 | tail -2 | sed 's/^/  /'

echo
echo "── Yaradılan TypeScript klienti ──"
if [ -f src/generated/prisma/client.ts ]; then
  echo "  ✓ client.ts var ($(ls src/generated/prisma | wc -l | tr -d ' ') fayl)"
else
  echo "  ✗ client.ts YOXDUR — «npx prisma generate» işlədin"
fi
)
