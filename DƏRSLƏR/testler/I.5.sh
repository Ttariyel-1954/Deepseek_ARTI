LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

echo "── 1) Build ──"
npm run build 2>&1 | tail -2
echo "  dist/ qovluğu: $([ -f dist/main.js ] && echo '✓ dist/main.js var' || echo '✗ YOXDUR')"

echo "── 2) Tip yoxlaması (build-in gizlətdiyi xətaları tutur) ──"
npx tsc --noEmit -p tsconfig.build.json && echo "  ✓ tip yoxlaması keçdi"

echo "── 3) Unit testlər ──"
npm test 2>&1 | grep -E 'Test Files|Tests ' | sed 's/^/  /'
)
