LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── TOKENSİZ çağırış ──"
printf '  HTTP %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/tehsil/pasport/SER-2024-001/yoxla")"

echo "── Cavab ──"
curl -s "$A/tehsil/pasport/SER-2024-001/yoxla" | python3 -m json.tool

echo "── Məlumat həddi yoxlaması ──"
curl -s "$A/tehsil/pasport/SER-2024-001/yoxla" | python3 -c "
import json,sys
d = json.load(sys.stdin)
for sahə in ('sahib', 'is_yeri', 'ata_adi'):
    print('  %-10s cavabda: %s' % (sahə, 'VAR ⚠️' if sahə in json.dumps(d) else 'yoxdur ✓'))
print()
print('  etibarlidir :', d['etibarlidir'])
print('  ad_soyad    :', d['ad_soyad'])
print('  hash        :', d['butovluk_hash'])
"

echo "── Olmayan nömrə → 404 ──"
printf '  HTTP %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/tehsil/pasport/XXX-0000-000/yoxla")"
)
