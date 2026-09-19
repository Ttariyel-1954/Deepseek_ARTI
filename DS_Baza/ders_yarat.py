# -*- coding: utf-8 -*-
"""Deepseek_Baza.html dərsini yaradır.

Mənbələr:
  - DS_Baza/sql/10_sorgular.sql   -> 40 sorğunun kodu
  - _hesabat/sorgu_cixis.txt      -> 40 sorğunun REAL çıxışı
  - DS_Baza/sql/00_*.sql          -> struktur faylları
Çıxış:
  - DƏRSLƏR/Deepseek_Baza.html    -> >=1700 sətir
"""
from __future__ import annotations

import html
import re
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent      # ~/Deepseek_ARTI
SQL = KOK / "DS_Baza/sql"
CIXIS = KOK / "_hesabat/sorgu_cixis.txt"
CIXIS.parent.mkdir(parents=True, exist_ok=True)

# ── CSS-i mövcud dərsdən götür (vahid görünüş) ──────────────────
CSS_FAYLI = Path(__file__).resolve().parent.parent / "DS_Baza/ders.css"
css = CSS_FAYLI.read_text(encoding="utf-8").strip("\n")

def e(metn: str) -> str:
    """HTML üçün təhlükəsiz hala gətirir."""
    return html.escape(str(metn), quote=False)

def blok(sinf: str, basliq: str, govde: str) -> str:
    return ('<div class="block %s">\n  <span class="block-title">%s</span>\n  %s\n</div>\n'
            % (sinf, basliq, govde))

# ══════════════════════════════════════════════════════════════
#  SORĞU İZAHATLARI — 40 ədəd
# ══════════════════════════════════════════════════════════════
S = {}

S[1] = dict(
    qrup="A", basliq="Sxemlər və cədvəl sayı",
    ne="information_schema.tables cədvəlindən bütün sxemləri oxuyur və hər sxemdə neçə əsas cədvəl olduğunu sayır.",
    gosterir="12 sxemin adını və hər birindəki cədvəl sayını: elm 8, struktur 7, kadrlar 5, tehsil 5 və s. Bu, bazanın 'kabinet siyahısı'dır.",
    olmaz="Hansı sxemin nə qədər böyük olduğunu bilməzdik. İşə başlayanda hara baxacağımızı təxmin etməli olardıq.",
    evez="<code>\\dt *.*</code> (psql xüsusi əmri) və ya DBeaver-in sol panelindəki ağac. Amma SQL sorğusu skriptə salına bilər, panel əl ilə baxılır.",
)

S[2] = dict(
    qrup="A", basliq="Cədvəllərin sətir sayı (canlı statistika)",
    ne="pg_stat_user_tables sistem cədvəlindən hər cədvəlin təxmini sətir sayını oxuyur.",
    gosterir="Hansı cədvəlin dolu, hansının boş olduğunu. audit_log 67, şöbələr 36, əməkdaşlar 14 sətir.",
    olmaz="Hər cədvəl üçün ayrı-ayrı <code>SELECT count(*)</code> yazmalı olardıq — 48 sorğu.",
    evez="<code>SELECT count(*) FROM ...</code> — dəqiq nəticə verir, amma hər cədvəli tam skan edir. <code>n_live_tup</code> isə statistikadan oxuyur və anidir.",
    xeber="<code>n_live_tup</code> təxmini rəqəmdir: PostgreSQL onu fon prosesi (autovacuum/analyze) yeniləyir. Dəqiq say lazımdırsa <code>count(*)</code> işlədin.",
)

S[3] = dict(
    qrup="A", basliq="Bir cədvəlin sütunları",
    ne="information_schema.columns cədvəlindən <code>kadrlar.emekdaslar</code>-ın bütün sütunlarını, tiplərini və məcburilik statusunu çıxarır.",
    gosterir="18 sütunu sıra ilə: id (bigint, MƏCBURİ), ad (text, MƏCBURİ), maas (numeric, opsional) və s.",
    olmaz="Excel hazırlayarkən hansı sütunun məcburi olduğunu bilməzdik və yükləmə zamanı xəta alardıq.",
    evez="<code>\\d kadrlar.emekdaslar</code> — psql-in qısa yolu. Eyni məlumatı daha yığcam göstərir, lakin sütun kimi emal etmək olmur.",
)

S[4] = dict(
    qrup="A", basliq="Xarici açarların xəritəsi",
    ne="pg_constraint sistem cədvəlindən bütün FOREIGN KEY əlaqələrini oxuyur: hansı cədvəlin hansı sütunu hara bağlıdır.",
    gosterir="35 xarici açardan ilk 12-ni. Məsələn: <code>doktorantlar.rehber_id &rarr; emekdaslar</code>.",
    olmaz="Yükləmə sırasını səhv seçərdik — valideyn cədvəldən əvvəl övladı doldursaq, 'foreign key violation' alardıq.",
    evez="<code>\\d+ cedvel_adi</code> və ya sxem diaqramı çəkən alətlər (DBeaver ER diagram).",
    xeber="Bu sorğu <strong>yükləmə sırasını planlaşdırmaq</strong> üçün ən vacib alətdir: əvvəl <code>merkezler</code>, sonra <code>shobeler</code>, ən sonda <code>emekdaslar</code>.",
)

S[5] = dict(
    qrup="A", basliq="Görünüşlər (view)",
    ne="Bazada təyin olunmuş 8 view-ın siyahısını çıxarır.",
    gosterir="audit.v_son_audit, elm.v_doktorant_sayi, kadrlar.v_emekdas_tam, maliyye.v_budce_istifadesi və s.",
    olmaz="Hazır JOIN-lardan xəbərsiz olardıq və hər dəfə eyni mürəkkəb birləşməni əl ilə yazardıq.",
    evez="<code>\\dv *.*</code>. Amma view-ın hansı sxemdə olduğunu süzgəcdən keçirmək üçün SQL daha çevikdir.",
)

S[6] = dict(
    qrup="A", basliq="Funksiyalar və triggerlər",
    ne="pg_proc sistem cədvəlindən bütün funksiyaları çıxarır və qaytardığı tipə görə ayırır: <code>trigger</code> ya adi funksiya.",
    gosterir="10 funksiyanı: 2-si trigger (fn_audit_yaz, fn_gun_sayi_hesabla), 8-i çağırıla bilən.",
    olmaz="Bazada artıq hazır hesablama məntiqi olduğunu bilməzdik və həmin məntiqi tətbiqetmə kodunda təkrar yazardıq.",
    evez="<code>\\df *.*</code> — siyahını verir, lakin tip üzrə ayırmır.",
)

S[7] = dict(
    qrup="B", basliq="Bütün mərkəzlər",
    ne="struktur.merkezler cədvəlindən id, ad, ünvan və telefonu oxuyur.",
    gosterir="10 mərkəzi sıra ilə. Bunlar ARTİ-nin təşkilati vahidləridir: Elmi katiblik, Tədqiqat mərkəzi, Kurikulum mərkəzi və s.",
    olmaz="Mərkəzlərin id-lərini bilməzdik — sonrakı sorğularda <code>merkez_id = 2</code> yazmaq üçün onları tanımalıyıq.",
    evez="<code>SELECT *</code> — bütün sütunları gətirir. Lakin lazımsız sütunlar şəbəkə trafiki və yaddaş artırır.",
    xeber="<strong>Qayda:</strong> həmişə lazım olan sütunları sadalayın. <code>SELECT *</code> yalnız kəşf mərhələsində işlədin.",
)

S[8] = dict(
    qrup="B", basliq="Əməkdaşların adı, soyadı, maaşı",
    ne="kadrlar.emekdaslar cədvəlindən yalnız üç sütunu oxuyur və id-yə görə sıralayır.",
    gosterir="İlk 3 əməkdaşı. Sıralama olmasa nəticə qarışıq gələr.",
    olmaz="Nəticə sırası zəmanətli olmazdı — PostgreSQL cədvəli necə oxuyursa, o sıra ilə qaytarır.",
    evez="<code>ORDER BY soyad</code> — əlifba sırası ilə. Hesabat üçün daha oxunaqlıdır.",
    xeber="<strong>ORDER BY olmayan LIMIT təhlükəlidir:</strong> hər icrada fərqli 3 sətir gələ bilər.",
)

