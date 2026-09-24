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

echo "  → 1) Bazanın başlanğıc vəziyyəti"
EVVEL=$(say "SELECT count(*) FROM kadrlar.istifadeciler;")
printf '      istifadəçi sayı     : %s\n' "$EVVEL"
printf '      rollar üzrə         : %s\n' \
  "$(psql "$DBURL" -At -F'=' -c "SELECT rol, count(*) FROM kadrlar.istifadeciler GROUP BY rol ORDER BY rol;" 2>/dev/null | tr '\n' ' ')"
[ "$EVVEL" -ge 4 ] || { echo "  ✗ istifadəçi sayı gözləniləndən azdır"; exit 1; }

echo ""
echo "  → 2) Hash formatı — heç bir açıq parol olmamalıdır"
ACIQ=$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE parol_hash NOT LIKE '\$2%';")
printf '      bcrypt formatında olmayan hash : %s (0 olmalıdır)\n' "$ACIQ"
[ "$ACIQ" = "0" ] || { echo "  ✗ bcrypt olmayan hash var!"; exit 1; }
QISA=$(say "SELECT count(*) FROM kadrlar.istifadeciler WHERE length(parol_hash) < 50;")
printf '      çox qısa hash (<50 simvol)     : %s (0 olmalıdır)\n' "$QISA"
[ "$QISA" = "0" ] || { echo "  ✗ şübhəli qısa hash var!"; exit 1; }
printf '      hash uzunluğu (nümunə)         : %s simvol\n' \
  "$(say "SELECT length(parol_hash) FROM kadrlar.istifadeciler ORDER BY id LIMIT 1;")"
printf '      eyni hash-li istifadəçi sayı   : %s\n' \
  "$(say "SELECT count(*) FROM (SELECT parol_hash FROM kadrlar.istifadeciler GROUP BY parol_hash HAVING count(*) > 1) t;")"

echo ""
echo "  → 3) istifadeci_yoxla.ts — canlı prob (37 yoxlama)"
NETICE=$(npx tsx skriptler/istifadeci_yoxla.ts 2>&1)
printf '%s\n' "$NETICE" | tail -n 4 | awk '{ print "      " $0 }'
KECDI=$(printf '%s' "$NETICE" | grep -oE 'keçdi: [0-9]+' | grep -oE '[0-9]+' | head -1)
UGURSUZ=$(printf '%s' "$NETICE" | grep -oE 'uğursuz: [0-9]+' | grep -oE '[0-9]+' | head -1)
printf '      keçdi=%s uğursuz=%s\n' "${KECDI:-?}" "${UGURSUZ:-?}"
[ "${KECDI:-0}" -ge 37 ] && [ "${UGURSUZ:-1}" = "0" ] \
  || { echo "  ✗ istifadəçi servisi probu uğursuz"; exit 1; }

echo ""
echo "  → 4) Hash sızması — cavabda parol_hash OLMAMALIDIR"
if printf '%s' "$NETICE" | grep -q 'parol_hash'; then
  # ⚠️ Probun özü hash-in olmadığını YOXLAYIR — söz keçməsi normaldır,
  #    ona görə yalnız «TƏHLÜKƏ» kimi işarələnmiş sətirləri axtarırıq.
  if printf '%s' "$NETICE" | grep -qiE 'parol_hash.*(var|sızd|aşkar)|TƏHLÜKƏ.*parol_hash'; then
    echo "      ✗ cavabda parol_hash AŞKAR OLUNDU"; exit 1
  fi
fi
echo "      ✓ hamisi() cavabında parol_hash yoxdur (prob təsdiqləyir)"
printf '      ISTIFADECI_SECIM sahələri      : %s\n' \
  "$(awk '/export const ISTIFADECI_SECIM/,/as const/' src/auth/istifadeci.service.ts \
     | grep -oE '[a-z_]+: true' | cut -d: -f1 | tr '\n' ' ')"
if grep -qE '^\s+parol_hash: true' src/auth/istifadeci.service.ts; then
  echo "      ⚠️ «parol_hash: true» var — yalnız daxiliTap() daxilində olmalıdır"
  printf '      daxiliTap-də mi?               : %s\n' \
    "$(grep -B12 'parol_hash: true' src/auth/istifadeci.service.ts | grep -c 'private async daxiliTap')"
fi

echo ""
echo "  → 5) Təmizlik"
temizle_kullanici
SONRA=$(say "SELECT count(*) FROM kadrlar.istifadeciler;")
printf '      istifadəçi sayı (sondan sonra): %s\n' "$SONRA"
[ "$SONRA" = "$EVVEL" ] || { echo "  ✗ test iz qoydu: $EVVEL → $SONRA"; exit 1; }

echo ""
echo "  ✓ IIIA.3 KEÇDİ — istifadəçi servisi işləyir, hash sızmır"
)
