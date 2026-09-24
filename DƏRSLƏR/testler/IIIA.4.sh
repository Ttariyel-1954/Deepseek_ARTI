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

echo "  → 1) JWT_SECRET vəziyyəti (DƏYƏR ÇAP EDİLMİR)"
SR=$(grep '^JWT_SECRET=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
[ -n "$SR" ] || { echo "  ✗ .env-də JWT_SECRET yoxdur"; exit 1; }
printf '      uzunluq        : %s simvol (min 32)\n' "${#SR}"
[ "${#SR}" -ge 32 ] || { echo "  ✗ sirr çox qısadır"; exit 1; }
printf '      sirr növü      : %s\n' "$(printf '%s' "$SR" | grep -qE '^[A-Za-z0-9+/=]+$' && echo 'base64 (openssl rand)' || echo 'qeyri-standart')"
if printf '%s' "$SR" | grep -qiE '^(secret|gizli|arti|test|parol|123456)'; then
  echo "      ✗ TƏHLÜKƏ: sirr zəif sözdür!"; exit 1
fi
echo "      ✓ sirr zəif söz deyil"
printf '      JWT_MUDDET     : %s\n' "$(grep '^JWT_MUDDET=' .env | head -1 | cut -d= -f2- | tr -d '\"')"
printf '      qısaltmalar    : %s\n' \
  "$(grep -oE '\{ s: 1, m: 60, h: 3600, d: 86400 \}' src/auth/token.service.ts | head -1)"

echo ""
echo "  → 2) token_yoxla.ts — canlı prob (35 yoxlama)"
NETICE=$(npx tsx skriptler/token_yoxla.ts 2>&1)
printf '%s\n' "$NETICE" | tail -n 4 | awk '{ print "      " $0 }'
KECDI=$(printf '%s' "$NETICE" | grep -oE 'keçdi: [0-9]+' | grep -oE '[0-9]+' | head -1)
UGURSUZ=$(printf '%s' "$NETICE" | grep -oE 'uğursuz: [0-9]+' | grep -oE '[0-9]+' | head -1)
printf '      keçdi=%s uğursuz=%s\n' "${KECDI:-?}" "${UGURSUZ:-?}"
[ "${KECDI:-0}" -ge 35 ] && [ "${UGURSUZ:-1}" = "0" ] \
  || { echo "  ✗ token servisi probu uğursuz"; exit 1; }

echo ""
echo "  → 3) Tokeni ƏL İLƏ yaradıb açırıq (base64url)"
cat > ./iiia4_tok.ts <<'TSEOF'
import { TokenService } from './src/auth/token.service.ts';

const sirr = 'A'.repeat(48);
const xidmet = new TokenService(null as never, {
  get: (k: string) => (k === 'JWT_SECRET' ? sirr : '1h'),
} as never);

async function yarat(): Promise<string> {
  // ⚠️ `jsonwebtoken`-in YERİNƏ sadə, AMA DÜZGÜN HMAC-SHA256 tətbiqi.
  // Beləliklə tokeni həm yaradırıq, həm də imzasını REAL yoxlayırıq.
  const imzala = async (metn: string, sirr: string, nov: 'base64url' | 'hex') => {
    const { createHmac } = await import('node:crypto');
    return createHmac('sha256', sirr).update(metn).digest(nov) as string;
  };
  const saxtaJwt = {
    signAsync: async (yuk: object, opt: { secret: string; expiresIn: number }) => {
      const h = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
      const iat = Math.floor(Date.now() / 1000);
      const p = Buffer.from(
        JSON.stringify({ ...yuk, iat, exp: iat + opt.expiresIn }),
      ).toString('base64url');
      const s = await imzala(`${h}.${p}`, opt.secret, 'base64url');
      return `${h}.${p}.${s}`;
    },
    verifyAsync: async (token: string, opt: { secret: string }) => {
      const [h, p, s] = token.split('.');
      if (!h || !p || !s) throw new Error('format səhvdir');
      const gozlenilen = await imzala(`${h}.${p}`, opt.secret, 'base64url');
      // ⚠️ SABİT VAXTLI müqayisə — adi `===` «timing attack»-a açıqdır.
      const { timingSafeEqual } = await import('node:crypto');
      const a = Buffer.from(gozlenilen);
      const b = Buffer.from(s);
      if (a.length !== b.length || !timingSafeEqual(a, b)) throw new Error('imza səhvdir');
      const yuk = JSON.parse(Buffer.from(p, 'base64url').toString('utf-8')) as {
        exp?: number;
      };
      if (!yuk.exp || yuk.exp < Math.floor(Date.now() / 1000)) {
        throw new Error('müddət bitib');
      }
      return yuk;
    },
  };
  (xidmet as unknown as { jwt: unknown }).jwt = saxtaJwt;
  return (await xidmet.yarat({
    id: 42, email: 'test@arti.edu.az', ad_soyad: 'Test', rol: 'baxici',
    aktiv: true, emekdas_id: null, yaradilma: new Date(),
  } as never)).access_token;
}

void (async () => {
  const t = await yarat();
  const hisseler = t.split('.');
  console.log(`      hissə sayı      : ${hisseler.length}`);
  const a = xidmet.ac(t);
  console.log(`      header          : ${JSON.stringify(a.header)}`);
  console.log(`      payload         : ${JSON.stringify(a.payload)}`);
  console.log(`      imza uzunluğu   : ${a.imza_uzunlugu} simvol`);
  const s = new Set(Object.keys(a.payload));
  const qadağan = ['parol', 'parol_hash', 'fin', 'maas', 'kart'];
  const sizma = qadağan.filter((q) => [...s].some((k) => k.toLowerCase().includes(q)));
  console.log(`      həssas sahə     : ${sizma.length === 0 ? 'YOXDUR ✓' : 'VAR — ' + sizma.join(',')}`);
  const qalan = xidmet.qalanMuddet(t);
  console.log(`      qalan müddət    : ${qalan} saniyə (gözlənilir ~3600)`);
  const yox = await xidmet.yoxla(t);
  console.log(`      yoxla()         : ${yox ? 'etibarlı ✓' : 'ETİBARSIZ'}`);
  const pozulmus = `${hisseler[0]}.${hisseler[1]}.${'X'.repeat(hisseler[2].length)}`;
  const yox2 = await xidmet.yoxla(pozulmus);
  console.log(`      saxta imza      : ${yox2 ? 'QƏBUL EDİLDİ ✗' : 'rədd edildi ✓'}`);
  const uğurlu =
    hisseler.length === 3 && sizma.length === 0 && !!yox && !yox2 &&
    qalan !== null && qalan > 3500 && qalan <= 3600;
  console.log(`\n      NƏTİCƏ: ${uğurlu ? 'KEÇDİ' : 'UĞURSUZ'}`);
  process.exit(uğurlu ? 0 : 1);
})();
TSEOF
if npx tsx ./iiia4_tok.ts >/tmp/iiia4_tok.log 2>&1; then
  awk '{ print "  " $0 }' /tmp/iiia4_tok.log
  echo "      ✓ token quruluşu təsdiqləndi"
else
  echo "  ✗ token quruluşu yoxlaması uğursuz"
  awk '{ print "      " $0 }' /tmp/iiia4_tok.log | tail -n 20
  rm -f ./iiia4_tok.ts; exit 1
fi
rm -f ./iiia4_tok.ts

echo ""
echo "  → 4) Yoxlama funksiyasının dörd addımı kodda"
for q in "token.split('.').length !== 3" 'verifyAsync' 'typeof y?.sub' 'catch {';
do
  printf '      %-34s : %s\n' "$q" "$(grep -c "$q" src/auth/token.service.ts 2>/dev/null || echo 0)"
done
printf '      token.service.ts sətir sayı     : %s\n' "$(wc -l < src/auth/token.service.ts | tr -d ' ')"
printf '      muddetiSaniyeye() ixrac olunub  : %s\n' "$(grep -c 'export function muddetiSaniyeye' src/auth/token.service.ts)"

echo ""
echo "  ✓ IIIA.4 KEÇDİ — JWT düzgün yaradılır, yoxlanılır və sirr qorunur"
)