S[9] = dict(
    qrup="B", basliq="Maaşa görə sıralama (azalan)",
    ne="Əməkdaşları maaşa görə böyükdən kiçiyə sıralayır və ilk 5-ni göstərir.",
    gosterir="Ən yüksək maaşlı əməkdaşları: Əliyev Elnur 3500, Talıbov Tariyel 3000, sonra 2800-lər.",
    olmaz="'Ən çox maaş alan kimdir?' sualına cavab verə bilməzdik.",
    evez="<code>ORDER BY maas DESC NULLS LAST</code> — NULL-ları sona atır. Əks halda PostgreSQL NULL-ları DESC-də birinci göstərir.",
    xeber="PostgreSQL-də NULL 'ən böyük' sayılır: <code>DESC</code> ilə birinci gəlir. Bunun qarşısını <code>NULLS LAST</code> alır.",
)

S[10] = dict(
    qrup="B", basliq="İlk 5 mərkəz (LIMIT)",
    ne="LIMIT 5 ilə yalnız ilk 5 sətri qaytarır.",
    gosterir="Böyük cədvəllərdə nəticəni kiçiltməyin ən sadə yolunu.",
    olmaz="48 cədvəlli bazada milyon sətir gələ bilərdi və terminal donardı.",
    evez="<code>FETCH FIRST 5 ROWS ONLY</code> — SQL standart sintaksisi. <code>LIMIT</code> PostgreSQL/Mysql-ə xasdır.",
)

S[11] = dict(
    qrup="B", basliq="NULL olan sətirlər",
    ne="telefon sütunu boş olan şöbələrin sayını hesablayır.",
    gosterir="36 şöbənin hamısında telefon NULL-dur — şöbə səviyyəsində telefon saxlanılmır, mərkəzin telefonu işlədilir.",
    olmaz="Məlumatın nə qədər natamam olduğunu bilməzdik; hesabatda boş sütunlar səbəbini izah edə bilməzdik.",
    evez="<code>WHERE telefon IS NULL OR telefon = ''</code> — boş sətri ('') də tutur. Sütunda həm NULL, həm '' ola bilər.",
    xeber="<strong>NULL != '' </strong>. <code>NULL</code> 'bilinmir' deməkdir; <code>''</code> 'boş mətn'. SQL-də <code>telefon = NULL</code> heç vaxt doğru deyil — <code>IS NULL</code> işlədin!",
)

S[12] = dict(
    qrup="B", basliq="Təkrarsız dəyərlər (DISTINCT)",
    ne="logistika.aktivler cədvəlindəki aktiv tiplərindən təkrarsızlarını çıxarır.",
    gosterir="4 tip: avadanlıq, kompyuter, mebel, neqliyyat. Bunlar kateqoriya siyahısıdır.",
    olmaz="Hansı kateqoriyaların mövcud olduğunu bilməzdik — süzgəc (filter) düymələri düzəldə bilməzdik.",
    evez="<code>GROUP BY tip</code> — eyni nəticə, üstəlik say da verə bilər: <code>GROUP BY tip</code> + <code>count(*)</code>.",
)

S[13] = dict(
    qrup="C", basliq="Bərabərlik filtri (WHERE)",
    ne="Yalnız <code>seviyye = 1</code> olan vəzifələri seçir.",
    gosterir="Təşkilatda ən yüksək pillənin — Direktorun — 1-ci səviyyədə olduğunu.",
    olmaz="Bütün 12 vəzifə gələrdi və təşkilati iyerarxiyanı görməzdik.",
    evez="<code>WHERE seviyye &lt;= 2</code> — rəhbər pillələri birlikdə göstərir.",
)

S[14] = dict(
    qrup="C", basliq="Müqayisə filtri (maaş &gt; 2000)",
    ne="Maaşı 2000-dən çox olan əməkdaşları seçir və azalan sıralayır.",
    gosterir="10 əməkdaşın 2000-dən yuxarı maaş aldığını; ən aşağısı 2200.",
    olmaz="'Yüksək maaşlılar kimlərdir?' sualı cavabsız qalardı.",
    evez="<code>WHERE maas &gt;= 2000</code> — bərabərliyi də daxil edir. <code>&gt;</code> və <code>&gt;=</code> fərqini unutmaq ən çox edilən xətadır.",
    xeber="<strong>Numerik müqayisə:</strong> <code>maas</code> sütunu <code>numeric</code> tipindədir, ona görə <code>'2000'</code> yazsaq da işləyir. Amma <code>text</code> sütunda <code>'9' &gt; '10'</code> doğru olardı — çünki mətn müqayisəsi simvol-simvoldur.",
)

S[15] = dict(
    qrup="C", basliq="BETWEEN — tarix aralığı",
    ne="2026-cı ildə başlayan təlim qruplarını seçir.",
    gosterir="5 qrupu başlama tarixi ilə: Sertifikasiya Qrup A (mart), Kurikulum Qrup 1 (may), İnklüziv Qrup 1 (sentyabr).",
    olmaz="İl üzrə hesabat çıxara bilməzdik — bütün qruplar qarışıq gələrdi.",
    evez="<code>WHERE baslama_tarixi &gt;= DATE '2026-01-01' AND baslama_tarixi &lt; DATE '2027-01-01'</code> — BETWEEN-dən daha dəqiqdir, çünki <code>BETWEEN</code> hər iki ucu daxil edir.",
    xeber="<strong>Tarix literalı:</strong> <code>DATE '2026-01-01'</code> yazılışı PostgreSQL-ə tipi dəqiq bildirir. Sadəcə <code>'2026-01-01'</code> yazsaq, sütun tipindən asılı olaraq şərh dəyişə bilər.",
)

S[16] = dict(
    qrup="C", basliq="IN — siyahıdan biri",
    ne="Statusu verilmiş siyahıya daxil olan satınalmaları seçir.",
    gosterir="Tamamlanmış və müqavilə mərhələsində olan 5 satınalmanı.",
    olmaz="<code>WHERE status='a' OR status='b'</code> yazmalı olardıq — siyahı böyüdükcə kod da böyüyür.",
    evez="<code>WHERE status = ANY(ARRAY['tamamlandi','muqavile'])</code> — eyni məna, massiv sintaksisi ilə.",
)

S[17] = dict(
    qrup="C", basliq="LIKE — mətn axtarışı",
    ne="E-poçt ünvanı <code>arti.edu.az</code> ilə bitən mərkəzləri tapır.",
    gosterir="5 mərkəzi və onların rəsmi e-poçtlarını. <code>%</code> istənilən sayda simvolu bildirir.",
    olmaz="Minlərlə sətirdə mətn axtara bilməzdik.",
    evez="<code>ILIKE</code> — böyük/kiçik hərf fərqini nəzərə almır. <code>LIKE</code> hərfə həssasdır: <code>'ARTI%'</code> və <code>'arti%'</code> fərqli nəticə verir.",
    xeber="<strong>Performans:</strong> <code>LIKE '%...%</code> (başda <code>%</code>) indeksi işlədə bilmir — tam cədvəl skanı olur. Böyük cədvəllərdə <code>ILIKE</code> yerinə <code>tsvector</code> tam mətn axtarışı qurun.",
)

S[18] = dict(
    qrup="C", basliq="AND / OR / NOT — mürəkkəb şərt",
    ne="Həm <code>status = 'davam edir'</code>, həm də bitmə tarixi gələcəkdə olan layihələri seçir.",
    gosterir="5 aktiv layihəni. Bu, 'hazırda işlənən layihələr' hesabatıdır.",
    olmaz="Bitmiş layihələr də siyahıya düşərdi və hesabat yanlış olardı.",
    evez="<code>WHERE status = 'davam edir' AND bitme_tarixi &gt; now()</code> — <code>CURRENT_DATE</code> yalnız günü, <code>now()</code> tarix+saatı verir.",
    xeber="<strong>Mötərizə qaydası:</strong> <code>AND</code> <code>OR</code>-dan güclüdür. <code>a AND b OR c</code> = <code>(a AND b) OR c</code>. Qarışıq şərtlərdə həmişə mötərizə yazın.",
)

