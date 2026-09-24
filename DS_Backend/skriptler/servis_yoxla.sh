#!/bin/bash
# ────────────────────────────────────────────────────────────────────
#  servis_yoxla.sh — serveri qaldırır, CANLI yoxlayır, söndürür.
#
#  İSTİFADƏ:
#     bash skriptler/servis_yoxla.sh            # port 4000 (standart)
#     PORT=4100 bash skriptler/servis_yoxla.sh  # başqa port
#
#  NƏ EDİR:
#     1. dist/main.js varmı — yoxlayır.
#     2. Portun boş olduğunu yoxlayır (məşğuldursa kim tutduğunu göstərir).
#     3. `node dist/main.js`-i ARXA PLANDA qaldırır, loqu fayla yazır.
#     4. Cavab verənə qədər gözləyir (maksimum 30 saniyə).
#     5. Üç yolu yoxlayır: /api/v1/saglamliq, /docs, /saglamliq.
#     6. Serveri MÜTLƏQ söndürür (trap) — terminalda asılı proses qalmır.
#
#  ⚠️ NİYƏ `trap`: skript hansı səbəbdən dayansa da (xəta, Ctrl+C,
#     normal son) server söndürülməlidir. `trap ... EXIT` bunu təmin edir.
# ────────────────────────────────────────────────────────────────────
set -u
cd "$(dirname "$0")/.." || exit 1

PORT="${PORT:-4000}"
LOQ="/tmp/arti_server_${PORT}.log"
CAVAB="/tmp/arti_cavab_${PORT}.json"
PID=""

temizle() {
  if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
    kill "$PID" 2>/dev/null
    wait "$PID" 2>/dev/null
    printf '  ✓ Server söndürüldü (PID %s) — port boşaldıldı\n' "$PID"
  fi
}
trap temizle EXIT INT TERM

printf '════════ SERVERİN CANLI YOXLAMASI (port %s) ════════\n' "$PORT"

# 1 ── build varmı?
if [ ! -f dist/main.js ]; then
  printf '  ✗ dist/main.js yoxdur. Əvvəlcə bunu işlədin:\n'
  printf '      npm run build\n'
  exit 1
fi
printf '  ✓ dist/main.js yerindədir\n'

# 2 ── port boşdurmu?
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  printf '  ✗ %s portu MƏŞĞULDUR. Onu tutan proses:\n' "$PORT"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | sed 's/^/      /'
  printf '      Həll: kill <PID>   (və ya başqa port: PORT=4100 ...)\n'
  exit 1
fi
printf '  ✓ %s portu boşdur\n' "$PORT"

# 3 ── serveri arxa planda qaldır
PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
printf '  → server qaldırıldı (PID %s) — loq: %s\n' "$PID" "$LOQ"

# 4 ── hazır olana qədər gözlə
hazir=0
cehd=0
while [ "$cehd" -lt 60 ]; do
  cehd=$((cehd + 1))
  if curl -fsS "http://localhost:$PORT/api/v1/saglamliq" -o "$CAVAB" 2>/dev/null; then
    hazir=1
    break
  fi
  if ! kill -0 "$PID" 2>/dev/null; then
    break
  fi
  sleep 0.5
done

if [ "$hazir" != "1" ]; then
  printf '  ✗ Server cavab vermədi. Loqun sonu:\n'
  tail -n 20 "$LOQ" | sed 's/^/      /'
  exit 1
fi
printf '  ✓ Server hazırdır (%s cəhddən sonra)\n' "$cehd"

# 5 ── yolları yoxla
kod() { curl -s -o /dev/null -w '%{http_code}' "$1"; }
S1=$(kod "http://localhost:$PORT/api/v1/saglamliq")
S2=$(kod "http://localhost:$PORT/docs")
S3=$(kod "http://localhost:$PORT/saglamliq")

printf '  /api/v1/saglamliq → %s\n' "$S1"
printf '  /docs             → %s\n' "$S2"
printf '  /saglamliq        → %s   (prefiks olmadan — 404 gözlənilir)\n' "$S3"
printf '  Cavab gövdəsi: %s\n' "$(cat "$CAVAB")"

if [ "$S1" != "200" ]; then
  printf '  ✗ Sağlamlıq 200 qaytarmadı!\n'
  exit 1
fi
if [ "$S3" != "404" ]; then
  printf '  ✗ Prefiks işləmədi — /saglamliq 404 olmalı idi.\n'
  exit 1
fi
printf '════════ BÜTÜN CANLI YOXLAMALAR KEÇDİ ════════\n'
