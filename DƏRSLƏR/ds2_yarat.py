#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-2.html dərsini yaradır — A / B / C / D formatında.

Hər addım 4 hissədən ibarətdir:
  A — bu addım nəyə görədir (3-4 cümlə)
  B — addıma aid kodun özü (hər fayl bloku `cat > ... <<'EOF'` formasında)
  C — kodun yazıldığını yoxlayın + bu kod olmasa nə olardı (REAL xətalar)
  D — bu koddan sonra sistemin durumu (REAL çıxışlar) — ÇIXIŞ, kopyalanmır

B hissəsindəki kodlar BACKEND qovluğundan CANLI oxunur — dərsdəki kod
həmişə real faylla eyni olur.

İSTİFADƏ:
    python3 DƏRSLƏR/ds2_yarat.py                     # ~/Deepseek_ARTI/DS_Backend
    BACKEND=/tmp/b2 python3 DƏRSLƏR/ds2_yarat.py     # başqa qovluqdan
"""
from __future__ import annotations

import html
import os
import pathlib

KOK = pathlib.Path(__file__).resolve().parent.parent
BACKEND = pathlib.Path(os.environ.get("BACKEND", str(KOK / "DS_Backend")))
CIXIS = KOK / "DƏRSLƏR" / "DS_Backend-2.html"
CSS_FAYLI = KOK / "DS_Baza" / "ders.css"


def e(metn: str) -> str:
    """HTML üçün təhlükəsiz hala gətirir."""
    return html.escape(str(metn), quote=False)


def app_module_araliq() -> str:
    """ADDIM 5 üçün ARALIQ versiya — hələ KadrlarModule yoxdur."""
    tam = (BACKEND / "src/app.module.ts").read_text(encoding="utf-8").rstrip(chr(10))
    setirler = [
        x for x in tam.split(chr(10))
        if "KadrlarModule" not in x
    ]
    govde = chr(10).join(setirler)
    return (f"mkdir -p src{chr(10)}"
            f"cat > src/app.module.ts <<'EOF'{chr(10)}{govde}{chr(10)}EOF")


def fayl(yol: str) -> str:
    """BACKEND içindən real faylı oxuyur və `cat > ... <<'EOF'` formasına salır."""
    p = BACKEND / yol
    if not p.exists():
        raise SystemExit(f"XƏTA: fayl tapılmadı: {p}")
    govde = p.read_text(encoding="utf-8").rstrip("\n")
    qovluq = os.path.dirname(yol)
    basliq = f"mkdir -p {qovluq}" + chr(10) if qovluq else ""
    return f"{basliq}cat > {yol} <<'EOF'\n{govde}\nEOF"


# ══════════════════════════════════════════════════════════════════
#  ƏLAVƏ CSS — A/B/C/D hissələri (Dərs 1 ilə eyni görünüş)
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
  .cixis-xeber {
    background: #fef2f2; border-left: 5px solid #dc2626;
    padding: .6rem .9rem; border-radius: 8px; margin: .2rem 0 .8rem;
    font-size: .84rem; font-weight: 600; color: #991b1b;
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
ADDIMLAR: list = []


def addim(n, ad, a, b, c_yoxla, c_olmaz, c_izah, d, d_izah, b_html=None):
    ADDIMLAR.append(dict(
        n=n, ad=ad, a=a, b=b, b_html=b_html, c_yoxla=c_yoxla,
        c_olmaz=c_olmaz, c_izah=c_izah, d=d, d_izah=d_izah,
    ))


D_CLEAN = """$ npx tsc --noEmit -p tsconfig.build.json
   (heç bir çıxış yoxdur — bu, tip yoxlamasının KEÇDİYİ deməkdir)

