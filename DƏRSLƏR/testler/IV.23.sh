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

H1=$(curl -s "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; print(json.load(sys.stdin)['butovluk']['hash'])")
H2=$(curl -s "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; print(json.load(sys.stdin)['butovluk']['hash'])")
H3=$(curl -s "$A/tehsil/istirakciler/2/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; print(json.load(sys.stdin)['butovluk']['hash'])")

echo "  iştirakçı 1 → hash: $H1"
echo "  iştirakçı 1 → hash: $H2   (təkrar çağırış)"
echo "  iştirakçı 2 → hash: $H3   (başqa şəxs)"
echo
echo "  deterministik (H1 = H2)      : $([ "$H1" = "$H2" ] && echo '✓ BƏLİ' || echo '✗ XEYR')"
echo "  fərqli şəxs fərqli hash      : $([ "$H1" != "$H3" ] && echo '✓ BƏLİ' || echo '✗ XEYR')"
echo
echo "── Hash hansı sahələrdən hesablanır? ──"
curl -s "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; d=json.load(sys.stdin)['butovluk']
print('  alqoritm:', d['alqoritm'])
print('  sahələr :', ', '.join(d['saheler']))
"
)
