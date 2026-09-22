#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-4.html dərsini yaradır — A / B / C / D formatında.

Hər addım 4 hissədən ibarətdir:
  A — bu addım nəyə görədir (3-4 cümlə)
  B — addıma aid kodun özü (hər fayl bloku `mkdir -p` + `cat > ... <<'EOF'`)
  C — kodun yazıldığını yoxlayın + bu kod olmasa nə olardı (REAL xətalar)
  D — bu koddan sonra sistemin durumu (REAL çıxışlar) — ÇIXIŞ, kopyalanmır

İSTİFADƏ:
    python3 DƏRSLƏR/ds3_yarat.py                     # ~/Deepseek_ARTI/DS_Backend
    BACKEND=/tmp/b3 python3 DƏRSLƏR/ds3_yarat.py     # başqa qovluqdan
"""
from __future__ import annotations

import html
import os
import pathlib

KOK = pathlib.Path(__file__).resolve().parent.parent
BACKEND = pathlib.Path(os.environ.get("BACKEND", str(KOK / "DS_Backend")))
CIXIS = KOK / "DƏRSLƏR" / "DS_Backend-4.html"
CSS_FAYLI = KOK / "DS_Baza" / "ders.css"


def e(metn: str) -> str:
    return html.escape(str(metn), quote=False)


def fayl(yol: str) -> str:
    """BACKEND içindən real faylı oxuyur, `mkdir -p` + `cat >` formasına salır."""
    p = BACKEND / yol
    if not p.exists():
        raise SystemExit(f"XƏTA: fayl tapılmadı: {p}")
    govde = p.read_text(encoding="utf-8").rstrip("\n")
    qovluq = os.path.dirname(yol)
    basliq = f"mkdir -p {qovluq}\n" if qovluq else ""
    return f"{basliq}cat > {yol} <<'EOF'\n{govde}\nEOF"


def app_module_araliq() -> str:
    """ADDIM 6 üçün ARALIQ `app.module.ts` — `IxracModule` hələ YOXDUR.

    ⚠️ `src/ixrac/ixrac.module.ts` yalnız ADDIM 7-də yaradılır. Əgər bu addım
    onu import etsə, `nest build` belə sınır:
        error TS2307: Cannot find module './ixrac/ixrac.module.js'
    Ona görə modul qeydiyyatı bu addımda AI ilə bitir, ixrac isə növbəti
    addımda — fayl YARADILDIQDAN SONRA — əlavə olunur.
    """
    s = fayl("src/app.module.ts")
    s = s.replace("import { IxracModule } from './ixrac/ixrac.module.js';\n", "")
    s = s.replace("    IxracModule,\n", "")
    if "IxracModule" in s:
        raise SystemExit("XƏTA: app_module_araliq — IxracModule silinmədi")
    return s


def terminal(metn: str) -> str:
    return metn.strip()

ADDIMLAR: list = []


def addim(n, ad, a, b, c_yoxla, c_olmaz, c_izah, d, d_izah, b_html=None):
    ADDIMLAR.append(dict(
        n=n, ad=ad, a=a, b=b, b_html=b_html, c_yoxla=c_yoxla,
        c_olmaz=c_olmaz, c_izah=c_izah, d=d, d_izah=d_izah,
    ))


# ─────────────────────────────────────────────────────────────────
addim(
    n=1,
    ad="AI paketləri və açar",
    a="""Bu dərs institutun fəaliyyətini <strong>süni intellektlə</strong> idarə
    etməyə başlayır. İki yeni qat gəlir: <em>AI</em> (sənəd axtarışı, təbii dil
    sualı, cavab) və <em>ixrac</em> (Excel). AI üçün ayrıca paket lazım deyil —
    Node-un daxili <code>fetch</code>-i kifayətdir; Excel üçün isə
    <code>exceljs</code> quraşdırırıq. Ən vacibi: <code>DEEPSEEK_API_KEY</code>
    <strong>boş olsa da sistem işləyir</strong> — «demo rejim» cavab qaytarır.""",
    b=[
        ("Terminal — exceljs quraşdır", terminal("""cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST

npm install exceljs@^4.4.0

