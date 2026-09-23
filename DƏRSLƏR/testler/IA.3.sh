LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1

echo "── TypeScript-in gördüyü YEKUN ayarlar ──"
npx tsc --showConfig 2>/dev/null | python3 -c "
import json, sys
o = json.load(sys.stdin)['compilerOptions']
for a in ['target', 'module', 'moduleResolution', 'strict',
          'experimentalDecorators', 'emitDecoratorMetadata',
          'outDir', 'rootDir', 'esModuleInterop']:
    print('  %-24s %s' % (a, o.get(a, '—')))
"

echo
echo "── NestJS ayarları ──"
python3 -c "
import json
d = json.load(open('nest-cli.json'))
c = d.get('compilerOptions', {})
print('  sourceRoot   :', d.get('sourceRoot'))
print('  deleteOutDir :', c.get('deleteOutDir'))
"

echo
echo "── Import-larda «.js» uzantısı varmı? ──"
say=$(grep -rhoE "from '\.[^']*\.js'" src/ 2>/dev/null | wc -l | tr -d ' ')
yox=$(grep -rhoE "from '\.[^']*'" src/ 2>/dev/null | grep -vc '\.js' | tr -d ' ')
echo "  .js ilə     : $say"
echo "  .js OLMADAN : $yox   ← 0 olmalıdır"
[ "$yox" = "0" ] && echo "  ✓ qayda gözlənilir" || echo "  ✗ uzantısız import var!"
)
