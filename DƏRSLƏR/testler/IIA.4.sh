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
)
