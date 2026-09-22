# -*- coding: utf-8 -*-
"""DƏRS 4 — yekun test skriptləri (IV.1–IV.30)."""

DERSLER = [
    dict(
        rumuz="IV",
        ad="Dərs 4 — AI qatı, ixrac və yerləşdirmə",
        qisa="<code>exceljs</code> və DeepSeek açarları, "
             "<code>EmbeddingService</code> və kosinus, <code>RagService</code>, "
             "resept ağ siyahısı, <code>DeepseekService</code> demo rejimi, "
             "AI endpoint-ləri, Excel ixracı, iştirakçı elektron pasportu, "
             "Docker və CI/CD.",
        testler=[
            dict(
                no="IV.1",
                ad="AI paketləri və demo rejim açarı",
                giris=(
                    "Bu test Dərs 4-ün birinci addımını yoxlayır: "
                    "<code>exceljs</code> paketinin quraşdırılmasını və "
                    "DeepSeek açarlarının <code>.env</code>-də olmasını. Ən "
                    "vacib məqam <code>DEEPSEEK_API_KEY</code>-in <strong>boş</strong> "
                    "olmasıdır — sistem açar olmadan da işləyir, sadəcə demo "
                    "rejimdə. Skript açarın boş olduğunu təsdiqləyir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── Paketlər ──"
for p in exceljs; do
  v=$(python3 -c "import json;print(json.load(open('node_modules/$p/package.json'))['version'])" 2>/dev/null)
  echo "  $p = ${v:-QURAŞDIRILMAYIB}"
done
python3 -c "
import json
d = json.load(open('package.json'))['dependencies']
print('  package.json-da exceljs:', d.get('exceljs', 'YOXDUR'))"

echo "── .env dəyişənləri ──"
for a in DEEPSEEK_API_KEY DEEPSEEK_MODEL DEEPSEEK_URL; do
  d=$(grep "^$a=" .env | sed "s/^$a=//; s/\"//g")
  if [ "$a" = "DEEPSEEK_API_KEY" ]; then
    echo "  $a → ${#d} simvol $([ -z "$d" ] && echo '(BOŞ → demo rejim)')"
  else
    echo "  $a → $d"
  fi
done

echo "── Demo rejim koda necə bağlanıb? ──"
grep -n 'demoRejim\|API_KEY' src/ai/deepseek.service.ts | head -5 | sed 's/^/  /'
''',
            ),
            dict(
                no="IV.2",
                ad="EmbeddingService — mətn 64 ölçülü vektora çevrilir",
                giris=(
                    "Bu test Dərs 4-ün ikinci addımını yoxlayır: mətnin "
                    "<strong>64 ölçülü</strong> vektora çevrilməsini və bunun "
                    "<em>deterministik</em> olmasını. Eyni mətn həmişə eyni "
                    "vektoru verməlidir, əks halda axtarış nəticələri hər "
                    "sorğuda dəyişərdi. Skript ölçünü və determinizmi yoxlayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

npx tsx -e "
import { EmbeddingService, OLCU } from './src/ai/embedding.service.ts';
const s = new EmbeddingService({} as any);
const a = s.vektor('Elmi Şura protokolu');
const b = s.vektor('Elmi Şura protokolu');
const c = s.vektor('idman yarışı');

console.log('OLCU sabiti        :', OLCU);
console.log('vektorun ölçüsü    :', a.length);
console.log('deterministik      :', JSON.stringify(a) === JSON.stringify(b));
console.log('fərqli mətn fərqli  :', JSON.stringify(a) !== JSON.stringify(c));
console.log();
console.log('vektorun ilk 8 elementi:');
console.log('  ', a.slice(0, 8).map((x: number) => x.toFixed(4)).join('  '));
console.log('sıfırdan fərqli element sayı:', a.filter((x: number) => x !== 0).length);
"
''',
            ),
            dict(
                no="IV.3",
                ad="⚠️ Normallaşdırma — kosinus 1-dən böyük olmamalıdır",
                giris=(
                    "Bu test Dərs 4-ün ikinci addımındaki normallaşdırmanı "
                    "yoxlayır. Vektor uzunluğu 1-ə çevrilməsəydi kosinus "
                    "<strong>5</strong> kimi mənasız rəqəmlər verərdi və bütün "
                    "sənədlər «çox oxşar» görünərdi. Skript vektorun uzunluğunu "
                    "hesablayır — 1.0 çıxmalıdır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

npx tsx -e "
import { EmbeddingService } from './src/ai/embedding.service.ts';
const s = new EmbeddingService({} as any);
const a = s.vektor('Elmi Şura protokolu haqqında sənəd');
const b = s.vektor('Elmi Şura protokolu haqqında sənəd');
const uzunluq = Math.sqrt(a.reduce((c: number, x: number) => c + x * x, 0));

console.log('vektorun uzunluğu  :', uzunluq.toFixed(6), '(≈ 1.0 olmalıdır)');
console.log('özü ilə kosinus    :', s.kosinus(a, b).toFixed(6), '(1.0-a çox yaxın)');
console.log();
console.log('⚠️ Normallaşdırma olmasaydı:');
const xam = a.map((x: number) => x * 10);
const xamUzunluq = Math.sqrt(xam.reduce((c: number, x: number) => c + x * x, 0));
console.log('  uzunluq        :', xamUzunluq.toFixed(4));
console.log('  kosinus        :', (xam.reduce((c: number, x: number, i: number) => c + x * xam[i]!, 0)).toFixed(4), '← 1-dən BÖYÜK!');
"
''',
            ),
            dict(
                no="IV.4",
                ad="Kosinus oxşarlığı — oxşar və fərqli mətn",
                giris=(
                    "Bu test oxşarlıq ölçüsünün mənalı işlədiyini yoxlayır: "
                    "oxşar mətnlər yüksək, tamamilə fərqli mətnlər isə sıfıra "
                    "yaxın bal almalıdır. Əgər bütün mətnlər eyni bal alsaydı, "
                    "axtarış faydasız olardı. Skript dörd müqayisə aparır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

npx tsx -e "
import { EmbeddingService } from './src/ai/embedding.service.ts';
const s = new EmbeddingService({} as any);
const v = (m: string) => s.vektor(m);
const c = (x: string, y: string) => s.kosinus(v(x), v(y)).toFixed(6);

console.log('eyni mətn              :', c('elmi şura iclası', 'elmi şura iclası'));
console.log('çox oxşar mətn         :', c('elmi şura iclası protokolu', 'elmi şura iclasının protokolu'));
console.log('qismən oxşar           :', c('elmi şura iclası', 'elmi jurnal nəşri'));
console.log('tamamilə fərqli         :', c('elmi şura iclası', 'idman yarışı nəticələri'));
console.log();
console.log('ballar 0..1 aralığındadır — müqayisə mənalıdır.');
"
''',
            ),
            dict(
                no="IV.5",
                ad="RAG axtarışı — azalan sıra və bal aralığı",
                giris=(
                    "Bu test Dərs 4-ün üçüncü addımını yoxlayır: "
                    "<code>RagService</code>-in sənədlər arasında axtarışını. "
                    "Nəticələr <strong>azalan</strong> sırada gəlməlidir — ən "
                    "oxşar sənəd birinci olmalıdır. Sıralama olmasaydı AI "
                    "kontekstə yanlış sənədləri qoyardı."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

curl -s -X POST "$A/ai/rag" -H "Authorization: Bearer $T" \
  -H 'Content-Type: application/json' \
  -d '{"sual":"elm və təhsil haqqında sənəd"}' | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  sual    :', d['sual'])
print('  tapıldı :', d['tapildi'])
print()
for n in d['neticeler']:
    print('  bal %.6f | sənəd #%s | %s' % (n['oxsarlıq'], n['sened_id'], n['metn'][:46]))
ballar = [n['oxsarlıq'] for n in d['neticeler']]
print()
print('  azalan sıra   :', ballar == sorted(ballar, reverse=True))
print('  hamısı > 0    :', all(b > 0 for b in ballar))
print('  hamısı ≤ 1    :', all(b <= 1 for b in ballar))
"
''',
            ),
            dict(
                no="IV.6",
                ad="RAG limiti — default 3, hədd 10",
                giris=(
                    "Bu test <code>RagDto</code>-daki <code>limit</code> "
                    "sahəsini yoxlayır: susmaya görə 3, ən azı 1, ən çoxu 10. "
                    "Hədd olmasaydı istifadəçi <code>limit=100000</code> "
                    "göndərib bütün bazanı oxuya bilərdi. Skript üç halı "
                    "yoxlayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"

yoxla() {
  printf '  %-26s → %s\n' "$1" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/ai/rag" -H "$H" \
        -H 'Content-Type: application/json' -d "$2")"
}

echo "── 1) Limit göstərilməyib (default 3) ──"
curl -s -X POST "$A/ai/rag" -H "$H" -H 'Content-Type: application/json' \
  -d '{"sual":"elm və təhsil haqqında"}' | python3 -c "
import json,sys; print('  tapıldı:', json.load(sys.stdin)['tapildi'])"

echo "── 2) limit=1 ──"
curl -s -X POST "$A/ai/rag" -H "$H" -H 'Content-Type: application/json' \
  -d '{"sual":"elm və təhsil haqqında","limit":1}' | python3 -c "
import json,sys; print('  tapıldı:', json.load(sys.stdin)['tapildi'])"

echo "── 3) Hədd yoxlaması ──"
yoxla "limit=10 (icazəli)"  '{"sual":"elm və təhsil","limit":10}'
yoxla "limit=11 (həddi aşır)" '{"sual":"elm və təhsil","limit":11}'
yoxla "limit=0 (mənfi hədd)" '{"sual":"elm və təhsil","limit":0}'
''',
            ),
            dict(
                no="IV.7",
                ad="Vektorlaşdırma — sənədlər bazaya yazılır",
                giris=(
                    "Bu test Dərs 4-ün üçüncü addımını yoxlayır: "
                    "<code>POST /ai/vektorlasdir</code> əməliyyatının sənədləri "
                    "oxuyub vektorlarını <code>ai.embeddingler</code> "
                    "cədvəlinə yazmasını. Yazma olmasaydı hər axtarış sıfırdan "
                    "hesablanardı və sistem çox yavaş olardı. Skript cədvəlin "
                    "sətir sayını əvvəl və sonra müqayisə edir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── Əvvəl ──"
psql -U arti_user -d arti_baza -tA -c \
  "SELECT '  ai.embeddingler: ' || count(*) || ' sətir' FROM ai.embeddingler"

echo "── POST /ai/vektorlasdir ──"
curl -s -X POST "$A/ai/vektorlasdir" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  baxılan sənəd:', d.get('baxildi'), '| yazılan:', d.get('yazildi'))"

echo "── Sonra ──"
psql -U arti_user -d arti_baza -tA -c \
  "SELECT '  ai.embeddingler: ' || count(*) || ' sətir' FROM ai.embeddingler"

echo "── Hansı cədvəllər vektorlaşdırılıb? ──"
psql -U arti_user -d arti_baza -c \
  "SELECT cedvel_adi, count(*) AS sayi, min(jsonb_array_length(vektor)) AS olcu
   FROM ai.embeddingler GROUP BY cedvel_adi" | sed 's/^/  /'
''',
            ),
            dict(
                no="IV.8",
                ad="AI statistikası — rejim, ölçü, resept sayı",
                giris=(
                    "Bu test Dərs 4-ün altıncı addımını yoxlayır: AI qatının "
                    "vəziyyətini bir endpoint-dən görməyi. Cavabda rejimin "
                    "<code>demo</code> olduğu, vektor ölçüsünün 64 olduğu və "
                    "10 reseptin mövcud olduğu görünməlidir. Bu, süni "
                    "intellektin işlədiyini yoxlamağın ən sürətli yoludur."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── GET /ai/statistika ──"
curl -s "$A/ai/statistika" -H "Authorization: Bearer $T" | python3 -m json.tool

echo "── Dörd rolun hamısı görə bilir? ──"
for rol in admin muhendis maliyyeci baxici; do
  RT=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  printf '  %-10s → %s\n' "$rol" "$(curl -s -o /dev/null -w '%{http_code}' "$A/ai/statistika" -H "Authorization: Bearer $RT")"
done
''',
            ),
            dict(
                no="IV.9",
                ad="⚠️ Resept ağ siyahısı və SIRA qaydası",
                giris=(
                    "Bu test Dərs 4-ün dördüncü addımını yoxlayır: 10 reseptin "
                    "mövcud olduğunu və <strong>sırasının</strong> düzgün "
                    "olduğunu. Xüsusi reseptlər ümumi olanlardan əvvəl "
                    "gəlməlidir — «orta maaş» sualı həm «orta maaş», həm "
                    "«maaş» açarına uyğun gəlir. Sıra pozulsa sistem səhv "
                    "cavab verər."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

curl -s "$A/ai/reseptler" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  resept sayı:', d['say'])
print()
for i, r in enumerate(d['reseptler'], 1):
    print('  %2d. %-22s ← %s' % (i, r['izah'], r['açar'][:46]))
print()
adlar = [r['izah'] for r in d['reseptler']]
o = adlar.index('Orta əmək haqqı')
u = adlar.index('Ən çox maaş alan 5 nəfər')
print('  «orta maaş» sırası :', o + 1)
print('  «ümumi maaş» sırası:', u + 1)
print('  ⚠️ xüsusi ümumidən ƏVVƏLdir:', o < u)
"
''',
            ),
            dict(
                no="IV.10",
                ad="Təbii dil — uyğun resept tapılır",
                giris=(
                    "Bu test Dərs 4-ün altıncı addımını yoxlayır: Azərbaycan "
                    "dilində yazılmış sualın düzgün reseptə bağlanmasını. "
                    "Sistem sualı açar sözlərlə tutuşdurur və yalnız uyğun "
                    "reseptin SQL-ini işlədir. Skript üç fərqli sualı sınayır "
                    "və nəticə cədvəlini göstərir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"

for s in "Neçə əməkdaş var?" "Mərkəzlər üzrə bölgü necədir?" "Şöbələrin sayı neçədir?"; do
  echo "── «$s» ──"
  curl -s -X POST "$A/ai/sual" -H "$H" -H 'Content-Type: application/json' \
    -d "{\"sual\":\"$s\"}" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  uygun_resept:', d['uygun_resept'])
print('  izah        :', d['izah'])
print('  sətir sayı  :', d['setir_sayi'])
if d['setirler']: print('  ilk sətir   :', json.dumps(d['setirler'][0], ensure_ascii=False)[:70])
"
done
''',
            ),
            dict(
                no="IV.11",
                ad="⚠️ «Orta maaş» testi — sıra səhvi qayıtmasın",
                giris=(
                    "Bu test Dərs 4-də tapılan real səhvi yoxlayır: «Orta maaş "
                    "nə qədərdir?» sualı əvvəllər <em>«Ən çox maaş alan 5 "
                    "nəfər»</em> reseptinə düşürdü, çünki ümumi resept xüsusidən "
                    "əvvəl yazılmışdı. Sistem xəta vermirdi — sadəcə səhv cavab "
                    "verirdi. Skript hər iki sualı sınayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"

for s in "Orta maaş nə qədərdir?" "Ən çox maaş alan kimdir?"; do
  echo "── «$s» ──"
  curl -s -X POST "$A/ai/sual" -H "$H" -H 'Content-Type: application/json' \
    -d "{\"sual\":\"$s\"}" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  izah  :', d['izah'])
print('  nəticə:', json.dumps(d['setirler'][:2], ensure_ascii=False))
"
done

echo "── ✅ «Orta maaş» XÜSUSİ reseptə düşməlidir, ümumi «maaş»-a YOX ──"
''',
            ),
            dict(
                no="IV.12",
                ad="Naməlum sual — 500 deyil, izahlı cavab",
                giris=(
                    "Bu test sistemin <em>yumşaq</em> uğursuzluğunu yoxlayır: "
                    "reseptə uyğun gəlməyən sual <strong>500</strong> yox, "
                    "<strong>200</strong> və izahlı cavab qaytarmalıdır. "
                    "İstifadəçi hansı sualların dəstəkləndiyini görməlidir. "
                    "Xəta versəydi istifadəçi sistemin sındığını sanardı."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"

CISIM='{"sual":"Banana qiyməti nə qədərdir?"}'
echo "── HTTP kodu ──"
printf '  %s (500 DEYİL)\n' "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/ai/sual" -H "$H" -H 'Content-Type: application/json' -d "$CISIM")"

echo "── Cavab ──"
curl -s -X POST "$A/ai/sual" -H "$H" -H 'Content-Type: application/json' -d "$CISIM" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  uygun_resept:', d['uygun_resept'])
print('  sətir sayı  :', d['setir_sayi'])
print('  izah (dəstəklənən suallar):')
for x in d['izah'].split('; '): print('     -', x)
"
''',
            ),
            dict(
                no="IV.13",
                ad="⚠️ SQL inyeksiya cəhdi — cədvəl SALAMAT qalır",
                giris=(
                    "Bu test Dərs 4-ün ən vacib təhlükəsizlik prinsipini "
                    "yoxlayır: <strong>LLM SQL yazmır</strong>, SQL koddadır. "
                    "Sual mətninin içində <code>DROP TABLE</code> olsa da, "
                    "işləyən SQL əvvəlcədən yazılmış reseptdir. Skript inyeksiya "
                    "göndərir və cədvəlin yerində qaldığını sübut edir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"

echo "── Əvvəl ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  struktur.merkezler: ' || (SELECT count(*) FROM struktur.merkezler)
      || ' | kadrlar.emekdaslar: ' || (SELECT count(*) FROM kadrlar.emekdaslar)"

echo "── İnyeksiya 1: reseptə UYĞUN gələn mətn ──"
curl -s -X POST "$A/ai/sual" -H "$H" -H 'Content-Type: application/json' \
  -d '{"sual":"mərkəz'"'"'; DROP TABLE struktur.merkezler; --"}' | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  uygun_resept:', d['uygun_resept'], '| izah:', d['izah'])
print('  → SQL koddan gəldi, sual mətnindən heç nə SQL-ə düşmədi')"

echo "── İnyeksiya 2: heç bir reseptə uyğun gəlmir ──"
curl -s -X POST "$A/ai/sual" -H "$H" -H 'Content-Type: application/json' \
  -d '{"sual":"'"'"'; DROP TABLE kadrlar.emekdaslar; --"}' | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  uygun_resept:', d['uygun_resept'], '| sətir sayı:', d['setir_sayi'])"

echo "── Sonra ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  struktur.merkezler: ' || (SELECT count(*) FROM struktur.merkezler)
      || ' | kadrlar.emekdaslar: ' || (SELECT count(*) FROM kadrlar.emekdaslar)"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  cədvəllər mövcuddur: ' || (to_regclass('struktur.merkezler') IS NOT NULL
      AND to_regclass('kadrlar.emekdaslar') IS NOT NULL)"
''',
            ),
            dict(
                no="IV.14",
                ad="AI DTO validasiyası — sualın uzunluğu",
                giris=(
                    "Bu test <code>SualDto</code>-nun sual uzunluğunu "
                    "yoxlamasını göstərir: ən azı 3, ən çoxu 500 simvol. "
                    "3 simvoldan qısa sual mənasızdır, 500-dən uzunu isə AI-ı "
                    "lazımsız yorur. Skript dörd halı sınayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"

UZUN=$(python3 -c "print('a' * 501)")

yoxla() {
  printf '  %-30s → %s\n' "$1" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/ai/sual" -H "$H" \
        -H 'Content-Type: application/json' -d "$2")"
}

yoxla "düzgün sual"          '{"sual":"Neçə əməkdaş var?"}'
yoxla "2 simvol"             '{"sual":"ab"}'
yoxla "boş sual"             '{"sual":""}'
yoxla "sual sahəsi yoxdur"   '{}'
yoxla "501 simvol"           "{\"sual\":\"$UZUN\"}"

echo "── DTO-da qaydalar ──"
grep -n 'MinLength\|MaxLength\|IsString' src/ai/dto/sual.dto.ts | sed 's/^/  /'
''',
            ),
            dict(
                no="IV.15",
                ad="RBAC — vektorlaşdırma yalnız admin və mühendis",
                giris=(
                    "Bu test Dərs 4-ün altıncı addımındaki rol qorumasını "
                    "yoxlayır: vektorlaşdırma ağır əməliyyatdır (10 sorğu + 10 "
                    "yazma), ona görə yalnız <code>admin</code> və "
                    "<code>muhendis</code> çağıra bilər. Skript dörd rolu "
                    "sınayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── POST /ai/vektorlasdir ──"
for rol in admin muhendis maliyyeci baxici; do
  T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  printf '  %-10s → %s\n' "$rol" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/ai/vektorlasdir" -H "Authorization: Bearer $T")"
done
printf '  %-10s → %s\n' "tokensiz" "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$A/ai/vektorlasdir")"

echo "── baxicinin aldığı cavab ──"
T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"baxici@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
curl -s -X POST "$A/ai/vektorlasdir" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  kod  :', d['xeta']['kod']); print('  mesaj:', d['xeta']['mesaj'])"
''',
            ),
            dict(
                no="IV.16",
                ad="Demo rejim — API açarı olmadan AI cavabı",
                giris=(
                    "Bu test Dərs 4-ün beşinci addımını yoxlayır: açar "
                    "olmadıqda sistemin <strong>sınmamasını</strong>. Cavabda "
                    "<code>demo: true</code> sahəsi olur ki, istifadəçi bunun "
                    "uydurma olduğunu bilsin. Demo rejim olmasaydı açar "
                    "qoyulmamış hər quraşdırma <em>fetch failed</em> verərdi."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── POST /ai/cavab ──"
curl -s -X POST "$A/ai/cavab" -H "Authorization: Bearer $T" \
  -H 'Content-Type: application/json' \
  -d '{"sual":"Elmi dərəcə ilə bağlı sənədlər hansılardır?"}' | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  demo               :', d['demo'], '← açar olmadığı üçün')
print('  model              :', d['model'])
print('  token_sayi         :', d['token_sayi'], '(demo rejimdə hesablanmır)')
print('  istifadə olunan sənəd:', d.get('istifade_olunan_senedler'))
print()
print('  cavab:')
for l in str(d['cavab']).splitlines()[:6]: print('   ', l)
"
''',
            ),
            dict(
                no="IV.17",
                ad="Excel ixracı — cavab başlıqları",
                giris=(
                    "Bu test Dərs 4-ün yeddinci addımını yoxlayır: "
                    "<code>.xlsx</code> faylının brauzerdə <em>yükləmə</em> kimi "
                    "davranmasını. Bunun üçün düzgün MIME tipi və "
                    "<code>attachment</code> başlığı lazımdır. Skript hər iki "
                    "başlığı yoxlayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── Cavab başlıqları ──"
curl -s -o /dev/null -D - "$A/ixrac/merkezler.xlsx" -H "Authorization: Bearer $T" \
  | grep -iE '^HTTP|content-type|content-disposition|content-length' | tr -d '\r' | sed 's/^/  /'

echo "── Dörd rolun hamısı yükləyə bilir? ──"
for rol in admin muhendis maliyyeci baxici; do
  RT=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  printf '  %-10s → %s\n' "$rol" "$(curl -s -o /dev/null -w '%{http_code}' "$A/ixrac/merkezler.xlsx" -H "Authorization: Bearer $RT")"
done
''',
            ),
            dict(
                no="IV.18",
                ad="⚠️ Fayl həqiqi Excel-dirmi? — PK baytları",
                giris=(
                    "Bu test faylın <code>.xlsx</code> adlanmağının kifayət "
                    "etmədiyini göstərir: həqiqi Excel faylı əslində ZIP "
                    "konteyneridir və <code>PK</code> (0x504B) baytları ilə "
                    "başlayır. Səhv import (<code>import * as ExcelJS</code>) "
                    "olsa fayl sıradan mətn olardı. Skript baytları və "
                    "<code>file</code> nəticəsini yoxlayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

curl -s -o /tmp/yoxla.xlsx "$A/ixrac/merkezler.xlsx" -H "Authorization: Bearer $T"

echo "── Bayt yoxlaması ──"
echo "  ilk 4 bayt (hex): $(xxd -p -l 4 /tmp/yoxla.xlsx)"
echo "  PK imzası       : $(xxd -p -l 2 /tmp/yoxla.xlsx | tr 'A-Z' 'a-z')  (504b olmalıdır)"

echo "── file əmri ──"
file -b /tmp/yoxla.xlsx | sed 's/^/  /'

echo "── ZIP içində nə var? ──"
unzip -l /tmp/yoxla.xlsx | head -8 | sed 's/^/  /'

echo "── Səhv import olsaydı nə olardı? ──"
grep -n "^import ExcelJS" src/ixrac/excel.service.ts | sed 's/^/  düzgün: /'
echo "  səhv  : import * as ExcelJS  →  ExcelJS.Workbook is not a constructor"
rm -f /tmp/yoxla.xlsx
''',
            ),
            dict(
                no="IV.19",
                ad="Excel sətir sayı = baza + başlıq",
                giris=(
                    "Bu test ixracın <em>tam</em> olduğunu yoxlayır: Excel-dəki "
                    "sətir sayı bazadakı sətir sayına bərabər olmalıdır, üstəgəl "
                    "bir başlıq sətri. Bu yoxlama olmasaydı ixrac səssizcə yarım "
                    "fayl verə bilərdi. Skript həm bazanı, həm faylı sayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

for cift in "merkezler:struktur.merkezler" "emekdaslar:kadrlar.emekdaslar"; do
  FAYL=$(echo "$cift" | cut -d: -f1); CEDVEL=$(echo "$cift" | cut -d: -f2)
  curl -s -o /tmp/yoxla.xlsx "$A/ixrac/$FAYL.xlsx" -H "Authorization: Bearer $T"
  DB=$(psql -U arti_user -d arti_baza -tA -c "SELECT count(*) FROM $CEDVEL" | tr -d ' ')
  XL=$(unzip -p /tmp/yoxla.xlsx xl/worksheets/sheet1.xml | grep -o '<row ' | wc -l | tr -d ' ')
  echo "── $FAYL ──"
  echo "  bazada      : $DB sətir"
  echo "  Excel-də    : $XL sətir (başlıq daxil)"
  echo "  gözlənilən  : $((DB + 1))  →  $([ "$XL" = "$((DB + 1))" ] && echo '✓ uyğundur' || echo '✗ UYĞUN DEYİL')"
  echo "  başlıq sətri: $(unzip -p /tmp/yoxla.xlsx xl/sharedStrings.xml 2>/dev/null | grep -o '<t>[^<]*</t>' | head -1 | sed 's/<[^>]*>//g')"
done
rm -f /tmp/yoxla.xlsx
''',
            ),
            dict(
                no="IV.20",
                ad="İki Excel faylı və ölçüləri",
                giris=(
                    "Bu test Dərs 4-ün yeddinci addımını tamamlayır: iki "
                    "endpointin də həqiqi fayl qaytarmasını. Fayllar "
                    "<strong>yaddaşda</strong> qurulur və diskdə heç nə "
                    "saxlanmır — paralel 100 istifadəçi yükləsə də disk "
                    "dolmur. Skript ölçüləri və fayl adlarını göstərir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── İki fayl ──"
for f in merkezler emekdaslar; do
  AD=$(curl -s -o /dev/null -D - "$A/ixrac/$f.xlsx" -H "Authorization: Bearer $T" \
    | grep -i 'content-disposition' | tr -d '\r' | sed 's/.*filename="//; s/"//')
  curl -s -o /tmp/yoxla.xlsx "$A/ixrac/$f.xlsx" -H "Authorization: Bearer $T"
  echo "  $f.xlsx → $(wc -c < /tmp/yoxla.xlsx | tr -d ' ') bayt | fayl adı: $AD"
done
rm -f /tmp/yoxla.xlsx

echo "── Server diskdə fayl saxlayırmı? ──"
echo "  /tmp-də artıq .xlsx: $(ls /tmp/*.xlsx 2>/dev/null | wc -l | tr -d ' ')"
echo "  layihədə: $(find . -name '*.xlsx' -not -path './node_modules/*' 2>/dev/null | wc -l | tr -d ' ')"
echo "  → fayl yalnız yaddaşda qurulur (Buffer), diskə yazılmır"

echo "── Content-Disposition necə qurulur? ──"
grep -n 'Content-Disposition\|attachment\|toISOString' src/ixrac/ixrac.controller.ts | sed 's/^/  /'
''',
            ),
            dict(
                no="IV.21",
                ad="Elektron pasport — hansı cədvəllər və hansı açar",
                giris=(
                    "Bu test Dərs 4-ün səkkizinci addımını başlayır: elektron "
                    "pasportun məlumatının <strong>dörd</strong> cədvəldən "
                    "yığıldığını göstərir. Bu cədvəlləri bağlayan açar "
                    "<code>sertifikat_no</code>-dur — ad üzrə bağlamaq "
                    "etibarsız olardı, çünki adlar təkrarlana bilər."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"

echo "── Pasportun mənbələri ──"
psql -U arti_user -d arti_baza -c "
  SELECT 'telim_istirakcilari' AS cedvel, count(*) AS setir FROM tehsil.telim_istirakcilari
  UNION ALL SELECT 'telim_qruplari',      count(*) FROM tehsil.telim_qruplari
  UNION ALL SELECT 'telim_proqramlari',   count(*) FROM tehsil.telim_proqramlari
  UNION ALL SELECT 'sertifikasiya',       count(*) FROM tehsil.sertifikasiya" | sed 's/^/  /'

echo "── Bağlayıcı açar: sertifikat_no ──"
psql -U arti_user -d arti_baza -c "
  SELECT i.ad || ' ' || i.soyad AS sahib, i.sertifikat_no,
         q.ad AS qrup, p.ad AS proqram, s.netice, s.bal
  FROM tehsil.telim_istirakcilari i
  LEFT JOIN tehsil.telim_qruplari    q ON q.id = i.qrup_id
  LEFT JOIN tehsil.telim_proqramlari p ON p.id = q.proqram_id
  LEFT JOIN tehsil.sertifikasiya     s ON s.sertifikat_no = i.sertifikat_no
  ORDER BY i.id LIMIT 5" | sed 's/^/  /'

echo "── Nə üçün ad üzrə deyil, NÖMRƏ üzrə? ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  eyni adlı sertifikasiya qeydi: ' || count(*)
  FROM (SELECT ad_soyad FROM tehsil.sertifikasiya GROUP BY ad_soyad HAVING count(*) > 1) x"
echo "  → ad təkrarlana bilər, sertifikat nömrəsi UNİKALdır"
''',
            ),
            dict(
                no="IV.22",
                ad="Pasportun oxunması — sahib, təlim, sertifikasiya",
                giris=(
                    "Bu test pasportun canlı oxunmasını yoxlayır: bir sorğuda "
                    "şəxsiyyət, təlim və imtahan nəticəsi birlikdə gəlir. Pasport "
                    "fayl kimi saxlanılmır — hər sorğuda dörd cədvəldən "
                    "<em>yenidən</em> qurulur. Skript üç bölmənin dolu olduğunu "
                    "yoxlayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── GET /tehsil/istirakciler/1/pasport ──"
curl -s "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  pasport_no  :', d['pasport_no'])
print('  etibarlidir :', d['etibarlidir'])
print()
print('  SAHİB       :', d['sahib']['tam_ad'], '| ata adı:', d['sahib']['ata_adi'])
print('  İŞ YERİ     :', d['sahib']['is_yeri'])
print('  TƏLİM       :', d['telim']['proqram'])
print('                qrup:', d['telim']['qrup'], '| saat:', d['telim']['saat'])
print('                müddət:', d['telim']['baslama_tarixi'], '→', d['telim']['bitme_tarixi'])
print('  SERTİFİKASİYA: nəticə', d['sertifikasiya']['netice'], '| bal', d['sertifikasiya']['bal'])
print('                imtahan:', d['sertifikasiya']['imtahan_tarixi'], '| tip:', d['sertifikasiya']['tip'])
"

echo "── Dörd rol oxuya bilir? ──"
for rol in admin muhendis maliyyeci baxici; do
  RT=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  printf '  %-10s → %s\n' "$rol" "$(curl -s -o /dev/null -w '%{http_code}' "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $RT")"
done
'''
            ),
            dict(
                no="IV.23",
                ad="Pasportun bütövlük hash-i",
                giris=(
                    "Bu test pasportun <strong>bütövlük barmaq izini</strong> "
                    "yoxlayır: FNV-1a ilə beş dəyişməz sahədən hesablanan hash. "
                    "İki çağırışda eyni olmalıdır, çünki dəyişən sahələr "
                    "(gecikmə, vaxt) hash-ə daxil edilmir. Bir hərf dəyişsə "
                    "hash tamam başqa olur."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

H1=$(curl -s "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; print(json.load(sys.stdin)['butovluk']['hash'])")
H2=$(curl -s "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; print(json.load(sys.stdin)['butovluk']['hash'])")
H3=$(curl -s "$A/tehsil/istirakciler/2/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; print(json.load(sys.stdin)['butovluk']['hash'])")

echo "  iştirakçı 1 → hash: $H1"
echo "  iştirakçı 1 → hash: $H2   (təkrar çağırış)"
echo "  iştirakçı 2 → hash: $H3   (başqa şəxs)"
echo
echo "  deterministik (H1 = H2)      : $([ "$H1" = "$H2" ] && echo '✓ BƏLİ' || echo '✗ XEYR')"
echo "  fərqli şəxs fərqli hash      : $([ "$H1" != "$H3" ] && echo '✓ BƏLİ' || echo '✗ XEYR')"
echo
echo "── Hash hansı sahələrdən hesablanır? ──"
curl -s "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; d=json.load(sys.stdin)['butovluk']
print('  alqoritm:', d['alqoritm'])
print('  sahələr :', ', '.join(d['saheler']))
"
''',
            ),
            dict(
                no="IV.24",
                ad="⚠️ Uyğunsuzluq aşkarlanır — kağızda sertifikat, imtahanda «qaldi»",
                giris=(
                    "Bu test pasportun ən dəyərli xüsusiyyətini — "
                    "<strong>uyğunsuzluğu tutmasını</strong> — yoxlayır. Real "
                    "bazada iştirakçı 3-ün sənədində sertifikat nömrəsi var, "
                    "amma <code>sertifikasiya</code> cədvəli «qaldi» göstərir. "
                    "Pasport bunu <code>etibarlidir: false</code> kimi qaytarır "
                    "və səbəbi yazır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── İştirakçı 3 ──"
curl -s "$A/tehsil/istirakciler/3/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print('  ad           :', d['sahib']['tam_ad'])
print('  pasport_no   :', d['pasport_no'], '← sənəddə nömrə VAR')
print('  etibarlidir  :', d['etibarlidir'], '← AMMA pasport ETİBARSIZDIR')
print('  uygunsuzluq  :', d['uygunsuzluq'])
s = d.get('sertifikasiya')
print('  sertifikasiya:', ('nəticə=' + str(s['netice']) + ' bal=' + str(s['bal'])) if s else 'yoxdur')
"

echo "── Etibarlı pasportla müqayisə (iştirakçı 1) ──"
curl -s "$A/tehsil/istirakciler/1/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  ad:', d['sahib']['tam_ad'], '| etibarlidir:', d['etibarlidir'], '| uygunsuzluq:', d['uygunsuzluq'])"
''',
            ),
            dict(
                no="IV.25",
                ad="Bütövlük hesabatı — statistika",
                giris=(
                    "Bu test uyğunsuzluqların <em>toplu</em> görünüşünü "
                    "yoxlayır: statistika endpointi neçə pasportun "
                    "təsdiqlənmədiyini bir rəqəmlə göstərir. Bu rəqəm olmasaydı "
                    "problem illərlə görünməz qalardı, çünki heç kim dörd "
                    "cədvəli əl ilə tutuşdurmur. Skript həm də keçid balını "
                    "yoxlayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

echo "── GET /tehsil/statistika ──"
curl -s "$A/tehsil/statistika" -H "Authorization: Bearer $T" | python3 -m json.tool

echo "── Uyğunsuz pasportların siyahısı ──"
for id in 1 2 3 4 5 6 7 8 9 10; do
  curl -s "$A/tehsil/istirakciler/$id/pasport" -H "Authorization: Bearer $T" | python3 -c "
import json,sys
d = json.load(sys.stdin)
if not d['etibarlidir']:
    print('  ✗ %-20s %-14s %s' % (d['sahib']['tam_ad'], d['pasport_no'], d['uygunsuzluq'][:52]))
"
done
''',
            ),
            dict(
                no="IV.26",
                ad="⚠️ Pasport necə ALINIR — tam dövr",
                giris=(
                    "Bu test Dərs 4-ün səkkizinci addımının əsas sualına cavab "
                    "verir: iştirakçı elektron pasportu <em>necə alır</em>. Üç "
                    "addım var — qrupa yazılma, imtahan balı ilə müraciət və "
                    "nömrənin verilməsi. Skript hər üç addımı icra edir və "
                    "sonda bazanı təmizləyir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"
ID=""
temizle() { [ -n "$ID" ] && curl -s -o /dev/null -X DELETE "$A/tehsil/istirakciler/$ID" -H "$H"; }
trap temizle EXIT

echo "── 1) Qrupa yazılır ──"
ID=$(curl -s -X POST "$A/tehsil/istirakciler" -H "$H" -H 'Content-Type: application/json' \
  -d '{"qrup_id":1,"ad":"Pasport","soyad":"Yoxlamasi","ata_adi":"Test","is_yeri":"Test məktəbi"}' \
  | python3 -c "
import json,sys; d=json.load(sys.stdin); print(d['id'])")
curl -s "$A/tehsil/istirakciler/$ID/pasport" -H "$H" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  id           :', d['sahib']['id'])
print('  status       :', d['sahib']['status'], '← hələ bitirməyib')
print('  pasport_no   :', d['pasport_no'], '← hələ YOXDUR')
print('  etibarlidir  :', d['etibarlidir'])
print('  səbəb        :', d['uygunsuzluq'])
"

echo "── 2) İmtahan balı ilə müraciət (bal = 72) ──"
curl -s -X POST "$A/tehsil/istirakciler/$ID/pasport" -H "$H" -H 'Content-Type: application/json' \
  -d '{"bal":72,"imtahan_tarixi":"2026-09-20","tip":"müəllim"}' | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  melumat      :', d['melumat'])
print('  pasport_no   :', d['pasport_no'])
print('  etibarlidir  :', d['etibarlidir'])
print('  netice       :', d['sertifikasiya']['netice'])
print('  hash         :', d['butovluk']['hash'])
"

echo "── 3) Nömrə bazada hara yazıldı? ──"
NO=$(curl -s "$A/tehsil/istirakciler/$ID/pasport" -H "$H" | python3 -c "
import json,sys; print(json.load(sys.stdin)['pasport_no'])")
psql -U arti_user -d arti_baza -c "
  SELECT 'telim_istirakcilari' AS cedvel, sertifikat_no, status
  FROM tehsil.telim_istirakcilari WHERE id = $ID
  UNION ALL
  SELECT 'sertifikasiya', sertifikat_no, netice
  FROM tehsil.sertifikasiya WHERE sertifikat_no = '$NO'" | sed 's/^/  /'
''',
            ),
            dict(
                no="IV.27",
                ad="⚠️ Bal 60-dan aşağıdırsa pasport VERİLMİR",
                giris=(
                    "Bu test keçid həddinin işlədiyini yoxlayır: bal 60-dan "
                    "aşağıdırsa nəticə «qaldi» yazılır və sertifikat nömrəsi "
                    "<strong>NULL</strong> qalır. Kağız üzərində sertifikat "
                    "verilsəydi, imtahandan keçməyən şəxs onu işəgötürənə "
                    "göstərə bilərdi. Skript iki balı müqayisə edir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"
ID=""
temizle() { [ -n "$ID" ] && curl -s -o /dev/null -X DELETE "$A/tehsil/istirakciler/$ID" -H "$H"; }
trap temizle EXIT

ID=$(curl -s -X POST "$A/tehsil/istirakciler" -H "$H" -H 'Content-Type: application/json' \
  -d '{"qrup_id":1,"ad":"Kesilen","soyad":"Namized","ata_adi":"Test"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")

for bal in 40 60 100; do
  echo "── bal = $bal ──"
  curl -s -X POST "$A/tehsil/istirakciler/$ID/pasport" -H "$H" \
    -H 'Content-Type: application/json' -d "{\"bal\":$bal}" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  nəticə     :', d['sertifikasiya']['netice'])
print('  pasport_no :', d['pasport_no'])
print('  etibarlidir:', d['etibarlidir'])
print('  melumat    :', d['melumat'])
"
  # Növbəti bal üçün pasportu sıfırlayırıq
  psql -U arti_user -d arti_baza -q -c "
    DELETE FROM tehsil.sertifikasiya WHERE ad_soyad = 'Kesilen Namized';
    UPDATE tehsil.telim_istirakcilari SET sertifikat_no = NULL
     WHERE id = $ID"
done
''',
            ),
            dict(
                no="IV.28",
                ad="⚠️ Təkrar müraciət — idempotentlik",
                giris=(
                    "Bu test eyni endpointin ikinci dəfə çağırılmasını yoxlayır: "
                    "yeni nömrə <em>yaradılmamalıdır</em>, mövcud nömrə "
                    "qaytarılmalıdır. İdempotentlik olmasaydı bir iştirakçının "
                    "iki sertifikatı olardı və hansının həqiqi olduğu "
                    "bilinməzdi. Skript bazadakı sətir sayını da yoxlayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

T=$(curl -s -X POST "$A/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
H="Authorization: Bearer $T"
ID=""
temizle() { [ -n "$ID" ] && curl -s -o /dev/null -X DELETE "$A/tehsil/istirakciler/$ID" -H "$H"; }
trap temizle EXIT

ID=$(curl -s -X POST "$A/tehsil/istirakciler" -H "$H" -H 'Content-Type: application/json' \
  -d '{"qrup_id":1,"ad":"Idempotent","soyad":"Yoxlama","ata_adi":"Test"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")

echo "── 1-ci müraciət (bal 70) ──"
NO1=$(curl -s -X POST "$A/tehsil/istirakciler/$ID/pasport" -H "$H" \
  -H 'Content-Type: application/json' -d '{"bal":70}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['pasport_no'])")
echo "  nömrə: $NO1"

echo "── 2-ci müraciət (bal 95) ──"
CVB=$(curl -s -X POST "$A/tehsil/istirakciler/$ID/pasport" -H "$H" \
  -H 'Content-Type: application/json' -d '{"bal":95}')
NO2=$(printf '%s' "$CVB" | python3 -c "import json,sys; print(json.load(sys.stdin)['pasport_no'])")
printf '%s' "$CVB" | python3 -c "
import json,sys; d=json.load(sys.stdin); print('  nömrə:', d['pasport_no']); print('  melumat:', d['melumat'])"

echo "── 3-cü müraciət (bal 30) ──"
NO3=$(curl -s -X POST "$A/tehsil/istirakciler/$ID/pasport" -H "$H" \
  -H 'Content-Type: application/json' -d '{"bal":30}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['pasport_no'])")
echo "  nömrə: $NO3"

echo "── Yoxlama ──"
echo "  üç müraciətdə eyni nömrə : $([ "$NO1" = "$NO2" ] && [ "$NO2" = "$NO3" ] && echo '✓ BƏLİ' || echo '✗ XEYR')"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  bazada bu nömrədən neçə sətir: ' || count(*)
  FROM tehsil.sertifikasiya WHERE sertifikat_no = '$NO1'"
''',
            ),
            dict(
                no="IV.29",
                ad="İctimai yoxlama — tokensiz və minimum məlumat",
                giris=(
                    "Bu test pasportun <em>kənara göstərilməsini</em> yoxlayır: "
                    "sertifikatı işəgötürən yoxlayır və onun sistemə istifadəçi "
                    "olması lazım deyil. Bu endpoint qəsdən minimum məlumat "
                    "verir — ata adı və iş yeri kimi şəxsi sahələr qaytarılmır. "
                    "Skript tokensiz çağırışı və məlumat həddini yoxlayır."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
A="${A:-http://localhost:4000/api/v1}"

kod=$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)
[ "$kod" = "200" ] || { echo "⚠️ Server işləmir — PORT=4000 npm run start:prod"; exit 1; }

echo "── TOKENSİZ çağırış ──"
printf '  HTTP %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/tehsil/pasport/SER-2024-001/yoxla")"

echo "── Cavab ──"
curl -s "$A/tehsil/pasport/SER-2024-001/yoxla" | python3 -m json.tool

echo "── Məlumat həddi yoxlaması ──"
curl -s "$A/tehsil/pasport/SER-2024-001/yoxla" | python3 -c "
import json,sys
d = json.load(sys.stdin)
for sahə in ('sahib', 'is_yeri', 'ata_adi'):
    print('  %-10s cavabda: %s' % (sahə, 'VAR ⚠️' if sahə in json.dumps(d) else 'yoxdur ✓'))
print()
print('  etibarlidir :', d['etibarlidir'])
print('  ad_soyad    :', d['ad_soyad'])
print('  hash        :', d['butovluk_hash'])
"

echo "── Olmayan nömrə → 404 ──"
printf '  HTTP %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/tehsil/pasport/XXX-0000-000/yoxla")"
''',
            ),
            dict(
                no="IV.30",
                ad="Docker və CI/CD — yerləşdirmə hazırlığı",
                giris=(
                    "Bu test Dərs 4-ün doqquzuncu addımını yoxlayır: layihənin "
                    "başqa kompüterdə də işləməsi üçün Docker quruluşunu və "
                    "GitHub Actions axınını. <code>Dockerfile</code> iki "
                    "mərhələlidir ki, obraz kiçik olsun; CI isə postgres-i "
                    "sağlamlıq yoxlaması ilə gözləyir. Skript hər faylın "
                    "vəzifəsini göstərir."
                ),
                skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST

echo "── Fayllar ──"
for f in Dockerfile .dockerignore docker-compose.yml .github/workflows/ci.yml; do
  [ -f "$f" ] && echo "  ✓ $f" || echo "  ✗ $f YOXDUR"
done

echo "── Dockerfile mərhələləri ──"
grep -nE '^FROM|^COPY --from|^USER|^EXPOSE|^CMD' Dockerfile | sed 's/^/  /'

echo "── docker-compose xidmətləri ──"
grep -nE '^  [a-z-]+:|image:|depends_on|healthcheck' docker-compose.yml | sed 's/^/  /'

echo "── CI addımları ──"
grep -nE 'image:|options:|run:' .github/workflows/ci.yml | sed 's/^/  /'

echo "── CI niyə postgres-i GÖZLƏYİR? ──"
grep -n -B2 'pg_isready' .github/workflows/ci.yml | sed 's/^/  /'
echo "  → health check olmasa testlər ECONNREFUSED alır"
''',
            ),
        ],
    ),
]
