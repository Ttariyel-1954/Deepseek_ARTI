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

ID=$(curl -s -X POST "$A/tehsil/istirakciler" -H "$H" -H 'Content-Type: application/json' \
  -d '{"qrup_id":1,"ad":"Kesilen","soyad":"Namized","ata_adi":"Test"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")

for bal in 40 60 100; do
  echo "── bal = $bal ──"
  curl -s -X POST "$A/tehsil/istirakciler/$ID/pasport" -H "$H" \
    -H 'Content-Type: application/json' -d "{\"bal\":$bal}" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  nəticə     :', d['sertifikasiya']['netice'])
print('  pasport_no :', d['pasport_no'])
print('  etibarlidir:', d['etibarlidir'])
print('  melumat    :', d['melumat'])
"
  # Növbəti bal üçün pasportu sıfırlayırıq
  psql -U arti_user -d arti_baza -q -c "
    DELETE FROM tehsil.sertifikasiya WHERE ad_soyad = 'Kesilen Namized';
    UPDATE tehsil.telim_istirakcilari SET sertifikat_no = NULL
     WHERE id = $ID"
done
)
