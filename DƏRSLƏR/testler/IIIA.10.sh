LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur: $(pwd)"; exit 1; }
[ -f .env ] || { echo "  ✗ .env yoxdur"; exit 1; }
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
[ -n "$DBURL" ] || { echo "  ✗ .env-də DATABASE_URL yoxdur"; exit 1; }
say() { psql "$DBURL" -At -c "$1" 2>/dev/null | tr -d ' '; }

temizle_kullanici() {
  psql "$DBURL" -At -c "DELETE FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%@arti.edu.az';" >/dev/null 2>&1
  true
}

trap temizle_kullanici EXIT INT TERM
XETA=0

echo "  → 1) Tip yoxlaması"
if npx tsc --noEmit; then echo "      ✓ təmiz (0 xəta)"; else echo "      ✗ tip xətası"; XETA=$((XETA+1)); fi

echo ""
echo "  → 2) 3A yoxlama alətləri (4 prob + 1 skript)"
for s in parol istifadeci token qoruyucu; do
  CIXIS=$(npx tsx "skriptler/${s}_yoxla.ts" 2>&1)
  N=$(printf '%s' "$CIXIS" | grep -oE 'keçdi: [0-9]+' | grep -oE '[0-9]+' | head -1)
  U=$(printf '%s' "$CIXIS" | grep -oE 'uğursuz: [0-9]+' | grep -oE '[0-9]+' | head -1)
  printf '      %-12s probu : keçdi=%s uğursuz=%s %s\n' "$s" "${N:-?}" "${U:-?}" \
    "$([ "${U:-1}" = "0" ] && echo '✓' || echo '✗')"
  [ "${U:-1}" = "0" ] || XETA=$((XETA+1))
done
printf '      %-12s skript: %s sətir\n' '3a_yoxla.sh' "$(wc -l < skriptler/3a_yoxla.sh | tr -d ' ')"

echo ""
echo "  → 3) 3A fayl sayı"
printf '      src/auth/     : %2s fayl, %4s sətir\n' \
  "$(find src/auth -name '*.ts' | wc -l | tr -d ' ')" \
  "$(cat $(find src/auth -name '*.ts') | wc -l | tr -d ' ')"
printf '      src/ cəmi     : %2s fayl, %4s sətir (generated xaric)\n' \
  "$(find src -name '*.ts' -not -path 'src/generated/*' | wc -l | tr -d ' ')" \
  "$(cat $(find src -name '*.ts' -not -path 'src/generated/*') | wc -l | tr -d ' ')"
printf '      skriptler/    : %2s fayl\n' "$(ls -1 skriptler/ | wc -l | tr -d ' ')"

echo ""
echo "  → 4) REQRESSİYA — köhnə alətlər hələ də işləyir"
for s in dto mapper servis statistika elaqeler toplu audit; do
  if [ -f "skriptler/${s}_yoxla.ts" ]; then
    CIXIS=$(npx tsx "skriptler/${s}_yoxla.ts" 2>&1)
    KOD=$?
    N=$(printf '%s' "$CIXIS" | grep -oE 'keçdi: [0-9]+' | grep -oE '[0-9]+' | head -1)
    U=$(printf '%s' "$CIXIS" | grep -oE 'uğursuz: [0-9]+' | grep -oE '[0-9]+' | head -1)
    if [ -n "$N" ]; then
      printf '      %-12s (2A/2B) : keçdi=%s uğursuz=%s %s\n' "$s" "$N" "${U:-?}" \
        "$([ "${U:-1}" = "0" ] && echo '✓' || echo '✗')"
      [ "${U:-1}" = "0" ] || XETA=$((XETA+1))
    else
      # ⚠️ Bəzi köhnə probelər «keçdi: N» formatında yazmır —
      #    onlar üçün ÇIXIŞ KODU yeganə obyektiv meyardır.
      printf '      %-12s (2A/2B) : exit=%s %s\n' "$s" "$KOD" \
        "$([ "$KOD" = "0" ] && echo '✓' || echo '✗')"
      [ "$KOD" = "0" ] || XETA=$((XETA+1))
    fi
  else
    printf '      %-12s (2A/2B) : fayl yoxdur\n' "$s"
  fi
