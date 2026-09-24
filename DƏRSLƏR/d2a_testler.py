#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-2A — 10 yekun test (IIA.1 … IIA.10).

Hər test müstəqildir. Testlər `LAYIHE` mühit dəyişənini oxuyur
(standart: $HOME/Deepseek_ARTI/DS_Backend) və öz serverlərini özləri
qaldırıb söndürürlər.

⚠️ TƏHLÜKƏSİZLİK: heç bir test mövcud 14 əməkdaşa zərər vermir.
Yazma əməliyyatları YALNIZ testin özünün yaratdığı müvəqqəti sətirlər
üzərindədir və `trap` ilə həmişə təmizlənir.
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
[ -f .env ] || { echo "  ✗ .env yoxdur — DATABASE_URL tapılmır"; exit 1; }
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
[ -n "$DBURL" ] || { echo "  ✗ .env-də DATABASE_URL yoxdur"; exit 1; }
say()  { psql "$DBURL" -At -c "$1" 2>/dev/null | tr -d ' '; }
'''

SERVER = r'''
PORT="${PORT:-4000}"
LOQ="/tmp/arti_iia_${PORT}.log"
BAZ="http://localhost:$PORT/api/v1/emekdaslar"

npm run build >/tmp/arti_iia_build.log 2>&1 \
  || { echo "  ✗ build uğursuz"; tail -n 20 /tmp/arti_iia_build.log | sed 's/^/      /'; exit 1; }

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "  ✗ $PORT portu məşğuldur"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | sed 's/^/      /'
  exit 1
fi

PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
temizle() {
  [ -n "$PID" ] && kill "$PID" 2>/dev/null
  [ -n "$PID" ] && wait "$PID" 2>/dev/null
  true
}
trap temizle EXIT INT TERM

hazir=0
i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  curl -fsS "http://localhost:$PORT/api/v1/saglamliq" -o /dev/null 2>/dev/null && { hazir=1; break; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.5
done
[ "$hazir" = "1" ] || { echo "  ✗ server qalxmadı"; tail -n 20 "$LOQ" | sed 's/^/      /'; exit 1; }
printf '  ✓ server hazırdır (%s cəhd)\n' "$i"

kod()    { curl -s -o /dev/null -w '%{http_code}' "$@"; }
govde()  { curl -s "$@"; }
'''


# ══════════════════════════════════════════════════════════════════════
_t("IIA.1",
   "DTO-lar mövcuddur və bütün validasiya qaydaları işləyir",
   """ADDIM 17-də yazdığımız üç DTO-nu və <strong>25 validasiya
   qaydasını</strong> yoxlayır. Skript <code>main.ts</code>-dəki
   <em>eyni</em> <code>ValidationPipe</code>-ı işlədir, ona görə nəticə
   canlı API-nin nəticəsi ilə üst-üstə düşür. Test həm də yoxlayır ki,
   DTO-larda Azərbaycanca xəta mesajları var — istifadəçi üçün vacibdir.""",
   BAS + r'''
echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) DTO faylları"
catmadi=0
for f in src/emekdaslar/dto/emekdas-sorgu.dto.ts \
         src/emekdaslar/dto/emekdas-yarat.dto.ts \
         src/emekdaslar/dto/emekdas-yenile.dto.ts \
         skriptler/dto_yoxla.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ DTO faylları natamamdır — ADDIM 17-ni işlədin"; exit 1; }