$ echo $?
0"""


# ─────────────────────────────────────────────────────────────────
addim(
    n=1,
    ad="Ortaq səhifələmə DTO-su",
    a="""Hər siyahı endpoint-i eyni suallara cavab verməlidir: cəmi neçə sətir,
    hansı səhifə, neçə səhifə. Bu cavabları hər modulda ayrı-ayrı yazsaq, frontend
    hər endpoint üçün fərqli kod yazmalı olar. Ona görə səhifələməni <strong>bir dəfə</strong>
    ortaq DTO-da yazırıq və bütün filtr DTO-ları ondan miras alır. Bu addımda həm
    sorğu parametrləri (<code>SehifeSorghu</code>), həm cavab forması
    (<code>Sehifelenmis&lt;T&gt;</code>), həm də iki köməkçi funksiya yaranır.""",
    b=[("src/common/dto/sehife.dto.ts", fayl("src/common/dto/sehife.dto.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayl yerindədirmi?
ls -l src/common/dto/sehife.dto.ts

# 2) Nə ixrac edir?
grep -nE '^export' src/common/dto/sehife.dto.ts

# 3) Tip yoxlaması keçirmi?
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi\"""",
    c_olmaz="""$ npx tsc --noEmit -p tsconfig.build.json      # fayl silinsə:

src/struktur/dto/merkez-filtr.dto.ts:3:30 - error TS2307:
  Cannot find module '../../common/dto/sehife.dto.js'
  or its corresponding type declarations.

src/kadrlar/dto/emekdas-filtr.dto.ts:4:30 - error TS2307:
  Cannot find module '../../common/dto/sehife.dto.js'
  or its corresponding type declarations.""",
    c_izah="""Bu fayl bütün filtr DTO-larının <strong>valideynidir</strong>. O olmasa
    nə struktur, nə də kadrlar modulu kompilyasiya olunur — <code>TS2307</code>
    xətası hər iki modulda çıxır. Səhifələməni hər modulda ayrı yazmağın digər
    yolu da var, amma o halda <code>limit</code> bir yerdə 100, başqa yerdə 50
    ola bilər və frontend hansına güvənəcəyini bilməz.""",
    d="""$ npx tsc --noEmit -p tsconfig.build.json
   (çıxış yoxdur — tip yoxlaması KEÇDİ)

$ npx tsx -e "
import { sehifeHesabla, sehifelenmis } from './src/common/dto/sehife.dto.js';
console.log(JSON.stringify(sehifeHesabla(3, 15)));
console.log(JSON.stringify(sehifeHesabla(1, 5000)));
console.log(JSON.stringify(sehifeHesabla(-7, 20)));
console.log(JSON.stringify(sehifelenmis([], 0, 1, 20)));
console.log(JSON.stringify(sehifelenmis([], 10, 1, 3)));"

{"sehife":3,"limit":15,"skip":30}
{"sehife":1,"limit":100,"skip":0}
{"sehife":1,"limit":20,"skip":0}
{"setirler":[],"cemi":0,"sehife":1,"limit":20,"sehife_sayi":1}
{"setirler":[],"cemi":10,"sehife":1,"limit":3,"sehife_sayi":4}""",
    d_izah="""Sistemin vəziyyəti: ortaq səhifələmə qatı hazırdır və <strong>hədləri
    özü qoruyur</strong>. Diqqət yetirin: <code>sehifeHesabla(1, 5000)</code>
    limiti <strong>100-ə kəsir</strong>; <code>sehifeHesabla(-7, 20)</code> isə
    mənfi səhifəni 1-ə düzəldib <code>skip: 0</code> verir. Bu qoruma olmasa
    istifadəçi <code>?limit=999999</code> göndərib bazanı boğa bilərdi.
    <code>sehife_sayi</code> hesablanmasında <code>Math.max(1, ...)</code> var:
    cəm 0 olsa da frontend "1 səhifə" görür, "0 səhifə" yox.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=2,
    ad="Struktur filtri DTO-su",
    a="""Mərkəzlər siyahısında istifadəçi tipə, aktivliyə görə süzgəc qoymalı və
    istədiyi sütun üzrə sıralamalıdır. Bu sahələrin adları birbaşa SQL/Prisma
    sorğusuna düşdüyü üçün onlar <strong>mütləq yoxlanılmalıdır</strong> — əks halda
    istifadəçi <code>?tip=&lt;script&gt;</code> kimi dəyər göndərə bilər. Bu DTO
    icazə verilən tipləri və sıralama sütunlarını sabit siyahı kimi elan edir və
    <code>@IsIn</code> ilə onları yoxlayır.""",
    b=[("src/struktur/dto/merkez-filtr.dto.ts",
        fayl("src/struktur/dto/merkez-filtr.dto.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) İcazə verilən dəyərlər sabit kimi elan olunubmu?
grep -n 'MERKEZ_TIPLERI\\|MERKEZ_SAHELERI' src/struktur/dto/merkez-filtr.dto.ts

# 2) Hər sahədə yoxlama varmı?
grep -nE '@IsIn|@IsBooleanString|@IsOptional' src/struktur/dto/merkez-filtr.dto.ts

# 3) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi\"""",
    c_olmaz="""$ curl "localhost:4000/api/v1/struktur/merkezler?tip=sehv"
   # @IsIn olmasa Prisma/sorğu "sehv" tipini qəbul edər və
   # nəticə BOŞ siyahı olar — istifadəçi səhvini bilməz:

{"setirler":[],"cemi":0,"sehife":1,"limit":20,"sehife_sayı":1}

   # @IsIn ilə isə dərhal aydın xəta gəlir:
{"ugur":false,"xeta":{"kod":"YANLIS_SORGU",
 "mesaj":"Validasiya xətası",
 "detallar":["tip yalnız bunlardan biri ola bilər:
             merkez, katiblik, sobe, sektor"]}}""",
    c_izah="""<code>@IsIn</code> olmasa səhv filtr <strong>sükutla</strong> boş nəticə
    qaytarır — istifadəçi "məlumat yoxdur" düşünür, halbuki özü səhv yazıb. Bu,
    ən çətin tapılan xəta növüdür. <code>@IsBooleanString</code> də vacibdir: URL-dən
    gələn hər şey <strong>mətn</strong>dir, ona görə <code>?aktiv=true</code>
    dəyəri <code>"true"</code> sətri kimi gəlir və onu yoxlamaq lazımdır.""",
    d="""$ npx tsx -e "
import { plainToInstance } from 'class-transformer';
import { validate } from 'class-validator';
import { MerkezFiltrDto } from './src/struktur/dto/merkez-filtr.dto.js';

for (const [ad, xam] of [
  ['düzgün',        { limit: '5', sehife: '2' }],
  ['limit=500',     { limit: '500' }],
  ['sehife=0',      { sehife: '0' }],
  ['tip=sehv',      { tip: 'sehv' }],
  ['siralama=sehv', { siralama: 'sehv' }],
  ['aktiv=belke',   { aktiv: 'belke' }],
] as const) {
  const x = await validate(plainToInstance(MerkezFiltrDto, xam));
  const m = x.flatMap((i) => Object.values(i.constraints ?? {}));
  console.log(ad.padEnd(16), '→', m.length ? m.join(' | ') : '✓ keçdi');
}"

düzgün           → ✓ keçdi
limit=500        → limit 100-dən çox ola bilməz
sehife=0         → sehife ən azı 1 olmalıdır
tip=sehv         → tip yalnız bunlardan biri ola bilər: merkez, katiblik, sobe, sektor
siralama=sehv    → siralama yalnız 'asc' və ya 'desc' ola bilər
aktiv=belke      → aktiv yalnız 'true' və ya 'false' ola bilər""",
    d_izah="""Sistemin vəziyyəti: filtr DTO-su <strong>6 səhv növünü</strong> tutur və
    hər biri öz Azərbaycan dilində mesajını verir. Diqqət yetirin ki, düzgün
    sorğu <code>limit: '5'</code> kimi <strong>sətir</strong> göndərilir, çünki
    URL-dən gələn hər şey sətirdir — <code>@Type(() => Number)</code> isə onu
    ədədə çevirir. Bu çevrilmə olmasa <code>@IsInt</code> həmişə uğursuz olar.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=3,
    ad="Yaratma və yeniləmə DTO-ları",
    a="""Yeni mərkəz yaradılarkən bütün sahələr yoxlanılmalıdır: ad kifayət qədər
    uzundurmu, e-poçt düzgündürmü, telefon formatı uyğundurmu. Yeniləmə zamanı isə
    istifadəçi <strong>yalnız bir sahə</strong> göndərə bilər — qalanı dəyişməməlidir.
    Bu iki tələb fərqli DTO tələb edir, amma <code>PartialType</code> sayəsində
    yeniləmə DTO-sunu əl ilə yazmaq lazım deyil. Bu addım həm validasiya
    qaydalarını, həm də onların təkrarını aradan qaldıran hiyləni göstərir.""",
    b=[
        ("src/struktur/dto/create-merkez.dto.ts",
         fayl("src/struktur/dto/create-merkez.dto.ts")),
        ("src/struktur/dto/update-merkez.dto.ts",
         fayl("src/struktur/dto/update-merkez.dto.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Hər iki fayl yerindədirmi?
ls -l src/struktur/dto/create-merkez.dto.ts src/struktur/dto/update-merkez.dto.ts

# 2) Yeniləmə DTO-su yalnız PartialType-dan ibarətdirmi?
cat src/struktur/dto/update-merkez.dto.ts

# 3) ⚠️ TS1272 — tip ayrıca 'import type' ilə gəlməlidir
grep -n 'import type' src/struktur/dto/create-merkez.dto.ts

# 4) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi\"""",
    c_olmaz="""$ npm run build      # 'import type' unudulsa:

src/struktur/dto/create-merkez.dto.ts:20:9 - error TS1272:
  A type referenced in a decorated signature must be imported
  with 'import type' or a namespace import when 'isolatedModules'
  and 'emitDecoratorMetadata' are enabled.

20   tip?: MerkezTipi;
         ~~~~~~~~~~

  src/struktur/dto/create-merkez.dto.ts:6:26
    'MerkezTipi' was imported here.

Found 1 error(s).""",
    c_izah="""<code>MerkezTipi</code> bir <strong>tipdir</strong>, dəyər deyil. Dekoratorlu
    sahədə istifadə olunanda TypeScript onu <code>emitDecoratorMetadata</code> üçün
    işlədilən koda çevirməyə çalışır və alınmır — <code>TS1272</code> xətası çıxır.
    Həll: tipi ayrıca <code>import type</code> ilə gətirmək. Bu, layihənin
    ən tez-tez rast gəlinən xətasıdır və <strong>yalnız build zamanı</strong> üzə
    çıxır — redaktorda hər şey qaydasında görünür.""",
    d="""$ npx tsx -e "
import { plainToInstance } from 'class-transformer';
import { validate } from 'class-validator';
import { CreateMerkezDto } from './src/struktur/dto/create-merkez.dto.js';
import { UpdateMerkezDto } from './src/struktur/dto/update-merkez.dto.js';

for (const [ad, xam] of [
  ['düzgün ad',      { ad: 'Yeni Mərkəz' }],
  ['ad 2 simvol',    { ad: 'ab' }],
  ['email səhv',     { ad: 'Yeni Mərkəz', email: 'pis' }],
  ['telefon səhv',   { ad: 'Yeni Mərkəz', telefon: '123' }],
  ['tarix səhv',     { ad: 'Yeni Mərkəz', yaradilma_tarixi: '15.02.2024' }],
  ['tip səhv',       { ad: 'Yeni Mərkəz', tip: 'sehv' }],
] as const) {
  const x = await validate(plainToInstance(CreateMerkezDto, xam));
  const m = x.flatMap((i) => Object.values(i.constraints ?? {}));
  console.log(ad.padEnd(16), '→', m.length ? m.join(' | ') : '✓ keçdi');
}

const u = plainToInstance(UpdateMerkezDto, { telefon: '+994 12 111 22 33' });
console.log('yeniləmə — yalnız telefon →', (await validate(u)).length ? 'XƏTA' : '✓ keçdi');"

düzgün ad        → ✓ keçdi
ad 2 simvol      → Ad ən azı 3 simvol olmalıdır
email səhv       → E-poçt ünvanı yanlışdır
telefon səhv     → Telefon formatı yanlışdır (+994 12 599 08 08)
tarix səhv       → Tarix İL-AY-GÜN formatında olmalıdır (2024-02-15)
tip səhv         → tip yalnız bunlardan biri ola bilər: merkez, katiblik, sobe, sektor
yeniləmə — yalnız telefon → ✓ keçdi""",
    d_izah="""Sistemin vəziyyəti: yaratma DTO-su <strong>5 səhv növünü</strong> tutur,
    yeniləmə DTO-su isə yalnız bir sahə ilə işləyir. Son sətir xüsusilə vacibdir:
    <code>UpdateMerkezDto</code> <code>PartialType</code> sayəsində bütün sahələri
    istəyə bağlı edir, ona görə <code>{ telefon: ... }</code> göndərmək kifayətdir —
    ad, e-poçt və qalan sahələr <strong>toxunulmur</strong>. <code>PartialType</code>
    olmasa 6 sahəni əl ilə <code>@IsOptional()</code> etmək lazım gələrdi.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=4,
    ad="StrukturService — tam servis (oxuma və yazma)",
    a="""Servis qatı controller ilə baza arasında dayanır: controller yalnız HTTP-yə
    cavabdehdir, baza isə xam SQL/Prisma bilir. <code>StrukturService</code> filtr
    DTO-sunu Prisma sorğusuna çevirir, səhifələyir və nəticəni vahid formada
    qaytarır. Bu addımda <strong>altı metod</strong> yaranır: üç oxuma
    (<code>merkezler</code>, <code>merkezStatistikasi</code>, <code>merkez</code>)
    və üç yazma (<code>yarat</code>, <code>yenile</code>, <code>sil</code>).
    Yazmada baza xətaları tutulub aydın Azərbaycan dilində 409 cavabına çevrilir.""",
    b=[("src/struktur/struktur.service.ts", fayl("src/struktur/struktur.service.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Üç oxuma metodu yerindədirmi?
grep -nE 'async (merkezler|merkezStatistikasi|merkez)\\(' src/struktur/struktur.service.ts

# 2) Səhifələmə köməkçisi işlədilirmi?
grep -n 'sehifeHesabla\\|sehifelenmis' src/struktur/struktur.service.ts

# 3) ⚠️ Xam SQL-də ::int çevirməsi varmı?
grep -n '::int' src/struktur/struktur.service.ts

# 4) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi\"""",
    c_olmaz="""$ curl "localhost:4000/api/v1/struktur/merkezler/statistika"
   # ① ::int çevirməsi olmasa:

{"ugur":false,"xeta":{"kod":"DAXILI_XETA",
 "mesaj":"Do not know how to serialize a BigInt"}}

[Nest] ERROR [XETA] GET /api/v1/struktur/merkezler/statistika —
  Do not know how to serialize a BigInt

$ curl -X DELETE localhost:4000/api/v1/struktur/merkezler/2
   # ② Silmədən əvvəl ön yoxlama olmasa:

HTTP/1.1 500 Internal Server Error

{"ugur":false,"xeta":{"kod":"DAXILI_XETA",
 "mesaj":"\nInvalid `prisma.merkezler.delete()` invocation:\n\n\nForeign key
          constraint violated on the constraint: `emekdaslar_merkez_id_fkey`"}}

[Nest] ERROR [XETA] DELETE /api/v1/struktur/merkezler/2 —
  Foreign key constraint violated on the constraint: `emekdaslar_merkez_id_fkey`""",
    c_izah="""İki fərqli <strong>500</strong> səbəbi var və ikisi də yalnız canlı
    sorğuda üzə çıxır — build və tip yoxlaması onları <strong>tutmur</strong>.
    <br><br>
    <strong>① BigInt:</strong> PostgreSQL-də <code>count(*)</code>
    <code>bigint</code> qaytarır, JavaScript isə <code>BigInt</code>-i JSON-a
    çevirə bilmir. <code>$queryRaw</code>-un nəticə tipini biz özümüz elan
    etdiyimiz üçün TypeScript bunu görmür.
    <br><br>
    <strong>② Xarici açar:</strong> ön yoxlama olmadan
    <code>prisma.merkezler.delete()</code> çağırılsa baza xəta verir və mesaj
    <em>texniki zibildir</em>. Ön yoxlama ilə cavab aydın olur:
    <em>«Elmi-pedaqoji tədqiqatlar mərkəzi» silinmir — ona bağlı 7 şöbə,
    2 əməkdaş var</em>.""",
    d="""$ npx tsc --noEmit -p tsconfig.build.json
   (çıxış yoxdur — KEÇDİ)

$ psql -U arti_user -w -d arti_baza -c "
    SELECT m.ad,
           count(DISTINCT s.id)::int AS shobe_sayi,
           count(DISTINCT e.id)::int AS emekdas_sayi
      FROM struktur.merkezler m
      LEFT JOIN struktur.shobeler  s ON s.merkez_id = m.id AND s.aktiv
      LEFT JOIN kadrlar.emekdaslar e ON e.merkez_id = m.id AND e.aktiv
     GROUP BY m.id, m.ad ORDER BY m.ad LIMIT 4;"

              ad               | shobe_sayi | emekdas_sayi
-------------------------------+------------+--------------
 Elmi katiblik                 |          0 |            2
 Elmi-pedaqoji tədqiqatlar mərkəzi |      7 |            2
 Funksional şöbələr            |          8 |            3
 Metodik dəstək mərkəzi        |          6 |            1""",
    d_izah="""Sistemin vəziyyəti: servis qatı hazırdır — <code>merkezler()</code> siyahını
    səhifələyir, <code>merkez()</code> bir sətri qaytarır, <code>merkezStatistikasi()</code>
    isə <code>GROUP BY</code> ilə şöbə və əməkdaş sayını hesablayır. Yuxarıdaki SQL
    sorğusu <strong>servisin içindəki sorğunun eynidir</strong> — onu psql-də işlədib
    nəticəni əvvəlcədən yoxlaya bilərsiniz. <code>count(DISTINCT ...)</code> işlədilir,
    çünki iki <code>LEFT JOIN</code> bir-birini çoxaldır: DISTINCT olmasa 7 şöbə və
    2 əməkdaş olan mərkəz <code>14</code> əməkdaş göstərərdi.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=5,
    ad="StrukturController və StrukturModule",
    a="""Controller HTTP qatıdır: URL-i metoda bağlayır, gələn məlumatı DTO-ya
    çevirir və servisi çağırır. Burada heç bir baza məntiqi olmamalıdır — controller
    yalnız <em>tərcüməçi</em>dir. <code>StrukturModule</code> isə ikisini bir paketə
    yığır və kök modula bir sətirlə qoşulur. Bu addımdan sonra endpoint-lər
    <strong>ilk dəfə canlı olur</strong>.""",
    b=[
        ("src/struktur/struktur.controller.ts", fayl("src/struktur/struktur.controller.ts")),
        ("src/struktur/struktur.module.ts", fayl("src/struktur/struktur.module.ts")),
        ("src/app.module.ts", app_module_araliq()),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Altı endpoint yerindədirmi?
grep -nE '@(Get|Post|Patch|Delete)' src/struktur/struktur.controller.ts

# 2) Controller-də baza məntiqi YOXDUR (yalnız servis çağırışı)
grep -n 'this.prisma\\|\\$queryRaw' src/struktur/struktur.controller.ts || \\
  echo "✓ controller-də birbaşa baza sorğusu yoxdur"

# 3) Modul kök modula qoşulubmu?
grep -n 'StrukturModule' src/app.module.ts

# 4) Build
npm run build && echo "✓ build keçdi\"""",
    c_olmaz="""$ curl localhost:4000/api/v1/struktur/merkezler
   # StrukturModule app.module.ts-də qeyd olunmasa:

HTTP/1.1 404 Not Found

{"ugur":false,"xeta":{"kod":"TAPILMADI",
 "mesaj":"Cannot GET /api/v1/struktur/merkezler"},
 "yol":"/struktur/merkezler","vaxt":"2026-09-21T03:44:53.425Z"}

   # Server logunda StrukturController ümumiyyətlə YOXDUR:
[Nest] LOG [RoutesResolver] SaglamliqController {/api/v1}: +7ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/saglamliq, GET} route +0ms
   (StrukturController sətri yoxdur)""",
    c_izah="""<code>@Module</code> dekoratoru sadəcə qeydiyyatdır — NestJS yalnız
    <code>app.module.ts</code>-in <code>imports</code> siyahısında olan modulları
    yükləyir. Fayl mövcud olsa da, modul qeyd olunmasa controller
    <strong>ümumiyyətlə yaranmır</strong> və marshrut qeydiyyatdan keçmir.
    Bu, ən tez-tez edilən səhvdir: fayllar yazılır, amma sonuncu sətir unudulur.""",
    d="""$ npm run build
> ds-backend@0.1.0 build
> nest build

$ node dist/main.js

[Nest] LOG [InstanceLoader] SaglamliqModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] StrukturModule dependencies initialized +0ms
[Nest] LOG [RoutesResolver] SaglamliqController {/api/v1}: +7ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1, GET} route +1ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/saglamliq, GET} route +0ms
[Nest] LOG [RoutesResolver] StrukturController {/api/v1/struktur/merkezler}: +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler/statistika, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler/:id, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler, POST} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler/:id, PATCH} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler/:id, DELETE} route +0ms
[Nest] LOG [BAZA] Baza bağlantısı açıldı
[Nest] LOG [BAŞLANGIC] API hazırdır → http://localhost:4000/api/v1""",
    d_izah="""Sistemin vəziyyəti: <code>StrukturController</code> yükləndi və
    <strong>6 marshrut</strong> qeydiyyatdan keçdi. Diqqət yetirin —
    <code>/struktur/merkezler/statistika</code> sətri <code>/struktur/merkezler/:id</code>-dən
    <strong>əvvəl</strong> gəlir. Bu, controller-dəki <code>@Get('statistika')</code>
    metodunun <code>@Get(':id')</code>-dən əvvəl yazılmasının nəticəsidir: NestJS
    marshrutları <em>yazılma sırası ilə</em> yoxlayır, ona görə tərs olsa
    "statistika" sözü <code>:id</code> kimi qəbul edilər və
    <code>ParseIntPipe</code> 400 verərdi.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=6,
    ad="Kadrlar filtri DTO-su",
    a="""Əməkdaşlar siyahısında istifadəçi mərkəzə, şöbəyə və aktivliyə görə
    süzgəc qoymalıdır. Bu DTO struktur filtri ilə eyni səhifələmə əsasını işlədir,
    amma öz sahələrini əlavə edir — <code>SehifeSorghu</code>-dan miras
    <code>extends</code> ilə alınır. Miras sayəsində <code>sehife</code>,
    <code>limit</code>, <code>axtar</code> və <code>siralama</code> yenidən
    yazılmır.""",
    b=[("src/kadrlar/dto/emekdas-filtr.dto.ts",
        fayl("src/kadrlar/dto/emekdas-filtr.dto.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayl yerindədirmi?
ls -l src/kadrlar/dto/emekdas-filtr.dto.ts

# 2) Ortaq əsasdan MİRAS alırmı?
grep -n 'extends SehifeSorghu' src/kadrlar/dto/emekdas-filtr.dto.ts

# 3) Öz sahələri yoxlanılırmı?
grep -nE '@Type|@IsInt|@IsBooleanString' src/kadrlar/dto/emekdas-filtr.dto.ts

# 4) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi\"""",
    c_olmaz="""$ curl "localhost:4000/api/v1/kadrlar/emekdaslar?merkez_id=abc"
   # @Type(() => Number) olmasa:

{"ugur":false,"xeta":{"kod":"YANLIS_SORGU",
 "mesaj":"Validasiya xətası",
 "detallar":["merkez_id tam ədəd olmalıdır"]}}

   # Amma @IsInt TƏK BAŞINA olsa və @Type olmasa, "2" sətri
   # heç vaxt ədədə çevrilməz və HƏMİŞƏ xəta verərdi —
   # düzgün sorğu belə keçməzdi.""",
    c_izah="""<code>@Type(() => Number)</code> və <code>@IsInt()</code> <strong>cütlükdə</strong>
    işləyir. URL-dən gələn <code>"2"</code> sətirdir; <code>@Type</code> onu
    <code>2</code> ədədinə çevirir, <code>@IsInt</code> isə çevrilmiş dəyəri yoxlayır.
    Biri olmasa ya hər şey səhv olur, ya da heç nə yoxlanılmır.
    <code>extends SehifeSorghu</code> isə vacibdir: miras olmasa
    <code>?limit=500</code> yoxlanılmadan keçər və baza lazımsız yüklənər.""",
    d="""$ npx tsx -e "
import { plainToInstance } from 'class-transformer';
import { validate } from 'class-validator';
import { EmekdasFiltrDto } from './src/kadrlar/dto/emekdas-filtr.dto.js';

for (const [ad, xam] of [
  ['düzgün',          { merkez_id: '2', limit: '5' }],
  ['merkez_id=abc',   { merkez_id: 'abc' }],
  ['merkez_id=0',     { merkez_id: '0' }],
  ['aktiv=belke',     { aktiv: 'belke' }],
  ['MİRAS: limit=500',{ limit: '500' }],
  ['MİRAS: sehife=0', { sehife: '0' }],
] as const) {
  const x = await validate(plainToInstance(EmekdasFiltrDto, xam));
  const m = x.flatMap((i) => Object.values(i.constraints ?? {}));
  console.log(ad.padEnd(20), '→', m.length ? m.join(' | ') : '✓ keçdi');
}"

düzgün               → ✓ keçdi
merkez_id=abc        → merkez_id tam ədəd olmalıdır
merkez_id=0          → merkez_id ən azı 1 olmalıdır
aktiv=belke          → aktiv yalnız 'true' və ya 'false' ola bilər
MİRAS: limit=500     → limit 100-dən çox ola bilməz
MİRAS: sehife=0      → sehife ən azı 1 olmalıdır""",
    d_izah="""Sistemin vəziyyəti: kadrlar filtri hazırdır və son iki sətir
    <strong>mirasın işlədiyini</strong> sübut edir — <code>limit</code> və
    <code>sehife</code> bu faylda ümumiyyətlə yazılmayıb, amma yoxlanılır.
    <code>merkez_id=abc</code> üçün mesaj gəlir, çünki <code>@Type</code> onu
    <code>NaN</code>-a çevirir və <code>@IsInt</code> tutur. Bu, istifadəçinin
    <code>?merkez_id=abc</code> yazdıqda boş siyahı yerinə aydın xəta görməsi
    deməkdir.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=7,
    ad="KadrlarService — JOIN ilə tam profil",
    a="""Əməkdaş cədvəlində yalnız <code>merkez_id</code>, <code>shobe_id</code>,
    <code>vezife_id</code> kimi <strong>rəqəmlər</strong> saxlanılır. İstifadəçiyə isə
    "Elmi katiblik / Elmi şöbə / Aparıcı mütəxəssis" kimi <strong>adlar</strong> lazımdır.
    Ona görə altı cədvəli <code>LEFT JOIN</code> ilə birləşdiririk. Bu addımda həm
    JOIN sorğusu, həm <code>::int</code>/<code>::float8</code> çevirmələri, həm də
    filtr şərtinin <em>bir dəfə</em> qurulub iki sorğuda işlədilməsi göstərilir.""",
    b=[("src/kadrlar/kadrlar.service.ts", fayl("src/kadrlar/kadrlar.service.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Üç metod yerindədirmi?
grep -nE 'async (emekdaslar|emekdas|icmal)\\(' src/kadrlar/kadrlar.service.ts

# 2) Neçə cədvəl JOIN olunur?
grep -c 'LEFT JOIN' src/kadrlar/kadrlar.service.ts

# 3) ⚠️ Çevirmələr yerindədirmi?
grep -nE '::int|::float8|::text|::boolean' src/kadrlar/kadrlar.service.ts | head

# 4) ⚠️ Filtr şərti BİR DƏFƏ qurulur (serh metodu)
grep -n 'private serh\\|Prisma.sql' src/kadrlar/kadrlar.service.ts

# 5) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi\"""",
    c_olmaz="""$ curl "localhost:4000/api/v1/kadrlar/emekdaslar?limit=2"
   # e.id::int çevirməsi olmasa:

{"ugur":false,"xeta":{"kod":"DAXILI_XETA",
 "mesaj":"Do not know how to serialize a BigInt"}}

   # e.maas::float8 olmasa maas SƏTİR kimi gəlir:
{"maas":"2800.00"}     ← rəqəm deyil, SÖZ!
   # Frontend onunla hesablama apara bilməz.""",
    c_izah="""İki fərqli problem var. Birincisi: <code>emekdaslar.id</code> sütunu
    PostgreSQL-də <code>bigint</code>-dir — <code>::int</code> olmasa JSON xəta verir.
    İkincisi: <code>maas</code> sütunu <code>numeric(12,2)</code>-dir; Prisma onu
    JavaScript-də <code>Decimal</code> obyektinə çevirir və JSON-da
    <strong>sətir</strong> kimi görünür. <code>::float8</code> isə həqiqi
    <code>number</code> qaytarır. Filtr şərtinin bir dəfə qurulması da vacibdir:
    <code>serh</code> metodu olmasa eyni 8 sətirlik <code>WHERE</code> həm siyahıda,
    həm saymada təkrarlanar və zamanla biri dəyişib digəri yaddan çıxar.""",
    d="""$ npx tsx -e "
import { PrismaService } from './src/prisma/prisma.service.js';
import { KadrlarService } from './src/kadrlar/kadrlar.service.js';
const s = new KadrlarService(new PrismaService());
const c = await s.emekdaslar({ sehife: 1, limit: 2, siralama: 'asc' });
for (const x of c.setirler)
  console.log(x.id, '|', x.ad, x.soyad, '|', x.merkez, '|', x.vezife,
              '| maas:', x.maas, typeof x.maas);
console.log('cemi:', c.cemi, 'sehife_sayi:', c.sehife_sayi);
await s['prisma'].\$disconnect?.();" 2>/dev/null

13 | Elçin Babayev | Təhsil texnologiyaları mərkəzi | Aparıcı mütəxəssis | maas: 1300 number
4 | İlham Cavadov | Metodik dəstək mərkəzi | Direktor müavini | maas: 2800 number
cemi: 14 sehife_sayi: 7""",
    d_izah="""Sistemin vəziyyəti: servis altı cədvəli birləşdirib tam profil
    qaytarır. Son sütun xüsusilə vacibdir: <code>maas: 1300 number</code> —
    yəni <strong>rəqəm</strong>, sətir deyil. <code>::float8</code> olmasa burada
    <code>'1300.00' string</code> yazardı. Həmçinin <code>cemi: 14</code> və
    <code>sehife_sayi: 7</code> göstərir ki, filtr şərti həm siyahıda, həm saymada
    <strong>eyni</strong> işləyir — <code>serh</code> metodu bunu təmin edir.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=8,
    ad="KadrlarController və KadrlarModule",
    a="""Controller üç endpoint açır: siyahı, icmal və bir əməkdaş. Burada diqqət
    yetirilməli bir incəlik var — <code>@Get('icmal')</code> <strong>mütləq</strong>
    <code>@Get(':id')</code>-dən əvvəl yazılmalıdır. NestJS marshrutları yazılma
    sırası ilə yoxlayır; tərs olsa "icmal" sözü <code>:id</code> kimi qəbul edilər və
    <code>ParseIntPipe</code> 400 verər. Modul isə əvvəlki addımdaki kimi kök
    modula qoşulur.""",
    b=[
        ("src/kadrlar/kadrlar.controller.ts", fayl("src/kadrlar/kadrlar.controller.ts")),
        ("src/kadrlar/kadrlar.module.ts", fayl("src/kadrlar/kadrlar.module.ts")),
        ("src/app.module.ts", fayl("src/app.module.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Üç endpoint yerindədirmi?
grep -nE '@Get' src/kadrlar/kadrlar.controller.ts

# 2) ⚠️ 'icmal' ':id'-dən ƏVVƏL yazılıbmı?
grep -n "@Get('icmal')\\|@Get(':id')" src/kadrlar/kadrlar.controller.ts

# 3) Modul kök modula qoşulubmu?
grep -n 'KadrlarModule' src/app.module.ts

# 4) Build
npm run build && echo "✓ build keçdi\"""",
    c_olmaz="""$ npm run build      # sıra TƏRS olsa:

$ node dist/main.js
[Nest] LOG [RouterExplorer] Mapped {/api/v1/kadrlar/emekdaslar/:id, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/kadrlar/emekdaslar/icmal, GET} route +0ms

$ curl localhost:4000/api/v1/kadrlar/emekdaslar/icmal
{"ugur":false,"xeta":{"kod":"YANLIS_SORGU",
 "mesaj":"Validasiya xətası",
 "detallar":["Validation failed (numeric string is expected)"]}}

   # 'icmal' sözü :id yerinə düşdü və ParseIntPipe onu rəqəmə çevirə bilmədi!""",
    c_izah="""Marshrut sırası <strong>sükutla</strong> işləyən səhvdir: build keçir,
    server qalxır, amma bir endpoint tamamilə işləməz olur. Üstəlik xəta mesajı
    ingiliscə və anlaşılmazdır (<em>numeric string is expected</em>) — istifadəçi
    heç vaxt "icmal" endpoint-inin sıra səbəbindən sındığını təxmin etməz.
    Qayda sadədir: <strong>sabit yollar dəyişən yollardan əvvəl</strong>.""",
    d="""$ node dist/main.js

[Nest] LOG [InstanceLoader] KadrlarModule dependencies initialized +0ms
[Nest] LOG [RoutesResolver] KadrlarController {/api/v1/kadrlar/emekdaslar}: +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/kadrlar/emekdaslar, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/kadrlar/emekdaslar/icmal, GET} route +1ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/kadrlar/emekdaslar/:id, GET} route +0ms
[Nest] LOG [BAZA] Baza bağlantısı açıldı
[Nest] LOG [BAŞLANGIC] API hazırdır → http://localhost:4000/api/v1

$ curl -s localhost:4000/api/v1/kadrlar/emekdaslar/icmal | python3 -m json.tool | head -12
{
    "cemi": 14,
    "aktiv": 14,
    "merkez_uzre": [
        { "ad": "Funksional şöbələr", "say": 3 },
        { "ad": "Elmi katiblik", "say": 2 },
        { "ad": "Elmi-pedaqoji tədqiqatlar mərkəzi", "say": 2 },
        { "ad": "Qiymətləndirmə, təhlil və monitorinq mərkəzi", "say": 2 }
    ],""",
    d_izah="""Sistemin vəziyyəti: <code>KadrlarModule</code> yükləndi və üç marshrut
    qeydiyyatdan keçdi. Log sırasına baxın: <code>icmal</code> sətri
    <code>:id</code>-dən əvvəl gəlir — düzgün sıradır. <code>icmal</code> endpoint-i
    işləyir və 14 əməkdaşı mərkəzlər üzrə bölür. Bu andan etibarən backend-in
    <strong>11 marshrutu</strong> var.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=9,
    ad="Build və tam canlı yoxlama",
    a="""Bütün modullar yerindədir — indi serveri qaldırıb <strong>hər endpoint-i</strong>
    yoxlayırıq. Bu addımda 11 marshrutun hamısı, filtr/axtarış/sıralama, validasiya
    xətaları və yazma əməliyyatlarının konflikt halları canlı sınanır. Bu, dərsin
    ən vacib yoxlamasıdır: burada hər şey <em>birlikdə</em> işləməlidir.""",
    b=[
        ("Terminal 1 — serveri qaldır", """cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST

