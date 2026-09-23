LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur — bu qovluq layihə deyil: $(pwd)"; exit 1; }

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
)
