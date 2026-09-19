-- ══════════════════════════════════════════════════════════════
--  Deepseek_ARTI · DS_Baza · 40 VACİB SORĞU
--  Baza: arti_baza | 12 sxem, 48 cədvəl, 8 view, 10 funksiya, 5 trigger
-- ══════════════════════════════════════════════════════════════

\echo '═══ A. BAZANI TANIMAQ (1-6) ═══'

\echo '── 1. Sxemlər və cədvəl sayı'
SELECT table_schema AS sxem, count(*) AS cedvel_sayi
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog','information_schema')
GROUP BY table_schema ORDER BY 2 DESC, 1;

\echo '── 2. Cədvəllərin sətir sayı (canlı statistika)'
SELECT schemaname AS sxem, relname AS cedvel, n_live_tup AS setir
FROM pg_stat_user_tables WHERE n_live_tup > 0
ORDER BY n_live_tup DESC, 1, 2 LIMIT 10;

\echo '── 3. Bir cədvəlin sütunları'
SELECT ordinal_position AS sira, column_name AS sutun, data_type AS tip,
       CASE WHEN is_nullable='NO' THEN 'MƏCBURİ' ELSE 'opsional' END AS mecburi
FROM information_schema.columns
WHERE table_schema='kadrlar' AND table_name='emekdaslar'
ORDER BY ordinal_position;

\echo '── 4. Xarici açarların xəritəsi'
SELECT conrelid::regclass::text AS cedvel, a.attname AS sutun,
       confrelid::regclass::text AS hedef
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid=c.conrelid AND a.attnum=c.conkey[1]
WHERE c.contype='f'
  AND c.connamespace::regnamespace::text NOT IN ('pg_catalog','information_schema')
ORDER BY 1 LIMIT 12;

\echo '── 5. Görünüşlər (view)'
SELECT table_schema AS sxem, table_name AS gorunus
FROM information_schema.views
WHERE table_schema NOT IN ('pg_catalog','information_schema')
ORDER BY 1,2;

\echo '── 6. Funksiyalar və triggerlər'
SELECT n.nspname AS sxem, p.proname AS funksiya,
       CASE WHEN p.prorettype::regtype::text='trigger' THEN 'trigger' ELSE 'adı çağırılan' END AS nov
FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
WHERE n.nspname NOT IN ('pg_catalog','information_schema')
ORDER BY 1,2;

\echo '═══ B. SADƏ SEÇİM (7-12) ═══'

\echo '── 7. Bütün mərkəzlər'
SELECT id, ad, unvan, telefon FROM struktur.merkezler ORDER BY id;

\echo '── 8. Əməkdaşlar: ad, soyad, maaş'
SELECT soyad, ad, maas FROM kadrlar.emekdaslar ORDER BY id LIMIT 3;

\echo '── 9. Maaşa görə sıralama (azalan)'
SELECT soyad || ' ' || ad AS emekdas, maas
FROM kadrlar.emekdaslar ORDER BY maas DESC LIMIT 5;

\echo '── 10. İlk 5 mərkəz (LIMIT)'
SELECT id, ad FROM struktur.merkezler ORDER BY id LIMIT 5;

\echo '── 11. NULL olan sütunlar'
SELECT count(*) AS telefonsuz FROM struktur.shobeler WHERE telefon IS NULL;

\echo '── 12. Təkrarsız dəyərlər (DISTINCT)'
SELECT DISTINCT tip AS aktiv_tipi FROM logistika.aktivler ORDER BY 1;

\echo '═══ C. FİLTRLƏMƏ (13-18) ═══'

\echo '── 13. Bərabərlik filtri'
SELECT ad, seviyye FROM struktur.vezifeler WHERE seviyye = 1;

\echo '── 14. Müqayisə filtri (maaş > 2000)'
SELECT soyad || ' ' || ad AS emekdas, maas
FROM kadrlar.emekdaslar WHERE maas > 2000 ORDER BY maas DESC;

\echo '── 15. BETWEEN — tarix aralığı (2026)'
SELECT ad, baslama_tarixi, bitme_tarixi
FROM tehsil.telim_qruplari
WHERE baslama_tarixi BETWEEN DATE '2026-01-01' AND DATE '2026-12-31'
ORDER BY baslama_tarixi LIMIT 5;

