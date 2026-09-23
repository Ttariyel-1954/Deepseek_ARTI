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
echo "  (yalnız NİSBİ importlar: './' və ya '../' ilə başlayanlar."
echo "   Paket importlarında — @nestjs/common, supertest — .js YAZILMIR."
echo "   Prisma-nın yaratdığı src/generated/ qovluğu sayılmır.)"
python3 - <<'PSON'
import pathlib
import re
import sys

say = 0
problem = []
for fayl in sorted(pathlib.Path('src').rglob('*.ts')):
    if 'generated' in fayl.parts:
        continue
    for n, setir in enumerate(fayl.read_text(encoding='utf-8').splitlines(), 1):
        s = setir.strip()
        if not (s.startswith('import') or s.startswith('export')):
            continue
        if s.startswith('//') or s.startswith('*') or s.startswith('/*'):
            continue
        for tam in re.findall(r"from\s+'\.[^']*'", s):
            yol = tam[len('from '):].strip().strip("'")
            if yol.endswith('.js'):
                say += 1
            else:
                problem.append('%s:%d → %s' % (fayl, n, yol))

print('  .js ilə     : %d' % say)
print('  .js OLMADAN : %d   ← 0 olmalıdır' % len(problem))
for x in problem:
    print('      ✗ ' + x)
if problem:
    print('  ✗ NİSBİ importda .js uzantısı ÇATIŞMIR!')
    sys.exit(1)
print('  ✓ bütün nisbi importlarda .js uzantısı var')
PSON
)
