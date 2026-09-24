#!/bin/bash
# YEKUN TESTLƏR — işlədici
#   bash testler/yoxla.sh IA       → Dərs 1A-nın 10 testi
#   bash testler/yoxla.sh IB       → Dərs 1B-nin 10 testi
#   bash testler/yoxla.sh IIA      → Dərs 2A-nın 10 testi
#   bash testler/yoxla.sh IIA.4    → yalnız bir test
#   bash testler/yoxla.sh --siyahi → testlərin siyahısı
cd "$(dirname "$0")" || exit 1
unset DATABASE_URL PGHOST
YASIL=$'\033[32m'; QIRMIZI=$'\033[31m'; MAVI=$'\033[36m'; SIFIR=$'\033[0m'
KECDI=0; XETA=0; ISLENDI=0

if [ "$1" = "--siyahi" ] || [ "$1" = "-s" ]; then
  echo "Mövcud testlər:"
  for f in $(ls [A-Z]*.sh 2>/dev/null | sort -t. -k1,1 -k2,2n); do
    printf '  %s\n' "${f%.sh}"
  done
  exit 0
fi

if [ -z "$1" ]; then
  FAYLLAR=$(ls [A-Z]*.sh 2>/dev/null | sort -t. -k1,1 -k2,2n); BASLIQ="BÜTÜN TESTLƏR"
elif [ -f "$1.sh" ]; then
  FAYLLAR="$1.sh"; BASLIQ="TEST $1"
elif ls "$1".*.sh >/dev/null 2>&1; then
  FAYLLAR=$(ls "$1".*.sh 2>/dev/null | sort -t. -k1,1 -k2,2n); BASLIQ="DƏRS $1"
else
  echo "⚠️ «$1» tapılmadı. Siyahı: bash testler/yoxla.sh --siyahi"; exit 1
fi

SAY=0; for f in $FAYLLAR; do SAY=$((SAY + 1)); done
printf "\n${MAVI}════════════════════════════════════════════════════════════════${SIFIR}\n"
printf "${MAVI}  %s — %d test${SIFIR}\n" "$BASLIQ" "$SAY"
printf "${MAVI}════════════════════════════════════════════════════════════════${SIFIR}\n"
for f in $FAYLLAR; do
  printf "\n${MAVI}── %s ──────────────────────────────────────────────────────${SIFIR}\n" "${f%.sh}"
  if bash "$f"; then
    printf "${YASIL}  ✓ %s KEÇDİ${SIFIR}\n" "${f%.sh}"; KECDI=$((KECDI + 1))
  else
    printf "${QIRMIZI}  ✗ %s UĞURSUZ${SIFIR}\n" "${f%.sh}"; XETA=$((XETA + 1))
  fi
  ISLENDI=$((ISLENDI + 1))
done
printf "\n${MAVI}════════════════════════════════════════════════════════════════${SIFIR}\n"
printf "  İŞLƏDİLDİ: %d   ${YASIL}KEÇDİ: %d${SIFIR}   ${QIRMIZI}UĞURSUZ: %d${SIFIR}\n" "$ISLENDI" "$KECDI" "$XETA"
[ "$XETA" -eq 0 ] && { printf "  ${YASIL}✓ HAMISI KEÇDİ${SIFIR}\n"; exit 0; }
printf "  ${QIRMIZI}✗ %d TEST UĞURSUZ${SIFIR}\n" "$XETA"; exit 1
