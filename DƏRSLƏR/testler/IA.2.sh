LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1

echo "── Layihə ──"
python3 -c "
import json
d = json.load(open('package.json'))
print('  ad        :', d['name'])
print('  versiya   :', d['version'])
print('  modul tipi:', d.get('type', 'commonjs'))
"

echo
echo "── Skriptlər ──"
python3 -c "
import json
for k, v in json.load(open('package.json'))['scripts'].items():
    print('  npm run %-14s → %s' % (k, v))
"

echo
echo "── Asılılıqlar ──"
python3 -c "
import json
d = json.load(open('package.json'))
print('  istehsalat (dependencies)   :', len(d.get('dependencies', {})))
print('  inkişaf    (devDependencies):', len(d.get('devDependencies', {})))
"

echo
echo "── Quraşdırılıbmı? ──"
if [ -d node_modules ]; then
  echo "  ✓ node_modules: $(ls node_modules | wc -l | tr -d ' ') paket"
else
  echo "  ✗ node_modules YOXDUR — «npm install» işlədin"
fi
)
