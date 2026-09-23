LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── Sxemanın əsas blokları ──"
grep -nE '^(generator|datasource)|^  (provider|output|url|schemas)' prisma/schema.prisma

echo "── Sxemada nə qədər model var? ──"
echo "  model sayı: $(grep -c '^model ' prisma/schema.prisma)"

echo "── Neçə PostgreSQL sxemi oxunub? ──"
grep -o '"[a-z]*"' prisma/schema.prisma | head -1 >/dev/null
python3 - <<'PY'
import re, pathlib
s = pathlib.Path('prisma/schema.prisma').read_text(encoding='utf-8')
m = re.search(r'schemas\s*=\s*\[(.*?)\]', s, re.S)
adlar = re.findall(r'"([^"]+)"', m.group(1)) if m else []
print('  sxem sayı:', len(adlar))
print('  ', ', '.join(adlar))
PY

echo "── Generasiya olunmuş klient ──"
[ -f src/generated/prisma/client.ts ] && echo "  ✓ src/generated/prisma/client.ts" \
  || echo "  ✗ klient generasiya olunmayıb — «npx prisma generate» lazımdır"

echo "── Sxemanın etibarlılığı ──"
npx prisma validate 2>&1 | tail -2
)