# Lazım olsa köhnə serveri dayandır
lsof -ti:4000 && kill $(lsof -ti:4000)

npm run start:dev"""),
        ("Terminal 2 — yoxla", """A=http://localhost:4000/api/v1

# ── 1) SƏHİFƏLƏMƏ ──
curl -s "$A/struktur/merkezler?limit=3" | python3 -m json.tool

# ── 2) FİLTR + AXTARIŞ + SIRALAMA ──
curl -s "$A/struktur/merkezler?tip=katiblik"
curl -s "$A/struktur/merkezler?axtar=elm"
curl -s "$A/struktur/merkezler?sirala=id&siralama=desc&limit=1"

# ── 3) STATİSTİKA ──
curl -s "$A/struktur/merkezler/statistika" | python3 -m json.tool | head -12

# ── 4) KADRLAR — JOIN ilə tam profil ──
curl -s "$A/kadrlar/emekdaslar?limit=1" | python3 -m json.tool

# ── 5) İCMAL ──
curl -s "$A/kadrlar/emekdaslar/icmal" | python3 -m json.tool | head -12"""),
        ("Terminal 2 — xəta halları", """A=http://localhost:4000/api/v1

printf 'limit=500        → %s\\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/struktur/merkezler?limit=500")"
printf 'tip=sehv         → %s\\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/struktur/merkezler?tip=sehv")"
printf 'id=999999        → %s\\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/struktur/merkezler/999999")"
printf 'id=abc           → %s\\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/struktur/merkezler/abc")"
printf 'emekdas 999999   → %s\\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/kadrlar/emekdaslar/999999")"
printf 'əlavə parametr   → %s\\n' "$(curl -s -o /dev/null -w '%{http_code}' "$A/struktur/merkezler?yoxdur=1")

