#!/bin/bash
# ══════════════════════════════════════════════════════════════════════
#  Deepseek_ARTI — VƏZİYYƏT YOXLAMASI
#
#  İSTİFADƏ:
#    ./yoxla.sh              bütün hesabat
#    ./yoxla.sh baza         yalnız baza
#    ./yoxla.sh backend      yalnız backend
#    ./yoxla.sh dersler      yalnız dərslər
#    ./yoxla.sh git          yalnız git
#    ./yoxla.sh test         testləri də işlət
#
#  Çıxış kodu: 0 — hər şey qaydasındadır · 1 — ən azı bir problem var
# ══════════════════════════════════════════════════════════════════════

cd "$(dirname "$0")" || exit 1
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"

BAZA="${BAZA:-arti_baza}"
DB_ISTIFADECI="${DB_ISTIFADECI:-arti_user}"
API="${API:-http://localhost:4000/api/v1}"

YASIL=$'\033[32m'; QIRMIZI=$'\033[31m'; SARI=$'\033[33m'
MAVI=$'\033[36m';  BOZ=$'\033[90m';     SIFIR=$'\033[0m'

PROBLEM=0

# ── KÖMƏKÇİLƏR ────────────────────────────────────────────────────────
basliq() {
  printf "\n${MAVI}════════════════════════════════════════════════════════════${SIFIR}\n"
  printf "${MAVI}  %s${SIFIR}\n" "$1"
  printf "${MAVI}════════════════════════════════════════════════════════════${SIFIR}\n"
}

