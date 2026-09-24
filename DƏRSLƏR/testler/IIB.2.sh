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

PORT="${PORT:-4000}"
LOQ="/tmp/arti_iib_${PORT}.log"
API="http://localhost:$PORT/api/v1"
EM="$API/emekdaslar"

npm run build >/tmp/arti_iib_build.log 2>&1 \
  || { echo "  ✗ build uğursuz"; tail -n 20 /tmp/arti_iib_build.log | sed 's/^/      /'; exit 1; }

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
  curl -fsS "$API/saglamliq" -o /dev/null 2>/dev/null && { hazir=1; break; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.5
done
[ "$hazir" = "1" ] || { echo "  ✗ server qalxmadı"; tail -n 20 "$LOQ" | sed 's/^/      /'; exit 1; }
printf '  ✓ server hazırdır (%s cəhd)\n' "$i"

kod()  { curl -s -o /dev/null -w '%{http_code}' "$@"; }
govde(){ curl -s "$@"; }

echo ""
echo "  → 1) GET /emekdaslar/statistika"
KOD=$(kod "$EM/statistika")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi (marşrut sırası!)"; exit 1; }
govde "$EM/statistika" -o /tmp/iib2.json
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iib2.json'))
problem = []
print('      əməkdaş : cem=%s aktiv=%s passiv=%s' % (d['emekdas']['cem'], d['emekdas']['aktiv'], d['emekdas']['passiv']))
print('      maaş    : fondu=%s orta=%s min=%s maks=%s' % (d['maas']['fondu'], d['maas']['orta'], d['maas']['min'], d['maas']['maks']))
print('      baza fn : fondu=%s sert_orta=%s' % (d['baza_funksiyalari']['maas_fondu'], d['baza_funksiyalari']['sertifikasiya_ortalamasi']))
print('      əlaqələr: %s' % json.dumps(d['elaqeler'], ensure_ascii=False))
print('      cədvəl  : %s   hesablanma: %s ms' % (d['cedvel_sayi'], d['hesablanma_ms']))
if d['emekdas']['cem'] != 14: problem.append('cem 14 deyil: %r' % d['emekdas']['cem'])
if d['emekdas']['aktiv'] + d['emekdas']['passiv'] != d['emekdas']['cem']:
    problem.append('aktiv + passiv != cem')
if not (d['maas']['min'] < d['maas']['orta'] < d['maas']['maks']):
    problem.append('min < orta < maks pozulub')
if abs(d['maas']['fondu'] - d['baza_funksiyalari']['maas_fondu']) > 0.01:
    problem.append('Prisma fondu != PL/pgSQL fondu')
if d['cedvel_sayi'] != 48: problem.append('cədvəl sayı 48 deyil')
if not isinstance(d['maas']['orta'], float): problem.append('orta maaş ədəd deyil')
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ statistika cavabı yoxlamadan keçmədi"; exit 1; }
echo "      ✓ bütün göstəricilər düzgündür"

echo ""
echo "  → 2) API rəqəmləri SQL ilə TUTUŞDURULUR"
API_CEM=$(python3 -c "import json;print(json.load(open('/tmp/iib2.json'))['emekdas']['cem'])")
SQL_CEM=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
API_AKTIV=$(python3 -c "import json;print(json.load(open('/tmp/iib2.json'))['emekdas']['aktiv'])")
SQL_AKTIV=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE aktiv;")
API_FOND=$(python3 -c "import json;print(json.load(open('/tmp/iib2.json'))['maas']['fondu'])")
SQL_FOND=$(say "SELECT COALESCE(sum(maas),0) FROM kadrlar.emekdaslar WHERE aktiv;")
printf '      cem    : API=%s  SQL=%s\n' "$API_CEM" "$SQL_CEM"
printf '      aktiv  : API=%s  SQL=%s\n' "$API_AKTIV" "$SQL_AKTIV"
printf '      fondu  : API=%s  SQL=%s\n' "$API_FOND" "$SQL_FOND"
[ "$API_CEM" = "$SQL_CEM" ] || { echo "  ✗ cem uyğun deyil"; exit 1; }
[ "$API_AKTIV" = "$SQL_AKTIV" ] || { echo "  ✗ aktiv uyğun deyil"; exit 1; }
python3 -c "
a=float('$API_FOND'); b=float('$SQL_FOND')
assert abs(a-b) < 0.01, 'fondu uyğun deyil: %s vs %s' % (a,b)
print('      ✓ üç göstərici də SQL ilə üst-üstə düşür')
" || { echo "  ✗ fondu uyğun deyil"; exit 1; }

echo ""
echo "  → 3) Mərkəzlər üzrə qruplaşdırma"
govde "$EM/statistika/merkezler" -o /tmp/iib2b.json
python3 - <<'PSON'
import json
m = json.load(open('/tmp/iib2b.json'))
u = json.load(open('/tmp/iib2.json'))
problem = []
print('      qrup sayı: %s' % len(m))
for x in m[:5]:
    print('        %-34s sayı=%s orta=%s fondu=%s' % (x['merkez'][:34], x['emekdas_sayi'], x['orta_maas'], x['maas_fondu']))
cem = sum(x['emekdas_sayi'] for x in m)
if cem != u['emekdas']['aktiv']:
    problem.append('qrupların cəmi (%s) aktiv sayına (%s) bərabər deyil' % (cem, u['emekdas']['aktiv']))
if not all(isinstance(x['merkez'], str) and x['merkez'] for x in m):
    problem.append('mərkəz adı boşdur — Map birləşməsi işləmədi')
if not all(x['merkez_id'] is not None for x in m):
    problem.append('merkez_id null gəldi')
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ mərkəz qruplaşdırması uğursuz"; exit 1; }
echo "      ✓ qrupların cəmi ümumi sayla üst-üstə düşür"

echo ""
echo "  → 4) Parametrli baza funksiyası"
govde "$EM/statistika/shobe-sayi/2" -o /tmp/iib2c.json
python3 -c "
import json
d = json.load(open('/tmp/iib2c.json'))
print('      merkez %s → %s şöbə' % (d['merkez_id'], d['shobe_sayi']))
assert isinstance(d['shobe_sayi'], int), 'şöbə sayı tam ədəd deyil'
assert d['shobe_sayi'] > 0, 'şöbə sayı 0-dır'
print('      ✓ SQL funksiyası işləyir')
" || { echo "  ✗ baza funksiyası uğursuz"; exit 1; }

echo ""
echo "  → 5) N+1 olmayan bütün mərkəzlər"
govde "$EM/statistika/merkezler-tam" -o /tmp/iib2d.json
python3 -c "
import json
d = json.load(open('/tmp/iib2d.json'))
print('      %s mərkəz, cəmi %s şöbə, %s əməkdaş' % (len(d), sum(x['shobe_sayi'] for x in d), sum(x['emekdas_sayi'] for x in d)))
assert len(d) == 10, '10 mərkəz gözlənilirdi'
assert sum(x['shobe_sayi'] for x in d) == 36, '36 şöbə gözlənilirdi'
assert sum(x['emekdas_sayi'] for x in d) == 14, '14 əməkdaş gözlənilirdi'
print('      ✓ 3 sorğu ilə 10 mərkəz + 36 şöbə + 14 əməkdaş')
" || { echo "  ✗ mərkəz tam siyahısı uğursuz"; exit 1; }

echo ""
echo "  → 6) Xəta halları"
for y in "yad_parametr=1" "siralama=parol_hash" "aktiv=səhv" "min_say=0"; do
  K=$(kod "$EM/statistika/merkezler?$y")
  printf '      ?%-24s → %s\n' "$y" "$K"
  [ "$K" = "400" ] || { echo "      ✗ 400 gözlənilirdi"; exit 1; }
done
echo "      ✓ DTO bütün səhv parametrləri tutur"

echo ""
echo "  ✓ IIB.2 KEÇDİ — statistika endpoint-ləri düzgün işləyir"
)
