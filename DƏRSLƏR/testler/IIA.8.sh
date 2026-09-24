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
E1="iia8a.${EPOX}@arti.edu.az"
E2="iia8b.${EPOX}@arti.edu.az"
ID1=""
ID2=""

temizle2() {
  say "DELETE FROM struktur.elmi_shura_uzvleri WHERE emekdas_id IN (SELECT id FROM kadrlar.emekdaslar WHERE email LIKE 'iia8%.%@arti.edu.az');" >/dev/null
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iia8%.%@arti.edu.az';" >/dev/null
  temizle
}
trap temizle2 EXIT INT TERM

echo ""
echo "  → 1) İki müvəqqəti əməkdaş yaradılır"
govde -X POST "$BAZ" -H 'Content-Type: application/json' \
  -d "{\"ad\":\"Asili\",\"soyad\":\"Var\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$E1\"}" \
  -o /tmp/iia8a.json
ID1=$(python3 -c "import json;print(json.load(open('/tmp/iia8a.json')).get('id',''))" 2>/dev/null)
govde -X POST "$BAZ" -H 'Content-Type: application/json' \
  -d "{\"ad\":\"Asili\",\"soyad\":\"Yox\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$E2\"}" \
  -o /tmp/iia8b.json
ID2=$(python3 -c "import json;print(json.load(open('/tmp/iia8b.json')).get('id',''))" 2>/dev/null)
[ -n "$ID1" ] && [ -n "$ID2" ] || { echo "  ✗ əməkdaşlar yaradıla bilmədi"; exit 1; }
printf '      asılısı OLACAQ : ID %s\n' "$ID1"
printf '      asılısı OLMAYAN: ID %s\n' "$ID2"

echo ""
printf '  → 2) ID %s üçün şura üzvü sətri əlavə edilir (psql ilə)\n' "$ID1"
say "INSERT INTO struktur.elmi_shura_uzvleri (emekdas_id, ad_soyad) VALUES ($ID1, 'IIA8 Test Uzv');" >/dev/null
N=$(say "SELECT count(*) FROM struktur.elmi_shura_uzvleri WHERE emekdas_id=$ID1;")
printf '      asılı qeyd sayı: %s\n' "$N"
[ "$N" = "1" ] || { echo "  ✗ asılı qeyd yaradıla bilmədi"; exit 1; }

echo ""
echo "  → 3) Adi SQL ilə silmək MÜMKÜN DEYİL (sübut)"
psql "$DBURL" -c "DELETE FROM kadrlar.emekdaslar WHERE id=$ID1;" 2>&1 | head -2 | sed 's/^/      /'
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE id=$ID1;")
printf '      amma sətir hələ də yerindədir: %s\n' "$N"
[ "$N" = "1" ] || { echo "  ✗ sətir gözlənilmədən silindi!"; exit 1; }
echo "      ✓ PostgreSQL xarici açarı qoruyur"

echo ""
echo "  → 4) API ilə DELETE → YUMŞAQ silmə"
KOD=$(curl -s -o /tmp/iia8c.json -w '%{http_code}' -X DELETE "$BAZ/$ID1")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; head -c 300 /tmp/iia8c.json; exit 1; }
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iia8c.json'))
print('      nov          :', d['nov'])
print('      mesaj        :', d['mesaj'])
print('      asılı qeydlər:', json.dumps(d['asili_qeydler'], ensure_ascii=False))
assert d['nov'] == 'soft', "soft gözlənilirdi, alındı: %r" % d['nov']
assert d['asili_qeydler'].get('elmi_shura_uzvleri') == 1, d['asili_qeydler']
print('      ✓ nov = soft, asılı qeyd sayıldı')
PSON
[ $? -eq 0 ] || { echo "  ✗ yumşaq silmə yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 5) Sətir bazada QALIR, amma aktiv=false"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE id=$ID1;")
A=$(say "SELECT aktiv FROM kadrlar.emekdaslar WHERE id=$ID1;")
printf '      bazada: %s   aktiv: %s\n' "$N" "$A"
[ "$N" = "1" ] || { echo "  ✗ sətir bazadan silindi — yumşaq silmə işləmədi"; exit 1; }
[ "$A" = "f" ] || { echo "  ✗ aktiv=false deyil: $A"; exit 1; }
echo "      ✓ sətir qorundu, sadəcə passiv edildi"

echo ""
echo "  → 6) Siyahıda passiv görünür, aktiv siyahıda yox"
N1=$(govde "$BAZ?aktiv=passiv" | python3 -c "import json,sys;print(json.load(sys.stdin)['cem'])")
N2=$(govde "$BAZ?aktiv=aktiv" | python3 -c "import json,sys;print(json.load(sys.stdin)['cem'])")
printf '      aktiv=passiv → %s   aktiv=aktiv → %s\n' "$N1" "$N2"
[ "$N1" -ge 1 ] || { echo "  ✗ passiv siyahıda görünmür"; exit 1; }
echo "      ✓ filtr passiv sətri göstərir"

echo ""
echo "  → 7) Asılısız sətir → ADİ silmə"
KOD=$(curl -s -o /tmp/iia8d.json -w '%{http_code}' -X DELETE "$BAZ/$ID2")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; head -c 300 /tmp/iia8d.json; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iia8d.json'))
print('      nov  :', d['nov'])
print('      mesaj:', d['mesaj'])
assert d['nov'] == 'hard', 'hard gözlənilirdi: %r' % d['nov']
" || { echo "  ✗ adi silmə yoxlaması uğursuz"; exit 1; }
echo "      ✓ nov = hard"

echo ""
echo "  → 8) Silinən sətir həqiqətən getdi (mənfi təsdiq)"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE id=$ID2;")
KOD=$(kod "$BAZ/$ID2")
printf '      bazada: %s   GET /%s → %s\n' "$N" "$ID2" "$KOD"
[ "$N" = "0" ] || { echo "  ✗ sətir bazada qaldı"; exit 1; }
[ "$KOD" = "404" ] || { echo "  ✗ 404 gözlənilirdi"; exit 1; }
echo "      ✓ həm bazadan, həm API-dən getdi"

echo ""
echo "  → 9) İdempotentlik — təkrar DELETE"
KOD=$(kod -X DELETE "$BAZ/$ID2")
printf '      ikinci DELETE → %s\n' "$KOD"
[ "$KOD" = "404" ] || { echo "  ✗ 404 gözlənilirdi"; exit 1; }
echo "      ✓ təkrar silmə xəta vermir, sadəcə 404 qaytarır"

echo ""
echo "  → 10) Yox olan ID → 404"
KOD=$(kod -X DELETE "$BAZ/999999")
printf '      DELETE /999999 → %s\n' "$KOD"
[ "$KOD" = "404" ] || { echo "  ✗ 404 gözlənilirdi"; exit 1; }
echo "      ✓ mövcud olmayan ID 404 qaytarır"

echo ""
echo "  → 11) Təmizlik"
say "DELETE FROM struktur.elmi_shura_uzvleri WHERE emekdas_id=$ID1;" >/dev/null
say "DELETE FROM kadrlar.emekdaslar WHERE id=$ID1;" >/dev/null
ID1=""
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
ZIBIL=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'iia8%.%@arti.edu.az';")
printf '      ümumi əməkdaş: %s   test zibili: %s\n' "$TOTAL" "$ZIBIL"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }
[ "$ZIBIL" = "0" ] || { echo "  ✗ test zibili qaldı: $ZIBIL"; exit 1; }
echo "      ✓ baza tam təmizdir"

echo ""
echo "  ✓ IIA.8 KEÇDİ — iki strategiyalı silmə düzgün işləyir"
)
