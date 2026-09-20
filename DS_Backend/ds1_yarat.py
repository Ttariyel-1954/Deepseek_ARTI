#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-1.html dərsini yaradır — A / B / C / D formatında.

Hər addım 4 hissədən ibarətdir:
  A — bu addım nəyə görədir (3-4 cümlə)
  B — addıma aid kodun özü
  C — kodun yazıldığını yoxlayın + bu kod olmasa nə olardı
  D — bu koddan sonra sistemin tam durumu (real çıxışlarla)

B hissəsindəki kodlar DS_Backend/ qovluğundan CANLI oxunur —
dərsdəki kod həmişə real faylla eyni olur.

İSTİFADƏ:
    python3 DS_Backend/ds1_yarat.py
"""
from __future__ import annotations

import html
import pathlib

KOK = pathlib.Path(__file__).resolve().parent.parent
BACKEND = KOK / "DS_Backend"
CIXIS = KOK / "DƏRSLƏR" / "DS_Backend-1.html"
CSS_FAYLI = KOK / "DS_Baza" / "ders.css"


def e(metn: str) -> str:
    """HTML üçün təhlükəsiz hala gətirir."""
    return html.escape(str(metn), quote=False)


def fayl(yol: str) -> str:
    """DS_Backend/ içindən real faylı oxuyur."""
    p = BACKEND / yol
    if not p.exists():
        raise SystemExit(f"XƏTA: fayl tapılmadı: {p}")
    return p.read_text(encoding="utf-8").rstrip("\n")


# ══════════════════════════════════════════════════════════════════
#  ƏLAVƏ CSS — A/B/C/D hissələri üçün
# ══════════════════════════════════════════════════════════════════
ELAVE_CSS = """
  /* ─── ADDIM BLOKU (A/B/C/D) ─── */
  .addim {
    border: 2px solid #e2e8f0; border-radius: 18px;
    padding: 0 0 1rem; margin: 2.6rem 0;
    background: #fff; overflow: hidden;
  }
  .addim-basliq {
    font-size: 1.45rem; font-weight: 800; color: #fff;
    background: linear-gradient(135deg, #7c2d12, #ea580c);
    padding: 1.1rem 1.5rem; margin: 0 0 1.2rem;
    display: flex; align-items: center; gap: .9rem; line-height: 1.3;
  }
  .addim-no {
    display: inline-flex; align-items: center; justify-content: center;
    background: rgba(255,255,255,.22); color: #fff;
    min-width: 44px; height: 44px; border-radius: 12px;
    font-weight: 800; font-size: 1.05rem; flex-shrink: 0;
  }
  .addim-govde { padding: 0 1.4rem; }

  .hisse {
    border-radius: 12px; padding: 1.1rem 1.4rem;
    margin: 1rem 0; border-left: 6px solid;
  }
  .hisse-a { background: #eff6ff; border-color: #2563eb; }
  .hisse-b { background: #f8fafc; border-color: #0f172a; }
  .hisse-c { background: #fffbeb; border-color: #d97706; }
  .hisse-d { background: #f5f3ff; border-color: #7c3aed; }
  .hisse-basliq {
    display: block; font-weight: 800; font-size: .78rem;
    letter-spacing: 1.6px; text-transform: uppercase;
    margin-bottom: .75rem;
  }
  .hisse-a .hisse-basliq { color: #1d4ed8; }
  .hisse-b .hisse-basliq { color: #0f172a; }
  .hisse-c .hisse-basliq { color: #b45309; }
  .hisse-d .hisse-basliq { color: #6d28d9; }
  .hisse p:last-child { margin-bottom: 0; }
  .hisse h4 {
    font-size: .95rem; font-weight: 700; color: #334155;
    margin: 1rem 0 .5rem;
  }
  .fayl-ad {
    display: inline-block; background: #1e293b; color: #7dd3fc;
    font-family: 'SF Mono', Menlo, Consolas, monospace;
    font-size: .74rem; font-weight: 600;
    padding: .28rem .85rem; border-radius: 6px; margin: .3rem 0 .4rem;
  }
  .olmaz {
    background: #fef2f2; border: 2px dashed #dc2626;
    border-radius: 10px; padding: .9rem 1.2rem; margin: 1rem 0 0;
  }
  .olmaz-basliq {
    display: block; font-weight: 800; font-size: .78rem;
    color: #b91c1c; letter-spacing: 1.2px; margin-bottom: .55rem;
  }
  .oldu {
    background: #f0fdf4; border: 2px solid #16a34a;
    border-radius: 10px; padding: .9rem 1.2rem; margin: 1rem 0 0;
  }
  .oldu-basliq {
    display: block; font-weight: 800; font-size: .78rem;
    color: #15803d; letter-spacing: 1.2px; margin-bottom: .55rem;
  }
  .addim-icmal {
    display: flex; gap: .5rem; flex-wrap: wrap;
    padding: .9rem 1.4rem 0; font-size: .78rem;
  }
  .addim-icmal span {
    background: #f1f5f9; color: #475569; padding: .3rem .8rem;
    border-radius: 20px; font-weight: 700;
  }
  .icmal {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: .8rem; margin: 1.4rem 0;
  }
  .icmal a {
    display: block; background: #fff7ed; border: 2px solid #fed7aa;
    border-radius: 12px; padding: .85rem 1rem; text-decoration: none;
    color: #9a3412; font-weight: 700; font-size: .86rem;
    transition: .15s;
  }
  .icmal a:hover { background: #ffedd5; border-color: #ea580c; }
  .icmal a b { display: block; font-size: .7rem; color: #ea580c; letter-spacing: 1px; }
"""


# ══════════════════════════════════════════════════════════════════
#  ADDIM MƏLUMATLARI
# ══════════════════════════════════════════════════════════════════
ADDIMLAR: list[dict] = []


def addim(n, ad, a, b, c_yoxla, c_olmaz, c_izah, d, d_izah):
    ADDIMLAR.append(dict(
        n=n, ad=ad, a=a, b=b, c_yoxla=c_yoxla,
        c_olmaz=c_olmaz, c_izah=c_izah, d=d, d_izah=d_izah,
    ))


# ──────────────────────────────────────────────────────────────────
addim(
    n=1,
    ad="Layihə qovluğu və skelet",
    a="""NestJS layihəsi müəyyən qovluq strukturunu gözləyir: <code>src/</code> mənbə kodu,
    <code>test/</code> testlər, <code>prisma/</code> isə baza sxemi üçündür. Bu strukturu
    əvvəlcədən yaratmasaq, sonrakı addımlarda fayllar səpələnmiş halda qalar və
    <code>nest build</code> hansı faylı haradan götürəcəyini bilməz. Biz
    <code>nest new</code> əmrini işlətmirik, çünki o, layihə adını kiçik hərflərə çevirir
    (<code>DS_Backend</code> → <code>ds_backend</code>) və onlarla lazımsız fayl yaradır.
    Qovluqları əl ilə yaradırıq ki, hər faylın nəyə görə olduğunu dəqiq bilək.""",
    b=[("Terminal — qovluq strukturu", """cd ~/Deepseek_ARTI

mkdir -p DS_Backend/src/prisma
mkdir -p DS_Backend/src/common/filters
mkdir -p DS_Backend/src/saglamliq
mkdir -p DS_Backend/prisma
mkdir -p DS_Backend/test""")],
    c_yoxla="""cd ~/Deepseek_ARTI

# Bütün qovluqlar yarandımı?
# (node_modules və dist hələ yoxdur, amma sonra işlətsəniz siyahını
#  doldurmasın deyə onları əvvəlcədən kənarlaşdırırıq)
find DS_Backend -type d \\
  -not -path '*/node_modules*' -not -path '*/dist*' \\
  -not -path '*/generated*' -not -path '*/.git*' | sort

# Hər biri ayrıca yoxlanılsın
for d in src src/prisma src/common/filters src/saglamliq prisma test; do
  [ -d "DS_Backend/$d" ] && echo "✓ $d" || echo "✗ $d YOXDUR"
done""",
    c_olmaz="""$ cd ~/Deepseek_ARTI/DS_Backend
$ npx prisma db pull

Error: Could not load `prisma/schema.prisma`: file or directory not found""",
    c_izah="""<code>prisma/</code> qovluğu olmasa sxem faylını ora qoymaq mümkün olmaz və
    <code>db pull</code> dərhal xəta verir. <code>src/</code> olmasa isə <code>nest build</code>
    ümumiyyətlə kompilyasiya etməyə fayl tapmaz — boş <code>dist/</code> yaranar.""",
    d="""$ find DS_Backend -type d \\
    -not -path '*/node_modules*' -not -path '*/dist*' \\
  -not -path '*/generated*' -not -path '*/.git*' | sort

DS_Backend
DS_Backend/prisma
DS_Backend/src
DS_Backend/src/common
DS_Backend/src/common/filters
DS_Backend/src/prisma
DS_Backend/src/saglamliq
DS_Backend/test""",
    d_izah="""8 qovluq yarandı. Hər birinin vəzifəsi fərqlidir:
    <ul>
      <li><code>src/</code> — bütün TypeScript mənbə kodu. <code>nest build</code> yalnız bura baxır.</li>
      <li><code>src/prisma/</code> — baza bağlantısı (<code>PrismaService</code>, <code>PrismaModule</code>).</li>
      <li><code>src/common/filters/</code> — bütün layihə üçün ümumi olan şeylər (xəta filtri).</li>
      <li><code>src/saglamliq/</code> — ilk funksional modul: sağlamlıq yoxlaması.</li>
      <li><code>prisma/</code> — <code>schema.prisma</code> faylı. Bu qovluq <code>src/</code>-dən
          kənardadır, çünki o, TypeScript deyil, Prisma dilindədir.</li>
      <li><code>test/</code> — e2e testlər. Ayrı qovluqdadır ki, <code>nest build</code> onları
          istehsalat yığımına salmasın.</li>
    </ul>""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=2,
    ad="package.json və asılılıqlar",
    a="""<code>package.json</code> layihənin şəxsiyyət vəsiqəsidir — adı, versiyası, əmrləri
    və asılılıqları burada yazılır. <code>npm install</code> yalnız bu faylı oxuyub
    <code>node_modules/</code> qovluğunu yaradır. Biz asılılıqları əl ilə, dəqiq
    siyahı ilə yazırıq ki, hansı paketin <em>niyə</em> lazım olduğunu bilək;
    <code>nest new</code> isə onlarla istifadə etmədiyimiz paket də qoşur.""",
    b=[("package.json", fayl("package.json"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayl düzgün JSON-dur?
python3 -m json.tool package.json > /dev/null && echo "✓ JSON düzgündür"

# 2) node_modules yarandımı və neçə paket var?
ls node_modules | wc -l

# 3) Əsas paketlər yerindədirmi?
for p in @nestjs/core @nestjs/config @prisma/client @prisma/adapter-pg prisma pg; do
  [ -d "node_modules/$p" ] && echo "✓ $p" || echo "✗ $p YOXDUR"
done""",
    c_olmaz="""$ cd /tmp/bosh_qovluq && npm install

npm error code ENOENT
npm error syscall open
npm error path /private/tmp/bosh_qovluq/package.json
npm error errno -2
npm error enoent Could not read package.json""",
    c_izah="""<code>package.json</code> olmadan <code>npm install</code> nə quraşdıracağını
    bilmir — dərhal <code>ENOENT</code> xətası verir. Versiyaları
    <code>^</code> ilə yazmaq da vacibdir: <code>^12.0.1</code> "<em>12.0.1 və ya daha yeni
    12.x</em>" deməkdir, yəni yamaq yeniləmələri avtomatik gəlir, amma 13-cü versiya
    özü-özünə gəlmir.""",
    d="""$ ls node_modules | wc -l
430

$ for p in @nestjs/core @nestjs/config @nestjs/swagger @prisma/client \\
           @prisma/adapter-pg prisma typescript vitest pg class-validator; do
    v=$(python3 -c "import json;print(json.load(open('node_modules/$p/package.json'))['version'])")
    printf '%-24s %s\\n' "$p" "$v"
  done

@nestjs/core             12.0.3
@nestjs/config           12.0.0
@nestjs/swagger          12.0.1
@prisma/client           7.10.0
@prisma/adapter-pg       7.10.0
prisma                   7.10.0
typescript               6.0.3
vitest                   4.1.11
pg                       8.23.0
class-validator          0.14.4""",
    d_izah="""430 paket quraşdırıldı. Bizim <code>package.json</code>-da 13 birbaşa asılılıq
    var, qalanı onların öz asılılıqlarıdır. Diqqət yetirin: <code>@prisma/adapter-pg</code>
    Prisma 7-nin tələbidir — bu paket olmasa <code>PrismaClient</code> ümumiyyətlə
    yaradıla bilmir (6-cı addımda bunu canlı görəcəyik).""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=3,
    ad="TypeScript konfiqurasiyası",
    a="""NestJS dekoratorlarla işləyir (<code>@Module</code>, <code>@Controller</code>,
    <code>@Get</code>), TypeScript isə onları yalnız <code>experimentalDecorators</code>
    açıq olduqda kompilyasiya edir. <code>moduleResolution: nodenext</code> bizi
    <code>import ... from './x.js'</code> yazmağa məcbur edir — bu, Node ESM-in tələbidir
    və <code>.js</code> uzantısı unudulsa kod işə düşmür. <code>nest-cli.json</code> isə
    <code>nest build</code> əmrinə mənbə qovluğunun <code>src</code> olduğunu deyir.""",
    b=[
        ("tsconfig.json", fayl("tsconfig.json")),
        ("tsconfig.build.json", fayl("tsconfig.build.json")),
        ("nest-cli.json", fayl("nest-cli.json")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# TypeScript-in HƏQİQƏTƏN istifadə etdiyi ayarlar
npx tsc --showConfig -p tsconfig.build.json | python3 -c "
import json, sys
d = json.load(sys.stdin)['compilerOptions']
for a in ['module','moduleResolution','target','experimentalDecorators',
          'emitDecoratorMetadata','strict','outDir','rootDir']:
    print(f'  {a:26s} {d.get(a)}')
"

# nest-cli mənbə qovluğunu tanıyırmı?
python3 -c "
import json
d = json.load(open('nest-cli.json'))
print('  sourceRoot:', d.get('sourceRoot'))
" """,
    c_olmaz="""$ npm run build

src/saglamliq/saglamliq.controller.ts:11:3 - error TS1241:
  Unable to resolve signature of method decorator when called as an expression.
  The runtime will invoke the decorator with 2 arguments,
  but the decorator expects 3.

src/saglamliq/saglamliq.controller.ts:11:4 - error TS1270:
  Decorator function return type 'void | TypedPropertyDescriptor<unknown>'
  is not assignable to type 'void | (() => { ... })'.""",
    c_izah="""<code>experimentalDecorators</code> söndürülsə TypeScript <code>@Get</code>-i
    adi funksiya kimi qəbul edir və <strong>TS1241 / TS1270</strong> xətaları verir.
    Build uğursuz olur, <code>dist/</code> qovluğu isə <strong>heç yaranmır</strong> —
    yəni <code>node dist/main.js</code> "fayl tapılmadı" deyəcək. <code>emitDecoratorMetadata</code>
    də vacibdir: NestJS məhz onun yazdığı <code>__metadata</code> məlumatına baxaraq
    hansı servisi hara ötürəcəyini anlayır.""",
    d="""$ npx tsc --showConfig -p tsconfig.build.json

  module                     nodenext
  moduleResolution           nodenext
  target                     ES2023
  experimentalDecorators     True
  emitDecoratorMetadata      True
  strict                     True
  outDir                     ./dist
  rootDir                    ./src""",
    d_izah="""Diqqət yetirin: <code>tsconfig.build.json</code> əsas fayldan miras alır və
    yalnız iki şeyi dəyişir — <code>rootDir</code> və <code>include</code>. Buna görə
    yuxarıdaki bütün ayarlar (dekoratorlar, strict, target) oradan gəlir.
    <code>rootDir: ./src</code> olmasa <code>dist/</code> daxilində
    <code>dist/src/main.js</code> kimi artıq qovluq yaranar və
    <code>node dist/main.js</code> işləməz.""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=4,
    ad=".env — baza açarı koddan ayrılır",
    a="""Baza parolu və port kimi məlumatlar koda <strong>yazılmamalıdır</strong> — onlar
    git-ə düşər və reponu görən hər kəs baza parolunu oxuyar. <code>.env</code> faylı
    bu dəyərləri koddan ayırır, <code>.gitignore</code> isə onun git-ə düşməsinin
    qarşısını alır. <code>dotenv</code> paketi faylı oxuyub dəyərləri
    <code>process.env</code>-ə yerləşdirir ki, kod onlara adi dəyişən kimi çatsın.""",
    b=[
        (".env", fayl(".env")),
        (".env.example", fayl(".env.example")),
        (".gitignore", fayl(".gitignore")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) .env git tərəfindən İGNORE olunurmu?
git check-ignore -v .env

# 2) İçində nə var? (diqqət: parolu ekrana çıxarır)
grep DATABASE_URL .env

# 3) Node bu dəyəri görürmü?
node -e "import('dotenv/config').then(() => {
  const u = process.env.DATABASE_URL || '';
  console.log('  DATABASE_URL oxundu :', u ? 'BƏLİ' : 'XEYR');
  console.log('  uzunluq             :', u.length, 'simvol');
  console.log('  baza adı            :', u.split('/').pop());
})"
""",
    c_olmaz="""$ DATABASE_URL= PORT=4102 node dist/main.js

[Nest] ERROR [ExceptionHandler] Error: DATABASE_URL təyin olunmayıb
  — .env faylını yoxlayın""",
    c_izah="""<code>PrismaService</code> konstruktorunda bu yoxlama var və server
    <strong>heç qalxmır</strong>. Bu, qəsdən belədir: səhv bağlantı ilə işləyib
    yanlış bazaya yazmaqdansa, dərhal dayanmaq daha yaxşıdır. Əgər <code>.env</code>
    <code>.gitignore</code>-da olmasa, parol GitHub-a düşər və onu tarixçədən
    təmizləmək çox çətin olar.""",
    d="""$ git check-ignore -v .env
.gitignore:1:.env	.env

$ node -e "..."      # dotenv ilə oxuma
  DATABASE_URL oxundu : BƏLİ
  uzunluq             : 61 simvol
  baza adı            : arti_baza

$ git status --short
?? .env.example
?? .gitignore
   (diqqət: .env siyahıda YOXDUR — git onu görmür)""",
    d_izah="""Sistemin vəziyyəti: <code>.env</code> faylı mövcuddur, oxunur və
    <code>process.env.DATABASE_URL</code> dəyəri <code>arti_baza</code>-nı göstərir.
    Eyni zamanda git onu <strong>görmür</strong> — <code>git status</code> siyahısında
    yoxdur. <code>.env.example</code> isə əksinə, git-ə düşür: başqa kompüterdə
    layihəni açan şəxs ona baxıb öz <code>.env</code>-ini yaradır.
    <code>.env.*</code> sətrindən sonra gələn <code>!.env.example</code>
    istisna qaydasıdır — ulduz işarəsi onu da udmasın deyə.""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=5,
    ad="Prisma sxeması — bazanı oxuyub tipləri çıxarmaq",
    a="""<code>arti_baza</code> artıq mövcuddur: 12 sxem, 48 cədvəl. Biz cədvəlləri
    TypeScript-də əl ilə təsvir etmirik — Prisma <code>db pull</code> əmri ilə bazanı
    oxuyub sxemi özü çıxarır. Sonra <code>generate</code> bu sxemdən
    <strong>tip-təhlükəsiz</strong> TypeScript müştərisini yaradır. Beləliklə kodda
    <code>prisma.merkezler.findMany()</code> yaza bilirik və səhv sütun adı dərhal
    kompilyasiyada tutulur, serverdə yox.""",
    b=[
        ("prisma/schema.prisma — datasource və generator", fayl("prisma/schema.prisma").split("\n\n")[0]),
        ("prisma.config.ts", fayl("prisma.config.ts")),
        ("Terminal — sxemi çıxar və müştərini yarat", """cd ~/Deepseek_ARTI/DS_Backend

# Bazanı oxu və sxemi doldur
npx prisma db pull

# Sxemdən TypeScript müştərisini yarat
npx prisma generate"""),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Sxem etibarlıdırmı?
npx prisma validate

# 2) Neçə model çıxarıldı?
grep -c '^model ' prisma/schema.prisma

# 3) Müştəri yarandımı?
ls src/generated/prisma/client.ts

# 4) Nümunə model — struktur.merkezler
sed -n '/^model merkezler /,/^}/p' prisma/schema.prisma""",
    c_olmaz="""$ npx prisma validate      # 'schemas' sətri BÖLÜNSƏ:

Error: Prisma schema validation - (validate wasm)
Error code: P1012
error: Error validating: This line is not a valid definition within a datasource.
  -->  prisma/schema.prisma:8
 7 |   provider = "postgresql"
 8 |   schemas  = [
 9 |     "ai", "audit", "elm", "kadrlar", "logistika", "maliyye",""",
    c_izah="""<code>schemas</code> siyahısı <strong>mütləq bir sətirdə</strong> olmalıdır —
    Prisma çoxsətirli massivi bu yerdə qəbul etmir və <code>P1012</code> verir.
    Sxem faylı heç olmasa <code>db pull</code> "file or directory not found" deyəcək.
    Müştəri yaradılmasa isə <code>import { PrismaClient } from
    '../generated/prisma/client.js'</code> sətri <code>TS2307: Cannot find module</code>
    xətası verəcək və build ümumiyyətlə keçməyəcək.""",
    d="""$ npx prisma db pull
✔ Introspected 12 models and wrote them into prisma/schema.prisma
  ... (48 model)

$ npx prisma generate
✔ Generated Prisma Client (7.10.0) to ./src/generated/prisma in 98ms

$ grep -c '^model ' prisma/schema.prisma
48

$ find src/generated -type f | wc -l
56
$ du -sh src/generated
3.4M

$ sed -n '/^model merkezler /,/^}/p' prisma/schema.prisma
model merkezler {
  id               Int       @id @default(autoincrement())
  ad               String
  tip              String?   @default("merkez")
  ...
  @@schema("struktur")
}""",
    d_izah="""Sistemin vəziyyəti: Prisma artıq bazanı <strong>tanıyır</strong>. 48 cədvəl
    TypeScript tipinə çevrildi və <code>src/generated/prisma/</code> qovluğunda 56 fayl
    (3.4 MB) yarandı. Bu qovluq <code>.gitignore</code>-dadır — onu git-ə salmırıq,
    çünki hər kəs öz kompüterində <code>npx prisma generate</code> ilə yenidən yarada bilər.
    <code>@@schema("struktur")</code> sətri modelin hansı PostgreSQL sxemində olduğunu göstərir —
    Prisma 7-də çoxsxemli baza üçün bu MÜTLƏQİDİR.""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=6,
    ad="PrismaService — baza bağlantısı",
    a="""Prisma müştərisi birbaşa <code>new PrismaClient()</code> ilə yaradıla bilməz:
    Prisma 7-də <em>driver adapter</em> mütləqdir. <code>PrismaService</code> bu
    bağlantını NestJS-in həyat dövrünə bağlayır — server qalxanda
    <code>$connect()</code>, sönəndə <code>$disconnect()</code> çağırılır.
    Əlavə olaraq <code>yoxla()</code> metodu var ki, sağlamlıq endpoint-i bazanın
    həqiqətən cavab verdiyini yoxlaya bilsin.""",
    b=[("src/prisma/prisma.service.ts", fayl("src/prisma/prisma.service.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# Adapter, həyat dövrü və yoxlama metodu yerindədirmi?
grep -n 'PrismaPg\\|super({\\|onModuleInit\\|onModuleDestroy\\|DATABASE_URL' \\
  src/prisma/prisma.service.ts

# Sadəcə bu fayl kompilyasiya olunurmu?
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi\"""",
    c_olmaz="""$ node dist/main.js      # adapter sətri silinsə:

[Nest] ERROR [ExceptionHandler] PrismaClientInitializationError:
PrismaClient was instantiated without any options.
A driver adapter is required to connect to your database.
Pass a driver adapter to the PrismaClient constructor, for example:
  import { PrismaPg } from '@prisma/adapter-pg'
  const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL })
  const prisma = new PrismaClient({ adapter })""",
    c_izah="""Prisma 7-dən əvvəl müştəri bazaya özü qoşulurdu; indi bu işi
    <code>pg</code> paketi görür və Prisma yalnız onun üstündə işləyir. Adapter
    olmadan <code>PrismaClient</code> <strong>ümumiyyətlə yaradılmır</strong> və
    server qalxmır. <code>onModuleInit</code> olmasa isə bağlantı yalnız ilk sorğuda
    açılar — yəni problem server qalxanda yox, istifadəçi ilk dəfə sorğu göndərəndə
    üzə çıxar, bu isə tapmağı çətinləşdirir.""",
    d="""$ node dist/main.js

[Nest] LOG [InstanceLoader] PrismaModule dependencies initialized +0ms
[Nest] LOG [BAZA] Baza bağlantısı açıldı
[Nest] LOG [NestApplication] Nest application successfully started +0ms

# yoxla() metodu real bazaya sorğu göndərir:
$ psql -U arti_user -w -d arti_baza -tAc \\
    "SELECT count(*)::int FROM information_schema.tables
      WHERE table_type='BASE TABLE'
        AND table_schema NOT IN ('pg_catalog','information_schema')"
48""",
    d_izah="""Sistemin vəziyyəti: server qalxanda <code>[BAZA] Baza bağlantısı açıldı</code>
    mesajı çıxır — bu o deməkdir ki, <code>$connect()</code> uğurla keçdi və
    PostgreSQL həqiqətən cavab verir. <code>yoxla()</code> metodundaki
    <code>::int</code> çevirməsi çox vacibdir: PostgreSQL <code>count(*)</code> üçün
    <code>bigint</code> qaytarır, JavaScript isə <code>BigInt</code>-i JSON-a çevirə
    bilmir və <em>Do not know how to serialize a BigInt</em> xətası verər.""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=7,
    ad="PrismaModule — @Global() ilə paylaşılan bağlantı",
    a="""Bundan sonra hər modul <code>PrismaService</code>-i işlədəcək. Onu hər modulun
    <code>providers</code> siyahısına yenidən yazmaq həm təkrarçılıqdır, həm də
    hər yerdə <strong>ayrı nüsxə</strong> yaranması riski daşıyır — 5 modul, 5 bağlantı
    deməkdir. <code>@Global()</code> dekoratoru modulu bütün layihə üçün əlçatan edir:
    bir dənə bağlantı havuzu, hamı onu paylaşır.""",
    b=[("src/prisma/prisma.module.ts", fayl("src/prisma/prisma.module.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# @Global, providers və exports üçlüyü yerindədirmi?
grep -n '@Global\\|providers\\|exports' src/prisma/prisma.module.ts

# Modul düzgün yazılıbsa build keçməlidir
npm run build && echo "✓ build keçdi\"""",
    c_olmaz="""$ node dist/main.js      # @Global() silinsə:

[Nest] ERROR [ExceptionHandler] UnknownDependenciesException [Error]:
Nest can't resolve dependencies of the SaglamliqService (?).
Please make sure that the argument PrismaService at index [0]
is available in the SaglamliqModule module.

    dependencies: [ '?' ]""",
    c_izah="""NestJS hər modulu ayrı bir qutu kimi görür: modul yalnız öz
    <code>providers</code>-ını və <code>imports</code> etdiyi modulların
    <code>exports</code>-unu görə bilir. <code>@Global()</code> olmasa
    <code>SaglamliqModule</code> <code>PrismaService</code>-i tanımır və
    <strong>server heç qalxmır</strong> — xəta isə konfiqurasiya mərhələsində,
    yəni ilk sorğudan əvvəl çıxır.""",
    d="""$ node dist/main.js

[Nest] LOG [InstanceLoader] AppModule dependencies initialized +8ms
[Nest] LOG [InstanceLoader] PrismaModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] ConfigHostModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] ConfigModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] SaglamliqModule dependencies initialized +0ms
[Nest] LOG [BAZA] Baza bağlantısı açıldı

# Modul ağacı — PrismaModule BİR dənədir, @Global sayəsində hamıya açıqdır:
AppModule
├── ConfigModule      (isGlobal: true)
├── PrismaModule      (@Global: true)  →  PrismaService
└── SaglamliqModule   →  SaglamliqService (PrismaService-i BİRBAŞA alır)""",
    d_izah="""Sistemin vəziyyəti: dörd modul növbə ilə yükləndi.
    <code>PrismaModule</code> yalnız <strong>bir dəfə</strong> qeydiyyatdan keçdi və
    <code>SaglamliqModule</code> onu import etmədən <code>PrismaService</code>-i
    konstruktorunda istifadə edə bildi. <code>exports</code> sətri isə vacibdir:
    <code>@Global()</code> modulu "hamıya açıq" edir, amma <code>exports</code>
    olmasa içindəki servis hələ də görünməz qalar.""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=8,
    ad="AllExceptionsFilter — vahid xəta formatı",
    a="""NestJS xəta baş verəndə öz formatını qaytarır:
    <code>{ statusCode, message, error }</code>. Frontend isə həmişə <strong>eyni</strong>
    formanı gözləməlidir, yoxsa hər endpoint üçün ayrı xəta emalı yazmaq lazım gələr.
    <code>AllExceptionsFilter</code> bütün xətaları tutub vahid formata salır:
    <code>{ ugur, xeta: { kod, mesaj, detallar }, yol, vaxt }</code>. Beləliklə frontend-də
    bir dənə funksiya bütün xətaları göstərə bilir.""",
    b=[("src/common/filters/all-exceptions.filter.ts",
        fayl("src/common/filters/all-exceptions.filter.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# @Catch() boş mötərizə ilə olmalıdır — hamısını tutur
grep -n '@Catch' src/common/filters/all-exceptions.filter.ts

# Status → kod xəritəsi tamdırmı?
grep -c ':' src/common/filters/all-exceptions.filter.ts

# main.ts-də qeydiyyatdan keçibmi?
grep -n 'useGlobalFilters' src/main.ts""",
    c_olmaz="""$ curl -s http://localhost:4000/api/v1/yoxdur

{"message":"Cannot GET /api/v1/yoxdur","error":"Not Found","statusCode":404}""",
    c_izah="""Bu, NestJS-in default formatıdır. Görünür ki, burada nə xəta
    <strong>kodu</strong> var, nə də <strong>vaxt</strong> — frontend yalnız
    <code>message</code> mətninə baxa bilər, o da ingiliscədir. Filtr olmadan
    hər modul öz xəta formatını qaytarar və frontend-də
    <code>if (res.statusCode) ... else if (res.xeta) ...</code> kimi qarışıq kod yaranar.""",
    d="""$ curl -s http://localhost:4000/api/v1/yoxdur | python3 -m json.tool

{
    "ugur": false,
    "xeta": {
        "kod": "TAPILMADI",
        "mesaj": "Cannot GET /api/v1/yoxdur"
    },
    "yol": "/yoxdur",
    "vaxt": "2026-09-20T12:40:36.106Z"
}""",
    d_izah="""Sistemin vəziyyəti: eyni 404 cavabı indi <strong>vahid formatdadır</strong>.
    <code>ugur: false</code> sahəsi uğurlu cavablardaki <code>ugur: true</code> ilə
    simmetrikdir — frontend hər cavabda əvvəlcə bu sahəyə baxır.
    <code>xeta.kod</code> isə sabit sözdür (<code>TAPILMADI</code>,
    <code>ICAZE_YOXDUR</code>...), yəni frontend mətn dəyişdikdə belə koda görə
    qərar verə bilir. <code>@Catch()</code> mötərizəsi boşdur — bu o deməkdir ki,
    filtr <strong>hər növ</strong> xətanı tutur, yalnız HTTP xətalarını yox.""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=9,
    ad="Sağlamlıq modulu — ilk işləyən endpoint",
    a="""Sistemin işlədiyini yoxlamaq üçün ən sadə endpoint budur. Sadəcə
    "işləyirəm" demək <strong>kifayət deyil</strong> — baza bağlantısı qopubsa API
    yenə də "işləyirəm" deyəcək və problem yalnız istifadəçi məlumat istəyəndə
    üzə çıxacaq. Ona görə <code>/saglamliq</code> hər çağırışda bazaya real sorğu
    göndərir və cavaba cədvəl sayını da əlavə edir.""",
    b=[
        ("src/saglamliq/saglamliq.service.ts", fayl("src/saglamliq/saglamliq.service.ts")),
        ("src/saglamliq/saglamliq.controller.ts",
         fayl("src/saglamliq/saglamliq.controller.ts")),
        ("src/saglamliq/saglamliq.module.ts", fayl("src/saglamliq/saglamliq.module.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# Controller yolu və metodları düzgündürmü?
grep -n "@Controller\\|@Get\\|@ApiTags" src/saglamliq/saglamliq.controller.ts

# Servis PrismaService-i çağırırmı?
grep -n 'prisma.yoxla\\|constructor' src/saglamliq/saglamliq.service.ts

# Modul controller və service-i qeydiyyata alıbmı?
cat src/saglamliq/saglamliq.module.ts""",
    c_olmaz="""$ curl -s -o /dev/null -w '%{http_code}\\n' http://localhost:4000/api/v1/saglamliq
404

$ curl -s http://localhost:4000/api/v1/saglamliq
{"ugur":false,"xeta":{"kod":"TAPILMADI",
 "mesaj":"Cannot GET /api/v1/saglamliq"},"yol":"/saglamliq",
 "vaxt":"2026-09-20T12:41:02.338Z"}""",
    c_izah="""Modul kök modula qoşulmasa NestJS bu yolu ümumiyyətlə tanımır və
    <strong>404</strong> qaytarır. Diqqət yetirin: xəta formatı bizim filtrdən gəlir —
    yəni filtr işləyir, sadəcə endpoint yoxdur. Bu, sağlamlıq yoxlamasının
    ən vacib xüsusiyyətini də göstərir: <strong>404 sağlamlıq problemi deyil</strong>,
    o, konfiqurasiya problemidir.""",
    d="""$ curl -s http://localhost:4000/api/v1/saglamliq | python3 -m json.tool

{
    "status": "saglam",
    "baza": {
        "qosulub": true,
        "cedvel_sayi": 48,
        "gecikme_ms": 31
    },
    "versiya": "0.1.0",
    "vaxt": "2026-09-20T12:39:17.362Z"
}

$ curl -s http://localhost:4000/api/v1/ | python3 -m json.tool

{
    "ad": "ARTİ ERP API",
    "versiya": "0.1.0",
    "prefiks": "/api/v1",
    "senedlesdirme": "/docs"
}""",
    d_izah="""Sistemin vəziyyəti: API artıq <strong>canlıdır və bazaya qoşulub</strong>.
    <code>cedvel_sayi: 48</code> rəqəmi birbaşa PostgreSQL-dən gəlir — bu o deməkdir ki,
    sorğu həqiqətən icra olundu. <code>gecikme_ms</code> sahəsi isə gələcəkdə
    monitorinq üçün lazımdır: bu rəqəm 500-ü keçməyə başlasa, baza yüklənməsini
    yoxlamaq lazımdır. <code>@Controller()</code> mötərizəsi <strong>boşdur</strong> —
    ona görə yollar <code>/saglamliq</code> və <code>/</code> kimi qlobal prefiksin
    düz altında yerləşir.""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=10,
    ad="app.module.ts — kök modul",
    a="""Kök modul bütün parçaları bir yerə yığır: <code>ConfigModule</code>
    <code>.env</code>-i oxuyur, <code>PrismaModule</code> baza bağlantısını gətirir,
    <code>SaglamliqModule</code> isə endpoint-ləri qeydiyyata alır. NestJS tətbiqi
    məhz bu moduldan başlayaraq bütün ağacı qurur. <code>isGlobal: true</code> olmasa
    <code>ConfigService</code>-i hər modulda ayrıca import etmək lazım gələrdi.""",
    b=[("src/app.module.ts", fayl("src/app.module.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# Hər üç modul imports siyahısındadırmı?
grep -n 'imports\\|ConfigModule\\|PrismaModule\\|SaglamliqModule\\|isGlobal' \\
  src/app.module.ts

# NestJS bu faylı giriş nöqtəsi kimi tanıyırmı?
grep -n 'AppModule' src/main.ts""",
    c_olmaz="""$ node dist/main.js      # ConfigModule silinsə:

[Nest] ERROR [ExceptionHandler] Error: DATABASE_URL təyin olunmayıb
  — .env faylını yoxlayın""",
    c_izah="""<code>ConfigModule.forRoot()</code> olmasa <code>.env</code> faylı
    <strong>heç oxunmur</strong> — <code>dotenv</code> paketi quraşdırılıb, amma
    onu işə salan yoxdur. Nəticədə <code>process.env.DATABASE_URL</code>
    <code>undefined</code> olur və server 4-cü addımdaki xəta ilə dayanır.
    <code>isGlobal: true</code> olmasa isə hər modul öz
    <code>imports</code>-una <code>ConfigModule</code> əlavə etməli olar —
    20 modulda 20 təkrar sətir.""",
    d="""$ node dist/main.js

[Nest] LOG [InstanceLoader] AppModule dependencies initialized +8ms
[Nest] LOG [InstanceLoader] PrismaModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] ConfigHostModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] ConfigModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] SaglamliqModule dependencies initialized +0ms
[Nest] LOG [RoutesResolver] SaglamliqController {/api/v1}: +37ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/saglamliq, GET} route +0ms
[Nest] LOG [BAZA] Baza bağlantısı açıldı
[Nest] LOG [NestApplication] Nest application successfully started +0ms
[Nest] LOG [BAŞLANGIC] API hazırdır → http://localhost:4000/api/v1
[Nest] LOG [BAŞLANGIC] Sənədləşdirmə → http://localhost:4000/docs""",
    d_izah="""Sistemin vəziyyəti: <code>Mapped {/api/v1/saglamliq, GET} route</code>
    sətri NestJS-in endpoint-i <strong>həqiqətən qeydiyyata aldığını</strong> təsdiqləyir.
    Diqqət yetirin ki, <code>ConfigHostModule</code> və <code>ConfigModule</code>
    ayrı-ayrı yüklənir — <code>ConfigModule.forRoot()</code> daxildə köməkçi modul
    yaradır, bu normaldır. Yüklənmə sırası da önəmlidir: PrismaModule
    SaglamliqModule-dən əvvəl gəlir, çünki o, bağlantını hazır saxlayır.""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=11,
    ad="main.ts — serverin giriş nöqtəsi",
    a="""<code>main.ts</code> tətbiqi işə salan fayldır. Burada üç qlobal qərar verilir:
    bütün yolların <code>/api/v1</code> altında toplanması, gələn məlumatın avtomatik
    yoxlanması və xətaların vahid formata salınması. Swagger sənədləşdirməsi də
    burada qoşulur ki, <code>/docs</code> ünvanında bütün API-yə baxmaq mümkün olsun.
    Bu qərarlar bir yerdə verildiyi üçün bütün modullar üçün eyni qaydalar qüvvədə olur.""",
    b=[("src/main.ts", fayl("src/main.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# Dörd qlobal qərar da yerindədirmi?
grep -n 'setGlobalPrefix\\|useGlobalPipes\\|useGlobalFilters\\|SwaggerModule\\|enableCors\\|app.listen' \\
  src/main.ts

# PORT dəyəri .env-dən gəlirmi?
grep -n 'PORT' .env src/main.ts""",
    c_olmaz="""$ node dist/main.js      # setGlobalPrefix silinsə:

$ curl -s -o /dev/null -w '%{http_code}\\n' http://localhost:4000/api/v1/saglamliq
404
$ curl -s -o /dev/null -w '%{http_code}\\n' http://localhost:4000/saglamliq
200""",
    c_izah="""<code>setGlobalPrefix('api/v1')</code> olmasa endpoint <code>/saglamliq</code>
    ünvanında işləyir və <code>/api/v1/saglamliq</code> <strong>404</strong> verir.
    Bu, sonradan düzəltməsi ən baha səhvdir: frontend, mobil tətbiq və sənədləşdirmə
    hamısı köhnə yola bağlanır. Versiya prefiksi (<code>v1</code>) isə gələcəkdə
    API dəyişəndə köhnə müştəriləri sındırmamaq üçündür.""",
    d="""$ npm run build && node dist/main.js

[Nest] LOG [NestApplication] Nest application successfully started +0ms
[Nest] LOG [BAŞLANGIC] API hazırdır → http://localhost:4000/api/v1
[Nest] LOG [BAŞLANGIC] Sənədləşdirmə → http://localhost:4000/docs

$ curl -s http://localhost:4000/docs-json | python3 -c "
import json,sys
d = json.load(sys.stdin)
for yol, metodlar in sorted(d['paths'].items()):
    for m in metodlar:
        print(f'  {m.upper():6s} {yol}')
"
  GET    /api/v1
  GET    /api/v1/saglamliq

$ curl -s -o /dev/null -w 'docs → %{http_code}\\n' http://localhost:4000/docs
docs → 200""",
    d_izah="""Sistemin vəziyyəti: server qalxdı, iki marshrut qeydiyyatdadır və Swagger
    sənədləşdirməsi <code>/docs</code> ünvanında canlıdır. <code>/docs-json</code>
    ünvanı OpenAPI spesifikasiyasını JSON kimi verir — bu fayl sonradan frontend
    üçün TypeScript tipləri yaratmağa yarayacaq. <code>ValidationPipe</code>-daki
    <code>whitelist</code> və <code>forbidNonWhitelisted</code> ayarları hələ
    görünmür, çünki hələ heç bir DTO yoxdur — onlar növbəti dərsdə işə düşəcək.""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=12,
    ad="Build və tam canlı yoxlama",
    a="""<code>nest build</code> TypeScript-i JavaScript-ə çevirib <code>dist/</code>
    qovluğuna yığır; istehsalatda <code>node dist/main.js</code> işlədilir, inkişafda
    isə <code>nest start --watch</code> hər dəyişiklikdə özü yenidən qurur. Bu addımda
    bütün əvvəlki addımları <strong>bir yerdə</strong> yoxlayırıq: yığım, serverin
    qalxması, baza bağlantısı, prefiks, xəta formatı və sənədləşdirmə.""",
    b=[("Terminal — yığ və işə sal", """cd ~/Deepseek_ARTI/DS_Backend

# Yığ
npm run build

# İstehsalat rejimində işə sal
node dist/main.js

# İnkiaf üçün (ayrı terminalda) — hər dəyişiklikdə özü yenilənir
# npm run start:dev"""),
        ("Terminal — beş yoxlama bir yerdə", """API=http://localhost:4000/api/v1

echo "1) Sağlamlıq        : $(curl -s -o /dev/null -w '%{http_code}' $API/saglamliq)"
echo "2) Kök endpoint     : $(curl -s -o /dev/null -w '%{http_code}' $API/)"
echo "3) Prefikssiz (404) : $(curl -s -o /dev/null -w '%{http_code}' http://localhost:4000/saglamliq)"
echo "4) Sənədləşdirmə    : $(curl -s -o /dev/null -w '%{http_code}' http://localhost:4000/docs)"
echo "5) Olmayan yol      : $(curl -s -o /dev/null -w '%{http_code}' $API/yoxdur)\"""")],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) dist yarandımı və içində nə var?
ls -1 dist/

# 2) Bizim mənbələr JavaScript-ə çevrildimi?
#    (generated/ kənarlaşdırılır — onun 56 faylı siyahını doldurur)
find dist -name '*.js' -not -path '*/generated/*' | sort

# 3) generated qovluğu da dist-ə düşdümü?
ls -d dist/generated/prisma""",
    c_olmaz="""$ npm run build      # xəta olsa:

src/saglamliq/saglamliq.controller.ts:11:3 - error TS1241: ...

$ ls dist/
ls: dist/: No such file or directory""",
    c_izah="""Build uğursuz olsa <code>dist/</code> qovluğu <strong>heç yaranmır</strong>
    (nest-cli.json-daki <code>deleteOutDir: true</code> əvvəlcə köhnəni silir).
    Yəni <code>node dist/main.js</code> köhnə kodu işlətməz — sadəcə
    "fayl tapılmadı" deyəcək. Bu yaxşı xüsusiyyətdir: sınıq kodun təsadüfən
    istehsalata düşməsi mümkün deyil.""",
    d="""$ npm run build
> ds-backend@0.1.0 build
> nest build
   (xəta yoxdur)

$ ls -1 dist/ | head
app.module.js
common
generated
main.js
prisma
saglamliq
tsconfig.build.tsbuildinfo

$ node dist/main.js &
$ API=http://localhost:4000/api/v1
1) Sağlamlıq        : 200
2) Kök endpoint     : 200
3) Prefikssiz (404) : 404
4) Sənədləşdirmə    : 200
5) Olmayan yol      : 404

$ curl -s $API/saglamliq
{"status":"saglam","baza":{"qosulub":true,"cedvel_sayi":48,
 "gecikme_ms":2},"versiya":"0.1.0","vaxt":"2026-09-20T12:39:17.362Z"}""",
    d_izah="""<strong>Backend-in bu andaki tam durumu:</strong>
    <ul>
      <li>Server <code>dist/main.js</code>-dən işləyir — yəni TypeScript yox,
          <strong>həqiqi JavaScript</strong> icra olunur.</li>
      <li>Baza bağlantısı canlıdır: 48 cədvəl, 2 ms gecikmə.</li>
      <li>İki endpoint işləyir, üçüncü qorunur (404), sənədləşdirmə açıqdır.</li>
      <li>Xəta formatı vahiddir — 5-ci yoxlamanın cavabı bizim formatdadır.</li>
      <li>Yoxlama üçün heç bir autentifikasiya yoxdur: bu, hələ
          <strong>açıq API</strong>-dir. Növbəti dərsdə JWT ilə bağlayacağıq.</li>
    </ul>""",
)

# ──────────────────────────────────────────────────────────────────
addim(
    n=13,
    ad="Testlər — hər dəyişiklikdən sonra bir əmr",
    a="""Hər dəfə əl ilə <code>curl</code> etmək yorucudur və vaxt keçdikcə unudulur.
    Vitest ilə avtomatik testlər yazırıq: <strong>unit</strong> testlər servisi təcrid
    olunmuş şəkildə yoxlayır (baza lazım deyil), <strong>e2e</strong> testlər isə real
    HTTP sorğusu göndərir. Bu andan sonra hər dəyişiklikdən sonra bir əmr bütün
    sistemi yoxlayır və nəyisə sındırdığımızı dərhal bilirik.""",
    b=[
        ("vitest.config.ts — unit testlər", fayl("vitest.config.ts")),
        ("vitest.config.e2e.ts — e2e testlər", fayl("vitest.config.e2e.ts")),
        ("src/saglamliq/saglamliq.service.spec.ts",
         fayl("src/saglamliq/saglamliq.service.spec.ts")),
        ("test/saglamliq.e2e-spec.ts", fayl("test/saglamliq.e2e-spec.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Unit testlər — baza lazım DEYİL
npm test

# 2) e2e testlər — real bazaya qoşulur
npx vitest run --config vitest.config.e2e.ts

# 3) Yalnız bir fayl
npx vitest run src/saglamliq/saglamliq.service.spec.ts

# 4) e2e XARİC edilibmi? (bu əmr YALNIZ spec.ts görməlidir)
echo "unit konfiqurasiyası:"
grep -n 'include\\|exclude' vitest.config.ts""",
    c_olmaz="""$ npm test      # exclude sətri silinsə:

 ✓ src/saglamliq/saglamliq.service.spec.ts (3 tests) 37ms
 ✓ test/saglamliq.e2e-spec.ts (4 tests) 143ms

 Test Files  2 passed (2)
      Tests  7 passed (7)""",
    c_izah="""Bu <em>uğurlu</em> görünür, amma gizli problemdir: artıq
    <code>npm test</code> bazaya qoşulur. Baza olmayan mühitdə — məsələn
    CI-ın unit mərhələsində və ya başqa kompüterdə — <code>ECONNREFUSED</code>
    alacaqsınız və səbəbi tapmaq çətin olacaq. Unit testlər <strong>sürətli və
    təcrid olunmuş</strong> olmalıdır; e2e isə ayrı əmrlə çağırılmalıdır.""",
    d="""$ npm test
 ✓ src/saglamliq/saglamliq.service.spec.ts (3 tests) 33ms
 Test Files  1 passed (1)
      Tests  3 passed (3)

$ npx vitest run --config vitest.config.e2e.ts
 ✓ test/saglamliq.e2e-spec.ts (4 tests) 267ms
 Test Files  1 passed (1)
      Tests  4 passed (4)

Yekun: 3 unit + 4 e2e = 7 test""",
    d_izah="""Sistemin vəziyyəti: artıq <strong>avtomatik təhlükəsizlik şəbəkəsi</strong>
    var. Unit testlər <code>PrismaService</code>-i saxta obyektlə əvəz edir
    (<code>useValue: prisma</code>) — buna görə baza olmadan da işləyir və
    33 ms çəkir. e2e testlər isə real <code>AppModule</code>-u qaldırıb
    <code>supertest</code> ilə HTTP sorğusu göndərir; onlar bazanı yoxlayır,
    ona görə 8 dəfə yavaşdır (267 ms). Bu ikisi birlikdə həm
    <em>məntiqi</em>, həm də <em>inteqrasiyanı</em> qoruyur.""",
)


# ══════════════════════════════════════════════════════════════════
#  HTML QURULMASI
# ══════════════════════════════════════════════════════════════════
def addim_html(x: dict) -> str:
    b_hissə = ""
    for fayl_ad, kod in x["b"]:
        b_hissə += (
            f'    <p class="fayl-ad">{e(fayl_ad)}</p>\n'
            f'<pre><code>{e(kod)}</code></pre>\n'
        )

    return f"""<div class="addim">
  <h2 class="addim-basliq" id="a{x['n']}">
    <span class="addim-no">{x['n']}</span> {e(x['ad'])}
  </h2>
  <div class="addim-govde">

    <div class="hisse hisse-a">
      <span class="hisse-basliq">A · Bu addım nəyə görədir</span>
      <p>{x['a']}</p>
    </div>

    <div class="hisse hisse-b">
      <span class="hisse-basliq">B · Kod</span>
{b_hissə}    </div>

    <div class="hisse hisse-c">
      <span class="hisse-basliq">C · Yoxlama — kod düzgün yazıldı?</span>
      <p>Aşağıdaki əmrləri işlədin və nəticəni yoxlayın:</p>
<pre><code>{e(x['c_yoxla'])}</code></pre>
      <div class="olmaz">
        <span class="olmaz-basliq">⚠️ Bu kod olmasa nə olardı</span>
<pre><code>{e(x['c_olmaz'])}</code></pre>
        <p>{x['c_izah']}</p>
      </div>
    </div>

    <div class="hisse hisse-d">
      <span class="hisse-basliq">D · Bu koddan sonra sistemin durumu</span>
<pre><code>{e(x['d'])}</code></pre>
      <div class="oldu">
        <span class="oldu-basliq">✔ Nəticə</span>
        <p>{x['d_izah']}</p>
      </div>
    </div>

  </div>
  <div class="addim-icmal">
    <span>Addım {x['n']} / {len(ADDIMLAR)}</span>
    <span>A · niyə</span><span>B · kod</span>
    <span>C · yoxlama</span><span>D · durum</span>
  </div>
</div>
"""


def toc_html() -> str:
    sətr = ""
    for x in ADDIMLAR:
        sətr += (f'    <li><a href="#a{x["n"]}">{x["n"]}. {e(x["ad"])}</a></li>\n')
    return sətr


def icmal_html() -> str:
    sətr = ""
    for x in ADDIMLAR:
        sətr += (f'  <a href="#a{x["n"]}"><b>ADDIM {x["n"]}</b>{e(x["ad"])}</a>\n')
    return sətr


def main() -> None:
    css = CSS_FAYLI.read_text(encoding="utf-8").rstrip("\n")
    css += "\n" + ELAVE_CSS

    addimlar = "\n".join(addim_html(x) for x in ADDIMLAR)

    sened = f"""<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Backend 1 — Sıfırdan ilk işləyən API (A/B/C/D)</title>
<style>
{css}
</style>
</head>
<body>
<div class="container">

<header>
  <div class="lesson-badge">DS_Backend · Hissə 1 / 4</div>
  <h1>Backend 1 — Sıfırdan ilk işləyən API</h1>
  <p class="subtitle">Hər addım 4 hissə: <strong>A</strong> niyə ·
    <strong>B</strong> kod · <strong>C</strong> yoxlama · <strong>D</strong> durum</p>
  <p class="meta">
    <span>NestJS 12</span>
    <span>Prisma 7</span>
    <span>PostgreSQL · arti_baza</span>
    <span>{len(ADDIMLAR)} addım</span>
    <span>7 test</span>
  </p>
</header>

<div class="block block-ne">
  <span class="block-title">NƏ EDƏCƏYİK</span>
  <p>Sıfırdan başlayıb <strong>işləyən, bazaya qoşulan və test edilən</strong> bir
  backend quracağıq. Sonda <code>http://localhost:4000/api/v1/saglamliq</code>
  ünvanı canlı olacaq və 48 cədvəlli <code>arti_baza</code> ilə danışacaq.</p>
  <p><strong>Bu dərsdə autentifikasiya YOXDUR</strong> — API açıqdır.
  İstifadəçi girişi və rollar növbəti dərsin mövzusudur.</p>
</div>

<div class="block block-nece">
  <span class="block-title">NECƏ OXUMALI — hər addımın 4 hissəsi</span>
  <table>
    <tr><th>Hissə</th><th>Nə var</th><th>Nə üçün lazımdır</th></tr>
    <tr>
      <td><strong>A</strong></td>
      <td>Bu addım nəyə görədir — 3-4 cümlə</td>
      <td>Kodu yazmadan <em>əvvəl</em> məqsədi anlamaq üçün</td>
    </tr>
    <tr>
      <td><strong>B</strong></td>
      <td>Addıma aid kodun özü — tam və kopyalana bilən</td>
      <td>Olduğu kimi kopyalayıb işlətmək üçün</td>
    </tr>
    <tr>
      <td><strong>C</strong></td>
      <td>Kodun düzgün yazıldığını yoxlayan əmrlər +
        <span style="color:#b91c1c">bu kod olmasa nə olardı</span></td>
      <td>Səhvi <em>dərhal</em> tutmaq və kodun <em>nə üçün</em> orada olduğunu
        görmək üçün</td>
    </tr>
    <tr>
      <td><strong>D</strong></td>
      <td>Sistemin bu koddan sonraki <strong>real</strong> durumu —
        əmrlərin həqiqi çıxışı</td>
      <td>Nəticənin uydurma deyil, ölçülmüş olduğunu görmək üçün</td>
    </tr>
  </table>
  <p>D hissəsindəki bütün çıxışlar bu dərs hazırlanarkən <strong>canlı sistemdə</strong>
  işlədilib və olduğu kimi köçürülüb. C hissəsindəki qırmızı xəta mətnləri də
  realdır — kodu bilərəkdən söndürüb alınmış çıxışlardır.</p>
</div>

<div class="block block-ipucu">
  <span class="block-title">💡 BAŞLAMAZDAN ƏVVƏL — ön şərtlər</span>
  <table>
    <tr><th>Nə</th><th>Yoxlama əmri</th><th>Gözlənilən</th></tr>
    <tr><td>Node.js 22+</td><td><code>node -v</code></td><td><code>v22</code> və yuxarı</td></tr>
    <tr><td>PostgreSQL işləyir</td><td><code>pg_isready -h localhost -p 5432</code></td>
        <td><code>accepting connections</code></td></tr>
    <tr><td><code>arti_baza</code> mövcuddur</td>
        <td><code>psql -U arti_user -w -d arti_baza -c '\\dt *.*'</code></td>
        <td>48 cədvəl</td></tr>
  </table>
  <p>Psql işlədərkən <code>unset DATABASE_URL PGHOST</code> əmrini verin — əks halda
  sistem dəyişəni başqa bazaya yönləndirə bilər.</p>
</div>

<div class="toc">
  <h3>📚 Addımlar</h3>
  <ol>
{toc_html()}  </ol>
</div>

<div class="icmal">
{icmal_html()}</div>

{addimlar}

<div class="success-box">
  <strong>Backend-1 tamamlandı.</strong> İşləyən API: 2 endpoint ·
  48 cədvəlli bazaya canlı bağlantı · vahid xəta formatı · Swagger ·
  3 unit + 4 e2e test. <strong>Növbəti dərs:</strong> ilk funksional modul —
  struktur (mərkəzlər, şöbələr) və kadrlar, DTO validasiyası ilə.
</div>

<div class="block block-xeber">
  <span class="block-title">⚠️ BU DƏRSDƏ NƏ YOXDUR</span>
  <ul>
    <li><strong>Autentifikasiya yoxdur</strong> — bütün endpoint-lər açıqdır.</li>
    <li><strong>Yazma əməliyyatı yoxdur</strong> — yalnız oxuma (GET).</li>
    <li><strong>Audit jurnalı yoxdur</strong> — kim nə etdiyi yazılmır.</li>
    <li><strong>AI qatı yoxdur</strong> — embedding, RAG və təbii dil sorğuları sonra.</li>
  </ul>
  <p>Bunlar qəsdən kənarda saxlanılıb: hər biri öz addımlarını tələb edir və
  ayrı-ayrılıqda yoxlanılmalıdır.</p>
</div>

</div>
<script>
  document.addEventListener('DOMContentLoaded', function () {{
    document.querySelectorAll('pre').forEach(function (pre) {{
      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.textContent = '📋 KOPYALA';
      btn.addEventListener('click', async function (ev) {{
        ev.preventDefault();
        var kod = pre.querySelector('code');
        var metn = kod ? kod.textContent : pre.textContent;
        try {{
          await navigator.clipboard.writeText(metn);
          btn.textContent = '✅ KOPYALANDI';
          btn.classList.add('copied');
          setTimeout(function () {{
            btn.textContent = '📋 KOPYALA';
            btn.classList.remove('copied');
          }}, 2000);
        }} catch (err) {{
          var ta = document.createElement('textarea');
          ta.value = metn;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          btn.textContent = '✅ KOPYALANDI';
          setTimeout(function () {{ btn.textContent = '📋 KOPYALA'; }}, 2000);
        }}
      }});
      pre.insertBefore(btn, pre.firstChild);
    }});
  }});
</script>
</body>
</html>
"""

    CIXIS.write_text(sened, encoding="utf-8")
    setir = sened.count("\n") + 1
    print(f"✅ {CIXIS.relative_to(KOK)}")
    print(f"   {setir} sətir · {len(ADDIMLAR)} addım × 4 hissə "
          f"= {len(ADDIMLAR) * 4} bölmə")


if __name__ == "__main__":
    main()