# ── Yazma əməliyyatları (test mərkəzi yaradıb silirik) ──
J='Content-Type: application/json'
AD="Test Mərkəz $(date +%s)"

ID=$(curl -s -X POST "$A/struktur/merkezler" -H "$J" \\
  -d "{\\"ad\\":\\"$AD\\",\\"tip\\":\\"sektor\\"}" \\
  | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")
echo "yaradıldı: $ID"

printf 'eyni ad (409)    → %s\\n' "$(curl -s -o /dev/null -w '%{http_code}' \\
  -X POST "$A/struktur/merkezler" -H "$J" -d "{\\"ad\\":\\"$AD\\"}")"
printf 'bağlı mərkəz (409) → %s\\n' "$(curl -s -o /dev/null -w '%{http_code}' \\
  -X DELETE "$A/struktur/merkezler/2")"

curl -s -X PATCH "$A/struktur/merkezler/$ID" -H "$J" \\
  -d '{"telefon":"+994 12 111 22 33"}' | python3 -c \\
  "import json,sys;d=json.load(sys.stdin);print('patch telefon:',d['telefon'])"

curl -s -X DELETE "$A/struktur/merkezler/$ID" | python3 -m json.tool"""),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Neçə marshrut qeydiyyatdadır?
curl -s http://localhost:4000/docs-json | python3 -c "
import json, sys
d = json.load(sys.stdin)
cemi = 0
for yol in sorted(d['paths']):
    for m in d['paths'][yol]:
        cemi += 1
        print(f'  {m.upper():6s} {yol}')
print('  CƏMİ:', cemi, 'marshrut')
"

# 2) Baza təmiz qalıbmı?
export PGPASSWORD=arti_secret_2025
psql -U arti_user -w -d arti_baza -tAc \\
  "SELECT count(*)::int FROM struktur.merkezler" | xargs echo "  mərkəz sayı:"

# 3) Qalıq test sətri varmı?
psql -U arti_user -w -d arti_baza -tAc \\
  "SELECT id || ' | ' || ad FROM struktur.merkezler WHERE ad LIKE 'Test Mərkəz%'"
echo "  (boşdursa təmizdir)\"""",
    c_olmaz="""$ curl -s "localhost:4000/api/v1/kadrlar/emekdaslar?limit=2"
   # Uyğunlaşdırılmamış endpoint (məsələn ServeStaticModule) olmasa:

{"ugur":false,"xeta":{"kod":"TAPILMADI",
 "mesaj":"Cannot GET /api/v1/kadrlar/emekdaslar"},
 "yol":"/kadrlar/emekdaslar","vaxt":"2026-09-21T03:44:53.425Z"}""",
    c_izah="""Yoxlama bloku üç şeyi təsdiqləyir: <strong>11 marshrut</strong> qeydiyyatdadır,
    baza <strong>təmiz qalıb</strong> (test sətri silinib) və xəta halları düzgün
    kod qaytarır. Son yoxlama xüsusilə vacibdir — test mərkəzi silinməsə baza
    zamanla zibillə dolur və növbəti dəfə <code>cemi</code> rəqəmi səhv çıxır.""",
    d="""$ curl -s localhost:4000/docs-json | python3 -c "..."
  GET    /api/v1
  GET    /api/v1/kadrlar/emekdaslar
  GET    /api/v1/kadrlar/emekdaslar/icmal
  GET    /api/v1/kadrlar/emekdaslar/{id}
  GET    /api/v1/saglamliq
  GET    /api/v1/struktur/merkezler
  POST   /api/v1/struktur/merkezler
  GET    /api/v1/struktur/merkezler/statistika
  GET    /api/v1/struktur/merkezler/{id}
  PATCH  /api/v1/struktur/merkezler/{id}
  DELETE /api/v1/struktur/merkezler/{id}
  CƏMİ: 11 marshrut

$ curl -s "localhost:4000/api/v1/struktur/merkezler?limit=2" | python3 -m json.tool
{
    "setirler": [
        { "id": 1, "ad": "Elmi katiblik", "tip": "katiblik", "aktiv": true },
        { "id": 2, "ad": "Elmi-pedaqoji tədqiqatlar mərkəzi",
          "tip": "merkez", "aktiv": true }
    ],
    "cemi": 10,
    "sehife": 1,
    "limit": 2,
    "sehife_sayi": 5
}

$ curl -s "localhost:4000/api/v1/kadrlar/emekdaslar?limit=1" | python3 -m json.tool
{
    "setirler": [
        {
            "id": 13,
            "ad": "Elçin",
            "soyad": "Babayev",
            "ata_adi": "Sərvər",
            "maas": 1300,
            "merkez": "Təhsil texnologiyaları mərkəzi",
            "shobe": null,
            "vezife": "Aparıcı mütəxəssis",
            "elmi_derece": "Magistr",
            "is_statusu": "Aktiv"
        }
    ],
    "cemi": 14, "sehife": 1, "limit": 1, "sehife_sayi": 14
}

════════════ XƏTA HALLARI ════════════
limit=500        → 400
tip=sehv         → 400
id=999999        → 404
id=abc           → 400
emekdas 999999   → 404
əlavə parametr   → 400

════════ YAZMA ƏMƏLİYYATLARI ════════════
yaradıldı: 270
eyni ad (409)      → 409
bağlı mərkəz (409) → 409
patch telefon: +994 12 111 22 33
{ "silindi": 270, "ad": "Test Mərkəz 1789962481" }""",
    d_izah="""<strong>Backend-in bu andaki tam durumu:</strong>
    <ul>
      <li><strong>11 marshrut</strong> — 2 sağlamlıq, 6 struktur, 3 kadrlar.</li>
      <li><strong>Səhifələmə</strong> hər iki siyahıda işləyir:
          <code>cemi: 10, sehife_sayi: 5</code> (limit 2) və
          <code>cemi: 14, sehife_sayi: 14</code> (limit 1).</li>
      <li><strong>JOIN-lar</strong> işləyir: əməkdaşın mərkəzi, vəzifəsi və
          elmi dərəcəsi <em>adlarla</em> gəlir; <code>maas</code> isə
          <code>1300</code> — <strong>rəqəm</strong>.</li>
      <li><strong>Validasiya</strong> 4 fərqli səhvi tutur (400), tapılmayan
          sətirlər 404, konfliktlər 409 verir.</li>
      <li><strong>Baza təmizdir</strong>: yaradılan test mərkəzi silinib,
          <code>merkezler</code> yenə 10 sətirdir.</li>
    </ul>""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=10,
    ad="Unit testlər",
    a="""Unit testlər servisi <strong>təcrid olunmuş</strong> yoxlayır: baza
    əvəzinə saxta obyekt işlədilir, ona görə testlər sürətli olur və baza
    olmayan mühitdə də keçir. Bu addımda iki fayl yaranır: səhifələmə
    funksiyalarının riyaziyyatı və <code>StrukturService</code>-in məntiqi.
    Sərhəd halları (limit 5000, mənfi səhifə, cəm 0) xüsusilə yoxlanılır —
    çünki səhvlər məhz orada gizlənir.""",
    b=[
        ("src/common/dto/sehife.dto.spec.ts", fayl("src/common/dto/sehife.dto.spec.ts")),
        ("src/struktur/struktur.service.spec.ts",
         fayl("src/struktur/struktur.service.spec.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Test faylları yerindədirmi?
ls -l src/common/dto/sehife.dto.spec.ts src/struktur/struktur.service.spec.ts

# 2) Sərhəd halları yoxlanılırmı?
grep -n '5000\\|mənfi\\|-7\\|0 olarsa' src/common/dto/sehife.dto.spec.ts

# 3) Testləri işlət
npm test""",
    c_olmaz="""$ npm test      # səhifələmə kəsilməsə (limit 5000 qəbul edilsə):

 FAIL  src/common/dto/sehife.dto.spec.ts > limit 100-dən yuxarı KƏSİLİR
 AssertionError: expected 5000 to be 100
   - Expected: 100
   + Received: 5000""",
    c_izah="""Testlər kodun <strong>nə etdiyini</strong> deyil, <code>nə etməli
    olduğunu</code> yazır. Sərhəd dəyərləri (5000, -7, 0) yoxlanmasa
    <code>Math.min(100, ...)</code> sətri təsadüfən silinsə heç kim fərqini
    görməz — kod işləyir, sadəcə baza lazımsız yüklənir. Test isə dərhal
    <code>expected 5000 to be 100</code> deyə xəbərdarlıq edir.""",
    d="""$ npm test

 RUN  v4.1.11 /Users/royatalibova/Deepseek_ARTI/DS_Backend

 ✓ src/common/dto/sehife.dto.spec.ts (9 tests) 2ms
 ✓ src/saglamliq/saglamliq.service.spec.ts (3 tests) 39ms
 ✓ src/struktur/struktur.service.spec.ts (9 tests) 38ms

 Test Files  3 passed (3)
      Tests  21 passed (21)
   Start at  07:43:24
   Duration  334ms""",
    d_izah="""Sistemin vəziyyəti: <strong>21 unit test</strong> keçir və cəmi
    <strong>334 ms</strong> çəkir — çünki baza işlədilmir, hər şey saxta
    obyektlə yoxlanılır. Dərs 1-dən gələn 3 sağlamlıq testi də yerindədir.
    <code>struktur.service.spec.ts</code> faylında <code>shobeler.count</code>
    saxta obyekti 0 qaytarır; test onu 7-yə dəyişib <code>sil()</code>-in
    409 verdiyini yoxlayır — yəni <strong>konflikt məntiqi də təcrid olunmuş</strong>
    şəkildə sınanır.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=11,
    ad="e2e testlər — struktur",
    a="""e2e testlər real <code>AppModule</code>-u qaldırır və <code>supertest</code>
    ilə <strong>həqiqi HTTP sorğusu</strong> göndərir — yəni bütün zəncir
    sınanır: marshrut, DTO validasiyası, servis, baza. Bu testlər real sətir
    yaradıb silir, ona görə <code>afterAll</code>-da təmizləmə mütləqdir.
    Struktur testi 13 yoxlama aparır.""",
    b=[("test/struktur.e2e-spec.ts", fayl("test/struktur.e2e-spec.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayl yerindədirmi?
ls -l test/struktur.e2e-spec.ts

# 2) ⚠️ Təmizləmə var?
grep -n 'afterAll\\|delete(' test/struktur.e2e-spec.ts | head -4

# 3) Testləri işlət
npx vitest run --config vitest.config.e2e.ts test/struktur.e2e-spec.ts

# 4) Baza təmiz qaldı?
export PGPASSWORD=arti_secret_2025
psql -U arti_user -w -d arti_baza -tAc \\
  "SELECT count(*)::int FROM struktur.merkezler WHERE ad LIKE 'E2E %'"
""",
    c_olmaz="""$ npx vitest run --config vitest.config.e2e.ts test/struktur.e2e-spec.ts
   # afterAll-da təmizləmə olmasa, hər işə salmada bir sətir qalır:

 ✓ test/struktur.e2e-spec.ts (13 tests)

$ psql ... "SELECT count(*) FROM struktur.merkezler WHERE ad LIKE 'E2E %'"
 7        ← 7 dəfə işlədildi, 7 zibil sətri qaldı!""",
    c_izah="""e2e testlər <strong>real bazanı dəyişir</strong> — bu, onların gücü və
    təhlükəsidir. <code>afterAll</code> olmasa hər işə salmada bir sətir əlavə
    olunur; 10 dəfə işlədəndən sonra <code>cemi</code> rəqəmi səhv çıxır və
    testlər özü-özünə sınmağa başlayır. Ona görə təmizləmə testin
    <strong>ayrılmaz hissəsidir</strong>, "sonra edərəm" işi deyil.""",
    d="""$ npx vitest run --config vitest.config.e2e.ts test/struktur.e2e-spec.ts

 RUN  v4.1.11 /Users/royatalibova/Deepseek_ARTI/DS_Backend

 ✓ test/struktur.e2e-spec.ts (13 tests) 185ms

 Test Files  1 passed (1)
      Tests  13 passed (13)

$ psql -U arti_user -w -d arti_baza -tAc \\
    "SELECT count(*)::int FROM struktur.merkezler WHERE ad LIKE 'E2E %'"
0        ← təmizdir""",
    d_izah="""Sistemin vəziyyəti: struktur modulu <strong>13 e2e yoxlamadan</strong>
    keçir və baza təmiz qalır. Testlər həm uğurlu yolu (səhifələmə, filtr,
    axtarış, yaratma, yeniləmə, silmə), həm də xəta yollarını (400, 404, 409)
    yoxlayır. <code>afterAll</code> bloku yaradılan sətri hər halda silir —
    hətta test uğursuz olsa belə, çünki <code>afterAll</code> həmişə işləyir.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=12,
    ad="e2e testlər — kadrlar",
    a="""Kadrlar testi JOIN sorğusunun nəticəsini yoxlayır: <code>id</code> həqiqətən
    rəqəmdirmi, <code>maas</code> sətir deyil rəqəmdirmi, əlaqəli adlar gəlirmi.
    Bu yoxlamalar <strong>xüsusilə vacibdir</strong>, çünki <code>bigint</code> və
    <code>numeric</code> sütunlarının JSON-a çevrilməsi sükutla səhv ola bilər —
    TypeScript bunu tutmur, yalnız canlı sorğu göstərir.""",
    b=[("test/kadrlar.e2e-spec.ts", fayl("test/kadrlar.e2e-spec.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayl yerindədirmi?
ls -l test/kadrlar.e2e-spec.ts

# 2) ⚠️ Tip yoxlamaları varmı?
grep -n "typeof s.id\\|typeof s.maas" test/kadrlar.e2e-spec.ts

# 3) Bütün e2e testlər
npx vitest run --config vitest.config.e2e.ts""",
    c_olmaz="""$ npx vitest run --config vitest.config.e2e.ts test/kadrlar.e2e-spec.ts
   # ::int çevirməsi olmasa:

 FAIL  test/kadrlar.e2e-spec.ts > tam profillə səhifələnmiş siyahı
 AssertionError: expected 'string' to be 'number'
   expected 'string' to be 'number'

   # Çünki id BigInt kimi gəlir və JSON-da sətirə çevrilir""",
    c_izah="""Bu test <strong>sükutla sınıq</strong> olan bir şeyi tutur.
    <code>e.id::int</code> olmasa sorğu işləyər, cavab gələr, heç bir xəta
    çıxmaz — sadəcə <code>id</code> sətir olar və frontend
    <code>row.id + 1</code> kimi hesablamalarda səhv nəticə verər.
    <code>typeof s.id === 'number'</code> yoxlaması məhz bunun üçündür.""",
    d="""$ npx vitest run --config vitest.config.e2e.ts

 RUN  v4.1.11 /Users/royatalibova/Deepseek_ARTI/DS_Backend

 ✓ test/struktur.e2e-spec.ts (13 tests) 185ms
 ✓ test/kadrlar.e2e-spec.ts (7 tests) 149ms
 ✓ test/saglamliq.e2e-spec.ts (4 tests) 112ms

 Test Files  3 passed (3)
      Tests  24 passed (24)
   Start at  07:43:48
   Duration  1.28s

──────────────────────────────────────────
YEKUN: 21 unit + 24 e2e = 45 test""",
    d_izah="""<strong>Backend-2 tamamlandı.</strong> Ümumi vəziyyət:
    <ul>
      <li><strong>21 unit + 24 e2e = 45 test</strong>, hamısı keçir
          (Dərs 1-də 7 test idi).</li>
      <li><strong>11 marshrut</strong> — 6 struktur (tam CRUD + statistika),
          3 kadrlar (siyahı + icmal + bir), 2 sağlamlıq.</li>
      <li><strong>Vahid cavab forma</strong>: hər siyahı
          <code>{ setirler, cemi, sehife, limit, sehife_sayi }</code> qaytarır.</li>
      <li><strong>Vahid xəta forma</strong>: 400 / 404 / 409 hamısı
          <code>{ ugur, xeta: { kod, mesaj, detallar }, yol, vaxt }</code>.</li>
      <li><strong>Baza təmizdir</strong>: testlərdən sonra qalıq sətir yoxdur.</li>
    </ul>
    <p><strong>Növbəti dərs (Backend-3):</strong> autentifikasiya və rollar —
    JWT token, <code>@Public()</code>/<code>@Roles()</code> dekoratorları və
    hər dəyişikliyin audit jurnalına yazılması. Bu dərsdə API hələ
    <strong>açıqdır</strong>.</p>""",
)



