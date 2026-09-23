LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur — bu qovluq layihə deyil: $(pwd)"; exit 1; }

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
)
