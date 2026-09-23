LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1

echo "── Fayl ──"
ls -l src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'

echo
echo "── Status → kod xəritəsi ──"
grep -E '^  [0-9]{3}:' src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'

echo
echo "── Cavabın quruluşu (koddan) ──"
grep -A9 'cavab.status(status).json' src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'

echo
echo "── Gözlənilməz xəta loqa yazılırmı? ──"
grep -n 'log.error' src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'

echo
echo "── Filter qlobal qoşulubmu? ──"
grep -n 'useGlobalFilters' src/main.ts 2>/dev/null | sed 's/^/  /' \
  || echo "  (main.ts hələ yoxdur — IA.10-a baxın)"
)