node -p "require('exceljs/package.json').version\"""")),
        (".env", fayl(".env")),
        (".env.example", fayl(".env.example")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Paket yerindədirmi?
node -p "require('exceljs/package.json').version"

# 2) .env-də AI açarları varmı?
grep -E 'DEEPSEEK_' .env

# 3) Açar BOŞ-dur (demo rejim) — bu normaldır
grep '^DEEPSEEK_API_KEY=""' .env && echo "→ demo rejim işləyəcək"

# 4) .env git-ə düşmür?
git check-ignore -v .env
""",
    c_olmaz="""$ curl -X POST localhost:4000/api/v1/ai/cavab \\
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \\
    -d '{"sual":"salam"}'

   # Açar təyin olunubsa, kod BİRBAŞA API-yə gedir və şəbəkə
   # olmayan mühitdə (CI, Docker) xəta verir:

Error: fetch failed
    at DeepseekService.soruş (dist/ai/deepseek.service.js:41:17)

   # Demo rejim isə həmişə cavab qaytarır — heç bir xarici asılılıq yoxdur.""",
    c_izah="""«Demo rejim» qəsdən belədir: açar olmayan mühitdə (yeni kompüter, CI,
    Docker) sistem <strong>sınmamalıdır</strong>. Cavabın
    <code>demo: true</code> sahəsi onun uydurma olduğunu bildirir — frontend
    bunu göstərib istifadəçini xəbərdar edə bilər. Əks halda hər yeni mühitdə
    "niyə AI işləmir?" sualı ilə başlamaq lazım gələrdi.""",
    d="""$ npm install exceljs@^4.4.0
added 12 packages in 3s

$ node -p "require('exceljs/package.json').version"
4.4.0

$ grep -E 'DEEPSEEK_' .env
DEEPSEEK_API_KEY=""
DEEPSEEK_MODEL="deepseek-chat"
DEEPSEEK_URL="https://api.deepseek.com"

$ git check-ignore -v .env
.gitignore:1:.env	.env""",
    d_izah="""Sistemin vəziyyəti: Excel üçün alət hazırdır və AI konfiqurasiyası
    <code>.env</code>-dədir. <code>DEEPSEEK_API_KEY</code> <strong>boşdur</strong> —
    bu, xəta deyil: növbəti addımlarda görəcəyik ki, bütün AI funksiyaları
    demo rejimdə də işləyir. Real açar əlavə etmək üçün sadəcə
    <code>.env</code>-də dırnaq içini doldurmaq kifayətdir —
    <strong>kod dəyişmir</strong>.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=2,
    ad="EmbeddingService — mətn → vektor",
    a="""AI-ın sənədləri «anlaması» üçün onları <strong>rəqəmlərə</strong> çevirmək
    lazımdır. <code>EmbeddingService</code> hər mətni 64 ölçülü vektora çevirir;
    oxşar mətnlərin vektorları bir-birinə yaxın olur. Real layihədə bu işi
    embedding API-si görür, biz isə <strong>FNV-1a hash</strong> ilə sadə
    deterministik versiya yazırıq — beləliklə açar olmadan da RAG-ın necə
    işlədiyini görürük. Vektor uzunluğu 1-ə normallaşdırılır ki, kosinus
    sadəcə skalyar hasili olsun.""",
    b=[("src/ai/embedding.service.ts", fayl("src/ai/embedding.service.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayl yerindədirmi?
ls -l src/ai/embedding.service.ts

# 2) Ölçü sabiti 64-dür?
grep -n 'OLCU' src/ai/embedding.service.ts | head -3

# 3) Vektor deterministikdir?
#    ⚠️ DİQQƏT: burada '.ts' yazılır — layihə fayllarında isə '.js' MƏCBURİDİR.
#    Səbəb: `tsx -e` əmri eval modulunda işləyir və onun öz qovluğu yoxdur;
#    tsx '.js' → '.ts' çevrilməsini edə bilmir və "Cannot find module" verir.
#    Layihə fayllarında isə NodeNext ESM '.js' tələb edir.
npx tsx -e "
import { EmbeddingService } from './src/ai/embedding.service.ts';
const s = new EmbeddingService({} as any);
const a = s.vektor('Elmi Şura protokolu');
const b = s.vektor('Elmi Şura protokolu');
const c = s.vektor('idman yarışı');
console.log('ölçü          :', a.length);
console.log('deterministik :', JSON.stringify(a) === JSON.stringify(b));
console.log('özü ilə oxşar :', s.kosinus(a, b));
console.log('başqası ilə   :', s.kosinus(a, c));
"

# 4) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi\"""",
    c_olmaz="""$ npx tsx -e "..."      # normallaşdırma olmasa:

ölçü          : 64
deterministik : true
özü ilə oxşar : 4.999999   ← 1 deyil! Çünki vektor uzunluğu 1 deyil.

   # Kosinus 1-dən böyük çıxır və müqayisə MƏNASIZ olur:
   # hər sənəd "çox oxşar" görünür, sıralama düzgün işləmir.""",
    c_izah="""Normallaşdırma (<code>x / uzunluq</code>) olmasa kosinus
    <strong>1-dən böyük</strong> çıxır və oxşarlıq müqayisəsi mənasını itirir.
    Hər vektorun uzunluğu 1 olsa, kosinus sadəcə <em>skalyar hasil</em> olur və
    nəticə həmişə −1…1 aralığında qalır. <code>|| 1</code> yazısı da vacibdir:
    boş mətn üçün uzunluq 0 olur və sıfıra bölmə <code>NaN</code> verərdi.""",
    d="""$ npx tsx -e "..."

ölçü          : 64
deterministik : true
özü ilə oxşar : 1
başqası ilə   : 0

$ npx tsc --noEmit -p tsconfig.build.json
   (çıxış yoxdur — KEÇDİ)""",
    d_izah="""Sistemin vəziyyəti: mətn → vektor çevirmə işləyir. Diqqət yetirin:
    <strong>eyni mətn həmişə eyni vektoru verir</strong> (deterministik) — bu,
    vacibdir, çünki sənəd bir dəfə vektorlaşdırılır, sonra həftələrlə
    saxlanılır. Əgər embedding hər dəfə fərqli olsaydı, köhnə vektorlar
    yararsız olardı. <code>başqası ilə: 0</code> isə göstərir ki, ortaq sözü
    olmayan mətnlər <em>heç oxşamır</em> — bu, hash əsaslı yanaşmanın
    məhdudiyyətidir: o, <strong>söz uyğunluğunu</strong> tapır, mənanı yox.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=3,
    ad="RagService — sənədlər arasında axtarış",
    a="""RAG (Retrieval-Augmented Generation) belə işləyir: sual vektora çevrilir,
    bazadakı bütün sənəd vektorları ilə müqayisə edilir və <strong>ən oxşar
    olanlar</strong> seçilir. Onlar AI-a «kontekst» kimi verilir. Bu addımda
    həm axtarış, həm də <code>sened.senedler</code> cədvəlini vektorlaşdıran
    köməkçi metod yaranır. Vektorlar <code>ai.embeddingler</code> cədvəlində
    JSONB kimi saxlanılır.""",
    b=[("src/ai/rag.service.ts", fayl("src/ai/rag.service.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayl yerindədirmi?
ls -l src/ai/rag.service.ts

# 2) İki metod var?
grep -nE 'async (axtar|vektorlasdir)\\(' src/ai/rag.service.ts

# 3) ⚠️ Nəticələr oxşarlığa görə SIRALANIRMI?
grep -n 'sort\\|slice' src/ai/rag.service.ts

# 4) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi\"""",
    c_olmaz="""$ curl -X POST localhost:4000/api/v1/ai/rag \\
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \\
    -d '{"sual":"Elmi Şura protokolu","limit":3}'

   # SIRALAMA olmasa — ən yaxşı nəticə BİRİNCİ gəlməz:

{
  "sual": "Elmi Şura protokolu",
  "tapildi": 3,
  "neticeler": [
    { "sened_id": 5, "metn": "Məzuniyyət ərizəsi",        "oxsarlıq": 0.12 },
    { "sened_id": 3, "metn": "Elmi Şura iclas protokolu", "oxsarlıq": 0.71 },
    { "sened_id": 8, "metn": "Yarımillik hesabat",        "oxsarlıq": 0.08 }
  ]
}

   # AI-a ən pis nəticə kontekst kimi verilir — cavab SƏHV olur.""",
    c_izah="""<code>sort((a, b) =&gt; b.oxsarlıq - a.oxsarlıq)</code> olmasa
    nəticələr bazadan gəldiyi sıra ilə qalır (yəni <code>id</code> üzrə) və
    <strong>ən oxşar sənəd həmişə birinci olmur</strong>. AI isə kontekstin
    <em>ilk</em> hissəsinə daha çox baxır — nəticədə düzgün sənəd tapılsa da,
    cavab yanlış olur. Sıralama bu addımın <strong>əsas məntiqidir</strong>.""",
    d="""$ curl -s -X POST localhost:4000/api/v1/ai/vektorlasdir \\
    -H "Authorization: Bearer $TOKEN"
{ "baxildi": 10, "yazildi": 10 }

$ curl -s -X POST localhost:4000/api/v1/ai/rag \\
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \\
    -d '{"sual":"Elmi Şura protokolu","limit":3}' | python3 -m json.tool
{
    "sual": "Elmi Şura protokolu",
    "tapildi": 3,
    "neticeler": [
        {
            "sened_id": 3,
            "metn": "Elmi Şura iclas protokolu",
            "oxsarlıq": 0.707107
        },
        {
            "sened_id": 7,
            "metn": "Elmi Şura qərarı (PISA qrupu)",
            "oxsarlıq": 0.408248
        },
        {
            "sened_id": 2,
            "metn": "Doktorantura yerləri barədə",
            "oxsarlıq": 0.0
        }
    ]
}""",
    d_izah="""Sistemin vəziyyəti: RAG işləyir. <code>sened_id: 3</code>
    <strong>0.707</strong> oxşarlıqla birinci gəlir — bu, «Elmi Şura» və
    «protokolu» sözlərinin hər ikisinin uyğun gəldiyini göstərir.
    Üçüncü nəticədə oxşarlıq <code>0.0</code>-dır, yəni heç bir ortaq söz yoxdur —
    o, sadəcə «limit 3» olduğu üçün siyahıya düşüb. Real sistemdə belə
    nəticələr <strong>kənarlaşdırılır</strong>: <code>oxsarlıq &gt; 0.3</code>
    kimi hədd qoyulur. Bu məhdudiyyət hash əsaslı embedding-dən irəli gəlir —
    real embedding API-si ilə «kurikulum» sualı «tədris proqramı» sənədini də
    tapardı, bizim versiya isə yalnız <em>eyni sözləri</em> tapır.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=4,
    ad="⚠️ SqlKomlekciService — resept ağ siyahısı",
    a="""Bu, dərsin <strong>ən vacib təhlükəsizlik addımıdır</strong>. «Təbii dil →
    SQL» adətən LLM-in SQL yazması kimi başa düşülür — bu isə
    <strong>təhlükəlidir</strong>: LLM <code>DROP TABLE</code> yaza bilər, səhv
    SQL ilə bazanı yora bilər, SQL inyeksiyasına qapı aça bilər. Biz fərqli yol
    seçirik: sual <em>əvvəlcədən yazılmış reseptlərin</em> açar sözləri ilə
    tutuşdurulur və yalnız uyğun reseptin SQL-i işlədilir. <strong>LLM SQL
    yazmır</strong> — SQL koda yazılıb.""",
    b=[("src/ai/sql-komlekci.service.ts", fayl("src/ai/sql-komlekci.service.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Neçə resept var?
grep -c "açar:" src/ai/sql-komlekci.service.ts

# 2) ⚠️ XÜSUSİ resept ümumidən ƏVVƏL gəlirmi?
grep -n "açar:" src/ai/sql-komlekci.service.ts | head -5

# 3) ⚠️ SQL KODDA yazılıb — istifadəçi mətnindən SQL-ə heç nə düşmür
grep -n 'prisma.\\$queryRaw' src/ai/sql-komlekci.service.ts | head -3

# 4) Nəticəni canlı yoxla
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi\"""",
    c_olmaz="""$ curl -s -X POST localhost:4000/api/v1/ai/sual \\
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \\
    -d '{"sual":"Orta maaş nə qədərdir?"}' | python3 -m json.tool

   # ⚠️ RESEPT SIRASI SƏHV OLSA (ümumi 'maaş' əvvəl gəlsə):

{
    "sual": "Orta maaş nə qədərdir?",
    "uygun_resept": true,
    "izah": "Ən çox maaş alan 5 nəfər",       ← SƏHV RESEPT!
    "setir_sayi": 5,
    "setirler": [ { "ad_soyad": "...", "maas": 2800 }, ... ]
}

   # İstifadəçi orta maaş soruşdu, sistem 5 nəfərin maaşını qaytardı.
   # Heç bir xəta çıxmır — sadəcə SƏHV cavab.""",
    c_izah="""«Orta maaş nə qədərdir?» sualı həm <code>orta maaş</code>, həm də
    <code>maaş</code> açarına uyğun gəlir. Reseptlər sıra ilə yoxlanıldığı üçün
    <strong>ümumi resept əvvəl olsa, xüsusi resept heç vaxt işləmir</strong>.
    Bu, ən çətin tapılan səhv növüdür: xəta yoxdur, cavab var — sadəcə yanlış
    cavab. Qayda: <strong>xüsusi reseptlər ümumilərdən əvvəl</strong>.""",
    d="""$ curl -s -X POST localhost:4000/api/v1/ai/sual \\
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \\
    -d '{"sual":"Neçə əməkdaş var?"}' | python3 -m json.tool
{
    "sual": "Neçə əməkdaş var?",
    "uygun_resept": true,
    "izah": "Ümumi əməkdaş sayı",
    "setir_sayi": 1,
    "setirler": [ { "emekdas_sayi": 14 } ]
}

════════ DÖRD SUAL — DÖRD DÜZGÜN RESEPT ════════

  Neçə əməkdaş var?         → Ümumi əməkdaş sayı
  Orta maaş nə qədərdir?    → Orta əmək haqqı          ← xüsusi resept
  Ən çox maaş alan 5 nəfər  → Ən çox maaş alan 5 nəfər
  Mərkəzlər üzrə bölgü      → Mərkəzlər üzrə şöbə və əməkdaş sayı
  Uçan boşqab neçədir?      → Bu sual üçün resept yoxdur

$ curl -s -X POST .../ai/reseptler -H "Authorization: Bearer $TOKEN"
{ "say": 10, "reseptler": [ { "açar": "...", "izah": "..." }, ... ] }""",
    d_izah="""Sistemin vəziyyəti: təbii dil sorğusu işləyir və
    <strong>təhlükəsizdir</strong>. «Uçan boşqab neçədir?» sualı üçün resept
    tapılmır və sistem <code>uygun_resept: false</code> qaytarır — uydurma
    cavab vermir. Diqqət yetirin: SQL sorğularının hamısı
    <code>sql-komlekci.service.ts</code> faylında, <strong>kodda</strong>
    yazılıb; istifadəçi mətnindən SQL-ə <em>heç nə</em> düşmür. Yeni sual növü
    lazım olsa, yeni resept əlavə edilir — bu, bir sətirlik dəyişiklikdir və
    hər dəfə yoxlanıla bilər.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=5,
    ad="DeepseekService — API müştərisi və demo rejim",
    a="""Bu servis DeepSeek API-si ilə danışır. Ən vacib qərar:
    <strong>açar olmayanda sistem sınmamalıdır</strong>. Ona görə
    <code>demoRejim</code> yoxlaması var — açar boşdursa kod API-yə
    <em>heç getmir</em>, dərhal nümunə cavab qaytarır. Cavabda
    <code>demo: true</code> sahəsi olur ki, frontend istifadəçini
    xəbərdar edə bilsin. Node 22-nin daxili <code>fetch</code>-i işlədilir —
    əlavə HTTP paketi lazım deyil.""",
    b=[("src/ai/deepseek.service.ts", fayl("src/ai/deepseek.service.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayl yerindədirmi?
ls -l src/ai/deepseek.service.ts

# 2) ⚠️ Demo rejim yoxlaması varmı?
grep -n 'demoRejim\\|demoCavab' src/ai/deepseek.service.ts

# 3) Konfiqurasiya .env-dən oxunurmu?
grep -n 'DEEPSEEK_API_KEY\\|DEEPSEEK_MODEL\\|DEEPSEEK_URL' src/ai/deepseek.service.ts

# 4) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi\"""",
    c_olmaz="""$ curl -s -X POST localhost:4000/api/v1/ai/cavab \\
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \\
    -d '{"sual":"Elmi Şura protokolu"}'

   # Demo rejim yoxlaması OLNASA — açar boş olduğu üçün
   # sorğu gedir və şəbəkə xətası qayıdır:

Error: fetch failed
    at DeepseekService.soruş (deepseek.service.js:41:17)
    at AiService.cavabla (ai.service.js:38:22)

HTTP/1.1 500 Internal Server Error""",
    c_izah="""Açar boş olsa da <code>fetch</code> çağırılsa, sorğu
    <code>Authorization: Bearer </code> ilə gedir və API <code>401</code>
    qaytarır — ya da şəbəkə olmayan mühitdə ümumiyyətlə uğursuz olur. Hər iki
    halda istifadəçi <strong>500</strong> görür. Demo rejim bunun qarşısını alır
    və eyni zamanda <em>dürüstdür</em>: cavabın uydurma olduğunu
    <code>demo: true</code> ilə bildirir.""",
    d="""$ curl -s -X POST localhost:4000/api/v1/ai/cavab \\
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \\
    -d '{"sual":"Elmi Şura protokolu"}' | python3 -m json.tool
{
    "sual": "Elmi Şura protokolu",
    "cavab": "[DEMO REJİM] «Elmi Şura protokolu» sualı üzrə 3 sənəd tapıldı. Ən uyğun: Elmi Şura iclas protokolu…",
    "model": "deepseek-chat (demo)",
    "demo": true,
    "token_sayi": 0,
    "istifade_olunan_senedler": [ 3, 7, 2 ]
}

$ curl -s localhost:4000/api/v1/ai/statistika -H "Authorization: Bearer $TOKEN"
{
    "rejim": "demo",
    "embedding_sayi": 18,
    "resept_sayi": 10,
    "olcu": 64,
    "vektor_bazasi": "JSONB (tətbiq tərəfində kosinus)"
}""",
    d_izah="""Sistemin vəziyyəti: AI cavabı işləyir — demo rejimdə belə
    <strong>faydalı məlumat</strong> qaytarır: RAG hansı sənədləri tapdığını
    göstərir (<code>[3, 7, 2]</code>). Yəni açar olmasa da sistemin
    <em>axtarış</em> hissəsi tam işləyir; yalnız təbii dil cavabı uydurmadır.
    Real açar əlavə edildikdə <code>rejim: "canli"</code> olacaq və eyni kod
    həqiqi AI cavabı qaytaracaq — <strong>bir sətir dəyişmədən</strong>.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=6,
    ad="AiService, DTO və controller",
    a="""Bu addım AI qatını HTTP-yə açır. <code>AiService</code> üç servisi
    (<code>RagService</code>, <code>SqlKomlekciService</code>,
    <code>DeepseekService</code>) bir yerə yığır. <code>SualDto</code> sualın
    uzunluğunu yoxlayır — 3 simvoldan qısa sual mənasızdır, 500 simvoldan uzun
    sual isə AI-ı lazımsız yorur. Controller beş endpoint açır və
    vektorlaşdırmanı <code>@Roles('admin','muhendis')</code> ilə qoruyur —
    bu, bütün sənədləri yenidən hesablayan ağır əməliyyatdır.""",
    b=[
        ("src/ai/dto/sual.dto.ts", fayl("src/ai/dto/sual.dto.ts")),
        ("src/ai/ai.service.ts", fayl("src/ai/ai.service.ts")),
        ("src/ai/ai.controller.ts", fayl("src/ai/ai.controller.ts")),
        ("src/ai/ai.module.ts", fayl("src/ai/ai.module.ts")),
        ("src/app.module.ts", app_module_araliq()),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Beş endpoint yerindədirmi?
grep -nE '@(Get|Post)\\(' src/ai/ai.controller.ts

# 2) ⚠️ Vektorlaşdırma @Roles ilə qorunurmu?
grep -n -B1 'vektorlasdir' src/ai/ai.controller.ts | head -4

# 3) AiModule kök modula qoşulubmu?
grep -n 'AiModule' src/app.module.ts

# 4) ⚠️ IxracModule HƏLƏ YOXDUR — qeydiyyat növbəti addımdadır
grep -c 'IxracModule' src/app.module.ts        # → 0

# 5) Build — məhz bu yoxlama irəliyə istinadı tutur
npm run build && echo "✓ build keçdi\"""",
    c_olmaz="""$ curl -s -o /dev/null -w '%{http_code}\\n' -X POST \\
    localhost:4000/api/v1/ai/vektorlasdir \\
    -H "Authorization: Bearer $BAXICI_TOKEN"

   # @Roles olmasa — istənilən istifadəçi bütün sənədləri
   # yenidən vektorlaşdıra bilər:

200        ← hər çağırışda 10 sorğu + 10 INSERT
           ← 5 dəfə çağırsa baza 50 yeni embedding sətri ilə dolar

   # @Roles('admin','muhendis') ilə:
403        ← yalnız səlahiyyətli şəxs işlədə bilər""",
    c_izah="""Vektorlaşdırma «oxuma» deyil, <strong>yazma</strong> əməliyyatıdır: hər
    çağırışda bütün sənədlər üçün embedding hesablanır və bazaya yazılır.
    Qorunmasa istənilən istifadəçi onu təkrar-təkrar çağırıb bazanı doldura
    bilər. Bu, <em>xidmətdən imtina</em> (DoS) hücumunun ən sadə formasıdır —
    ona görə <code>@Roles</code> mütləqdir.""",
    d="""$ npm run build
> ds-backend@0.1.0 build
> nest build

$ node dist/main.js
[Nest] LOG [RoutesResolver] AiController {/api/v1/ai}: +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/ai/statistika, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/ai/reseptler, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/ai/rag, POST} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/ai/sual, POST} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/ai/cavab, POST} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/ai/vektorlasdir, POST} route +0ms
[Nest] LOG [BAŞLANGIC] API hazırdır → http://localhost:4000/api/v1

$ curl -s -o /dev/null -w '%{http_code}\\n' -X POST .../ai/vektorlasdir \\
    -H "Authorization: Bearer $BAXICI_TOKEN"
403

$ curl -s -o /dev/null -w '%{http_code}\\n' -X POST .../ai/vektorlasdir \\
    -H "Authorization: Bearer $ADMIN_TOKEN"
200""",
    d_izah="""Sistemin vəziyyəti: AI qatı HTTP-yə açıldı — <strong>5 yeni
    marshrut</strong>. Vektorlaşdırma qorunur: <code>baxici</code> rolu
    <code>403</code>, <code>admin</code> <code>200</code> alır. Diqqət yetirin:
    <code>GET /ai/statistika</code> və <code>GET /ai/reseptler</code>
    qorunmur (yalnız token tələb olunur) — onlar heç nə dəyişmir, sadəcə
    məlumat göstərir. <code>POST /ai/sual</code> və <code>/ai/rag</code> isə
    yalnız <em>oxuyur</em>, ona görə rol tələb etmir.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=7,
    ad="Excel ixracı",
    a="""İstifadəçilər məlumatı Excel-də görmək istəyir — bu, hesabatların
    ən çox yayılmış formasıdır. <code>ExcelService</code> iki fayl yaradır:
    mərkəzlər və əməkdaşlar. Fayl <strong>yaddaşda</strong> qurulur və birbaşa
    HTTP cavabı kimi göndərilir — diskə heç nə yazılmır. Başlıq sətri qalın və
    boz fonla işarələnir, avtofiltr əlavə olunur ki, istifadəçi dərhal
    süzgəc qoya bilsin.""",
    b=[
        ("src/ixrac/excel.service.ts", fayl("src/ixrac/excel.service.ts")),
        ("src/ixrac/ixrac.controller.ts", fayl("src/ixrac/ixrac.controller.ts")),
        ("src/ixrac/ixrac.module.ts", fayl("src/ixrac/ixrac.module.ts")),
        ("src/app.module.ts", fayl("src/app.module.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayllar yerindədirmi?
ls -1 src/ixrac/

# 2) ⚠️ ExcelJS DEFAULT import ilə gəlirmi?
grep -n "import ExcelJS" src/ixrac/excel.service.ts

# 3) ⚠️ Düzgün MIME tipi göndərilirmi?
grep -n 'spreadsheetml' src/ixrac/ixrac.controller.ts

# 4) ⚠️ app.module.ts-ə IxracModule əlavə olundumu?
grep -n 'IxracModule' src/app.module.ts

# 5) Fayl REAL Excel-dirmi?
npm run build && node dist/main.js &
sleep 6
TOKEN=$(curl -s -X POST localhost:4000/api/v1/auth/login \\
  -H 'Content-Type: application/json' \\
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \\
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
curl -s -o /tmp/yoxla.xlsx localhost:4000/api/v1/ixrac/merkezler.xlsx \\
  -H "Authorization: Bearer $TOKEN"
file /tmp/yoxla.xlsx
""",
    c_olmaz="""$ curl -s -o /tmp/yoxla.xlsx localhost:4000/api/v1/ixrac/merkezler.xlsx \\
    -H "Authorization: Bearer $TOKEN"
$ file /tmp/yoxla.xlsx

   # ⚠️ 'import * as ExcelJS' işlədilsə:

/tmp/yoxla.xlsx: ASCII text

$ cat /tmp/yoxla.xlsx
{"ugur":false,"xeta":{"kod":"DAXILI_XETA",
 "mesaj":"ExcelJS.Workbook is not a constructor"}}

   # Fayl Excel DEYİL — sadəcə xəta mesajı olan mətn faylı!""",
    c_izah="""<code>import * as ExcelJS from 'exceljs'</code> yazsaq, ESM/CJS
    qarışıqlığı yaranır: <code>ExcelJS</code> obyektinin içində
    <code>Workbook</code> <strong>olmur</strong> (o, <code>default</code> altında
    gizlənir). Nəticədə <code>new ExcelJS.Workbook()</code> xəta atır və
    istifadəçi <em>Excel əvəzinə JSON xətası</em> yükləyir. Fayl
    <code>.xlsx</code> adlanır, amma açılmır — bu, ən çaşdırıcı xəta növüdür.""",
    d="""$ curl -s -D - -o /tmp/merkezler.xlsx \\
    localhost:4000/api/v1/ixrac/merkezler.xlsx -H "Authorization: Bearer $TOKEN"

HTTP/1.1 200 OK
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="merkezler_2026-09-21.xlsx"
Content-Length: 7121

$ file /tmp/merkezler.xlsx
/tmp/merkezler.xlsx: Microsoft Excel 2007+

$ curl -s -o /tmp/emekdaslar.xlsx \\
    localhost:4000/api/v1/ixrac/emekdaslar.xlsx -H "Authorization: Bearer $TOKEN"
$ ls -l /tmp/*.xlsx
-rw-r--r--  1 user  staff  7121  merkezler.xlsx
-rw-r--r--  1 user  staff  8197  emekdaslar.xlsx""",
    d_izah="""Sistemin vəziyyəti: Excel ixracı işləyir. Fayllar
    <strong>həqiqi Excel 2007+</strong> formatındadır (mərkəzlər 7 121 bayt,
    əməkdaşlar 8 197 bayt) və brauzer onları avtomatik yükləyir — çünki
    <code>Content-Disposition: attachment</code> başlığı var.
    <code>autoFilter</code> sayəsində istifadəçi faylı açan kimi başlıq
    sətrində süzgəc düymələrini görür. Fayllar <strong>yaddaşda</strong>
    qurulur — server diskdə heç nə saxlamır, ona görə paralel 100 istifadəçi
    yükləsə də disk dolmur.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=8,
    ad="Docker və CI/CD",
    a="""Layihə işləyir, amma başqa kompüterdə də işləməlidir. Docker
    <strong>iki mərhələli</strong> yığım işlədir: birinci mərhələdə TypeScript
    yığılır, ikincidə isə yalnız <code>dist</code> və istehsalat asılılıqları
    köçürülür — beləliklə obraz kiçik olur. <code>docker-compose.yml</code> həm
    bazanı, həm API-ı qaldırır. CI isə hər <code>push</code>-da testləri
    avtomatik işlədir ki, sınıq kod əsas budağa düşməsin.""",
    b=[
        ("Dockerfile", fayl("Dockerfile")),
        (".dockerignore", fayl(".dockerignore")),
        ("docker-compose.yml", fayl("docker-compose.yml")),
        (".github/workflows/ci.yml", fayl(".github/workflows/ci.yml")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayllar yerindədirmi?
ls -1 Dockerfile .dockerignore docker-compose.yml .github/workflows/ci.yml

# 2) ⚠️ CI-da PostgreSQL HEALTH CHECK varmı?
grep -n -A5 'options:' .github/workflows/ci.yml

# 3) ⚠️ .env Docker obrazına düşməsin
grep -n '.env' .dockerignore

# 4) docker-compose konfiqurasiyası düzgündürmü?
docker compose config > /dev/null 2>&1 && echo "✓ compose faylı düzgündür" || \\
  echo "(docker quraşdırılmayıb — fayl yenə etibarlıdır)\"""",
    c_olmaz="""$ npx vitest run --config vitest.config.e2e.ts      # CI-da:

 FAIL  test/backend3-auth.e2e-spec.ts
Error: connect ECONNREFUSED 127.0.0.1:5432

   # HEALTH CHECK olmasa GitHub Actions PostgreSQL-i qaldırır,
   # amma HAZIR OLMAMIŞ testlər başlayır — bağlantı rədd olunur.

   # ⚠️ Və ən pisi: bu xəta TƏSADÜFİ olur — bəzən keçir, bəzən yox.
   # Ona görə "yenidən işlət" düyməsi problemi gizlədir.""",
    c_izah="""GitHub Actions <code>services</code> bloku konteyneri qaldırır, amma
    <strong>hazır olmasını gözləmir</strong> — növbəti addım dərhal başlayır.
    <code>--health-cmd pg_isready</code> seçimi Actions-a «bu servis hazır
    olana qədər gözlə» deyir. Bu olmasa testlər <code>ECONNREFUSED</code> alır
    və xəta <em>təsadüfi</em> görünür — bu, ən bezdirici CI problemidir.""",
    d="""$ ls -1 Dockerfile .dockerignore docker-compose.yml .github/workflows/ci.yml
Dockerfile
.dockerignore
docker-compose.yml
.github/workflows/ci.yml

$ grep -n -A5 'options:' .github/workflows/ci.yml
17:        options: >-
18-          --health-cmd pg_isready
19-          --health-interval 10s
20-          --health-timeout 5s
21-          --health-retries 5

$ docker compose config --services
baza
api

$ npm test
 Test Files  6 passed (6)
      Tests  42 passed (42)

$ npx vitest run --config vitest.config.e2e.ts
 Test Files  4 passed (4)
      Tests  39 passed (39)""",
    d_izah="""Sistemin vəziyyəti: layihə <strong>yerləşdirilməyə hazırdır</strong>.
    <code>docker compose up</code> əmri bazanı və API-ı birgə qaldırır;
    <code>Dockerfile</code> iki mərhələli olduğu üçün istehsalat obrazına
    <code>node_modules</code>-un hamısı deyil, yalnız lazımlı hissəsi düşür.
    CI isə hər <code>push</code>-da <strong>81 testi</strong>
    (42 unit + 39 e2e) avtomatik işlədir. <code>.dockerignore</code> faylı
    <code>.env</code>-i obrazdan kənarda saxlayır — bu vacibdir, çünki
    <code>.env</code>-dəki JWT açarı obrazın içinə düşsə, onu istənilən şəxs
    çıxara bilər.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=9,
    ad="Build və tam canlı yoxlama",
    a="""İndi bütün yeni qatları canlı yoxlayırıq: AI statistikası, reseptlər,
    vektorlaşdırma, RAG axtarışı, təbii dil sualı, AI cavabı və Excel ixracı.
    Yeddi yoxlamanın hamısı keçməlidir. Bu, dərsin ən vacib anıdır — burada
    ayrı-ayrı hissələr deyil, <strong>bütün sistem birlikdə</strong> işləyir.""",
    b=[
        ("Terminal 1 — serveri qaldır", terminal("""cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST

lsof -ti:4000 && kill $(lsof -ti:4000)
npm run build
npm run start:dev""")),
        ("Terminal 2 — AI və ixrac yoxlaması", terminal("""A=http://localhost:4000/api/v1

# ── Token AL və YADDA SAXLA ──
TOKEN=$(curl -s -X POST "$A/auth/login" \\
  -H 'Content-Type: application/json' \\
  -d '{"email":"admin@arti.edu.az","parol":"123456"}' \\
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
echo "$TOKEN" > /tmp/arti_token.txt

# ── 1) AI STATİSTİKA ──
curl -s "$A/ai/statistika" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# ── 2) RESEPTLƏR (ağ siyahı) ──
curl -s "$A/ai/reseptler" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# ── 3) VEKTORLAŞDIRMA ──
curl -s -X POST "$A/ai/vektorlasdir" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# ── 4) RAG AXTARIŞ ──
curl -s -X POST "$A/ai/rag" -H 'Content-Type: application/json' \\
  -H "Authorization: Bearer $TOKEN" \\
  -d '{"sual":"Elmi Şura protokolu","limit":3}' | python3 -m json.tool

# ── 5) TƏBİİ DİL SUALI ──
for s in "Neçə əməkdaş var?" "Orta maaş nə qədərdir?" "Uçan boşqab neçədir?"; do
  printf '%-26s → ' "$s"
  curl -s -X POST "$A/ai/sual" -H 'Content-Type: application/json' \\
    -H "Authorization: Bearer $TOKEN" -d "{\\"sual\\":\\"$s\\"}" \\
    | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['izah'][:45])"
done

# ── 6) AI CAVABI (RAG ilə) ──
curl -s -X POST "$A/ai/cavab" -H 'Content-Type: application/json' \\
  -H "Authorization: Bearer $TOKEN" -d '{"sual":"Elmi Şura protokolu"}' \\
  | python3 -m json.tool

# ── 7) EXCEL İXRACI ──
for f in merkezler emekdaslar; do
  curl -s -o "/tmp/$f.xlsx" "$A/ixrac/$f.xlsx" -H "Authorization: Bearer $TOKEN"
  printf '  %-12s → %s bayt · %s\\n' "$f" "$(wc -c < /tmp/$f.xlsx | tr -d ' ')" \\
    "$(file -b /tmp/$f.xlsx)"
done
""")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Neçə marshrut var? (23 olmalıdır — 15 əvvəlki + 6 AI + 2 ixrac)
curl -s http://localhost:4000/docs-json | python3 -c "
import json, sys
d = json.load(sys.stdin)
say = 0
for yol in sorted(d['paths']):
    for m in d['paths'][yol]:
        say += 1
        qeyd = 'AI' if '/ai/' in yol else ('IXRAC' if '/ixrac/' in yol else '')
        print(f'  {m.upper():6s} {yol:<42} {qeyd}')
print('  CƏMİ:', say, 'marshrut')
"

# 2) Excel faylları REAL-dırmı?
file /tmp/merkezler.xlsx /tmp/emekdaslar.xlsx

# 3) ⚠️ Vektorlaşdırma rol qorunması
for rol in admin baxici; do
  T=$(curl -s -X POST http://localhost:4000/api/v1/auth/login \\
    -H 'Content-Type: application/json' \\
    -d "{\\"email\\":\\"$rol@arti.edu.az\\",\\"parol\\":\\"123456\\"}" \\
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  printf '  %-10s vektorlasdir → %s\\n' "$rol" \\
    "$(curl -s -o /dev/null -w '%{http_code}' -X POST \\
       http://localhost:4000/api/v1/ai/vektorlasdir -H "Authorization: Bearer $T")"
done
""",
    c_olmaz="""$ curl -s localhost:4000/api/v1/ai/statistika -H "Authorization: Bearer $TOKEN"

   # AI modulu app.module-a qoşulmasa:

{"ugur":false,"xeta":{"kod":"TAPILMADI",
 "mesaj":"Cannot GET /api/v1/ai/statistika"},
 "yol":"/ai/statistika","vaxt":"2026-09-21T06:12:44.118Z"}

   # Server logunda AiController ÜMUMİYYƏTLƏ yoxdur:
[Nest] LOG [RoutesResolver] KadrlarController {/api/v1/kadrlar/emekdaslar}: +0ms
   (AiController sətri yoxdur)""",
    c_izah="""<code>AiModule</code> və <code>IxracModule</code>
    <code>app.module.ts</code>-in <code>imports</code> siyahısına əlavə
    olunmasa, controller-lər <strong>ümumiyyətlə yaranmır</strong> — marshrutlar
    qeydiyyatdan keçmir və bütün AI endpoint-ləri <code>404</code> verir. Bu,
    Dərs 2-də gördüyümüz eyni səhvdir: fayllar yazılır, modul qoşulmağı
    unudulur.""",
    d="""$ curl -s localhost:4000/docs-json | python3 -c "..."
  GET    /api/v1
  POST   /api/v1/ai/cavab                            AI
  POST   /api/v1/ai/rag                              AI
  GET    /api/v1/ai/reseptler                        AI
  GET    /api/v1/ai/statistika                       AI
  POST   /api/v1/ai/sual                             AI
  POST   /api/v1/ai/vektorlasdir                     AI
  GET    /api/v1/auth/istifadeciler
  POST   /api/v1/auth/login
  GET    /api/v1/auth/profil
  POST   /api/v1/auth/qeydiyyat
  GET    /api/v1/ixrac/emekdaslar.xlsx               IXRAC
  GET    /api/v1/ixrac/merkezler.xlsx                IXRAC
  ... (struktur, kadrlar, sağlamlıq)
  CƏMİ: 23 marshrut

════════ EXCEL FAYLLARI ════════
  merkezler    → 7121 bayt · Microsoft Excel 2007+
  emekdaslar   → 8197 bayt · Microsoft Excel 2007+

════════ VEKTORLAŞDIRMA QORUNMASI ════════
  admin      vektorlasdir → 200
  baxici     vektorlasdir → 403""",
    d_izah="""<strong>Backend-4 tam işlək vəziyyətdədir.</strong> Əlavə olunan
    <strong>8 marshrut</strong> (6 AI + 2 ixrac) digər 15 ilə birlikdə işləyir —
    cəmi <strong>23 marshrut</strong>. Excel faylları həqiqi Excel formatındadır
    və brauzer onları yükləyir. Vektorlaşdırma isə rol ilə qorunur:
    <code>admin</code> <code>200</code>, <code>baxici</code>
    <code>403</code>. Bu andan etibarən institutun məlumatları həm
    <em>API</em>, həm <em>Excel</em>, həm də <em>təbii dil</em> vasitəsilə
    əlçatandır.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=10,
    ad="Testlər — AI və ixrac",
    a="""AI qatının testləri xüsusi diqqət tələb edir: <strong>vektor
    riyaziyyatı</strong> səhv olsa heç bir xəta çıxmır, sadəcə axtarış
    nəticələri yanlış olur. Ona görə burada sərhəd halları yoxlanılır:
    vektor ölçüsü, normallaşdırma, deterministiklik, oxşarlıq və
    <strong>resept sırası</strong>. Sonuncu xüsusilə vacibdir — bu dərsdə
    məhz o səhvi tapıb düzəltdik.""",
    b=[
        ("src/ai/embedding.service.spec.ts", fayl("src/ai/embedding.service.spec.ts")),
        ("src/ai/sql-komlekci.service.spec.ts",
         fayl("src/ai/sql-komlekci.service.spec.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Test faylları yerindədirmi?
ls -1 src/ai/*.spec.ts

# 2) ⚠️ Sərhəd halları yoxlanılırmı?
grep -n 'OLCU\\|normallaş\\|deterministik\\|XÜSUSİ' src/ai/embedding.service.spec.ts \\
  src/ai/sql-komlekci.service.spec.ts

# 3) BÜTÜN testlər
npm test
npx vitest run --config vitest.config.e2e.ts
""",
    c_olmaz="""$ npm test      # resept sırası testi olmasa:

 Test Files  6 passed (6)
      Tests  41 passed (41)          ← "Orta maaş" səhvi TUTULMUR

$ curl ... -d '{"sual":"Orta maaş nə qədərdir?"}'
{ "izah": "Ən çox maaş alan 5 nəfər" }     ← YANLIŞ cavab,
                                             heç bir test sınıq deyil""",
    c_izah="""Test <code>expect(r?.izah).toBe('Orta əmək haqqı')</code> yazır —
    yəni kodun <em>nə etdiyini</em> deyil, <code>nə etməli olduğunu</code>.
    Test olmasa resept sırası dəyişdirilsə (məsələn yeni developer faylı
    redaktə etsə) səhv <strong>sükutla</strong> qayıdar. AI qatında bu xüsusilə
    təhlükəlidir: istifadəçi yanlış rəqəmə baxıb yanlış <em>qərar</em> verə
    bilər və bunu heç vaxt bilməz.""",
    d="""$ npm test

 RUN  v4.1.11 /Users/royatalibova/Deepseek_ARTI/DS_Backend

 ✓ src/common/dto/sehife.dto.spec.ts (9 tests)
 ✓ src/saglamliq/saglamliq.service.spec.ts (3 tests)
 ✓ src/struktur/struktur.service.spec.ts (9 tests)
 ✓ src/auth/auth.service.spec.ts (8 tests)
 ✓ src/ai/embedding.service.spec.ts (7 tests)
 ✓ src/ai/sql-komlekci.service.spec.ts (6 tests)

 Test Files  6 passed (6)
      Tests  42 passed (42)

$ npx vitest run --config vitest.config.e2e.ts

 ✓ test/struktur.e2e-spec.ts (14 tests)
 ✓ test/kadrlar.e2e-spec.ts (7 tests)
 ✓ test/backend3-auth.e2e-spec.ts (14 tests)
 ✓ test/saglamliq.e2e-spec.ts (4 tests)

 Test Files  4 passed (4)
      Tests  39 passed (39)

──────────────────────────────────────────────
YEKUN: 42 unit + 39 e2e = 81 test""",
    d_izah="""<strong>Backend-4 tamamlandı.</strong> Bütün backend kursunun yekunu:
    <ul>
      <li><strong>42 unit + 39 e2e = 81 test</strong> — Dərs 1-də 7 test idi.</li>
      <li><strong>23 marshrut</strong> — sağlamlıq, struktur, kadrlar, auth,
          AI və ixrac.</li>
      <li><strong>AI qatı</strong> — RAG axtarışı, 10 reseptli təbii dil
          sorğusu, demo rejim.</li>
      <li><strong>Excel ixracı</strong> — həqiqi <code>.xlsx</code> faylları.</li>
      <li><strong>Docker + CI</strong> — layihə istənilən mühitdə qalxır.</li>
    </ul>
    <p><strong>Növbəti addım:</strong> frontend — bu API-ı istifadəçiyə
    göstərən veb interfeys. Bütün endpoint-lər hazırdır və
    <code>/docs</code> ünvanında sənədləşdirilib.</p>""",
)

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






