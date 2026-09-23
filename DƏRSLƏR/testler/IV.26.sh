LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"
ID=""
temizle() { [ -n "$ID" ] && curl -s -o /dev/null -X DELETE "$A/tehsil/istirakciler/$ID" -H "$H"; }
trap temizle EXIT

echo "── 1) Qrupa yazılır ──"
ID=$(curl -s -X POST "$A/tehsil/istirakciler" -H "$H" -H 'Content-Type: application/json' \
  -d '{"qrup_id":1,"ad":"Pasport","soyad":"Yoxlamasi","ata_adi":"Test","is_yeri":"Test məktəbi"}' \
  | python3 -c "
import json,sys; d=json.load(sys.stdin); print(d['id'])")
curl -s "$A/tehsil/istirakciler/$ID/pasport" -H "$H" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  id           :', d['sahib']['id'])
print('  status       :', d['sahib']['status'], '← hələ bitirməyib')
print('  pasport_no   :', d['pasport_no'], '← hələ YOXDUR')
print('  etibarlidir  :', d['etibarlidir'])
print('  səbəb        :', d['uygunsuzluq'])
"

echo "── 2) İmtahan balı ilə müraciət (bal = 72) ──"
curl -s -X POST "$A/tehsil/istirakciler/$ID/pasport" -H "$H" -H 'Content-Type: application/json' \
  -d '{"bal":72,"imtahan_tarixi":"2026-09-20","tip":"müəllim"}' | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  melumat      :', d['melumat'])
print('  pasport_no   :', d['pasport_no'])
print('  etibarlidir  :', d['etibarlidir'])
print('  netice       :', d['sertifikasiya']['netice'])
print('  hash         :', d['butovluk']['hash'])
"

echo "── 3) Nömrə bazada hara yazıldı? ──"
NO=$(curl -s "$A/tehsil/istirakciler/$ID/pasport" -H "$H" | python3 -c "
import json,sys; print(json.load(sys.stdin)['pasport_no'])")
psql -U arti_user -d arti_baza -c "
  SELECT 'telim_istirakcilari' AS cedvel, sertifikat_no, status
  FROM tehsil.telim_istirakcilari WHERE id = $ID
  UNION ALL
  SELECT 'sertifikasiya', sertifikat_no, netice
  FROM tehsil.sertifikasiya WHERE sertifikat_no = '$NO'" | sed 's/^/  /'
)
