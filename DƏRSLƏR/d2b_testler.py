#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-2B — 10 yekun test (IIB.1 … IIB.10).

Hər test müstəqildir. Testlər `LAYIHE` mühit dəyişənini oxuyur
(standart: $HOME/Deepseek_ARTI/DS_Backend) və öz serverlərini özləri
qaldırıb söndürürlər.

⚠️ TƏHLÜKƏSİZLİK: mövcud 14 əməkdaşa HEÇ BİR test zərər vermir.
Bütün yazma əməliyyatları testin özünün yaratdığı müvəqqəti sətirlər
üzərindədir və `trap` ilə həmişə təmizlənir.

⚠️ QEYD: audit loqu testlərdən SONRA da qalır — bu, qəsdən belədir,
audit loqu əbədidir. Testlər yalnız `emekdaslar` cədvəlini təmizləyir.
"""

TESTLER = []


def _t(no, ad, giris, skript):
    TESTLER.append({"no": no, "ad": ad, "giris": giris,
                    "skript": skript.strip("\n")})


# ── Ümumi başlanğıclar ──────────────────────────────────────────────
BAS = r'''
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur: $(pwd)"; exit 1; }
[ -f .env ] || { echo "  ✗ .env yoxdur"; exit 1; }
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
[ -n "$DBURL" ] || { echo "  ✗ .env-də DATABASE_URL yoxdur"; exit 1; }
say() { psql "$DBURL" -At -c "$1" 2>/dev/null | tr -d ' '; }
'''

SERVER = r'''
PORT="${PORT:-4000}"
LOQ="/tmp/arti_iib_${PORT}.log"
API="http://localhost:$PORT/api/v1"
EM="$API/emekdaslar"

npm run build >/tmp/arti_iib_build.log 2>&1 \
  || { echo "  ✗ build uğursuz"; tail -n 20 /tmp/arti_iib_build.log | sed 's/^/      /'; exit 1; }

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "  ✗ $PORT portu məşğuldur"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN | sed 's/^/      /'
  exit 1
fi

PORT="$PORT" node dist/main.js >"$LOQ" 2>&1 &
PID=$!
temizle() {
  [ -n "$PID" ] && kill "$PID" 2>/dev/null
  [ -n "$PID" ] && wait "$PID" 2>/dev/null
  true
}
trap temizle EXIT INT TERM

hazir=0
i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  curl -fsS "$API/saglamliq" -o /dev/null 2>/dev/null && { hazir=1; break; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.5
done
[ "$hazir" = "1" ] || { echo "  ✗ server qalxmadı"; tail -n 20 "$LOQ" | sed 's/^/      /'; exit 1; }
printf '  ✓ server hazırdır (%s cəhd)\n' "$i"

kod()  { curl -s -o /dev/null -w '%{http_code}' "$@"; }
govde(){ curl -s "$@"; }
'''


# ══════════════════════════════════════════════════════════════════════
_t("IIB.1",
   "Statistika modulu: fayllar, aqreqatlar və canlı probe",
   """ADDIM 22-də yazdığımız statistika modulunu yoxlayır. Test
   <strong>üç</strong> səviyyəni yoxlayır: (1) fayllar və Prisma
   aqreqat metodlarının istifadəsi, (2) bazadaki PL/pgSQL funksiyaları,
   (3) 21 yoxlamalı canlı probe — real bazada.""",
   BAS + r'''
echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) Statistika faylları"
catmadi=0
for f in src/emekdaslar/statistika/dto/statistika-sorgu.dto.ts \
         src/emekdaslar/statistika/statistika.service.ts \
         src/emekdaslar/statistika/statistika.controller.ts \
         skriptler/statistika_yoxla.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ fayllar natamamdır — ADDIM 22-ni işlədin"; exit 1; }

echo ""
echo "  → 2) Prisma aqreqat metodları"
S=src/emekdaslar/statistika/statistika.service.ts
for m in 'groupBy' '_count' '_avg' '_sum' '_min' '_max' 'aggregate'; do
  N=$(grep -c "$m" "$S" || true)
  printf '      %-12s %s\n' "$m" "$N"
  [ "$N" -ge 1 ] || { echo "      ✗ $m istifadə olunmur!"; exit 1; }
done

echo ""
echo "  → 3) Baza funksiyaları və təhlükəsizlik"
grep -q 'queryRaw' "$S" || { echo "      ✗ queryRaw yoxdur!"; exit 1; }
printf '      $queryRaw çağırışı : %s\n' "$(grep -c 'queryRaw' "$S")"
grep -q 'queryRawUnsafe' "$S" && { echo "      ✗ TƏHLÜKƏLİ: queryRawUnsafe işlədilir!"; exit 1; }
echo "      ✓ queryRawUnsafe işlədilmir (SQL inyeksiyası qorunur)"
printf '      $transaction       : %s\n' "$(grep -c 'transaction' "$S")"

echo ""
echo "  → 4) Statistika endpoint-ləri"
printf '      endpoint sayı: %s\n' "$(grep -c '@Get' src/emekdaslar/statistika/statistika.controller.ts)"
for y in statistika statistika/merkezler statistika/vezifeler statistika/merkezler-tam; do
  grep -q "'$y'" src/emekdaslar/statistika/statistika.controller.ts \
    || { echo "      ✗ /$y yoxdur!"; exit 1; }
done
echo "      ✓ dörd endpoint mövcuddur"

echo ""
echo "  → 5) Tip yoxlaması"
npx tsc --noEmit || { echo "  ✗ tip xətası var"; exit 1; }
echo "      ✓ təmiz"

echo ""
echo "  → 6) CANLI statistika yoxlaması"
npx tsx skriptler/statistika_yoxla.ts
[ $? -eq 0 ] || { echo "  ✗ statistika probe uğursuz oldu"; exit 1; }

echo ""
echo "  ✓ IIB.1 KEÇDİ — statistika modulu tam işləyir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIB.2",
   "Statistika endpoint-ləri canlı işləyir və rəqəmlər uyğundur",
   """ADDIM 22-ni HTTP səviyyəsində yoxlayır. Test rəqəmləri
   <strong>iki fərqli yolla</strong> alıb tutuşdurur: API-dən və
   birbaşa SQL-dən. Əgər uyğun gəlməsə, problem statistika servisindədir.""",
   BAS + SERVER + r'''
echo ""
echo "  → 1) GET /emekdaslar/statistika"
KOD=$(kod "$EM/statistika")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi (marşrut sırası!)"; exit 1; }
govde "$EM/statistika" -o /tmp/iib2.json
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iib2.json'))
problem = []
print('      əməkdaş : cem=%s aktiv=%s passiv=%s' % (d['emekdas']['cem'], d['emekdas']['aktiv'], d['emekdas']['passiv']))
print('      maaş    : fondu=%s orta=%s min=%s maks=%s' % (d['maas']['fondu'], d['maas']['orta'], d['maas']['min'], d['maas']['maks']))
print('      baza fn : fondu=%s sert_orta=%s' % (d['baza_funksiyalari']['maas_fondu'], d['baza_funksiyalari']['sertifikasiya_ortalamasi']))
print('      əlaqələr: %s' % json.dumps(d['elaqeler'], ensure_ascii=False))
print('      cədvəl  : %s   hesablanma: %s ms' % (d['cedvel_sayi'], d['hesablanma_ms']))
if d['emekdas']['cem'] != 14: problem.append('cem 14 deyil: %r' % d['emekdas']['cem'])
if d['emekdas']['aktiv'] + d['emekdas']['passiv'] != d['emekdas']['cem']:
    problem.append('aktiv + passiv != cem')
if not (d['maas']['min'] < d['maas']['orta'] < d['maas']['maks']):
    problem.append('min < orta < maks pozulub')
if abs(d['maas']['fondu'] - d['baza_funksiyalari']['maas_fondu']) > 0.01:
    problem.append('Prisma fondu != PL/pgSQL fondu')
if d['cedvel_sayi'] != 48: problem.append('cədvəl sayı 48 deyil')
if not isinstance(d['maas']['orta'], float): problem.append('orta maaş ədəd deyil')
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ statistika cavabı yoxlamadan keçmədi"; exit 1; }
echo "      ✓ bütün göstəricilər düzgündür"

echo ""
echo "  → 2) API rəqəmləri SQL ilə TUTUŞDURULUR"
API_CEM=$(python3 -c "import json;print(json.load(open('/tmp/iib2.json'))['emekdas']['cem'])")
SQL_CEM=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
API_AKTIV=$(python3 -c "import json;print(json.load(open('/tmp/iib2.json'))['emekdas']['aktiv'])")
SQL_AKTIV=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE aktiv;")
API_FOND=$(python3 -c "import json;print(json.load(open('/tmp/iib2.json'))['maas']['fondu'])")
SQL_FOND=$(say "SELECT COALESCE(sum(maas),0) FROM kadrlar.emekdaslar WHERE aktiv;")
printf '      cem    : API=%s  SQL=%s\n' "$API_CEM" "$SQL_CEM"
printf '      aktiv  : API=%s  SQL=%s\n' "$API_AKTIV" "$SQL_AKTIV"
printf '      fondu  : API=%s  SQL=%s\n' "$API_FOND" "$SQL_FOND"
[ "$API_CEM" = "$SQL_CEM" ] || { echo "  ✗ cem uyğun deyil"; exit 1; }
[ "$API_AKTIV" = "$SQL_AKTIV" ] || { echo "  ✗ aktiv uyğun deyil"; exit 1; }
python3 -c "
a=float('$API_FOND'); b=float('$SQL_FOND')
assert abs(a-b) < 0.01, 'fondu uyğun deyil: %s vs %s' % (a,b)
print('      ✓ üç göstərici də SQL ilə üst-üstə düşür')
" || { echo "  ✗ fondu uyğun deyil"; exit 1; }

echo ""
echo "  → 3) Mərkəzlər üzrə qruplaşdırma"
govde "$EM/statistika/merkezler" -o /tmp/iib2b.json
python3 - <<'PSON'
import json
m = json.load(open('/tmp/iib2b.json'))
u = json.load(open('/tmp/iib2.json'))
problem = []
print('      qrup sayı: %s' % len(m))
for x in m[:5]:
    print('        %-34s sayı=%s orta=%s fondu=%s' % (x['merkez'][:34], x['emekdas_sayi'], x['orta_maas'], x['maas_fondu']))
cem = sum(x['emekdas_sayi'] for x in m)
if cem != u['emekdas']['aktiv']:
    problem.append('qrupların cəmi (%s) aktiv sayına (%s) bərabər deyil' % (cem, u['emekdas']['aktiv']))
if not all(isinstance(x['merkez'], str) and x['merkez'] for x in m):
    problem.append('mərkəz adı boşdur — Map birləşməsi işləmədi')
if not all(x['merkez_id'] is not None for x in m):
    problem.append('merkez_id null gəldi')
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ mərkəz qruplaşdırması uğursuz"; exit 1; }
echo "      ✓ qrupların cəmi ümumi sayla üst-üstə düşür"

echo ""
echo "  → 4) Parametrli baza funksiyası"
govde "$EM/statistika/shobe-sayi/2" -o /tmp/iib2c.json
python3 -c "
import json
d = json.load(open('/tmp/iib2c.json'))
print('      merkez %s → %s şöbə' % (d['merkez_id'], d['shobe_sayi']))
assert isinstance(d['shobe_sayi'], int), 'şöbə sayı tam ədəd deyil'
assert d['shobe_sayi'] > 0, 'şöbə sayı 0-dır'
print('      ✓ SQL funksiyası işləyir')
" || { echo "  ✗ baza funksiyası uğursuz"; exit 1; }

echo ""
echo "  → 5) N+1 olmayan bütün mərkəzlər"
govde "$EM/statistika/merkezler-tam" -o /tmp/iib2d.json
python3 -c "
import json
d = json.load(open('/tmp/iib2d.json'))
print('      %s mərkəz, cəmi %s şöbə, %s əməkdaş' % (len(d), sum(x['shobe_sayi'] for x in d), sum(x['emekdas_sayi'] for x in d)))
assert len(d) == 10, '10 mərkəz gözlənilirdi'
assert sum(x['shobe_sayi'] for x in d) == 36, '36 şöbə gözlənilirdi'
assert sum(x['emekdas_sayi'] for x in d) == 14, '14 əməkdaş gözlənilirdi'
print('      ✓ 3 sorğu ilə 10 mərkəz + 36 şöbə + 14 əməkdaş')
" || { echo "  ✗ mərkəz tam siyahısı uğursuz"; exit 1; }

echo ""
echo "  → 6) Xəta halları"
for y in "yad_parametr=1" "siralama=parol_hash" "aktiv=səhv" "min_say=0"; do
  K=$(kod "$EM/statistika/merkezler?$y")
  printf '      ?%-24s → %s\n' "$y" "$K"
  [ "$K" = "400" ] || { echo "      ✗ 400 gözlənilirdi"; exit 1; }
done
echo "      ✓ DTO bütün səhv parametrləri tutur"

echo ""
echo "  ✓ IIB.2 KEÇDİ — statistika endpoint-ləri düzgün işləyir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIB.3",
   "Əlaqələr: sorğu sayı ÖLÇÜLÜR və _count optimallaşdırması işləyir",
   """ADDIM 23-ün ən vacib nəticəsini yoxlayır: <strong>sorğu sayı
   ölçülür</strong>. Test üç yanaşmanı müqayisə edir — <code>icmal()</code>
   (yalnız saylar), <code>hamisi()</code> (paralel) və
   <code>birSorquda()</code> (bir <code>findUnique</code>). Əsas iddia:
   <em>sorğu sayını kod üslubu yox, Prisma strategiyası müəyyən edir</em>.""",
   BAS + r'''
echo "  → Layihə: $(pwd)"

echo ""
echo "  → 1) Əlaqələr faylları"
catmadi=0
for f in src/emekdaslar/elaqeler/elaqeler.service.ts \
         src/emekdaslar/elaqeler/elaqeler.controller.ts \
         skriptler/elaqeler_yoxla.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ fayllar natamamdır — ADDIM 23-ü işlədin"; exit 1; }

echo ""
echo "  → 2) Nazik sarğı naxışı (təkrar yoxlamanın qarşısı)"
N=$(grep -cE '^  private async [a-z]+Xam' src/emekdaslar/elaqeler/elaqeler.service.ts || true)
printf '      xam (private) metod sayı: %s\n' "$N"
[ "$N" -ge 6 ] || { echo "      ✗ xam metodlar yoxdur — təkrar yoxlama 6 sorğu artırar!"; exit 1; }
grep -q 'this.doktorantlarXam' src/emekdaslar/elaqeler/elaqeler.service.ts \
  || { echo "      ✗ hamisi() xam metodları çağırmır!"; exit 1; }
echo "      ✓ hamisi() xam versiyaları işlədir"

echo ""
echo "  → 3) _count optimallaşdırması"
grep -q '_count' src/emekdaslar/elaqeler/elaqeler.service.ts \
  || { echo "      ✗ _count istifadə olunmur!"; exit 1; }
grep -q 'Promise.all' src/emekdaslar/elaqeler/elaqeler.service.ts \
  || { echo "      ✗ Promise.all yoxdur!"; exit 1; }
echo "      ✓ _count və Promise.all mövcuddur"

echo ""
echo "  → 4) Əlaqəli cədvəllərdə məlumat"
for c in "elm.doktorantlar" "tehsil.sertifikasiya" "kadrlar.mezuniyyetler" \
         "kadrlar.is_tecrubesi" "elm.tedqiqat_layiheleri" "struktur.elmi_shura_uzvleri"; do
  N=$(say "SELECT count(*) FROM $c;")
  printf '      %-30s %s\n' "$c" "$N"
  [ "$N" -ge 1 ] || { echo "      ✗ $c boşdur"; exit 1; }
done

echo ""
echo "  → 5) CANLI ölçmə (sorğu sayğacı ilə)"
npx tsx skriptler/elaqeler_yoxla.ts
[ $? -eq 0 ] || { echo "  ✗ əlaqələr probe uğursuz oldu"; exit 1; }

echo ""
echo "  ✓ IIB.3 KEÇDİ — sorğu sayı ölçüldü və optimallaşdırma təsdiqləndi"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIB.4",
   "Əlaqə endpoint-ləri canlı işləyir: tam kart, saylar və altı siyahı",
   """ADDIM 23-ü HTTP səviyyəsində yoxlayır. On endpoint-in hamısı
   yoxlanılır: <code>/:id/icmal</code>, <code>/:id/tam</code>,
   altı ayrı əlaqə siyahısı, <code>/:id/tam-ad</code> və
   <code>/:id/tam-bir-sorqu</code>.""",
   BAS + SERVER + r'''
ID=6

echo ""
echo "  → 1) icmal() — yalnız saylar"
KOD=$(kod "$EM/$ID/icmal")
printf '      GET /$ID/icmal → %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$EM/$ID/icmal" -o /tmp/iib4.json
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iib4.json'))
problem = []
print('      %s' % d['tam_ad'])
print('      saylar: %s   cem=%s' % (json.dumps(d['saylar'], ensure_ascii=False), d['cem_elaqe']))
if not isinstance(d['emekdas_id'], str): problem.append('emekdas_id mətn deyil')
if d['cem_elaqe'] != sum(d['saylar'].values()): problem.append('cem_elaqe uyğun deyil')
if d['saylar']['doktorantlar'] != 4: problem.append('doktorant sayı 4 deyil: %r' % d['saylar']['doktorantlar'])
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ icmal yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 2) tam() — bütün əlaqələr paralel"
KOD=$(kod "$EM/$ID/tam")
printf '      GET /$ID/tam → %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$EM/$ID/tam" -o /tmp/iib4b.json
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iib4b.json'))
i = json.load(open('/tmp/iib4.json'))
problem = []
print('      doktorant=%s sertifikat=%s məzuniyyət=%s təcrübə=%s layihə=%s şura=%s (%s ms)' % (
  len(d['doktorantlar']), len(d['sertifikatlar']), len(d['mezuniyyetler']),
  len(d['tecrube']), len(d['layiheler']), len(d['shura_uzvleri']), d['cekme_ms']))
if len(d['doktorantlar']) != i['saylar']['doktorantlar']: problem.append('doktorant sayı icmal ilə uyğun deyil')
if len(d['shura_uzvleri']) != i['saylar']['shura_uzvleri']: problem.append('şura sayı uyğun deyil')
for k in ('doktorantlar','sertifikatlar','mezuniyyetler','tecrube','layiheler','shura_uzvleri'):
    if not isinstance(d[k], list): problem.append('%s massiv deyil' % k)
ke = d['doktorantlar'][0] if d['doktorantlar'] else None
if ke and ke['qebul_tarixi'] and len(ke['qebul_tarixi']) != 10:
    problem.append('tarix YYYY-MM-DD deyil: %r' % ke['qebul_tarixi'])
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ tam yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 3) Altı ayrı əlaqə endpoint-i"
for y in doktorantlar sertifikatlar mezuniyyetler tecrube layiheler shura; do
  K=$(kod "$EM/$ID/$y")
  N=$(govde "$EM/$ID/$y" | python3 -c "import json,sys;print(len(json.load(sys.stdin)))")
  printf '      /%-16s → %s  (%s sətir)\n' "$y" "$K" "$N"
  [ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
done

echo ""
echo "  → 4) tam-ad() — baza funksiyası ilə"
govde "$EM/$ID/tam-ad" -o /tmp/iib4c.json
TS=$(python3 -c "import json;print(json.load(open('/tmp/iib4b.json'))['tam_ad'])")
SQL=$(python3 -c "import json;print(json.load(open('/tmp/iib4c.json'))['tam_ad'])")
printf '      TypeScript : %s\n' "$TS"
printf '      SQL        : %s\n' "$SQL"
[ "$TS" = "$SQL" ] || { echo "  ✗ iki üsul fərqli nəticə verir!"; exit 1; }
echo "      ✓ hər iki üsul eyni nəticə verir"

echo ""
echo "  → 5) tam-bir-sorqu() — eyni nəticə, fərqli üsul"
K=$(kod "$EM/$ID/tam-bir-sorqu")
printf '      GET /$ID/tam-bir-sorqu → %s\n' "$K"
[ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$EM/$ID/tam-bir-sorqu" -o /tmp/iib4d.json
python3 -c "
import json
a = json.load(open('/tmp/iib4b.json'))
b = json.load(open('/tmp/iib4d.json'))
assert a['tam_ad'] == b['tam_ad'], 'tam_ad fərqlidir'
assert len(a['doktorantlar']) == len(b['doktorantlar']), 'doktorant sayı fərqlidir'
assert len(a['shura_uzvleri']) == len(b['shura_uzvleri']), 'şura sayı fərqlidir'
print('      ✓ hər iki üsul EYNİ nəticə verir')
" || { echo "  ✗ nəticələr fərqlidir"; exit 1; }

echo ""
echo "  → 6) Boş əlaqə boş massiv qaytarır"
govde "$EM/2/tam" -o /tmp/iib4e.json
python3 -c "
import json
d = json.load(open('/tmp/iib4e.json'))
print('      ID 2 — %s: doktorant=%s sertifikat=%s' % (d['tam_ad'], len(d['doktorantlar']), len(d['sertifikatlar'])))
for k in ('doktorantlar','sertifikatlar','mezuniyyetler','tecrube','layiheler','shura_uzvleri'):
    assert isinstance(d[k], list), '%s massiv deyil' % k
print('      ✓ boş əlaqələr [] qaytarır, null yox')
" || { echo "  ✗ boş əlaqə yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 7) Xəta halları"
printf '      /999999/icmal      → %s\n' "$(kod "$EM/999999/icmal")"
printf '      /999999/tam        → %s\n' "$(kod "$EM/999999/tam")"
printf '      /abc/icmal         → %s\n' "$(kod "$EM/abc/icmal")"
[ "$(kod "$EM/999999/icmal")" = "404" ] || { echo "  ✗ 404 gözlənilirdi"; exit 1; }
[ "$(kod "$EM/abc/icmal")" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
echo "      ✓ xəta halları düzgündür"

echo ""
echo "  ✓ IIB.4 KEÇDİ — bütün əlaqə endpoint-ləri işləyir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIB.5",
   "Toplu əməliyyatlar: createMany, atomiklik və validasiya",
   """ADDIM 24-ü yoxlayır. Əsas iddialar: (1) massiv validasiyası
   <code>@ValidateNested</code> ilə işləyir; (2) <code>createMany</code>
   atomikdir; (3) <code>skipDuplicates</code> işləyir. Test müvəqqəti
   sətirləri <em>özü</em> yaradır və <code>trap</code> ilə təmizləyir.""",
   BAS + r'''
EPOX=$(date +%s)
P="iib5.${EPOX}"
temizle2() {
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iib5.%@arti.edu.az';" >/dev/null
  true
}
trap temizle2 EXIT INT TERM

echo "  → 1) Toplu faylları"
catmadi=0
for f in src/emekdaslar/toplu/dto/toplu.dto.ts \
         src/emekdaslar/toplu/toplu.service.ts \
         src/emekdaslar/toplu/toplu.controller.ts \
         skriptler/toplu_yoxla.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ fayllar natamamdır — ADDIM 24-ü işlədin"; exit 1; }

echo ""
echo "  → 2) Massiv validasiyası"
D=src/emekdaslar/toplu/dto/toplu.dto.ts
for m in 'ValidateNested' 'ArrayMinSize' 'ArrayMaxSize' 'IsArray' 'Type(() =>'; do
  grep -q "$m" "$D" || { echo "      ✗ $m yoxdur!"; exit 1; }
  printf '      ✓ %s\n' "$m"
done
grep -q 'each: true' "$D" || { echo "      ✗ { each: true } yoxdur — massiv elementləri yoxlanılmayacaq!"; exit 1; }
echo "      ✓ each: true mövcuddur"

echo ""
echo "  → 3) Təhlükəsizlik qaydaları"
S=src/emekdaslar/toplu/toplu.service.ts
grep -q 'Filtrsiz toplu maaş' "$S" || { echo "      ✗ filtrsiz maaş qadağası yoxdur!"; exit 1; }
echo "      ✓ filtrsiz maaş dəyişikliyi qadağandır"
grep -q 'createManyAndReturn' "$S" || { echo "      ✗ createManyAndReturn yoxdur!"; exit 1; }
echo "      ✓ createManyAndReturn işlədilir"
grep -q 'multiply' "$S" || { echo "      ✗ atomik multiply yoxdur!"; exit 1; }
echo "      ✓ atomik multiply işlədilir"
grep -q "Min(-50" "$D" || { echo "      ✗ faiz -50 həddi yoxdur (sıfırlama riski!)"; exit 1; }
echo "      ✓ faiz həddi qorunur (-50)"

echo ""
echo "  → 4) Bazanın vəziyyəti (əvvəl)"
EVVEL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      emekdaş: %s\n' "$EVVEL"

echo ""
echo "  → 5) CANLI toplu əməliyyat yoxlaması"
npx tsx skriptler/toplu_yoxla.ts
[ $? -eq 0 ] || { echo "  ✗ toplu probe uğursuz oldu"; exit 1; }

echo ""
echo "  → 6) Bazanın vəziyyəti (sonra)"
SONRA=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
ZIBIL=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'toplu.%' OR email LIKE 'iib5.%';")
printf '      emekdaş: %s   zibil: %s\n' "$SONRA" "$ZIBIL"
[ "$EVVEL" = "$SONRA" ] || { echo "  ✗ sətir sayı dəyişdi!"; exit 1; }
[ "$ZIBIL" = "0" ] || { echo "  ✗ test zibili qaldı"; exit 1; }
echo "      ✓ baza toxunulmaz qaldı"

echo ""
echo "  ✓ IIB.5 KEÇDİ — toplu əməliyyatlar düzgün işləyir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIB.6",
   "Toplu endpoint-lər canlı: 201, atomiklik və filtrsiz qadağa",
   """ADDIM 24-ü HTTP səviyyəsində yoxlayır. Ən vacib yoxlama:
   <strong>təkrar e-poçt olan partiya HEÇ NƏ yazmır</strong>.
   Bu, atomikliyin canlı sübutudur — dövr içində yazmağın heç vaxt
   verə bilməyəcəyi zəmanət.""",
   BAS + SERVER + r'''
EPOX=$(date +%s)
P="iib6.${EPOX}"
YARADILAN=""
temizle2() {
  say "DELETE FROM struktur.elmi_shura_uzvleri WHERE emekdas_id IN (SELECT id FROM kadrlar.emekdaslar WHERE email LIKE 'iib6.%@arti.edu.az');" >/dev/null
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iib6.%@arti.edu.az';" >/dev/null
  temizle
}
trap temizle2 EXIT INT TERM

EVVEL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
echo "  → başlanğıc: $EVVEL əməkdaş"

echo ""
echo "  → 1) POST /toplu/yarat — 3 sətir bir sorğuda"
KOD=$(curl -s -o /tmp/iib6.json -w '%{http_code}' -X POST "$EM/toplu/yarat" \
  -H 'Content-Type: application/json' \
  -d "{\"emekdaslar\":[
    {\"ad\":\"Toplu1\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.1@arti.edu.az\",\"maas\":1000},
    {\"ad\":\"Toplu2\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.2@arti.edu.az\",\"maas\":2000},
    {\"ad\":\"Toplu3\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.3@arti.edu.az\",\"maas\":3000}]}")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "201" ] || { echo "  ✗ 201 gözlənilirdi"; head -c 300 /tmp/iib6.json; exit 1; }
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iib6.json'))
problem = []
print('      göndərilən=%s  yaradılan=%s  atlanan=%s' % (d['gonderilen'], d['yaradilan'], d['atlanan']))
print('      ID-lər: %s' % d['idler'])
if d['yaradilan'] != 3: problem.append('3 sətir yaradılmadı')
if d['atlanan'] != 0: problem.append('atlanan 0 deyil')
if not all(isinstance(i, str) for i in d['idler']): problem.append('ID-lər mətn deyil (BigInt sızır!)')
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ toplu yaratma cavabı uğursuz"; exit 1; }

IDLER=$(python3 -c "import json;print(','.join(json.load(open('/tmp/iib6.json'))['idler']))")
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE '$P.%';")
printf '      bazada təsdiqləndi: %s sətir\n' "$N"
[ "$N" = "3" ] || { echo "  ✗ bazada 3 sətir yoxdur"; exit 1; }

echo ""
echo "  → 2) ATOMİKLİK — təkrar e-poçt BÜTÜN partiyanı ləğv edir"
KOD=$(curl -s -o /tmp/iib6b.json -w '%{http_code}' -X POST "$EM/toplu/yarat" \
  -H 'Content-Type: application/json' \
  -d "{\"emekdaslar\":[
    {\"ad\":\"Yeni\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.9@arti.edu.az\"},
    {\"ad\":\"Tekrar\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.1@arti.edu.az\"}]}")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi (təkrar e-poçt)"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iib6b.json'))
print('      mesaj: %s' % d['xeta']['mesaj'][:120])
" || true
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE '$P.%';")
printf '      bazada sətir: %s (3 olmalıdır — HEÇ NƏ yazılmadı)\n' "$N"
[ "$N" = "3" ] || { echo "  ✗ ATOMİKLİK POZULDU — yarımçıq partiya yazıldı!"; exit 1; }
echo "      ✓ atomiklik təsdiqləndi"

echo ""
echo "  → 3) tekrarlariAtla: true — təkrar ATLANIR"
KOD=$(curl -s -o /tmp/iib6c.json -w '%{http_code}' -X POST "$EM/toplu/yarat" \
  -H 'Content-Type: application/json' \
  -d "{\"tekrarlariAtla\":true,\"emekdaslar\":[
    {\"ad\":\"Yeni9\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.9@arti.edu.az\"},
    {\"ad\":\"Tekrar\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.1@arti.edu.az\"}]}")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "201" ] || { echo "  ✗ 201 gözlənilirdi"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iib6c.json'))
print('      göndərilən=%s yaradılan=%s atlanan=%s' % (d['gonderilen'], d['yaradilan'], d['atlanan']))
assert d['yaradilan'] == 1 and d['atlanan'] == 1, 'gözlənilən 1/1'
print('      ✓ 1 yaradıldı, 1 atlandı')
" || { echo "  ✗ skipDuplicates işləmədi"; exit 1; }

IDLER="$IDLER,$(python3 -c "import json;print(','.join(json.load(open('/tmp/iib6c.json'))['idler']))")"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE '$P.%';")
printf '      bazada sətir: %s (4 olmalıdır)\n' "$N"
[ "$N" = "4" ] || { echo "  ✗ sətir sayı gözlənilən deyil"; exit 1; }

echo ""
echo "  → 4) PATCH /toplu/aktivlik"
KOD=$(curl -s -o /tmp/iib6d.json -w '%{http_code}' -X PATCH "$EM/toplu/aktivlik" \
  -H 'Content-Type: application/json' -d "{\"idler\":[$IDLER],\"aktiv\":false}")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iib6d.json'))
print('      %s (dəyişən=%s tapılmayan=%s)' % (d['melumat'], d['deyisen'], d['tapilmayan']))
assert d['deyisen'] == 4, '4 sətir dəyişməli idi'
assert d['tapilmayan'] == 0
"
N=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE '$P.%' AND NOT aktiv;")
printf '      bazada passiv: %s\n' "$N"
[ "$N" = "4" ] || { echo "  ✗ passiv sətir sayı səhvdir"; exit 1; }

echo ""
echo "  → 5) Mövcud olmayan ID → tapilmayan"
KOD=$(curl -s -o /tmp/iib6e.json -w '%{http_code}' -X PATCH "$EM/toplu/aktivlik" \
  -H 'Content-Type: application/json' -d "{\"idler\":[${IDLER%%,*},999999],\"aktiv\":true}")
python3 -c "
import json
d = json.load(open('/tmp/iib6e.json'))
print('      göndərilən=%s dəyişən=%s tapılmayan=%s' % (d['gonderilen_id'], d['deyisen'], d['tapilmayan']))
assert d['tapilmayan'] == 1, 'tapılmayan 1 olmalıdır'
print('      ✓ mövcud olmayan ID ayrıca bildirilir')
" || { echo "  ✗ tapılmayan ID yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 6) PATCH /toplu/maas-artim"
KOD=$(curl -s -o /dev/null -w '%{http_code}' -X PATCH "$EM/toplu/maas-artim" \
  -H 'Content-Type: application/json' -d "{\"faiz\":10,\"idler\":[$IDLER]}")
printf '      +10%% → %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
MAAS=$(say "SELECT maas FROM kadrlar.emekdaslar WHERE email='$P.1@arti.edu.az';")
printf '      1000 → %s\n' "$MAAS"
[ "$MAAS" = "1100.00" ] || { echo "  ✗ 10% artım səhvdir: $MAAS"; exit 1; }
echo "      ✓ atomik multiply düzgün işləyir"

echo ""
echo "  → 7) Filtrsiz maaş artımı → QADAĞAN"
FOND_EVVEL=$(say "SELECT COALESCE(sum(maas),0) FROM kadrlar.emekdaslar;")
KOD=$(curl -s -o /tmp/iib6f.json -w '%{http_code}' -X PATCH "$EM/toplu/maas-artim" \
  -H 'Content-Type: application/json' -d '{"faiz":50}')
printf '      status: %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi (təhlükəsizlik qaydası)"; exit 1; }
python3 -c "
import json
d = json.load(open('/tmp/iib6f.json'))
print('      mesaj: %s' % d['xeta']['mesaj'])
"
FOND_SONRA=$(say "SELECT COALESCE(sum(maas),0) FROM kadrlar.emekdaslar;")
printf '      ümumi fondu: %s → %s\n' "$FOND_EVVEL" "$FOND_SONRA"
[ "$FOND_EVVEL" = "$FOND_SONRA" ] || { echo "  ✗ FONDU DƏYİŞDİ — qadağa işləmədi!"; exit 1; }
echo "      ✓ filtrsiz artım rədd edildi, fondu dəyişmədi"

echo ""
echo "  → 8) Validasiya xəta halları"
printf '      boş massiv          → %s\n' "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":[]}')"
printf '      massiv deyil        → %s\n' "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":"abc"}')"
printf '      element səhvdir     → %s\n' "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":[{"ad":"A"}]}')"
printf '      faiz həddən kənar   → %s\n' "$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":-100,\"idler\":[$IDLER]}")"
printf '      idler boş           → %s\n' "$(kod -X PATCH "$EM/toplu/aktivlik" -H 'Content-Type: application/json' -d '{"idler":[],"aktiv":true}')"
for K in \
  "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":[]}')" \
  "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":"abc"}')" \
  "$(kod -X POST "$EM/toplu/yarat" -H 'Content-Type: application/json' -d '{"emekdaslar":[{"ad":"A"}]}')" \
  "$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":-100,\"idler\":[$IDLER]}")" \
  "$(kod -X PATCH "$EM/toplu/aktivlik" -H 'Content-Type: application/json' -d '{"idler":[],"aktiv":true}')"; do
  [ "$K" = "400" ] || { echo "  ✗ 400 gözlənilirdi, alındı: $K"; exit 1; }
done
echo "      ✓ beş validasiya halı düzgün tutulur"

echo ""
echo "  → 9) GET /toplu/atomiklik — rollback sübutu"
govde "$EM/toplu/atomiklik" -o /tmp/iib6g.json
python3 -c "
import json
d = json.load(open('/tmp/iib6g.json'))
print('      cəhd=%s  bazada qalan=%s  audit artımı=%s' % (d['cehd_edilen'], d['bazada_qalan'], d['audit_artimi']))
print('      izah: %s' % d['izah'])
assert d['bazada_qalan'] == 0, 'rollback işləmədi'
assert d['audit_artimi'] == 0, 'audit loqu artdı — rollback natamamdır'
print('      ✓ rollback: nə məlumat, nə audit qeydi qalmadı')
" || { echo "  ✗ atomiklik yoxlaması uğursuz"; exit 1; }

echo ""
echo "  → 10) Təmizlik"
say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE '$P.%';" >/dev/null
SONRA=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      emekdaş: %s → %s\n' "$EVVEL" "$SONRA"
[ "$EVVEL" = "$SONRA" ] || { echo "  ✗ baza vəziyyəti dəyişdi"; exit 1; }
echo "      ✓ baza əvvəlki vəziyyətindədir"

echo ""
echo "  ✓ IIB.6 KEÇDİ — bütün toplu endpoint-lər düzgün işləyir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIB.7",
   "FAİZ TƏLƏSİ: +10% sonra −10% əvvəlki dəyəri qaytarmır",
   """Dərsin ən praktik riyazi tapıntısını yoxlayır. <strong>Faiz artımı
   geri qaytarıla bilməz</strong> sadəcə əks faizlə: <code>x·1.1·0.9 =
   0.99x</code>. Test bunu real maaşlarla göstərir, sonra
   <em>düzgün</em> bərpa yolunu (bölmək) yoxlayır.""",
   BAS + SERVER + r'''
EPOX=$(date +%s)
P="iib7.${EPOX}"
IDLER=""
temizle2() {
  say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE 'iib7.%@arti.edu.az';" >/dev/null
  temizle
}
trap temizle2 EXIT INT TERM

echo ""
echo "  → 1) Üç test əməkdaşı yaradılır"
KOD=$(curl -s -o /tmp/iib7.json -w '%{http_code}' -X POST "$EM/toplu/yarat" \
  -H 'Content-Type: application/json' \
  -d "{\"emekdaslar\":[
    {\"ad\":\"Faiz1\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.1@arti.edu.az\",\"maas\":1000},
    {\"ad\":\"Faiz2\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.2@arti.edu.az\",\"maas\":2000},
    {\"ad\":\"Faiz3\",\"soyad\":\"$P\",\"ata_adi\":\"Sistem\",\"cinsiyyet_id\":1,\"vezife_id\":6,\"email\":\"$P.3@arti.edu.az\",\"maas\":3000}]}")
printf '      status: %s\n' "$KOD"
[ "$KOD" = "201" ] || { echo "  ✗ 201 gözlənilirdi"; exit 1; }
IDLER=$(python3 -c "import json;print(','.join(json.load(open('/tmp/iib7.json'))['idler']))")
printf '      ID-lər: %s\n' "$IDLER"

oxu() {
  say "SELECT string_agg(maas::text, ',' ORDER BY id) FROM kadrlar.emekdaslar WHERE id IN ($IDLER);"
}

EVVEL=$(oxu)
printf '      başlanğıc maaşlar: %s\n' "$EVVEL"
[ "$EVVEL" = "1000.00,2000.00,3000.00" ] || { echo "  ✗ başlanğıc maaşlar gözlənilən deyil: $EVVEL"; exit 1; }

echo ""
echo "  → 2) +10% tətbiq edilir"
KOD=$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":10,\"idler\":[$IDLER]}")
printf '      status: %s\n' "$KOD"
ARTMIS=$(oxu)
printf '      +10%% sonra: %s\n' "$ARTMIS"
[ "$ARTMIS" = "1100.00,2200.00,3300.00" ] || { echo "  ✗ 10% artım səhvdir: $ARTMIS"; exit 1; }
echo "      ✓ hər maaş dəqiq 10% artdı"

echo ""
echo "  → 3) −10% tətbiq edilir (FAİZ TƏLƏSİ)"
KOD=$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":-10,\"idler\":[$IDLER]}")
printf '      status: %s\n' "$KOD"
TELEDEN=$(oxu)
printf '      −10%% sonra: %s\n' "$TELEDEN"
printf '      başlanğıc : %s\n' "$EVVEL"
[ "$TELEDEN" != "$EVVEL" ] || { echo "  ✗ gözlənilməz: dəyərlər bərpa olundu — riyaziyyat səhvdir!"; exit 1; }
[ "$TELEDEN" = "990.00,1980.00,2970.00" ] || { echo "  ✗ gözlənilən 990/1980/2970, alındı: $TELEDEN"; exit 1; }
echo "      ✓ SÜBUT: +10% sonra −10% əvvəlki dəyəri QAYTARMADI"
echo "        riyazi izah: 3000 × 1.1 = 3300,  3300 × 0.9 = 2970 ≠ 3000"
python3 -c "
print('        itki: 1000→990 (10), 2000→1980 (20), 3000→2970 (30) = cəmi 60 AZN')
"

echo ""
echo "  → 4) İtki KÜMÜLATİVDİR — düzəliş onu geri qaytarmır"
KOD=$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":10,\"idler\":[$IDLER]}")
GERI_ARTMIS=$(oxu)
printf '      itkidən sonra +10%%: %s\n' "$GERI_ARTMIS"
[ "$GERI_ARTMIS" = "1089.00,2178.00,3267.00" ] || { echo "  ✗ gözlənilən 1089/2178/3267, alındı: $GERI_ARTMIS"; exit 1; }
echo "      ✓ düzəliş itkini geri qaytarmır — 1089 ≠ 1100"

say "UPDATE kadrlar.emekdaslar SET maas = maas / 1.1 WHERE id IN ($IDLER);" >/dev/null
GERI_SAKIT=$(oxu)
printf '      ÷1.1 ilə sakitləşdirdik: %s\n' "$GERI_SAKIT"
[ "$GERI_SAKIT" = "990.00,1980.00,2970.00" ] || { echo "  ✗ gözlənilən 990/1980/2970, alındı: $GERI_SAKIT"; exit 1; }
echo "      ✓ ÷1.1 ×1.1-i DƏQİQ geri qaytarır (amma itki artıq olub)"

echo ""
echo "  → 4b) TƏMİZ SÜBUT: ×1.1 sonra ÷1.1 → dəqiq bərpa"
ID3=$(say "SELECT id FROM kadrlar.emekdaslar WHERE email='$P.3@arti.edu.az';")
say "UPDATE kadrlar.emekdaslar SET maas = 3000 WHERE id = $ID3;" >/dev/null
ONCE=$(say "SELECT maas FROM kadrlar.emekdaslar WHERE id = $ID3;")
kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":10,\"idler\":[$ID3]}" >/dev/null
ORTADA=$(say "SELECT maas FROM kadrlar.emekdaslar WHERE id = $ID3;")
say "UPDATE kadrlar.emekdaslar SET maas = maas / 1.1 WHERE id = $ID3;" >/dev/null
SON=$(say "SELECT maas FROM kadrlar.emekdaslar WHERE id = $ID3;")
printf '      %s --(x1.1)--> %s --(/1.1)--> %s\n' "$ONCE" "$ORTADA" "$SON"
[ "$ONCE" = "$SON" ] || { echo "  ✗ bölmə dəqiq bərpa etmədi!"; exit 1; }
echo "      ✓ bölmə DƏQİQ tərs əməliyyatdır; faiz isə YOX"

echo ""
echo "  → 5) Sıfırlama riski — faiz = -100 qadağandır"
ONCE5=$(oxu)
printf '      cəhddən ƏVVƏL: %s\n' "$ONCE5"
KOD=$(kod -X PATCH "$EM/toplu/maas-artim" -H 'Content-Type: application/json' -d "{\"faiz\":-100,\"idler\":[$IDLER]}")
printf '      faiz=-100 → %s\n' "$KOD"
[ "$KOD" = "400" ] || { echo "  ✗ 400 gözlənilirdi — sıfırlama riski!"; exit 1; }
SON5=$(oxu)
printf '      cəhddən SONRA: %s\n' "$SON5"
[ "$ONCE5" = "$SON5" ] || { echo "  ✗ maaşlar dəyişdi: $ONCE5 → $SON5"; exit 1; }
echo "      ✓ -100 rədd edildi, maaşlar TOXUNULMAZ qaldı (əmsal 0 olardı)"
python3 -c "
print('        izah: 1 + (-100/100) = 0  →  bütün maaşlar 0.00 olardı')
"

echo ""
echo "  → 6) Təmizlik"
say "DELETE FROM kadrlar.emekdaslar WHERE email LIKE '$P.%';" >/dev/null
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
printf '      bazada əməkdaş: %s\n' "$TOTAL"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }

echo ""
echo "  ✓ IIB.7 KEÇDİ — faiz tələsi sübut olundu, düzgün bərpa yolu göstərildi"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIB.8",
   "Audit modulu: trigger, atomiklik və loqun oxunması",
   """ADDIM 25-i yoxlayır. Ən vacib iddia: bazadaki trigger
   <strong>heç bir tətbiq kodu olmadan</strong> hər dəyişikliyi yazır.
   Test həm də audit-in tranzaksiya ilə atomikliyini təsdiqləyir.""",
   BAS + r'''
echo "  → 1) Audit faylları"
catmadi=0
for f in src/audit/dto/audit-sorgu.dto.ts src/audit/audit.service.ts \
         src/audit/audit.controller.ts src/audit/audit.module.ts \
         skriptler/audit_yoxla.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ fayllar natamamdır — ADDIM 25-i işlədin"; exit 1; }

echo ""
echo "  → 2) Bazadaki trigger-lər (tətbiq kodundan asılı olmayaraq)"
psql "$DBURL" -c "
SELECT event_object_schema || '.' || event_object_table AS cedvel, trigger_name
  FROM information_schema.triggers
 WHERE trigger_schema NOT IN ('pg_catalog','information_schema')
 GROUP BY 1, trigger_name ORDER BY 1;" 2>/dev/null | sed 's/^/      /'
N=$(say "SELECT count(DISTINCT event_object_table) FROM information_schema.triggers WHERE trigger_schema NOT IN ('pg_catalog','information_schema') AND trigger_name LIKE '%audit%';")
printf '      audit trigger-i olan cədvəl: %s\n' "$N"
[ "$N" -ge 4 ] || { echo "  ✗ audit trigger-ləri tapılmadı"; exit 1; }
echo "      ✓ trigger-lər bazadadır (Baza dərslərindən)"

echo ""
echo "  → 3) Loqun həcmi və paylanması"
CEM=$(say "SELECT count(*) FROM audit.audit_log;")
CEDVEL=$(say "SELECT count(DISTINCT cedvel_adi) FROM audit.audit_log;")
printf '      cəmi qeyd   : %s\n' "$CEM"
printf '      cədvəl sayı : %s\n' "$CEDVEL"
[ "$CEM" -ge 1000 ] || { echo "  ✗ loq gözləniləndən kiçikdir"; exit 1; }
[ "$CEDVEL" -ge 3 ] || { echo "  ✗ ən azı 3 cədvəl gözlənilirdi"; exit 1; }
psql "$DBURL" -c "
SELECT cedvel_adi, emeliyyat, count(*) AS say FROM audit.audit_log
 GROUP BY 1,2 ORDER BY say DESC LIMIT 5;" 2>/dev/null | sed 's/^/      /'

echo ""
echo "  → 4) Sxem yoxlaması"
printf '      setir_id tipi  : %s (mətn olmalıdır!)\n' "$(say "SELECT data_type FROM information_schema.columns WHERE table_schema='audit' AND table_name='audit_log' AND column_name='setir_id';")"
[ "$(say "SELECT data_type FROM information_schema.columns WHERE table_schema='audit' AND table_name='audit_log' AND column_name='setir_id';")" = "text" ] \
  || { echo "  ✗ setir_id text deyil!"; exit 1; }
VAXT_TIP=$(say "SELECT data_type FROM information_schema.columns WHERE table_schema='audit' AND table_name='audit_log' AND column_name='vaxt';")
printf '      vaxt tipi      : %s\n' "$VAXT_TIP"
[ "$VAXT_TIP" = "timestampwithtimezone" ] \
  || { echo "  ✗ vaxt timestamptz deyil (say() boşluqları silir): $VAXT_TIP"; exit 1; }
echo "      ✓ sxem düzgündür"

echo ""
echo "  → 5) CANLI audit yoxlaması (28 yoxlama)"
EVVEL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
npx tsx skriptler/audit_yoxla.ts
[ $? -eq 0 ] || { echo "  ✗ audit probe uğursuz oldu"; exit 1; }

echo ""
echo "  → 6) Təmizlik və yekun"
SONRA=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
ZIBIL=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'audit.%' OR email LIKE 'toplu.%';")
printf '      emekdaş: %s → %s   zibil: %s\n' "$EVVEL" "$SONRA" "$ZIBIL"
[ "$EVVEL" = "$SONRA" ] || { echo "  ✗ sətir sayı dəyişdi!"; exit 1; }
[ "$ZIBIL" = "0" ] || { echo "  ✗ test zibili qaldı"; exit 1; }
printf '      audit loqu: %s → %s (artdı — gözlənilən)\n' "$CEM" "$(say "SELECT count(*) FROM audit.audit_log;")"

echo ""
echo "  ✓ IIB.8 KEÇDİ — audit loqu və trigger düzgün işləyir"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIB.9",
   "Audit endpoint-ləri və marşrut sırası (statistika ↔ :id)",
   """ADDIM 25 və 26-nı birlikdə yoxlayır. Ən vacib hissə:
   <strong>marşrut sırası</strong>. <code>/emekdaslar/statistika</code>
   və <code>/audit/statistika</code> hər ikisi <code>:id</code> ilə
   toqquşa bilər — test bunun düzgün həll olunduğunu təsdiqləyir.""",
   BAS + SERVER + r'''
echo ""
echo "  → 1) Audit endpoint-ləri"
KOD=$(kod "$API/audit?limit=3")
printf '      GET /audit?limit=3 → %s\n' "$KOD"
[ "$KOD" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$API/audit?limit=3" -o /tmp/iib9.json
python3 - <<'PSON'
import json
d = json.load(open('/tmp/iib9.json'))
problem = []
print('      cem=%s sehife=%s/%s gosterilen=%s' % (d['cem'], d['sehife'], d['sehife_sayi'], len(d['melumat'])))
for q in d['melumat']:
    print('        #%s %s %s setir=%s' % (q['id'], q['cedvel_adi'], q['emeliyyat'], q['setir_id']))
if len(d['melumat']) != 3: problem.append('3 qeyd gözlənilirdi')
if not isinstance(d['melumat'][0]['id'], str): problem.append('id mətn deyil (BigInt sızır!)')
if 'T' not in d['melumat'][0]['vaxt']: problem.append('vaxt ISO deyil')
for p in problem: print('      ✗ ' + p)
raise SystemExit(1 if problem else 0)
PSON
[ $? -eq 0 ] || { echo "  ✗ audit siyahısı uğursuz"; exit 1; }

echo ""
echo "  → 2) Statistika endpoint-ləri"
K=$(kod "$API/audit/statistika")
printf '      GET /audit/statistika → %s\n' "$K"
[ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi — marşrut sırası problemi!"; exit 1; }
govde "$API/audit/statistika" -o /tmp/iib9b.json
python3 -c "
import json
d = json.load(open('/tmp/iib9b.json'))
print('      cem qeyd=%s  cədvəl sayı=%s' % (d['cem_qeyd'], d['cedvel_sayi']))
print('      əməliyyat: %s' % '  '.join('%s=%s' % (x['emeliyyat'], x['cem']) for x in d['emeliyyat_uzre']))
assert d['cem_qeyd'] > 1000
assert sum(x['cem'] for x in d['emeliyyat_uzre']) == d['cem_qeyd'], 'əməliyyat cəmi uyğun deyil'
print('      ✓ paylanma düzgündür')
" || { echo "  ✗ audit statistikası uğursuz"; exit 1; }

echo ""
echo "  → 3) Süzgəclər"
K=$(kod "$API/audit?cedvel=kadrlar.emekdaslar&limit=2")
printf '      cedvel süzgəci     → %s\n' "$K"
[ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$API/audit?cedvel=kadrlar.emekdaslar&limit=5" -o /tmp/iib9c.json
python3 -c "
import json
d = json.load(open('/tmp/iib9c.json'))
assert all(q['cedvel_adi'] == 'kadrlar.emekdaslar' for q in d['melumat']), 'süzgəc işləmir'
print('      ✓ cədvəl süzgəci: %s qeyd, hamısı kadrlar.emekdaslar' % d['cem'])
" || { echo "  ✗ cədvəl süzgəci uğursuz"; exit 1; }
K=$(kod "$API/audit?emeliyyat=DELETE&limit=2")
printf '      emeliyyat süzgəci  → %s\n' "$K"
govde "$API/audit?emeliyyat=DELETE&limit=5" -o /tmp/iib9d.json
python3 -c "
import json
d = json.load(open('/tmp/iib9d.json'))
assert all(q['emeliyyat'] == 'DELETE' for q in d['melumat']), 'əмəliyyat süzgəci işləmir'
print('      ✓ əməliyyat süzgəci: %s qeyd, hamısı DELETE' % d['cem'])
" || { echo "  ✗ əməliyyat süzgəci uğursuz"; exit 1; }

echo ""
echo "  → 4) Trigger nümayişi (HTTP)"
K=$(kod "$API/audit/trigger-numayisi")
printf '      GET /audit/trigger-numayisi → %s\n' "$K"
[ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$API/audit/trigger-numayisi" -o /tmp/iib9e.json
python3 -c "
import json
d = json.load(open('/tmp/iib9e.json'))
print('      audit artımı: %s' % d['audit_artimi'])
print('      izah: %s' % d['izah'])
print('      əməliyyatlar: %s' % ','.join(q['emeliyyat'] for q in d['qeydler']))
assert d['audit_artimi'] == 3, '3 qeyd gözlənilirdi'
assert [q['emeliyyat'] for q in d['qeydler']] == ['INSERT','UPDATE','DELETE']
assert all(isinstance(q['setir_id'], str) for q in d['qeydler'])
print('      ✓ trigger INSERT/UPDATE/DELETE yazdı, setir_id mətndir')
" || { echo "  ✗ trigger nümayişi uğursuz"; exit 1; }

echo ""
echo "  → 5) Tranzaksiya nümayişi (HTTP)"
K=$(kod "$API/audit/tranzaksiya-numayisi")
printf '      GET /audit/tranzaksiya-numayisi → %s\n' "$K"
[ "$K" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
govde "$API/audit/tranzaksiya-numayisi" -o /tmp/iib9f.json
python3 -c "
import json
d = json.load(open('/tmp/iib9f.json'))
print('      əməkdaş=%s  audit artımı=%s' % (d['bazada_qalan_emekdas'], d['bazada_qalan_audit']))
print('      izah: %s' % d['izah'])
assert d['bazada_qalan_emekdas'] == 0 and d['bazada_qalan_audit'] == 0, 'rollback işləmədi'
print('      ✓ əməkdaş və audit BİR tranzaksiyada geri qaytarıldı')
" || { echo "  ✗ tranzaksiya nümayişi uğursuz"; exit 1; }

echo ""
echo "  → 6) MARŞRUT SIRASI — statistika ↔ :id toqquşması"
echo "      ── bütün 2 seqmentli yollar (toqquşma riski olan) ──"
for y in "emekdaslar/statistika" "emekdaslar/5" "emekdaslar/abc" "audit/statistika" "audit/1" "audit/abc"; do
  printf '      %-26s → %s\n' "/$y" "$(kod "$API/$y")"
done
[ "$(kod "$API/emekdaslar/statistika")" = "200" ] || { echo "  ✗ statistika işləmir — controller sırası!"; exit 1; }
[ "$(kod "$API/emekdaslar/5")" = "200" ] || { echo "  ✗ :id işləmir"; exit 1; }
[ "$(kod "$API/emekdaslar/abc")" = "400" ] || { echo "  ✗ mətn ID 400 verməlidir"; exit 1; }
[ "$(kod "$API/audit/statistika")" = "200" ] || { echo "  ✗ audit statistikası işləmir"; exit 1; }
[ "$(kod "$API/audit/1")" = "200" ] || { echo "  ✗ audit :id işləmir"; exit 1; }
[ "$(kod "$API/audit/abc")" = "400" ] || { echo "  ✗ audit mətn ID 400 verməlidir"; exit 1; }
echo "      ✓ KONKRET yollar :id-dən əvvəl qeydiyyatdadır"

echo ""
echo "  → 7) 3 seqmentli yollar (toqquşmamalıdır)"
for y in "emekdaslar/6/icmal" "emekdaslar/6/tam" "emekdaslar/6/doktorantlar" "emekdaslar/toplu/atomiklik"; do
  printf '      %-34s → %s\n' "/$y" "$(kod "$API/$y")"
  [ "$(kod "$API/$y")" = "200" ] || { echo "  ✗ 200 gözlənilirdi"; exit 1; }
done
echo "      ✓ uzun yollar toqquşmur"

echo ""
echo "  → 8) Xəta halları"
printf '      audit/99999999  → %s\n' "$(kod "$API/audit/99999999")"
printf '      audit?limit=500 → %s\n' "$(kod "$API/audit?limit=500")"
printf '      audit?emeliyyat=SIL → %s\n' "$(kod "$API/audit?emeliyyat=SIL")"
[ "$(kod "$API/audit/99999999")" = "404" ] || { echo "  ✗ 404 gözlənilirdi"; exit 1; }
[ "$(kod "$API/audit?limit=500")" = "400" ] || { echo "  ✗ 400 gözlənilirdi"; exit 1; }
echo "      ✓ xəta halları düzgündür"

echo ""
echo "  ✓ IIB.9 KEÇDİ — audit endpoint-ləri və marşrut sırası düzgündür"
'''),


# ══════════════════════════════════════════════════════════════════════
_t("IIB.10",
   "Yekun: tam 2B yoxlaması, optimallaşdırma və baza toxunulmazlığı",
   """Dərsin ən son testi. Üç hissə: (1) <code>skriptler/2b_yoxla.sh</code>
   — 48 canlı yoxlama; (2) <code>EXPLAIN ANALYZE</code> və indeks
   yoxlaması; (3) <em>simmetriya</em> — baza əvvəlki vəziyyətindədir.
   Ən sonda bütün dörd dərsin yoxlama alətləri bir yerdə işlədilir.""",
   BAS + r'''
[ -f skriptler/2b_yoxla.sh ] \
  || { echo "  ✗ skriptler/2b_yoxla.sh yoxdur — ADDIM 26-nı işlədin"; exit 1; }

echo "  → 1) Skriptin sintaksisi"
bash -n skriptler/2b_yoxla.sh || { echo "  ✗ bash sintaksisi səhvdir"; exit 1; }
printf '      ✓ düzgündür (%s sətir)\n' "$(wc -l < skriptler/2b_yoxla.sh | tr -d ' ')"

echo ""
echo "  → 2) Modul qrafı"
grep -q 'EmekdaslarModule' src/app.module.ts || { echo "  ✗ EmekdaslarModule qoşulmayıb!"; exit 1; }
grep -q 'AuditModule' src/app.module.ts || { echo "  ✗ AuditModule qoşulmayıb!"; exit 1; }
echo "      ✓ hər iki modul app.module.ts-dədir"
python3 - <<'PSON'
import pathlib, re
s = pathlib.Path('src/emekdaslar/emekdaslar.module.ts').read_text(encoding='utf-8')
m = re.search(r'controllers:\s*\[(.*?)\]', s, re.S)
adlar = re.findall(r'(\w+Controller)', m.group(1))
print('      controller sırası: %s' % ' → '.join(adlar))
if adlar[-1] != 'EmekdaslarController':
    raise SystemExit('✗ :id controller ƏN SONDA deyil!')
if 'StatistikaController' not in adlar[:2]:
    raise SystemExit('✗ StatistikaController əvvəldə deyil!')
print('      ✓ StatistikaController əvvəldə, EmekdaslarController axırda')
PSON
[ $? -eq 0 ] || { echo "  ✗ controller sırası səhvdir"; exit 1; }

echo ""
echo "  → 3) Bazanın vəziyyəti (əvvəl)"
EVVEL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
AUDIT_EVVEL=$(say "SELECT count(*) FROM audit.audit_log;")
printf '      emekdaş: %s   audit: %s\n' "$EVVEL" "$AUDIT_EVVEL"

echo ""
echo "  → 4) TAM 2B YOXLAMASI (48 yoxlama)"
bash skriptler/2b_yoxla.sh
CIXIS=$?
echo ""
printf '      skriptin çıxış kodu: %s\n' "$CIXIS"
[ "$CIXIS" -eq 0 ] || { echo "  ✗ 2b_yoxla.sh uğursuz oldu"; exit 1; }

echo ""
echo "  → 5) Simmetriya yoxlaması"
SONRA=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
ZIBIL=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'b%.%@arti.edu.az' OR email LIKE 'toplu.%' OR email LIKE 'audit.%' OR email LIKE 'iib%';")
AUDIT_SONRA=$(say "SELECT count(*) FROM audit.audit_log;")
printf '      emekdaş : %s → %s   zibil: %s\n' "$EVVEL" "$SONRA" "$ZIBIL"
printf '      audit   : %s → %s (+%s)\n' "$AUDIT_EVVEL" "$AUDIT_SONRA" "$((AUDIT_SONRA - AUDIT_EVVEL))"
[ "$EVVEL" = "$SONRA" ] || { echo "  ✗ sətir sayı dəyişdi!"; exit 1; }
[ "$ZIBIL" = "0" ] || { echo "  ✗ test zibili qaldı: $ZIBIL"; exit 1; }
echo "      ✓ baza toxunulmaz qaldı"
[ "$AUDIT_SONRA" -ge "$AUDIT_EVVEL" ] || { echo "  ✗ audit loqu azaldı — bu mümkün deyil"; exit 1; }
echo "      ✓ audit loqu yalnız ARTDIRILIR (append-only)"

echo ""
echo "  → 6) OPTİMALLAŞDIRMA — indeks və plan yoxlaması"
echo "      ── indekslər ──"
IDX=$(say "SELECT count(*) FROM pg_indexes WHERE schemaname='kadrlar' AND tablename='emekdaslar';")
printf '      emekdaslar üzrə indeks sayı: %s\n' "$IDX"
[ "$IDX" -ge 4 ] || { echo "  ✗ indekslər azdır"; exit 1; }
say "SELECT indexname FROM pg_indexes WHERE schemaname='kadrlar' AND tablename='emekdaslar';" | sed 's/^/        /'

echo "      ── EXPLAIN ANALYZE: audit_log ──"
for sorqu in \
  "SELECT count(*) FROM audit.audit_log WHERE cedvel_adi = 'kadrlar.emekdaslar'" \
  "SELECT count(*) FROM audit.audit_log WHERE istifadeci = 'arti_user'" \
  "SELECT id, soyad FROM kadrlar.emekdaslar ORDER BY soyad LIMIT 5"; do
  printf '        %s\n' "$sorqu"
  psql "$DBURL" -c "EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF, SUMMARY OFF) $sorqu" 2>/dev/null \
    | grep -E 'Scan|Rows Removed' | sed 's/^/          /'
done
echo "      ✓ indeks işlədilən və işlədilməyən hallar görüldü"
echo "        (indeksin OLMASI onun İŞLƏDİLƏCƏYİ demək deyil — planner qərar verir)"

echo ""
echo "  → 7) YEKUN: bütün yoxlama alətləri bir yerdə"
printf '      a) tip yoxlaması      : '
npx tsc --noEmit && echo "✓ təmiz"
printf '      b) DTO matrisi (2A)   : '
npx tsx skriptler/dto_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      c) mapper (2A)        : '
npx tsx skriptler/mapper_yoxla.ts 2>&1 | grep -c 'JSON.stringify İŞLƏDİ' >/dev/null && echo "✓ işləyir"
printf '      d) servis (2A)        : '
npx tsx skriptler/servis_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      e) statistika (2B)    : '
npx tsx skriptler/statistika_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      f) əlaqələr (2B)      : '
npx tsx skriptler/elaqeler_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      g) toplu (2B)         : '
npx tsx skriptler/toplu_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      h) audit (2B)         : '
npx tsx skriptler/audit_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'

echo ""
echo "  → 8) Son vəziyyət"
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
CEDVEL=$(say "SELECT count(*) FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog','information_schema');")
FAYL=$(find src -name '*.ts' | wc -l | tr -d ' ')
SKRIPT=$(ls -1 skriptler/ | wc -l | tr -d ' ')
printf '      bazada əməkdaş : %s\n' "$TOTAL"
printf '      bazada cədvəl  : %s\n' "$CEDVEL"
printf '      TypeScript     : %s fayl\n' "$FAYL"
printf '      yoxlama aləti  : %s\n' "$SKRIPT"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }

echo ""
echo "  ✓ IIB.10 KEÇDİ — Dərs 2B-nin bütün nəticələri təsdiqləndi"
''')
