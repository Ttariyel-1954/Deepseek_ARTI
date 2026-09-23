LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── Tokensiz GET sorğuları (hamısı 401 olmalıdır) ──"
for yol in /struktur/merkezler /struktur/merkezler/1 /struktur/merkezler/statistika \
           /kadrlar/emekdaslar /kadrlar/emekdaslar/1 /kadrlar/emekdaslar/icmal \
           /auth/profil /auth/istifadeciler; do
  printf '  %-34s → %s\n' "$yol" "$(curl -s -o /dev/null -w '%{http_code}' "$A$yol")"
done

echo "── Birinin cavabı ──"
curl -s "$A/struktur/merkezler" | python3 -m json.tool
)
