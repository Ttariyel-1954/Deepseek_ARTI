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
  -d '{"qrup_id":1,"ad":"Idempotent","soyad":"Yoxlama","ata_adi":"Test"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")

echo "── 1-ci müraciət (bal 70) ──"
NO1=$(curl -s -X POST "$A/tehsil/istirakciler/$ID/pasport" -H "$H" \
  -H 'Content-Type: application/json' -d '{"bal":70}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['pasport_no'])")
echo "  nömrə: $NO1"

echo "── 2-ci müraciət (bal 95) ──"
CVB=$(curl -s -X POST "$A/tehsil/istirakciler/$ID/pasport" -H "$H" \
  -H 'Content-Type: application/json' -d '{"bal":95}')
NO2=$(printf '%s' "$CVB" | python3 -c "import json,sys; print(json.load(sys.stdin)['pasport_no'])")
printf '%s' "$CVB" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  nömrə:', d['pasport_no']); print('  melumat:', d['melumat'])"

echo "── 3-cü müraciət (bal 30) ──"
NO3=$(curl -s -X POST "$A/tehsil/istirakciler/$ID/pasport" -H "$H" \
  -H 'Content-Type: application/json' -d '{"bal":30}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['pasport_no'])")
echo "  nömrə: $NO3"

echo "── Yoxlama ──"
echo "  üç müraciətdə eyni nömrə : $([ "$NO1" = "$NO2" ] && [ "$NO2" = "$NO3" ] && echo '✓ BƏLİ' || echo '✗ XEYR')"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  bazada bu nömrədən neçə sətir: ' || count(*)
  FROM tehsil.sertifikasiya WHERE sertifikat_no = '$NO1'"
)