# ─────────────────────────────────────────────────────────────────
#  ADDIM 11 — BACKEND-4 TAM QƏBUL TESTİ
# ─────────────────────────────────────────────────────────────────
_CEDVEL = """<table>
  <tr><th>#</th><th>Nə yoxlanılır</th><th>Rol</th><th>Gözlənilən cavab</th></tr>
  <tr><td>1</td><td>Fayllar və paketlər — 13 AI/ixrac faylı, Docker, CI</td><td>—</td>
      <td>hamısı <code>var</code> · <code>exceljs 4.4.0</code></td></tr>
  <tr><td>2</td><td><code>.env</code> → <code>DEEPSEEK_API_KEY</code> boşdur</td><td>—</td>
      <td>boş sətir → <strong>demo rejim</strong> işə düşür</td></tr>
  <tr><td>3</td><td>⚠️ SQL xidməti LLM-ə qoşulmur</td><td>—</td>
      <td><code>fetch = 0</code> · <code>deepseek = 0</code></td></tr>
  <tr><td>4</td><td><code>GET /ai/statistika</code></td>
      <td><strong>4 rolun hamısı</strong></td><td><code>200</code> · tokensiz <code>401</code></td></tr>
  <tr><td>5</td><td>Statistikanın məzmunu</td><td>admin</td>
      <td><code>rejim=demo</code> · <code>olcu=64</code> · <code>resept_sayi=10</code></td></tr>
  <tr><td>6</td><td><code>GET /ai/reseptler</code></td><td>admin</td>
      <td><code>say=10</code> · hər reseptdə <code>açar</code> + <code>izah</code></td></tr>
  <tr><td>7</td><td>⚠️ <strong>Resept SIRASI</strong></td><td>—</td>
      <td>«orta maaş» ümumi «maaş»-dan <strong>ƏVVƏL</strong></td></tr>
  <tr><td>8</td><td><code>POST /ai/sual</code> — uyğun sual</td><td>admin</td>
      <td><code>uygun_resept=true</code> · <code>setir_sayi ≥ 1</code></td></tr>
  <tr><td>9</td><td>⚠️ «Orta maaş nə qədərdir?»</td><td>admin</td>
      <td><strong>Orta əmək haqqı</strong> — səhv reseptə düşmür</td></tr>
  <tr><td>10</td><td>Naməlum sual</td><td>admin</td>
      <td><code>200</code> · <code>uygun_resept=false</code> — <strong>500 DEYİL</strong></td></tr>
  <tr><td>11</td><td>DTO validasiyası: boş · 2 simvol · sahəsiz</td><td>—</td>
      <td><code>400 · 400 · 400</code></td></tr>
  <tr><td>12</td><td>⚠️ <strong>SQL inyeksiya cəhdi</strong></td><td>admin</td>
      <td><code>200</code> · cədvəllər <strong>SALAMAT</strong> qalır</td></tr>
  <tr><td>13</td><td><code>POST /ai/rag</code> — kosinus axtarışı</td><td>admin</td>
      <td>3 nəticə · <strong>azalan</strong> · ballar <code>0..1</code></td></tr>
  <tr><td>14</td><td><code>POST /ai/cavab</code></td><td>admin</td>
      <td><code>demo=true</code> · <code>token_sayi=0</code></td></tr>
  <tr><td>15</td><td><code>POST /ai/vektorlasdir</code></td>
      <td><strong>admin</strong>, <strong>muhendis</strong></td><td><code>200</code></td></tr>
  <tr><td>16</td><td><code>POST /ai/vektorlasdir</code></td>
      <td><strong>maliyyeci</strong>, <strong>baxici</strong></td><td><code>403</code></td></tr>
  <tr><td>17</td><td>Excel ixracı — <code>PK</code> baytları</td>
      <td><strong>4 rolun hamısı</strong></td>
      <td><code>200</code> · <code>504b</code> · sətir = baza + 1</td></tr>
  <tr><td>18</td><td>Docker və GitHub Actions</td><td>—</td>
      <td>2 × <code>FROM node</code> · <code>npm ci</code> · <code>vitest.config.e2e.ts</code></td></tr>
  <tr><td>19</td><td>Marshrutlar</td><td>—</td>
      <td><strong>20 yol</strong> · <strong>23 metod+yol</strong></td></tr>
  <tr><td>20</td><td>Testlər</td><td>—</td>
      <td><strong>42 unit + 39 e2e = 81</strong></td></tr>
</table>"""