# ─────────────────────────────────────────────────────────────────
#  ADDIM 13 — ENDPOINT ARAYIŞI (serverin tam qaldırılması + 11 endpoint)
# ─────────────────────────────────────────────────────────────────
ENDPOINTLER = [
    dict(
        n=1, metod="GET", yol="/api/v1", ad="Kök endpoint",
        qatlar=("Express → qlobal prefiks → <code>SaglamliqController.kok()</code> "
                "→ <em>servis yoxdur</em> → JSON"),
        ne=("API-nin ünvanını, versiyasını, prefiksini və sənədləşdirmə yolunu "
            "qaytarır. Frontend işə düşəndə ilk bunu çağırıb API-nin yerində "
            "olduğunu yoxlayır."),
        gozle="<code>200</code> · <code>{ ad, versiya, prefiks, senedlesdirme }</code>",
        curl="curl -s http://localhost:4000/api/v1/ | python3 -m json.tool",
    ),
    dict(
        n=2, metod="GET", yol="/api/v1/saglamliq", ad="Sağlamlıq yoxlaması",
        qatlar=("Express → prefiks → <code>SaglamliqController.yoxla()</code> → "
                "<code>SaglamliqService.yoxla()</code> → "
                "<code>PrismaService.yoxla()</code> → <code>$queryRaw</code> "
                "(information_schema) → JSON"),
        ne=("Bazaya <strong>real sorğu</strong> göndərib cədvəl sayını sayır. "
            "Sadəcə «işləyirəm» demir — baza qopsa <code>500</code> verir. "
            "Monitorinq sistemləri bu endpoint-i mütəmadi çağırır."),
        gozle=("<code>200</code> · <code>{ status: \"saglam\", baza: { qosulub: true, "
               "cedvel_sayi: 48, gecikme_ms }, versiya, vaxt }</code>"),
        curl="curl -s http://localhost:4000/api/v1/saglamliq | python3 -m json.tool",
    ),
    dict(
        n=3, metod="GET", yol="/api/v1/struktur/merkezler",
        ad="Mərkəzlərin siyahısı",
        qatlar=("Express → prefiks → <strong>ValidationPipe</strong> "
                "(<code>MerkezFiltrDto</code>) → "
                "<code>StrukturController.siyahi()</code> → "
                "<code>StrukturService.merkezler()</code> → Prisma "
                "<code>findMany</code> + <code>count</code> (paralel) → "
                "<code>sehifelenmis()</code> → JSON"),
        ne=("Səhifələnmiş siyahı qaytarır. Altı sorğu parametri dəstəklənir: "
            "<code>sehife</code>, <code>limit</code>, <code>axtar</code> (ad üzrə), "
            "<code>tip</code>, <code>aktiv</code>, <code>sirala</code> + "
            "<code>siralama</code>."),
        gozle=("<code>200</code> · <code>{ setirler: [...], cemi: 10, sehife: 1, "
               "limit: 2, sehife_sayi: 5 }</code>"),
        curl=("curl -s \"http://localhost:4000/api/v1/struktur/merkezler?limit=2\" | python3 -m json.tool"),
    ),
    dict(
        n=4, metod="GET", yol="/api/v1/struktur/merkezler/statistika",
        ad="Mərkəz statistikası",
        qatlar=("Express → prefiks → <em>ValidationPipe yoxdur — parametr yoxdur</em> "
                "→ <code>StrukturController.statistika()</code> → "
                "<code>StrukturService.merkezStatistikasi()</code> → "
                "<code>$queryRaw</code>: <code>GROUP BY</code> + 2 × "
                "<code>LEFT JOIN</code> → JSON"),
        ne=("Hər mərkəz üzrə şöbə və əməkdaş sayını hesablayır. "
            "<code>count(DISTINCT ...)</code> işlədilir, çünki iki "
            "<code>LEFT JOIN</code> bir-birini çoxaldır."),
        gozle=("<code>200</code> · massiv <code>[{ merkez_id, ad, shobe_sayi, "
               "emekdas_sayi }]</code> · <strong>10 sətir</strong>"),
        curl=("curl -s http://localhost:4000/api/v1/struktur/merkezler/statistika | python3 -m json.tool"),
    ),
    dict(
        n=5, metod="GET", yol="/api/v1/struktur/merkezler/:id", ad="Bir mərkəz",
        qatlar=("Express → prefiks → <strong>ParseIntPipe</strong> "
                "(<code>:id</code> → ədəd) → <code>StrukturController.bir()</code> → "
                "<code>StrukturService.merkez()</code> → Prisma "
                "<code>findUnique</code> → JSON"),
        ne=("Bir mərkəzin bütün sahələrini qaytarır. Tapılmasa "
            "<code>NotFoundException</code> atılır və filtr onu <code>404</code>-ə "
            "çevirir. <code>:id</code> rəqəm deyilsə <code>ParseIntPipe</code> "
            "<code>400</code> verir."),
        gozle="<code>200</code> · tək obyekt · tapılmasa <code>404</code> · rəqəm deyilsə <code>400</code>",
        curl="curl -s http://localhost:4000/api/v1/struktur/merkezler/2 | python3 -m json.tool",
    ),
    dict(
        n=6, metod="POST", yol="/api/v1/struktur/merkezler", ad="Yeni mərkəz",
        qatlar=("Express → prefiks → <strong>ValidationPipe</strong> "
                "(<code>CreateMerkezDto</code>, 9 qayda) → "
                "<code>StrukturController.yarat()</code> → "
                "<code>StrukturService.yarat()</code> → Prisma <code>create</code> → "
                "JSON"),
        ne=("Yeni mərkəz yaradır. <code>ad</code> sütunu unikaldır — eyni adla "
            "ikinci cəhd <code>P2002</code> xətası verir və servis onu aydın "
            "<code>409</code> cavabına çevirir."),
        gozle=("<code>201</code> · yaradılmış obyekt (<code>id</code> ilə) · "
               "ad təkrarı <code>409</code> · validasiya <code>400</code>"),
        curl=("ID=$(curl -s -X POST http://localhost:4000/api/v1/struktur/merkezler \\\n"
              "  -H 'Content-Type: application/json' \\\n"
              "  -d '{\"ad\":\"Nümunə Test Mərkəzi\",\"tip\":\"sektor\",\"email\":\"numune@arti.edu.az\",\"telefon\":\"+994 12 555 44 33\"}' \\\n"
              "  | python3 -c \"import json,sys;print(json.load(sys.stdin)['id'])\")\n"
              "echo \"yaradıldı: id=$ID\"\n"
              "echo $ID > /tmp/test_merkez_id.txt      # sonrakı addımlar üçün"),
    ),
    dict(
        n=7, metod="PATCH", yol="/api/v1/struktur/merkezler/:id", ad="Mərkəzi yenilə",
        qatlar=("Express → prefiks → ParseIntPipe → <strong>ValidationPipe</strong> "
                "(<code>UpdateMerkezDto</code> = <code>PartialType</code>) → "
                "<code>StrukturController.yenile()</code> → "
                "<code>StrukturService.yenile()</code> → Prisma <code>update</code> → JSON"),
        ne=("Yalnız göndərilən sahələri dəyişir. <code>PartialType</code> sayəsində "
            "bütün sahələr istəyə bağlıdır — yalnız <code>telefon</code> göndərsəniz "
            "qalan 8 sahə <strong>toxunulmur</strong>."),
        gozle=("<code>200</code> · yenilənmiş obyekt · yoxdursa <code>404</code> · "
               "ad təkrarı <code>409</code>"),
        curl=("ID=$(cat /tmp/test_merkez_id.txt)\n"
              "curl -s -X PATCH http://localhost:4000/api/v1/struktur/merkezler/$ID \\\n"
              "  -H 'Content-Type: application/json' \\\n"
              "  -d '{\"telefon\":\"+994 12 999 88 77\",\"tesvir\":\"Yenilənmiş təsvir\"}' \\\n"
              "  | python3 -m json.tool"),
    ),
    dict(
        n=8, metod="DELETE", yol="/api/v1/struktur/merkezler/:id", ad="Mərkəzi sil",
        qatlar=("Express → prefiks → ParseIntPipe → "
                "<code>StrukturController.sil()</code> → "
                "<code>StrukturService.sil()</code> → <strong>3 × count</strong> "
                "(əvvəlcədən FK yoxlaması) → Prisma <code>delete</code> → JSON"),
        ne=("Mərkəzi silir. Əvvəlcə <code>shobeler</code>, <code>emekdaslar</code> və "
            "<code>rehberlik</code> cədvəlləri sayılır — bağlı sətir varsa silmə "
            "<strong>dayandırılır</strong> və nəyin mane olduğu mesajda göstərilir."),
        gozle=("<code>200</code> · <code>{ silindi, ad }</code> · bağlı sətir varsa "
               "<code>409</code> · yoxdursa <code>404</code>"),
        curl=("ID=$(cat /tmp/test_merkez_id.txt)\n"
              "curl -s -X DELETE http://localhost:4000/api/v1/struktur/merkezler/$ID \\\n"
              "  | python3 -m json.tool"),
    ),
    dict(
        n=9, metod="GET", yol="/api/v1/kadrlar/emekdaslar", ad="Əməkdaşların siyahısı",
        qatlar=("Express → prefiks → <strong>ValidationPipe</strong> "
                "(<code>EmekdasFiltrDto</code>, mirasla) → "
                "<code>KadrlarController.siyahi()</code> → "
                "<code>KadrlarService.emekdaslar()</code> → "
                "<code>serh()</code> + <code>$queryRaw</code> — <strong>6 LEFT JOIN</strong> "
                "+ <code>count</code> → JSON"),
        ne=("Səhifələnmiş siyahı qaytarır, amma hər sətir <strong>tam profildir</strong>: "
            "mərkəzin, şöbənin, vəzifənin, elmi dərəcənin və statusun <em>adı</em> "
            "gəlir. Filtr: <code>merkez_id</code>, <code>shobe_id</code>, "
            "<code>aktiv</code>, <code>axtar</code>."),
        gozle=("<code>200</code> · <code>{ setirler, cemi: 14, sehife_sayi: 14 }</code> · "
               "<code>id</code> və <code>maas</code> <strong>rəqəm</strong> olmalıdır"),
        curl=("curl -s \"http://localhost:4000/api/v1/kadrlar/emekdaslar?limit=1\" | python3 -m json.tool"),
    ),
    dict(
        n=10, metod="GET", yol="/api/v1/kadrlar/emekdaslar/icmal", ad="Kadr icmalı",
        qatlar=("Express → prefiks → <em>ValidationPipe yoxdur</em> → "
                "<code>KadrlarController.icmal()</code> → "
                "<code>KadrlarService.icmal()</code> → <strong>3 × "
                "<code>$queryRaw</code> paralel</strong> "
                "(<code>count</code>, <code>GROUP BY</code> ×2, "
                "<code>FILTER</code>) → JSON"),
        ne=("Ümumi mənzərə: cəmi və aktiv əməkdaş sayı, mərkəzlər üzrə bölgü və "
            "vəzifələr üzrə ilk 10. Üç sorğu <code>Promise.all</code> ilə "
            "<strong>eyni anda</strong> göndərilir."),
        gozle=("<code>200</code> · <code>{ cemi: 14, aktiv: 14, merkez_uzre: [...], "
               "vezife_uzre: [...] }</code>"),
        curl="curl -s http://localhost:4000/api/v1/kadrlar/emekdaslar/icmal | python3 -m json.tool",
    ),
    dict(
        n=11, metod="GET", yol="/api/v1/kadrlar/emekdaslar/:id", ad="Bir əməkdaş",
        qatlar=("Express → prefiks → ParseIntPipe → "
                "<code>KadrlarController.bir()</code> → "
                "<code>KadrlarService.emekdas()</code> → "
                "<code>$queryRaw</code> — <code>WHERE e.id = $1</code>, "
                "6 <code>LEFT JOIN</code> → JSON"),
        ne=("Bir əməkdaşın tam profili. Siyahı sorğusu ilə <strong>eyni</strong> "
            "JOIN-ları işlədir, sadəcə <code>LIMIT 1</code> və <code>WHERE</code> "
            "əlavə olunur."),
        gozle="<code>200</code> · tək obyekt · tapılmasa <code>404</code>",
        curl="curl -s http://localhost:4000/api/v1/kadrlar/emekdaslar/4 | python3 -m json.tool",
    ),
]

