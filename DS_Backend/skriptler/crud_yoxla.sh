#!/bin/bash
# ────────────────────────────────────────────────────────────────────
#  crud_yoxla.sh — CRUD endpoint-lərini CANLI yoxlayır.
#
#  İSTİFADƏ:
#     bash skriptler/crud_yoxla.sh            # port 4000
#     PORT=4100 bash skriptler/crud_yoxla.sh
#
#  NƏ EDİR:
#     1. Serveri arxa planda qaldırır (build-i özü edir).
#     2. POST  → yeni əməkdaş yaradır (201) və ID-ni götürür.
#     3. GET   → həmin əməkdaşı oxuyur (200).
#     4. PATCH → vəzifəsini və maaşını dəyişir (200).
#     5. XƏTA HALLARI: 400 (validasiya), 400 (yanlış FK), 404, 409.
#     6. DELETE→ yaratdığımız sətri silir (200, adi silmə).
#     7. Yoxlayır ki, baza əvvəlki vəziyyətinə qayıdıb.
#     8. Serveri MÜTLƏQ söndürür (trap).
#
#  ⚠️ Skript YALNIZ özü yaratdığı sətri silir — mövcud 14 əməkdaşa
#     heç bir zərər vermir.
# ────────────────────────────────────────────────────────────────────
set -u
cd "$(dirname "$0")/.." || exit 1

PORT="${PORT:-4000}"
BAZ="http://localhost:$PORT/api/v1/emekdaslar"
LOQ="/tmp/arti_crud_${PORT}.log"
TMP="/tmp/arti_crud_$$"
mkdir -p "$TMP"
PID=""

temizle() {
  [ -n "$PID" ] && kill "$PID" 2>/dev/null
  [ -n "$PID" ] && wait "$PID" 2>/dev/null
  rm -rf "$TMP"
  true
}
trap temizle EXIT INT TERM

KECDI=0
XETA=0