_A11 = """Bu dərsdə <strong>10 addımda</strong> backend-in üstünə tamamilə yeni bir
qat qurduq: AI. İndi isə hamısını <strong>bir dəfəlik yoxlayan</strong> qəbul
testi yazırıq. Bu, Backend-3-dəki qəbul testindən <em>tamamilə fərqlidir</em> —
o test autentifikasiyanı yoxlayırdı, bu test isə <strong>süni intellekt qatını,
RAG axtarışını, resept ağ siyahısını, Excel ixracını və Docker quruluşunu</strong>
yoxlayır. Skript serveri ayağa qaldırdıqdan sonra <strong>122 yoxlama</strong>
aparır və hər biri üçün <em>hansı rolu</em> yoxladığını və <em>cavabın necə
olmalı olduğunu</em> göstərir."""

_C_YOXLA = """cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST

# 1) Sintaksis düzgündürmü?
bash -n scripts/yoxla-backend4.sh && echo "✓ sintaksis OK"

# 2) Server AYRI terminalda işləməlidir
PORT=4000 npm run start:prod

# 3) Digər terminalda — tam qəbul testi
bash scripts/yoxla-backend4.sh

# 4) Çıxış kodu (CI üçün)
echo "exit: $?"
#   0 → bütün yeniliklər işləyir
#   1 → ən azı bir yoxlama uğursuz

# 5) ⚠️ Ən vacib yoxlama tək başına — SQL inyeksiyası
psql -U arti_user -d arti_baza -tA \
  -c "SELECT count(*) FROM struktur.merkezler"      # 10
# serveri işlək saxlayaraq inyeksiya göndərin:
curl -s -X POST http://localhost:4000/api/v1/ai/sual \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $ADMIN" \
  -d '{"sual":"mərkəz'"'"'; DROP TABLE struktur.merkezler; --"}'
psql -U arti_user -d arti_baza -tA \
  -c "SELECT count(*) FROM struktur.merkezler"      # YENƏ 10 — cədvəl yerindədir

# 6) Server başqa portdadırsa
A=http://localhost:4100/api/v1 bash scripts/yoxla-backend4.sh"""

