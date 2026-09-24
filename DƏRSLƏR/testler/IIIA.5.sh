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

echo "  → 1) qoruyucu_yoxla.ts — canlı prob (26 yoxlama)"
NETICE=$(npx tsx skriptler/qoruyucu_yoxla.ts 2>&1)
printf '%s\n' "$NETICE" | tail -n 4 | awk '{ print "      " $0 }'
KECDI=$(printf '%s' "$NETICE" | grep -oE 'keçdi: [0-9]+' | grep -oE '[0-9]+' | head -1)
UGURSUZ=$(printf '%s' "$NETICE" | grep -oE 'uğursuz: [0-9]+' | grep -oE '[0-9]+' | head -1)
printf '      keçdi=%s uğursuz=%s\n' "${KECDI:-?}" "${UGURSUZ:-?}"
[ "${KECDI:-0}" -ge 26 ] && [ "${UGURSUZ:-1}" = "0" ] \
  || { echo "  ✗ qoruyucu probu uğursuz"; exit 1; }

echo ""
echo "  → 2) Guard sırası (ƏN VACİB yoxlama)"
SIRA=$(grep -oE '@UseGuards\([^)]*\)' src/auth/auth.controller.ts | head -1)
printf '      controller-də    : %s\n' "$SIRA"
case "$SIRA" in
  *'AuthGuard, RollerGuard'*) echo "      ✓ sıra düzgündür (əvvəlcə kim, sonra icazə)" ;;
  *) echo "      ✗ SIRA SƏHVDİR — 403 yerinə 401 gələcək"; exit 1 ;;
esac

echo ""
echo "  → 3) Guard faylları və ixrac olunan simvollar"
for f in src/auth/qoruyucu/auth.guard.ts src/auth/qoruyucu/roller.guard.ts; do
  printf '      %-44s %4s sətir\n' "$f" "$(wc -l < "$f" | tr -d ' ')"
done
for s in 'export class AuthGuard' 'export class RollerGuard' \
         'export const Ictimai' 'export const Roller' 'export const CariIstifadeci' \
         'export function cariIstifadeciFabriki'; do
  N=$(grep -rl "$s" src/auth/qoruyucu/ 2>/dev/null | wc -l | tr -d ' ')
  [ "$N" -ge 1 ] && printf '      ✓ %s\n' "$s" || { printf '      ✗ %s TAPILMADI\n' "$s"; exit 1; }
done

echo ""
echo "  → 4) 401 / 403 ayrımı kodda"
printf '      UnauthorizedException (401) : %s yer\n' \
  "$(grep -c 'UnauthorizedException' src/auth/qoruyucu/auth.guard.ts) (auth.guard)"
printf '      ForbiddenException    (403) : %s yer (roller.guard)\n' \
  "$(grep -c 'ForbiddenException' src/auth/qoruyucu/roller.guard.ts)"
if grep -q 'ForbiddenException' src/auth/qoruyucu/auth.guard.ts; then
  echo "      ⚠️ auth.guard-da 403 var — orada YALNIZ 401 olmalıdır"
fi
printf '      rol tələb olunmayanda keçir : %s\n' \
  "$(grep -c 'teleb.length === 0) return true' src/auth/qoruyucu/roller.guard.ts)"
printf '      nəticə sorğuya yazılır      : %s\n' \
  "$(grep -c 'sorgu.istifadeci = yuk' src/auth/qoruyucu/auth.guard.ts)"

echo ""
echo "  → 5) @Ictimai() işarələri — açıq endpoint-lər"
printf '      @Ictimai() sayı  : %s\n' "$(grep -c '@Ictimai()' src/auth/auth.controller.ts)"
printf '      @Roller(...) sayı: %s\n' "$(grep -c '@Roller(' src/auth/auth.controller.ts)"
grep -nE '@(Get|Post|Patch)\(' src/auth/auth.controller.ts | awk '{ print "      " $0 }'

echo ""
echo "  → 6) cariIstifadeciFabriki AYRICA test edilə bilir"
grep -n 'createParamDecorator(cariIstifadeciFabriki)' src/auth/qoruyucu/cari-istifadeci.dekorator.ts | awk '{ print "      " $0 }'
printf '      niyə vacibdir: dekoratorun özü test edilə bilmir,\n'
printf '      fabrik funksiyası isə birbaşa çağırıla bilir (4 yoxlama)\n'

echo ""
echo "  ✓ IIIA.5 KEÇDİ — qoruyucular düzgün yazılıb və qoşulub"
)