\echo '── 16. IN — siyahıdan biri'
SELECT ad, nov, status FROM maliyye.satinalmalar WHERE status IN ('tamamlandi','muqavile');

\echo '── 17. LIKE — mətn axtarışı'
SELECT ad, email FROM struktur.merkezler WHERE email LIKE '%arti.edu.az' LIMIT 5;

\echo '── 18. AND / OR / NOT'
SELECT ad, status FROM elm.tedqiqat_layiheleri
WHERE status = 'davam edir' AND bitme_tarixi > CURRENT_DATE;

\echo '═══ D. AQREQASİYA (19-24) ═══'

\echo '── 19. COUNT'
SELECT count(*) AS emekdas_sayi FROM kadrlar.emekdaslar;

\echo '── 20. SUM / AVG / MIN / MAX'
SELECT count(*) AS say, round(avg(maas),2) AS orta,
       min(maas) AS min_maas, max(maas) AS max_maas, sum(maas) AS fond
FROM kadrlar.emekdaslar;

\echo '── 21. GROUP BY — mərkəz üzrə'
SELECT merkez_id, count(*) AS emekdas, round(avg(maas),2) AS orta_maas
FROM kadrlar.emekdaslar GROUP BY merkez_id ORDER BY emekdas DESC;

\echo '── 22. GROUP BY + HAVING'
SELECT tip AS aktiv_tipi, count(*) AS say, sum(deyer) AS cem
FROM logistika.aktivler GROUP BY tip HAVING count(*) > 1 ORDER BY cem DESC;

\echo '── 23. COUNT + FILTER (şərti say)'
SELECT tip,
       count(*) AS cem,
       count(*) FILTER (WHERE veziyyet = 'yaxşı') AS yaxsi,
       count(*) FILTER (WHERE veziyyet <> 'yaxşı') AS qeyri_saz
FROM logistika.aktivler GROUP BY tip;

\echo '── 24. ROLLUP — yekun sətirləri'
SELECT COALESCE(il::text,'CƏMİ') AS il, count(*) AS setir, sum(mebleg) AS mebleg
FROM maliyye.budce GROUP BY ROLLUP (il) ORDER BY il NULLS LAST;

\echo '═══ E. BİRLƏŞMƏ (25-31) ═══'

\echo '── 25. INNER JOIN — şöbə + mərkəz'
SELECT s.ad AS shobe, m.ad AS merkez
FROM struktur.shobeler s
JOIN struktur.merkezler m ON m.id = s.merkez_id
ORDER BY m.ad, s.ad LIMIT 6;

\echo '── 26. LEFT JOIN — şöbəsi olmayan mərkəz də görünür'
SELECT m.ad AS merkez, count(s.id) AS shobe_sayi
FROM struktur.merkezler m
LEFT JOIN struktur.shobeler s ON s.merkez_id = m.id
GROUP BY m.ad ORDER BY shobe_sayi DESC LIMIT 6;

\echo '── 27. 3 cədvəl birləşməsi'
SELECT e.soyad || ' ' || e.ad AS emekdas, v.ad AS vezife, m.ad AS merkez
FROM kadrlar.emekdaslar e
JOIN struktur.vezifeler v ON v.id = e.vezife_id
LEFT JOIN struktur.merkezler m ON m.id = e.merkez_id
ORDER BY e.soyad LIMIT 6;

\echo '── 28. 5 cədvəl birləşməsi (tam profil)'
SELECT e.soyad || ' ' || e.ad AS emekdas, v.ad AS vezife, s.ad AS shobe,
       m.ad AS merkez, c.ad AS cins
FROM kadrlar.emekdaslar e
JOIN struktur.vezifeler v ON v.id = e.vezife_id
JOIN struktur.shobeler  s ON s.id = e.shobe_id
JOIN struktur.merkezler m ON m.id = e.merkez_id
JOIN ortaq.cinsiyyet   c ON c.id = e.cinsiyyet_id
ORDER BY e.soyad LIMIT 6;