_C_OLMAZ = """$ A=http://localhost:4101/api/v1 bash scripts/yoxla-backend4.sh
     # ⚠️ SIRA TƏRS ÇEVRİLMİŞ: ümumi 'maaş' resepti xüsusi 'orta maaş'-dan ƏVVƏL

════════════════════════════════════════════════════════════
  3 · GET /ai/reseptler — 10 resept və SIRA qaydası
════════════════════════════════════════════════════════════
  ✗ xüsusi resept ümumidən ƏVVƏLdir               yox (gözlənilən: var)

════════════════════════════════════════════════════════════
  4 · POST /ai/sual — təbii dil → cədvəl (LLM SQL YAZMIR)
════════════════════════════════════════════════════════════
  ✗ «Orta maaş…» → xüsusi resept      Ən çox maaş alan 5 nəfər (gözlənilən: Orta əmək haqqı)
  ✗ «Orta maaş…» SƏHV reseptə düşmür                var (gözlənilən: yox)

════════════════════════════════════════════════════════════
  12 · ADDIM 10 — unit və e2e testlər
════════════════════════════════════════════════════════════
  ✗ unit testlər keçir = 42                          0 (gözlənilən: 42)
  ✗ cəmi test = 81                                    39 (gözlənilən: 81)

════════════════════════════════════════════════════════════
  ✗ 5 YOXLAMA UĞURSUZ — 117 keçdi
════════════════════════════════════════════════════════════

     # ⚠️ DİQQƏT: XƏTA VERMİR — sadəcə SƏHV CAVAB verir.
     # «Orta maaş nə qədərdir?» sualına «Ən çox maaş alan 5 nəfər»
     # cavabı gəlir. HTTP 200 qayıdır, jurnal təmizdir, heç nə
     # qırılmır — istifadəçi sadəcə YANLIŞ rəqəm görür.
     # Bu, ən təhlükəli xəta növüdür: səssiz səhv cavab."""

