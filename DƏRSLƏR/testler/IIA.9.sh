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
)