# ── B hissəsi: server qaldırma + hər endpoint ──
B13 = (
    '  <p class="fayl-ad">Terminal 1 — serveri əvvəldən sona qaldır</p>\n'
    '<pre><code>' + e("""cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST

# 1) Əvvəlcə portu təmizlə (köhnə server varsa)
lsof -ti:4000 && kill $(lsof -ti:4000) && sleep 2

# 2) Yığ
npm run build

# 3) Serveri qaldır — bu terminal AÇIQ QALIR
node dist/main.js

# İnkişaf üçün (hər dəyişiklikdə özü yenilənir):
#   npm run start:dev
# Dayandırmaq: Ctrl + C""") + '</code></pre>\n'
    '  <p>Server qalxanda <strong>aşağıdaki logu</strong> görməlisiniz. '
    'Sətirləri sıra ilə oxuyun — bu, sistemin özünü necə qurduğunun xəritəsidir. '
    'Tam çıxış D hissəsindədir.</p>\n'
    '  <p class="fayl-ad">Terminal 2 — hər endpoint-i bir-bir yoxla</p>\n'
    '  <p>Aşağıda <strong>11 endpoint-in hamısı</strong> verilir. Hər biri üçün '
    'üç şey yazılıb: <strong>keçdiyi mərhələlər</strong>, <strong>nə etdiyi</strong> '
    'və <strong>gözlənilən nəticə</strong>. Əmrləri sıra ilə işlədin.</p>\n'
)

