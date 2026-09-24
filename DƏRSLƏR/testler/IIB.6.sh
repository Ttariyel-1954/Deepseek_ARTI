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

EPOX=$(date +%s)
P="iib6.${EPOX}"
YARADILAN=""
temizle2() {
  say "DELETE FROM struktur.elmi_shura_uzvleri WHERE emekdas_id IN (SELECT id FROM kadrlar.emekdaslar WHERE email LIKE 'iib6.%@arti.edu.az');" >/dev/null
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iib6.%@arti.edu.az';" >/dev/null
  temizle
}
trap temizle2 EXIT INT TERM

EVVEL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
echo "  → başlanğıc: $EVVEL əməkdaş"

echo ""
echo "  → 1) POST /toplu/yarat — 3 sətir bir sorğuda"
KOD=$(curl -s -o /tmp/iib6.json -w '%{http_code}' -X POST "$EM/toplu/yarat" \
  -H 'Content-Type: application/json' \
  -d "{\"emekdaslar\":[
    {\"ad\":\"Toplu1\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.1@arti.edu.az\",\"maas\":1000},
    {\"ad\":\"Toplu2\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.2@arti.edu.az\",\"maas\":2000},
    {\"ad\":\"Toplu3\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.3@arti.edu.az\",\"maas\":3000}]}")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "201" ] || { echo "  ✗ 201 gözlənilirdi"; head -c 300 /tmp/iib6.json; exit 1; }
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iib6.json'))
problem = []
print('      göndərilən=%s  yaradılan=%s  atlanan=%s' % (d['gonderilen'], d['yaradilan'], d['atlanan']))
print('      ID-lər: %s' % d['idler'])
if d['yaradilan'] != 3: problem.append('3 sətir yaradılmadı')
if d['atlanan'] != 0: problem.append('atlanan 0 deyil')
if not all(isinstance(i, str) for i in d['idler']): problem.append('ID-lər mətn deyil (BigInt sızır!)')
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ toplu yaratma cavabı uğursuz"; exit 1; }

IDLER=$(python3 -c "import json;print(','.join(json.load(open('/tmp/iib6.json'))['idler']))")
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE '$P.%';")
printf '      bazada təsdiqləndi: %s sətir\n' "$N"
[ "$N" = "3" ] || { echo "  ✗ bazada 3 sətir yoxdur"; exit 1; }

echo ""
echo "  → 2) ATOMİKLİK — təkrar e-poçt BÜTÜN partiyanı ləğv edir"
KOD=$(curl -s -o /tmp/iib6b.json -w '%{http_code}' -X POST "$EM/toplu/yarat" \
  -H 'Content-Type: application/json' \
  -d "{\"emekdaslar\":[
    {\"ad\":\"Yeni\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.9@arti.edu.az\"},
    {\"ad\":\"Tekrar\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.1@arti.edu.az\"}]}")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi (təkrar e-poçt)"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iib6b.json'))
print('      mesaj: %s' % d['xeta']['mesaj'][:120])
" || true
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE '$P.%';")
printf '      bazada sətir: %s (3 olmalıdır — HEÇ NƏ yazılmadı)\n' "$N"
[ "$N" = "3" ] || { echo "  ✗ ATOMİKLİK POZULDU — yarımçıq partiya yazıldı!"; exit 1; }
echo "      ✓ atomiklik təsdiqləndi"

echo ""
echo "  → 3) tekrarlariAtla: true — təkrar ATLANIR"
KOD=$(curl -s -o /tmp/iib6c.json -w '%{http_code}' -X POST "$EM/toplu/yarat" \
  -H 'Content-Type: application/json' \
  -d "{\"tekrarlariAtla\":true,\"emekdaslar\":[
    {\"ad\":\"Yeni9\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.9@arti.edu.az\"},
    {\"ad\":\"Tekrar\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.1@arti.edu.az\"}]}")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "201" ] || { echo "  ✗ 201 gözlənilirdi"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iib6c.json'))
print('      göndərilən=%s yaradılan=%s atlanan=%s' % (d['gonderilen'], d['yaradilan'], d['atlanan']))
assert d['yaradilan'] == 1 and d['atlanan'] == 1, 'gözlənilən 1/1'
print('      ✓ 1 yaradıldı, 1 atlandı')
" || { echo "  ✗ skipDuplicates işləmədi"; exit 1; }

IDLER="$IDLER,$(python3 -c "import json;print(','.join(json.load(open('/tmp/iib6c.json'))['idler']))")"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE '$P.%';")
printf '      bazada sətir: %s (4 olmalıdır)\n' "$N"
[ "$N" = "4" ] || { echo "  ✗ sətir sayı gözlənilən deyil"; exit 1; }

echo ""
echo "  → 4) PATCH /toplu/aktivlik"
KOD=$(curl -s -o /tmp/iib6d.json -w '%{http_code}' -X PATCH "$EM/toplu/aktivlik" \
  -H 'Content-Type: application/json' -d "{\"idler\":[$IDLER],\"aktiv\":false}")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iib6d.json'))
print('      %s (dəyişən=%s tapılmayan=%s)' % (d['melumat'], d['deyisen'], d['tapilmayan']))
assert d['deyisen'] == 4, '4 sətir dəyişməli idi'
assert d['tapilmayan'] == 0
"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE '$P.%' AND NOT aktiv;")
printf '      bazada passiv: %s\n' "$N"
[ "$N" = "4" ] || { echo "  ✗ passiv sətir sayı səhvdir"; exit 1; }

echo ""
echo "  → 5) Mövcud olmayan ID → tapilmayan"
KOD=$(curl -s -o /tmp/iib6e.json -w '%{http_code}' -X PATCH "$EM/toplu/aktivlik" \
  -H 'Content-Type: application/json' -d "{\"idler\":[${IDLER%%,*},999999],\"aktiv\":true}")
python3 -c "
import json
d = json.load(open('/tmp/iib6e.json'))
print('      göndərilən=%s dəyişən=%s tapılmayan=%s' % (d['gonderilen_id'], d['deyisen'], d['tapilmayan']))
assert d['tapilmayan'] == 1, 'tapılmayan 1 olmalıdır'
print('      ✓ mövcud olmayan ID ayrıca bildirilir')
" || { echo "  ✗ tapılmayan ID yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 6) PATCH /toplu/maas-artim"
KOD=$(curl -s -o /dev/null -w '%{http_code}' -X PATCH "$EM/toplu/maas-artim" \
  -H 'Content-Type: application/json' -d "{\"faiz\":10,\"idler\":[$IDLER]}")
printf '      +10%% → %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
MAAS=$(say "SELECT maas FROM kadrlar.emekdaslar WHERE email='$P.1@arti.edu.az';")
printf '      1000 → %s\n' "$MAAS"
[ "$MAAS" = "1100.00" ] || { echo "  ✗ 10% artım səhvdir: $MAAS"; exit 1; }
echo "      ✓ atomik multiply düzgün işləyir"

echo ""
echo "  → 7) Filtrsiz maaş artımı → QADAĞAN"
FOND_EVVEL=$(say "SELECT COALESCE(sum(maas),0) FROM kadrlar.emekdaslar;")
KOD=$(curl -s -o /tmp/iib6f.json -w '%{http_code}' -X PATCH "$EM/toplu/maas-artim" \
  -H 'Content-Type: application/json' -d '{"faiz":50}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi (təhlükəsizlik qaydası)"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iib6f.json'))
print('      mesaj: %s' % d['xeta']['mesaj'])
"
FOND_SONRA=$(say "SELECT COALESCE(sum(maas),0) FROM kadrlar.emekdaslar;")
printf '      ümumi fondu: %s → %s\n' "$FOND_EVVEL" "$FOND_SONRA"
[ "$FOND_EVVEL" = "$FOND_SONRA" ] || { echo "  ✗ FONDU DƏYİŞDİ — qadağa işləmədi!"; exit 1; }
echo "      ✓ filtrsiz artım rədd edildi, fondu dəyişmədi"

echo ""
echo "  → 8) Validasiya xəta halları"
printf '      boş massiv          → %s\n' "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":[]}')"
printf '      massiv deyil        → %s\n' "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":"abc"}')"
printf '      element səhvdir     → %s\n' "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":[{"ad":"A"}]}')"
printf '      faiz həddən kənar   → %s\n' "$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":-100,\"idler\":[$IDLER]}")"
printf '      idler boş           → %s\n' "$(kod -X PATCH "$EM/toplu/aktivlik" -H 'Content-Type: application/json' -d '{"idler":[],"aktiv":true}')"
for K in \
  "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":[]}')" \
  "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":"abc"}')" \
  "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":[{"ad":"A"}]}')" \
  "$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":-100,\"idler\":[$IDLER]}")" \
  "$(kod -X PATCH "$EM/toplu/aktivlik" -H 'Content-Type: application/json' -d '{"idler":[],"aktiv":true}')"; do
  [ "$K" = "400" ] || { echo "  ✗ 400 gözlənilirdi, alındı: $K"; exit 1; }
