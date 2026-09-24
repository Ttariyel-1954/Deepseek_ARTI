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

ID=6

echo ""
echo "  → 1) icmal() — yalnız saylar"
KOD=$(kod "$EM/$ID/icmal")
printf '      GET /$ID/icmal → %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$EM/$ID/icmal" -o /tmp/iib4.json
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iib4.json'))
problem = []
print('      %s' % d['tam_ad'])
print('      saylar: %s   cem=%s' % (json.dumps(d['saylar'], ensure_ascii=False), d['cem_elaqe']))
if not isinstance(d['emekdas_id'], str): problem.append('emekdas_id mətn deyil')
if d['cem_elaqe'] != sum(d['saylar'].values()): problem.append('cem_elaqe uyğun deyil')
if d['saylar']['doktorantlar'] != 4: problem.append('doktorant sayı 4 deyil: %r' % d['saylar']['doktorantlar'])
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ icmal yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 2) tam() — bütün əlaqələr paralel"
KOD=$(kod "$EM/$ID/tam")
printf '      GET /$ID/tam → %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$EM/$ID/tam" -o /tmp/iib4b.json
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iib4b.json'))
i = json.load(open('/tmp/iib4.json'))
problem = []
print('      doktorant=%s sertifikat=%s məzuniyyət=%s təcrübə=%s layihə=%s şura=%s (%s ms)' % (
  len(d['doktorantlar']), len(d['sertifikatlar']), len(d['mezuniyyetler']),
  len(d['tecrube']), len(d['layiheler']), len(d['shura_uzvleri']), d['cekme_ms']))
if len(d['doktorantlar']) != i['saylar']['doktorantlar']: problem.append('doktorant sayı icmal ilə uyğun deyil')
if len(d['shura_uzvleri']) != i['saylar']['shura_uzvleri']: problem.append('şura sayı uyğun deyil')
for k in ('doktorantlar','sertifikatlar','mezuniyyetler','tecrube','layiheler','shura_uzvleri'):
    if not isinstance(d[k], list): problem.append('%s massiv deyil' % k)
ke = d['doktorantlar'][0] if d['doktorantlar'] else None
if ke and ke['qebul_tarixi'] and len(ke['qebul_tarixi']) != 10:
    problem.append('tarix YYYY-MM-DD deyil: %r' % ke['qebul_tarixi'])
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ tam yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 3) Altı ayrı əlaqə endpoint-i"
for y in doktorantlar sertifikatlar mezuniyyetler tecrube layiheler shura; do
  K=$(kod "$EM/$ID/$y")
  N=$(govde "$EM/$ID/$y" | python3 -c "import json,sys;print(len(json.load(sys.stdin)))")
  printf '      /%-16s → %s  (%s sətir)\n' "$y" "$K" "$N"
  [ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
done

echo ""
echo "  → 4) tam-ad() — baza funksiyası ilə"
govde "$EM/$ID/tam-ad" -o /tmp/iib4c.json
TS=$(python3 -c "import json;print(json.load(open('/tmp/iib4b.json'))['tam_ad'])")
SQL=$(python3 -c "import json;print(json.load(open('/tmp/iib4c.json'))['tam_ad'])")
printf '      TypeScript : %s\n' "$TS"
printf '      SQL        : %s\n' "$SQL"
[ "$TS" = "$SQL" ] || { echo "  ✗ iki üsul fərqli nəticə verir!"; exit 1; }
echo "      ✓ hər iki üsul eyni nəticə verir"

echo ""
echo "  → 5) tam-bir-sorqu() — eyni nəticə, fərqli üsul"
K=$(kod "$EM/$ID/tam-bir-sorqu")
printf '      GET /$ID/tam-bir-sorqu → %s\n' "$K"
[ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$EM/$ID/tam-bir-sorqu" -o /tmp/iib4d.json
python3 -c "
import json
a = json.load(open('/tmp/iib4b.json'))
b = json.load(open('/tmp/iib4d.json'))
assert a['tam_ad'] == b['tam_ad'], 'tam_ad fərqlidir'
assert len(a['doktorantlar']) == len(b['doktorantlar']), 'doktorant sayı fərqlidir'
assert len(a['shura_uzvleri']) == len(b['shura_uzvleri']), 'şura sayı fərqlidir'
print('      ✓ hər iki üsul EYNİ nəticə verir')
" || { echo "  ✗ nəticələr fərqlidir"; exit 1; }

echo ""
echo "  → 6) Boş əlaqə boş massiv qaytarır"
govde "$EM/2/tam" -o /tmp/iib4e.json
python3 -c "
import json
d = json.load(open('/tmp/iib4e.json'))
print('      ID 2 — %s: doktorant=%s sertifikat=%s' % (d['tam_ad'], len(d['doktorantlar']), len(d['sertifikatlar'])))
for k in ('doktorantlar','sertifikatlar','mezuniyyetler','tecrube','layiheler','shura_uzvleri'):
    assert isinstance(d[k], list), '%s massiv deyil' % k
print('      ✓ boş əlaqələr [] qaytarır, null yox')
" || { echo "  ✗ boş əlaqə yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 7) Xəta halları"
printf '      /999999/icmal      → %s\n' "$(kod "$EM/999999/icmal")"
printf '      /999999/tam        → %s\n' "$(kod "$EM/999999/tam")"
printf '      /abc/icmal         → %s\n' "$(kod "$EM/abc/icmal")"
[ "$(kod "$EM/999999/icmal")" = "404" ] || { echo "  ✗ 404 gözlənilirdi"; exit 1; }
[ "$(kod "$EM/abc/icmal")" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
echo "      ✓ xəta halları düzgündür"

echo ""
echo "  ✓ IIB.4 KEÇDİ — bütün əlaqə endpoint-ləri işləyir"
)
