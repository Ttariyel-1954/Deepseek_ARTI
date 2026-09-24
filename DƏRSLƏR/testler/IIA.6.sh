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
EPOST="iia6.${EPOX}@arti.edu.az"
YENI=""

temizle2() {
  if [ -n "$YENI" ]; then
    printf '  → təmizlik: ID %s silinir\n' "$YENI"
    curl -s -o /dev/null -X DELETE "$BAZ/$YENI"
  fi
  say "DELETE FROM struktur.elmi_shura_uzvleri WHERE emekdas_id IN (SELECT id FROM kadrlar.emekdaslar WHERE email LIKE 'iia6.%@arti.edu.az');" >/dev/null
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iia6.%@arti.edu.az';" >/dev/null
  temizle
}
trap temizle2 EXIT INT TERM

DUZGUN="{\"ad\":\"Test\",\"soyad\":\"IIA6\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"merkez_id\":1,\"email\":\"$EPOST\",\"ise_baslama\":\"2026-03-01\",\"maas\":1234.56}"

echo ""
echo "  → 1) Düzgün POST"
KOD=$(curl -s -o /tmp/iia6a.json -w '%{http_code}' \
      -X POST "$BAZ" -H 'Content-Type: application/json' -d "$DUZGUN")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "201" ] || { echo "  ✗ 201 Created gözlənilirdi"; head -c 300 /tmp/iia6a.json; exit 1; }
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iia6a.json'))
print('      id     :', d['id'], type(d['id']).__name__)
print('      tam_ad :', d['tam_ad'])
print('      vezife :', d['vezife']['ad'])
print('      status :', d['is_statusu']['ad'])
print('      maas   :', d['maas'])
print('      tarix  :', d['ise_baslama'])
assert d['ad'] == 'Test' and d['soyad'] == 'IIA6'
assert d['maas'] == '1234.56', 'maas formatı səhvdir: %r' % d['maas']
assert d['ise_baslama'] == '2026-03-01', 'tarix səhvdir: %r' % d['ise_baslama']
assert d['is_statusu']['id'] == 1, 'standart status tətbiq olunmadı'
assert d['aktiv'] is True
print('      ✓ bütün sahələr düzgündür')
PSON
[ $? -eq 0 ] || { echo "  ✗ cavab yoxlaması uğursuz"; exit 1; }

YENI=$(python3 -c "import json;print(json.load(open('/tmp/iia6a.json'))['id'])" 2>/dev/null)

echo ""
echo "  → 2) Yaradılan sətir bazadadır"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email='$EPOST';")
printf '      e-poçt üzrə tapıldı: %s\n' "$N"
[ "$N" = "1" ] || { echo "  ✗ sətir bazada tapılmadı"; exit 1; }

echo ""
echo "  → 3) TƏKRAR e-poçt → 409"
KOD=$(curl -s -o /tmp/iia6b.json -w '%{http_code}' \
      -X POST "$BAZ" -H 'Content-Type: application/json' -d "$DUZGUN")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "409" ] || { echo "  ✗ 409 Conflict gözlənilirdi (P2002 çevrilməsi)"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iia6b.json'))
print('      kod  :', d['xeta']['kod'])
print('      mesaj:', d['xeta']['mesaj'])
assert d['xeta']['kod'] == 'TOQQUSMA', d['xeta']['kod']
"
echo "      ✓ P2002 → 409 TOQQUSMA"

echo ""
echo "  → 4) Natamam gövdə → 400"
KOD=$(curl -s -o /tmp/iia6c.json -w '%{http_code}' \
      -X POST "$BAZ" -H 'Content-Type: application/json' -d '{"ad":"A"}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iia6c.json'))
print('      kod     :', d['xeta']['kod'])
print('      mesaj   :', d['xeta']['mesaj'])
for x in d['xeta'].get('detallar', [])[:4]:
    print('        ·', x)
assert d['xeta']['kod'] == 'YANLIS_SORGU'
assert len(d['xeta'].get('detallar', [])) >= 3, 'validasiya detalları gəlmədi'
"
echo "      ✓ validasiya xətaları siyahı kimi gəlir"

echo ""
echo "  → 5) Yox olan vəzifə (xarici açar) → 400"
KOD=$(kod -X POST "$BAZ" -H 'Content-Type: application/json' \
      -d '{"ad":"Test","soyad":"FK","ata_adi":"Sistem","cinsiyyet_id":1,"vezife_id":99}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi (P2003 çevrilməsi)"; exit 1; }
echo "      ✓ P2003 → 400 YANLIS_SORGU"

echo ""
echo "  → 6) Gövdədə YAD sahə → 400"
KOD=$(kod -X POST "$BAZ" -H 'Content-Type: application/json' \
      -d '{"ad":"Test","soyad":"Yad","ata_adi":"Sistem","cinsiyyet_id":1,"vezife_id":6,"yoluxucu":true}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
echo "      ✓ forbidNonWhitelisted işləyir"

echo ""
echo "  → 7) Cinsiyyet ID həddən kənar → 400"
KOD=$(kod -X POST "$BAZ" -H 'Content-Type: application/json' \
      -d '{"ad":"Test","soyad":"Hedd","ata_adi":"Sistem","cinsiyyet_id":99,"vezife_id":6}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
echo "      ✓ DTO həddi işləyir"

echo ""
echo "  → 8) Bazada YALNIZ bizim sətir var"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'iia6.%@arti.edu.az';")
printf '      iia6.* e-poçtlu sətir: %s (1 olmalıdır — təkrar 409 aldı)\n' "$N"
[ "$N" = "1" ] || { echo "  ✗ gözlənilməz sətir sayı: $N"; exit 1; }
echo "      ✓ təkrar cəhd bazaya heç nə yazmadı"

echo ""
echo "  → 9) Təmizlik"
curl -s -o /dev/null -X DELETE "$BAZ/$YENI"
YENI=""
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'iia6.%@arti.edu.az';")
printf '      qalan sətir: %s\n' "$N"
[ "$N" = "0" ] || { echo "  ✗ təmizlik alınmadı"; exit 1; }
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      ümumi əməkdaş: %s\n' "$TOTAL"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }

echo ""
echo "  ✓ IIA.6 KEÇDİ — yaratma və dörd xəta halı düzgün işləyir"
)
