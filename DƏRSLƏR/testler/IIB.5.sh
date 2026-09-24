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

EPOX=$(date +%s)
P="iib5.${EPOX}"
temizle2() {
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iib5.%@arti.edu.az';" >/dev/null
  true
}
trap temizle2 EXIT INT TERM

echo "  → 1) Toplu faylları"
catmadi=0
for f in src/emekdaslar/toplu/dto/toplu.dto.ts \
         src/emekdaslar/toplu/toplu.service.ts \
         src/emekdaslar/toplu/toplu.controller.ts \
         skriptler/toplu_yoxla.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ fayllar natamamdır — ADDIM 24-ü işlədin"; exit 1; }

echo ""
echo "  → 2) Massiv validasiyası"
D=src/emekdaslar/toplu/dto/toplu.dto.ts
for m in 'ValidateNested' 'ArrayMinSize' 'ArrayMaxSize' 'IsArray' 'Type(() =>'; do
  grep -q "$m" "$D" || { echo "      ✗ $m yoxdur!"; exit 1; }
  printf '      ✓ %s\n' "$m"
done
grep -q 'each: true' "$D" || { echo "      ✗ { each: true } yoxdur — massiv elementləri yoxlanılmayacaq!"; exit 1; }
echo "      ✓ each: true mövcuddur"

echo ""
echo "  → 3) Təhlükəsizlik qaydaları"
S=src/emekdaslar/toplu/toplu.service.ts
grep -q 'Filtrsiz toplu maaş' "$S" || { echo "      ✗ filtrsiz maaş qadağası yoxdur!"; exit 1; }
echo "      ✓ filtrsiz maaş dəyişikliyi qadağandır"
grep -q 'createManyAndReturn' "$S" || { echo "      ✗ createManyAndReturn yoxdur!"; exit 1; }
echo "      ✓ createManyAndReturn işlədilir"
grep -q 'multiply' "$S" || { echo "      ✗ atomik multiply yoxdur!"; exit 1; }
echo "      ✓ atomik multiply işlədilir"
grep -q "Min(-50" "$D" || { echo "      ✗ faiz -50 həddi yoxdur (sıfırlama riski!)"; exit 1; }
echo "      ✓ faiz həddi qorunur (-50)"

echo ""
echo "  → 4) Bazanın vəziyyəti (əvvəl)"
EVVEL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      emekdaş: %s\n' "$EVVEL"

echo ""
echo "  → 5) CANLI toplu əməliyyat yoxlaması"
npx tsx skriptler/toplu_yoxla.ts
[ $? -eq 0 ] || { echo "  ✗ toplu probe uğursuz oldu"; exit 1; }

echo ""
echo "  → 6) Bazanın vəziyyəti (sonra)"
SONRA=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
ZIBIL=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'toplu.%' OR email LIKE 'iib5.%';")
printf '      emekdaş: %s   zibil: %s\n' "$SONRA" "$ZIBIL"
[ "$EVVEL" = "$SONRA" ] || { echo "  ✗ sətir sayı dəyişdi!"; exit 1; }
[ "$ZIBIL" = "0" ] || { echo "  ✗ test zibili qaldı"; exit 1; }
echo "      ✓ baza toxunulmaz qaldı"

echo ""
echo "  ✓ IIB.5 KEÇDİ — toplu əməliyyatlar düzgün işləyir"
)