_C_IZAH = """Bu, bütün kursun <strong>ən vacib dərsi</strong>dir. Yuxarıdaki çıxışda
skript <em>xəta vermir</em> — <code>npm run build</code> təmiz keçir, server
işləyir, jurnal təmizdir. Sadəcə <strong>səhv cavab</strong> qayıdır. Bu cür
səssiz səhvlər ən təhlükəlidir, çünki heç bir siqnal yoxdur: istifadəçi
«Orta maaş nə qədərdir?» soruşur, sistem «Ən çox maaş alan 5 nəfər» cavabını
verir və bunu <em>düzgün cavab</em> kimi təqdim edir. Qərar verən şəxs yanlış
rəqəmə baxaraq qərar verir. Qəbul testi məhz bu səhvi tutur: <code>117 keçdi,
5 xəta</code> — və xətaların hamısı <strong>eyni səbəbdən</strong>dir. Skript
həm də <strong>CI üçün yararlıdır</strong>: çıxış kodu <code>0</code>/<code>1</code>
olduğu üçün GitHub Actions-da birbaşa işlədilə bilər."""

_D11 = """
════════════════════════════════════════════════════════════
  0 · GİRİŞ — dörd rol üçün token
════════════════════════════════════════════════════════════
  ✓ admin token alındı                               var
  ✓ muhendis token alındı                            var
  ✓ maliyyeci token alındı                           var
  ✓ baxici token alındı                              var

════════════════════════════════════════════════════════════
  1 · ADDIM 1, 2, 7, 8 — fayllar və paketlər
════════════════════════════════════════════════════════════
  ✓ exceljs package.json-da                            4.4.0
  ✓ src/ai/embedding.service.ts                        var
  ✓ src/ai/rag.service.ts                              var
  ✓ src/ai/sql-komlekci.service.ts                     var
  ✓ src/ai/deepseek.service.ts                         var
  ✓ src/ai/ai.service.ts                               var
  ✓ src/ai/dto/sual.dto.ts                             var
  ✓ src/ixrac/excel.service.ts                         var
  ✓ Dockerfile                                         var
  ✓ .dockerignore                                      var
  ✓ docker-compose.yml                                 var
  ✓ .github/workflows/ci.yml                           var
  ✓ .env → DEEPSEEK_API_KEY boşdur (demo)           
  ✓ .env → DEEPSEEK_MODEL                            deepseek-chat
  ✓ .env → DEEPSEEK_URL                              https://api.deepseek.com
  ✓ sql-komlekci fetch çağırmır                    0
  ✓ sql-komlekci DeepseekService-i import etmir        0

════════════════════════════════════════════════════════════
  2 · GET /ai/statistika — AI qatının vəziyyəti (rol: HAMISI)
════════════════════════════════════════════════════════════
  ✓ admin     → 200                                  200
  ✓ muhendis  → 200                                  200
  ✓ maliyyeci → 200                                  200
  ✓ baxici    → 200                                  200
  ✓ tokensiz  → 401                                  401
  ✓ rejim = demo (açar boş)                          demo
  ✓ olcu = 64                                          64
  ✓ resept_sayi = 10                                   10
  ✓ vektor bazası JSONB-dir                           var

════════════════════════════════════════════════════════════
  3 · GET /ai/reseptler — 10 resept və SIRA qaydası
════════════════════════════════════════════════════════════
  ✓ resept sayı = 10                                  10
  ✓ hər reseptdə 'açar' sahəsi                     10
  ✓ hər reseptdə 'izah' sahəsi                      10
  ✓ tokensiz → 401                                   401
  ✓ «orta maaş» resepti mövcuddur                  var
  ✓ «ümumi maaş» resepti mövcuddur                var
  ✓ xüsusi resept ümumidən ƏVVƏLdir               var

════════════════════════════════════════════════════════════
  4 · POST /ai/sual — təbii dil → cədvəl (LLM SQL YAZMIR)
════════════════════════════════════════════════════════════
  ✓ «Neçə əməkdaş var?» → 200                 200
  ✓ uygun_resept = true                                true
  ✓ izah = «Ümumi əməkdaş sayı»                 Ümumi əməkdaş sayı
  ✓ setir_sayi ≥ 1                                   var
  ✓ «Orta maaş…» → xüsusi resept               Orta əmək haqqı
  ✓ «Orta maaş…» SƏHV reseptə düşmür         yox
  ✓ «Ən çox maaş…» → ümumi resept            Ən çox maaş alan 5 nəfər
  ✓ naməlum sual → uygun_resept = false             false
  ✓ naməlum sual → setir_sayi = 0                   0
  ✓ naməlum sual → 500 DEYİL                       200
  ✓ naməlum sual → mövcud reseptləri sadalayır   var
  ✓ boş sual → 400                                  400
  ✓ 2 simvolluq sual → 400                           400
  ✓ sual sahəsi yoxdur → 400                        400
  ✓ tokensiz → 401                                   401

════════════════════════════════════════════════════════════
  5 · SQL inyeksiya cəhdi — SQL KODDADIR, bazaya çatmır
════════════════════════════════════════════════════════════
  ✓ inyeksiya mətni reseptə uyğun gəlir            true
  ✓ …amma 200 qaytarır (xəta yox)                  200
  ✓ uyğunsuz inyeksiya → uygun_resept = false       false
  ✓ struktur.merkezler cədvəli SALAMATDIR            10
  ✓ kadrlar.emekdaslar cədvəli SALAMATDIR            14
  ✓ struktur.merkezler hələ də mövcuddur           t
  ✓ kadrlar.emekdaslar hələ də mövcuddur           t

════════════════════════════════════════════════════════════
  6 · POST /ai/rag — kosinus oxşarlığı, azalan sıra
════════════════════════════════════════════════════════════
  ✓ rag → 200                                        200
  ✓ default limit = 3                                  3
  ✓ hər nəticədə sened_id var                      3
  ✓ hər nəticədə oxsarlıq var                     3
  ✓ oxşarlıqlar AZALAN sıradadır                   
  ✓ ballar 0..1 aralığındadır                      
  ✓ normallaşdırma: vahid vektor uzunluğu           var
  ✓ limit=1 → 1 nəticə                             1
  ✓ limit=11 → 400 (Max 10)                          400
  ✓ limit=0 → 400 (Min 1)                            400
  ✓ tokensiz → 401                                   401

════════════════════════════════════════════════════════════
  7 · POST /ai/cavab — API açarı OLMADAN işləyir
════════════════════════════════════════════════════════════
  ✓ cavab → 200                                      200
  ✓ demo = true                                        true
  ✓ model adında «demo» işarəsi                   var
  ✓ cavab boş deyil                                   var
  ✓ istifadə_olunan_senedler var                      var
  ✓ token_sayi = 0 (demo)                              0

════════════════════════════════════════════════════════════
  8 · POST /ai/vektorlasdir — RBAC (yalnız admin, mühendis)
════════════════════════════════════════════════════════════
  ✓ admin     → 200                                  200
  ✓ muhendis  → 200                                  200
  ✓ maliyyeci → 403                                  403
  ✓ baxici    → 403                                  403
  ✓ tokensiz  → 401                                  401
  ✓ 403 → xeta.kod = ICAZE_YOXDUR                    var
  ✓ vektorlaşdırmadan sonra embedding > 0            var

════════════════════════════════════════════════════════════
  9 · GET /ixrac/*.xlsx — həqiqi Excel faylı
════════════════════════════════════════════════════════════
  ✓ merkezler.xlsx → 200                             200
  ✓ emekdaslar.xlsx → 200                            200
  ✓ Content-Type düzgündür                          application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
  ✓ Content-Disposition = attachment                   var
  ✓ fayl adı .xlsx ilə bitir                         var
  ✓ merkezler PK baytları ilə başlayır             504b
  ✓ emekdaslar PK baytları ilə başlayır            504b
  ✓ merkezler ölçüsü > 5000 bayt                   var
  ✓ emekdaslar ölçüsü > 5000 bayt                  var
  ✓ file: merkezler = Excel 2007+                      var
  ✓ file: emekdaslar = Excel 2007+                     var
  ✓ merkezler: Excel sətri = baza + başlıq          11
  ✓ emekdaslar: Excel sətri = baza + başlıq         15
  ✓ Excel boş deyil (başlıqdan çox sətir)         var
  ✓ baxici    → merkezler.xlsx 200                   200
  ✓ maliyyeci → emekdaslar.xlsx 200                  200
  ✓ tokensiz  → 401                                  401

════════════════════════════════════════════════════════════
  10 · ADDIM 8 — Docker, docker-compose, GitHub Actions
════════════════════════════════════════════════════════════
  ✓ Dockerfile → FROM node                           var
  ✓ Dockerfile çoxmərhələlidir (2+ FROM)           var
  ✓ Dockerfile → prisma generate                     var
  ✓ Dockerfile yalnız istehsalat asılılıqları     var
  ✓ .dockerignore → node_modules                     var
  ✓ compose → postgres xidməti                      var
  ✓ compose → depends_on                             var
  ✓ CI → npm ci                                      var
  ✓ CI → npm run build                               var
  ✓ CI → vitest.config.e2e.ts                        var
  ✓ CI → postgres health check                       var

════════════════════════════════════════════════════════════
  11 · Bütün marshrutlar — Backend-4 sonrası
════════════════════════════════════════════════════════════
  ✓ Swagger cavab verir                                var
  ✓ fərqli yol sayı = 20                             20
  ✓ AI marshrutları = 6                               6
  ✓ ixrac marshrutları = 2                            2
  ✓ auth marshrutları = 4                             4
  ✓ kadrlar marshrutları = 3                          3
  ✓ struktur marshrutları = 3                         3
  ✓ metod+yol cütü = 23                              23

════════════════════════════════════════════════════════════
  12 · ADDIM 10 — unit və e2e testlər
════════════════════════════════════════════════════════════
  ✓ unit testlər keçir = 42                          42
  ✓ e2e testlər keçir = 39                           39
  ✓ cəmi test = 81                                    81

════════════════════════════════════════════════════════════
  ✓ BÜTÜN YENİLİKLƏR İŞLƏYİR — 122 yoxlama keçdi
════════════════════════════════════════════════════════════"""

