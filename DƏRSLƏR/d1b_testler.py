#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-1B — 10 yekun test (IB.1 … IB.10).

Hər test müstəqildir: bir-birindən asılı deyil və istənilən sırada
işlədilə bilər. Testlər `LAYIHE` mühit dəyişənini oxuyur (standart:
$HOME/Deepseek_ARTI/DS_Backend) və öz serverlərini özləri qaldırıb
söndürürlər.
"""

TESTLER = []


def _t(no, ad, giris, skript):
    TESTLER.append({"no": no, "ad": ad, "giris": giris,
                    "skript": skript.strip("\n")})


# ── Ümumi başlanğıc ─────────────────────────────────────────────────
BAS = r'''
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur — bu qovluq layihə deyil: $(pwd)"; exit 1; }
'''


# ══════════════════════════════════════════════════════════════════════
_t("IB.1",
   "Build işləyir və dist/main.js yaranır",
   """ADDIM 12-də öyrəndiyimiz build-in <strong>həqiqətən</strong> işlədiyini
   yoxlayır. Test köhnə <code>dist/</code> qovluğunu tamamilə silir, sıfırdan
   build edir və vacib faylların yerində olduğunu yoxlayır. Əgər
   <code>tsconfig.build.json</code> səhv olsaydı (məsələn
   <code>rootDir</code> olmasaydı), fayllar <code>dist/src/main.js</code>
   kimi yaranardı və bu test uğursuz olardı.""",
   BAS + r'''
echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) Köhnə dist/ qovluğunu silirik (sıfırdan build yoxlaması)"
rm -rf dist
printf '      dist/ əvvəlcə → %s\n' "$([ -d dist ] && echo 'VAR' || echo 'yoxdur (silindi)')"

echo ""
echo "  → 2) npm run build"
npm run build
KOD=$?
printf '      exit kodu: %s\n' "$KOD"
[ "$KOD" -eq 0 ] || { echo "  ✗ BUILD UĞURSUZ — xəta mesajına baxın"; exit 1; }

echo ""
echo "  → 3) dist/ içində nə var?"
ls dist | sed 's/^/      /'

echo ""
echo "  → 4) vacib fayllar yerindədirmi?"
catmadi=0
for f in dist/main.js dist/app.module.js dist/prisma/prisma.service.js \
         dist/prisma/prisma.module.js \
         dist/saglamliq/saglamliq.service.js \
         dist/saglamliq/saglamliq.controller.js \
         dist/saglamliq/saglamliq.module.js \
         dist/common/filters/all-exceptions.filter.js \
         dist/generated/prisma/client.js; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ build nəticəsi natamamdır"; exit 1; }

echo ""
printf '  → cəmi .js fayl: %s\n' "$(find dist -name '*.js' | wc -l | tr -d ' ')"
printf '  → dist/main.js ölçüsü: %s bayt\n' "$(wc -c < dist/main.js | tr -d ' ')"

echo ""
echo "  ✓ IB.1 KEÇDİ — build sıfırdan işləyir və dist/main.js yaranır"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IB.2",
   "Tip yoxlaması təmizdir və səhvi tutur",
   """ADDIM 12-nin ikinci yarısını yoxlayır: <code>tsc --noEmit</code>.
   Test <strong>iki</strong> şeyi sübut edir: (1) layihədə tip xətası yoxdur;
   (2) qəsdən səhv kod yazsaq, kompilyator onu <em>tutur</em>. İkinci hissə
   olmasa, «hevk təmizdir» nəticəsi etibarsız olardı — bəlkə
   <code>tsc</code> ümumiyyətlə işləmir?""",
   BAS + r'''
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
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IB.3",
   "dist strukturu düzgündür və testlər build-ə düşmür",
   """ADDIM 12-də öyrəndiyimiz iki qaydanı yoxlayır:
   <code>rootDir</code> sayəsində yolların düzgün olması və
   <code>deleteOutDir: true</code> sayəsində köhnə faylların silinməsi.
   Həm də sübut edir ki, <code>exclude: ["**/*spec.ts"]</code> işləyir və
   test faylları istehsalat build-inə <strong>düşmür</strong>.""",
   BAS + r'''
echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) Təzə build"
npm run build >/dev/null 2>&1 || { echo "  ✗ build uğursuz oldu"; exit 1; }
echo "      ✓ build tamamlandı"

echo ""
echo "  → 2) Gözlənilən fayllar (rootDir düzgün işləyirmi?)"
catmadi=0
for f in dist/main.js dist/app.module.js \
         dist/prisma/prisma.service.js dist/prisma/prisma.module.js \
         dist/saglamliq/saglamliq.service.js \
         dist/saglamliq/saglamliq.controller.js \
         dist/saglamliq/saglamliq.module.js \
         dist/common/filters/all-exceptions.filter.js; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ dist strukturu natamamdır"; exit 1; }

echo ""
echo "  → 3) YANLIŞ yol olmamalıdır: dist/src/main.js"
if [ -f dist/src/main.js ]; then
  echo "      ✗ dist/src/main.js VAR — rootDir işləmir!"
  exit 1
fi
echo "      ✓ dist/src/main.js yoxdur (rootDir düzgündür)"

echo ""
echo "  → 4) Test faylları dist-ə DÜŞMƏMƏLİDİR"
SAY=$(find dist -name '*spec*' | wc -l | tr -d ' ')
find dist -name '*spec*' | sed 's/^/      /'
printf '      tapılan *spec* fayl sayı: %s\n' "$SAY"
[ "$SAY" -eq 0 ] || { echo "  ✗ testlər build-ə düşüb — exclude işləmir!"; exit 1; }
echo "      ✓ heç bir test faylı dist-ə düşməyib"

echo ""
echo "  → 5) deleteOutDir yoxlaması"
mkdir -p dist
echo "kohne" > dist/kohne_fayl.js
printf '      dist/kohne_fayl.js (build-dən əvvəl) → %s\n' "$([ -f dist/kohne_fayl.js ] && echo VAR || echo yoxdur)"
npm run build >/dev/null 2>&1
printf '      dist/kohne_fayl.js (build-dən sonra) → %s\n' "$([ -f dist/kohne_fayl.js ] && echo 'HƏLƏ DURUR' || echo silindi)"
[ -f dist/kohne_fayl.js ] && { echo "  ✗ deleteOutDir işləmədi"; exit 1; }
echo "      ✓ saxta köhnə fayl build zamanı silindi"

echo ""
echo "  ✓ IB.3 KEÇDİ — dist strukturu və deleteOutDir düzgündür"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IB.4",
   "Server qalxır və sağlamlıq endpointi 200 qaytarır",
   """ADDIM 13-ü avtomatlaşdırır: serveri arxa planda qaldırır, cavab
   verənə qədər gözləyir, <code>/api/v1/saglamliq</code> yolundan
   <code>200</code> alır və JSON-un <strong>bütün</strong> sahələrini
   yoxlayır. Test bitəndə serveri söndürür və portun boşaldığını təsdiqləyir
   — yəni arxada asılı proses qalmır.""",
   BAS + r'''
PORT="${PORT:-4000}"
LOQ="/tmp/arti_ib4_${PORT}.log"
CAVAB="/tmp/arti_ib4_${PORT}.json"

echo "  → Layihə: $(pwd)"
echo "  → Port:   $PORT"

echo ""
echo "  → 1) İlkin şərtlər"
[ -f dist/main.js ] || { echo "      ✗ dist/main.js yoxdur — əvvəlcə build edin (IB.1)"; exit 1; }
echo "      ✓ dist/main.js yerindədir"
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "      ✗ $PORT portu MƏŞĞULDUR:"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | sed 's/^/          /'
  echo "      Həll: kill <PID> və ya PORT=4100 ilə işlədin"
  exit 1
fi
echo "      ✓ $PORT portu boşdur"

echo ""
echo "  → 2) Serveri arxa planda qaldırırıq"
PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
temizle() { kill "$PID" 2>/dev/null; wait "$PID" 2>/dev/null; true; }
trap temizle EXIT INT TERM
printf '      PID %s, loq: %s\n' "$PID" "$LOQ"

echo ""
echo "  → 3) Cavab verənə qədər gözləyirik (maks. 30 saniyə)"
hazir=0
i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  if curl -fsS "http://localhost:$PORT/api/v1/saglamliq" -o "$CAVAB" 2>/dev/null; then
    hazir=1
    break
  fi
  if ! kill -0 "$PID" 2>/dev/null; then
    echo "      ✗ server prosesi dayandı! Loqun sonu:"
    tail -n 20 "$LOQ" | sed 's/^/          /'
    exit 1
  fi
  sleep 0.5
done
[ "$hazir" = "1" ] || { echo "      ✗ server 30 saniyə içində cavab vermədi"; tail -n 20 "$LOQ" | sed 's/^/          /'; exit 1; }
printf '      ✓ server hazırdır (%s cəhddən sonra)\n' "$i"

echo ""
echo "  → 4) Status kodu"
KOD=$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:$PORT/api/v1/saglamliq")
printf '      GET /api/v1/saglamliq → %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "      ✗ 200 gözlənilirdi, alındı: $KOD"; exit 1; }
echo "      ✓ 200 OK"

echo ""
echo "  → 5) Cavab gövdəsi"
printf '%s\n' "$(cat "$CAVAB")" | sed 's/^/      /'
printf '      Content-Type: %s\n' "$(curl -s -o /dev/null -D - "http://localhost:$PORT/api/v1/saglamliq" | grep -i '^content-type' | tr -d '\r')"

echo ""
echo "  → 6) JSON sahələrinin dəqiq yoxlanması"
python3 - "$CAVAB" <<'PSON'
import json
import sys

d = json.load(open(sys.argv[1], encoding='utf-8'))
problem = []

if d.get('status') != 'saglam':
    problem.append("status 'saglam' deyil: %r" % d.get('status'))
b = d.get('baza') or {}
if b.get('qosulub') is not True:
    problem.append("baza.qosulub true deyil: %r" % b.get('qosulub'))
if b.get('cedvel_sayi') != 48:
    problem.append("baza.cedvel_sayi 48 deyil: %r" % b.get('cedvel_sayi'))
if not isinstance(b.get('gecikme_ms'), int):
    problem.append("baza.gecikme_ms tam ədəd deyil: %r" % b.get('gecikme_ms'))
if d.get('versiya') != '0.1.0':
    problem.append("versiya '0.1.0' deyil: %r" % d.get('versiya'))
if not isinstance(d.get('vaxt'), str) or 'T' not in str(d.get('vaxt')):
    problem.append("vaxt ISO mətn deyil: %r" % d.get('vaxt'))

for p in problem:
    print('      ✗ ' + p)
if problem:
    sys.exit(1)
print('      ✓ status, baza.qosulub, cedvel_sayi, gecikme_ms, versiya, vaxt — hamısı düzgündür')
PSON
[ $? -eq 0 ] || { echo "  ✗ JSON yoxlaması uğursuz oldu"; exit 1; }

echo ""
echo "  → 7) Serveri söndürürük və portu yoxlayırıq"
kill "$PID" 2>/dev/null
wait "$PID" 2>/dev/null
sleep 1
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "      ✗ server söndürülməsinə baxmayaraq port məşğuldur"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | sed 's/^/          /'
  exit 1
fi
echo "      ✓ server söndü, port boşdur"

echo ""
echo "  ✓ IB.4 KEÇDİ — server qalxır, sağlamlıq 200 qaytarır, təmiz sönür"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IB.5",
   "API prefiksi (/api/v1) işləyir",
   """ADDIM 13-də gördüyümüz <strong>mənfi yoxlamanı</strong> rəsmiləşdirir.
   <code>setGlobalPrefix('api/v1')</code> sətri silinsəydi, bütün
   <code>/api/v1/...</code> sorğuları <code>404</code> alardı — bu test
   həmin səhvi dərhal tutur. Eyni zamanda prefikssiz yolların
   <code>404</code> qaytardığını yoxlayır ki, prefiksin həqiqətən
   <em>tətbiq olunduğuna</em> əmin olaq.""",
   BAS + r'''
PORT="${PORT:-4000}"
LOQ="/tmp/arti_ib5_${PORT}.log"

echo "  → Port: $PORT"

[ -f dist/main.js ] || { echo "  ✗ dist/main.js yoxdur — əvvəlcə build edin (IB.1)"; exit 1; }
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "  ✗ $PORT portu məşğuldur"; exit 1
fi

PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
temizle() { kill "$PID" 2>/dev/null; wait "$PID" 2>/dev/null; true; }
trap temizle EXIT INT TERM

hazir=0
i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  curl -fsS "http://localhost:$PORT/api/v1" -o /dev/null 2>/dev/null && { hazir=1; break; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.5
done
[ "$hazir" = "1" ] || { echo "  ✗ server cavab vermədi"; tail -n 20 "$LOQ" | sed 's/^/      /'; exit 1; }
printf '  ✓ server hazırdır (%s cəhddən sonra)\n' "$i"

kod() { curl -s -o /dev/null -w '%{http_code}' "http://localhost:$PORT$1"; }

echo ""
echo "  → Yolların status kodları"
XETA=0
yoxla() {
  N=$(kod "$1")
  if [ "$N" = "$2" ]; then
    printf '      ✓ %-24s → %s\n' "$1" "$N"
  else
    printf '      ✗ %-24s → %s  (gözlənilirdi: %s)\n' "$1" "$N" "$2"
    XETA=1
  fi
}
yoxla "/api/v1"                 200
yoxla "/api/v1/saglamliq"       200
yoxla "/docs"                   200
yoxla "/saglamliq"              404
yoxla "/"                       404
yoxla "/api/saglamliq"          404
yoxla "/api/v2/saglamliq"       404

echo ""
[ "$XETA" -eq 0 ] || { echo "  ✗ bəzi yollar gözlənilən statusu qaytarmadı"; exit 1; }

echo "  → Kök endpoint-in cavabı:"
curl -s "http://localhost:$PORT/api/v1" | sed 's/^/      /'
echo ""
printf '%s' "$(curl -s "http://localhost:$PORT/api/v1")" | grep -q '/api/v1' \
  || { echo "  ✗ /api/v1 cavabında prefiks məlumatı yoxdur"; exit 1; }
echo "      ✓ cavabda prefiks məlumatı var"

echo ""
echo "  ✓ IB.5 KEÇDİ — prefiks işləyir, prefikssiz yollar 404 qaytarır"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IB.6",
   "Xətalar vahid formatdadır (AllExceptionsFilter)",
   """1A-nın ADDIM 8-də yazdığımız <code>AllExceptionsFilter</code> həqiqətən
   işləyirmi? Bu test <code>404</code> və <code>400</code> xətalarının
   <strong>eyni</strong> JSON quruluşunda qaytarıldığını yoxlayır:
   <code>ugur</code>, <code>xeta.kod</code>, <code>xeta.mesaj</code>,
   <code>yol</code>, <code>vaxt</code>. Filtr olmasaydı, Nest öz standart cavabını verərdi
   (<code>statusCode</code>, <code>message</code>, <code>error</code>) və
   frontend hər endpoint üçün ayrı format yazmalı olardı.""",
   BAS + r'''
PORT="${PORT:-4000}"
LOQ="/tmp/arti_ib6_${PORT}.log"

echo "  → Port: $PORT"

[ -f dist/main.js ] || { echo "  ✗ dist/main.js yoxdur — əvvəlcə build edin (IB.1)"; exit 1; }
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "  ✗ $PORT portu məşğuldur"; exit 1
fi

PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
temizle() { kill "$PID" 2>/dev/null; wait "$PID" 2>/dev/null; true; }
trap temizle EXIT INT TERM

hazir=0
i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  curl -fsS "http://localhost:$PORT/api/v1/saglamliq" -o /dev/null 2>/dev/null && { hazir=1; break; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.5
done
[ "$hazir" = "1" ] || { echo "  ✗ server cavab vermədi"; tail -n 20 "$LOQ" | sed 's/^/      /'; exit 1; }
printf '  ✓ server hazırdır (%s cəhddən sonra)\n' "$i"

echo ""
echo "  → GET /api/v1/yoxdur (mövcud olmayan yol)"
curl -s -o /tmp/ib6a.json -w '      status kodu: %{http_code}\n' "http://localhost:$PORT/api/v1/yoxdur"
printf '      gövdə: %s\n' "$(cat /tmp/ib6a.json)"

echo ""
echo "  → GET /api/v1/yoxdur/123 (alt yol da eyni formatda olmalıdır)"
curl -s -o /tmp/ib6b.json -w '      status kodu: %{http_code}\n' "http://localhost:$PORT/api/v1/yoxdur/123"
printf '      gövdə: %s\n' "$(cat /tmp/ib6b.json)"

echo ""
echo "  → JSON quruluşunun yoxlanması"
python3 - /tmp/ib6a.json /tmp/ib6b.json <<'PSON'
import json
import sys

# Filtrin REAL formatı (all-exceptions.filter.ts) — ADDIM 8:
#   { ugur: false, xeta: { kod, mesaj, detallar? }, yol, vaxt }
GEREKLI = {'ugur', 'xeta', 'yol', 'vaxt'}
ICAZELI = {'kod', 'mesaj', 'detallar'}
problem = []
gorulen = []

for fayl in sys.argv[1:]:
    d = json.load(open(fayl, encoding='utf-8'))
    ad = fayl.split('/')[-1]
    gorulen.append(d)

    if set(d.keys()) != GEREKLI:
        problem.append("%s: gözlənilən açarlar %s, alındı %s"
                       % (ad, sorted(GEREKLI), sorted(d.keys())))

    if d.get('ugur') is not False:
        problem.append("%s: 'ugur' false deyil: %r" % (ad, d.get('ugur')))

    x = d.get('xeta')
    if not isinstance(x, dict):
        problem.append("%s: 'xeta' obyekt deyil: %r" % (ad, x))
    else:
        if not {'kod', 'mesaj'} <= set(x.keys()):
            problem.append("%s: xeta içində kod/mesaj yoxdur: %s"
                           % (ad, sorted(x.keys())))
        if set(x.keys()) - ICAZELI:
            problem.append("%s: xeta içində gözlənilməz açar: %s"
                           % (ad, sorted(set(x.keys()) - ICAZELI)))
        if x.get('kod') != 'TAPILMADI':
            problem.append("%s: xeta.kod 'TAPILMADI' deyil: %r" % (ad, x.get('kod')))
        if not isinstance(x.get('mesaj'), str) or not x.get('mesaj'):
            problem.append("%s: xeta.mesaj boşdur: %r" % (ad, x.get('mesaj')))

    if not isinstance(d.get('yol'), str) or not d.get('yol').startswith('/'):
        problem.append("%s: 'yol' düzgün mətn deyil: %r" % (ad, d.get('yol')))

    if not isinstance(d.get('vaxt'), str) or 'T' not in str(d.get('vaxt')):
        problem.append("%s: 'vaxt' ISO mətn deyil: %r" % (ad, d.get('vaxt')))

    # Nest-in STANDART formatı olmamalıdır:
    for a in ('statusCode', 'message', 'error'):
        if a in d:
            problem.append("%s: Nest standart formatı görünür ('%s') "
                           "— filtr işləmir!" % (ad, a))

    print('      %s → %s' % (ad, json.dumps(d, ensure_ascii=False)))

# ƏN GÜCLÜ YOXLAMA: iki FƏRQLİ xəta EYNİ quruluşdadır
a, b = gorulen
if set(a.keys()) != set(b.keys()):
    problem.append("iki xətanın açarları fərqlidir: %s vs %s"
                   % (sorted(a.keys()), sorted(b.keys())))
if set(a['xeta'].keys()) != set(b['xeta'].keys()):
    problem.append("iki xətanın xeta açarları fərqlidir: %s vs %s"
                   % (sorted(a['xeta'].keys()), sorted(b['xeta'].keys())))
if a.get('yol') == b.get('yol'):
    problem.append("iki sorğu fərqli yollara getməli idi")

for p in problem:
    print('      ✗ ' + p)
if problem:
    sys.exit(1)
print('      ✓ hər iki xəta EYNİ vahid formatdadır:')
print('        ugur / xeta.kod / xeta.mesaj / yol / vaxt')
print('      ✓ Nest-in standart statusCode/message/error formatı YOXDUR')
PSON
[ $? -eq 0 ] || { echo "  ✗ vahid xəta formatı yoxlaması uğursuz oldu"; exit 1; }

echo ""
echo "  ✓ IB.6 KEÇDİ — bütün xətalar vahid formatdadır"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IB.7",
   "Port məşğul olanda aydın xəta, təmizlik isə zəmanətlidir",
   """ADDIM 13-də yazdığımız <code>skriptler/servis_yoxla.sh</code> faylının
   <strong>iki</strong> ssenarisini yoxlayır. (1) Port məşğul olanda skript
   serveri qaldırmağa cəhd etməməli, tutan prosesin PID-ini göstərməli və
   <code>exit 1</code> ilə dayanmalıdır. (2) Port boş olanda işləməli və
   <em>bitəndə portu boş qoymalıdır</em> — bu, <code>trap</code> təmizliyinin
   sübutudur.""",
   BAS + r'''
[ -f skriptler/servis_yoxla.sh ] || { echo "  ✗ skriptler/servis_yoxla.sh yoxdur — ADDIM 13-ü işlədin"; exit 1; }
echo "  ✓ servis_yoxla.sh yerindədir"

PORT="${PORT:-4000}"
echo "  → İstifadə olunan port: $PORT"

echo ""
echo "  → 1) Portun BOŞ olduğunu yoxlayırıq"
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "      ✗ $PORT portu artıq məşğuldur — test başlaya bilməz"
  exit 1
fi
echo "      ✓ boşdur"

echo ""
echo "  → 2) Portu SÜNİ olaraq tuturuq (python http.server)"
python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
TUTAN=$!
temizle() {
  kill "$TUTAN" 2>/dev/null
  wait "$TUTAN" 2>/dev/null
  true
}
trap temizle EXIT INT TERM
sleep 1.5

if ! lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "      ✗ süni tutucu qalxa bilmədi"
  exit 1
fi
echo "      ✓ port indi məşğuldur:"
lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | sed 's/^/          /'

echo ""
echo "  → 3) servis_yoxla.sh MƏŞĞUL portla — rədd etməlidir"
CIXIS=$(PORT="$PORT" bash skriptler/servis_yoxla.sh 2>&1)
KOD=$?
printf '%s\n' "$CIXIS" | sed 's/^/      /'
printf '      exit kodu: %s\n' "$KOD"

[ "$KOD" -eq 1 ] || { echo "  ✗ skript məşğul portu TANIMADI (exit 0 verdi)"; exit 1; }
echo "      ✓ exit 1 qaytardı"

printf '%s' "$CIXIS" | grep -q 'MƏŞĞUL' || { echo "  ✗ xəbərdarlıq mətni yoxdur"; exit 1; }
echo "      ✓ problemi aydın Azərbaycanca bildirdi"

printf '%s' "$CIXIS" | grep -q "$TUTAN" || { echo "  ✗ tutan prosesin PID-i göstərilmədi"; exit 1; }
echo "      ✓ tutan prosesin PID-ini ($TUTAN) göstərdi"

printf '%s' "$CIXIS" | grep -q 'Server hazırdır' && { echo "  ✗ skript serveri qaldırmağa cəhd ETDİ!"; exit 1; }
echo "      ✓ serveri qaldırmağa cəhd belə etmədi"

echo ""
echo "  → 4) Süni tutucunu dayandırırıq"
kill "$TUTAN" 2>/dev/null
wait "$TUTAN" 2>/dev/null
sleep 1.5
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "      ✗ port hələ məşğuldur"; exit 1
fi
echo "      ✓ port boşdur"

echo ""
echo "  → 5) servis_yoxla.sh BOŞ portla — işləməlidir"
PORT="$PORT" bash skriptler/servis_yoxla.sh
KOD=$?
printf '      exit kodu: %s\n' "$KOD"
[ "$KOD" -eq 0 ] || { echo "  ✗ skript boş portda uğursuz oldu"; exit 1; }
echo "      ✓ exit 0 qaytardı"

echo ""
echo "  → 6) Skript bitdikdən sonra port BOŞ qalmalıdır (trap təmizliyi)"
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "      ✗ port məşğul qaldı — trap təmizliyi işləmədi"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | sed 's/^/          /'
  exit 1
fi
echo "      ✓ port boşdur — arxada asılı proses qalmadı"

echo ""
echo "  ✓ IB.7 KEÇDİ — port idarəsi və təmizlik zəmanətlidir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IB.8",
   "Vitest konfiqurasiyaları düzgün ayrılıb",
   """ADDIM 14-də qurduğumuz <strong>iki</strong> konfiqurasiyanın həqiqətən
   işlədiyini yoxlayır: vahid konfiqurasiyası yalnız
   <code>src/**/*.spec.ts</code> fayllarını, e2e konfiqurasiyası isə yalnız
   <code>test/**/*.e2e-spec.ts</code> fayllarını görməlidir. Test
   <code>vitest list</code> əmrindən istifadə edir — bu əmr testləri
   <em>işlətmədən</em> sadəcə siyahısını çıxarır.""",
   BAS + r'''
echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) Konfiqurasiya faylları varmı?"
catmadi=0
for f in vitest.config.ts vitest.config.e2e.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ konfiqurasiya faylları natamamdır"; exit 1; }

echo ""
echo "  → 2) Vitest qurulubmu?"
V=$(npx vitest --version 2>&1 | tail -n 1)
printf '      %s\n' "$V"
printf '%s' "$V" | grep -q 'vitest/' || { echo "  ✗ vitest işləmir"; exit 1; }

echo ""
echo "  → 3) package.json skriptləri"
for s in test test:unit test:izle test:e2e; do
  D=$(npm pkg get "scripts.$s" 2>/dev/null)
  printf '      %-12s → %s\n' "$s" "$D"
  [ "$D" = '{}' ] && { echo "  ✗ '$s' skripti yoxdur"; exit 1; }
done
npm pkg get "scripts.test:e2e" 2>/dev/null | grep -q 'vitest.config.e2e.ts' \
  || { echo "  ✗ test:e2e skripti e2e konfiqurasiyasına işarə etmir"; exit 1; }
echo "      ✓ bütün dörd skript mövcuddur və düzgün əmrlərə işarə edir"

echo ""
echo "  → 4) Vahid konfiqurasiyası hansı testləri görür?"
ULIST=$(npx vitest list --config vitest.config.ts 2>&1)
USAY=$(printf '%s\n' "$ULIST" | grep -c . )
printf '%s\n' "$ULIST" | sed 's/^/      /'
printf '      cəmi: %s test\n' "$USAY"

echo ""
echo "  → 5) E2E konfiqurasiyası hansı testləri görür?"
ELIST=$(npx vitest list --config vitest.config.e2e.ts 2>&1)
ESAY=$(printf '%s\n' "$ELIST" | grep -c . )
printf '%s\n' "$ELIST" | sed 's/^/      /'
printf '      cəmi: %s test\n' "$ESAY"

echo ""
echo "  → 6) Ayrı-seçkilik yoxlaması"
printf '%s' "$ULIST" | grep -q 'e2e-spec' && { echo "      ✗ e2e testlər vahid dəstinə SIZIB!"; exit 1; }
echo "      ✓ vahid dəstində e2e test yoxdur"
printf '%s' "$ELIST" | grep -q 'service.spec' && { echo "      ✗ vahid testlər e2e dəstinə SIZIB!"; exit 1; }
echo "      ✓ e2e dəstində vahid test yoxdur"
printf '%s' "$ULIST" | grep -q 'vitest.saltsiz' && { echo "      ✗ müvəqqəti konfiqurasiya qalıb"; exit 1; }

[ "$USAY" -eq 3 ] || { echo "      ✗ vahid dəstində 3 test gözlənilirdi, alındı: $USAY"; exit 1; }
[ "$ESAY" -eq 4 ] || { echo "      ✗ e2e dəstində 4 test gözlənilirdi, alındı: $ESAY"; exit 1; }
echo "      ✓ vahid dəst: 3 test — e2e dəst: 4 test"

echo ""
echo "  → 7) Konfiqurasiya fayllarının vacib ayarları"
grep -q "include: \['src/\*\*/\*.spec.ts'\]" vitest.config.ts \
  || { echo "      ✗ vahid include ayarı gözlənilən deyil"; exit 1; }
echo "      ✓ vahid include: src/**/*.spec.ts"
grep -q 'fileParallelism: false' vitest.config.e2e.ts \
  || { echo "      ✗ e2e konfiqurasiyasında fileParallelism: false yoxdur"; exit 1; }
echo "      ✓ e2e fileParallelism: false (ardıcıl işləyir)"
grep -q 'testTimeout: 30_000' vitest.config.e2e.ts \
  || { echo "      ✗ e2e testTimeout ayarı yoxdur"; exit 1; }
echo "      ✓ e2e testTimeout: 30 saniyə"

echo ""
echo "  ✓ IB.8 KEÇDİ — iki konfiqurasiya düzgün ayrılıb"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IB.9",
   "Vahid testlər keçir və bazadan asılı deyil",
   """ADDIM 15-in nəticəsini yoxlayır. İki hissə var: (1) üç vahid test
   keçməlidir; (2) <code>DATABASE_URL</code> qəsdən mövcud olmayan bazaya
   yönləndirildikdə də testlər <strong>keçməlidir</strong> — çünki saxta
   (mock) <code>PrismaService</code> sayəsində baza heç soruşulmur. İkinci
   hissə olmasa, «testlər keçir» nəticəsi bazanın işləməsindən asılı olardı
   və bu, vahid test anlayışına zidd olardı.""",
   BAS + r'''
[ -f src/saglamliq/saglamliq.service.spec.ts ] \
  || { echo "  ✗ src/saglamliq/saglamliq.service.spec.ts yoxdur — ADDIM 15-i işlədin"; exit 1; }
echo "  ✓ test faylı yerindədir"

echo ""
echo "  → 1) Vahid testləri işlədirik"
CIXIS=$(npx vitest run 2>&1)
KOD=$?
printf '%s\n' "$CIXIS" | tail -n 12 | sed 's/^/      /'
printf '      exit kodu: %s\n' "$KOD"
[ "$KOD" -eq 0 ] || { echo "  ✗ vahid testlər UĞURSUZ oldu"; exit 1; }

echo ""
echo "  → 2) Nəticənin dəqiq yoxlanması"
printf '%s' "$CIXIS" | grep -q 'Tests  3 passed' \
  || { echo "      ✗ 'Tests 3 passed' gözlənilirdi"; exit 1; }
echo "      ✓ 3 test keçdi"
printf '%s' "$CIXIS" | grep -q 'Test Files  1 passed' \
  || { echo "      ✗ 'Test Files 1 passed' gözlənilirdi"; exit 1; }
echo "      ✓ 1 test faylı işlədi (yalnız vahid faylı)"
printf '%s' "$CIXIS" | grep -q 'e2e-spec' \
  && { echo "      ✗ e2e testlər də işlədi — konfiqurasiya səhvdir"; exit 1; }
echo "      ✓ e2e testlər qarışmadı"

echo ""
echo "  → 3) Üç testin adı çıxışda görünürmü?"
VERBOSE=$(npx vitest run --reporter=verbose 2>&1)
printf '%s\n' "$VERBOSE" | grep '✓' | sed 's/^/      /'
SATIR=$(printf '%s\n' "$VERBOSE" | grep -c '✓ src/saglamliq')
[ "$SATIR" -ge 3 ] || { echo "      ✗ 3 test adı gözlənilirdi, tapıldı: $SATIR"; exit 1; }
echo "      ✓ hər üç test adı ilə görünür"

echo ""
echo "  → 4) SÜBUT: vahid testlər BAZADAN ASILI DEYİL"
echo "      DATABASE_URL-i qəsdən mövcud olmayan bazaya yönləndiririk"
echo "      (localhost:9999 — orada heç nə yoxdur)"
CIXIS2=$(env -u DATABASE_URL -u PGHOST \
  DATABASE_URL="postgresql://yoxdur:yoxdur@localhost:9999/yoxdur" \
  npx vitest run 2>&1)
KOD2=$?
printf '%s\n' "$CIXIS2" | tail -n 8 | sed 's/^/      /'
printf '      exit kodu: %s\n' "$KOD2"
[ "$KOD2" -eq 0 ] || { echo "  ✗ vahid testlər bazadan ASILIDIR — təcrid pozulub!"; exit 1; }
printf '%s' "$CIXIS2" | grep -q 'Tests  3 passed' \
  || { echo "      ✗ bazasız halda 3 test keçmədi"; exit 1; }
echo "      ✓ bazasız halda da 3/3 keçdi — saxta PrismaService işləyir"

echo ""
echo "  → 5) Test təmizliyi: müvəqqəti fayllar qalmayıb?"
for f in src/saglamliq/_muveqqeti.spec.ts src/_ib2_tip.ts src/_tip_yoxlamasi.ts; do
  [ -f "$f" ] && { echo "      ✗ $f QALIB"; exit 1; }
done
echo "      ✓ müvəqqəti fayl yoxdur"

echo ""
echo "  ✓ IB.9 KEÇDİ — vahid testlər keçir və bazadan asılı deyil"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IB.10",
   "E2E testlər keçir, bazadan asılıdır və build-ə düşmür",
   """ADDIM 16-nın nəticəsini yoxlayır — dərsin ən vacib testi. Üç hissə:
   (1) dörd e2e test real bazanın iştirakı ilə keçməlidir; (2)
   <code>DATABASE_URL</code> yanlış verildikdə <strong>keçməməlidir</strong>
   — bu, e2e testin həqiqətən bazaya toxunduğunu sübut edir; (3) heç bir
   test faylı <code>dist/</code> içinə düşməməlidir.""",
   BAS + r'''
[ -f test/saglamliq.e2e-spec.ts ] \
  || { echo "  ✗ test/saglamliq.e2e-spec.ts yoxdur — ADDIM 16-nı işlədin"; exit 1; }
echo "  ✓ e2e test faylı yerindədir"

echo ""
echo "  → 1) E2E testləri işlədirik (npm run test:e2e)"
CIXIS=$(npm run test:e2e 2>&1)
KOD=$?
printf '%s\n' "$CIXIS" | tail -n 14 | sed 's/^/      /'
printf '      exit kodu: %s\n' "$KOD"
[ "$KOD" -eq 0 ] || { echo "  ✗ e2e testlər UĞURSUZ oldu (baza işləyirmi?)"; exit 1; }

echo ""
echo "  → 2) Nəticənin dəqiq yoxlanması"
printf '%s' "$CIXIS" | grep -q 'Tests  4 passed' \
  || { echo "      ✗ 'Tests 4 passed' gözlənilirdi"; exit 1; }
echo "      ✓ 4 test keçdi"
printf '%s' "$CIXIS" | grep -q 'Test Files  1 passed' \
  || { echo "      ✗ 'Test Files 1 passed' gözlənilirdi"; exit 1; }
echo "      ✓ 1 e2e faylı işlədi"

echo ""
echo "  → 3) Dörd testin adı (verbose)"
VERBOSE=$(npx vitest run --config vitest.config.e2e.ts --reporter=verbose 2>&1)
printf '%s\n' "$VERBOSE" | grep '✓' | sed 's/^/      /'
SATIR=$(printf '%s\n' "$VERBOSE" | grep -c '✓ test/saglamliq.e2e-spec.ts')
[ "$SATIR" -ge 4 ] || { echo "      ✗ 4 test adı gözlənilirdi, tapıldı: $SATIR"; exit 1; }
echo "      ✓ hər dörd test adı ilə görünür"

echo ""
echo "  → 4) SÜBUT: e2e testlər BAZADAN ASILIDIR"
echo "      DATABASE_URL-i qəsdən mövcud olmayan bazaya yönləndiririk."
echo "      Vahid testlər bu halda KEÇİRDİ (IB.9) — indi KEÇMƏMƏLİDİR:"
CIXIS2=$(env -u DATABASE_URL -u PGHOST \
  DATABASE_URL="postgresql://yoxdur:yoxdur@localhost:9999/yoxdur" \
  npx vitest run --config vitest.config.e2e.ts 2>&1)
KOD2=$?
printf '%s\n' "$CIXIS2" | tail -n 10 | sed 's/^/      /'
printf '      exit kodu: %s (0 OLMAMALIDIR)\n' "$KOD2"
[ "$KOD2" -ne 0 ] || { echo "  ✗ e2e testlər bazasız KEÇDİ — bu mümkün deyil!"; exit 1; }
printf '%s' "$CIXIS2" | grep -q 'failed' \
  || { echo "      ✗ uğursuzluq hesabatı gözlənilirdi"; exit 1; }
printf '%s' "$CIXIS2" | grep -q '3 passed' \
  || { echo "      ✗ digər 3 test keçməli idi (onlar bazaya toxunmur)"; exit 1; }
echo "      ✓ bazasız halda 1 test uğursuz oldu, 3-ü keçdi — gözlənilən nəticə"

echo ""
echo "  → 5) Test faylları build-ə düşürmü?"
npm run build >/dev/null 2>&1 || { echo "  ✗ build uğursuz"; exit 1; }
SAY=$(find dist -name '*spec*' | wc -l | tr -d ' ')
printf '      dist içində *spec* fayl sayı: %s\n' "$SAY"
[ "$SAY" -eq 0 ] || { echo "  ✗ testlər dist-ə düşüb!"; exit 1; }
echo "      ✓ heç bir test faylı build-ə düşməyib"

echo ""
echo "  → 6) YEKUN: hər şey bir yerdə"
printf '      tip yoxlaması: '
npx tsc --noEmit && echo "✓ təmiz"
printf '      vahid testlər: '
npx vitest run 2>&1 | grep 'Tests ' | sed 's/^ *//'
printf '      e2e testlər:   '
npx vitest run --config vitest.config.e2e.ts 2>&1 | grep 'Tests ' | sed 's/^ *//'

echo ""
echo "  ✓ IB.10 KEÇDİ — e2e testlər bütöv sistemi yoxlayır"
''')