done
echo "      ✓ beş validasiya halı düzgün tutulur"

echo ""
echo "  → 9) GET /toplu/atomiklik — rollback sübutu"
govde "$EM/toplu/atomiklik" -o /tmp/iib6g.json
python3 -c "
import json
d = json.load(open('/tmp/iib6g.json'))
print('      cəhd=%s  bazada qalan=%s  audit artımı=%s' % (d['cehd_edilen'], d['bazada_qalan'], d['audit_artimi']))
print('      izah: %s' % d['izah'])
assert d['bazada_qalan'] == 0, 'rollback işləmədi'
assert d['audit_artimi'] == 0, 'audit loqu artdı — rollback natamamdır'
print('      ✓ rollback: nə məlumat, nə audit qeydi qalmadı')
" || { echo "  ✗ atomiklik yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 10) Təmizlik"
say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE '$P.%';" >/dev/null
SONRA=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      emekdaş: %s → %s\n' "$EVVEL" "$SONRA"
[ "$EVVEL" = "$SONRA" ] || { echo "  ✗ baza vəziyyəti dəyişdi"; exit 1; }
echo "      ✓ baza əvvəlki vəziyyətindədir"

echo ""
echo "  ✓ IIB.6 KEÇDİ — bütün toplu endpoint-lər düzgün işləyir"
)
