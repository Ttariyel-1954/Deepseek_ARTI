#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-3A — 10 yekun test (IIIA.1 … IIIA.10).

Hər test müstəqildir. Testlər `LAYIHE` mühit dəyişənini oxuyur
(standart: $HOME/Deepseek_ARTI/DS_Backend) və canlı testlər öz
serverlərini özləri qaldırıb söndürürlər.

⚠️ TƏHLÜKƏSİZLİK: 4 REAL istifadəçiyə (admin@ / muhendis@ /
maliyyeci@ / baxici@arti.edu.az) HEÇ BİR test zərər vermir. Bütün
yazma əməliyyatları `test.3a.` prefiksli MÜVƏQQƏTİ istifadəçilər
üzərindədir və `trap` ilə HƏMİŞƏ təmizlənir.

⚠️ JWT_SECRET heç bir testdə ÇAP EDİLMİR — yalnız uzunluğu.
"""

TESTLER = []


def _t(no, ad, giris, skript):
    TESTLER.append({"no": no, "ad": ad, "giris": giris,
                    "skript": skript.strip("\n")})


# ── Ümumi başlanğıclar ──────────────────────────────────────────────
BAS = r'''
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur: $(pwd)"; exit 1; }
[ -f .env ] || { echo "  ✗ .env yoxdur"; exit 1; }
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
[ -n "$DBURL" ] || { echo "  ✗ .env-də DATABASE_URL yoxdur"; exit 1; }
say() { psql "$DBURL" -At -c "$1" 2>/dev/null | tr -d ' '; }
'''

# Test istifadəçilərini hər halda silən təmizlik funksiyası
TEMIZLIK = r'''
temizle_kullanici() {
  psql "$DBURL" -At -c "DELETE FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%@arti.edu.az';" >/dev/null 2>&1
  true
}
'''

SERVER = r'''
PORT="${PORT:-4000}"
LOQ="/tmp/arti_iiia_${PORT}.log"
API="http://localhost:$PORT/api/v1"
AUTH="$API/auth"

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "  ✗ $PORT portu məşğuldur — əvvəlcə həmin serveri dayandırın"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | awk '{ print "      " $0 }'
  exit 1
fi

npm run build >/tmp/arti_iiia_build.log 2>&1 \
  || { echo "  ✗ build uğursuz"; tail -n 25 /tmp/arti_iiia_build.log | awk '{ print "      " $0 }'; exit 1; }
echo "  ✓ build uğurlu"

PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
temizle() {
  [ -n "$PID" ] && kill "$PID" 2>/dev/null
  [ -n "$PID" ] && wait "$PID" 2>/dev/null
  psql "$DBURL" -At -c "DELETE FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%@arti.edu.az';" >/dev/null 2>&1
  true
}
trap temizle EXIT INT TERM

hazir=0
i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  curl -fsS "$API/saglamliq" -o /dev/null 2>/dev/null && { hazir=1; break; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.5
done
[ "$hazir" = "1" ] || { echo "  ✗ server qalxmadı"; tail -n 25 "$LOQ" | awk '{ print "      " $0 }'; exit 1; }
printf '  ✓ server hazırdır (%s cəhd)\n' "$i"

kod()   { curl -s -o /dev/null -w '%{http_code}' "$@"; }
govde() { curl -s "$@"; }
jsonf() { python3 -c 'import sys,json; d=json.load(sys.stdin); print(eval("d"+sys.argv[1]))' "$1"; }

EPOK=$(date +%s)
TE="test.3a.${EPOK}@arti.edu.az"
PAROL='GucluParol123!'
GOVDE="{\"email\":\"$TE\",\"parol\":\"$PAROL\",\"ad_soyad\":\"Test Istifadeci\"}"
# ⚠️ Giriş DTO-su YALNIZ email + parol qəbul edir! `ad_soyad` göndərsək
#    `forbidNonWhitelisted` onu 400 ilə rədd edər.
GIRIS_GOVDE="{\"email\":\"$TE\",\"parol\":\"$PAROL\"}"
def_giris_kod() { kod -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "$GIRIS_GOVDE"; }
def_giris_token() { govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "$GIRIS_GOVDE" | jsonf "['access_token']"; }

# ⚠️⚠️ NİYƏ AYRICA DƏYİŞƏNLƏR? — bash 3.2-nin ÇOX MƏKRİ XƏTASI!
#
#   gozle '...' 400 "$(kod ... -d "{\"email\":\"$TE\"}")"
#                    └──────────── İÇ-İÇƏ dırnaqlar ────────────┘
#
# macOS-un bash 3.2-si bu formada gövdəni SƏHV parse edir: `\"` ilə
# qorunan dırnaqlar itir və `{...}` qalin mötərizə genişlənməsinə
# (brace expansion) düşür — nəticədə serverə YARIMÇIQ JSON gedir və
# gözlənilməz 400 qayıdır. Gövdəni DƏYİŞƏNDƏ saxlasaq, problem yox olur.
G_Z1="{\"email\":\"test.3a.z1.$EPOK@arti.edu.az\",\"parol\":\"123456\",\"ad_soyad\":\"Test Ad\"}"
G_Z2="{\"email\":\"test.3a.z2.$EPOK@arti.edu.az\",\"parol\":\"$PAROL\",\"ad_soyad\":\"Test Ad\",\"rol\":\"admin\"}"
G_Z3="{\"email\":\"test.3a.z3.$EPOK@arti.edu.az\",\"parol\":\"$PAROL\",\"ad_soyad\":\"A\"}"
G_SAHVE="{\"email\":\"bu-e-poct-deyil\",\"parol\":\"$PAROL\",\"ad_soyad\":\"Test Ad\"}"
G_SEHV_PAROL="{\"email\":\"$TE\",\"parol\":\"YanlisParol123!\"}"
'''

# ══════════════════════════════════════════════════════════════════════
_t("IIIA.1",
   "Autentifikasiya faylları, tip təhlükəsizliyi və sirr gigiyenası",
   """Dərs 3A-nın <strong>bütün</strong> fayllarının mövcudluğunu,
   TypeScript tip yoxlamasını və <strong>sirr gigiyenasını</strong>
   yoxlayır. Xüsusi diqqət: <code>.env.example</code>-də real sirr
   olmamalıdır və <code>parol_hash</code> heç bir DTO-da
   görünməməlidir.<br>
   Səhv olsa: sızma <em>sükutla</em> baş verər — heç bir test qırmızı
   olmaz.""",
   BAS + r'''
echo "  → 1) Fayl strukturu"
FAYLLAR="
src/auth/parol.service.ts
src/auth/istifadeci.service.ts
src/auth/token.service.ts
src/auth/auth.controller.ts
src/auth/auth.module.ts
src/auth/dto/parol.validator.ts
src/auth/dto/qeydiyyat.dto.ts
src/auth/dto/giris.dto.ts
src/auth/dto/token.dto.ts
src/auth/dto/rol.dto.ts
src/auth/qoruyucu/auth.guard.ts
src/auth/qoruyucu/roller.guard.ts
src/auth/qoruyucu/ictimai.dekorator.ts
src/auth/qoruyucu/roller.dekorator.ts
src/auth/qoruyucu/cari-istifadeci.dekorator.ts
skriptler/parol_yoxla.ts
skriptler/istifadeci_yoxla.ts
skriptler/token_yoxla.ts
skriptler/qoruyucu_yoxla.ts
skriptler/3a_yoxla.sh
"
EKSIK=0
for f in $FAYLLAR; do
  if [ -f "$f" ]; then
    printf '      ✓ %-52s %4s sətir\n' "$f" "$(wc -l < "$f" | tr -d ' ')"
  else
    printf '      ✗ %-52s YOXDUR\n' "$f"; EKSIK=$((EKSIK + 1))
  fi
done
[ "$EKSIK" = "0" ] || { echo "  ✗ $EKSIK fayl əskikdir"; exit 1; }
printf '      cəmi: %s fayl, %s sətir\n' \
  "$(echo "$FAYLLAR" | grep -c . )" \
  "$(cat $FAYLLAR | wc -l | tr -d ' ')"

echo ""
echo "  → 2) TypeScript tip yoxlaması"
if npx tsc --noEmit 2>/tmp/iiia1_tsc.log; then
  echo "      ✓ tip xətası yoxdur (0 xəta)"
else
  echo "      ✗ tip xətası var"; awk '{ print "      " $0 }' /tmp/iiia1_tsc.log | head -20; exit 1
fi

echo ""
echo "  → 3) SİRR GİGİYENASI (ən vacib yoxlama)"
if [ -f .gitignore ] && grep -qE '^\.env$|^/\.env$' .gitignore; then
  echo "      ✓ .gitignore .env-i istisna edir"
else
  echo "      ✗ .gitignore .env-i istisna ETMİR"; exit 1
fi
if [ -f .env.example ]; then
  NUM=$(grep '^JWT_SECRET=' .env.example | head -1 | cut -d= -f2- | tr -d '"' | tr -d ' ')
  case "$NUM" in
    *openssl*|*YAZIN*|*yazin*|*nümune*|*numune*|*example*|"")
      echo "      ✓ .env.example-də REAL sirr yoxdur (nümunə mətni)" ;;
    *)
      LEN=${#NUM}
      if [ "$LEN" -ge 32 ] && printf '%s' "$NUM" | grep -qE '^[A-Za-z0-9+/=]+$'; then
        echo "      ✗ TƏHLÜKƏ: .env.example-də REAL sirr ola bilər (uzunluq $LEN)"; exit 1
      else
        echo "      ✓ .env.example-də real sirr görünmür"
      fi ;;
  esac
else
  echo "      ✗ .env.example yoxdur"; exit 1
fi
for f in $(find src -name '*.ts'); do
  if grep -qE "JWT_SECRET\s*[:=]\s*['\"][A-Za-z0-9+/=]{16,}['\"]" "$f"; then
    echo "      ✗ TƏHLÜKƏ: $f içində SABİT JWT sirri var"; exit 1
  fi
done
echo "      ✓ src/ içində sabit JWT sirri yoxdur"

echo ""
echo "  → 4) parol_hash sızması yoxlaması"
SIZMA=0
for f in src/auth/dto/*.ts; do
  if grep -q 'parol_hash' "$f"; then
    echo "      ✗ $f içində parol_hash var"; SIZMA=$((SIZMA + 1))
  fi
done
[ "$SIZMA" = "0" ] && echo "      ✓ heç bir DTO-da parol_hash YOXDUR"
[ "$SIZMA" = "0" ] || exit 1
printf '      «parol_hash: true» oxunan yer sayı : %s (yalnız 1 olmalıdır — daxiliTap)\n' \
  "$(grep -c 'parol_hash: true' src/auth/istifadeci.service.ts)"
printf '      istifadeci.service-də parol_hash   : %s yer\n' \
  "$(grep -c 'parol_hash' src/auth/istifadeci.service.ts)"

echo ""
echo "  → 5) Qlobal guard QƏSDƏN yoxdur (3B-də əlavə olunacaq)"
APP=$(grep -rn 'APP_GUARD' src/ 2>/dev/null | grep -vE ':\s*(//|\*|/\*)' | wc -l | tr -d ' ')
if [ "$APP" = "0" ]; then
  echo "      ✓ APP_GUARD yoxdur — köhnə 40 test qorunur"
else
  echo "      ✗ APP_GUARD tapıldı — köhnə testlər qırılacaq"; exit 1
fi
printf '      guard qoşulan yer (UseGuards)      : %s\n' \
  "$(grep -rn 'UseGuards' src/auth/auth.controller.ts | wc -l | tr -d ' ')"

echo ""
echo "  ✓ IIIA.1 KEÇDİ — fayllar tamdır, tip təmizdir, sirr sızmır"
''')

# ══════════════════════════════════════════════════════════════════════
_t("IIIA.2",
   "Parol siyasəti: hash-ləmə, güclülük qaydaları və DTO validasiyası",
   """İki səviyyəni yoxlayır: (1) <code>parol_yoxla.ts</code> canlı
   probu — bcrypt duz, dərəcə, vaxt, şəffaf yüksəltmə;
   (2) <strong>QeydiyyatDto</strong> validasiya matrisi —
   <code>class-validator</code> ilə 9 nümunə, o cümlədən
   <strong>rol inyeksiyası</strong> cəhdi.<br>
   Bu olmasa: zəif parol və «rol: admin» sükutla keçərdi.""",
   BAS + r'''
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
''')

# ══════════════════════════════════════════════════════════════════════
_t("IIIA.3",
   "İstifadəçi servisi: qeydiyyat, giriş və hash sızmaması",
   """<code>istifadeci_yoxla.ts</code> probunu işlədir (37 yoxlama) və
   sonra <strong>bazanın özünə</strong> baxır: hash-lər bcrypt
   formatındadır, açıq parol yoxdur, istifadəçi siyahısında həssas
   sahə yoxdur.<br>
   Hash sızsa: hücumçu offline sındırmağa başlayar və server bunu
   <em>görə bilməz</em>.""",
   BAS + TEMIZLIK + r'''
trap temizle_kullanici EXIT INT TERM

echo "  → 1) Bazanın başlanğıc vəziyyəti"
EVVEL=$(say "SELECT count(*) FROM kadrlar.istifadeciler;")
printf '      istifadəçi sayı     : %s\n' "$EVVEL"
printf '      rollar üzrə         : %s\n' \
  "$(psql "$DBURL" -At -F'=' -c "SELECT rol, count(*) FROM kadrlar.istifadeciler GROUP BY rol ORDER BY rol;" 2>/dev/null | tr '\n' ' ')"
[ "$EVVEL" -ge 4 ] || { echo "  ✗ istifadəçi sayı gözləniləndən azdır"; exit 1; }

echo ""
echo "  → 2) Hash formatı — heç bir açıq parol olmamalıdır"
ACIQ=$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE parol_hash NOT LIKE '\$2%';")
printf '      bcrypt formatında olmayan hash : %s (0 olmalıdır)\n' "$ACIQ"
[ "$ACIQ" = "0" ] || { echo "  ✗ bcrypt olmayan hash var!"; exit 1; }
QISA=$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE length(parol_hash) < 50;")
printf '      çox qısa hash (<50 simvol)     : %s (0 olmalıdır)\n' "$QISA"
[ "$QISA" = "0" ] || { echo "  ✗ şübhəli qısa hash var!"; exit 1; }
printf '      hash uzunluğu (nümunə)         : %s simvol\n' \
  "$(say "SELECT length(parol_hash) FROM kadrlar.istifadeciler ORDER BY id LIMIT 1;")"
printf '      eyni hash-li istifadəçi sayı   : %s\n' \
  "$(say "SELECT count(*) FROM (SELECT parol_hash FROM kadrlar.istifadeciler GROUP BY parol_hash HAVING count(*) > 1) t;")"

echo ""
echo "  → 3) istifadeci_yoxla.ts — canlı prob (37 yoxlama)"
NETICE=$(npx tsx skriptler/istifadeci_yoxla.ts 2>&1)
printf '%s\n' "$NETICE" | tail -n 4 | awk '{ print "      " $0 }'
KECDI=$(printf '%s' "$NETICE" | grep -oE 'keçdi: [0-9]+' | grep -oE '[0-9]+' | head -1)
UGURSUZ=$(printf '%s' "$NETICE" | grep -oE 'uğursuz: [0-9]+' | grep -oE '[0-9]+' | head -1)
printf '      keçdi=%s uğursuz=%s\n' "${KECDI:-?}" "${UGURSUZ:-?}"
[ "${KECDI:-0}" -ge 37 ] && [ "${UGURSUZ:-1}" = "0" ] \
  || { echo "  ✗ istifadəçi servisi probu uğursuz"; exit 1; }

echo ""
echo "  → 4) Hash sızması — cavabda parol_hash OLMAMALIDIR"
if printf '%s' "$NETICE" | grep -q 'parol_hash'; then
  # ⚠️ Probun özü hash-in olmadığını YOXLAYIR — söz keçməsi normaldır,
  #    ona görə yalnız «TƏHLÜKƏ» kimi işarələnmiş sətirləri axtarırıq.
  if printf '%s' "$NETICE" | grep -qiE 'parol_hash.*(var|sızd|aşkar)|TƏHLÜKƏ.*parol_hash'; then
    echo "      ✗ cavabda parol_hash AŞKAR OLUNDU"; exit 1
  fi
fi
echo "      ✓ hamisi() cavabında parol_hash yoxdur (prob təsdiqləyir)"
printf '      ISTIFADECI_SECIM sahələri      : %s\n' \
  "$(awk '/export const ISTIFADECI_SECIM/,/as const/' src/auth/istifadeci.service.ts \
     | grep -oE '[a-z_]+: true' | cut -d: -f1 | tr '\n' ' ')"
if grep -qE '^\s+parol_hash: true' src/auth/istifadeci.service.ts; then
  echo "      ⚠️ «parol_hash: true» var — yalnız daxiliTap() daxilində olmalıdır"
  printf '      daxiliTap-də mi?               : %s\n' \
    "$(grep -B12 'parol_hash: true' src/auth/istifadeci.service.ts | grep -c 'private async daxiliTap')"
fi

echo ""
echo "  → 5) Təmizlik"
temizle_kullanici
SONRA=$(say "SELECT count(*) FROM kadrlar.istifadeciler;")
printf '      istifadəçi sayı (sondan sonra): %s\n' "$SONRA"
[ "$SONRA" = "$EVVEL" ] || { echo "  ✗ test iz qoydu: $EVVEL → $SONRA"; exit 1; }

echo ""
echo "  ✓ IIIA.3 KEÇDİ — istifadəçi servisi işləyir, hash sızmır"
''')

# ══════════════════════════════════════════════════════════════════════
_t("IIIA.4",
   "Token servisi: JWT quruluşu, imza, müddət və sirr uzunluğu",
   """<code>token_yoxla.ts</code> probunu işlədir (35 yoxlama) və
   <strong>əl ilə</strong> tokeni açıb yoxlayır: 3 hissə, base64url
   payload, <code>sub/email/rol/iat/exp</code> sahələri və
   <strong>heç bir həssas məlumat olmaması</strong>.<br>
   ⚠️ JWT şifrələnmir — payload hər kəs tərəfindən oxunur. Ona görə
   ora <em>yalnız identifikasiya</em> yazılmalıdır.""",
   BAS + r'''
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
''')

# ══════════════════════════════════════════════════════════════════════
_t("IIIA.5",
   "Qoruyucular: AuthGuard, RollerGuard, dekoratorlar və 401/403",
   """<code>qoruyucu_yoxla.ts</code> probunu işlədir (26 yoxlama) və
   guard-ların <strong>düzgün qoşulduğunu</strong> yoxlayır: sıra
   <code>AuthGuard → RollerGuard</code>-dir, <code>@Ictimai()</code>
   açıq endpoint-lərdə var, <code>APP_GUARD</code> isə
   <em>yoxdur</em>.<br>
   Sıra səhv olsa: 403 yerinə 401 gələr və istifadəçi boş yerə
   yenidən giriş edər.""",
   BAS + r'''
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
''')

# ══════════════════════════════════════════════════════════════════════
_t("IIIA.6",
   "Canlı server: açıq endpoint-lər, qeydiyyat və validasiya",
   """Real server qaldırılır və <strong>açıq</strong> endpoint-lər
   yoxlanılır: qeydiyyat (201), zəif parol (400), rol inyeksiyası
   (400), mövcud e-poçt (400), səhv parol (401), düzgün parol (200),
   sağlamlıq (200).<br>
   Status kodları yoxlanılır — çünki 401/400/201 qarışsa, frontend
   səhv qərar verir (məsələn 401 alanda giriş səhifəsinə atır).""",
   BAS + SERVER + r'''
XETA=0
gozle() {
  AD="$1"; GOZ="$2"; GEL="$3"
  if [ "$GEL" = "$GOZ" ]; then
    printf '      [OK] %-44s → %s\n' "$AD" "$GEL"
  else
    printf '      [XX] %-44s → %s (gözlənilirdi %s)\n' "$AD" "$GEL" "$GOZ"; XETA=$((XETA+1))
  fi
}

echo "  → 1) Sağlamlıq yoxlaması (açıq)"
gozle 'GET /auth/yoxlama (açıq)' 200 "$(kod "$AUTH/yoxlama")"
govde "$AUTH/yoxlama" | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("      auth          :", d.get("auth"))
print("      sirr_uzunlugu :", d.get("sirr_uzunlugu"), "(DƏYƏR YOX — yalnız uzunluq)")
print("      muddet        :", d.get("muddet"))
' 2>/dev/null

echo ""
echo "  → 2) Qeydiyyat — uğurlu hal (201)"
gozle 'POST /auth/qeydiyyat (güclü parol)' 201 "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$GOVDE")"
printf '      bazada yeni sətir : %s\n' "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email = '$TE';")"
printf '      rolu              : %s (standart «baxici» olmalıdır)\n' \
  "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE email = '$TE';")"
[ "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE email = '$TE';")" = "baxici" ] \
  || { echo "      ✗ standart rol «baxici» deyil!"; XETA=$((XETA+1)); }

echo ""
echo "  → 3) Qeydiyyat — rədd halları"
gozle 'POST zəif parol (123456)' 400 \
  "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$G_Z1")"
gozle 'POST rol inyeksiyası (rol=admin)' 400 \
  "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$G_Z2")"
gozle 'POST mövcud e-poçt (409 konflikt)' 409 \
  "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$GOVDE")"
gozle 'POST səhv e-poçt formatı' 400 \
  "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$G_SAHVE")"
gozle 'POST boş gövdə' 400 "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d '{}')"
gozle 'POST qısa ad_soyad' 400 \
  "$(kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$G_Z3")"

echo ""
echo "  → 4) Rol inyeksiyası cəhdi BAZAYA düşmədi"
printf '      test.3a.z2 bazada : %s (0 olmalıdır)\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email = 'test.3a.z2.$EPOK@arti.edu.az';")"
printf '      admin rolunda test: %s (0 olmalıdır)\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%' AND rol = 'admin';")"
[ "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%' AND rol <> 'baxici';")" = "0" ] \
  || { echo "      ✗ test istifadəçisi «baxici»-dən başqa rola malikdir!"; XETA=$((XETA+1)); }

echo ""
echo "  → 5) Giriş — 401 və 200"
gozle 'POST giriş səhv parol (401)' 401 \
  "$(kod -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "$G_SEHV_PAROL")"
gozle 'POST giriş mövcud olmayan e-poçt' 401 \
  "$(kod -X POST "$AUTH/giris" -H 'Content-Type: application/json' \
     -d '{"email":"yoxdur.3a@arti.edu.az","parol":"YanlisParol123!"}')"
gozle 'POST giriş düzgün parol (200)' 200 "$(def_giris_kod)"

echo ""
echo "  → 6) Giriş cavabının quruluşu"
CAVAB=$(govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "$GIRIS_GOVDE")
printf '%s' "$CAVAB" | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("      ugur          :", d.get("ugur"))
print("      token_novu    :", d.get("token_novu"))
print("      muddet_saniye :", d.get("muddet_saniye"))
print("      bitme_vaxti   :", d.get("bitme_vaxti"))
t = d.get("access_token", "")
print("      token hissəsi :", len(t.split(".")))
hamisi = json.dumps(d)
print("      parol_hash    :", "VAR — TƏHLÜKƏ!" if "parol_hash" in hamisi else "yoxdur ✓")
' 2>/dev/null

echo ""
echo "  → 7) Səhv parol ilə düzgün parolun cavab QURULUŞU eynidir (enumeration)"
S1=$(govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "{\"email\":\"$TE\",\"parol\":\"Yanlis1!\"}" | python3 -c 'import sys,json;print(json.load(sys.stdin)["xeta"]["kod"])' 2>/dev/null)
S2=$(govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d '{"email":"yoxdur.3a@arti.edu.az","parol":"Yanlis1!"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["xeta"]["kod"])' 2>/dev/null)
printf '      mövcud e-poçt + səhv parol : %s\n' "$S1"
printf '      mövcud olmayan e-poçt      : %s\n' "$S2"
[ "$S1" = "$S2" ] && echo "      ✓ hər ikisi eyni kodu verir — e-poçt siyahısı sızmır" \
  || { echo "      ✗ fərqli kodlar — enumeration mümkündür"; XETA=$((XETA+1)); }

echo ""
[ "$XETA" = "0" ] || { echo "  ✗ $XETA yoxlama uğursuz"; exit 1; }
echo "  ✓ IIIA.6 KEÇDİ — açıq endpoint-lər və validasiya düzgün işləyir"
''')

# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
_t("IIIA.7",
   "Canlı server: qorunan endpoint-lər, token başlığı və saxtalaşdırma",
   """Token <em>olmadan</em>, <em>səhv</em> və <em>düzgün</em> hallarda
   qorunan endpoint-lərin davranışı yoxlanılır. Sonra token
   <strong>saxtalaşdırılır</strong> (payload dəyişdirilir, imza
   saxlanılır) və serverin onu rədd etdiyi təsdiqlənir.<br>
   Saxtalaşdırma keçsəydi: hər kəs özünü <code>admin</code> edə
   bilərdi.""",
   BAS + SERVER + r'''
XETA=0
gozle() {
  AD="$1"; GOZ="$2"; GEL="$3"
  if [ "$GEL" = "$GOZ" ]; then printf '      [OK] %-46s → %s\n' "$AD" "$GEL"
  else printf '      [XX] %-46s → %s (gözlənilirdi %s)\n' "$AD" "$GEL" "$GOZ"; XETA=$((XETA+1)); fi
}

kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$GOVDE" >/dev/null
TOKEN=$(def_giris_token)
[ -n "$TOKEN" ] || { echo "  ✗ token alınmadı"; exit 1; }
printf '  token alındı: %s simvol, %s hissə\n\n' "${#TOKEN}" "$(printf '%s' "$TOKEN" | awk -F. '{print NF}')"

echo "  → 1) Token OLMADAN qorunan endpoint-lər → 401"
for yol in me admin-yoxlama muhendis-yoxlama istifadeciler; do
  gozle "GET /$yol (token yox)" 401 "$(kod "$AUTH/$yol")"
done
gozle 'PATCH rol (token yox)' 401 "$(kod -X PATCH "$AUTH/istifadeci/1/rol" -H 'Content-Type: application/json' -d '{"rol":"admin"}')"

echo ""
echo "  → 2) Səhv token başlığı → 401"
gozle 'Authorization: Bearer bu-token-deyil' 401 "$(kod -H 'Authorization: Bearer bu-token-deyil' "$AUTH/me")"
gozle 'Authorization: Bearer (boş)' 401 "$(kod -H 'Authorization: Bearer ' "$AUTH/me")"
gozle 'Authorization: Basic dXNlcjpwYXNz' 401 "$(kod -H 'Authorization: Basic dXNlcjpwYXNz' "$AUTH/me")"
gozle 'Authorization olmadan (başqa başlıq)' 401 "$(kod -H 'X-Test: 1' "$AUTH/me")"
gozle 'Bearer sözü olmadan' 401 "$(kod -H "Authorization: $TOKEN" "$AUTH/me")"

echo ""
echo "  → 3) Düzgün token → 200"
gozle 'GET /me (düzgün token)' 200 "$(kod -H "Authorization: Bearer $TOKEN" "$AUTH/me")"
govde -H "Authorization: Bearer $TOKEN" "$AUTH/me" | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("      sub           :", d.get("sub"))
print("      email         :", d.get("email"))
print("      rol           :", d.get("rol"))
print("      token_verildi :", d.get("token_verildi"))
print("      token_bitir   :", d.get("token_bitir"))
' 2>/dev/null
gozle 'GET /muhendis-yoxlama (baxici → 403)' 403 "$(kod -H "Authorization: Bearer $TOKEN" "$AUTH/muhendis-yoxlama")"

echo ""
echo "  → 4) 401 və 403 cavablarının KODLARI fərqlidir"
K401=$(govde "$AUTH/me" | python3 -c 'import sys,json;print(json.load(sys.stdin)["xeta"]["kod"])' 2>/dev/null)
K403=$(govde -H "Authorization: Bearer $TOKEN" "$AUTH/admin-yoxlama" | python3 -c 'import sys,json;print(json.load(sys.stdin)["xeta"]["kod"])' 2>/dev/null)
printf '      401 kodu : %s\n' "$K401"
printf '      403 kodu : %s\n' "$K403"
[ "$K401" != "$K403" ] && echo "      ✓ frontend 401 və 403-ü AYIRD EDƏ BİLİR" \
  || { echo "      ✗ kodlar eynidir — frontend ayırd edə bilməz"; XETA=$((XETA+1)); }

echo ""
echo "  → 5) SAXTALAŞDIRMA: payload dəyişdirilir, imza saxlanılır"
cat > /tmp/iiia7_saxta.py <<'PYSUB7'
import base64, json, sys
h, p, s = sys.argv[1].split('.')
def ac(x): return json.loads(base64.urlsafe_b64decode(x + '=' * (-len(x) % 4)))
def bag(d): return base64.urlsafe_b64encode(json.dumps(d, separators=(',', ':')).encode()).rstrip(b'=').decode()
yuk = ac(p)
print('      orijinal rol :', yuk.get('rol'), file=sys.stderr)
yuk['rol'] = 'admin'
print('%s.%s.%s' % (h, bag(yuk), s))
PYSUB7
SAXTA=$(python3 /tmp/iiia7_saxta.py "$TOKEN" 2>/dev/null)
printf '      saxta token uzunluğu : %s (orijinal %s)\n' "${#SAXTA}" "${#TOKEN}"
[ "${#SAXTA}" -gt 0 ] || { echo "  ✗ saxta token yaradıla bilmədi"; exit 1; }
gozle 'saxta token (rol=admin) → 401' 401 "$(kod -H "Authorization: Bearer $SAXTA" "$AUTH/admin-yoxlama")"
gozle 'saxta token /me → 401' 401 "$(kod -H "Authorization: Bearer $SAXTA" "$AUTH/me")"
rm -f /tmp/iiia7_saxta.py

echo ""
echo "  → 6) İmzasız / pozulmuş tokenlər"
H=$(printf '%s' "$TOKEN" | cut -d. -f1)
P=$(printf '%s' "$TOKEN" | cut -d. -f2)
gozle 'yalnız 2 hissə' 401 "$(kod -H "Authorization: Bearer $H.$P" "$AUTH/me")"
gozle '4 hissə' 401 "$(kod -H "Authorization: Bearer $TOKEN.artiq" "$AUTH/me")"
gozle 'imza tamamilə dəyişdirilib' 401 \
  "$(kod -H "Authorization: Bearer $H.$P.${H}${P}" "$AUTH/me")"

echo ""
[ "$XETA" = "0" ] || { echo "  ✗ $XETA yoxlama uğursuz"; exit 1; }
echo "  ✓ IIIA.7 KEÇDİ — token qoruması və saxtalaşdırma müdafiəsi işləyir"
''')

# ══════════════════════════════════════════════════════════════════════
_t("IIIA.8",
   "Canlı server: RBAC — 4 real istifadəçi və 401/403 ayrımı",
   """<strong>Real</strong> 4 istifadəçi ilə (<code>admin@</code>,
   <code>muhendis@</code>, <code>maliyyeci@</code>,
   <code>baxici@arti.edu.az</code>, parol <code>123456</code>) giriş
   edilir və hər birinin roluna uyğun cavabları yoxlanılır.<br>
   ⚠️ Bu istifadəçilərə <em>heç nə yazılmır</em> — yalnız oxunur.
   Rol matrisi səhv olsa, maliyyə məlumatı baxıcıya açıq ola bilər.""",
   BAS + SERVER + r'''
XETA=0
gozle() {
  AD="$1"; GOZ="$2"; GEL="$3"
  if [ "$GEL" = "$GOZ" ]; then printf '      [OK] %-48s → %s\n' "$AD" "$GEL"
  else printf '      [XX] %-48s → %s (gözlənilirdi %s)\n' "$AD" "$GEL" "$GOZ"; XETA=$((XETA+1)); fi
}

SEED='123456'
tok_al() {
  govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$1\",\"parol\":\"$SEED\"}" | jsonf "['access_token']" 2>/dev/null
}
rol_al() {
  govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$1\",\"parol\":\"$SEED\"}" | jsonf "['istifadeci']['rol']" 2>/dev/null
}

echo "  → 1) Dörd real istifadəçi ilə giriş"
for e in admin@arti.edu.az muhendis@arti.edu.az maliyyeci@arti.edu.az baxici@arti.edu.az; do
  K=$(kod -X POST "$AUTH/giris" -H 'Content-Type: application/json' -d "{\"email\":\"$e\",\"parol\":\"$SEED\"}")
  R=$(rol_al "$e")
  printf '      [%s] %-30s rol=%-10s (gözlənilən: %s)\n' \
    "$([ "$K" = "200" ] && echo OK || echo XX)" "$e" "$R" "${e%%@*}"
  [ "$K" = "200" ] || XETA=$((XETA+1))
  [ "$R" = "${e%%@*}" ] || { echo "      ✗ rol uyğun deyil!"; XETA=$((XETA+1)); }
done

echo ""
echo "  → 2) Rol matrisi (admin/muhendis/maliyyeci/baxici)"
T_ADMIN=$(tok_al admin@arti.edu.az)
T_MUH=$(tok_al muhendis@arti.edu.az)
T_MAL=$(tok_al maliyyeci@arti.edu.az)
T_BAX=$(tok_al baxici@arti.edu.az)
for t in "$T_ADMIN" "$T_MUH" "$T_MAL" "$T_BAX"; do
  [ -n "$t" ] || { echo "  ✗ token alınmadı"; exit 1; }
done

printf '      %-12s %-22s %-22s\n' 'İSTİFADƏÇİ' '/admin-yoxlama' '/muhendis-yoxlama'
for c in "admin:$T_ADMIN:200:200" "muhendis:$T_MUH:403:200" \
         "maliyyeci:$T_MAL:403:403" "baxici:$T_BAX:403:403"; do
  AD=${c%%:*}; REST=${c#*:}; T=${REST%%:*}; REST=${REST#*:}
  G1=${REST%%:*}; G2=${REST##*:}
  K1=$(kod -H "Authorization: Bearer $T" "$AUTH/admin-yoxlama")
  K2=$(kod -H "Authorization: Bearer $T" "$AUTH/muhendis-yoxlama")
  printf '      %-12s %-22s %-22s\n' "$AD" "$K1 (gözlənilir $G1)" "$K2 (gözlənilir $G2)"
  [ "$K1" = "$G1" ] || { echo "      ✗ $AD admin-yoxlama"; XETA=$((XETA+1)); }
  [ "$K2" = "$G2" ] || { echo "      ✗ $AD muhendis-yoxlama"; XETA=$((XETA+1)); }
done

echo ""
echo "  → 3) 403 gəlməlidir, 401 YOX (tanınan istifadəçi üçün)"
K=$(kod -H "Authorization: Bearer $T_BAX" "$AUTH/admin-yoxlama")
printf '      baxici /admin-yoxlama : %s\n' "$K"
[ "$K" = "403" ] && echo "      ✓ 403 — istifadəçi TANINIR, sadəcə icazəsi yoxdur" \
  || { echo "      ✗ 401 gəldi — istifadəçi «tanınmır» kimi cavab aldı"; XETA=$((XETA+1)); }

echo ""
echo "  → 4) İstifadəçi siyahısı yalnız admin üçündür"
gozle 'admin  /istifadeciler' 200 "$(kod -H "Authorization: Bearer $T_ADMIN" "$AUTH/istifadeciler")"
gozle 'muhendis /istifadeciler → 403' 403 "$(kod -H "Authorization: Bearer $T_MUH" "$AUTH/istifadeciler")"
gozle 'maliyyeci /istifadeciler → 403' 403 "$(kod -H "Authorization: Bearer $T_MAL" "$AUTH/istifadeciler")"
gozle 'baxici /istifadeciler → 403' 403 "$(kod -H "Authorization: Bearer $T_BAX" "$AUTH/istifadeciler")"

echo ""
echo "  → 5) Siyahıda parol_hash YOXDUR"
SIYAHI=$(govde -H "Authorization: Bearer $T_ADMIN" "$AUTH/istifadeciler")
printf '%s' "$SIYAHI" | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("      istifadəçi sayı :", len(d) if isinstance(d, list) else "?")
print("      parol_hash      :", "VAR — TƏHLÜKƏ!" if "parol_hash" in json.dumps(d) else "yoxdur ✓")
if isinstance(d, list) and d:
    print("      sahələr         :", ", ".join(sorted(d[0].keys())))
' 2>/dev/null
printf '%s' "$SIYAHI" | grep -q 'parol_hash' && { echo "      ✗ parol_hash SIZDI!"; XETA=$((XETA+1)); }

echo ""
echo "  → 6) Dörd real istifadəçi toxunulmazdır"
printf '      real istifadəçi sayı : %s\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE '%@arti.edu.az' AND email NOT LIKE 'test.3a.%';")"
printf '      hamısı aktiv         : %s\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE '%@arti.edu.az' AND email NOT LIKE 'test.3a.%' AND aktiv;")"
printf '      rollar               : %s\n' \
  "$(psql "$DBURL" -At -F'=' -c "SELECT rol, count(*) FROM kadrlar.istifadeciler WHERE email NOT LIKE 'test.3a.%' GROUP BY rol ORDER BY rol;" 2>/dev/null | tr '\n' ' ')"

echo ""
[ "$XETA" = "0" ] || { echo "  ✗ $XETA yoxlama uğursuz"; exit 1; }
echo "  ✓ IIIA.8 KEÇDİ — RBAC düzgün işləyir, 401 və 403 ayrılır"
''')

# ══════════════════════════════════════════════════════════════════════
_t("IIIA.9",
   "Canlı server: admin istifadəçi idarəsi (rol, aktivlik) və təmizlik",
   """Admin funksiyaları: istifadəçi siyahısı, rol dəyişmə, aktiv/deaktiv
   etmə. Hər dəyişiklik <strong>dərhal</strong> təsir göstərməlidir —
   yeni rol həmin anda işləməlidir, deaktiv hesab isə dərhal giriş edə
   bilməməlidir.<br>
   Test həm də JWT-nin <em>geri çağırıla bilmədiyini</em> göstərir:
   köhnə token hələ də köhnə rolu daşıyır. Test sonda
   <code>test.3a.</code> prefiksli bütün istifadəçiləri silir.""",
   BAS + SERVER + r'''
XETA=0
gozle() {
  AD="$1"; GOZ="$2"; GEL="$3"
  if [ "$GEL" = "$GOZ" ]; then printf '      [OK] %-46s → %s\n' "$AD" "$GEL"
  else printf '      [XX] %-46s → %s (gözlənilirdi %s)\n' "$AD" "$GEL" "$GOZ"; XETA=$((XETA+1)); fi
}

EVVEL=$(say "SELECT count(*) FROM kadrlar.istifadeciler;")
echo "  → 0) Başlanğıc: $EVVEL istifadəçi"

T_ADMIN=$(govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' | jsonf "['access_token']" 2>/dev/null)
[ -n "$T_ADMIN" ] || { echo "  ✗ admin tokeni alınmadı"; exit 1; }

kod -X POST "$AUTH/qeydiyyat" -H 'Content-Type: application/json' -d "$GOVDE" >/dev/null
ID=$(say "SELECT id FROM kadrlar.istifadeciler WHERE email = '$TE';")
[ -n "$ID" ] || { echo "  ✗ test istifadəçisi yaradılmadı"; exit 1; }
printf '      test istifadəçisi : id=%s, %s\n' "$ID" "$TE"
TOKEN_BAXICI=$(def_giris_token)
printf '      köhnə token alındı : %s simvol (rol=baxici)\n' "${#TOKEN_BAXICI}"

echo ""
echo "  → 1) İstifadəçi siyahısı (admin)"
gozle 'GET /auth/istifadeciler' 200 "$(kod -H "Authorization: Bearer $T_ADMIN" "$AUTH/istifadeciler")"
printf '      siyahıda test ist.: %s\n' \
  "$(govde -H "Authorization: Bearer $T_ADMIN" "$AUTH/istifadeciler" | grep -c "$TE")"

echo ""
echo "  → 2) Rol dəyişmə: baxici → muhendis"
gozle "PATCH /istifadeci/$ID/rol (baxici→muhendis)" 200 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/rol" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"rol":"muhendis"}')"
printf '      bazada yeni rol    : %s\n' "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE id = $ID;")"
[ "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE id = $ID;")" = "muhendis" ] \
  || { echo "      ✗ rol bazada dəyişmədi"; XETA=$((XETA+1)); }

echo ""
echo "  → 3) YENİ ROL DƏRHAL İŞLƏYİR (yeni token ilə)"
T_YENI=$(def_giris_token)
gozle 'YENİ token /muhendis-yoxlama' 200 "$(kod -H "Authorization: Bearer $T_YENI" "$AUTH/muhendis-yoxlama")"
gozle 'YENİ token /admin-yoxlama → 403' 403 "$(kod -H "Authorization: Bearer $T_YENI" "$AUTH/admin-yoxlama")"
printf '      ⚠️ KÖHNƏ token hələ də «baxici» deyir — JWT LƏĞV EDİLƏ BİLMİR:\n'
gozle 'KÖHNƏ token /muhendis-yoxlama → 403' 403 \
  "$(kod -H "Authorization: Bearer $TOKEN_BAXICI" "$AUTH/muhendis-yoxlama")"
gozle 'KÖHNƏ token /me → 200 (hələ etibarlıdır!)' 200 \
  "$(kod -H "Authorization: Bearer $TOKEN_BAXICI" "$AUTH/me")"

echo ""
echo "  → 4) Yanlış rol adı və id rədd edilir"
gozle 'PATCH rol=superadmin' 400 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/rol" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"rol":"superadmin"}')"
gozle 'PATCH rol boş gövdə' 400 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/rol" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{}')"
gozle 'PATCH mövcud olmayan id → 404 (500 YOX)' 404 \
  "$(kod -X PATCH "$AUTH/istifadeci/999999/rol" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"rol":"baxici"}')"

echo ""
echo "  → 5) Deaktiv etmə: aktiv=false → giriş 401"
gozle "PATCH /istifadeci/$ID/aktivlik (false)" 200 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/aktivlik" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"aktiv":false}')"
printf '      bazada aktiv       : %s\n' "$(say "SELECT aktiv FROM kadrlar.istifadeciler WHERE id = $ID;")"
gozle 'deaktiv hesabla giriş → 403' 403 "$(def_giris_kod)"
gozle 'səhv tip (aktiv="beli") → 400' 400 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/aktivlik" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"aktiv":"beli"}')"

echo ""
echo "  → 6) Yenidən aktiv etmə"
gozle "PATCH /istifadeci/$ID/aktivlik (true)" 200 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/aktivlik" -H "Authorization: Bearer $T_ADMIN" \
     -H 'Content-Type: application/json' -d '{"aktiv":true}')"
gozle 'yenidən giriş → 200' 200 "$(def_giris_kod)"

echo ""
echo "  → 7) Qeyri-admin rol dəyişə BİLMƏZ"
T_MUH=$(govde -X POST "$AUTH/giris" -H 'Content-Type: application/json' \
  -d '{"email":"muhendis@arti.edu.az","parol":"123456"}' | jsonf "['access_token']")
gozle 'muhendis PATCH rol → 403' 403 \
  "$(kod -X PATCH "$AUTH/istifadeci/$ID/rol" -H "Authorization: Bearer $T_MUH" \
     -H 'Content-Type: application/json' -d '{"rol":"admin"}')"
printf '      rol dəyişməyib    : %s (muhendis olmalıdır)\n' \
  "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE id = $ID;")"
[ "$(say "SELECT rol FROM kadrlar.istifadeciler WHERE id = $ID;")" = "muhendis" ] \
  || { echo "      ✗ İCAZƏSİZ DƏYİŞİKLİK BAŞ VERDİ!"; XETA=$((XETA+1)); }

echo ""
echo "  → 8) Təmizlik"
psql "$DBURL" -At -c "DELETE FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%@arti.edu.az';" >/dev/null 2>&1
SONRA=$(say "SELECT count(*) FROM kadrlar.istifadeciler;")
printf '      istifadəçi sayı : %s → %s\n' "$EVVEL" "$SONRA"
[ "$SONRA" = "$EVVEL" ] || { echo "      ✗ test iz qoydu!"; XETA=$((XETA+1)); }
printf '      qalan test ist. : %s (0 olmalıdır)\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%';")"
printf '      real istifadəçi : %s (4 olmalıdır)\n' \
  "$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE '%@arti.edu.az' AND email NOT LIKE 'test.3a.%';")"

echo ""
[ "$XETA" = "0" ] || { echo "  ✗ $XETA yoxlama uğursuz"; exit 1; }
echo "  ✓ IIIA.9 KEÇDİ — admin idarəsi işləyir və test iz qoymur"
''')

# ══════════════════════════════════════════════════════════════════════
_t("IIIA.10",
   "YEKUN: bütün alətlər, reqressiya və baza vəziyyəti",
   """Dərs 3A-nın bütün yoxlama alətlərini bir yerdə işlədir,
   <strong>əvvəlki dərslərin reqressiyasını</strong> (1A, 1B, 2A, 2B)
   təsdiqləyir və bazanın son vəziyyətini yoxlayır.<br>
   Reqressiya olmasa: yeni autentifikasiya qatı köhnə funksionallığı
   sükutla sındıra bilər və bunu yalnız istehsalatda bilərsən.""",
   BAS + TEMIZLIK + r'''
trap temizle_kullanici EXIT INT TERM
XETA=0

echo "  → 1) Tip yoxlaması"
if npx tsc --noEmit; then echo "      ✓ təmiz (0 xəta)"; else echo "      ✗ tip xətası"; XETA=$((XETA+1)); fi

echo ""
echo "  → 2) 3A yoxlama alətləri (4 prob + 1 skript)"
for s in parol istifadeci token qoruyucu; do
  CIXIS=$(npx tsx "skriptler/${s}_yoxla.ts" 2>&1)
  N=$(printf '%s' "$CIXIS" | grep -oE 'keçdi: [0-9]+' | grep -oE '[0-9]+' | head -1)
  U=$(printf '%s' "$CIXIS" | grep -oE 'uğursuz: [0-9]+' | grep -oE '[0-9]+' | head -1)
  printf '      %-12s probu : keçdi=%s uğursuz=%s %s\n' "$s" "${N:-?}" "${U:-?}" \
    "$([ "${U:-1}" = "0" ] && echo '✓' || echo '✗')"
  [ "${U:-1}" = "0" ] || XETA=$((XETA+1))
done
printf '      %-12s skript: %s sətir\n' '3a_yoxla.sh' "$(wc -l < skriptler/3a_yoxla.sh | tr -d ' ')"

echo ""
echo "  → 3) 3A fayl sayı"
printf '      src/auth/     : %2s fayl, %4s sətir\n' \
  "$(find src/auth -name '*.ts' | wc -l | tr -d ' ')" \
  "$(cat $(find src/auth -name '*.ts') | wc -l | tr -d ' ')"
printf '      src/ cəmi     : %2s fayl, %4s sətir (generated xaric)\n' \
  "$(find src -name '*.ts' -not -path 'src/generated/*' | wc -l | tr -d ' ')" \
  "$(cat $(find src -name '*.ts' -not -path 'src/generated/*') | wc -l | tr -d ' ')"
printf '      skriptler/    : %2s fayl\n' "$(ls -1 skriptler/ | wc -l | tr -d ' ')"

echo ""
echo "  → 4) REQRESSİYA — köhnə alətlər hələ də işləyir"
for s in dto mapper servis statistika elaqeler toplu audit; do
  if [ -f "skriptler/${s}_yoxla.ts" ]; then
    CIXIS=$(npx tsx "skriptler/${s}_yoxla.ts" 2>&1)
    KOD=$?
    N=$(printf '%s' "$CIXIS" | grep -oE 'keçdi: [0-9]+' | grep -oE '[0-9]+' | head -1)
    U=$(printf '%s' "$CIXIS" | grep -oE 'uğursuz: [0-9]+' | grep -oE '[0-9]+' | head -1)
    if [ -n "$N" ]; then
      printf '      %-12s (2A/2B) : keçdi=%s uğursuz=%s %s\n' "$s" "$N" "${U:-?}" \
        "$([ "${U:-1}" = "0" ] && echo '✓' || echo '✗')"
      [ "${U:-1}" = "0" ] || XETA=$((XETA+1))
    else
      # ⚠️ Bəzi köhnə probelər «keçdi: N» formatında yazmır —
      #    onlar üçün ÇIXIŞ KODU yeganə obyektiv meyardır.
      printf '      %-12s (2A/2B) : exit=%s %s\n' "$s" "$KOD" \
        "$([ "$KOD" = "0" ] && echo '✓' || echo '✗')"
      [ "$KOD" = "0" ] || XETA=$((XETA+1))
    fi
  else
    printf '      %-12s (2A/2B) : fayl yoxdur\n' "$s"
  fi
done
for s in crud_yoxla.sh 2b_yoxla.sh; do
  if [ -f "skriptler/$s" ]; then
    if bash "skriptler/$s" >/tmp/iiia10_$s.log 2>&1; then
      printf '      %-12s (köhnə) : ✓ %s\n' "$s" \
        "$(grep -oE 'KEÇDİ: [0-9]+|keçdi: [0-9]+' /tmp/iiia10_$s.log | tail -1)"
    else
      printf '      %-12s (köhnə) : ✗ uğursuz\n' "$s"; XETA=$((XETA+1))
    fi
  fi
done

echo ""
echo "  → 5) Əvvəlki dərslərin modulları hələ də qoşuludur"
for m in PrismaModule SaglamliqModule EmekdaslarModule AuditModule AuthModule; do
  N=$(grep -c "$m" src/app.module.ts)
  [ "$N" -ge 1 ] && printf '      ✓ %s\n' "$m" || { printf '      ✗ %s YOXDUR\n' "$m"; XETA=$((XETA+1)); }
done
printf '      qlobal guard : %s (0 olmalıdır — 3B-də əlavə olunacaq)\n' \
  "$(grep -rn 'APP_GUARD' src/ 2>/dev/null | grep -vE ':\s*(//|\*|/\*)' | wc -l | tr -d ' ')"

echo ""
echo "  → 6) Bazanın son vəziyyəti"
CEDVEL=$(say "SELECT count(*) FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog','information_schema');")
SXEM=$(say "SELECT count(*) FROM information_schema.schemata WHERE schema_name NOT LIKE 'pg_%' AND schema_name <> 'information_schema';")
EMEK=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
IST=$(say "SELECT count(*) FROM kadrlar.istifadeciler;")
printf '      cədvəl + görünüş : %s\n' "$CEDVEL"
printf '      sxem             : %s\n' "$SXEM"
printf '      əməkdaş          : %s\n' "$EMEK"
printf '      istifadəçi       : %s (4 real + 0 test)\n' "$IST"
[ "$EMEK" = "14" ] || { echo "      ✗ əməkdaş sayı dəyişdi!"; XETA=$((XETA+1)); }
[ "$IST" -ge 4 ] || { echo "      ✗ istifadəçi sayı azaldı!"; XETA=$((XETA+1)); }
TESTQ=$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%';")
[ "$TESTQ" = "0" ] || { echo "      ✗ bazada test istifadəçisi qalıb: $TESTQ"; XETA=$((XETA+1)); }

echo ""
echo "  → 7) Sirr gigiyenası (son yoxlama)"
grep -qE '^\.env$' .gitignore && echo "      ✓ .env git-ə yazılmır" || { echo "      ✗ .env .gitignore-da deyil"; XETA=$((XETA+1)); }
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  echo "      ✗ TƏHLÜKƏ: .env GIT-Ə İZLƏNİR!"; XETA=$((XETA+1))
else
  echo "      ✓ .env git tərəfindən izlənmir"
fi
SR=$(grep '^JWT_SECRET=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
printf '      JWT_SECRET uzunluğu : %s (>=32)\n' "${#SR}"
[ "${#SR}" -ge 32 ] || XETA=$((XETA+1))

echo ""
[ "$XETA" = "0" ] || { echo "  ✗ $XETA yoxlama uğursuz"; exit 1; }
echo "  ✓ IIIA.10 KEÇDİ — Dərs 3A tam təsdiqləndi, reqressiya təmizdir"
echo "  ✓ NÖVBƏTİ ADDIM: Dərs 3B (refresh token, httpOnly cookie, qlobal APP_GUARD)"
''')
