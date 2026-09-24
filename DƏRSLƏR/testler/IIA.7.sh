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
)
