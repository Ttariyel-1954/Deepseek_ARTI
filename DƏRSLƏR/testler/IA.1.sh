LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || {
  echo "⚠️ Layihə qovluğu tapılmadı."; exit 1; }

echo "── Alətlər ──"
echo "  node  : $(node -v)"
echo "  npm   : $(npm -v)"

echo
echo "── Konfiqurasiya faylları ──"
for f in package.json tsconfig.json tsconfig.build.json nest-cli.json \
         .env .gitignore prisma/schema.prisma prisma.config.ts; do
  if [ -f "$f" ]; then
    printf '  ✓ %-26s %4s sətir\n' "$f" "$(wc -l < "$f" | tr -d ' ')"
  else
    printf '  ✗ %-26s YOXDUR\n' "$f"
  fi
done

echo
echo "── Qovluq strukturu ──"
find . -type f -not -path './node_modules/*' -not -path './src/generated/*' \
       -not -path './dist/*' | sort | sed 's/^/  /'
)
