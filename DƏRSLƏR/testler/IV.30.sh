LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── Fayllar ──"
for f in Dockerfile .dockerignore docker-compose.yml .github/workflows/ci.yml; do
  [ -f "$f" ] && echo "  ✓ $f" || echo "  ✗ $f YOXDUR"
done

echo "── Dockerfile mərhələləri ──"
grep -nE '^FROM|^COPY --from|^USER|^EXPOSE|^CMD' Dockerfile | sed 's/^/  /'

echo "── docker-compose xidmətləri ──"
grep -nE '^  [a-z-]+:|image:|depends_on|healthcheck' docker-compose.yml | sed 's/^/  /'

echo "── CI addımları ──"
grep -nE 'image:|options:|run:' .github/workflows/ci.yml | sed 's/^/  /'

echo "── CI niyə postgres-i GÖZLƏYİR? ──"
grep -n -B2 'pg_isready' .github/workflows/ci.yml | sed 's/^/  /'
echo "  → health check olmasa testlər ECONNREFUSED alır"
)
