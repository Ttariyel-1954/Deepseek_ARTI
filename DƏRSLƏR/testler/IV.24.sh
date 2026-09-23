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

echo "── İştirakçı 3 ──"
curl -s "$A/tehsil/istirakciler/3/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  ad           :', d['sahib']['tam_ad'])
print('  pasport_no   :', d['pasport_no'], '← sənəddə nömrə VAR')
print('  etibarlidir  :', d['etibarlidir'], '← AMMA pasport ETİBARSIZDIR')
print('  uygunsuzluq  :', d['uygunsuzluq'])
s = d.get('sertifikasiya')
print('  sertifikasiya:', ('nəticə=' + str(s['netice']) + ' bal=' + str(s['bal'])) if s else 'yoxdur')
"

echo "── Etibarlı pasportla müqayisə (iştirakçı 1) ──"
curl -s "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  ad:', d['sahib']['tam_ad'], '| etibarlidir:', d['etibarlidir'], '| uygunsuzluq:', d['uygunsuzluq'])"
)