S[19] = dict(
    qrup="D", basliq="COUNT — sətir sayı",
    ne="Əməkdaşların ümumi sayını hesablayır.",
    gosterir="14 əməkdaş. <code>count(*)</code> bütün sətirləri, <code>count(sutun)</code> isə yalnız NULL olmayanları sayır.",
    olmaz="'Neçə işçimiz var?' sualına cavab verə bilməzdik.",
    evez="<code>count(id)</code> — <code>id</code> heç vaxt NULL olmadığı üçün eyni nəticəni verir və bir qədər sürətlidir.",
)

S[20] = dict(
    qrup="D", basliq="SUM / AVG / MIN / MAX",
    ne="Bir sorğuda beş aqreqat hesablayır: say, orta, minimum, maksimum və cəm maaş.",
    gosterir="14 əməkdaş, orta maaş 2357.14, ən aşağı 1100, ən yüksək 3500, ümumi fond 33 000 AZN.",
    olmaz="Beş ayrı sorğu yazmalı olardıq — hər biri cədvəli yenidən skan edərdi.",
    evez="<code>round(avg(maas), 2)</code> — <code>avg</code> çox rəqəmli nəticə verir. <code>round</code> onu oxunaqlı edir.",
    xeber="<strong>AVG və NULL:</strong> <code>avg</code> NULL-ları saymır. 14 sətirdən 4-ü NULL olsa, orta 10 sətir üzrə hesablanar — bu, gözlənilməz nəticə verə bilər. Lazımsa <code>COALESCE(maas,0)</code> işlədin.",
)

S[21] = dict(
    qrup="D", basliq="GROUP BY — mərkəz üzrə bölgü",
    ne="Əməkdaşları mərkəzə görə qruplaşdırır və hər qrupda say və orta maaşı hesablayır.",
    gosterir="10 mərkəzdən 9-da əməkdaş var. Funksional şöbələr 3 nəfərlə birinci, orta maaş 1466.67.",
    olmaz="Hər mərkəz üçün ayrı sorğu yazmalı olardıq.",
    evez="<code>GROUP BY merkez_id</code> yerinə <code>GROUP BY m.ad</code> — ad daha oxunaqlıdır, lakin iki fərqli mərkəzin adı eyni olsa, səhvən birləşər.",
    xeber="<strong>Qayda:</strong> <code>SELECT</code>-də olan hər sütun ya <code>GROUP BY</code>-da olmalı, ya da aqreqat funksiyası içində. Əks halda PostgreSQL xəta verir.",
)

S[22] = dict(
    qrup="D", basliq="HAVING — qrup süzgəci",
    ne="Qruplaşdırmadan SONRA süzgəc tətbiq edir: yalnız 1-dən çox aktivı olan tipləri saxlayır.",
    gosterir="3 tipi (kompyuter 2, avadanlıq 5, mebel 2) və onların ümumi dəyərini. 'neqliyyat' 1 ədəd olduğu üçün düşür.",
    olmaz="<code>WHERE count(*) &gt; 1</code> yazsaq xəta alardıq — aqreqat funksiyası <code>WHERE</code>-də işləmir.",
    evez="<code>WHERE</code> sətir süzür, <code>HAVING</code> qrup süzür. İkisi bir sorğuda birlikdə işlədilə bilər.",
    xeber="<strong>İcra sırası:</strong> <code>FROM &rarr; WHERE &rarr; GROUP BY &rarr; HAVING &rarr; SELECT &rarr; ORDER BY &rarr; LIMIT</code>. Bu sıra yadda saxlanmalıdır — <code>SELECT</code>-dəki ləqəb <code>WHERE</code>-də işləmir, çünki hələ hesablanmayıb.",
)

S[23] = dict(
    qrup="D", basliq="COUNT + FILTER — şərti say",
    ne="Hər aktiv tipində vəziyyəti 'yaxşı' olanların və qeyri-saz olanların sayını ayrı-ayrı sütunlarda hesablayır.",
    gosterir="5 avadanlığın 3-ü saz, 2-si qeyri-sazdır. Kompyuterlərin hamısı sazdır.",
    olmaz="Hər vəziyyət üçün ayrı sorğu yazmalı, sonra nəticələri əl ilə birləşdirməli olardıq.",
    evez="<code>count(CASE WHEN veziyyet='yaxşı' THEN 1 END)</code> — <code>FILTER</code> olmadan eyni nəticə, lakin uzundur. <code>FILTER</code> SQL:2003 standartıdır.",
)

S[24] = dict(
    qrup="D", basliq="ROLLUP — avtomatik yekun sətri",
    ne="İl üzrə bölgüyə əlavə olaraq ümumi yekun sətrini avtomatik əlavə edir.",
    gosterir="2024-2027 illəri üzrə büdcə və ən altda CƏMİ: 18 805 000 AZN. Yekun sətri əl ilə yazılmır.",
    olmaz="Yekunu ayrı sorğu ilə hesablayıb iki nəticəni birləşdirməli olardıq.",
    evez="<code>GROUP BY CUBE(il)</code> — bütün mümkün kombinasiyaları verir. <code>GROUPING SETS</code> isə hansı yekunların lazım olduğunu dəqiq göstərir.",
    xeber="<strong>COALESCE(-in rolu):</strong> yekun sətrində <code>il</code> NULL olur. <code>COALESCE(il::text,'CƏMİ')</code> onu oxunaqlı mətnə çevirir.",
)

S[25] = dict(
    qrup="E", basliq="INNER JOIN — şöbə + mərkəz",
    ne="İki cədvəli xarici açar üzərindən birləşdirir: hər şöbəyə onun mərkəzini qoşur.",
    gosterir="Elmi-pedaqoji tədqiqatlar mərkəzinin 6 şöbəsini (Elmi kitabxana, Psixologiya şöbəsi və s.).",
    olmaz="Yalnız <code>merkez_id = 2</code> rəqəmini görərdik — hansı mərkəz olduğunu bilməzdik.",
    evez="<code>LEFT JOIN</code> — şöbəsi olmayan mərkəzləri də göstərir. <code>INNER JOIN</code> yalnız uyğunluğu olanları qaytarır.",
)

S[26] = dict(
    qrup="E", basliq="LEFT JOIN — boş tərəf də görünür",
    ne="Bütün mərkəzləri göstərir və hər birinə şöbə sayını yazır. Şöbəsi olmayan mərkəz də siyahıda qalır.",
    gosterir="Funksional şöbələr 8 şöbə ilə birinci; Tədris resursları mərkəzi 0 ilə sonuncu.",
    olmaz="Şöbəsi olmayan mərkəzlər siyahıdan tamamilə yox olardı və 'niyə görünmür?' sualı yaranardı.",
    evez="<code>RIGHT JOIN</code> — eyni nəticəni tərsinə yazmaqla verir, lakin oxunaqlığı azaldır. <code>FULL OUTER JOIN</code> hər iki tərəfi tam göstərir.",
    xeber="<strong>LEFT JOIN + count():</strong> <code>count(*)</code> boş tərəf üçün 1 qaytarır (səhv!), <code>count(s.id)</code> isə 0 qaytarır (doğru). Səbəb: <code>count(*)</code> NULL sətri də sayır.",
)

S[27] = dict(
    qrup="E", basliq="Üç cədvəlin birləşməsi",
    ne="Əməkdaş + vəzifə + mərkəz cədvəllərini birləşdirir.",
    gosterir="Əməkdaşın tam vəzifəsini və hansı mərkəzdə işlədiyini bir sətirdə.",
    olmaz="Üç ayrı sorğu icra edib nəticələri əl ilə uyğunlaşdırmalı olardıq.",
    evez="Hazır view işlətmək: <code>kadrlar.v_emekdas_tam</code> bu birləşməni artıq edir (36-cı sorğu).",
)