for _ep in ENDPOINTLER:
    B13 += (
        f'  <h4>{_ep["n"]} · <code>{_ep["metod"]} {e(_ep["yol"])}</code> — {e(_ep["ad"])}</h4>\n'
        f'  <p><strong>Keçdiyi mərhələlər:</strong> {_ep["qatlar"]}</p>\n'
        f'  <p><strong>Nə edir:</strong> {_ep["ne"]}</p>\n'
        f'  <p><strong>Gözlənilən:</strong> {_ep["gozle"]}</p>\n'
        f'<pre><code>{e(_ep["curl"])}</code></pre>\n'
    )

# ── D hissəsi: real çıxışlar ──
D13 = """════════════ TERMINAL 1 — SERVERİN TAM LOGU ════════════

$ npm run build
> ds-backend@0.1.0 build
> nest build

$ node dist/main.js

[Nest] LOG [NestFactory] Starting Nest application...
[Nest] LOG [InstanceLoader] AppModule dependencies initialized +8ms
[Nest] LOG [InstanceLoader] PrismaModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] ConfigHostModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] ConfigModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] SaglamliqModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] StrukturModule dependencies initialized +0ms
[Nest] LOG [InstanceLoader] KadrlarModule dependencies initialized +0ms
[Nest] LOG [RoutesResolver] SaglamliqController {/api/v1}: +7ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1, GET} route +1ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/saglamliq, GET} route +0ms
[Nest] LOG [RoutesResolver] StrukturController {/api/v1/struktur/merkezler}: +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler/statistika, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler/:id, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler, POST} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler/:id, PATCH} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/struktur/merkezler/:id, DELETE} route +0ms
[Nest] LOG [RoutesResolver] KadrlarController {/api/v1/kadrlar/emekdaslar}: +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/kadrlar/emekdaslar, GET} route +1ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/kadrlar/emekdaslar/icmal, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/kadrlar/emekdaslar/:id, GET} route +0ms
[Nest] LOG [BAZA] Baza bağlantısı açıldı
[Nest] LOG [NestApplication] Nest application successfully started +0ms
[Nest] LOG [BAŞLANGIC] API hazırdır → http://localhost:4000/api/v1
[Nest] LOG [BAŞLANGIC] Sənədləşdirmə → http://localhost:4000/docs


════════════ TERMINAL 2 — 11 ENDPOINT ════════════

── 1 · GET /api/v1 ──────────────────────────────
$ curl -s http://localhost:4000/api/v1/ | python3 -m json.tool
{
    "ad": "ARTİ ERP API",
    "versiya": "0.1.0",
    "prefiks": "/api/v1",
    "senedlesdirme": "/docs"
}

── 2 · GET /api/v1/saglamliq ────────────────────
$ curl -s http://localhost:4000/api/v1/saglamliq | python3 -m json.tool
{
    "status": "saglam",
    "baza": {
        "qosulub": true,
        "cedvel_sayi": 48,
        "gecikme_ms": 19
    },
    "versiya": "0.1.0",
    "vaxt": "2026-09-21T05:03:01.172Z"
}

── 3 · GET /api/v1/struktur/merkezler?limit=2 ───
$ curl -s "http://localhost:4000/api/v1/struktur/merkezler?limit=2" | python3 -m json.tool
{
    "setirler": [
        {
            "id": 1,
            "ad": "Elmi katiblik",
            "tip": "katiblik",
            "tesvir": "Elmi Şuranın işinin təşkili və sənədləşdirilməsi",
            "unvan": "Zərifə Əliyeva 96, Bakı",
            "telefon": "+994 12 599 08 08",
            "email": "elmi.katib@arti.edu.az",
            "yaradilma_tarixi": "2016-11-14T00:00:00.000Z",
            "aktiv": true
        },
        {
            "id": 2,
            "ad": "Elmi-pedaqoji tədqiqatlar mərkəzi",
            "tip": "merkez",
            "tesvir": "Təhsilin nəzəriyyəsi, tarixi, iqtisadiyyatı üzrə tədqiqatlar",
            "unvan": "Zərifə Əliyeva 96, Bakı",
            "telefon": "+994 12 599 08 08",
            "email": "tedqiqat@arti.edu.az",
            "yaradilma_tarixi": "2016-11-14T00:00:00.000Z",
            "aktiv": true
        }
    ],
    "cemi": 10,
    "sehife": 1,
    "limit": 2,
    "sehife_sayi": 5
}

── 4 · GET /api/v1/struktur/merkezler/statistika ─
$ curl -s http://localhost:4000/api/v1/struktur/merkezler/statistika | python3 -m json.tool
[
    { "merkez_id": 1,  "ad": "Elmi katiblik",                        "shobe_sayi": 0, "emekdas_sayi": 2 },
    { "merkez_id": 2,  "ad": "Elmi-pedaqoji tədqiqatlar mərkəzi",    "shobe_sayi": 7, "emekdas_sayi": 2 },
    { "merkez_id": 10, "ad": "Funksional şöbələr",                   "shobe_sayi": 8, "emekdas_sayi": 3 }
    ...
]
   → cəmi 10 sətir

── 5 · GET /api/v1/struktur/merkezler/2 ─────────
$ curl -s http://localhost:4000/api/v1/struktur/merkezler/2 | python3 -m json.tool
{
    "id": 2,
    "ad": "Elmi-pedaqoji tədqiqatlar mərkəzi",
    "tip": "merkez",
    "tesvir": "Təhsilin nəzəriyyəsi, tarixi, iqtisadiyyatı üzrə tədqiqatlar",
    "unvan": "Zərifə Əliyeva 96, Bakı",
    "telefon": "+994 12 599 08 08",
    "email": "tedqiqat@arti.edu.az",
    "yaradilma_tarixi": "2016-11-14T00:00:00.000Z",
    "aktiv": true
}

── 6 · POST /api/v1/struktur/merkezler ──────────
$ curl -s -X POST http://localhost:4000/api/v1/struktur/merkezler \\
    -H 'Content-Type: application/json' \\
    -d '{"ad":"Nümunə Test Mərkəzi","tip":"sektor",
         "email":"numune@arti.edu.az","telefon":"+994 12 555 44 33"}'
{
    "id": 280,
    "ad": "Nümunə Test Mərkəzi",
    "tip": "sektor",
    "tesvir": null,
    "unvan": null,
    "telefon": "+994 12 555 44 33",
    "email": "numune@arti.edu.az",
    "yaradilma_tarixi": null,
    "aktiv": true
}

── 7 · PATCH /api/v1/struktur/merkezler/280 ─────
$ curl -s -X PATCH http://localhost:4000/api/v1/struktur/merkezler/280 \\
    -H 'Content-Type: application/json' \\
    -d '{"telefon":"+994 12 999 88 77","tesvir":"Yenilənmiş təsvir"}'
{
    "id": 280,
    "ad": "Nümunə Test Mərkəzi",      ← DƏYİŞMƏDİ (göndərilmədi)
    "tip": "sektor",
    "tesvir": "Yenilənmiş təsvir",    ← dəyişdi
    "unvan": null,
    "telefon": "+994 12 999 88 77",   ← dəyişdi
    "email": "numune@arti.edu.az",
    "yaradilma_tarixi": null,
    "aktiv": true
}

── 8 · DELETE /api/v1/struktur/merkezler/280 ────
$ curl -s -X DELETE http://localhost:4000/api/v1/struktur/merkezler/280
{
    "silindi": 280,
    "ad": "Nümunə Test Mərkəzi"
}

── 9 · GET /api/v1/kadrlar/emekdaslar?limit=1 ───
$ curl -s "http://localhost:4000/api/v1/kadrlar/emekdaslar?limit=1" | python3 -m json.tool
{
    "setirler": [
        {
            "id": 13,
            "ad": "Elçin",
            "soyad": "Babayev",
            "ata_adi": "Sərvər",
            "email": "elcin.babayev@arti.edu.az",
            "telefon": "+994 50 211 01 13",
            "maas": 1300,
            "ise_baslama": "2023-03-08",
            "aktiv": true,
            "merkez": "Təhsil texnologiyaları mərkəzi",
            "shobe": null,
            "vezife": "Aparıcı mütəxəssis",
            "elmi_derece": "Magistr",
            "elmi_ad": null,
            "is_statusu": "Aktiv"
        }
    ],
    "cemi": 14,
    "sehife": 1,
    "limit": 1,
    "sehife_sayi": 14
}

── 10 · GET /api/v1/kadrlar/emekdaslar/icmal ────
$ curl -s http://localhost:4000/api/v1/kadrlar/emekdaslar/icmal | python3 -m json.tool
{
    "cemi": 14,
    "aktiv": 14,
    "merkez_uzre": [
        { "ad": "Funksional şöbələr",                        "say": 3 },
        { "ad": "Elmi katiblik",                             "say": 2 },
        { "ad": "Elmi-pedaqoji tədqiqatlar mərkəzi",         "say": 2 },
        { "ad": "Qiymətləndirmə, təhlil və monitorinq mərkəzi", "say": 2 },
        { "ad": "Metodik dəstək mərkəzi",                    "say": 1 }
    ],
    "vezife_uzre": [
        { "ad": "Direktor müavini",       "say": 6 },
        { "ad": "Mərkəz rəhbəri",         "say": 2 },
        { "ad": "Aparıcı mütəxəssis",     "say": 1 },
        { "ad": "Baş mütəxəssis",         "say": 1 }
    ]
}

── 11 · GET /api/v1/kadrlar/emekdaslar/4 ────────
$ curl -s http://localhost:4000/api/v1/kadrlar/emekdaslar/4 | python3 -m json.tool
{
    "id": 4,
    "ad": "İlham",
    "soyad": "Cavadov",
    "ata_adi": "Ağaqardaş",
    "email": "ilham.cavadov@arti.edu.az",
    "telefon": "+994 50 211 01 04",
    "maas": 2800,
    "ise_baslama": "2020-05-10",
    "aktiv": true,
    "merkez": "Metodik dəstək mərkəzi",
    "shobe": "Metodik xidmətin təşkili və monitorinqi şöbəsi",
    "vezife": "Direktor müavini",
    "elmi_derece": "Fəlsəfə doktoru",
    "elmi_ad": null,
    "is_statusu": "Aktiv"
}

════════════ XƏTA CAVABLARI ════════════

── 400 · Validasiya (limit=500) ──
{
    "ugur": false,
    "xeta": {
        "kod": "YANLIS_SORGU",
        "mesaj": "Validasiya xətası",
        "detallar": ["limit 100-dən çox ola bilməz"]
    },
    "yol": "/api/v1/struktur/merkezler?limit=500",
    "vaxt": "2026-09-21T05:04:33.353Z"
}

── 404 · Tapılmadı (id=999999) ──
{
    "ugur": false,
    "xeta": { "kod": "TAPILMADI", "mesaj": "999999 nömrəli mərkəz tapılmadı" },
    "yol": "/api/v1/struktur/merkezler/999999",
    "vaxt": "2026-09-21T05:04:33.396Z"
}

── 409 · Konflikt (bağlı mərkəzi silmək) ──
{
    "ugur": false,
    "xeta": {
        "kod": "TOQQUSMA",
        "mesaj": "«Elmi-pedaqoji tədqiqatlar mərkəzi» silinmir — ona bağlı 7 şöbə, 2 əməkdaş var"
    },
    "yol": "/api/v1/struktur/merkezler/2",
    "vaxt": "2026-09-21T05:04:33.426Z"
}

════════════ ƏLAVƏ ÜNVANLAR ════════════

  GET /docs              → 200   (Swagger interfeysi — brauzerdə açın)
  GET /docs-json         → 200   (OpenAPI spesifikasiyası, JSON)
  GET /saglamliq         → 404   (prefiks olmadan — düzgün davranış)"""


