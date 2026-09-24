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

echo "  → 1) Fayl strukturu"
FAYLLAR="
src/auth/parol.service.ts
src/auth/istifadeci.service.ts
src/auth/token.service.ts
src/auth/auth.controller.ts
src/auth/auth.module.ts
src/auth/dto/parol.validator.ts
src/auth/dto/qeydiyyat.dto.ts
src/auth/dto/giris.dto.ts
src/auth/dto/token.dto.ts
src/auth/dto/rol.dto.ts
src/auth/qoruyucu/auth.guard.ts
src/auth/qoruyucu/roller.guard.ts
src/auth/qoruyucu/ictimai.dekorator.ts
src/auth/qoruyucu/roller.dekorator.ts
src/auth/qoruyucu/cari-istifadeci.dekorator.ts
skriptler/parol_yoxla.ts
skriptler/istifadeci_yoxla.ts
skriptler/token_yoxla.ts
skriptler/qoruyucu_yoxla.ts
skriptler/3a_yoxla.sh
"
EKSIK=0
for f in $FAYLLAR; do
  if [ -f "$f" ]; then
    printf '      ✓ %-52s %4s sətir\n' "$f" "$(wc -l < "$f" | tr -d ' ')"
  else
    printf '      ✗ %-52s YOXDUR\n' "$f"; EKSIK=$((EKSIK + 1))
  fi
done
[ "$EKSIK" = "0" ] || { echo "  ✗ $EKSIK fayl əskikdir"; exit 1; }
printf '      cəmi: %s fayl, %s sətir\n' \
  "$(echo "$FAYLLAR" | grep -c . )" \
  "$(cat $FAYLLAR | wc -l | tr -d ' ')"

echo ""
echo "  → 2) TypeScript tip yoxlaması"
if npx tsc --noEmit 2>/tmp/iiia1_tsc.log; then
  echo "      ✓ tip xətası yoxdur (0 xəta)"
else
  echo "      ✗ tip xətası var"; awk '{ print "      " $0 }' /tmp/iiia1_tsc.log | head -20; exit 1
fi

echo ""
echo "  → 3) SİRR GİGİYENASI (ən vacib yoxlama)"
if [ -f .gitignore ] && grep -qE '^\.env$|^/\.env$' .gitignore; then
  echo "      ✓ .gitignore .env-i istisna edir"
else
  echo "      ✗ .gitignore .env-i istisna ETMİR"; exit 1
fi
if [ -f .env.example ]; then
  NUM=$(grep '^JWT_SECRET=' .env.example | head -1 | cut -d= -f2- | tr -d '"' | tr -d ' ')
  case "$NUM" in
    *openssl*|*YAZIN*|*yazin*|*nümune*|*numune*|*example*|"")
      echo "      ✓ .env.example-də REAL sirr yoxdur (nümunə mətni)" ;;
    *)
      LEN=${#NUM}
      if [ "$LEN" -ge 32 ] && printf '%s' "$NUM" | grep -qE '^[A-Za-z0-9+/=]+$'; then
        echo "      ✗ TƏHLÜKƏ: .env.example-də REAL sirr ola bilər (uzunluq $LEN)"; exit 1
      else
        echo "      ✓ .env.example-də real sirr görünmür"
      fi ;;
  esac
else
  echo "      ✗ .env.example yoxdur"; exit 1
fi
for f in $(find src -name '*.ts'); do
  if grep -qE "JWT_SECRET\s*[:=]\s*['\"][A-Za-z0-9+/=]{16,}['\"]" "$f"; then
    echo "      ✗ TƏHLÜKƏ: $f içində SABİT JWT sirri var"; exit 1
  fi
done
echo "      ✓ src/ içində sabit JWT sirri yoxdur"

echo ""
echo "  → 4) parol_hash sızması yoxlaması"
SIZMA=0
for f in src/auth/dto/*.ts; do
  if grep -q 'parol_hash' "$f"; then
    echo "      ✗ $f içində parol_hash var"; SIZMA=$((SIZMA + 1))
  fi
done
[ "$SIZMA" = "0" ] && echo "      ✓ heç bir DTO-da parol_hash YOXDUR"
[ "$SIZMA" = "0" ] || exit 1
printf '      «parol_hash: true» oxunan yer sayı : %s (yalnız 1 olmalıdır — daxiliTap)\n' \
  "$(grep -c 'parol_hash: true' src/auth/istifadeci.service.ts)"
printf '      istifadeci.service-də parol_hash   : %s yer\n' \
  "$(grep -c 'parol_hash' src/auth/istifadeci.service.ts)"

echo ""
echo "  → 5) Qlobal guard QƏSDƏN yoxdur (3B-də əlavə olunacaq)"
APP=$(grep -rn 'APP_GUARD' src/ 2>/dev/null | grep -vE ':\s*(//|\*|/\*)' | wc -l | tr -d ' ')
if [ "$APP" = "0" ]; then
  echo "      ✓ APP_GUARD yoxdur — köhnə 40 test qorunur"
else
  echo "      ✗ APP_GUARD tapıldı — köhnə testlər qırılacaq"; exit 1
fi
printf '      guard qoşulan yer (UseGuards)      : %s\n' \
  "$(grep -rn 'UseGuards' src/auth/auth.controller.ts | wc -l | tr -d ' ')"

echo ""
echo "  ✓ IIIA.1 KEÇDİ — fayllar tamdır, tip təmizdir, sirr sızmır"
)