S[28] = dict(
    qrup="E", basliq="Beş cədvəlin birləşməsi (tam profil)",
    ne="Əməkdaş + vəzifə + şöbə + mərkəz + cinsiyyət cədvəllərini bir sorğuda birləşdirir.",
    gosterir="Hər əməkdaş üçün tam təşkilati mənzərə: vəzifə, şöbə, mərkəz, cins.",
    olmaz="İnsan resursları hesabatı üçün əl ilə cədvəl birləşdirməli olardıq — Excel-də VLOOKUP cəhənnəmi.",
    evez="<code>JOIN</code> yerinə <code>LEFT JOIN</code> — şöbəsi təyin olunmamış əməkdaş da siyahıda qalsın. Bu, məlumat tamlığını yoxlamaq üçün vacibdir.",
    xeber="<strong>Performans:</strong> 5 cədvəlin birləşməsi ağırdır. Tez-tez lazımdırsa <code>MATERIALIZED VIEW</code> yaradın — nəticə diskdə saxlanar və sorğu sürətlənər.",
)

S[29] = dict(
    qrup="E", basliq="Layihə + istiqamət + rəhbər",
    ne="Elmi layihələri istiqaməti və rəhbəri ilə birlikdə göstərir.",
    gosterir="Hansı layihənin hansı sahədə olduğunu və kimin rəhbərlik etdiyini.",
    olmaz="Layihə hesabatında yalnız <code>istiqamet_id = 3</code> görünərdi.",
    evez="<code>elm.v_tedqiqat_layiheleri</code> view-ı — bu birləşmə artıq hazırdır.",
)

S[30] = dict(
    qrup="E", basliq="LEFT JOIN + IS NULL — yetim sətirlər",
    ne="Şöbəsi olmayan mərkəzləri tapır: LEFT JOIN edir və uyğunluğu olmayanları süzür.",
    gosterir="Boş nəticə — bütün 10 mərkəzin şöbəsi var. Bu, məlumat tamlığının yoxlamasıdır.",
    olmaz="Təşkilatda 'boş' mərkəzin olub-olmadığını bilməzdik.",
    evez="<code>NOT EXISTS (SELECT 1 FROM shobeler WHERE merkez_id = m.id)</code> — çox vaxt daha sürətlidir, xüsusən böyük cədvəllərdə.",
    xeber="<strong>Anti-join nümunəsi:</strong> bu texnika 'A var, amma B yoxdur' tipindəki bütün sualları cavablandırır — məsələn, 'heç bir təlim keçməmiş müəllimlər'.",
)

S[31] = dict(
    qrup="E", basliq="Ad → id xəritəsi (yükləmə üçün tipik)",
    ne="Hər təlim proqramı üzrə qrup sayını hesablayır.",
    gosterir="Hansı proqramın daha çox qrupu olduğunu.",
    olmaz="Excel-dən yükləmə zamanı yalnız proqram ADINI bilirik, bazada isə ID lazımdır. Bu sorğu həmin xəritəni qurur.",
    evez="<code>LEFT JOIN</code> əvəzinə <code>INNER JOIN</code> — heç qrupu olmayan proqram siyahıdan düşər.",
)

S[32] = dict(
    qrup="F", basliq="WHERE ... IN (alt sorğu)",
    ne="Alt sorğu ilə 'təhsil' sözü keçən mərkəzlərin id-lərini tapır, sonra həmin mərkəzlərin əməkdaşlarını seçir.",
    gosterir="Alt sorğunun nəticəsini əl ilə yazmaq lazım olmadığını — SQL bunu özü edir.",
    olmaz="Əvvəlcə mərkəz id-lərini tapıb, sonra onları sorğuya əl ilə yazmalı olardıq. Məlumat dəyişdikcə kod köhnələr.",
    evez="<code>JOIN</code> — çox vaxt optimallaşdırıcı onu daha sürətli icra edir. <code>IN</code> alt sorğusunu isə hər sətir üçün yenidən hesablaya bilər.",
)

S[33] = dict(
    qrup="F", basliq="EXISTS — korrelyasiyalı alt sorğu",
    ne="Şöbəsi olan mərkəzləri seçir. Alt sorğu xarici sorğunun hər sətri ilə əlaqəlidir.",
    gosterir="<code>EXISTS</code> yalnız 'heç olmasa bir sətir varmı?' sualına cavab verdiyi üçün say hesablamır — sürətlidir.",
    olmaz="<code>count() &gt; 0</code> ilə eyni nəticəni alasıq da, bütün sətirlər sayılardı.",
    evez="<code>IN</code> — oxunaqlıdır, lakin alt sorğu NULL qaytarırsa gözlənilməz davranır: <code>x IN (NULL)</code> heç vaxt doğru deyil.",
    xeber="<strong>EXISTS erkən dayanır:</strong> ilk uyğunluğu tapanda axtarışı dayandırır. <code>IN</code> isə bütün alt sorğunu tam icra edir.",
)

S[34] = dict(
    qrup="F", basliq="Skalyar alt sorğu — ortadan yuxarı",
    ne="Bir dəyər qaytaran alt sorğu ilə orta maaşı hesablayır və ondan yuxarı maaş alanları seçir.",
    gosterir="Orta maaşdan (2357.14) yuxarı olan 7 əməkdaşı.",
    olmaz="Ortanı əvvəlcə ayrı sorğu ilə tapıb, sonra rəqəmi əl ilə yazmalı olardıq — məlumat dəyişdikcə köhnələr.",
    evez="Pəncərə funksiyası: <code>WHERE maas &gt; avg(maas) OVER ()</code> — eyni nəticə, lakin cədvəl bir dəfə skan olunur.",
    xeber="<strong>Skalyar alt sorğu bir dəyər qaytarmalıdır.</strong> İki sətir qaytarsa 'more than one row returned by a subquery' xətası alınar.",
)

S[35] = dict(
    qrup="F", basliq="FROM (alt sorğu) — törəmə cədvəl",
    ne="Alt sorğunu müvəqqəti cədvəl kimi işlədib onun üzərində süzgəc tətbiq edir.",
    gosterir="Orta maaşı 1800-dən yuxarı olan mərkəzləri.",
    olmaz="<code>WHERE avg(maas) &gt; 1800</code> birbaşa yazıla bilməz — aqreqat funksiyası <code>WHERE</code>-də işləmir. Yəni bu texnika olmasa HAVING ilə məhdudlaşardıq.",
    evez="<code>WITH</code> (CTE) — eyni məntiqi daha oxunaqlı yazır və eyni alt sorğunu bir neçə yerdə işlətməyə imkan verir (40-cı sorğu).",
    xeber="<strong>Ləqəb məcburidir:</strong> <code>) x</code> hissəsindəki <code>x</code> olmasa PostgreSQL xəta verir — hər törəmə cədvəlin adı olmalıdır.",
)

S[36] = dict(
    qrup="G", basliq="View-dan sorğu",
    ne="Hazır <code>kadrlar.v_emekdas_tam</code> görünüşündən oxuyur. Bu view 5 cədvəli artıq birləşdirib.",
    gosterir="Əməkdaşın tam adını, vəzifəsini, şöbəsini, mərkəzini və maaşını — mürəkkəb JOIN yazmadan.",
    olmaz="Hər dəfə 5 cədvəlli JOIN yazmalı olardıq; biri səhv yazsa nəticə yanlış olardı.",
    evez="<code>MATERIALIZED VIEW</code> — nəticəni diskdə saxlayır, sorğu çox sürətlənir. Lakin məlumat avtomatik yenilənmir: <code>REFRESH MATERIALIZED VIEW</code> lazımdır.",
    xeber="<strong>View nədir:</strong> saxlanılmış SELECT. Yer tutmur, hər sorğuda yenidən hesablanır. 'Virtual cədvəl' də demək olar.",
)

