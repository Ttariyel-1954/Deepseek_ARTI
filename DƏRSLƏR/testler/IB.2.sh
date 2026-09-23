LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur — bu qovluq layihə deyil: $(pwd)"; exit 1; }

echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) Təmiz layihədə tip yoxlaması"
if npx tsc --noEmit; then
  echo "      ✓ exit 0 — heç bir tip xətası yoxdur"
else
  echo "      ✗ TİP XƏTASI VAR (yuxarıya baxın)"
  exit 1
fi

echo ""
echo "  → 2) Qəsdən səhv kod yazırıq ki, kompilyator onu tutsun"
cat > src/_ib2_tip.ts <<'SON'
// ⚠️ BU FAYL QƏSDƏN SƏHVDİR — test bitəndə silinəcək.
const say: number = 'metn';
export default say;
SON
printf '      fayl yaradıldı: src/_ib2_tip.ts\n'

CIXIS=$(npx tsc --noEmit 2>&1)
KOD=$?
printf '%s\n' "$CIXIS" | sed 's/^/      /'
printf '      exit kodu: %s (0 OLMAMALIDIR)\n' "$KOD"

rm -f src/_ib2_tip.ts
printf '      müvəqqəti fayl silindi → %s\n' "$([ -f src/_ib2_tip.ts ] && echo 'HƏLƏ DURUR' || echo 'bəli')"

[ "$KOD" -ne 0 ] || { echo "  ✗ tsc səhvi TUTMADI — bu gözlənilməzdir!"; exit 1; }

echo ""
echo "  → 3) xəta DÜZGÜN faylı göstərir?"
printf '%s' "$CIXIS" | grep -q '_ib2_tip.ts' \
  || { echo "  ✗ xəta mesajında fayl adı yoxdur"; exit 1; }
printf '%s' "$CIXIS" | grep -q 'TS2322' \
  || { echo "  ✗ gözlənilən xəta kodu TS2322 deyil"; exit 1; }
echo "      ✓ xəta fayl adı və TS2322 kodu ilə göstərildi"

echo ""
echo "  → 4) Təmizlikdən sonra yenidən yoxlayırıq"
npx tsc --noEmit || { echo "  ✗ müvəqqəti fayl silindikdən sonra yenə xəta var"; exit 1; }
echo "      ✓ exit 0 — layihə təmizdir"

echo ""
echo "  ✓ IB.2 KEÇDİ — tip yoxlaması işləyir və səhvi tutur"
)
