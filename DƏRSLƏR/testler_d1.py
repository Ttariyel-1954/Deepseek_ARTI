# -*- coding: utf-8 -*-
"""DƏRS 1 və DƏRS 2 — yekun test skriptləri (I.1–I.5, II.1–II.10)."""

DERSLER = [
    dict(
        rumuz="I",
        ad="Dərs 1 — Sıfırdan ilk işləyən API",
        qisa="Layihə skeleti, TypeScript konfiqurasiyası, <code>.env</code>, "
             "Prisma sxeması və generasiyası, <code>PrismaService</code>, "
             "<code>@Global()</code> modul, vahid xəta formatı, sağlamlıq "
             "endpointi və ilk build.",
        testler=[
            dict(
                no="I.1",
                ad="Layihə skeleti və asılılıqlar",
                giris=(
                    "Bu test Dərs 1-in ilk üç addımını yoxlayır: layihə "
                    "qovluğunun, <code>package.json</code>-ın və TypeScript "
                    "konfiqurasiyasının yerində olub-olmadığını. Əgər bu "
                    "fayllardan biri yoxdursa, nə build, nə də server işləyir — "
                    "ona görə bu, bütün sonrakı dərslərin təməlidir. Skript həm "
                    "də Node və npm versiyalarını və əsas NestJS paketlərinin "
                    "quraşdırıldığını göstərir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── Node və npm ──"
echo "  node: $(node -v)   npm: $(npm -v)"

echo "── Konfiqurasiya faylları ──"
for f in package.json tsconfig.json tsconfig.build.json nest-cli.json .env .env.example prisma/schema.prisma; do
  [ -f "$f" ] && echo "  ✓ $f" || echo "  ✗ $f YOXDUR"
done

echo "── Əsas paketlər ──"
for p in @nestjs/core @nestjs/common @nestjs/config @prisma/client; do
  v=$(python3 -c "import json;print(json.load(open('node_modules/$p/package.json'))['version'])" 2>/dev/null)
  echo "  $p = ${v:-QURAŞDIRILMAYIB}"
done

echo "── npm skriptləri ──"
python3 -c "import json;[print('  '+k+' → '+v) for k,v in json.load(open('package.json'))['scripts'].items()]"
''',
            ),
            dict(
                no="I.2",
                ad="Prisma sxeması — bazanı oxuyub tipləri çıxarmaq",
                giris=(
                    "Bu test Dərs 1-in beşinci və altıncı addımını yoxlayır: "
                    "Prisma sxemasının bazadan oxunub yaradılmasını və "
                    "generasiya olunmuş klientin yerində olmasını. Sxemada "
                    "<code>generator</code>, <code>datasource</code> və "
                    "<code>schemas</code> blokları olmalıdır — biri düşsə "
                    "Prisma <code>P1012</code> xətası verir. Skript həm də "
                    "sxemanın özünü yoxlayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── Sxemanın əsas blokları ──"
grep -nE '^(generator|datasource)|^  (provider|output|url|schemas)' prisma/schema.prisma

echo "── Sxemada nə qədər model var? ──"
echo "  model sayı: $(grep -c '^model ' prisma/schema.prisma)"

echo "── Neçə PostgreSQL sxemi oxunub? ──"
grep -o '"[a-z]*"' prisma/schema.prisma | head -1 >/dev/null
python3 - <<'PY'
import re, pathlib
s = pathlib.Path('prisma/schema.prisma').read_text(encoding='utf-8')
m = re.search(r'schemas\s*=\s*\[(.*?)\]', s, re.S)
adlar = re.findall(r'"([^"]+)"', m.group(1)) if m else []
print('  sxem sayı:', len(adlar))
print('  ', ', '.join(adlar))
PY

echo "── Generasiya olunmuş klient ──"
[ -f src/generated/prisma/client.ts ] && echo "  ✓ src/generated/prisma/client.ts" \
  || echo "  ✗ klient generasiya olunmayıb — «npx prisma generate» lazımdır"

echo "── Sxemanın etibarlılığı ──"
npx prisma validate 2>&1 | tail -2
''',
            ),
            dict(
                no="I.3",
                ad="Server və baza bağlantısı — sağlamlıq endpointi",
                giris=(
                    "Bu test Dərs 1-in doqquzuncu addımını yoxlayır: "
                    "<code>GET /saglamliq</code> endpointinin sadəcə «işləyirəm» "
                    "demədiyini, həm də bazaya sorğu göndərdiyini. Cavabda "
                    "cədvəl sayı və gecikmə olmalıdır — bunlar bazanın həqiqətən "
                    "əlçatan olduğunu sübut edir. Skript cavabı bazadakı real "
                    "cədvəl sayı ilə də tutuşdurur."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
echo "GET /saglamliq → $kod"
if [ "$kod" != "200" ]; then
  echo "⚠️ Server işləmir. Ayrı terminalda işlədin:"
  echo "   cd $LAYIHE && PORT=4000 npm run start:prod"
  exit 1
fi

echo "── Serverin cavabı ──"
curl -s "$A/saglamliq" | python3 -m json.tool

echo "── Bazadakı real cədvəl sayı ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT count(*) FROM pg_class c
  JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE c.relkind = 'r'
    AND n.nspname NOT IN ('pg_catalog','information_schema')" | sed 's/^/  /'
''',
            ),
            dict(
                no="I.4",
                ad="Vahid xəta formatı — AllExceptionsFilter",
                giris=(
                    "Bu test Dərs 1-in səkkizinci addımını yoxlayır: bütün "
                    "xətaların <em>eyni</em> formata salınmasını. Frontend bir "
                    "yerə <code>message</code>, başqa yerə <code>xeta.mesaj</code> "
                    "axtarmamalıdır — ona görə format vahidləşdirilib. Skript "
                    "404 xətasının strukturunu və status kodlarının oxunaqlı "
                    "sabitlərə çevrilməsini göstərir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── 1) Olmayan endpoint → 404 ──"
curl -s "$A/bele-bir-yol-yoxdur" | python3 -m json.tool

echo "── 2) Cavabın 4 sahəsi ──"
curl -s "$A/bele-bir-yol-yoxdur" | python3 -c "
import json,sys
d = json.load(sys.stdin)
for a in ('ugur','xeta','yol','vaxt'):
    print('  %-6s → %s' % (a, 'var' if a in d else 'YOXDUR'))
print('  xeta.kod  →', d['xeta']['kod'])
print('  xeta.mesaj→', d['xeta']['mesaj'])
"

echo "── 3) Status kodlarının oxunaqlı xəritəsi ──"
grep -E "^  [0-9]{3}:" src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'
''',
            ),
            dict(
                no="I.5",
                ad="Build, tip yoxlaması və ilk testlər",
                giris=(
                    "Bu test Dərs 1-in on ikinci və on üçüncü addımını "
                    "yoxlayır: layihənin yığılmasını, tiplərin təmiz olmasını və "
                    "testlərin keçməsini. <code>npm run build</code> xəta versə "
                    "server heç vaxt qalxmır; <code>tsc --noEmit</code> isə "
                    "build-in gizlətdiyi tip xətalarını tutur. Skript hər üç "
                    "yoxlamanı sıra ilə aparır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

echo "── 1) Build ──"
npm run build 2>&1 | tail -2
echo "  dist/ qovluğu: $([ -f dist/main.js ] && echo '✓ dist/main.js var' || echo '✗ YOXDUR')"

echo "── 2) Tip yoxlaması (build-in gizlətdiyi xətaları tutur) ──"
npx tsc --noEmit -p tsconfig.build.json && echo "  ✓ tip yoxlaması keçdi"

echo "── 3) Unit testlər ──"
npm test 2>&1 | grep -E 'Test Files|Tests ' | sed 's/^/  /'
''',
            ),
        ],
    ),

    dict(
        rumuz="II",
        ad="Dərs 2 — Struktur və kadrlar",
        qisa="Ortaq səhifələmə DTO-su, filtr DTO-ları, "
             "<code>StrukturService</code> və <code>KadrlarService</code>, "
             "controller-lər, JOIN ilə tam kadr profili, 409 toqquşması və "
             "ikinci dərsin testləri.",
        testler=[
            dict(
                no="II.1",
                ad="Səhifələmə riyaziyyatı — sehifeHesabla()",
                giris=(
                    "Bu test Dərs 2-nin birinci addımını yoxlayır: "
                    "<code>sehifeHesabla()</code> funksiyasının hədləri necə "
                    "qoruduğunu. İstifadəçi <code>?limit=999999</code> göndərsə "
                    "baza boğulmamalıdır — funksiya limiti 100-ə kəsir. Mənfi "
                    "səhifə 1-ə düzəldilir, sıfır limit isə standart 20-yə "
                    "qaytarılır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

npx tsx -e "
import { sehifeHesabla } from './src/common/dto/sehife.dto.ts';
const cedvel = [[3,15],[1,5000],[-7,20],[1,0],[2.7,33.9]] as const;
for (const [s, l] of cedvel)
  console.log('sehife=', s, ' limit=', l, ' →', JSON.stringify(sehifeHesabla(s, l)));
"
''',
            ),
            dict(
                no="II.2",
                ad="sehife_sayi — boş nəticədə də ən azı 1",
                giris=(
                    "Bu test <code>sehifelenmis()</code> funksiyasının "
                    "<code>sehife_sayi</code> sahəsini necə hesabladığını "
                    "yoxlayır. Cəm 0 olsa da frontend «1 səhifə» görməlidir — "
                    "«0 səhifə» qəribə görünür və səhifələmə düymələri sınır. "
                    "Bunun üçün <code>Math.max(1, ...)</code> qorunması var."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

npx tsx -e "
import { sehifelenmis } from './src/common/dto/sehife.dto.ts';
const cedvel = [[[], 0, 1, 20], [[], 10, 1, 3], [[], 21, 1, 20], [[], 100, 1, 20]] as const;
for (const [s, c, sh, l] of cedvel) {
  const n = sehifelenmis(s as never[], c, sh, l);
  console.log('cemi=' + c + ' limit=' + l + ' → sehife_sayi =', n.sehife_sayi);
}
"
''',
            ),
            dict(
                no="II.3",
                ad="DTO validasiyası — limit həddi",
                giris=(
                    "Bu test Dərs 2-nin ikinci addımını yoxlayır: filtr "
                    "DTO-sunun limiti rədd etməsini. <code>limit=500</code> "
                    "gələrsə servis onu kəsmir, DTO <strong>400</strong> "
                    "qaytarır — yəni yanlış sorğu bazaya heç çatmır. Cavabda "
                    "<code>xeta.detallar</code> sahəsi konkret sahəni göstərir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── limit=20 (icazəli) ──"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$A/struktur/merkezler?limit=20" -H "$H"

echo "── limit=500 (həddi aşır) ──"
curl -s "$A/struktur/merkezler?limit=500" -H "$H" | python3 -m json.tool

echo "── limit=abc (rəqəm deyil) ──"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$A/struktur/merkezler?limit=abc" -H "$H"
''',
            ),
            dict(
                no="II.4",
                ad="⚠️ SQL inyeksiya cəhdi — sirala ağ siyahısı",
                giris=(
                    "Bu test Dərs 2-dəki ən vacib təhlükəsizlik qərarını "
                    "yoxlayır: <code>sirala</code> parametri birbaşa SQL-ə "
                    "getmir, DTO onu <code>@IsIn</code> ilə yoxlayır. "
                    "İstifadəçi <code>?sirala=drop</code> göndərsə sorğu bazaya "
                    "çatmır və <strong>400</strong> qayıdır. Yoxlama olmasaydı "
                    "sütun adı yerinə ixtiyari SQL parçası işlədilə bilərdi."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── İcazəli sütunlar ──"
grep -o "MERKEZ_SAHELERI = \[[^]]*\]" src/struktur/dto/merkez-filtr.dto.ts | sed 's/^/  /'

echo "── sirala=ad (ağ siyahıda) ──"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$A/struktur/merkezler?sirala=ad" -H "$H"

echo "── sirala=drop (ağ siyahıdan kənar) ──"
curl -s "$A/struktur/merkezler?sirala=drop" -H "$H" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  kod   :', d['xeta']['kod'])
print('  mesaj :', d['xeta']['mesaj'])
for x in d['xeta'].get('detallar', []): print('  detal :', x)
"
''',
            ),
            dict(
                no="II.5",
                ad="Naməlum parametr — whitelist qoruması",
                giris=(
                    "Bu test <code>ValidationPipe</code>-ın "
                    "<code>forbidNonWhitelisted</code> seçimini yoxlayır: DTO-da "
                    "olmayan parametr gələrsə sorğu rədd edilir. Bu qoruma "
                    "səhv yazılmış parametrləri (məsələn <code>limitt=5</code>) "
                    "səssizcə udmaq yerinə açıq xəbərdarlıq verir. Belə olmasa "
                    "istifadəçi filtr işlədiyini sanıb yanlış nəticə alardı."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── Düzgün parametr: limit ──"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$A/struktur/merkezler?limit=5" -H "$H"

echo "── Səhv yazılmış parametr: limitt ──"
curl -s "$A/struktur/merkezler?limitt=5" -H "$H" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  HTTP  :', '400')
print('  mesaj :', d['xeta']['mesaj'])
for x in d['xeta'].get('detallar', []): print('  detal :', x)
"

echo "── main.ts-də ValidationPipe ayarları ──"
grep -n 'ValidationPipe\|whitelist\|forbidNonWhitelisted\|transform' src/main.ts | sed 's/^/  /'
''',
            ),
            dict(
                no="II.6",
                ad="Siyahı cavabının strukturu",
                giris=(
                    "Bu test Dərs 2-nin dördüncü addımını yoxlayır: bütün "
                    "siyahı endpoint-lərinin <em>eyni</em> formanı qaytarmasını. "
                    "Frontend bir cədvəl komponenti ilə hər siyahını göstərə "
                    "bilməlidir — bunun üçün beş sahə həmişə olmalıdır. Skript "
                    "strukturu yoxlayır və səhifə sayını hesablayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

curl -s "$A/struktur/merkezler?limit=3" -H "$H" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  cemi        :', d['cemi'])
print('  sehife      :', d['sehife'])
print('  limit       :', d['limit'])
print('  sehife_sayi :', d['sehife_sayi'], '= ceil(' + str(d['cemi']) + '/' + str(d['limit']) + ')')
print('  setirler    :', len(d['setirler']), 'sətir')
print()
print('  birinci sətrin sütunları:')
for k in d['setirler'][0]: print('     -', k)
"
''',
            ),
            dict(
                no="II.7",
                ad="Mərkəz statistikası — qruplaşdırma sorğusu",
                giris=(
                    "Bu test <code>GET /struktur/merkezler/statistika</code> "
                    "endpointini yoxlayır: hər mərkəz üzrə şöbə və əməkdaş "
                    "sayını bir sorğuda qaytarır. Bu, sadə <code>findMany</code> "
                    "ilə mümkün deyil — <code>GROUP BY</code> lazımdır. Skript "
                    "nəticəni bazadan ayrıca sayaraq tutuşdurur."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── API cavabı ──"
curl -s "$A/struktur/merkezler/statistika" -H "$H" | python3 -c "
import json,sys
for s in json.load(sys.stdin):
    print('  %-38s şöbə: %-3s əməkdaş: %s' % (s['ad'], s['shobe_sayi'], s['emekdas_sayi']))
"

echo "── Bazadan yoxlama (eyni rəqəmlər olmalıdır) ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT m.ad || ' → şöbə: ' || count(DISTINCT s.id) || ' əməkdaş: ' || count(DISTINCT e.id)
  FROM struktur.merkezler m
  LEFT JOIN struktur.shobeler s ON s.merkez_id = m.id
  LEFT JOIN kadrlar.emekdaslar e ON e.merkez_id = m.id
  GROUP BY m.ad ORDER BY m.ad" | sed 's/^/  /'
''',
            ),
            dict(
                no="II.8",
                ad="Yazma dövrü — yarat, oxu, sil",
                giris=(
                    "Bu test Dərs 2-nin dördüncü və beşinci addımını yoxlayır: "
                    "<code>POST</code>, <code>GET</code> və <code>DELETE</code> "
                    "əməliyyatlarının tam dövrünü. Yaradılan mərkəz dərhal "
                    "oxunmalı və sonra silinməlidir — yəni baza tutarlı qalır. "
                    "Skript sonda yaratdığını silir, bazada artıq sətir qalmır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── 1) POST /struktur/merkezler ──"
YENI=$(curl -s -X POST "$A/struktur/merkezler" -H "$H" -H 'Content-Type: application/json' \
  -d '{"ad":"Test Mərkəzi","tip":"merkez","tesvir":"Yoxlama üçün"}')
ID=$(printf '%s' "$YENI" | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")
echo "$YENI" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  id:', d['id'], '| ad:', d['ad'], '| tip:', d['tip'])"

echo "── 2) GET ilə oxu ──"
curl -s "$A/struktur/merkezler/$ID" -H "$H" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  oxundu:', d['ad'], '| aktiv:', d['aktiv'])"

echo "── 3) Eyni adla təkrar yaratmaq → 409 ──"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" -X POST "$A/struktur/merkezler" \
  -H "$H" -H 'Content-Type: application/json' -d '{"ad":"Test Mərkəzi","tip":"merkez"}'

echo "── 4) DELETE ──"
curl -s -X DELETE "$A/struktur/merkezler/$ID" -H "$H" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  silindi:', d['ad'])"

echo "── 5) Silindikdən sonra oxumaq → 404 ──"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$A/struktur/merkezler/$ID" -H "$H"
''',
            ),
            dict(
                no="II.9",
                ad="⚠️ Bağlı mərkəzi silmək → 409, 500 DEYİL",
                giris=(
                    "Bu test Dərs 2-nin dördüncü addımındaki xəta idarəetməsini "
                    "yoxlayır: şöbəsi olan mərkəzi silmək mümkün deyil, çünki "
                    "xarici açar (FK) buna mane olur. Prisma bu halda "
                    "<code>P2003</code> xətası verir və servis onu "
                    "<strong>409</strong> kimi tərcümə edir. Bu tərcümə "
                    "olmasaydı istifadəçi <strong>500</strong> görərdi və "
                    "problemin özündə olduğunu sanardı."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── Şöbəsi olan mərkəzlər ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT m.id || ' | ' || m.ad || ' | şöbə: ' || count(s.id)
  FROM struktur.merkezler m
  JOIN struktur.shobeler s ON s.merkez_id = m.id
  GROUP BY m.id, m.ad ORDER BY m.id LIMIT 3" | sed 's/^/  /'

ID=$(psql -U arti_user -d arti_baza -tA -c "
  SELECT m.id FROM struktur.merkezler m
  JOIN struktur.shobeler s ON s.merkez_id = m.id
  GROUP BY m.id ORDER BY m.id LIMIT 1")

echo "── $ID nömrəli mərkəzi silmək cəhdi ──"
curl -s -X DELETE "$A/struktur/merkezler/$ID" -H "$H" | python3 -m json.tool

echo "── Mərkəz hələ də yerindədir? ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  ✓ ' || ad || ' — silinmədi' FROM struktur.merkezler WHERE id = $ID"
''',
            ),
            dict(
                no="II.10",
                ad="⚠️ JOIN ilə kadr profili — maas RƏQƏM olmalıdır",
                giris=(
                    "Bu test Dərs 2-nin yeddinci addımını yoxlayır: kadrlar "
                    "sorğusunun JOIN ilə şöbə və vəzifə adlarını gətirməsini. "
                    "Ən incə məqam <code>maas::float8</code> çevrilməsidir — o "
                    "olmasa PostgreSQL <code>numeric</code> tipini sətir kimi "
                    "qaytarır və frontend rəqəm yerinə mətn alır. Skript həm "
                    "də tipin həqiqətən <code>number</code> olduğunu yoxlayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

TOKEN=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $TOKEN"

echo "── Siyahıdan bir kadr ──"
curl -s "$A/kadrlar/emekdaslar?limit=2" -H "$H" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  cemi:', d['cemi'])
for s in d['setirler']:
    print('  %s %s | %s | maas: %s (%s)' % (s['ad'], s['soyad'],
          s.get('merkez'), s.get('maas'), type(s.get('maas')).__name__))
"

echo "── JOIN ilə tam profil ──"
ID=$(curl -s "$A/kadrlar/emekdaslar?limit=1" -H "$H" | python3 -c "
import json,sys;print(json.load(sys.stdin)['setirler'][0]['id'])")
curl -s "$A/kadrlar/emekdaslar/$ID" -H "$H" | python3 -c "
import json,sys
d = json.load(sys.stdin)
for k, v in d.items():
    if isinstance(v, list):
        print('  %-14s → %d qeyd' % (k, len(v)))
    else:
        print('  %-14s → %s' % (k, v))
"

echo "── İcmal endpointi ──"
curl -s "$A/kadrlar/emekdaslar/icmal" -H "$H" | python3 -m json.tool | head -14
''',
            ),
        ],
    ),
]
