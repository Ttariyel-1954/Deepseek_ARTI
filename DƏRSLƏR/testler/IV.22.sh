LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── GET /tehsil/istirakciler/1/pasport ──"
curl -s "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  pasport_no  :', d['pasport_no'])
print('  etibarlidir :', d['etibarlidir'])
print()
print('  SAHİB       :', d['sahib']['tam_ad'], '| ata adı:', d['sahib']['ata_adi'])
print('  İŞ YERİ     :', d['sahib']['is_yeri'])
print('  TƏLİM       :', d['telim']['proqram'])
print('                qrup:', d['telim']['qrup'], '| saat:', d['telim']['saat'])
print('                müddət:', d['telim']['baslama_tarixi'], '→', d['telim']['bitme_tarixi'])
print('  SERTİFİKASİYA: nəticə', d['sertifikasiya']['netice'], '| bal', d['sertifikasiya']['bal'])
print('                imtahan:', d['sertifikasiya']['imtahan_tarixi'], '| tip:', d['sertifikasiya']['tip'])
"

echo "── Dörd rol oxuya bilir? ──"
for rol in admin muhendis maliyyeci baxici; do
  RT=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  printf '  %-10s → %s\n' "$rol" "$(curl -s -o /dev/null -w '%{http_code}' "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $RT")"
done
)
