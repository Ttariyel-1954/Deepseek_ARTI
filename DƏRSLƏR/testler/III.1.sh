LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── Auth paketləri ──"
for p in @nestjs/jwt @nestjs/passport passport passport-jwt bcryptjs; do
  v=$(python3 -c "import json;print(json.load(open('node_modules/$p/package.json'))['version'])" 2>/dev/null)
  echo "  %-20s %s" | sed "s/%-20s/$p/" | sed "s/%s/${v:-YOXDUR}/"
done

echo "── JWT ayarları (.env) ──"
for a in JWT_SECRET JWT_MUDDET; do
  d=$(grep "^$a=" .env | sed "s/^$a=//; s/\"//g")
  echo "  $a → ${#d} simvol (dəyər göstərilmir)"
done

echo "── Açar koda hardcode yazılıbmı? ──"
if grep -rn 'JWT_SECRET' src/ --include=*.ts | grep -qv 'configService\|config\.get\|ConfigService'; then
  echo "  ⚠️ koda yazılmış istinad var — yoxlayın"
else
  echo "  ✓ açar yalnız ConfigService ilə oxunur, koda yazılmayıb"
fi

echo "── .env git-ə düşürmü? ──"
grep -q '^\.env$' .gitignore && echo "  ✓ .env .gitignore-dadır" || echo "  ✗ .env git-ə düşə bilər!"
)
