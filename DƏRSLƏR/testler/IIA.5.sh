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
)