echo ""
echo "  → 2) Qaydaların sayı"
IS=$(grep -c '@Is' src/emekdaslar/dto/*.ts | awk -F: '{s+=$2} END {print s}')
MSJ=$(grep -c 'message:' src/emekdaslar/dto/*.ts | awk -F: '{s+=$2} END {print s}')
printf '      @Is… dekoratoru      : %s\n' "$IS"
printf '      Azərbaycanca mesaj   : %s\n' "$MSJ"
[ "$IS" -ge 45 ] || { echo "  ✗ @Is dekoratorlarının sayı azdır: $IS"; exit 1; }
[ "$MSJ" -ge 30 ] || { echo "  ✗ Azərbaycanca mesajların sayı azdır: $MSJ"; exit 1; }
echo "      ✓ hər qaydanın öz mesajı var"

echo ""
echo "  → 3) Ağ siyahı (allowlist) varmı?"
grep -q 'SIRALANA_BILEN' src/emekdaslar/dto/emekdas-sorgu.dto.ts \
  || { echo "      ✗ sıralama ağ siyahısı yoxdur!"; exit 1; }
grep -q '@IsIn' src/emekdaslar/dto/emekdas-sorgu.dto.ts \
  || { echo "      ✗ @IsIn dekoratoru yoxdur!"; exit 1; }
echo "      ✓ sıralama yalnız icazəli sütunlarla məhdudlaşır"

echo ""
echo "  → 4) Tip yoxlaması"
npx tsc --noEmit || { echo "  ✗ tip xətası var"; exit 1; }
echo "      ✓ təmiz"

echo ""
echo "  → 5) REAL validasiya matrisi"
npx tsx skriptler/dto_yoxla.ts
CIXIS=$?
[ "$CIXIS" -eq 0 ] || { echo "  ✗ validasiya matrisi uğursuz oldu (exit $CIXIS)"; exit 1; }

echo ""
echo "  ✓ IIA.1 KEÇDİ — DTO-lar tamdır və 25 qayda işləyir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIA.2",
   "BigInt və Decimal problemi həll olunub (mapper işləyir)",
   """ADDIM 18-in ən vacib nəticəsini yoxlayır. Test <strong>iki</strong>
   şeyi təsdiqləyir: (1) xam baza sətri JSON-a çevrilmir (problem
   həqiqətən var); (2) mapper-dən sonra çevrilir (həll işləyir). Əgər
   yalnız ikincisini yoxlasaydıq, problem vaxtı ilə geri qayıda bilərdi.""",
   BAS + r'''
[ -f src/emekdaslar/dto/emekdas-cavab.dto.ts ] \
  || { echo "  ✗ emekdas-cavab.dto.ts yoxdur — ADDIM 18-i işlədin"; exit 1; }
[ -f skriptler/mapper_yoxla.ts ] \
  || { echo "  ✗ skriptler/mapper_yoxla.ts yoxdur"; exit 1; }
echo "  ✓ mapper faylları yerindədir"

echo ""
echo "  → 1) Mapper-in vacib hissələri"
grep -q 'String(e.id)' src/emekdaslar/dto/emekdas-cavab.dto.ts \
  || { echo "      ✗ id BigInt-dən mətnə çevrilmir!"; exit 1; }
echo "      ✓ id → String()"
grep -q 'toFixed(2)' src/emekdaslar/dto/emekdas-cavab.dto.ts \
  || { echo "      ✗ maas toFixed(2) ilə formatlanmır!"; exit 1; }
echo "      ✓ maas → toFixed(2)"
grep -q 'slice(0, 10)' src/emekdaslar/dto/emekdas-cavab.dto.ts \
  || { echo "      ✗ tarixlər yalnız günə kəsilmir!"; exit 1; }
echo "      ✓ tarixlər → YYYY-MM-DD"
grep -q 'as const' src/emekdaslar/dto/emekdas-cavab.dto.ts \
  || { echo "      ✗ EMEKDAS_SECIM-də as const yoxdur!"; exit 1; }
echo "      ✓ select sabiti as const ilə"

echo ""
echo "  → 2) select (include yox) işlədilir?"
N=$(grep -c 'select: EMEKDAS_SECIM' src/emekdaslar/emekdaslar.service.ts || true)
printf '      select: EMEKDAS_SECIM → %s yerdə
' "$N"
[ "$N" -ge 4 ] || { echo "      ✗ servis select işlətmir (include ola bilər)!"; exit 1; }
grep -q 'include:' src/emekdaslar/emekdaslar.service.ts \
  && { echo "      ✗ servisdə include istifadə olunur — select gözlənilirdi!"; exit 1; }
echo "      ✓ yalnız select işlədilir (include yox)"

echo ""
echo "  → 3) CANLI sübut: problem və həll yan-yana"
npx tsx skriptler/mapper_yoxla.ts
CIXIS=$?
[ "$CIXIS" -eq 0 ] || { echo "  ✗ mapper skripti uğursuz oldu"; exit 1; }

echo ""
echo "  → 4) Bazadaki real sütun tipləri"
psql "$DBURL" -At -c "
SELECT '      ' || column_name || ' → ' || data_type
  FROM information_schema.columns
 WHERE table_schema='kadrlar' AND table_name='emekdaslar'
   AND column_name IN ('id','maas','dogum_tarixi','yaradilma')
 ORDER BY ordinal_position;" 2>/dev/null

echo ""
echo "  ✓ IIA.2 KEÇDİ — BigInt/Decimal problemi həll olunub"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIA.3",
   "Servisin bütün CRUD əməliyyatları real bazada işləyir",
   """ADDIM 19-un nəticəsini yoxlayır. Servis HTTP-dən asılı olmadan,
   birbaşa çağırılır — 34 yoxlama. Test həm də təsdiqləyir ki, servis
   <strong>mövcud məlumata zərər vermir</strong> (əvvəl 14, sonra 14) və
   yumşaq silmə yolu həqiqətən işləyir.""",
   BAS + r'''
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
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIA.4",
   "Modul qoşulub, marşrutlar qeydiyyatdadır və GET işləyir",
   """ADDIM 20-nin nəticəsini yoxlayır. Test serveri qaldırır, logdan
   <strong>marşrut cədvəlini</strong> oxuyur və beş CRUD marşrutunun
   hamısının qeydiyyatdan keçdiyini təsdiqləyir. Sonra canlı cavabın
   <em>tip</em> yoxlamasını aparır: <code>id</code> mətn,
   <code>maas</code> mətn, tarixlər <code>YYYY-MM-DD</code>.""",
   BAS + SERVER + r'''
echo ""
echo "  → 1) Marşrut cədvəli (serverin öz logundan)"
grep 'Mapped {' "$LOQ" | sed 's/.*Mapped //' | sed 's/ route.*//' | sort -u | sed 's/^/      /'
XETA=0
for yol in "/api/v1/emekdaslar, GET" "/api/v1/emekdaslar/:id, GET" \
           "/api/v1/emekdaslar, POST" "/api/v1/emekdaslar/:id, PATCH" \
           "/api/v1/emekdaslar/:id, DELETE"; do
  grep -q "Mapped {$yol}" "$LOQ" || { echo "      ✗ marşrut yoxdur: $yol"; XETA=1; }
done
[ "$XETA" -eq 0 ] || { echo "  ✗ CRUD marşrutları tam deyil — app.module.ts-ə əlavə olunubmu?"; exit 1; }
echo "      ✓ beş CRUD marşrutu qeydiyyatdadır"

echo ""
echo "  → 2) GET /api/v1/emekdaslar?limit=2"
KOD=$(kod "$BAZ?limit=2")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$BAZ?limit=2" -o /tmp/iia4.json
python3 -c "
import json
d = json.load(open('/tmp/iia4.json'))
print('      cem=%s  sehife=%s/%s  gosterilen=%s' % (d['cem'], d['sehife'], d['sehife_sayi'], len(d['melumat'])))
for e in d['melumat']:
    print('        - id=%s  %s  |  %s' % (e['id'], e['tam_ad'], e['vezife']['ad']))
"

echo ""
echo "  → 3) GET /api/v1/emekdaslar/1 — tip yoxlaması"
govde "$BAZ/1" -o /tmp/iia4b.json
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iia4b.json'))
problem = []
if not isinstance(d.get('id'), str):
    problem.append("id mətn deyil: %r (BigInt JSON-a düşüb?)" % d.get('id'))
if not isinstance(d.get('maas'), str):
    problem.append("maas mətn deyil: %r" % d.get('maas'))
for a in ('dogum_tarixi', 'ise_baslama'):
    v = d.get(a)
    if v is not None and (not isinstance(v, str) or len(v) != 10):
        problem.append("%s YYYY-MM-DD deyil: %r" % (a, v))
if not isinstance(d.get('yas'), int):
    problem.append("yas tam ədəd deyil: %r" % d.get('yas'))
if not isinstance(d.get('mezuniyyetler', None), type(None)) and 'mezuniyyetler' in d:
    problem.append("xam əlaqə adı sızıb: mezuniyyetler")
for a in ('cinsiyyet', 'vezife', 'merkez'):
    if not isinstance(d.get(a), (dict, type(None))):
        problem.append("%s obyekt deyil: %r" % (a, d.get(a)))
print('      id     →', repr(d['id']), type(d['id']).__name__)
print('      maas   →', repr(d['maas']), type(d['maas']).__name__)
print('      tarix  →', repr(d['dogum_tarixi']))
print('      yas    →', d['yas'])
print('      vezife →', d['vezife'])
for p in problem:
    print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ tip yoxlaması uğursuz"; exit 1; }
echo "      ✓ bütün tiplər düzgündür (BigInt və Decimal sızmır)"

echo ""
echo "  → 4) Prefiks yoxlaması"
printf '      /api/v1/emekdaslar  → %s\n' "$(kod "http://localhost:$PORT/api/v1/emekdaslar")"
printf '      /emekdaslar         → %s\n' "$(kod "http://localhost:$PORT/emekdaslar")"
[ "$(kod "http://localhost:$PORT/emekdaslar")" = "404" ] \
  || { echo "  ✗ prefikssiz yol 404 qaytarmadı"; exit 1; }
echo "      ✓ prefiks işləyir"

echo ""
echo "  → 5) Swagger-də endpoint-lər"
govde "http://localhost:$PORT/docs-json" -o /tmp/iia4c.json
python3 -c "
import json
d = json.load(open('/tmp/iia4c.json'))
yollar = [y for y in d.get('paths', {}) if 'emekdaslar' in y]
print('      OpenAPI-də emekdaslar yolları:', len(yollar))
for y in sorted(yollar):
    print('        %-30s %s' % (y, ', '.join(sorted(m.upper() for m in d['paths'][y]))))
"
N=$(python3 -c "
import json
d=json.load(open('/tmp/iia4c.json'))
print(len([y for y in d['paths'] if 'emekdaslar' in y]))
")
[ "$N" -eq 2 ] || { echo "  ✗ OpenAPI-də 2 yol gözlənilirdi, tapıldı: $N"; exit 1; }
echo "      ✓ Swagger avtomatik yenilənib"

echo ""
echo "  ✓ IIA.4 KEÇDİ — modul qoşulub və API canlı işləyir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIA.5",
   "GET siyahı: səhifələmə, sıralama, filtr və axtarış",
   """ADDIM 19-daki <code>hamisi()</code> metodunun bütün imkanlarını
   HTTP səviyyəsində yoxlayır. Xüsusilə <strong>səhifələmə
   riyaziyyatını</strong>: <code>skip = (sehife-1) × limit</code> səhvi
   ən çox rast gəlinən səhvdir və bu test onu tutur.""",
   BAS + SERVER + r'''
echo ""
echo "  → 1) Səhifələmə"
govde "$BAZ?limit=3&seife=1&siralama=soyad&tertib=asc" -o /tmp/a.json
govde "$BAZ?limit=3&seife=2&siralama=soyad&tertib=asc" -o /tmp/b.json
python3 - <<'PSON'
import json
a = json.load(open('/tmp/a.json'))
b = json.load(open('/tmp/b.json'))
problem = []
print('      1-ci səhifə: cem=%s sehife_sayi=%s gosterilen=%s' % (a['cem'], a['sehife_sayi'], len(a['melumat'])))
print('      2-ci səhifə: cem=%s sehife_sayi=%s gosterilen=%s' % (b['cem'], b['sehife_sayi'], len(b['melumat'])))
for e in a['melumat']:
    print('        - ' + e['tam_ad'])
if a['cem'] != 14:
    problem.append("cem 14 deyil: %r" % a['cem'])
if a['sehife_sayi'] != 5:
    problem.append("sehife_sayi 5 deyil (14/3 → 5): %r" % a['sehife_sayi'])
if len(a['melumat']) != 3 or len(b['melumat']) != 3:
    problem.append("hər səhifədə 3 sətir olmalıdır")
if a['melumat'][0]['id'] == b['melumat'][0]['id']:
    problem.append("1-ci və 2-ci səhifə EYNİ sətirlə başlayır — skip səhvdir!")
soyadlar = [e['soyad'] for e in a['melumat']]
if soyadlar != sorted(soyadlar):
    problem.append("sıralama düzgün deyil: %r" % soyadlar)
for p in problem:
    print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ səhifələmə yoxlaması uğursuz"; exit 1; }
echo "      ✓ skip = (sehife-1) × limit düzgün işləyir"

echo ""
echo "  → 2) Sıralama istiqaməti"
govde "$BAZ?limit=3&siralama=maas&tertib=desc" -o /tmp/c.json
govde "$BAZ?limit=3&siralama=maas&tertib=asc" -o /tmp/d.json
python3 -c "
import json
c = json.load(open('/tmp/c.json')); d = json.load(open('/tmp/d.json'))
print('      maas desc:', [e['maas'] for e in c['melumat']])
print('      maas asc :', [e['maas'] for e in d['melumat']])
assert float(c['melumat'][0]['maas']) > float(c['melumat'][-1]['maas']), 'desc sıralama səhvdir'
assert float(d['melumat'][0]['maas']) < float(d['melumat'][-1]['maas']), 'asc sıralama səhvdir'
print('      ✓ hər iki istiqamət düzgündür')
" || { echo "  ✗ sıralama yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 3) Axtarış (hərf böyüklüyündən asılı olmayan)"
A1=$(python3 -c "import urllib.parse; print(urllib.parse.quote('Əliyev'))")
A2=$(python3 -c "import urllib.parse; print(urllib.parse.quote('ƏLİYEV'))")
KICIK=$(govde "$BAZ?axtar=$A1" | python3 -c "import json,sys;print(json.load(sys.stdin)['cem'])")
BOYUK=$(govde "$BAZ?axtar=$A2" | python3 -c "import json,sys;print(json.load(sys.stdin)['cem'])")
printf '      "Əliyev"  → %s nəticə\n' "$KICIK"
printf '      "ƏLİYEV"  → %s nəticə\n' "$BOYUK"
[ "$KICIK" = "2" ] || { echo "  ✗ kiçik hərflə 2 nəticə gözlənilirdi: $KICIK"; exit 1; }
[ "$BOYUK" = "2" ] || { echo "  ✗ böyük hərflə 2 nəticə gözlənilirdi: $BOYUK"; exit 1; }
echo "      ✓ hərf böyüklüyü nəzərə alınmır"

echo ""
echo "  → 4) Axtarış — ata adı və e-poçt üzrə"
AXTAR=$(python3 -c "import urllib.parse; print(urllib.parse.quote('Qəzənfər'))")
govde "$BAZ?axtar=$AXTAR" -o /tmp/e.json
python3 -c "
import json
d = json.load(open('/tmp/e.json'))
print('      ata adı «Qəzənfər» →', d['cem'], 'nəticə')
assert d['cem'] >= 1, 'ata adı üzrə axtarış işləmir'
print('      ✓ ata adı üzrə tapıldı:', d['melumat'][0]['tam_ad'])
" || { echo "  ✗ ata adı axtarışı uğursuz"; exit 1; }

echo ""
echo "  → 5) Filtr — merkez və aktivlik"
for q in "merkez_id=1" "merkez_id=2" "shobe_id=1"; do
  N=$(govde "$BAZ?$q" | python3 -c "import json,sys;print(json.load(sys.stdin)['cem'])")
  printf '      %-14s → %s əməkdaş\n' "$q" "$N"
done
N1=$(govde "$BAZ?aktiv=aktiv" | python3 -c "import json,sys;print(json.load(sys.stdin)['cem'])")
N2=$(govde "$BAZ?aktiv=passiv" | python3 -c "import json,sys;print(json.load(sys.stdin)['cem'])")
N3=$(govde "$BAZ?aktiv=hamisi" | python3 -c "import json,sys;print(json.load(sys.stdin)['cem'])")
printf '      aktiv=aktiv    → %s\n' "$N1"
printf '      aktiv=passiv   → %s\n' "$N2"
printf '      aktiv=hamisi   → %s\n' "$N3"
[ "$N3" = "14" ] || { echo "  ✗ hamisi 14 olmalıdır: $N3"; exit 1; }
[ "$((N1 + N2))" -eq "$N3" ] || { echo "  ✗ aktiv + passiv = hamisi olmalıdır"; exit 1; }
echo "      ✓ filtr düzgün işləyir"

echo ""
echo "  → 6) Boş nəticə"
N=$(govde "$BAZ?axtar=ZZZQQQxxx" | python3 -c "import json,sys;print(json.load(sys.stdin)['cem'])")
printf '      mövcud olmayan ad → %s nəticə (200 qaytarır, xəta yox)\n' "$N"
[ "$N" = "0" ] || { echo "  ✗ 0 gözlənilirdi"; exit 1; }
echo "      ✓ boş nəticə xəta deyil"

echo ""
echo "  ✓ IIA.5 KEÇDİ — səhifələmə, sıralama, filtr və axtarış işləyir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIA.6",
   "POST yaradır: 201, düzgün cavab və xəta halları",
   """Yaratma əməliyyatını yoxlayır: status <code>201</code>, cavabda
   yaradılmış obyekt, standart dəyərlərin tətbiqi. Sonra dörd xəta
   halını: validasiya (<code>400</code>), yox olan xarici açar
   (<code>400</code>), təkrar e-poçt (<code>409</code>) və gövdədə yad
   sahə (<code>400</code>). Testin yaratdığı sətir sonda silinir.""",
   BAS + SERVER + r'''
EPOX=$(date +%s)
EPOST="iia6.${EPOX}@arti.edu.az"
YENI=""

temizle2() {
  if [ -n "$YENI" ]; then
    printf '  → təmizlik: ID %s silinir\n' "$YENI"
    curl -s -o /dev/null -X DELETE "$BAZ/$YENI"
  fi
  say "DELETE FROM struktur.elmi_shura_uzvleri WHERE emekdas_id IN (SELECT id FROM kadrlar.emekdaslar WHERE email LIKE 'iia6.%@arti.edu.az');" >/dev/null
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iia6.%@arti.edu.az';" >/dev/null
  temizle
}
trap temizle2 EXIT INT TERM

DUZGUN="{\"ad\":\"Test\",\"soyad\":\"IIA6\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"merkez_id\":1,\"email\":\"$EPOST\",\"ise_baslama\":\"2026-03-01\",\"maas\":1234.56}"

echo ""
echo "  → 1) Düzgün POST"
KOD=$(curl -s -o /tmp/iia6a.json -w '%{http_code}' \
      -X POST "$BAZ" -H 'Content-Type: application/json' -d "$DUZGUN")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "201" ] || { echo "  ✗ 201 Created gözlənilirdi"; head -c 300 /tmp/iia6a.json; exit 1; }
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iia6a.json'))
print('      id     :', d['id'], type(d['id']).__name__)
print('      tam_ad :', d['tam_ad'])
print('      vezife :', d['vezife']['ad'])
print('      status :', d['is_statusu']['ad'])
print('      maas   :', d['maas'])
print('      tarix  :', d['ise_baslama'])
assert d['ad'] == 'Test' and d['soyad'] == 'IIA6'
assert d['maas'] == '1234.56', 'maas formatı səhvdir: %r' % d['maas']
assert d['ise_baslama'] == '2026-03-01', 'tarix səhvdir: %r' % d['ise_baslama']
assert d['is_statusu']['id'] == 1, 'standart status tətbiq olunmadı'
assert d['aktiv'] is True
print('      ✓ bütün sahələr düzgündür')
PSON
[ $? -eq 0 ] || { echo "  ✗ cavab yoxlaması uğursuz"; exit 1; }

YENI=$(python3 -c "import json;print(json.load(open('/tmp/iia6a.json'))['id'])" 2>/dev/null)

echo ""
echo "  → 2) Yaradılan sətir bazadadır"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email='$EPOST';")
printf '      e-poçt üzrə tapıldı: %s\n' "$N"
[ "$N" = "1" ] || { echo "  ✗ sətir bazada tapılmadı"; exit 1; }

echo ""
echo "  → 3) TƏKRAR e-poçt → 409"
KOD=$(curl -s -o /tmp/iia6b.json -w '%{http_code}' \
      -X POST "$BAZ" -H 'Content-Type: application/json' -d "$DUZGUN")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "409" ] || { echo "  ✗ 409 Conflict gözlənilirdi (P2002 çevrilməsi)"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iia6b.json'))
print('      kod  :', d['xeta']['kod'])
print('      mesaj:', d['xeta']['mesaj'])
assert d['xeta']['kod'] == 'TOQQUSMA', d['xeta']['kod']
"
echo "      ✓ P2002 → 409 TOQQUSMA"

echo ""
echo "  → 4) Natamam gövdə → 400"
KOD=$(curl -s -o /tmp/iia6c.json -w '%{http_code}' \
      -X POST "$BAZ" -H 'Content-Type: application/json' -d '{"ad":"A"}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iia6c.json'))
print('      kod     :', d['xeta']['kod'])
print('      mesaj   :', d['xeta']['mesaj'])
for x in d['xeta'].get('detallar', [])[:4]:
    print('        ·', x)
assert d['xeta']['kod'] == 'YANLIS_SORGU'
assert len(d['xeta'].get('detallar', [])) >= 3, 'validasiya detalları gəlmədi'
"
echo "      ✓ validasiya xətaları siyahı kimi gəlir"

echo ""
echo "  → 5) Yox olan vəzifə (xarici açar) → 400"
KOD=$(kod -X POST "$BAZ" -H 'Content-Type: application/json' \
      -d '{"ad":"Test","soyad":"FK","ata_adi":"Sistem","cinsiyyet_id":1,"vezife_id":99}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi (P2003 çevrilməsi)"; exit 1; }
echo "      ✓ P2003 → 400 YANLIS_SORGU"

echo ""
echo "  → 6) Gövdədə YAD sahə → 400"
KOD=$(kod -X POST "$BAZ" -H 'Content-Type: application/json' \
      -d '{"ad":"Test","soyad":"Yad","ata_adi":"Sistem","cinsiyyet_id":1,"vezife_id":6,"yoluxucu":true}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
echo "      ✓ forbidNonWhitelisted işləyir"

echo ""
echo "  → 7) Cinsiyyet ID həddən kənar → 400"
KOD=$(kod -X POST "$BAZ" -H 'Content-Type: application/json' \
      -d '{"ad":"Test","soyad":"Hedd","ata_adi":"Sistem","cinsiyyet_id":99,"vezife_id":6}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
echo "      ✓ DTO həddi işləyir"

echo ""
echo "  → 8) Bazada YALNIZ bizim sətir var"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'iia6.%@arti.edu.az';")
printf '      iia6.* e-poçtlu sətir: %s (1 olmalıdır — təkrar 409 aldı)\n' "$N"
[ "$N" = "1" ] || { echo "  ✗ gözlənilməz sətir sayı: $N"; exit 1; }
echo "      ✓ təkrar cəhd bazaya heç nə yazmadı"

echo ""
echo "  → 9) Təmizlik"
curl -s -o /dev/null -X DELETE "$BAZ/$YENI"
YENI=""
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'iia6.%@arti.edu.az';")
printf '      qalan sətir: %s\n' "$N"
[ "$N" = "0" ] || { echo "  ✗ təmizlik alınmadı"; exit 1; }
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      ümumi əməkdaş: %s\n' "$TOTAL"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }

echo ""
echo "  ✓ IIA.6 KEÇDİ — yaratma və dörd xəta halı düzgün işləyir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIA.7",
   "PATCH qismən dəyişir və səhv halları tutur",
   """ADDIM 19-daki <code>yenile()</code> metodunu yoxlayır. Ən vacib
   yoxlama: <strong>göndərilməyən sahələr toxunulmaz qalmalıdır</strong>.
   Əgər kod <code>data = { ...dto }</code> kimi yazılsaydı, çatışmayan
   sahələr <code>undefined</code> olub bazada silinərdi — bu, sükutlu
   məlumat itkisidir və test məhz onu tutur.""",
   BAS + SERVER + r'''
EPOX=$(date +%s)
EPOST="iia7.${EPOX}@arti.edu.az"
YENI=""

temizle2() {
  say "DELETE FROM struktur.elmi_shura_uzvleri WHERE emekdas_id IN (SELECT id FROM kadrlar.emekdaslar WHERE email LIKE 'iia7.%@arti.edu.az');" >/dev/null
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iia7.%@arti.edu.az';" >/dev/null
  temizle
}
trap temizle2 EXIT INT TERM

echo ""
echo "  → 1) Test əməkdaşı yaradılır"
govde -X POST "$BAZ" -H 'Content-Type: application/json' \
  -d "{\"ad\":\"Kohnə\",\"soyad\":\"Ad\",\"ata_adi\":\"AtaAdi\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"merkez_id\":1,\"email\":\"$EPOST\",\"telefon\":\"+994 50 000 00 00\",\"maas\":1000}" \
  -o /tmp/iia7a.json
YENI=$(python3 -c "import json;print(json.load(open('/tmp/iia7a.json')).get('id',''))" 2>/dev/null)
[ -n "$YENI" ] || { echo "  ✗ əməkdaş yaradıla bilmədi"; head -c 300 /tmp/iia7a.json; exit 1; }
printf '      ID %s yaradıldı\n' "$YENI"

echo ""
echo "  → 2) PATCH — yalnız iki sahə"
KOD=$(curl -s -o /tmp/iia7b.json -w '%{http_code}' \
      -X PATCH "$BAZ/$YENI" -H 'Content-Type: application/json' \
      -d '{"vezife_id":4,"maas":2500.75}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iia7b.json'))
problem = []
print('      ad      :', d['ad'], '(dəyişməməlidir)')
print('      soyad   :', d['soyad'], '(dəyişməməlidir)')
print('      ata_adi :', d['ata_adi'], '(dəyişməməlidir)')
print('      telefon :', d['telefon'], '(dəyişməməlidir)')
print('      vezife  :', d['vezife']['ad'], '(dəyişməlidir)')
print('      maas    :', d['maas'], '(dəyişməlidir)')
if d['ad'] != 'Kohnə':
    problem.append("ad dəyişdi: %r" % d['ad'])
if d['soyad'] != 'Ad':
    problem.append("soyad dəyişdi: %r" % d['soyad'])
if d['ata_adi'] != 'AtaAdi':
    problem.append("ata_adi dəyişdi: %r" % d['ata_adi'])
if d['telefon'] != '+994 50 000 00 00':
    problem.append("telefon dəyişdi: %r" % d['telefon'])
if d['vezife']['id'] != 4:
    problem.append("vezife dəyişmədi: %r" % d['vezife'])
if d['maas'] != '2500.75':
    problem.append("maas dəyişmədi: %r" % d['maas'])
for p in problem:
    print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ qismən yeniləmə yoxlaması uğursuz"; exit 1; }
echo "      ✓ yalnız göndərilən sahələr dəyişdi"

echo ""
echo "  → 3) Boş gövdə → 400"
KOD=$(kod -X PATCH "$BAZ/$YENI" -H 'Content-Type: application/json' -d '{}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
govde -X PATCH "$BAZ/$YENI" -H 'Content-Type: application/json' -d '{}' -o /tmp/iia7c.json
python3 -c "
import json
d = json.load(open('/tmp/iia7c.json'))
print('      mesaj:', d['xeta']['mesaj'])
assert 'ən azı bir sahə' in d['xeta']['mesaj'], d['xeta']['mesaj']
"
echo "      ✓ boş PATCH rədd edilir"

echo ""
echo "  → 4) Səhv tip → 400"
KOD=$(kod -X PATCH "$BAZ/$YENI" -H 'Content-Type: application/json' -d '{"maas":"cox"}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
echo "      ✓ tip yoxlaması işləyir"

echo ""
echo "  → 5) Mənfi maaş → 400"
KOD=$(kod -X PATCH "$BAZ/$YENI" -H 'Content-Type: application/json' -d '{"maas":-10}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
echo "      ✓ @Min(0) işləyir"

echo ""
echo "  → 6) Səhv formatlı e-poçt → 400"
KOD=$(kod -X PATCH "$BAZ/$YENI" -H 'Content-Type: application/json' -d '{"email":"cox@"}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
echo "      ✓ @IsEmail işləyir"

echo ""
echo "  → 7) Yox olan ID → 404"
KOD=$(kod -X PATCH "$BAZ/999999" -H 'Content-Type: application/json' -d '{"maas":100}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "404" ] || { echo "  ✗ 404 gözlənilirdi (P2025 çevrilməsi)"; exit 1; }
govde -X PATCH "$BAZ/999999" -H 'Content-Type: application/json' -d '{"maas":100}' -o /tmp/iia7d.json
python3 -c "
import json
d = json.load(open('/tmp/iia7d.json'))
print('      kod:', d['xeta']['kod'])
assert d['xeta']['kod'] == 'TAPILMADI', d['xeta']['kod']
"
echo "      ✓ P2025 → 404 TAPILMADI"

echo ""
echo "  → 8) Uğursuz cəhdlər heç nəyi dəyişmədi"
govde "$BAZ/$YENI" -o /tmp/iia7e.json
python3 -c "
import json
d = json.load(open('/tmp/iia7e.json'))
print('      vezife:', d['vezife']['ad'])
print('      maas  :', d['maas'])
assert d['maas'] == '2500.75', 'uğursuz PATCH məlumatı dəyişdi!'
assert d['vezife']['id'] == 4
print('      ✓ bütün uğursuz cəhdlər təsirsiz qaldı')
" || { echo "  ✗ uğursuz cəhdlər məlumatı dəyişdi"; exit 1; }

echo ""
echo "  → 9) Təmizlik"
curl -s -o /dev/null -X DELETE "$BAZ/$YENI"
YENI=""
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      ümumi əməkdaş: %s\n' "$TOTAL"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }

echo ""
echo "  ✓ IIA.7 KEÇDİ — qismən yeniləmə və altı xəta halı düzgündür"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIA.8",
   "DELETE: asılısız sətri silir, asılısı olanı passiv edir",
   """Dərsin ən vacib arxitektura qərarını yoxlayır: <strong>iki
   strategiyalı silmə</strong>. Test müvəqqəti əməkdaş yaradır, ona
   <code>elmi_shura_uzvleri</code> sətri bağlayır və <code>DELETE</code>
   edir — gözlənilən nəticə <code>nov: "soft"</code>. Sonra asılısız
   sətirdə <code>nov: "hard"</code> yoxlanılır. <strong>Mövcud 14
   əməkdaşa toxunulmur.</strong>""",
   BAS + SERVER + r'''
EPOX=$(date +%s)
E1="iia8a.${EPOX}@arti.edu.az"
E2="iia8b.${EPOX}@arti.edu.az"
ID1=""
ID2=""

temizle2() {
  say "DELETE FROM struktur.elmi_shura_uzvleri WHERE emekdas_id IN (SELECT id FROM kadrlar.emekdaslar WHERE email LIKE 'iia8%.%@arti.edu.az');" >/dev/null
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iia8%.%@arti.edu.az';" >/dev/null
  temizle
}
trap temizle2 EXIT INT TERM

echo ""
echo "  → 1) İki müvəqqəti əməkdaş yaradılır"
govde -X POST "$BAZ" -H 'Content-Type: application/json' \
  -d "{\"ad\":\"Asili\",\"soyad\":\"Var\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$E1\"}" \
  -o /tmp/iia8a.json
ID1=$(python3 -c "import json;print(json.load(open('/tmp/iia8a.json')).get('id',''))" 2>/dev/null)
govde -X POST "$BAZ" -H 'Content-Type: application/json' \
  -d "{\"ad\":\"Asili\",\"soyad\":\"Yox\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$E2\"}" \
  -o /tmp/iia8b.json
ID2=$(python3 -c "import json;print(json.load(open('/tmp/iia8b.json')).get('id',''))" 2>/dev/null)
[ -n "$ID1" ] && [ -n "$ID2" ] || { echo "  ✗ əməkdaşlar yaradıla bilmədi"; exit 1; }
printf '      asılısı OLACAQ : ID %s\n' "$ID1"
printf '      asılısı OLMAYAN: ID %s\n' "$ID2"

echo ""
printf '  → 2) ID %s üçün şura üzvü sətri əlavə edilir (psql ilə)\n' "$ID1"
say "INSERT INTO struktur.elmi_shura_uzvleri (emekdas_id, ad_soyad) VALUES ($ID1, 'IIA8 Test Uzv');" >/dev/null
N=$(say "SELECT count(*) FROM struktur.elmi_shura_uzvleri WHERE emekdas_id=$ID1;")
printf '      asılı qeyd sayı: %s\n' "$N"
[ "$N" = "1" ] || { echo "  ✗ asılı qeyd yaradıla bilmədi"; exit 1; }

echo ""
echo "  → 3) Adi SQL ilə silmək MÜMKÜN DEYİL (sübut)"
psql "$DBURL" -c "DELETE FROM kadrlar.emekdaslar WHERE id=$ID1;" 2>&1 | head -2 | sed 's/^/      /'
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE id=$ID1;")
printf '      amma sətir hələ də yerindədir: %s\n' "$N"
[ "$N" = "1" ] || { echo "  ✗ sətir gözlənilmədən silindi!"; exit 1; }
echo "      ✓ PostgreSQL xarici açarı qoruyur"

echo ""
echo "  → 4) API ilə DELETE → YUMŞAQ silmə"
KOD=$(curl -s -o /tmp/iia8c.json -w '%{http_code}' -X DELETE "$BAZ/$ID1")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; head -c 300 /tmp/iia8c.json; exit 1; }
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iia8c.json'))
print('      nov          :', d['nov'])
print('      mesaj        :', d['mesaj'])
print('      asılı qeydlər:', json.dumps(d['asili_qeydler'], ensure_ascii=False))
assert d['nov'] == 'soft', "soft gözlənilirdi, alındı: %r" % d['nov']
assert d['asili_qeydler'].get('elmi_shura_uzvleri') == 1, d['asili_qeydler']
print('      ✓ nov = soft, asılı qeyd sayıldı')
PSON
[ $? -eq 0 ] || { echo "  ✗ yumşaq silmə yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 5) Sətir bazada QALIR, amma aktiv=false"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE id=$ID1;")
A=$(say "SELECT aktiv FROM kadrlar.emekdaslar WHERE id=$ID1;")
printf '      bazada: %s   aktiv: %s\n' "$N" "$A"
[ "$N" = "1" ] || { echo "  ✗ sətir bazadan silindi — yumşaq silmə işləmədi"; exit 1; }
[ "$A" = "f" ] || { echo "  ✗ aktiv=false deyil: $A"; exit 1; }
echo "      ✓ sətir qorundu, sadəcə passiv edildi"

echo ""
echo "  → 6) Siyahıda passiv görünür, aktiv siyahıda yox"
N1=$(govde "$BAZ?aktiv=passiv" | python3 -c "import json,sys;print(json.load(sys.stdin)['cem'])")
N2=$(govde "$BAZ?aktiv=aktiv" | python3 -c "import json,sys;print(json.load(sys.stdin)['cem'])")
printf '      aktiv=passiv → %s   aktiv=aktiv → %s\n' "$N1" "$N2"
[ "$N1" -ge 1 ] || { echo "  ✗ passiv siyahıda görünmür"; exit 1; }
echo "      ✓ filtr passiv sətri göstərir"

echo ""
echo "  → 7) Asılısız sətir → ADİ silmə"
KOD=$(curl -s -o /tmp/iia8d.json -w '%{http_code}' -X DELETE "$BAZ/$ID2")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; head -c 300 /tmp/iia8d.json; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iia8d.json'))
print('      nov  :', d['nov'])
print('      mesaj:', d['mesaj'])
assert d['nov'] == 'hard', 'hard gözlənilirdi: %r' % d['nov']
" || { echo "  ✗ adi silmə yoxlaması uğursuz"; exit 1; }
echo "      ✓ nov = hard"

echo ""
echo "  → 8) Silinən sətir həqiqətən getdi (mənfi təsdiq)"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE id=$ID2;")
KOD=$(kod "$BAZ/$ID2")
printf '      bazada: %s   GET /%s → %s\n' "$N" "$ID2" "$KOD"
[ "$N" = "0" ] || { echo "  ✗ sətir bazada qaldı"; exit 1; }
[ "$KOD" = "404" ] || { echo "  ✗ 404 gözlənilirdi"; exit 1; }
echo "      ✓ həm bazadan, həm API-dən getdi"

echo ""
echo "  → 9) İdempotentlik — təkrar DELETE"
KOD=$(kod -X DELETE "$BAZ/$ID2")
printf '      ikinci DELETE → %s\n' "$KOD"
[ "$KOD" = "404" ] || { echo "  ✗ 404 gözlənilirdi"; exit 1; }
echo "      ✓ təkrar silmə xəta vermir, sadəcə 404 qaytarır"

echo ""
echo "  → 10) Yox olan ID → 404"
KOD=$(kod -X DELETE "$BAZ/999999")
printf '      DELETE /999999 → %s\n' "$KOD"
[ "$KOD" = "404" ] || { echo "  ✗ 404 gözlənilirdi"; exit 1; }
echo "      ✓ mövcud olmayan ID 404 qaytarır"

echo ""
echo "  → 11) Təmizlik"
say "DELETE FROM struktur.elmi_shura_uzvleri WHERE emekdas_id=$ID1;" >/dev/null
say "DELETE FROM kadrlar.emekdaslar WHERE id=$ID1;" >/dev/null
ID1=""
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
ZIBIL=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'iia8%.%@arti.edu.az';")
printf '      ümumi əməkdaş: %s   test zibili: %s\n' "$TOTAL" "$ZIBIL"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }
[ "$ZIBIL" = "0" ] || { echo "  ✗ test zibili qaldı: $ZIBIL"; exit 1; }
echo "      ✓ baza tam təmizdir"

echo ""
echo "  ✓ IIA.8 KEÇDİ — iki strategiyalı silmə düzgün işləyir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIA.9",
   "Xəta kodları və vahid format — DTO-dan Prisma-ya qədər",
   """Bütün xəta mənbələrinin <strong>eyni</strong> JSON formatında
   qaytardığını və düzgün status kodunu verdiyini yoxlayır: DTO
   validasiyası, <code>ParseIntPipe</code>, servisin
   <code>NotFoundException</code>-ı, Prisma <code>P2002</code> və
   <code>P2003</code>. Həm də təsdiqləyir ki, Prisma-nın xam xəta mətni
   <em>heç vaxt</em> istifadəçiyə çatmır.""",
   BAS + SERVER + r'''
EPOX=$(date +%s)
EPOST="iia9.${EPOX}@arti.edu.az"

temizle2() {
  say "DELETE FROM struktur.elmi_shura_uzvleri WHERE emekdas_id IN (SELECT id FROM kadrlar.emekdaslar WHERE email LIKE 'iia9.%@arti.edu.az');" >/dev/null
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iia9.%@arti.edu.az';" >/dev/null
  temizle
}
trap temizle2 EXIT INT TERM

govde -X POST "$BAZ" -H 'Content-Type: application/json' \
  -d "{\"ad\":\"Test\",\"soyad\":\"IIA9\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$EPOST\"}" \
  -o /tmp/iia9a.json

echo ""
echo "  → Xəta hallarının yoxlanması"
echo "  ┌────────────────────────────────────┬────────┬──────────────┐"
printf '  │ %-34s │ %-6s │ %-12s │\n' "SORĞU" "STATUS" "XƏTA KODU"
echo "  ├────────────────────────────────────┼────────┼──────────────┤"

XETA=0
yoxla() {
  local ad="$1"; shift
  local gozle="$1"; shift
  local gozle_kod="$1"; shift
  local kod; kod=$(kod "$@")
  local f=/tmp/iia9c.json
  curl -s -o "$f" "$@" >/dev/null 2>&1
  local xk; xk=$(python3 -c "
import json
try:
    d = json.load(open('$f'))
    print(d.get('xeta', {}).get('kod', '—'))
except Exception:
    print('PARSE-XƏTA')
" 2>/dev/null)
  if [ "$kod" = "$gozle" ] && [ "$xk" = "$gozle_kod" ]; then
    printf '  │ %-34s │ %-6s │ %-12s │\n' "$ad" "$kod" "$xk"
  else
    printf '  │ %-34s │ %-6s │ %-12s │  ✗ gözlənilirdi %s / %s\n' "$ad" "$kod" "$xk" "$gozle" "$gozle_kod"
    XETA=1
  fi
}
yoxla "POST natamam gövdə" 400 YANLIS_SORGU \
  -X POST "$BAZ" -H 'Content-Type: application/json' -d '{"ad":"X"}'
yoxla "POST yox olan vezife_id" 400 YANLIS_SORGU \
  -X POST "$BAZ" -H 'Content-Type: application/json' \
  -d '{"ad":"Test","soyad":"FK","ata_adi":"Sistem","cinsiyyet_id":1,"vezife_id":99}'
yoxla "POST təkrar e-poçt" 409 TOQQUSMA \
  -X POST "$BAZ" -H 'Content-Type: application/json' \
  -d "{\"ad\":\"Test\",\"soyad\":\"IIA9\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$EPOST\"}"
yoxla "GET /abc (mətn ID)" 400 YANLIS_SORGU "$BAZ/abc"
yoxla "GET ?limit=500" 400 YANLIS_SORGU "$BAZ?limit=500"
yoxla "GET ?yad=1" 400 YANLIS_SORGU "$BAZ?yad=1"
yoxla "GET /999999" 404 TAPILMADI "$BAZ/999999"
yoxla "PATCH /999999" 404 TAPILMADI -X PATCH "$BAZ/999999" \
  -H 'Content-Type: application/json' -d '{"maas":100}'
yoxla "DELETE /999999" 404 TAPILMADI -X DELETE "$BAZ/999999"
yoxla "GET /api/v1/yoxdur" 404 TAPILMADI "http://localhost:$PORT/api/v1/yoxdur"
echo "  └────────────────────────────────────┴────────┴──────────────┘"
[ "$XETA" -eq 0 ] || { echo "  ✗ bəzi xəta halları gözlənilən deyil"; exit 1; }

echo ""
echo "  → Formatın vahidliyi (10 xətanın hamısı eyni açarlarla)"
python3 - <<'PSON'
import json, urllib.request, urllib.error

BAZ = "http://localhost:4000/api/v1/emekdaslar"
hallar = [
    ("POST", BAZ + "?x=1", {"ad": "X"}),
    ("GET", BAZ + "/abc", None),
    ("GET", BAZ + "/999999", None),
    ("GET", "http://localhost:4000/api/v1/yoxdur", None),
]
GEREKLI = {"ugur", "xeta", "yol", "vaxt"}
problem = []
aciqlar = set()

for metod, yol, govde in hallar:
    data = json.dumps(govde).encode() if govde else None
    req = urllib.request.Request(yol, data=data, method=metod,
                                 headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
        problem.append("%s %s — xəta gözlənilirdi" % (metod, yol))
        continue
    except urllib.error.HTTPError as e:
        d = json.loads(e.read().decode())

    if set(d.keys()) != GEREKLI:
        problem.append("%s %s: açarlar %s" % (metod, yol, sorted(d.keys())))
    aciqlar.add(tuple(sorted(d.keys())))
    if d.get("ugur") is not False:
        problem.append("%s %s: ugur false deyil" % (metod, yol))
    x = d.get("xeta") or {}
    for a in ("statusCode", "message", "error"):
        if a in d:
            problem.append("%s %s: Nest standart formatı ('%s')" % (metod, yol, a))
    if not isinstance(x.get("kod"), str) or not x.get("kod"):
        problem.append("%s %s: xeta.kod yoxdur" % (metod, yol))
    if not isinstance(x.get("mesaj"), (str, list)):
        problem.append("%s %s: xeta.mesaj yoxdur" % (metod, yol))
    print("      %-6s %-42s → %s" % (metod, yol.replace("http://localhost:4000", ""), x.get("kod")))

if len(aciqlar) != 1:
    problem.append("formatlar fərqlidir: %s" % aciqlar)
for p in problem:
    print("      ✗ " + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ format vahidliyi pozulub"; exit 1; }
echo "      ✓ bütün xətalar EYNİ formatdadır: ugur / xeta / yol / vaxt"

echo ""
echo "  → Prisma xam xətası heç vaxt sızmır"
govde -X POST "$BAZ" -H 'Content-Type: application/json' \
  -d "{\"ad\":\"Test\",\"soyad\":\"IIA9\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$EPOST\"}" \
  -o /tmp/iia9d.json
python3 - <<'PSON'
import json
m = open('/tmp/iia9d.json', encoding='utf-8').read()
d = json.loads(m)
problem = []
for q in ("PrismaClient", "invocation", "Unique constraint failed", "P2002", "prisma.emekdaslar"):
    if q in m:
        problem.append("xam Prisma mətni sızıb: %r" % q)
print('      mesaj:', d['xeta']['mesaj'])
print('      kod  :', d['xeta']['kod'])
for p in problem:
    print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ xam Prisma xətası istifadəçiyə çatır"; exit 1; }
echo "      ✓ istifadəçi yalnız Azərbaycanca mesaj görür"

echo ""
echo "  → Təmizlik"
say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iia9.%@arti.edu.az';" >/dev/null
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      ümumi əməkdaş: %s\n' "$TOTAL"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }

echo ""
echo "  ✓ IIA.9 KEÇDİ — bütün xəta yolları vahid formatdadır"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIA.10",
   "Bütöv CRUD skripti keçir və baza toxunulmaz qalır",
   """ADDIM 21-də yazdığımız <code>skriptler/crud_yoxla.sh</code> faylını
   işlədir — istifadəçinin <em>özünün</em> işlədəcəyi əmrlə. Test həm də
   skriptin <strong>simmetriya prinsipini</strong> ayrıca yoxlayır:
   sətir sayı əvvəl və sonra eyni olmalıdır. Ən sonda bütün dəst
   — <code>tsc</code>, vahid və servis yoxlamaları — bir yerdə işlədilir.""",
   BAS + r'''
[ -f skriptler/crud_yoxla.sh ] \
  || { echo "  ✗ skriptler/crud_yoxla.sh yoxdur — ADDIM 21-i işlədin"; exit 1; }

echo ""
echo "  → 1) Skriptin sintaksisi"
bash -n skriptler/crud_yoxla.sh || { echo "  ✗ bash sintaksisi səhvdir"; exit 1; }
printf '      ✓ düzgündür (%s sətir, %s yoxlama)\n' \
  "$(wc -l < skriptler/crud_yoxla.sh | tr -d ' ')" \
  "$(grep -c '^sorqu ' skriptler/crud_yoxla.sh)"

echo ""
echo "  → 2) Bazanın vəziyyəti (əvvəl)"
EVVEL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      əməkdaş sayı: %s\n' "$EVVEL"

echo ""
echo "  → 3) Skript işlədilir (istifadəçinin əmri ilə)"
bash skriptler/crud_yoxla.sh
CIXIS=$?
echo ""
printf '      skriptin çıxış kodu: %s\n' "$CIXIS"
[ "$CIXIS" -eq 0 ] || { echo "  ✗ CRUD skripti uğursuz oldu"; exit 1; }

echo ""
echo "  → 4) Simmetriya yoxlaması"
SONRA=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
ZIBIL=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'test.crud.%@arti.edu.az';")
printf '      əvvəl: %s   sonra: %s   test zibili: %s\n' "$EVVEL" "$SONRA" "$ZIBIL"
[ "$EVVEL" = "$SONRA" ] || { echo "  ✗ sətir sayı dəyişdi!"; exit 1; }
[ "$ZIBIL" = "0" ] || { echo "  ✗ test zibili qaldı: $ZIBIL"; exit 1; }
echo "      ✓ baza tam əvvəlki vəziyyətindədir"

echo ""
echo "  → 5) Səhv port → skript aydın xəta verirmi?"
python3 -m http.server 4187 --bind 127.0.0.1 >/dev/null 2>&1 &
TUTAN=$!
sleep 1.5
CIXIS2=$(PORT=4187 bash skriptler/crud_yoxla.sh 2>&1)
KOD2=$?
kill $TUTAN 2>/dev/null
wait $TUTAN 2>/dev/null
printf '%s\n' "$CIXIS2" | head -3 | sed 's/^/      /'
printf '      exit kodu: %s\n' "$KOD2"
[ "$KOD2" -ne 0 ] || { echo "  ✗ məşğul portda skript uğurlu oldu — bu mümkün deyil"; exit 1; }
echo "      ✓ məşğul portu tanıdı və dayandı"

echo ""
echo "  → 6) YEKUN: bütün yoxlama alətləri bir yerdə"
printf '      a) tip yoxlaması   : '
npx tsc --noEmit && echo "✓ təmiz"
printf '      b) DTO matrisi     : '
npx tsx skriptler/dto_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      c) mapper          : '
npx tsx skriptler/mapper_yoxla.ts 2>&1 | grep -c 'JSON.stringify İŞLƏDİ' >/dev/null && echo "✓ işləyir"
printf '      d) servis yoxlaması: '
npx tsx skriptler/servis_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'

echo ""
echo "  → 7) Son vəziyyət"
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      bazada əməkdaş: %s\n' "$TOTAL"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }

echo ""
echo "  ✓ IIA.10 KEÇDİ — Dərs 2A-nın bütün nəticələri təsdiqləndi"
''')