addim(
    n=13,
    ad="Serveri tam qaldır və bütün endpoint-ləri yoxla (arayış)",
    a="""Bu addım bir <strong>arayış səhifəsidir</strong> — gündəlik işdə ən çox
    açacağınız yer. Serveri əvvəldən sona qədər qaldırırıq və bu vaxta qədər
    yazdığımız <strong>11 endpoint-in hamısını</strong> bir-bir yoxlayırıq. Hər
    endpoint üçün üç şey verilir: hansı qatlardan keçdiyi, nə etdiyi və nəticənin
    necə olması. Sonda üç xəta kodu (<code>400</code>, <code>404</code>,
    <code>409</code>) və onların real cavabları göstərilir.""",
    b=[],
    b_html=B13,
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Server işləyirmi?
curl -s -o /dev/null -w 'sağlamlıq → %{http_code}\\n' \\
  http://localhost:4000/api/v1/saglamliq

# 2) Neçə marshrut qeydiyyatdadır? (11 olmalıdır)
curl -s http://localhost:4000/docs-json | python3 -c "
import json, sys
d = json.load(sys.stdin)
say = 0
for yol in sorted(d['paths']):
    for m in d['paths'][yol]:
        say += 1
        print(f'  {m.upper():6s} {yol}')
print('  CƏMİ:', say, 'marshrut')
"

# 3) Hər endpoint bir dəfə cavab verirmi? (kodları topla)
A=http://localhost:4000/api/v1
for yol in "" "saglamliq" "struktur/merkezler?limit=1" \\
           "struktur/merkezler/statistika" "struktur/merkezler/2" \\
           "kadrlar/emekdaslar?limit=1" "kadrlar/emekdaslar/icmal" \\
           "kadrlar/emekdaslar/4"; do
  printf '  GET /%-34s → %s\\n' "$yol" \\
    "$(curl -s -o /dev/null -w '%{http_code}' "$A/$yol")"
done

# 4) Portu kim tutur?
lsof -nP -iTCP:4000 | tail -1

# 5) Baza təmiz qaldı?
export PGPASSWORD=arti_secret_2025
psql -U arti_user -w -d arti_baza -tAc \\
  "SELECT '  mərkəz sayı: ' || count(*)::int FROM struktur.merkezler\"""",
    c_olmaz="""$ curl -s -o /dev/null -w '%{http_code}\\n' http://localhost:4000/api/v1/struktur/merkezler
000

$ curl -s http://localhost:4000/api/v1/struktur/merkezler
curl: (7) Failed to connect to localhost port 4000: Connection refused

   # Yaxud server qalxmayıbsa:
[Nest] ERROR [ExceptionHandler] Error: listen EADDRINUSE:
  address already in use :::4000""",
    c_izah="""<code>000</code> kodu <code>curl</code>-un öz kodudur — <strong>server
    ümumiyyətlə cavab vermir</strong>. Səbəb ikidir: ya server qalxmamışdır
    (<code>node dist/main.js</code> işlədilməyib), ya da port məşğuldur
    (<code>EADDRINUSE</code>). Hər iki halda kömək edən əmrlər:
    <code>lsof -ti:4000</code> (portu kim tutur) və
    <code>npm run build</code> (yığım varmı).""",
    d=D13,
    d_izah="""<strong>Backend-2 tam işlək vəziyyətdədir.</strong> Serverin logunu
    yuxarıdan aşağı oxusanız, sistemin necə qurulduğunu görürsünüz:
    <ol>
      <li><strong>7 modul</strong> sıra ilə yükləndi —
          <code>AppModule</code>, <code>PrismaModule</code>,
          <code>ConfigHostModule</code>, <code>ConfigModule</code>,
          <code>SaglamliqModule</code>, <code>StrukturModule</code>,
          <code>KadrlarModule</code>.</li>
      <li><strong>11 marshrut</strong> üç controller altında qeydiyyatdan keçdi.</li>
      <li><code>[BAZA] Baza bağlantısı açıldı</code> — Prisma
          <code>onModuleInit</code> işlədi.</li>
      <li>Yalnız bundan <em>sonra</em> server "hazırdır" dedi.</li>
    </ol>
    <p><strong>Müşahidə etməyə dəyər iki şey:</strong></p>
    <ul>
      <li>Birinci sorğu <code>1.2 ms</code>, sonrakılar <code>0.6 ms</code> çəkir
          (3-cü endpoint) — bu, sorğunun yerli şəbəkədə getdiyini göstərir.</li>
      <li><code>PATCH</code> cavabında <code>ad</code> sahəsi
          <strong>dəyişməyib</strong> — çünki göndərilməmişdi.
          <code>PartialType</code> məhz bunun üçündür.</li>
    </ul>
    <p>Bu andan etibarən backend <strong>11 endpoint</strong> ilə işləyir, amma
    hələ də <strong>açıqdır</strong> — istənilən şəxs <code>DELETE</code> edə bilər.
    Növbəti dərs məhz bunu bağlayır: JWT token, <code>@Public()</code> və
    <code>@Roles()</code> dekoratorları, audit jurnalı.</p>""",
)

# ══════════════════════════════════════════════════════════════════
#  HTML QURULMASI
# ══════════════════════════════════════════════════════════════════
def addim_html(x: dict) -> str:
    b_hisse = x.get("b_html") or ""
    if x.get("b_html"):
        pass
    else:
      for fayl_ad, kod in x["b"]:
        b_hisse += (
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
{b_hisse}    </div>

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
      <span class="hisse-basliq">D · Bu koddan sonra sistemin durumu — ÇIXIŞ</span>
      <p class="cixis-xeber">⚠️ Bu blok <strong>çıxışdır</strong> — kopyalayıb terminala yapıştırmayın. Sadəcə oxuyun. Əmrlər B hissəsindədir.</p>
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
    return "".join(
        f'    <li><a href="#a{x["n"]}">{x["n"]}. {e(x["ad"])}</a></li>\n'
        for x in ADDIMLAR
    )


def icmal_html() -> str:
    return "".join(
        f'  <a href="#a{x["n"]}"><b>ADDIM {x["n"]}</b>{e(x["ad"])}</a>\n'
        for x in ADDIMLAR
    )


def main() -> None:
    css = CSS_FAYLI.read_text(encoding="utf-8").rstrip("\n") + "\n" + ELAVE_CSS
    addimlar = "\n".join(addim_html(x) for x in ADDIMLAR)
    n = len(ADDIMLAR)

    sened = f"""<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Backend 2 — Struktur və kadrlar: ilk real modullar (A/B/C/D)</title>
<style>
{css}
</style>
</head>
<body>
<div class="container">

<header>
  <div class="lesson-badge">DS_Backend · Hissə 2 / 4</div>
  <h1>Backend 2 — Struktur və kadrlar</h1>
  <p class="subtitle">İlk real modullar: səhifələmə, filtr, JOIN və tam CRUD —
    hər addım 4 hissə: <strong>A</strong> niyə · <strong>B</strong> kod ·
    <strong>C</strong> yoxlama · <strong>D</strong> durum</p>
  <p class="meta">
    <span>NestJS 12</span>
    <span>Prisma 7</span>
    <span>{n} addım</span>
    <span>11 marshrut</span>
    <span>45 test</span>
  </p>
</header>

<div class="block block-ne">
  <span class="block-title">NƏ EDƏCƏYİK</span>
  <p>Backend-1-də yalnız iki endpoint vardı: sağlamlıq və kök. İndi
  <strong>ilk real modulları</strong> yazacağıq — ARTİ-nin mərkəzləri və
  əməkdaşları üçün tam API. Sonda <strong>11 marshrut</strong> və
  <strong>45 test</strong> olacaq.</p>
  <p><strong>Ön şərt:</strong> Backend-1 tamamlanmalıdır —
  <code>DS_Backend</code> işləyən serverlə qalxmalı, <code>/api/v1/saglamliq</code>
  <code>200</code> verməlidir. Yoxlamaq üçün:</p>
  <pre><code>cd ~/Deepseek_ARTI/DS_Backend
npm run build &amp;&amp; node dist/main.js
# ayrı terminalda:
curl -s localhost:4000/api/v1/saglamliq</code></pre>
</div>

<div class="block block-nece">
  <span class="block-title">NECƏ OXUMALI — hər addımın 4 hissəsi</span>
  <table>
    <tr><th>Hissə</th><th>Nə var</th><th>Kopyalanır?</th></tr>
    <tr><td><strong>A</strong></td><td>Bu addım nəyə görədir — 3-4 cümlə</td>
        <td>—</td></tr>
    <tr><td><strong>B</strong></td><td>Kod — <code>cat &gt; fayl &lt;&lt;'EOF'</code>
        formasında, birbaşa yapışdırıla bilər</td>
        <td style="color:#15803d"><strong>✅ Bəli</strong></td></tr>
    <tr><td><strong>C</strong></td><td>Yoxlama əmrləri +
        <span style="color:#b91c1c">bu kod olmasa nə olardı</span></td>
        <td style="color:#15803d"><strong>✅ Bəli</strong></td></tr>
    <tr><td><strong>D</strong></td><td>Sistemin bu koddan sonraki
        <strong>real</strong> çıxışı</td>
        <td style="color:#b91c1c"><strong>❌ Xeyr — oxuyun</strong></td></tr>
  </table>
  <p>C və D hissələrindəki bütün çıxışlar <strong>realdır</strong> — kodu
  bilərəkdən söndürüb alınmış xətalar və canlı sistemdən götürülmüş nəticələr.</p>
</div>

<div class="block block-xeber">
  <span class="block-title">⚠️ BU DƏRSDƏ NƏ YOXDUR</span>
  <ul>
    <li><strong>Autentifikasiya yoxdur</strong> — bütün endpoint-lər açıqdır.
        İstənilən şəxs <code>POST</code>/<code>DELETE</code> edə bilər.</li>
    <li><strong>Audit jurnalı yoxdur</strong> — kimin nə dəyişdiyi yazılmır.</li>
    <li><strong>AI qatı yoxdur</strong> — RAG, embedding və təbii dil sorğuları sonra.</li>
  </ul>
  <p>Bunlar qəsdən kənarda saxlanılıb: hər biri öz addımlarını tələb edir.
  <strong>Backend-3</strong> məhz autentifikasiya, rollar və auditdən başlayır.</p>
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
  <strong>Backend-2 tamamlandı — {n} addım.</strong> 11 marshrut ·
  səhifələmə və filtr hər siyahıda · 6 cədvəlli JOIN ·
  tam CRUD + konflikt idarəsi · 21 unit + 24 e2e = <strong>45 test</strong>.
  <strong>Növbəti dərs:</strong> autentifikasiya və rollar (JWT),
  <code>@Public()</code>/<code>@Roles()</code> dekoratorları və audit jurnalı.
</div>

<div class="block block-ipucu">
  <span class="block-title">🔁 GÜNDƏLİK İŞ AXINI</span>
  <table>
    <tr><th>#</th><th>Nə</th><th>Əmr</th></tr>
    <tr><td>1</td><td>Portu təmizlə</td>
        <td><code>kill $(lsof -ti:4000)</code></td></tr>
    <tr><td>2</td><td>Serveri qaldır <em>(T1)</em></td>
        <td><code>npm run start:dev</code></td></tr>
    <tr><td>3</td><td>Yoxla <em>(T2)</em></td>
        <td><code>curl -s localhost:4000/api/v1/struktur/merkezler</code></td></tr>
    <tr><td>4</td><td>Testlər</td>
        <td><code>npm test &amp;&amp; npx vitest run --config vitest.config.e2e.ts</code></td></tr>
    <tr><td>5</td><td>Yaz</td>
        <td><code>git add -A &amp;&amp; git commit -m "..."</code></td></tr>
  </table>
  <p><strong>Serveri dayandırmaq:</strong> T1-də <code>Ctrl + C</code>.
  <code>start:dev</code> rejimində faylı saxladıqca server özü yenilənir.</p>
</div>

</div>
<script>
  document.addEventListener('DOMContentLoaded', function () {{
    document.querySelectorAll('pre').forEach(function (pre) {{
      // D hissəsi ÇIXIŞDIR — kopyala düyməsi qoyulmur
      if (pre.closest('.hisse-d')) return;
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
    print(f"✅ {CIXIS.relative_to(KOK)}")
    print(f"   {sened.count(chr(10)) + 1} sətir · {len(ADDIMLAR)} addım × 4 hissə "
          f"= {len(ADDIMLAR) * 4} bölmə")


if __name__ == "__main__":
    main()
