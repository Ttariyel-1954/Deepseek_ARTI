#!/bin/bash
# ══════════════════════════════════════════════════════════════
#  Ehtiyat nusxe (backup) — pg_dump + sıxılmış arxiv + kohne temizleme
#
#  Istifade:  bash scripts/ehtiyat.sh
#  Cron:      0 2 * * * cd ~/Deepseek_ARTI/DS_Backend && bash scripts/ehtiyat.sh
# ══════════════════════════════════════════════════════════════
set -e

unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"

BAZA="${BAZA:-arti_baza}"
ISTIFADECI="${ISTIFADECI:-arti_user}"
QOVLUQ="${QOVLUQ:-$HOME/Deepseek_ARTI/_arxiV/ehtiyat}"
SAXLAMA_GUN="${SAXLAMA_GUN:-30}"

mkdir -p "$QOVLUQ"
VAXT=$(date +%Y%m%d_%H%M%S)
FAYL="$QOVLUQ/${BAZA}_${VAXT}.sql.gz"

echo "════ Ehtiyat nusxe ════"
echo "  Baza  : $BAZA"
echo "  Hedef : $FAYL"

# 1) Dump + sixma
pg_dump -U "$ISTIFADECI" -d "$BAZA" --no-owner --no-privileges | gzip > "$FAYL"

OLCU=$(du -h "$FAYL" | cut -f1)
echo "  Olcu  : $OLCU"

# 2) Yoxla — fayl bos deyil?
if [ ! -s "$FAYL" ]; then
  echo "  XETA: ehtiyat faylı BOSDUR!"
  exit 1
fi

# 3) Yoxla — bərpa oluna bilermi? (strukturu say)
# QEYD: macOS-un zcat-i BSD versiyasidir ve .Z fayl gozleyir.
#       gunzip -c HER platformada isleyir.
SETIR=$(gunzip -c "$FAYL" | grep -c 'CREATE TABLE' || true)
echo "  CREATE TABLE: $SETIR"
if [ "$SETIR" -lt 40 ]; then
  echo "  XEBERDARLIQ: gozlenilenden az cedvel ($SETIR < 40)"
fi

# 4) Kohne ehtiyatlari temizle
SILINEN=$(find "$QOVLUQ" -name "${BAZA}_*.sql.gz" -mtime "+$SAXLAMA_GUN" | wc -l | tr -d ' ')
find "$QOVLUQ" -name "${BAZA}_*.sql.gz" -mtime "+$SAXLAMA_GUN" -delete
echo "  Silinen kohne: $SILINEN (${SAXLAMA_GUN} gunden kohne)"

# 5) İcmal
CEMI=$(find "$QOVLUQ" -name "${BAZA}_*.sql.gz" | wc -l | tr -d ' ')
UMUMI=$(du -sh "$QOVLUQ" | cut -f1)
echo "  Arxivde: $CEMI fayl, $UMUMI"
echo "════ HAZIR ════"
