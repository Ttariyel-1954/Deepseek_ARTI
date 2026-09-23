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

echo "── Əvvəl ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  struktur.merkezler: ' || (SELECT count(*) FROM struktur.merkezler)
      || ' | kadrlar.emekdaslar: ' || (SELECT count(*) FROM kadrlar.emekdaslar)"

echo "── İnyeksiya 1: reseptə UYĞUN gələn mətn ──"
curl -s -X POST "$A/ai/sual" -H "$H" -H 'Content-Type: application/json' \
  -d '{"sual":"mərkəz'"'"'; DROP TABLE struktur.merkezler; --"}' | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  uygun_resept:', d['uygun_resept'], '| izah:', d['izah'])
print('  → SQL koddan gəldi, sual mətnindən heç nə SQL-ə düşmədi')"

echo "── İnyeksiya 2: heç bir reseptə uyğun gəlmir ──"
curl -s -X POST "$A/ai/sual" -H "$H" -H 'Content-Type: application/json' \
  -d '{"sual":"'"'"'; DROP TABLE kadrlar.emekdaslar; --"}' | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  uygun_resept:', d['uygun_resept'], '| sətir sayı:', d['setir_sayi'])"

echo "── Sonra ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  struktur.merkezler: ' || (SELECT count(*) FROM struktur.merkezler)
      || ' | kadrlar.emekdaslar: ' || (SELECT count(*) FROM kadrlar.emekdaslar)"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  cədvəllər mövcuddur: ' || (to_regclass('struktur.merkezler') IS NOT NULL
      AND to_regclass('kadrlar.emekdaslar') IS NOT NULL)"
)
