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

echo "  → 1) parol_yoxla.ts — canlı prob (25 yoxlama)"
NETICE=$(npx tsx skriptler/parol_yoxla.ts 2>&1)
printf '%s\n' "$NETICE" | tail -n 4 | awk '{ print "      " $0 }'
KECDI=$(printf '%s' "$NETICE" | grep -oE 'keçdi: [0-9]+' | grep -oE '[0-9]+' | head -1)
UGURSUZ=$(printf '%s' "$NETICE" | grep -oE 'uğursuz: [0-9]+' | grep -oE '[0-9]+' | head -1)
printf '      keçdi=%s uğursuz=%s\n' "${KECDI:-?}" "${UGURSUZ:-?}"
[ "${KECDI:-0}" -ge 25 ] && [ "${UGURSUZ:-1}" = "0" ] \
  || { echo "  ✗ parol probu uğursuz"; exit 1; }

echo ""
echo "  → 2) bcrypt dərəcəsi və duz"
printf '      standart dərəcə : %s (10 olmalıdır)\n' \
  "$(grep -oE 'BCRYPT_DERECE = [0-9]+' src/auth/parol.service.ts | grep -oE '[0-9]+')"
printf '      bcryptjs import : %s\n' "$(grep -c "from 'bcryptjs'" src/auth/parol.service.ts)"
printf '      parolProblemleri: %s\n' "$(grep -c 'parolProblemleri' src/auth/parol.service.ts)"

echo ""
echo "  → 3) QeydiyyatDto validasiya matrisi (class-validator)"
cat > ./iiia2_dto.ts <<'TSEOF'
import { validate } from 'class-validator';
import { plainToInstance } from 'class-transformer';
import { QeydiyyatDto } from './src/auth/dto/qeydiyyat.dto.ts';

const HALLAR: Array<[string, boolean, Record<string, unknown>]> = [
  ['güclü parol', true,
   { email: 'yeni@arti.edu.az', parol: 'GucluParol123!', ad_soyad: 'Test Ad' }],
  ['zəif 123456', false,
   { email: 'yeni@arti.edu.az', parol: '123456', ad_soyad: 'Test Ad' }],
  ['kiçik hərfsiz', false,
   { email: 'yeni@arti.edu.az', parol: 'GUCLUPAROL123!', ad_soyad: 'Test Ad' }],
  ['rəqəmsiz', false,
   { email: 'yeni@arti.edu.az', parol: 'GucluParol!!!', ad_soyad: 'Test Ad' }],
  ['xüsusi simvolsuz', false,
   { email: 'yeni@arti.edu.az', parol: 'GucluParol123', ad_soyad: 'Test Ad' }],
  ['qısa parol', false,
   { email: 'yeni@arti.edu.az', parol: 'Gu1!', ad_soyad: 'Test Ad' }],
  ['e-poçtun hissəsi', false,
   { email: 'yeni@arti.edu.az', parol: 'YeniParol123!', ad_soyad: 'Test Ad' }],
  ['səhv e-poçt', false,
   { email: 'bu-e-poct-deyil', parol: 'GucluParol123!', ad_soyad: 'Test Ad' }],
  ['qısa ad_soyad', false,
   { email: 'yeni@arti.edu.az', parol: 'GucluParol123!', ad_soyad: 'A' }],
];

void (async () => {
  let kecdi = 0;
  let xeta = 0;
  for (const [ad, gozlenilen, x] of HALLAR) {
    const d = plainToInstance(QeydiyyatDto, x);
    const xetalar = await validate(d, { whitelist: true, forbidNonWhitelisted: true });
    const gecti = xetalar.length === 0;
    if (gecti === gozlenilen) {
      kecdi++;
      const mesaj = gecti ? '' : ` → ${Object.values(xetalar[0].constraints ?? {})[0]}`;
      console.log(`      [OK] ${ad.padEnd(20)} ${gecti ? 'qəbul' : 'rədd'}${mesaj}`);
    } else {
      xeta++;
      console.log(`      [XX] ${ad.padEnd(20)} gözlənilirdi ${gozlenilen ? 'qəbul' : 'rədd'}`);
    }
  }

  // ⚠️ ROL İNYEKSİYASI — ən vacib yoxlama
  const d = plainToInstance(QeydiyyatDto, {
    email: 'yeni@arti.edu.az', parol: 'GucluParol123!', ad_soyad: 'Test Ad',
    rol: 'admin',
  });
  const x = await validate(d, { whitelist: true, forbidNonWhitelisted: true });
  const mesajlar = x.flatMap((e) => Object.values(e.constraints ?? {}));
  if (x.length > 0 && mesajlar.some((m) => m.includes('rol'))) {
    kecdi++;
    console.log(`      [OK] ${'rol inyeksiyası'.padEnd(20)} rədd → ${mesajlar[0]}`);
  } else {
    xeta++;
    console.log('      [XX] rol inyeksiyası QƏBUL EDİLDİ — TƏHLÜKƏ!');
  }

  // ⚠️ DTO-nun özündə parol_hash olmamalıdır
  const saheler = Object.keys(plainToInstance(QeydiyyatDto, {}));
  if (!saheler.includes('parol_hash')) {
    kecdi++;
    console.log(`      [OK] ${'DTO sahələri'.padEnd(20)} ${saheler.join(', ')}`);
  } else {
    xeta++;
    console.log('      [XX] DTO-da parol_hash var!');
  }

  console.log(`\n      NƏTİCƏ: keçdi=${kecdi} uğursuz=${xeta}`);
  process.exit(xeta === 0 ? 0 : 1);
})();
TSEOF
if npx tsx ./iiia2_dto.ts >/tmp/iiia2_dto.log 2>&1; then
  awk '{ print "  " $0 }' /tmp/iiia2_dto.log
  echo "      ✓ DTO validasiya matrisi keçdi"
else
  echo "  ✗ DTO validasiya matrisi uğursuz"
  awk '{ print "      " $0 }' /tmp/iiia2_dto.log | tail -n 20
  rm -f ./iiia2_dto.ts; exit 1
fi
rm -f ./iiia2_dto.ts

echo ""
echo "  → 4) DTO-larda «rol» sahəsi YOXDUR (imtiyaz yüksəltmə qapadılıb)"
for f in src/auth/dto/qeydiyyat.dto.ts src/auth/dto/giris.dto.ts; do
  N=$(grep -cE '^\s+rol[!?]?\s*:' "$f" || true)
  printf '      %-34s rol sahəsi: %s (0 olmalıdır)\n' "$f" "$N"
  [ "$N" = "0" ] || { echo "      ✗ İMTİYAZ YÜKSƏLTMƏ RİSKİ!"; exit 1; }
done
printf '      QeydiyyatDto sahələri : %s\n' \
  "$(grep -oE '^\s+[a-z_]+[!?]?:' src/auth/dto/qeydiyyat.dto.ts | tr -d ' :!?' | tr '\n' ' ')"
printf '      GirisDto sahələri     : %s\n' \
  "$(grep -oE '^\s+[a-z_]+[!?]?:' src/auth/dto/giris.dto.ts | tr -d ' :!?' | tr '\n' ' ')"

echo ""
echo "  ✓ IIIA.2 KEÇDİ — parol siyasəti və DTO validasiyası işləyir"
)
