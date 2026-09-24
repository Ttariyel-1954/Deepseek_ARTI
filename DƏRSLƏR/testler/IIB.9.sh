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
echo "  → 1) Audit endpoint-ləri"
KOD=$(kod "$API/audit?limit=3")
printf '      GET /audit?limit=3 → %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$API/audit?limit=3" -o /tmp/iib9.json
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iib9.json'))
problem = []
print('      cem=%s sehife=%s/%s gosterilen=%s' % (d['cem'], d['sehife'], d['sehife_sayi'], len(d['melumat'])))
for q in d['melumat']:
    print('        #%s %s %s setir=%s' % (q['id'], q['cedvel_adi'], q['emeliyyat'], q['setir_id']))
if len(d['melumat']) != 3: problem.append('3 qeyd gözlənilirdi')
if not isinstance(d['melumat'][0]['id'], str): problem.append('id mətn deyil (BigInt sızır!)')
if 'T' not in d['melumat'][0]['vaxt']: problem.append('vaxt ISO deyil')
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ audit siyahısı uğursuz"; exit 1; }

echo ""
echo "  → 2) Statistika endpoint-ləri"
K=$(kod "$API/audit/statistika")
printf '      GET /audit/statistika → %s\n' "$K"
[ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi — marşrut sırası problemi!"; exit 1; }
govde "$API/audit/statistika" -o /tmp/iib9b.json
python3 -c "
import json
d = json.load(open('/tmp/iib9b.json'))
print('      cem qeyd=%s  cədvəl sayı=%s' % (d['cem_qeyd'], d['cedvel_sayi']))
print('      əməliyyat: %s' % '  '.join('%s=%s' % (x['emeliyyat'], x['cem']) for x in d['emeliyyat_uzre']))
assert d['cem_qeyd'] > 1000
assert sum(x['cem'] for x in d['emeliyyat_uzre']) == d['cem_qeyd'], 'əməliyyat cəmi uyğun deyil'
print('      ✓ paylanma düzgündür')
" || { echo "  ✗ audit statistikası uğursuz"; exit 1; }

echo ""
echo "  → 3) Süzgəclər"
K=$(kod "$API/audit?cedvel=kadrlar.emekdaslar&limit=2")
printf '      cedvel süzgəci     → %s\n' "$K"
[ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$API/audit?cedvel=kadrlar.emekdaslar&limit=5" -o /tmp/iib9c.json
python3 -c "
import json
d = json.load(open('/tmp/iib9c.json'))
assert all(q['cedvel_adi'] == 'kadrlar.emekdaslar' for q in d['melumat']), 'süzgəc işləmir'
print('      ✓ cədvəl süzgəci: %s qeyd, hamısı kadrlar.emekdaslar' % d['cem'])
" || { echo "  ✗ cədvəl süzgəci uğursuz"; exit 1; }
K=$(kod "$API/audit?emeliyyat=DELETE&limit=2")
printf '      emeliyyat süzgəci  → %s\n' "$K"
govde "$API/audit?emeliyyat=DELETE&limit=5" -o /tmp/iib9d.json
python3 -c "
import json
d = json.load(open('/tmp/iib9d.json'))
assert all(q['emeliyyat'] == 'DELETE' for q in d['melumat']), 'əмəliyyat süzgəci işləmir'
print('      ✓ əməliyyat süzgəci: %s qeyd, hamısı DELETE' % d['cem'])
" || { echo "  ✗ əməliyyat süzgəci uğursuz"; exit 1; }

echo ""
echo "  → 4) Trigger nümayişi (HTTP)"
K=$(kod "$API/audit/trigger-numayisi")
printf '      GET /audit/trigger-numayisi → %s\n' "$K"
[ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$API/audit/trigger-numayisi" -o /tmp/iib9e.json
python3 -c "
import json
d = json.load(open('/tmp/iib9e.json'))
print('      audit artımı: %s' % d['audit_artimi'])
print('      izah: %s' % d['izah'])
print('      əməliyyatlar: %s' % ','.join(q['emeliyyat'] for q in d['qeydler']))
assert d['audit_artimi'] == 3, '3 qeyd gözlənilirdi'
assert [q['emeliyyat'] for q in d['qeydler']] == ['INSERT','UPDATE','DELETE']
assert all(isinstance(q['setir_id'], str) for q in d['qeydler'])
print('      ✓ trigger INSERT/UPDATE/DELETE yazdı, setir_id mətndir')
" || { echo "  ✗ trigger nümayişi uğursuz"; exit 1; }

echo ""
echo "  → 5) Tranzaksiya nümayişi (HTTP)"
K=$(kod "$API/audit/tranzaksiya-numayisi")
printf '      GET /audit/tranzaksiya-numayisi → %s\n' "$K"
[ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$API/audit/tranzaksiya-numayisi" -o /tmp/iib9f.json
python3 -c "
import json
d = json.load(open('/tmp/iib9f.json'))
print('      əməkdaş=%s  audit artımı=%s' % (d['bazada_qalan_emekdas'], d['bazada_qalan_audit']))
print('      izah: %s' % d['izah'])
assert d['bazada_qalan_emekdas'] == 0 and d['bazada_qalan_audit'] == 0, 'rollback işləmədi'
print('      ✓ əməkdaş və audit BİR tranzaksiyada geri qaytarıldı')
" || { echo "  ✗ tranzaksiya nümayişi uğursuz"; exit 1; }

echo ""
echo "  → 6) MARŞRUT SIRASI — statistika ↔ :id toqquşması"
echo "      ── bütün 2 seqmentli yollar (toqquşma riski olan) ──"
for y in "emekdaslar/statistika" "emekdaslar/5" "emekdaslar/abc" "audit/statistika" "audit/1" "audit/abc"; do
  printf '      %-26s → %s\n' "/$y" "$(kod "$API/$y")"
done
[ "$(kod "$API/emekdaslar/statistika")" = "200" ] || { echo "  ✗ statistika işləmir — controller sırası!"; exit 1; }
[ "$(kod "$API/emekdaslar/5")" = "200" ] || { echo "  ✗ :id işləmir"; exit 1; }
[ "$(kod "$API/emekdaslar/abc")" = "400" ] || { echo "  ✗ mətn ID 400 verməlidir"; exit 1; }
[ "$(kod "$API/audit/statistika")" = "200" ] || { echo "  ✗ audit statistikası işləmir"; exit 1; }
[ "$(kod "$API/audit/1")" = "200" ] || { echo "  ✗ audit :id işləmir"; exit 1; }
[ "$(kod "$API/audit/abc")" = "400" ] || { echo "  ✗ audit mətn ID 400 verməlidir"; exit 1; }
echo "      ✓ KONKRET yollar :id-dən əvvəl qeydiyyatdadır"

echo ""
echo "  → 7) 3 seqmentli yollar (toqquşmamalıdır)"
for y in "emekdaslar/6/icmal" "emekdaslar/6/tam" "emekdaslar/6/doktorantlar" "emekdaslar/toplu/atomiklik"; do
  printf '      %-34s → %s\n' "/$y" "$(kod "$API/$y")"
  [ "$(kod "$API/$y")" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
done
echo "      ✓ uzun yollar toqquşmur"

echo ""
echo "  → 8) Xəta halları"
printf '      audit/99999999  → %s\n' "$(kod "$API/audit/99999999")"
printf '      audit?limit=500 → %s\n' "$(kod "$API/audit?limit=500")"
printf '      audit?emeliyyat=SIL → %s\n' "$(kod "$API/audit?emeliyyat=SIL")"
[ "$(kod "$API/audit/99999999")" = "404" ] || { echo "  ✗ 404 gözlənilirdi"; exit 1; }
[ "$(kod "$API/audit?limit=500")" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
echo "      ✓ xəta halları düzgündür"

echo ""
echo "  ✓ IIB.9 KEÇDİ — audit endpoint-ləri və marşrut sırası düzgündür"
)