# ── Köməkçi: sorğu göndərir, statusu yoxlayır ─────────────────────
#   $1 = metod · $2 = yol · $3 = gövdə (boş ola bilər) · $4 = gözlənilən status
CAVAB=""
sorqu() {
  METOD="$1"; YOL="$2"; GOVDE="$3"; GOZLE="$4"
  CAVAB="$TMP/cavab.json"

  if [ -z "$GOVDE" ]; then
    KOD=$(curl -s -o "$CAVAB" -w '%{http_code}' -X "$METOD" "$YOL")
  else
    KOD=$(curl -s -o "$CAVAB" -w '%{http_code}' -X "$METOD" "$YOL" \
          -H 'Content-Type: application/json' -d "$GOVDE")
  fi

  QISA="${YOL#$BAZ}"
  [ -z "$QISA" ] && QISA="emekdaslar"
  case "$QISA" in
    \?*) QISA="emekdaslar$QISA" ;;
    /*)  QISA="emekdaslar$QISA" ;;
  esac

  if [ "$KOD" = "$GOZLE" ]; then
    printf '  [OK] %-6s %-46s -> %s\n' "$METOD" "$QISA" "$KOD"
    KECDI=$((KECDI + 1))
  else
    printf '  [XX] %-6s %-46s -> %s  (gözlənilirdi %s)\n' \
      "$METOD" "$QISA" "$KOD" "$GOZLE"
    XETA=$((XETA + 1))
    printf '       cavab: %s\n' "$(head -c 300 "$CAVAB")"
  fi
}

# ── Gövdədən sahə oxuyan köməkçi ────────────────────────────────────
saha() {
  python3 -c "
import json, sys
d = json.load(open('$TMP/cavab.json'))
for a in sys.argv[1:]:
    d = d.get(a) if isinstance(d, dict) else None
    if d is None:
        break
print('' if d is None else (json.dumps(d, ensure_ascii=False) if isinstance(d, (list, dict)) else d))
" "$@"
}

# ── Serveri qaldır ──────────────────────────────────────────────────
printf '════════ CRUD CANLI YOXLAMASI (port %s) ════════\n' "$PORT"

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  printf '  ✗ %s portu məşğuldur. Əvvəlcə boşaldın:\n' "$PORT"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | sed 's/^/      /'
  exit 1
fi

printf '  → build...\n'
npm run build >"$TMP/build.log" 2>&1 || { printf '  ✗ build uğursuz\n'; tail -20 "$TMP/build.log" | sed 's/^/      /'; exit 1; }

PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!

hazir=0
i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  curl -fsS "http://localhost:$PORT/api/v1/saglamliq" -o /dev/null 2>/dev/null && { hazir=1; break; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.5
done
[ "$hazir" = "1" ] || { printf '  ✗ server qalxmadı\n'; tail -20 "$LOQ" | sed 's/^/      /'; exit 1; }
printf '  ✓ server hazırdır (PID %s, %s cəhd)\n\n' "$PID" "$i"

# ── Başlanğıc sayı yadda saxla ──────────────────────────────────────
curl -s "$BAZ?limit=1&aktiv=hamisi" -o "$TMP/evvel.json"
EVVEL=$(python3 -c "import json;print(json.load(open('$TMP/evvel.json'))['cem'])")
printf '  → Əvvəlcə bazada %s əməkdaş var\n\n' "$EVVEL"

EPOX=$(date +%s)
EPOST="test.crud.${EPOX}@arti.edu.az"

# ── 1. CREATE ───────────────────────────────────────────────────────
printf '── 1) CREATE (POST) ──────────────────────────────────────────\n'
sorqu POST "$BAZ" "{\"ad\":\"Test\",\"soyad\":\"Yoxlayıcı\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"merkez_id\":1,\"email\":\"$EPOST\",\"ise_baslama\":\"2026-01-15\",\"maas\":1234.56}" 201
YENI_ID=$(python3 -c "
import json
try:
    d = json.load(open('$TMP/cavab.json'))
    print(d['data']['id'] if 'data' in d else d['id'])
except Exception:
    print('')
")
printf '      → yaradılan ID: %s\n\n' "$YENI_ID"
if [ -z "$YENI_ID" ]; then printf '  ✗ ID alına bilmədi — davam etmək mümkün deyil\n'; exit 1; fi

# ── 2. READ (biri) ──────────────────────────────────────────────────
printf '── 2) READ (GET /:id) ───────────────────────────────────────\n'
sorqu GET "$BAZ/$YENI_ID" "" 200
python3 -c "
import json
d = json.load(open('$TMP/cavab.json'))
print('      ad       :', d['tam_ad'])
print('      vezife   :', d['vezife']['ad'])
print('      maas     :', d['maas'], '(mətn!)')
print('      id tipi  :', type(d['id']).__name__, '→', repr(d['id']))
"
printf '\n'

# ── 3. UPDATE ───────────────────────────────────────────────────────
printf '── 3) UPDATE (PATCH) ────────────────────────────────────────\n'
sorqu PATCH "$BAZ/$YENI_ID" '{"vezife_id":4,"maas":2500}' 200
python3 -c "
import json
d = json.load(open('$TMP/cavab.json'))
print('      yeni vezife:', d['vezife']['ad'])
print('      yeni maas  :', d['maas'])
"
printf '\n'

# ── 4. XƏTA HALLARI ─────────────────────────────────────────────────
printf '── 4) XƏTA HALLARI ─────────────────────────────────────────\n'
sorqu POST "$BAZ" '{"ad":"A"}' 400
python3 -c "
import json
d = json.load(open('$TMP/cavab.json'))
print('      kod    :', d['xeta']['kod'])
print('      mesaj  :', d['xeta']['mesaj'])
for x in d['xeta'].get('detallar', [])[:6]:
    print('        ·', x)
"
printf '\n'

sorqu POST "$BAZ" '{"ad":"Test","soyad":"Yoxlayıcı","ata_adi":"Sistem","cinsiyyet_id":1,"vezife_id":99}' 400
python3 -c "
import json
d = json.load(open('$TMP/cavab.json'))
print('      kod :', d['xeta']['kod'], '← vezife_id 99 bazada yoxdur (FK xətası)')
"
printf '\n'

sorqu POST "$BAZ" "{\"ad\":\"Test\",\"soyad\":\"Təkrar\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$EPOST\"}" 409
python3 -c "
import json
d = json.load(open('$TMP/cavab.json'))
print('      kod :', d['xeta']['kod'], '← e-poçt artıq mövcuddur (UNIQUE)')
"
printf '\n'

sorqu POST "$BAZ" '{"ad":"Test","soyad":"Naməlum","ata_adi":"Sistem","cinsiyyet_id":1,"vezife_id":6,"yoluxucu":true}' 400
printf '      ↑ gövdədə olmayan sahə (yoluxucu) — forbidNonWhitelisted onu tutdu\n\n'

sorqu GET "$BAZ/999999" "" 404
sorqu PATCH "$BAZ/999999" '{"maas":100}' 404
sorqu GET "$BAZ/abc" "" 400
printf '      ↑ :id ədəd deyil — ParseIntPipe tutdu\n\n'

sorqu GET "$BAZ?limit=500" "" 400
printf '      ↑ limit 100-dən böyükdür — DTO tutdu\n\n'

sorqu GET "$BAZ?yoluxucu=1" "" 400
printf '      ↑ sorğuda olmayan parametr — forbidNonWhitelisted tutdu\n\n'

# ── 5. READ (siyahı, filtr, səhifələmə) ─────────────────────────────
printf '── 5) READ (siyahı · filtr · səhifələmə) ────────────────────\n'
sorqu GET "$BAZ?limit=3&seife=2&siralama=soyad&tertib=asc" "" 200
python3 -c "
import json
d = json.load(open('$TMP/cavab.json'))
print('      sehife %s/%s · cem %s' % (d['sehife'], d['sehife_sayi'], d['cem']))
for e in d['melumat']:
    print('        -', e['tam_ad'], '|', e['vezife']['ad'])
"
printf '\n'

sorqu GET "$BAZ?axtar=%C6%8Fliyev" "" 200
python3 -c "
import json
d = json.load(open('$TMP/cavab.json'))
print('      «Əliyev» axtarışı → %s nəticə' % d['cem'])
for e in d['melumat']:
    print('        -', e['tam_ad'])
"
printf '\n'

sorqu GET "$BAZ?merkez_id=1" "" 200
python3 -c "
import json
d = json.load(open('$TMP/cavab.json'))
print('      merkez_id=1 → %s əməkdaş' % d['cem'])
"
printf '\n'

# ── 6. DELETE ───────────────────────────────────────────────────────
printf '── 6) DELETE ────────────────────────────────────────────────\n'
sorqu DELETE "$BAZ/$YENI_ID" "" 200
python3 -c "
import json
d = json.load(open('$TMP/cavab.json'))
print('      silmə növü:', d['nov'], '(asılı qeyd yox idi → adi silmə)')
print('      mesaj     :', d['mesaj'])
print('      asılı qeyd:', d['asili_qeydler'])
"
printf '\n'

sorqu GET "$BAZ/$YENI_ID" "" 404
sorqu DELETE "$BAZ/$YENI_ID" "" 404
printf '\n'

# ── 7. TƏMİZLİK YOXLAMASI ───────────────────────────────────────────
printf '── 7) TƏMİZLİK ──────────────────────────────────────────────\n'
curl -s "$BAZ?limit=1&aktiv=hamisi" -o "$TMP/sonra.json"
SONRA=$(python3 -c "import json;print(json.load(open('$TMP/sonra.json'))['cem'])")
printf '      əvvəl: %s · sonra: %s\n' "$EVVEL" "$SONRA"
if [ "$EVVEL" = "$SONRA" ]; then
  printf '      \033[32m✓\033[0m baza əvvəlki vəziyyətinə qayıtdı\n'
  KECDI=$((KECDI + 1))
else
  printf '      \033[31m✗\033[0m sətir sayı dəyişdi!\n'
  XETA=$((XETA + 1))
fi

printf '\n════════ NƏTİCƏ ════════\n'
printf '  keçdi: %s   uğursuz: %s\n' "$KECDI" "$XETA"
if [ "$XETA" -eq 0 ]; then
  printf '  \033[32m✓ BÜTÜN CRUD VƏ XƏTA HALLARI DÜZGÜN İŞLƏYİR\033[0m\n'
  exit 0
fi
printf '  \033[31m✗ %s YOXLAMA UĞURSUZ\033[0m\n' "$XETA"
printf '  server loqu: %s\n' "$LOQ"
exit 1
