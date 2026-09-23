# -*- coding: utf-8 -*-
"""DS_Backend-1A — 10 yekun test (IA.1 – IA.10).

Hər test: nömrə, başlıq, 3-4 cümlə giriş və Terminal-da işlədilə bilən skript.
Skriptlər BACKEND qovluğundan və canlı API-dən asılıdır.
"""

TESTLER = [
    dict(
        no="IA.1",
        ad="Layihə skeleti və konfiqurasiya faylları",
        giris="""Bu test Dərs 1A-nın birinci addımını yoxlayır: layihə
        qovluğunun və onun üçün lazım olan konfiqurasiya fayllarının yerində
        olub-olmadığını. Bu fayllardan biri düşsə, sonrakı heç bir addım
        işləmir — build də, server də. Skript həm Node alətlərinin versiyasını,
        həm də hər faylın mövcudluğunu göstərir.""",
        skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || {
  echo "⚠️ Layihə qovluğu tapılmadı."; exit 1; }

echo "── Alətlər ──"
echo "  node  : $(node -v)"
echo "  npm   : $(npm -v)"

echo
echo "── Konfiqurasiya faylları ──"
for f in package.json tsconfig.json tsconfig.build.json nest-cli.json \
         .env .gitignore prisma/schema.prisma prisma.config.ts; do
  if [ -f "$f" ]; then
    printf '  ✓ %-26s %4s sətir\n' "$f" "$(wc -l < "$f" | tr -d ' ')"
  else
    printf '  ✗ %-26s YOXDUR\n' "$f"
  fi
done

echo
echo "── Qovluq strukturu ──"
find . -type f -not -path './node_modules/*' -not -path './src/generated/*' \
       -not -path './dist/*' | sort | sed 's/^/  /'
''',
    ),
    dict(
        no="IA.2",
        ad="package.json — skriptlər və asılılıqlar",
        giris="""Bu test Dərs 1A-nın ikinci addımını yoxlayır: layihənin
        manifestinin düzgün qurulub-qurulmadığını. <code>package.json</code>
        olmasa npm heç bir əmri işlədə bilmir. Skript həm skriptləri, həm
        asılılıqları, həm də paketlərin həqiqətən quraşdırıldığını yoxlayır.""",
        skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1

echo "── Layihə ──"
python3 -c "
import json
d = json.load(open('package.json'))
print('  ad        :', d['name'])
print('  versiya   :', d['version'])
print('  modul tipi:', d.get('type', 'commonjs'))
"

echo
echo "── Skriptlər ──"
python3 -c "
import json
for k, v in json.load(open('package.json'))['scripts'].items():
    print('  npm run %-14s → %s' % (k, v))
"

echo
echo "── Asılılıqlar ──"
python3 -c "
import json
d = json.load(open('package.json'))
print('  istehsalat (dependencies)   :', len(d.get('dependencies', {})))
print('  inkişaf    (devDependencies):', len(d.get('devDependencies', {})))
"

echo
echo "── Quraşdırılıbmı? ──"
if [ -d node_modules ]; then
  echo "  ✓ node_modules: $(ls node_modules | wc -l | tr -d ' ') paket"
else
  echo "  ✗ node_modules YOXDUR — «npm install» işlədin"
fi
''',
    ),
    dict(
        no="IA.3",
        ad="TypeScript ayarları — decorator və NodeNext",
        giris="""Bu test Dərs 1A-nın üçüncü addımını yoxlayır: TypeScript-in
        NestJS üçün lazım olan ayarlarını. <code>experimentalDecorators</code>
        və <code>emitDecoratorMetadata</code> sönsə, NestJS-in
        <code>@İşarə</code>-ləri tanınmır və heç bir modul işləmir. Skript
        həm də <code>.js</code> uzantı qaydasını yoxlayır.""",
        skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1

echo "── TypeScript-in gördüyü YEKUN ayarlar ──"
npx tsc --showConfig 2>/dev/null | python3 -c "
import json, sys
o = json.load(sys.stdin)['compilerOptions']
for a in ['target', 'module', 'moduleResolution', 'strict',
          'experimentalDecorators', 'emitDecoratorMetadata',
          'outDir', 'rootDir', 'esModuleInterop']:
    print('  %-24s %s' % (a, o.get(a, '—')))
"

echo
echo "── NestJS ayarları ──"
python3 -c "
import json
d = json.load(open('nest-cli.json'))
c = d.get('compilerOptions', {})
print('  sourceRoot   :', d.get('sourceRoot'))
print('  deleteOutDir :', c.get('deleteOutDir'))
"

echo
echo "── Import-larda «.js» uzantısı varmı? ──"
echo "  (yalnız NİSBİ importlar: './' və ya '../' ilə başlayanlar."
echo "   Paket importlarında — @nestjs/common, supertest — .js YAZILMIR."
echo "   Prisma-nın yaratdığı src/generated/ qovluğu sayılmır.)"
python3 - <<'PSON'
import pathlib
import re
import sys

say = 0
problem = []
for fayl in sorted(pathlib.Path('src').rglob('*.ts')):
    if 'generated' in fayl.parts:
        continue
    for n, setir in enumerate(fayl.read_text(encoding='utf-8').splitlines(), 1):
        s = setir.strip()
        if not (s.startswith('import') or s.startswith('export')):
            continue
        if s.startswith('//') or s.startswith('*') or s.startswith('/*'):
            continue
        for tam in re.findall(r"from\s+'\.[^']*'", s):
            yol = tam[len('from '):].strip().strip("'")
            if yol.endswith('.js'):
                say += 1
            else:
                problem.append('%s:%d → %s' % (fayl, n, yol))

print('  .js ilə     : %d' % say)
print('  .js OLMADAN : %d   ← 0 olmalıdır' % len(problem))
for x in problem:
    print('      ✗ ' + x)
if problem:
    print('  ✗ NİSBİ importda .js uzantısı ÇATIŞMIR!')
    sys.exit(1)
print('  ✓ bütün nisbi importlarda .js uzantısı var')
PSON
''',
    ),
    dict(
        no="IA.4",
        ad=".env — sirr koddan ayrılıb və qorunur",
        giris="""Bu test Dərs 1A-nın dördüncü addımını yoxlayır: baza şifrəsinin
        koda yazılmadığını və git-ə düşmədiyini. Şifrə koda yazılsa, onu görən
        hər kəs bazaya girə bilər. Skript şifrənin özünü <em>çap etmir</em> —
        yalnız onun təhlükəsiz saxlandığını təsdiqləyir.""",
        skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1
unset DATABASE_URL PGHOST

echo "── .env dəyişənləri (şifrələr gizlədilir) ──"
python3 -c "
import pathlib
for x in pathlib.Path('.env').read_text().splitlines():
    if not x.strip() or x.startswith('#'):
        continue
    a, _, d = x.partition('=')
    d = d.strip('\"')
    if any(k in a for k in ('URL', 'SECRET', 'PASSWORD', 'KEY')):
        print('  %-18s %s' % (a, '•' * 20))
    else:
        print('  %-18s %s' % (a, d))
"

echo
echo "── DATABASE_URL hissələri ──"
python3 -c "
import re, pathlib
m = re.search(r'DATABASE_URL=\"([^\"]+)\"', pathlib.Path('.env').read_text())
u = m.group(1)
sxem, _, qalan = u.partition('://')
kimlik, _, host = qalan.partition('@')
ist, _, sifre = kimlik.partition(':')
host, _, baza = host.partition('/')
print('  protokol   :', sxem)
print('  istifadəçi :', ist)
print('  şifrə      :', '•' * len(sifre), '(%d simvol)' % len(sifre))
print('  host:port  :', host)
print('  baza adı   :', baza)
"

echo
echo "── .gitignore nəyi qoruyur? ──"
grep -v '^#' .gitignore | grep -v '^$' | sed 's/^/  /'

echo
echo "── Şifrə koda yazılıbmı? ──"
if grep -rn 'arti_secret' src/ --include=*.ts 2>/dev/null; then
  echo "  ✗ ŞİFRƏ KODA YAZILIB!"
else
  echo "  ✓ şifrə koda yazılmayıb — yalnız .env-dədir"
fi

echo
echo "── Kod .env-i adı ilə oxuyurmu? ──"
grep -rn "DATABASE_URL" src/prisma/prisma.service.ts | sed 's/^/  /'
''',
    ),
    dict(
        no="IA.5",
        ad="Prisma sxeması və klientin generasiyası",
        giris="""Bu test Dərs 1A-nın beşinci addımını yoxlayır: bazanın
        oxunub TypeScript tiplərinə çevrilməsini. <code>schemas</code> sətri
        bir sətirdə olmasa Prisma <code>P1012</code> xətası verir. Skript həm
        sxemanın etibarlılığını, həm də yaradılan klientin mövcudluğunu
        yoxlayır.""",
        skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

echo "── Sxemanın əsas blokları ──"
grep -nE '^(generator|datasource)|^  (provider|output|url|schemas)' \
  prisma/schema.prisma | head -8 | sed 's/^/  /'

echo
echo "── Bazadan nə oxundu? ──"
echo "  model sayı : $(grep -c '^model ' prisma/schema.prisma)"
echo "  @@schema    : $(grep -c '@@schema' prisma/schema.prisma)"
echo "  sətir sayı : $(wc -l < prisma/schema.prisma | tr -d ' ')"

echo
echo "── İlk model nümunə ──"
sed -n '/^model merkezler /,/^}/p' prisma/schema.prisma | head -12 | sed 's/^/  /'

echo
echo "── Sxema etibarlıdırmı? ──"
npx prisma validate 2>&1 | tail -2 | sed 's/^/  /'

echo
echo "── Yaradılan TypeScript klienti ──"
if [ -f src/generated/prisma/client.ts ]; then
  echo "  ✓ client.ts var ($(ls src/generated/prisma | wc -l | tr -d ' ') fayl)"
else
  echo "  ✗ client.ts YOXDUR — «npx prisma generate» işlədin"
fi
''',
    ),
    dict(
        no="IA.6",
        ad="PrismaService — baza bağlantısı işləyir",
        giris="""Bu test Dərs 1A-nın altıncı addımını yoxlayır: baza
        bağlantısının həqiqətən qurulduğunu. Serveri qaldırmadan servisi
        birbaşa işlədirik — beləliklə problem serverdədir, yoxsa bazadadır,
        dərhal bilirik. Prisma 7-də adapter məcburi olduğu üçün bu yoxlama
        xüsusilə vacibdir.""",
        skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

echo "── PrismaService faylı ──"
ls -l src/prisma/prisma.service.ts | sed 's/^/  /'

echo
echo "── Baza bağlantısını BİRBAŞA sınayırıq ──"
npx tsx -e "
import 'dotenv/config';
import { PrismaService } from './src/prisma/prisma.service.ts';
void (async () => {
  const s = new PrismaService({ get: () => process.env.DATABASE_URL } as never);
  await s.onModuleInit();
  const n = await s.yoxla();
  console.log('  bağlantı    : quruldu');
  console.log('  cədvəl sayı :', n.cedvelSayi);
  console.log('  gecikmə     :', n.gecikmeMs, 'ms');
  await s.onModuleDestroy();
  console.log('  bağlantı düzgün bağlandı');
})();
"

echo
echo "── Adapter istifadə olunurmu? ──"
grep -nE 'PrismaPg|adapter|connectionString' src/prisma/prisma.service.ts | sed 's/^/  /'
''',
    ),
    dict(
        no="IA.7",
        ad="PrismaModule — @Global() və exports",
        giris="""Bu test Dərs 1A-nın yeddinci addımını yoxlayır: baza
        bağlantısının bütün layihəyə açıq olmasını. <code>@Global()</code> və
        <code>exports</code> sətirlərindən biri unudulsa, servislər
        <code>PrismaService</code>-i tapa bilmir və server belə xəta ilə
        qalxmır: <em>Nest can't resolve dependencies</em>. Skript hər iki
        sətri yoxlayır.""",
        skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1

echo "── Modulun tam məzmunu ──"
cat -n src/prisma/prisma.module.ts | sed 's/^/  /'

echo
echo "── Yoxlamalar ──"
for yox in '@Global()' 'providers' 'exports'; do
  n=$(grep -c "$yox" src/prisma/prisma.module.ts)
  [ "$n" -gt 0 ] && printf '  ✓ %-12s var\n' "$yox" || printf '  ✗ %-12s YOXDUR\n' "$yox"
done

echo
echo "── Başqa modul PrismaService-i istəyirmi? ──"
grep -rn 'PrismaService' src/ --include=*.service.ts | grep constructor | sed 's/^/  /'

echo
echo "── Kök modula qoşulubmu? ──"
if [ -f src/app.module.ts ]; then
  grep -n 'PrismaModule' src/app.module.ts | sed 's/^/  /'
else
  echo "  (app.module.ts hələ yoxdur — IA.9-a baxın)"
fi
''',
    ),
    dict(
        no="IA.8",
        ad="AllExceptionsFilter — vahid xəta formatı",
        giris="""Bu test Dərs 1A-nın səkkizinci addımını yoxlayır: bütün
        xətaların eyni formata salınmasını. Filter olmasa, hər endpoint fərqli
        format qaytarır və frontend hər dəfə «bu dəfə hansı format gəldi?» deyə
        yoxlamağa məcbur qalır. Skript status-kod xəritəsini və cavabın dörd
        sahəsini yoxlayır.""",
        skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1

echo "── Fayl ──"
ls -l src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'

echo
echo "── Status → kod xəritəsi ──"
grep -E '^  [0-9]{3}:' src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'

echo
echo "── Cavabın quruluşu (koddan) ──"
grep -A9 'cavab.status(status).json' src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'

echo
echo "── Gözlənilməz xəta loqa yazılırmı? ──"
grep -n 'log.error' src/common/filters/all-exceptions.filter.ts | sed 's/^/  /'

echo
echo "── Filter qlobal qoşulubmu? ──"
grep -n 'useGlobalFilters' src/main.ts 2>/dev/null | sed 's/^/  /' \
  || echo "  (main.ts hələ yoxdur — IA.10-a baxın)"
''',
    ),
    dict(
        no="IA.9",
        ad="Sağlamlıq modulu — ilk endpoint məntiqi",
        giris="""Bu test Dərs 1A-nın doqquzuncu addımını yoxlayır: sağlamlıq
        yoxlamasının bazaya <em>həqiqi</em> sorğu göndərdiyini. Sadəcə
        «işləyirəm» desəydi, baza kəsiləndə də yaşıl işıq yanardı və problem
        gizli qalardı. Skript servisi birbaşa işlədib cavabı göstərir.""",
        skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

echo "── Modulun hissələri ──"
ls -1 src/saglamliq/ | sed 's/^/  /'

echo
echo "── Endpoint-lər ──"
grep -nE '@(Get|Post|Controller)' src/saglamliq/saglamliq.controller.ts | sed 's/^/  /'

echo
echo "── Kök modula qoşulubmu? ──"
grep -c 'SaglamliqModule' src/app.module.ts 2>/dev/null | sed 's/^/  sayı: /'

echo
echo "── Sağlamlıq yoxlaması (birbaşa) ──"
npx tsx -e "
import 'dotenv/config';
import { PrismaService } from './src/prisma/prisma.service.ts';
import { SaglamliqService } from './src/saglamliq/saglamliq.service.ts';
void (async () => {
  const p = new PrismaService({ get: () => process.env.DATABASE_URL } as never);
  await p.onModuleInit();
  const c = await new SaglamliqService(p).yoxla();
  console.log('  status      :', c.status);
  console.log('  qoşulub     :', c.baza.qosulub);
  console.log('  cədvəl sayı :', c.baza.cedvel_sayi);
  console.log('  gecikmə     :', c.baza.gecikme_ms, 'ms');
  console.log('  versiya     :', c.versiya);
  await p.onModuleDestroy();
})();
"
''',
    ),
    dict(
        no="IA.10",
        ad="Server qalxır — prefiks, marşrutlar, Swagger",
        giris="""Bu test Dərs 1A-nın on birinci addımını yoxlayır: serverin
        həqiqətən qalxdığını və dörd vacib şeyin işlədiyini. Serveri özü
        qaldırır, dörd yoxlama aparır və sonda dayandırır — yəni tam
        avtomatikdir. Gözlənilən nəticə: prefiks <code>/api/v1</code>, iki
        marşrut, vahid xəta formatı və açıq Swagger.""",
        skript=r'''
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache
A="${A:-http://localhost:4000/api/v1}"
PORT="${PORT:-4000}"

echo "── Build ──"
npm run build 2>&1 | tail -2 | sed 's/^/  /'
[ -f dist/main.js ] || { echo "  ✗ dist/main.js yoxdur"; exit 1; }

echo
echo "── Köhnə proses təmizlənir ──"
lsof -ti:$PORT 2>/dev/null | xargs -r kill 2>/dev/null
sleep 1

echo "── Server qalxır (port $PORT) ──"
PORT=$PORT nohup npm run start:prod > /tmp/ders1a_ia10.log 2>&1 &
for i in $(seq 1 30); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' "$A/saglamliq" 2>/dev/null)" = "200" ] && break
  sleep 1
done

echo "  Marşrutlar:"
grep 'Mapped' /tmp/ders1a_ia10.log | sed 's/.*Mapped //' | sed 's/^/    /'

echo
echo "── 1) Kök ünvan ──"
curl -s "$A" | python3 -m json.tool | sed 's/^/  /'

echo
echo "── 2) Sağlamlıq ──"
curl -s "$A/saglamliq" | python3 -m json.tool | sed 's/^/  /'

echo
echo "── 3) Olmayan yol → vahid xəta formatı ──"
curl -s "$A/bele-yol-yoxdur" | python3 -m json.tool | sed 's/^/  /'

echo
echo "── 4) Swagger ──"
kok="${A%/api/v1}"
echo "  $kok/docs      → HTTP $(curl -s -o /dev/null -w '%{http_code}' "$kok/docs")"
echo "  $kok/docs-json → HTTP $(curl -s -o /dev/null -w '%{http_code}' "$kok/docs-json")"

echo
echo "── Server dayandırılır ──"
lsof -ti:$PORT 2>/dev/null | xargs -r kill 2>/dev/null
echo "  ✓ dayandırıldı"
''',
    ),
]