S[37] = dict(
    qrup="G", basliq="Funksiya çağırışı",
    ne="Bazada təyin olunmuş üç funksiyanı birbaşa çağırır: maaş fondu, mərkəzin şöbə sayı, qrupun iştirakçı sayı.",
    gosterir="Aylıq fond 33 000 AZN; 2-ci mərkəzin 7 şöbəsi; 1-ci qrupun 3 iştirakçısı.",
    olmaz="Bu hesablamaları hər tətbiqdə (frontend, mobil, hesabat) təkrar yazmalı olardıq — biri dəyişsə, hamısını yeniləmək lazım gələrdi.",
    evez="View ilə də mümkündür, lakin funksiya PARAMETR qəbul edir (<code>fn_shobe_sayi(2)</code>), view isə bütün cədvəli verir.",
    xeber="<strong>Funksiya nə vaxt:</strong> parametrli hesablama, tətbiq məntiqi, trigger. <strong>View nə vaxt:</strong> təkrarlanan mürəkkəb JOIN.",
)

S[38] = dict(
    qrup="G", basliq="View + filtr + sıralama",
    ne="View-ı adi cədvəl kimi işlədir: süzgəc tətbiq edir və sıralayır.",
    gosterir="İştirakçısı olan qrupları çoxdan aza sıralayır.",
    olmaz="View-ın gücünü tam işlədə bilməzdik — sadəcə bütün sətirləri göstərməklə kifayətlənərdik.",
    evez="View üzərində <code>GROUP BY</code>, <code>JOIN</code>, alt sorğu — hamısı mümkündür. View adi cədvəl kimidir.",
    xeber="<strong>Diqqət:</strong> view üzərində <code>WHERE</code> tətbiq etmək view-ın daxilindəki məntiqi dəyişmir. Məsələn qruplaşdırılmış view-da filtr qruplaşdırmadan SONRA işləyir.",
)

S[39] = dict(
    qrup="H", basliq="ROW_NUMBER — qrup daxilində sıra",
    ne="Hər mərkəz daxilində əməkdaşları maaşa görə nömrələyir.",
    gosterir="Hər mərkəzin '1 nömrəli' ən yüksək maaşlı əməkdaşını ayırd etmək imkanı.",
    olmaz="'Hər mərkəzin ən çox maaş alanı kimdir?' sualına tək sorğu ilə cavab verə bilməzdik.",
    evez="<code>RANK()</code> — bərabər maaşlara eyni nömrə verir, sonra atlayır (1,1,3). <code>DENSE_RANK()</code> atlamır (1,1,2). <code>ROW_NUMBER()</code> həmişə fərqli nömrə verir (1,2,3).",
    xeber="<strong>Pəncərə funksiyası nədir:</strong> <code>OVER (...)</code> ilə yazılan və sətirləri QRUPLAŞDIRMADAN hesablayan funksiya. <code>GROUP BY</code>-dan fərqi: sətir sayı azalmır.",
)

S[40] = dict(
    qrup="H", basliq="CTE (WITH) — mərhələli analitika",
    ne="Əvvəlcə mərkəz üzrə cəm hesablayır (CTE), sonra həmin nəticə üzərində faiz payını çıxarır.",
    gosterir="Hər mərkəzin ümumi maaş fondunun neçə faizini təşkil etdiyini.",
    olmaz="İkiqat alt sorğu yazmalı olardıq — oxunaqlığı çox aşağı düşərdi.",
    evez="Müvəqqəti cədvəl (<code>CREATE TEMP TABLE</code>) — eyni məntiq, lakin diskdə yer tutur və sessiya bitəndə silinir.",
    xeber="<strong>CTE-nin üstünlüyü:</strong> sorğu yuxarıdan aşağı oxunur — əvvəl 'nə hesablayırıq', sonra 'nə edirik'. Mürəkkəb analitikada bu, kodun oxunaqlığını ikiqat artırır.",
)

# ══════════════════════════════════════════════════════════════
#  MƏNBƏLƏRİ OXU
# ══════════════════════════════════════════════════════════════
sql_metn = (SQL / "10_sorgular.sql").read_text(encoding="utf-8")
hisseler = re.split(r"\\echo '── (\d+)\. ([^']*)'", sql_metn)
sorgular = {}
for i in range(1, len(hisseler), 3):
    no = int(hisseler[i]); basliq = hisseler[i + 1]; govde = hisseler[i + 2]
    govde = re.sub(r"\\echo '═══[^']*'", "", govde).strip()
    sorgular[no] = (basliq, govde)

cixis_metn = CIXIS.read_text(encoding="utf-8") if CIXIS.exists() else ""
chisseler = re.split(r"^── (\d+)\. ", cixis_metn, flags=re.M)
cixisler = {}
for i in range(1, len(chisseler), 2):
    no = int(chisseler[i])
    govde = chisseler[i + 1]
    # növbəti qrup başlığını və \echo sətrini təmizlə
    govde = re.split(r"^═══ ", govde, flags=re.M)[0]
    govde = re.sub(r"^[^\n]*\n", "", govde, count=1)   # başlıq sətri
    cixisler[no] = govde.strip("\n")

QRUP_ADLARI = {
    "A": ("A", "Bazanı tanımaq", "Sxem, cədvəl, sütun, açar, view və funksiyaları kəşf etmək."),
    "B": ("B", "Sadə seçim", "SELECT, sıralama, limit, NULL yoxlaması, DISTINCT."),
    "C": ("C", "Filtrləmə", "WHERE, müqayisə, BETWEEN, IN, LIKE, məntiqi operatorlar."),
    "D": ("D", "Aqreqasiya", "COUNT, SUM, AVG, GROUP BY, HAVING, FILTER, ROLLUP."),
    "E": ("E", "Birləşmə (JOIN)", "INNER, LEFT, çoxcədvətli birləşmələr, anti-join."),
    "F": ("F", "Alt sorğular", "IN, EXISTS, skalyar alt sorğu, törəmə cədvəl."),
    "G": ("G", "View və funksiya", "Hazır görünüşlər və bazadaxili funksiyalar."),
    "H": ("H", "Pəncərə və CTE", "ROW_NUMBER, OVER (PARTITION BY), WITH."),
}

# ══════════════════════════════════════════════════════════════
#  HTML QURULMASI
# ══════════════════════════════════════════════════════════════
H = []
A = H.append