_D_IZAH = """<strong>Backend-4-ün bütün yenilikləri işləyir — 122 yoxlama, 0 xəta.</strong>
Çıxışı yuxarıdan aşağı oxusanız, dərsin hər addımının canlı sübutunu görürsünüz:
<ul>
  <li><strong>Bölmə 1:</strong> 13 yeni fayl yerindədir, <code>exceljs</code>
      quraşdırılıb və <code>DEEPSEEK_API_KEY</code> <strong>boşdur</strong> —
      yəni aşağıdaki bütün AI nəticələri API açarı olmadan alınıb.</li>
  <li><strong>Bölmə 3:</strong> 10 reseptin <em>sırası</em> yoxlanılır: xüsusi
      «orta maaş» ümumi «maaş»-dan əvvəldir. Bu, ADDIM 4-də tapılan real
      səhvin bir daha təkrarlanmamasını təmin edir.</li>
  <li><strong>Bölmə 5:</strong> <code>'; DROP TABLE struktur.merkezler; --</code>
      mətni göndərilir, server <code>200</code> qaytarır və cədvəl
      <strong>10 sətirlə yerində qalır</strong>. Səbəb sadədir: SQL koddadır,
      istifadəçi mətnindən SQL-ə <em>heç nə</em> düşmür.</li>
  <li><strong>Bölmə 6:</strong> RAG nəticələri azalan sıradadır və ballar
      <code>0..1</code> aralığındadır — normallaşdırma işləyir.</li>
  <li><strong>Bölmə 8:</strong> vektorlaşdırma rol ilə qorunur:
      <code>admin</code>/<code>muhendis</code> <code>200</code>,
      <code>maliyyeci</code>/<code>baxici</code> <code>403</code>.</li>
  <li><strong>Bölmə 9:</strong> Excel faylları <code>PK</code> baytları ilə
      başlayır (həqiqi ZIP konteyneri) və sətir sayı <strong>bazadakı ilə
      üst-üstə düşür</strong> — 10 mərkəz + başlıq = 11 sətir.</li>
  <li><strong>Bölmə 11–12:</strong> 20 fərqli yol, 23 metod+yol cütü və
      <strong>42 unit + 39 e2e = 81 test</strong> keçir.</li>
</ul>
<p>Bu andan etibarən <strong>backend tamamlandı</strong> sayılır. Növbəti
mərhələ frontend-dir: eyni API-ni brauzerdə göstərən interfeys.</p>"""

