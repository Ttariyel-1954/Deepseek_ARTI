LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1

echo "── Modulun tam məzmunu ──"
cat -n src/prisma/prisma.module.ts | sed 's/^/  /'

echo
echo "── Yoxlamalar ──"
for yox in '@Global()' 'providers' 'exports'; do
  n=$(grep -c "$yox" src/prisma/prisma.module.ts)
  [ "$n" -gt 0 ] && printf '  ✓ %-12s var\n' "$yox" || printf '  ✗ %-12s YOXDUR\n' "$yox"
done

echo
echo "── Başqa modul PrismaService-i istəyirmi? ──"
grep -rn 'PrismaService' src/ --include=*.service.ts | grep constructor | sed 's/^/  /'

echo
echo "── Kök modula qoşulubmu? ──"
if [ -f src/app.module.ts ]; then
  grep -n 'PrismaModule' src/app.module.ts | sed 's/^/  /'
else
  echo "  (app.module.ts hələ yoxdur — IA.9-a baxın)"
fi
)