A('<!DOCTYPE html>')
A('<html lang="az">')
A('<head>')
A('<meta charset="UTF-8">')
A('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
A('<title>Deepseek Baza — ARTİ ERP bazası: 40 vacib sorğu</title>')
A('<style>')
A(css)
A('</style>')
A('</head>')
A('<body>')
A('<div class="container">')
A('<header>')
A('  <div class="lesson-badge">DS_Baza · Hissə 1/1</div>')
A('  <h1>Deepseek Baza — hazır bazanın bütün imkanları</h1>')
A('  <p class="subtitle">Bazaya sıfırdan qoşulmaq, 12 sxemi tanımaq və 40 vacib sorğu</p>')
A('  <p class="meta">Layihə: <strong>Deepseek_ARTI</strong> · Baza: <code>arti_baza</code> · '
  'PostgreSQL 18 · 12 sxem · 48 cədvəl · 8 view · 10 funksiya · 5 trigger · 35 xarici açar</p>')
A('</header>')

# ── TOC ──
A('<div class="toc">')
A('  <h3>📚 Bu dərsdə nələr öyrənəcəksiniz</h3>')
A('  <ol>')
A('    <li><a href="#b1">Baza nədir və bu dərs nə verir</a></li>')
A('    <li><a href="#b2">Layihə strukturu — Deepseek_ARTI</a></li>')
A('    <li><a href="#b3">Bazaya qoşulmaq — sıfırdan</a></li>')
A('    <li><a href="#b4">Bazanın xəritəsi — 12 sxem</a></li>')
A('    <li><a href="#b5">Bazanın imkanları — nə var, nə yox</a></li>')
A('    <li><a href="#b6">40 vacib sorğu</a></li>')
A('    <li><a href="#b7">Yoxlama siyahısı</a></li>')
A('    <li><a href="#b8">Növbəti dərs</a></li>')
A('  </ol>')
A('</div>')

# ── BÖLMƏ 1 ──
A('<h2 id="b1">1. Baza nədir və bu dərs nə verir</h2>')
A(blok("block-ne", "NƏ EDƏCƏYİK",
       "<p>Bu dərsdə <strong>heç bir kod yazmadan</strong> mövcud bazanı gəzəcəyik. "
       "Əvvəlcə bazaya qoşulacağıq, sonra 12 sxemi tanıyacaq, sonda "
       "<strong>40 vacib sorğu</strong> ilə bazanın bütün imkanlarını nümayiş etdirəcəyik.</p>"))
A(blok("block-niye", "NİYƏ LAZIMDIR",
       "<p>Baza layihənin <strong>ürəyidir</strong>. Backend, frontend və AI qatı — hamısı "
       "bu bazadan oxuyur. Bazanı tanımayan proqramçı səhv sorğu yazır, yavaş işləyən "
       "sistem qurur və məlumatı düzgün göstərə bilmir.</p>"
       "<p>Bu dərs bitəndə siz bazanın <em>hər küncünü</em> biləcəksiniz.</p>"))
A(blok("block-hara", "HARA",
       "<p>Baza: <code>arti_baza</code> · İstifadəçi: <code>arti_user</code> · Port: <code>5432</code></p>"))
A(blok("block-izah", "İZAH — bu baza hardan gəldi?",
       "<p>Baza əvvəlki <strong>ARTİ ERP-1</strong> layihəsində qurulmuş və bu yeni "
       "<strong>Deepseek_ARTI</strong> layihəsinə <em>olduğu kimi</em> götürülmüşdür. "
       "Struktur dəyişməyib, məlumat isə 2024-2028 illərinə köçürülmüşdür.</p>"))
A('<div class="success-box">Bu dərsin sonunda siz 40 sorğunu müstəqil yaza və '
  'izah edə biləcəksiniz.</div>')

# ── BÖLMƏ 2 ──
A('<h2 id="b2">2. Layihə strukturu — Deepseek_ARTI</h2>')
A(blok("block-ne", "NƏ EDƏCƏYİK",
       "<p>Layihənin 4 blokunu və dərslər qovluğunu tanıyacağıq.</p>"))
A('<pre data-lang="bash"><code>'
  '~/Deepseek_ARTI/\n'
  '├── DS_Baza/          ← baza bloku  (SQL, sxem, sorğular)\n'
  '│   └── sql/\n'
  '│       ├── 00_TAM_DDL.sql        bütün strukturu yenidən qurur\n'
  '│       ├── 10_sorgular.sql       40 vacib sorğu\n'
  '│       └── ...\n'
  '├── DS_Backend/       ← NestJS + Prisma\n'
  '├── DS_Frontend/      ← Next.js + React\n'
  '├── DS_Web/           ← ARTI_web (yenidən yazılacaq)\n'
  '├── DƏRSLƏR/          ← bütün HTML dərslər\n'
  '│   └── Deepseek_Baza.html        ← bu dərs\n'
  '├── _arxiV/           ← ehtiyat nüsxələr\n'
  '└── _hesabat/         ← hesabatlar\n'
  '</code></pre>')
A(blok("block-ipucu", "💡 NİYƏ 4 AYRI BLOK?",
       "<table><tr><th>Blok</th><th>Nə edir</th><th>Texnologiya</th></tr>"
       "<tr><td><code>DS_Baza</code></td><td>Məlumatı saxlayır</td><td>PostgreSQL 18</td></tr>"
       "<tr><td><code>DS_Backend</code></td><td>Məlumatı API kimi verir</td><td>NestJS + Prisma</td></tr>"
       "<tr><td><code>DS_Frontend</code></td><td>İstifadəçi interfeysi</td><td>Next.js + React</td></tr>"
       "<tr><td><code>DS_Web</code></td><td>Xarici veb təqdimat</td><td>yenidən yazılır</td></tr></table>"
       "<p>Hər blok <strong>müstəqil</strong> yenilənə və genişlənə bilər.</p>"))

# ── BÖLMƏ 3 ──
A('<h2 id="b3">3. Bazaya qoşulmaq — sıfırdan</h2>')
A(blok("block-ne", "NƏ EDƏCƏYİK",
       "<p>Bazaya üç yolla qoşulacağıq: <strong>psql</strong> (terminal), "
       "<strong>Python</strong> və <strong>Node.js</strong>. Əvvəlcə psql.</p>"))
A('<h3><span class="step-num">1</span> PostgreSQL işləyirmi?</h3>')
A('<pre data-lang="bash"><code># PostgreSQL xidməti işləyir?\n'
  'brew services list | grep postgresql\n\n'
  '# Port 5432 dinlənir?\n'
  'lsof -ti :5432\n\n'
  '# Versiya\n'
  'psql --version</code></pre>')
A(blok("block-yox", "YOXLAMA 1 — gözlənilən çıxış",
       "<pre><code>postgresql@18  started\n"
       "5432\n"
       "psql (PostgreSQL) 18.6</code></pre>"
       "<p>Əgər <code>started</code> yoxdursa: <code>brew services start postgresql@18</code></p>"))

A('<h3><span class="step-num">2</span> Mühiti təmizlə (MÜTLƏQ)</h3>')
A('<pre data-lang="bash"><code>unset DATABASE_URL PGHOST</code></pre>')
A(blok("block-xeber", "⚠️ NİYƏ BU ƏMR MÜTLƏQDİR?",
       "<p>macOS-da qlobal <code>DATABASE_URL</code> dəyişəni ola bilər (başqa layihədən). "
       "O, <code>psql</code>-i və tətbiqləri <strong>səhv bazaya</strong> yönəldir. Nəticədə "
       "<code>relation \"...\" does not exist</code> xətası alırsınız — halbuki cədvəl yerindədir.</p>"
       "<p><strong>Hər sessiyanın əvvəlində</strong> bu əmri işlədin.</p>"))

A('<h3><span class="step-num">3</span> Bazaya qoşul</h3>')
A('<pre data-lang="bash"><code>export PGPASSWORD=arti_secret_2025\n'
  'psql -U arti_user -d arti_baza</code></pre>')
A(blok("block-yox", "YOXLAMA 2 — qoşulma uğurlu?",
       "<pre><code>psql (18.6)\n"
       "Type \"help\" for help.\n\n"
       "arti_baza=&gt;</code></pre>"
       "<p>Prompt <code>arti_baza=&gt;</code> görünürsə, qoşulma uğurludur.</p>"))
A(blok("block-olmaz", "OLMASA NƏ OLAR — 'password authentication failed'",
       "<p>Şifrə səhvdir və ya <code>PGPASSWORD</code> təyin olunmayıb. "
       "Yoxlayın: <code>psql -U arti_user -d arti_baza -c 'SELECT current_user;'</code></p>"
       "<p>Alternativ — <code>~/.pgpass</code> faylı:</p>"
       "<pre><code>echo 'localhost:5432:arti_baza:arti_user:arti_secret_2025' &gt;&gt; ~/.pgpass\n"
       "chmod 600 ~/.pgpass</code></pre>"))
A(blok("block-evez", "ƏVƏZİNDƏ — qrafik alətlər",
       "<table><tr><th>Alət</th><th>Üstünlük</th></tr>"
       "<tr><td><strong>DBeaver</strong></td><td>Cədvəl ağacı, ER diaqram, nəticə ixracı</td></tr>"
       "<tr><td><strong>pgAdmin</strong></td><td>Rəsmi alət, sorğu planı vizuallaşdırması</td></tr>"
       "<tr><td><strong>TablePlus</strong></td><td>macOS üçün sürətli, gözəl interfeys</td></tr></table>"
       "<p>Lakin <code>psql</code> <strong>hər yerdə işləyir</strong> — serverdə, Docker-də, CI-da.</p>"))

A('<h3><span class="step-num">4</span> İlk sorğu</h3>')
A('<pre data-lang="sql"><code>SELECT version();\nSELECT current_database(), current_user, now();</code></pre>')
A('<pre data-lang="çıxış"><code> current_database | current_user |              now\n'
  '------------------+--------------+-------------------------------\n'
  ' arti_baza        | arti_user    | 2026-09-19 10:45:12.345678+04</code></pre>')
A(blok("block-ipucu", "💡 psql-DƏN ÇIXMAQ", "<p><code>\\q</code> — çıxış. "
       "<code>\\?</code> — bütün psql əmrləri. <code>\\h SELECT</code> — SQL köməyi.</p>"))
A('<h3><span class="step-num">5</span> Python ilə qoşulma</h3>')
A('<pre data-lang="bash"><code>pip3 install psycopg2-binary</code></pre>')
A('<pre data-lang="python"><code>import psycopg2\n\n'
  'conn = psycopg2.connect(\n'
  '    host="localhost", port=5432,\n'
  '    dbname="arti_baza", user="arti_user",\n'
  '    password="arti_secret_2025",\n'
  ')\n'
  'with conn.cursor() as cur:\n'
  '    cur.execute("SELECT count(*) FROM struktur.merkezler")\n'
  '    print("Mərkəz sayı:", cur.fetchone()[0])\n'
  'conn.close()</code></pre>')
A(blok("block-olmaz", "OLMASA NƏ OLAR — 'Do not know how to serialize a BigInt'",
       "<p>PostgreSQL <code>BIGINT</code> qaytarır, JavaScript isə onu JSON-a çevirə bilmir. "
       "<strong>Həll:</strong> SQL-də həmişə cast edin:</p>"
       "<table><tr><th>PG tipi</th><th>Problem</th><th>Cast</th></tr>"
       "<tr><td><code>BIGINT</code></td><td>JS BigInt</td><td><code>id::int</code></td></tr>"
       "<tr><td><code>NUMERIC</code></td><td>Sətir kimi gəlir</td><td><code>maas::float8</code></td></tr>"
       "<tr><td><code>COUNT(*)</code></td><td>BIGINT qaytarır</td><td><code>count(*)::int</code></td></tr>"
       "<tr><td><code>DATE</code></td><td>Obyekt kimi gəlir</td><td><code>tarix::text</code></td></tr></table>"))

# ── BÖLMƏ 4 ──
A('<h2 id="b4">4. Bazanın xəritəsi — 12 sxem</h2>')
A(blok("block-ne", "NƏ EDƏCƏYİK", "<p>Bazanın 12 sxemini və hər birinin nə üçün lazım olduğunu öyrənəcəyik.</p>"))
A('<table>')
A('  <tr><th>Sxem</th><th>Cədvəl</th><th>Nə saxlayır</th></tr>')
SXEMLER = [
    ("ortaq", 4, "Lüğətlər: cinsiyyət, elmi dərəcə, elmi ad, iş statusu"),
    ("struktur", 7, "Təşkilati quruluş: mərkəz, şöbə, vəzifə, rəhbərlik, Elmi Şura"),
    ("kadrlar", 5, "Əməkdaşlar, istifadəçilər, təyinatlar, məzuniyyətlər, iş təcrübəsi"),
    ("elm", 8, "Elmi fəaliyyət: layihə, doktorant, məqalə, nəşr, jurnal, tədbir"),
    ("tehsil", 5, "Təlim: qrup, proqram, iştirakçı, imtahan, sertifikasiya"),
    ("qiymetlendirme", 3, "Beynəlxalq qiymətləndirmə (PISA/TIMSS), monitorinq, statistika"),
    ("metodika", 2, "Metodik vəsaitlər və xidmətlər"),
    ("maliyye", 4, "Büdcə, əməliyyat, satınalma, müqavilə"),
    ("logistika", 3, "Aktivlər, binalar, IT sistemləri"),
    ("sened", 3, "Əmrlər, sənədlər, sənəd növləri"),
    ("audit", 1, "Audit jurnalı — hər dəyişikliyin izi"),
    ("ai", 3, "AI sorğuları, promptlar, embeddinglər (RAG üçün)"),
]
for sx, n, iz in SXEMLER:
    A('  <tr><td><code>%s</code></td><td>%d</td><td>%s</td></tr>' % (sx, n, iz))
A('</table>')
A(blok("block-izah", "İZAH — sxem nədir?",
       "<p>Sxem (schema) — cədvəlləri <strong>məntiqi qruplara</strong> ayıran qovluqdur. "
       "Fayl sistemindəki qovluq kimidir. <code>kadrlar.emekdaslar</code> yazılışı "
       "'<em>kadrlar</em> sxemindəki <em>emekdaslar</em> cədvəli' deməkdir.</p>"))
A(blok("block-niye", "NİYƏ SXEMLƏRƏ AYIRIRIQ?",
       "<table><tr><th>Səbəb</th><th>İzah</th></tr>"
       "<tr><td><strong>Oxunaqlıq</strong></td><td><code>kadrlar.emekdaslar</code> dərhal mənası aydın olur</td></tr>"
       "<tr><td><strong>İcazələr</strong></td><td>Maliyyəçiyə yalnız <code>maliyye</code> sxemini aça bilərsiniz</td></tr>"
       "<tr><td><strong>Ad toqquşması</strong></td><td>Hər sxemdə <code>id</code>, <code>ad</code> ola bilər</td></tr>"
       "<tr><td><strong>Genişlənmə</strong></td><td>Yeni modul = yeni sxem, mövcuduna toxunmadan</td></tr></table>"))

# ── BÖLMƏ 5 ──
A('<h2 id="b5">5. Bazanın imkanları — nə var, nə yox</h2>')
A(blok("block-ne", "NƏ EDƏCƏYİK",
       "<p>Bazada hansı obyektlərin olduğunu dəqiq sayacağıq. Bu, sonrakı dərslərin əsasıdır.</p>"))
A('<pre data-lang="sql"><code>SELECT\n'
  "    (SELECT count(DISTINCT table_schema) FROM information_schema.tables\n"
  "     WHERE table_schema NOT IN ('pg_catalog','information_schema'))     AS sxem,\n"
  "    (SELECT count(*) FROM information_schema.tables\n"
  "     WHERE table_type='BASE TABLE'\n"
  "       AND table_schema NOT IN ('pg_catalog','information_schema'))     AS cedvel,\n"
  "    (SELECT count(*) FROM information_schema.views\n"
  "     WHERE table_schema NOT IN ('pg_catalog','information_schema'))     AS gorunus,\n"
  "    (SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace\n"
  "     WHERE n.nspname NOT IN ('pg_catalog','information_schema'))        AS funksiya,\n"
  "    (SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid\n"
  "     JOIN pg_namespace n ON n.oid=c.relnamespace\n"
  "     WHERE NOT t.tgisinternal\n"
  "       AND n.nspname NOT IN ('pg_catalog','information_schema'))        AS trigger,\n"
  "    (SELECT count(*) FROM pg_constraint WHERE contype='f'\n"
  "       AND connamespace::regnamespace::text\n"
  "           NOT IN ('pg_catalog','information_schema'))                  AS xarici_acar;</code></pre>")
A('<pre data-lang="çıxış"><code> sxem | cedvel | gorunus | funksiya | trigger | xarici_acar\n'
  '------+--------+---------+----------+---------+-------------\n'
  '   12 |     48 |       8 |       10 |       5 |          35</code></pre>')
A(blok("block-izah", "İZAH — hər obyekt nə edir?",
       "<table>"
       "<tr><th>Obyekt</th><th>Nədir</th><th>Nə vaxt işlədilir</th></tr>"
       "<tr><td><strong>Cədvəl</strong> (table)</td><td>Məlumatı fiziki saxlayır</td><td>Həmişə</td></tr>"
       "<tr><td><strong>Görünüş</strong> (view)</td><td>Saxlanılmış SELECT</td><td>Təkrarlanan JOIN-lar</td></tr>"
       "<tr><td><strong>Funksiya</strong></td><td>Bazadaxili hesablama</td><td>Parametrli məntiq</td></tr>"
       "<tr><td><strong>Trigger</strong></td><td>Avtomatik işləyən funksiya</td><td>Audit, biznes qaydası</td></tr>"
       "<tr><td><strong>Xarici açar</strong></td><td>Cədvəllərarası əlaqə</td><td>Bütövlüyün qorunması</td></tr>"
       "</table>"))
A(blok("block-ne", "NƏ YOXDUR (hələ)",
       "<table><tr><th>İmkan</th><th>Vəziyyət</th><th>Nə lazımdır</th></tr>"
       "<tr><td>Vektor axtarış (RAG)</td><td><code>ai.embeddingler</code> var</td><td><code>pgvector</code> genişlənməsi</td></tr>"
       "<tr><td>Tam mətn axtarış</td><td>Mümkündür</td><td><code>tsvector</code> + GIN indeks</td></tr>"
       "<tr><td>Bölmələmə</td><td>Böyük cədvəllər üçün</td><td><code>PARTITION BY RANGE</code></td></tr>"
       "<tr><td>Səviyyəli icazə</td><td>Rollar var</td><td><code>CREATE POLICY</code> (RLS)</td></tr>"
       "<tr><td>Coğrafi məlumat</td><td><code>unvan</code> mətn kimi</td><td>PostGIS</td></tr></table>"))

# ── BÖLMƏ 6: 40 SORĞU ──
A('<h2 id="b6">6. 40 vacib sorğu</h2>')
A(blok("block-ne", "NƏ EDƏCƏYİK",
       "<p>40 sorğunu <strong>8 qrupda</strong> nəzərdən keçirəcəyik. Hər sorğu üçün:</p>"
       "<ol><li><strong>NƏ EDİR</strong> — sorğunun nə etdiyi</li>"
       "<li><strong>NƏ GÖSTƏRİR</strong> — real nəticə nə deməkdir</li>"
       "<li>Kod və <strong>real çıxış</strong></li>"
       "<li><strong>OLMASA NƏ OLAR</strong> — bu texnika olmasa nə itirərdik</li>"
       "<li><strong>ƏVƏZİNDƏ</strong> — alternativ yol</li></ol>"))
A('<pre data-lang="bash"><code>cd ~/Deepseek_ARTI/DS_Baza/sql\n'
  'unset DATABASE_URL PGHOST\n'
  'export PGPASSWORD=arti_secret_2025\n'
  'psql -U arti_user -d arti_baza -f 10_sorgular.sql</code></pre>')

for qrup_kodu in "ABCDEFGH":
    harf, ad, tesvir = QRUP_ADLARI[qrup_kodu]
    A('<h3><span class="step-num">%s</span> Qrup %s — %s</h3>' % (harf, harf, ad))
    A(blok("block-izah", "BU QRUP NƏ EDİR", "<p>%s</p>" % tesvir))
    for no in sorted(sorgular):
        if S[no]["qrup"] != qrup_kodu:
            continue
        b = S[no]
        basliq, kod = sorgular[no]
        A('<h4 id="s%d">Sorğu %d — %s</h4>' % (no, no, e(b["basliq"])))
        A(blok("block-ne", "NƏ EDİR", "<p>%s</p>" % b["ne"]))
        A(blok("block-izah", "NƏ GÖSTƏRİR", "<p>%s</p>" % b["gosterir"]))
        A('<pre data-lang="sql"><code>%s</code></pre>' % e(kod))
        if cixisler.get(no):
            A('<pre data-lang="çıxış"><code>%s</code></pre>' % e(cixisler[no]))
        A(blok("block-olmaz", "OLMASA NƏ OLAR", "<p>%s</p>" % b["olmaz"]))
        A(blok("block-evez", "ƏVƏZİNDƏ", "<p>%s</p>" % b["evez"]))
        if b.get("xeber"):
            A(blok("block-xeber", "⚠️ DİQQƏT", "<p>%s</p>" % b["xeber"]))
        A(blok("block-yox", "YOXLAMA %d" % no,
               "<p>Nəticə cədvəldə göstərilənə uyğundursa, sorğu düzgün işləyir.</p>"))

# ── BÖLMƏ 7 ──
A('<h2 id="b7">7. Yoxlama siyahısı</h2>')
A('<div class="block block-yox">')
A('  <span class="block-title">YOXLAMA — DS_BAZA HAZIRDIR?</span>')
A('  <table>')
A('    <tr><th>#</th><th>Yoxlama</th><th>Gözlənilən</th></tr>')
YOXLAMALAR = [
    ("PostgreSQL işləyir", "<code>brew services list</code> → started"),
    ("Bazaya qoşulma", "<code>psql -U arti_user -d arti_baza</code> → prompt gəlir"),
    ("Sxem sayı", "12"),
    ("Cədvəl sayı", "48"),
    ("View sayı", "8"),
    ("Funksiya sayı", "10"),
    ("Trigger sayı", "5"),
    ("Xarici açar sayı", "35"),
    ("40 sorğu xətasız işləyir", "<code>psql -f 10_sorgular.sql</code> → 0 ERROR"),
    ("Tarixlər 2024-2028 aralığında", "<code>min/max</code> yoxlaması"),
]
for i, (y, g) in enumerate(YOXLAMALAR, 1):
    A('    <tr><td>%d</td><td>%s</td><td>%s</td></tr>' % (i, y, g))
A('  </table>')
A('</div>')

# ── BÖLMƏ 8 ──
A('<h2 id="b8">8. Növbəti dərs</h2>')
A(blok("block-ne", "NƏ GƏLİR",
       "<p>Növbəti <strong>DS_Backend</strong> blokudur — 4 dərs:</p>"
       "<table><tr><th>#</th><th>Dərs</th><th>Nə öyrədəcək</th></tr>"
       "<tr><td>1</td><td>Backend-1</td><td>NestJS qurulumu, Prisma 7, ilk endpoint</td></tr>"
       "<tr><td>2</td><td>Backend-2</td><td>Modullar, DTO, validasiya, CRUD</td></tr>"
       "<tr><td>3</td><td>Backend-3</td><td>JWT autentifikasiya, rollar, guard-lar</td></tr>"
       "<tr><td>4</td><td>Backend-4</td><td>AI qatı, audit, testlər, deploy</td></tr></table>"))
A('<div class="success-box">'
  '<strong>DS_Baza tamamlandı.</strong> Baza tanındı, 40 sorğu işlədildi. '
  'Növbəti addım — bu bazanı API kimi dünyaya açmaq: <strong>DS_Backend</em>.</div>')
A('</div>')

A('<script>')
A("""  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('pre').forEach(function (pre) {
      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.textContent = '📋 KOPYALA';
      btn.addEventListener('click', async function (ev) {
        ev.preventDefault();
        var kod = pre.querySelector('code');
        var metn = kod ? kod.textContent : pre.textContent;
        try {
          await navigator.clipboard.writeText(metn);
          btn.textContent = '✅ KOPYALANDI';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = '📋 KOPYALA';
            btn.classList.remove('copied');
          }, 2000);
        } catch (err) {
          var ta = document.createElement('textarea');
          ta.value = metn;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          btn.textContent = '✅ KOPYALANDI';
          setTimeout(function () { btn.textContent = '📋 KOPYALA'; }, 2000);
        }
      });
      pre.insertBefore(btn, pre.firstChild);
    });
  });""")
A('</script>')
A('</body>')
A('</html>')

html_metn = "\n".join(H)
hedef = KOK / "DƏRSLƏR/Deepseek_Baza.html"
hedef.write_text(html_metn, encoding="utf-8")
print("  yazıldı: %s" % hedef)
print("  sətir sayı: %d" % len(html_metn.splitlines()))
print("  həcm: %.1f KB" % (len(html_metn.encode()) / 1024))
