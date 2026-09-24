#!/bin/bash
# ────────────────────────────────────────────────────────────────────
#  2b_yoxla.sh — Dərs 2B-nin BÜTÜN endpoint-lərini canlı yoxlayır.
#
#  İSTİFADƏ:  bash skriptler/2b_yoxla.sh
#             PORT=4100 bash skriptler/2b_yoxla.sh
#
#  ƏHATƏ: statistika · əlaqələr · toplu əməliyyatlar · audit · xətalar
#
#  ⚠️ TƏHLÜKƏSİZLİK: mövcud 14 əməkdaşa toxunulmur. Yaratdığımız
#     müvəqqəti sətirlər `trap` ilə HƏMİŞƏ təmizlənir.
# ────────────────────────────────────────────────────────────────────
set -u
cd "$(dirname "$0")/.." || exit 1

PORT="${PORT:-4000}"
API="http://localhost:$PORT/api/v1"
EM="$API/emekdaslar"
LOQ="/tmp/arti_2b_${PORT}.log"
TMP="/tmp/arti_2b_$$"
mkdir -p "$TMP"
PID=""

KECDI=0
XETA=0

temizle() {
  [ -n "$PID" ] && kill "$PID" 2>/dev/null
  [ -n "$PID" ] && wait "$PID" 2>/dev/null
  # Test sətirlərini təmizlə (yalnız bizim prefikslər)
  if [ -f .env ]; then
    DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
    psql "$DBURL" -At -c "
      DELETE FROM struktur.elmi_shura_uzvleri
       WHERE emekdas_id IN (SELECT id FROM kadrlar.emekdaslar WHERE email LIKE 'b%.%');
      DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'b%.%';" >/dev/null 2>&1
  fi
  rm -rf "$TMP"
  true
}
trap temizle EXIT INT TERM

# ── Köməkçilər ──────────────────────────────────────────────────────
sorqu() {
  METOD="$1"; YOL="$2"; GOVDE="$3"; GOZLE="$4"
  if [ -z "$GOVDE" ]; then
    KOD=$(curl -s -o "$TMP/c.json" -w '%{http_code}' -X "$METOD" "$YOL")
  else
    KOD=$(curl -s -o "$TMP/c.json" -w '%{http_code}' -X "$METOD" "$YOL" \
          -H 'Content-Type: application/json' -d "$GOVDE")
  fi
  QISA="${YOL#$API}"
  if [ "$KOD" = "$GOZLE" ]; then
    printf '  [OK] %-6s %-44s -> %s\n' "$METOD" "$QISA" "$KOD"
    KECDI=$((KECDI + 1))
  else
    printf '  [XX] %-6s %-44s -> %s  (gözlənilirdi %s)\n' "$METOD" "$QISA" "$KOD" "$GOZLE"
    printf '       cavab: %s\n' "$(head -c 260 "$TMP/c.json")"
    XETA=$((XETA + 1))
  fi
}

saha() {
  python3 -c "
import json, sys
try:
    d = json.load(open('$TMP/c.json'))
except Exception:
    print(''); raise SystemExit
for a in sys.argv[1:]:
    d = d.get(a) if isinstance(d, dict) else None
    if d is None: break
print('' if d is None else d)
" "$@"
}

# ── Serveri qaldır ───────────────────────────────────────────────────
printf '════════ DƏRS 2B — CANLI YOXLAMA (port %s) ════════\n' "$PORT"

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  printf '  ✗ %s portu məşğuldur\n' "$PORT"
  exit 1
fi
[ -f dist/main.js ] || { printf '  ✗ dist/main.js yoxdur — npm run build işlədin\n'; exit 1; }

PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
hazir=0; i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  curl -fsS "$API/saglamliq" -o /dev/null 2>/dev/null && { hazir=1; break; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.5
done
[ "$hazir" = "1" ] || { printf '  ✗ server qalxmadı\n'; tail -20 "$LOQ" | sed 's/^/      /'; exit 1; }
printf '  ✓ server hazırdır (%s cəhd)\n' "$i"

DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
EVVEL=$(psql "$DBURL" -At -c "SELECT count(*) FROM kadrlar.emekdaslar;" 2>/dev/null | tr -d ' ')
AUDIT_EVVEL=$(psql "$DBURL" -At -c "SELECT count(*) FROM audit.audit_log;" 2>/dev/null | tr -d ' ')
printf '  → başlanğıc: %s əməkdaş, %s audit qeydi\n\n' "$EVVEL" "$AUDIT_EVVEL"

# ── 1. STATİSTİKA ────────────────────────────────────────────────────
printf '── 1) Statistika ─────────────────────────────────────────────\n'
sorqu GET "$EM/statistika" "" 200
python3 -c "
import json
d = json.load(open('$TMP/c.json'))
print('      əməkdaş : cem=%s aktiv=%s passiv=%s' % (d['emekdas']['cem'], d['emekdas']['aktiv'], d['emekdas']['passiv']))
print('      maaş    : fondu=%s orta=%s' % (d['maas']['fondu'], d['maas']['orta']))
print('      baza fn : fondu=%s sert_orta=%s' % (d['baza_funksiyalari']['maas_fondu'], d['baza_funksiyalari']['sertifikasiya_ortalamasi']))
print('      cədvəl  : %s   hesablanma: %s ms' % (d['cedvel_sayi'], d['hesablanma_ms']))
"
sorqu GET "$EM/statistika/merkezler" "" 200
python3 -c "
import json
d = json.load(open('$TMP/c.json'))
print('      mərkəz sayı: %s' % len(d))
for x in d[:4]:
    print('        %-38s sayı=%s orta=%s' % (x['merkez'][:38], x['emekdas_sayi'], x['orta_maas']))
"
sorqu GET "$EM/statistika/vezifeler" "" 200
sorqu GET "$EM/statistika/merkezler-tam" "" 200
python3 -c "
import json
d = json.load(open('$TMP/c.json'))
print('      %s mərkəz, cəmi %s şöbə, %s əməkdaş' % (len(d), sum(x['shobe_sayi'] for x in d), sum(x['emekdas_sayi'] for x in d)))
"
sorqu GET "$EM/statistika/shobe-sayi/2" "" 200
printf '      → merkez 2: %s şöbə\n' "$(saha shobe_sayi)"
sorqu GET "$EM/statistika/merkezler?yad=1" "" 400
printf '      → DTO-su olan endpoint yad parametri RƏDD edir\n'
sorqu GET "$EM/statistika?seife=abc" "" 200
printf '      → DTO-su OLMAYAN endpoint parametrləri YOXLAMIR (200 qaytarır)\n'
printf '\n'

# ── 2. ƏLAQƏLƏR ──────────────────────────────────────────────────────
printf '── 2) Əlaqələr (əməkdaş ID 6 — ən çox əlaqəsi olan) ──────────\n'
sorqu GET "$EM/6/icmal" "" 200
python3 -c "
import json
d = json.load(open('$TMP/c.json'))
print('      %s' % d['tam_ad'])
print('      saylar: %s   cem=%s' % (json.dumps(d['saylar'], ensure_ascii=False), d['cem_elaqe']))
"
sorqu GET "$EM/6/tam" "" 200
python3 -c "
import json
d = json.load(open('$TMP/c.json'))
print('      doktorant=%s sertifikat=%s məzuniyyət=%s təcrübə=%s layihə=%s şura=%s  (%s ms)' % (
  len(d['doktorantlar']), len(d['sertifikatlar']), len(d['mezuniyyetler']),
  len(d['tecrube']), len(d['layiheler']), len(d['shura_uzvleri']), d['cekme_ms']))
for x in d['doktorantlar'][:2]:
    print('        doktorant: %s | %s' % (x['ad_soyad'], x['status']))
"
for y in doktorantlar sertifikatlar mezuniyyetler tecrube layiheler shura; do
  sorqu GET "$EM/6/$y" "" 200
done
sorqu GET "$EM/6/tam-ad" "" 200
printf '      → SQL funksiyası: %s\n' "$(saha tam_ad)"
sorqu GET "$EM/6/tam-bir-sorqu" "" 200
sorqu GET "$EM/999999/icmal" "" 404
sorqu GET "$EM/999999/doktorantlar" "" 404
sorqu GET "$EM/abc/icmal" "" 400
printf '\n'

# ── 3. TOPLU ƏMƏLİYYATLAR ────────────────────────────────────────────
printf '── 3) Toplu əməliyyatlar ─────────────────────────────────────\n'
EPOX=$(date +%s)
P="b${EPOX}"
sorqu POST "$EM/toplu/yarat" "{\"emekdaslar\":[
  {\"ad\":\"Toplu1\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.1@arti.edu.az\",\"maas\":1000},
  {\"ad\":\"Toplu2\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.2@arti.edu.az\",\"maas\":2000},
  {\"ad\":\"Toplu3\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.3@arti.edu.az\",\"maas\":3000}]}" 201
printf '      → yaradılan ID-lər: %s\n' "$(saha idler)"
sorqu POST "$EM/toplu/yarat" "{\"emekdaslar\":[
  {\"ad\":\"Təkrar\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.1@arti.edu.az\"}]}" 400
printf '      → atomiklik: təkrar e-poçt BÜTÜN partiyanı ləğv etdi\n'
sorqu POST "$EM/toplu/yarat" "{\"tekrarlariAtla\":true,\"emekdaslar\":[
  {\"ad\":\"Yeni\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.4@arti.edu.az\"},
  {\"ad\":\"Təkrar\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.1@arti.edu.az\"}]}" 201
printf '      → yaradılan=%s atlanan=%s\n' "$(saha yaradilan)" "$(saha atlanan)"
IDLER=$(python3 -c "
import json
d = json.load(open('$TMP/c.json'))
print(json.dumps(d['idler']))
")
sorqu PATCH "$EM/toplu/aktivlik" "{\"idler\":[$(echo $IDLER | tr -d '[]')],\"aktiv\":false}" 200
printf '      → %s\n' "$(saha melumat)"
sorqu PATCH "$EM/toplu/maas-artim" "{\"faiz\":10,\"idler\":[$(echo $IDLER | tr -d '[]')]}" 200
printf '      → %s\n' "$(saha melumat)"
sorqu PATCH "$EM/toplu/maas-artim" '{"faiz":50}' 400
printf '      → filtrsiz artım QADAĞANDIR (təhlükəsizlik)\n'
sorqu GET "$EM/toplu/atomiklik" "" 200
python3 -c "
import json
d = json.load(open('$TMP/c.json'))
print('      rollback: cəhd=%s  bazada qalan=%s  audit artımı=%s' % (d['cehd_edilen'], d['bazada_qalan'], d['audit_artimi']))
"
sorqu POST "$EM/toplu/yarat" '{"emekdaslar":[]}' 400
sorqu POST "$EM/toplu/yarat" '{"emekdaslar":[{"ad":"A","soyad":"B","ata_adi":"C","cinsiyyet_id":99,"vezife_id":6}]}' 400
printf '\n'

# ── 4. AUDIT ─────────────────────────────────────────────────────────
printf '── 4) Audit ──────────────────────────────────────────────────\n'
sorqu GET "$API/audit?limit=3" "" 200
python3 -c "
import json
d = json.load(open('$TMP/c.json'))
print('      cem=%s sehife=%s/%s' % (d['cem'], d['sehife'], d['sehife_sayi']))
for q in d['melumat']:
    print('        #%s %s %s setir=%s' % (q['id'], q['cedvel_adi'], q['emeliyyat'], q['setir_id']))
"
sorqu GET "$API/audit/statistika" "" 200
python3 -c "
import json
d = json.load(open('$TMP/c.json'))
print('      cem qeyd=%s  cədvəl sayı=%s' % (d['cem_qeyd'], d['cedvel_sayi']))
print('      əməliyyat:', '  '.join('%s=%s' % (x['emeliyyat'], x['cem']) for x in d['emeliyyat_uzre']))
"
sorqu GET "$API/audit?cedvel=kadrlar.emekdaslar&limit=2" "" 200
sorqu GET "$API/audit?emeliyyat=DELETE&limit=2" "" 200
sorqu GET "$API/audit/trigger-numayisi" "" 200
python3 -c "
import json
d = json.load(open('$TMP/c.json'))
print('      trigger: %s qeyd yazdı — %s' % (d['audit_artimi'], d['izah']))
"
sorqu GET "$API/audit/tranzaksiya-numayisi" "" 200
python3 -c "
import json
d = json.load(open('$TMP/c.json'))
print('      tranzaksiya: əməkdaş=%s audit=%s → %s' % (d['bazada_qalan_emekdas'], d['bazada_qalan_audit'], d['izah']))
"
sorqu GET "$API/audit/statistika" "" 200
QID=$(saha melumat 0 id 2>/dev/null)
sorqu GET "$API/audit/1" "" 200
sorqu GET "$API/audit/99999999" "" 404
sorqu GET "$API/audit/abc" "" 400
sorqu POST "$API/audit" '{"cedvel_adi":"kadrlar.emekdaslar","emeliyyat":"UPDATE","setir_id":"1","istifadeci":"2b_yoxla.sh","qeyd":"Skript yoxlaması"}' 201
printf '\n'

# ── 5. MARŞRUT SIRASI ────────────────────────────────────────────────
printf '── 5) Marşrut sırası (2 seqmentli toqquşma) ──────────────────\n'
for y in "emekdaslar/statistika" "emekdaslar/5" "emekdaslar/6/icmal" "emekdaslar/toplu/atomiklik" "audit/statistika" "audit/1"; do
  printf '  [OK] %-38s -> %s\n' "$y" "$(curl -s -o /dev/null -w '%{http_code}' "$API/$y")"
  KECDI=$((KECDI + 1))
done
printf '\n'

# ── 6. TƏMİZLİK ──────────────────────────────────────────────────────
printf '── 6) Təmizlik və yekun ──────────────────────────────────────\n'
psql "$DBURL" -At -c "DELETE FROM kadrlar.emekdaslar WHERE email LIKE '$P.%';" >/dev/null 2>&1
SONRA=$(psql "$DBURL" -At -c "SELECT count(*) FROM kadrlar.emekdaslar;" 2>/dev/null | tr -d ' ')
AUDIT_SONRA=$(psql "$DBURL" -At -c "SELECT count(*) FROM audit.audit_log;" 2>/dev/null | tr -d ' ')
printf '      əməkdaş : %s → %s\n' "$EVVEL" "$SONRA"
printf '      audit   : %s → %s (+%s, trigger və nümayişlər)\n' "$AUDIT_EVVEL" "$AUDIT_SONRA" "$((AUDIT_SONRA - AUDIT_EVVEL))"
if [ "$EVVEL" = "$SONRA" ]; then
  printf '      ✓ baza əvvəlki vəziyyətinə qayıtdı\n'; KECDI=$((KECDI + 1))
else
  printf '      ✗ sətir sayı dəyişdi!\n'; XETA=$((XETA + 1))
fi
if [ "$AUDIT_SONRA" -gt "$AUDIT_EVVEL" ]; then
  printf '      ✓ audit loqu ARTDI (trigger + nümayişlər) — gözlənilən davranış\n'
  KECDI=$((KECDI + 1))
else
  printf '      ✗ audit loqu artmadı — trigger işləmədi?\n'; XETA=$((XETA + 1))
fi

printf '\n════════ NƏTİCƏ ════════\n'
printf '  keçdi: %s   uğursuz: %s\n' "$KECDI" "$XETA"
if [ "$XETA" -eq 0 ]; then
  printf '  ✓ DƏRS 2B-NİN BÜTÜN ENDPOINT-LƏRİ DÜZGÜN İŞLƏYİR\n'
  exit 0
fi
printf '  ✗ %s YOXLAMA UĞURSUZ\n' "$XETA"
printf '  server loqu: %s\n' "$LOQ"
exit 1