_B11 = chr(10).join([
    '  <p><strong>Əvvəlcə — hər yoxlamanın nəyi, hansı rolu və nə gözlədiyi:</strong></p>',
    '  ' + _CEDVEL,
    '  <p>Aşağıdaki skript məhz bu yoxlamaları sıra ilə aparır. '
    'Onu <code>scripts/</code> qovluğuna yazın.</p>',
    '  <p class="fayl-ad">scripts/yoxla-backend4.sh</p>',
    '<pre><code>' + e(fayl("scripts/yoxla-backend4.sh")) + '</code></pre>',
]) + chr(10)

addim(
    n=11,
    ad="Tam qəbul testi — bütün yenilikləri bir-bir yoxla",
    a=_A11,
    b=[],
    b_html=_B11,
    c_yoxla=_C_YOXLA,
    c_olmaz=_C_OLMAZ,
    c_izah=_C_IZAH,
    d=_D11,
    d_izah=_D_IZAH,
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
<title>Backend 4 — AI qatı, ixrac və yerləşdirmə (A/B/C/D)</title>
<style>
{css}
</style>
</head>
<body>
<div class="container">

<header>
  <div class="lesson-badge">DS_Backend · Hissə 4 / 4</div>
  <h1>Backend 4 — AI qatı, ixrac və yerləşdirmə</h1>
  <p class="subtitle">Sistemi bağla, sonra açar paylaş — JWT token, dörd rol
    və hər dəyişikliyin izi. Hər addım 4 hissə: <strong>A</strong> niyə ·
    <strong>B</strong> kod · <strong>C</strong> yoxlama · <strong>D</strong> durum</p>
  <p class="meta">
    <span>NestJS 12</span>
    <span>Prisma 7</span>
    <span>{n} addım</span>
    <span>23 marshrut</span>
    <span>81 test</span>
  </p>
</header>

<div class="block block-ne">
  <span class="block-title">NƏ EDƏCƏYİK</span>
  <p>Backend-3-də API bağlandı. İndi onun üstünə <strong>süni intellekt
  qatını</strong> qururuq: sənədlər arasında məna axtarışı (RAG), təbii dildə
  sual vermə imkanı və Excel-ə ixrac. Sonda layihəni Docker ilə istənilən
  mühitə yerləşdirə biləcəyik.</p>
  <p><strong>Ön şərt:</strong> Backend-3 tamamlanmalıdır —
  <code>/api/v1/auth/login</code> token qaytarmalı və qorunan endpoint-lər
  tokensiz <code>401</code> verməlidir.</p>
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
