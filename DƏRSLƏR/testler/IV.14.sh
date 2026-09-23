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
H="Authorization: Bearer $T"

UZUN=$(python3 -c "print('a' * 501)")

yoxla() {
  printf '  %-30s → %s\n' "$1" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/ai/sual" -H "$H" \
        -H 'Content-Type: application/json' -d "$2")"
}

yoxla "düzgün sual"          '{"sual":"Neçə əməkdaş var?"}'
yoxla "2 simvol"             '{"sual":"ab"}'
yoxla "boş sual"             '{"sual":""}'
yoxla "sual sahəsi yoxdur"   '{}'
yoxla "501 simvol"           "{\"sual\":\"$UZUN\"}"

echo "── DTO-da qaydalar ──"
grep -n 'MinLength\|MaxLength\|IsString' src/ai/dto/sual.dto.ts | sed 's/^/  /'
)