done
for s in crud_yoxla.sh 2b_yoxla.sh; do
  if [ -f "skriptler/$s" ]; then
    if bash "skriptler/$s" >/tmp/iiia10_$s.log 2>&1; then
      printf '      %-12s (köhnə) : ✓ %s\n' "$s" \
        "$(grep -oE 'KEÇDİ: [0-9]+|keçdi: [0-9]+' /tmp/iiia10_$s.log | tail -1)"
    else
      printf '      %-12s (köhnə) : ✗ uğursuz\n' "$s"; XETA=$((XETA+1))
    fi
  fi
done

echo ""
echo "  → 5) Əvvəlki dərslərin modulları hələ də qoşuludur"
for m in PrismaModule SaglamliqModule EmekdaslarModule AuditModule AuthModule; do
  N=$(grep -c "$m" src/app.module.ts)
  [ "$N" -ge 1 ] && printf '      ✓ %s\n' "$m" || { printf '      ✗ %s YOXDUR\n' "$m"; XETA=$((XETA+1)); }
done
printf '      qlobal guard : %s (0 olmalıdır — 3B-də əlavə olunacaq)\n' \
  "$(grep -rn 'APP_GUARD' src/ 2>/dev/null | grep -vE ':\s*(//|\*|/\*)' | wc -l | tr -d ' ')"

echo ""
echo "  → 6) Bazanın son vəziyyəti"
CEDVEL=$(say "SELECT count(*) FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog','information_schema');")
SXEM=$(say "SELECT count(*) FROM information_schema.schemata WHERE schema_name NOT LIKE 'pg_%' AND schema_name <> 'information_schema';")
EMEK=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
IST=$(say "SELECT count(*) FROM kadrlar.istifadeciler;")
printf '      cədvəl + görünüş : %s\n' "$CEDVEL"
printf '      sxem             : %s\n' "$SXEM"
printf '      əməkdaş          : %s\n' "$EMEK"
printf '      istifadəçi       : %s (4 real + 0 test)\n' "$IST"
[ "$EMEK" = "14" ] || { echo "      ✗ əməkdaş sayı dəyişdi!"; XETA=$((XETA+1)); }
[ "$IST" -ge 4 ] || { echo "      ✗ istifadəçi sayı azaldı!"; XETA=$((XETA+1)); }
TESTQ=$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE email LIKE 'test.3a.%';")
[ "$TESTQ" = "0" ] || { echo "      ✗ bazada test istifadəçisi qalıb: $TESTQ"; XETA=$((XETA+1)); }

echo ""
echo "  → 7) Sirr gigiyenası (son yoxlama)"
grep -qE '^\.env$' .gitignore && echo "      ✓ .env git-ə yazılmır" || { echo "      ✗ .env .gitignore-da deyil"; XETA=$((XETA+1)); }
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  echo "      ✗ TƏHLÜKƏ: .env GIT-Ə İZLƏNİR!"; XETA=$((XETA+1))
else
  echo "      ✓ .env git tərəfindən izlənmir"
fi
SR=$(grep '^JWT_SECRET=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
printf '      JWT_SECRET uzunluğu : %s (>=32)\n' "${#SR}"
[ "${#SR}" -ge 32 ] || XETA=$((XETA+1))

echo ""
[ "$XETA" = "0" ] || { echo "  ✗ $XETA yoxlama uğursuz"; exit 1; }
echo "  ✓ IIIA.10 KEÇDİ — Dərs 3A tam təsdiqləndi, reqressiya təmizdir"
echo "  ✓ NÖVBƏTİ ADDIM: Dərs 3B (refresh token, httpOnly cookie, qlobal APP_GUARD)"
)