pad() {   # pad "mətn" genişlik — Azərbaycan hərfləri sütunu sürüşdürməsin
  local metn="$1" en="$2" uzunluq=${#1} i
  printf '%s' "$metn"
  i=$((en - uzunluq))
  while [ "$i" -gt 0 ]; do printf ' '; i=$((i - 1)); done
}

setir() {   # setir "ad" "dəyər" [gözlənilən]
  local reng="$YASIL"
  if [ -n "${3:-}" ] && [ "$2" != "$3" ]; then
    reng="$QIRMIZI"; PROBLEM=$((PROBLEM + 1))
  fi
  printf "  %s${reng}%s${SIFIR}" "$(pad "$1" 26)" "$2"
  [ -n "${3:-}" ] && printf " ${BOZ}(gözlənilən: %s)${SIFIR}" "$3"
  printf "\n"
}

setir_boz() { printf "  %s${BOZ}%s${SIFIR}\n" "$(pad "$1" 26)" "$2"; }

# ── 1) QOVLUQLAR ──────────────────────────────────────────────────────
qovluqlar() {
  basliq "1 · QOVLUQLAR"
  for d in DS_Baza DS_Backend DƏRSLƏR _hesabat _arxiV; do
    if [ -d "$d" ]; then
      local n
      n=$(find "$d" -type f \
            -not -path '*/node_modules/*' -not -path '*/dist/*' \
            -not -path '*/src/generated/*' -not -path '*/.git/*' 2>/dev/null \
          | wc -l | tr -d ' ')
      printf "  %s${YASIL}✓${SIFIR} %s fayl\n" "$(pad "$d" 14)" "$n"
    else
      printf "  %s${QIRMIZI}✗ YOXDUR${SIFIR}\n" "$(pad "$d" 14)"
      PROBLEM=$((PROBLEM + 1))
    fi
  done
}

# ── 2) BAZA ───────────────────────────────────────────────────────────
baza() {
  basliq "2 · BAZA"

  if ! pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
    printf "  ${QIRMIZI}✗ PostgreSQL 5432 portunda cavab vermir${SIFIR}\n"
    PROBLEM=$((PROBLEM + 1))
    return
  fi
  setir "PostgreSQL 5432" "işləyir"

  local P="psql -U $DB_ISTIFADECI -w -d $BAZA -tAc"
  local n

  n=$($P "SELECT count(*)::int FROM information_schema.schemata
           WHERE schema_name NOT IN ('pg_catalog','information_schema','public')" 2>/dev/null || echo 0)
  setir "sxem" "$n" "12"

  n=$($P "SELECT count(*)::int FROM information_schema.tables
           WHERE table_type='BASE TABLE'
             AND table_schema NOT IN ('pg_catalog','information_schema')" 2>/dev/null || echo 0)
  setir "cədvəl" "$n" "48"

  n=$($P "SELECT count(*)::int FROM information_schema.views
           WHERE table_schema NOT IN ('pg_catalog','information_schema')" 2>/dev/null || echo 0)
  setir "view" "$n" "8"

  n=$($P "SELECT count(*)::int FROM information_schema.routines
           WHERE routine_schema NOT IN ('pg_catalog','information_schema')" 2>/dev/null || echo 0)
  setir "funksiya" "$n" "10"

  n=$($P "SELECT count(*)::int FROM information_schema.triggers
           WHERE trigger_schema NOT IN ('pg_catalog','information_schema')" 2>/dev/null || echo 0)
  setir "trigger" "$n" "14"

  n=$($P "SELECT count(*)::int FROM information_schema.table_constraints
           WHERE constraint_type='FOREIGN KEY'
             AND table_schema NOT IN ('pg_catalog','information_schema')" 2>/dev/null || echo 0)
  setir "xarici açar (FK)" "$n" "35"

  printf "\n  ${SARI}▸ Əsas cədvəllərdəki sətirlər${SIFIR}\n"
  for c in struktur.merkezler struktur.shobeler struktur.rehberlik \
           kadrlar.emekdaslar kadrlar.istifadeciler; do
    n=$($P "SELECT count(*)::int FROM $c" 2>/dev/null || echo "?")
    printf "    %s${BOZ}%s${SIFIR}\n" "$(pad "$c" 24)" "$n"
  done
}

# ── 3) BACKEND ────────────────────────────────────────────────────────
backend() {
  basliq "3 · BACKEND"

  if [ ! -d DS_Backend ]; then
    printf "  ${QIRMIZI}✗ DS_Backend/ yoxdur${SIFIR}\n"; PROBLEM=$((PROBLEM + 1)); return
  fi

  setir_boz "mənbə faylları (.ts)" \
    "$(find DS_Backend/src -name '*.ts' -not -path '*/generated/*' 2>/dev/null | wc -l | tr -d ' ')"

  [ -d DS_Backend/node_modules ] \
    && setir "npm install" "olunub" \
    || { setir "npm install" "OLUNMAYIB" "olunub"
         printf "    ${BOZ}→ cd DS_Backend && npm install${SIFIR}\n"; }

  [ -f DS_Backend/src/generated/prisma/client.ts ] \
    && setir "Prisma müştərisi" "yaradılıb" \
    || { setir "Prisma müştərisi" "YARADILMAYIB" "yaradılıb"
         printf "    ${BOZ}→ cd DS_Backend && npx prisma generate${SIFIR}\n"; }

  [ -f DS_Backend/.env ] \
    && setir ".env" "var" \
    || { setir ".env" "YOXDUR" "var"
         printf "    ${BOZ}→ cp DS_Backend/.env.example DS_Backend/.env${SIFIR}\n"; }

  [ -f DS_Backend/dist/main.js ] \
    && setir "dist/main.js" "var" \
    || setir_boz "dist/main.js" "yoxdur (npm run build)"

  printf "\n${SARI}  ▸ Server canlıdırmı?${SIFIR} ${BOZ}%s${SIFIR}\n" "$API"
  local kod
  kod=$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 "$API/saglamliq" 2>/dev/null)
  if [ "$kod" = "200" ]; then
    printf "    ${YASIL}✓${SIFIR} işləyir\n"
    curl -s --max-time 3 "$API/saglamliq" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin); b = d.get('baza', {})
    print('      status: %s · cədvəl: %s · gecikmə: %s ms'
          % (d.get('status'), b.get('cedvel_sayi'), b.get('gecikme_ms')))
except Exception:
    pass" 2>/dev/null
  else
    printf "    ${SARI}●${SIFIR} işləmir ${BOZ}(npm run start:dev)${SIFIR}\n"
  fi
}

# ── 4) DƏRSLƏR ────────────────────────────────────────────────────────
dersler() {
  basliq "4 · DƏRSLƏR"
  local var=0
  for f in DƏRSLƏR/*.html; do
    [ -e "$f" ] || continue
    var=$((var + 1))
    printf "  %-28s ${YASIL}%s sətir${SIFIR}\n" "$(basename "$f")" "$(wc -l < "$f" | tr -d ' ')"
  done
  [ "$var" -eq 0 ] && { printf "  ${QIRMIZI}✗ heç bir dərs yoxdur${SIFIR}\n"; PROBLEM=$((PROBLEM + 1)); }

  printf "\n  ${SARI}▸ Generatorlar${SIFIR}\n"
  for g in DS_Baza/ders_yarat.py DS_Backend/ds1_yarat.py; do
    [ -f "$g" ] \
      && printf "    ${YASIL}✓${SIFIR} %s\n" "$g" \
      || { printf "    ${QIRMIZI}✗${SIFIR} %s YOXDUR\n" "$g"; PROBLEM=$((PROBLEM + 1)); }
  done

  printf "\n  ${SARI}▸ Generatorların işlətdiyi girişlər${SIFIR}\n"
  for g in _hesabat/sorgu_cixis.txt DS_Baza/ders.css; do
    [ -f "$g" ] \
      && printf "    ${YASIL}✓${SIFIR} %s\n" "$g" \
      || { printf "    ${QIRMIZI}✗${SIFIR} %s YOXDUR\n" "$g"; PROBLEM=$((PROBLEM + 1)); }
  done
}

# ── 5) GİT ────────────────────────────────────────────────────────────
git_yoxla() {
  basliq "5 · GİT"
  [ -d .git ] || { printf "  ${QIRMIZI}✗ .git yoxdur${SIFIR}\n"; PROBLEM=$((PROBLEM + 1)); return; }

  local budaq say cirkli
  budaq=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  setir "budaq" "$budaq" "main"

  cirkli=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  if [ "$cirkli" -eq 0 ]; then
    setir "işçi qovluq" "təmiz"
  else
    setir "işçi qovluq" "$cirkli dəyişiklik" "təmiz"
  fi

  say=$(git log --oneline 2>/dev/null | wc -l | tr -d ' ')
  setir_boz "commit sayı" "$say"

  local yerli uzaq
  yerli=$(git rev-parse HEAD 2>/dev/null | cut -c1-7)
  uzaq=$(git rev-parse origin/main 2>/dev/null | cut -c1-7)
  if [ "$yerli" = "$uzaq" ]; then
    setir "GitHub ilə sinxron" "bəli ($yerli)"
  else
    setir "GitHub ilə sinxron" "XEYR ($yerli/$uzaq)" "bəli"
    printf "    ${BOZ}→ git push origin main${SIFIR}\n"
  fi

  if [ "$(git config core.hooksPath 2>/dev/null)" = ".githooks" ]; then
    setir "gizli məlumat qoruyucusu" "qurulub"
  else
    setir "gizli məlumat qoruyucusu" "QURULMAYIB" "qurulub"
    printf "    ${BOZ}→ git config core.hooksPath .githooks${SIFIR}\n"
  fi

  printf "\n  ${SARI}▸ Son 3 commit${SIFIR}\n"
  git log --oneline -3 2>/dev/null | while read -r s; do
    printf "    ${BOZ}%s${SIFIR}\n" "$s"
  done
}

# ── 6) TESTLƏR ────────────────────────────────────────────────────────
testler() {
  basliq "6 · TESTLƏR"
  cd DS_Backend 2>/dev/null || { printf "  ${QIRMIZI}✗ DS_Backend/ yoxdur${SIFIR}\n"; return; }

  if [ ! -d node_modules ]; then
    printf "  ${SARI}⚠ node_modules yoxdur — npm install lazımdır${SIFIR}\n"; cd ..; return
  fi

  local u x
  printf "  ${SARI}▸ Unit testlər${SIFIR}\n"
  u=$(NO_COLOR=1 npm test 2>&1 | sed $'s/\033\\[[0-9;]*m//g' \
        | grep -E '^[[:space:]]*Tests[[:space:]]' | head -1 | sed 's/^ *//')
  if [ -n "$u" ]; then printf "    ${YASIL}✓${SIFIR} %s\n" "$u"
  else printf "    ${QIRMIZI}✗ xəta verdi${SIFIR}\n"; PROBLEM=$((PROBLEM + 1)); fi

  printf "  ${SARI}▸ e2e testlər${SIFIR}\n"
  x=$(NO_COLOR=1 npx vitest run --config vitest.config.e2e.ts 2>&1 \
        | sed $'s/\033\\[[0-9;]*m//g' | grep -E '^[[:space:]]*Tests[[:space:]]' \
        | head -1 | sed 's/^ *//')
  if [ -n "$x" ]; then printf "    ${YASIL}✓${SIFIR} %s\n" "$x"
  else printf "    ${QIRMIZI}✗ xəta verdi${SIFIR}\n"; PROBLEM=$((PROBLEM + 1)); fi

  cd ..
}

# ── GİRİŞ ─────────────────────────────────────────────────────────────
basliq "DEEPSEEK_ARTI — VƏZİYYƏT"
printf "  ${BOZ}tarix: %s · qovluq: %s${SIFIR}\n" "$(date '+%Y-%m-%d %H:%M')" "$(pwd)"

case "${1:-hamisi}" in
  hamisi|"")            qovluqlar; baza; backend; dersler; git_yoxla ;;
  baza)                 baza ;;
  backend)              backend ;;
  dersler|dərslər)      dersler ;;
  git)                  git_yoxla ;;
  test|testler|testlər) testler ;;
  *)
    printf "\n${SARI}İSTİFADƏ:${SIFIR} %s [hamisi|baza|backend|dersler|git|test]\n\n" "$0"
    exit 0
    ;;
esac

# ── NƏTİCƏ ────────────────────────────────────────────────────────────
basliq "NƏTİCƏ"
if [ "$PROBLEM" -eq 0 ]; then
  printf "  ${YASIL}✅ Hər şey qaydasındadır${SIFIR}\n\n"
  exit 0
else
  printf "  ${QIRMIZI}❌ %s problem tapıldı${SIFIR}\n\n" "$PROBLEM"
  exit 1
fi
