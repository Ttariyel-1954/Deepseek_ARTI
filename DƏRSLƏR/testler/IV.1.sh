LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── Paketlər ──"
for p in exceljs; do
  v=$(python3 -c "import json;print(json.load(open('node_modules/$p/package.json'))['version'])" 2>/dev/null)
  echo "  $p = ${v:-QURAŞDIRILMAYIB}"
done
python3 -c "
import json
d = json.load(open('package.json'))['dependencies']
print('  package.json-da exceljs:', d.get('exceljs', 'YOXDUR'))"

echo "── .env dəyişənləri ──"
for a in DEEPSEEK_API_KEY DEEPSEEK_MODEL DEEPSEEK_URL; do
  d=$(grep "^$a=" .env | sed "s/^$a=//; s/\"//g")
  if [ "$a" = "DEEPSEEK_API_KEY" ]; then
    echo "  $a → ${#d} simvol $([ -z "$d" ] && echo '(BOŞ → demo rejim)')"
  else
    echo "  $a → $d"
  fi
done

echo "── Demo rejim koda necə bağlanıb? ──"
grep -n 'demoRejim\|API_KEY' src/ai/deepseek.service.ts | head -5 | sed 's/^/  /'
)
