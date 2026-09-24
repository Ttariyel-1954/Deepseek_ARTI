LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur: $(pwd)"; exit 1; }
[ -f .env ] || { echo "  ✗ .env yoxdur — DATABASE_URL tapılmır"; exit 1; }
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
[ -n "$DBURL" ] || { echo "  ✗ .env-də DATABASE_URL yoxdur"; exit 1; }
say()  { psql "$DBURL" -At -c "$1" 2>/dev/null | tr -d ' '; }

[ -f src/emekdaslar/emekdaslar.service.ts ] \
  || { echo "  ✗ emekdaslar.service.ts yoxdur — ADDIM 19-u işlədin"; exit 1; }
[ -f skriptler/servis_yoxla.ts ] \
  || { echo "  ✗ skriptler/servis_yoxla.ts yoxdur"; exit 1; }
echo "  ✓ servis və yoxlama skripti yerindədir"

echo ""
echo "  → 1) Servisin strukturu"
printf '      sətir sayı       : %s\n' "$(wc -l < src/emekdaslar/emekdaslar.service.ts | tr -d ' ')"
printf '      ictimai metodlar : %s\n' "$(grep -cE '^  async [a-z]' src/emekdaslar/emekdaslar.service.ts)"
grep -nE '^  async [a-z]' src/emekdaslar/emekdaslar.service.ts | sed 's/^/      /'
for m in hamisi biri yarat yenile sil; do
  grep -qE "^  async $m\(" src/emekdaslar/emekdaslar.service.ts \
    || { echo "  ✗ $m() metodu yoxdur!"; exit 1; }
done
echo "      ✓ beş CRUD metodu mövcuddur"

echo ""
echo "  → 2) Vacib detallar"
grep -q 'BigInt(id)' src/emekdaslar/emekdaslar.service.ts \
  || { echo "      ✗ BigInt(id) çevrilməsi yoxdur!"; exit 1; }
echo "      ✓ id → BigInt(id)"
grep -q '\$transaction' src/emekdaslar/emekdaslar.service.ts \
  || { echo "      ✗ \$transaction işlədilmir!"; exit 1; }
echo "      ✓ \$transaction var (cem + siyahı bir yerdə)"
grep -q "mode: 'insensitive'" src/emekdaslar/emekdaslar.service.ts \
  || { echo "      ✗ hərf böyüklüyünə həssas olmayan axtarış yoxdur!"; exit 1; }
echo "      ✓ axtarış hərf böyüklüyünə həssas deyil"
grep -q 'aktiv: false' src/emekdaslar/emekdaslar.service.ts \
  || { echo "      ✗ yumşaq silmə yoxdur!"; exit 1; }
echo "      ✓ yumşaq silmə (aktiv = false) var"
for kod in P2002 P2003 P2025; do
  grep -q "$kod" src/emekdaslar/emekdaslar.service.ts \
    || { echo "      ✗ $kod çevrilməsi yoxdur!"; exit 1; }
done
echo "      ✓ P2002 / P2003 / P2025 çevrilmələri var"

echo ""
echo "  → 3) Bazanın vəziyyəti (əvvəl)"
EVVEL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      emekdaslar: %s\n' "$EVVEL"

echo ""
echo "  → 4) CANLI servis yoxlaması"
npx tsx skriptler/servis_yoxla.ts
CIXIS=$?
[ "$CIXIS" -eq 0 ] || { echo "  ✗ servis yoxlaması uğursuz oldu"; exit 1; }

echo ""
echo "  → 5) Bazanın vəziyyəti (sonra)"
SONRA=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      emekdaslar: %s\n' "$SONRA"
[ "$EVVEL" = "$SONRA" ] || { echo "  ✗ sətir sayı dəyişdi ($EVVEL → $SONRA) — test zibil buraxdı!"; exit 1; }
echo "      ✓ baza toxunulmaz qaldı"

echo ""
echo "  ✓ IIA.3 KEÇDİ — servis tam işləyir və məlumata zərər vermir"
)
