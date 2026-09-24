LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur: $(pwd)"; exit 1; }
[ -f .env ] || { echo "  ✗ .env yoxdur"; exit 1; }
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
[ -n "$DBURL" ] || { echo "  ✗ .env-də DATABASE_URL yoxdur"; exit 1; }
say() { psql "$DBURL" -At -c "$1" 2>/dev/null | tr -d ' '; }

echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) Əlaqələr faylları"
catmadi=0
for f in src/emekdaslar/elaqeler/elaqeler.service.ts \
         src/emekdaslar/elaqeler/elaqeler.controller.ts \
         skriptler/elaqeler_yoxla.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ fayllar natamamdır — ADDIM 23-ü işlədin"; exit 1; }

echo ""
echo "  → 2) Nazik sarğı naxışı (təkrar yoxlamanın qarşısı)"
N=$(grep -cE '^  private async [a-z]+Xam' src/emekdaslar/elaqeler/elaqeler.service.ts || true)
printf '      xam (private) metod sayı: %s\n' "$N"
[ "$N" -ge 6 ] || { echo "      ✗ xam metodlar yoxdur — təkrar yoxlama 6 sorğu artırar!"; exit 1; }
grep -q 'this.doktorantlarXam' src/emekdaslar/elaqeler/elaqeler.service.ts \
  || { echo "      ✗ hamisi() xam metodları çağırmır!"; exit 1; }
echo "      ✓ hamisi() xam versiyaları işlədir"

echo ""
echo "  → 3) _count optimallaşdırması"
grep -q '_count' src/emekdaslar/elaqeler/elaqeler.service.ts \
  || { echo "      ✗ _count istifadə olunmur!"; exit 1; }
grep -q 'Promise.all' src/emekdaslar/elaqeler/elaqeler.service.ts \
  || { echo "      ✗ Promise.all yoxdur!"; exit 1; }
echo "      ✓ _count və Promise.all mövcuddur"

echo ""
echo "  → 4) Əlaqəli cədvəllərdə məlumat"
for c in "elm.doktorantlar" "tehsil.sertifikasiya" "kadrlar.mezuniyyetler" \
         "kadrlar.is_tecrubesi" "elm.tedqiqat_layiheleri" "struktur.elmi_shura_uzvleri"; do
  N=$(say "SELECT count(*) FROM $c;")
  printf '      %-30s %s\n' "$c" "$N"
  [ "$N" -ge 1 ] || { echo "      ✗ $c boşdur"; exit 1; }
done

echo ""
echo "  → 5) CANLI ölçmə (sorğu sayğacı ilə)"
npx tsx skriptler/elaqeler_yoxla.ts
[ $? -eq 0 ] || { echo "  ✗ əlaqələr probe uğursuz oldu"; exit 1; }

echo ""
echo "  ✓ IIB.3 KEÇDİ — sorğu sayı ölçüldü və optimallaşdırma təsdiqləndi"
)
