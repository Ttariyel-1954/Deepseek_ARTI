LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
export npm_config_cache=/tmp/npmcache

say() {
  echo "  istifadəçi: $(psql -U arti_user -d arti_baza -tA -c 'SELECT count(*) FROM kadrlar.istifadeciler' | tr -d ' ')  |  bcrypt hash-li: $(psql -U arti_user -d arti_baza -tA -c "SELECT count(*) FROM kadrlar.istifadeciler WHERE parol_hash LIKE '\$2%'" | tr -d ' ')"
}

echo "── Əvvəl ──"; say

echo "── 1-ci işə salma ──"
npm run seed:auth 2>&1 | tail -3 | sed 's/^/  /'
say

echo "── 2-ci işə salma (idempotent olmalıdır) ──"
npm run seed:auth 2>&1 | tail -3 | sed 's/^/  /'
say

echo "── Rollar üzrə ──"
psql -U arti_user -d arti_baza -c "
  SELECT rol, count(*) AS sayi FROM kadrlar.istifadeciler GROUP BY rol ORDER BY rol" | sed 's/^/  /'

echo "── Seed skriptində idempotentlik ──"
grep -nE 'upsert|ON CONFLICT|update:|create:' scripts/seed-auth.ts | head -6 | sed 's/^/  /'
)