\echo '── 29. Layihə + istiqamət + rəhbər'
SELECT l.ad AS layihe, i.ad AS istiqamet, e.soyad AS rehber, l.status
FROM elm.tedqiqat_layiheleri l
JOIN elm.tedqiqat_istiqametleri i ON i.id = l.istiqamet_id
LEFT JOIN kadrlar.emekdaslar e ON e.id = l.rehber_id
ORDER BY l.ad LIMIT 6;

\echo '── 30. LEFT JOIN + IS NULL — yetim sətirlər'
SELECT m.ad AS merkez FROM struktur.merkezler m
LEFT JOIN struktur.shobeler s ON s.merkez_id = m.id
WHERE s.id IS NULL;

\echo '── 31. Ad → id xəritəsi (yükləmə üçün tipik)'
SELECT p.ad AS proqram, p.id AS proqram_id, count(q.id) AS qrup
FROM tehsil.telim_proqramlari p
LEFT JOIN tehsil.telim_qruplari q ON q.proqram_id = p.id
GROUP BY p.ad, p.id ORDER BY qrup DESC LIMIT 6;

\echo '═══ F. ALT SORĞULAR (32-35) ═══'

\echo '── 32. WHERE ... IN (alt sorğu)'
SELECT soyad || ' ' || ad AS emekdas, maas
FROM kadrlar.emekdaslar
WHERE merkez_id IN (SELECT id FROM struktur.merkezler WHERE ad ILIKE '%təhsil%')
ORDER BY maas DESC LIMIT 6;

\echo '── 33. EXISTS — korrelyasiyalı alt sorğu'
SELECT m.ad AS merkez FROM struktur.merkezler m
WHERE EXISTS (SELECT 1 FROM struktur.shobeler s WHERE s.merkez_id = m.id)
ORDER BY m.ad LIMIT 6;

\echo '── 34. Skalyar alt sorğu — ortadan yuxarı'
SELECT soyad || ' ' || ad AS emekdas, maas
FROM kadrlar.emekdaslar
WHERE maas > (SELECT avg(maas) FROM kadrlar.emekdaslar)
ORDER BY maas DESC;

\echo '── 35. FROM (alt sorğu) — törəmə cədvəl'
SELECT merkez_id, orta_maas FROM (
  SELECT merkez_id, round(avg(maas),2) AS orta_maas
  FROM kadrlar.emekdaslar GROUP BY merkez_id
) x WHERE orta_maas > 1800 ORDER BY orta_maas DESC;

\echo '═══ G. GÖRÜNÜŞ VƏ FUNKSİYA (36-38) ═══'

\echo '── 36. View-dan sorğu'
SELECT tam_adi, vezife, shobe, merkez, maas FROM kadrlar.v_emekdas_tam ORDER BY maas DESC LIMIT 6;

\echo '── 37. Funksiya çağırışı'
SELECT kadrlar.fn_maas_fondu() AS aylıq_fond,
       struktur.fn_shobe_sayi(2) AS merkez_2_shobe,
       tehsil.fn_telim_istirakci_sayi(1) AS qrup_1_istirakci;

\echo '── 38. View + filtr + sıralama'
SELECT qrup, proqram, istirakci_sayi FROM tehsil.v_telim_qrup_istirakci_sayi
WHERE istirakci_sayi > 0 ORDER BY istirakci_sayi DESC LIMIT 6;

\echo '═══ H. PƏNCƏRƏ VƏ CTE (39-40) ═══'

\echo '── 39. ROW_NUMBER — mərkəz daxilində maaş sırası'
SELECT merkez_id, soyad, maas,
       ROW_NUMBER() OVER (PARTITION BY merkez_id ORDER BY maas DESC) AS sira
FROM kadrlar.emekdaslar ORDER BY merkez_id, sira LIMIT 8;

\echo '── 40. CTE (WITH) — mərhələli analitika'
WITH merkez_cemi AS (
  SELECT merkez_id, count(*) AS emekdas, sum(maas) AS fond
  FROM kadrlar.emekdaslar GROUP BY merkez_id
)
SELECT m.ad AS merkez, c.emekdas AS emekdas_sayi, c.fond AS aylıq_fond,
       round(100.0 * c.fond / sum(c.fond) OVER (), 1) AS pay_faiz
FROM merkez_cemi c JOIN struktur.merkezler m ON m.id = c.merkez_id
ORDER BY c.fond DESC LIMIT 6;
