--
-- PostgreSQL database dump
--

\restrict abVJVP8RHGXGZG6dfWnh5vgW6nsaidUMpmi0AstdCNBp1gE2AR3cvRFfsmaLM8p

-- Dumped from database version 18.6 (Homebrew)
-- Dumped by pg_dump version 18.6 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: ai_promptlar; Type: TABLE DATA; Schema: ai; Owner: -
--

INSERT INTO ai.ai_promptlar (id, ad, tip, prompt_metni, aktiv) VALUES (1, 'İllik hesabat xülasəsi', 'xulase', 'Aşağıdakı hesabat məlumatını 5 cümlə ilə xülasələ:', true);
INSERT INTO ai.ai_promptlar (id, ad, tip, prompt_metni, aktiv) VALUES (2, 'Təlim nəticələrinin analizi', 'analiz', 'Təlim nəticələrini təhlil et və tendensiyaları çıxar:', true);
INSERT INTO ai.ai_promptlar (id, ad, tip, prompt_metni, aktiv) VALUES (3, 'Büdcə icrası sual-cavab', 'sual-cavab', 'Büdcə məlumatına əsasən istifadəçinin sualını cavablandır:', true);
INSERT INTO ai.ai_promptlar (id, ad, tip, prompt_metni, aktiv) VALUES (4, 'PISA nəticələrinin şərhi', 'analiz', 'PISA bal göstəricilərini izah et və tövsiyələr ver:', true);
INSERT INTO ai.ai_promptlar (id, ad, tip, prompt_metni, aktiv) VALUES (5, 'Müəllim sertifikasiya hesabatı', 'xulase', 'Sertifikasiya nəticələrini qısa hesabat kimi yaz:', true);
INSERT INTO ai.ai_promptlar (id, ad, tip, prompt_metni, aktiv) VALUES (6, 'Elmi Şura qərar layihəsi', 'sual-cavab', 'Gündəliyə əsasən qərar layihəsinin mətnini hazırla:', true);
INSERT INTO ai.ai_promptlar (id, ad, tip, prompt_metni, aktiv) VALUES (7, 'Doktorantura statistikası', 'analiz', 'Doktorantlar üzrə statistikanı təhlil et:', true);
INSERT INTO ai.ai_promptlar (id, ad, tip, prompt_metni, aktiv) VALUES (8, 'Satınalma prosesi köməkçisi', 'sual-cavab', 'Satınalma məlumatına əsasən sualı cavablandır:', true);


--
-- Data for Name: ai_sorghular; Type: TABLE DATA; Schema: ai; Owner: -
--

INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (1, 'arti_user', 'İnstitutda neçə mərkəz var?', 'İnstitutda 10 mərkəz/blok var.', 'deepseek', 85, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (2, 'arti_user', '2024-cü il büdcəsi nə qədərdir?', '2024-cü il üzrə ümumi büdcə 4.97 milyon AZN-dir.', 'deepseek', 92, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (3, 'arti_user', 'Neçə elmi tədqiqat layihəsi davam edir?', 'Hazırda 5 layihə davam edir, 3-ü tamamlanıb, 2-si planlaşdırılır.', 'deepseek', 104, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (4, 'arti_user', 'PISA 2022 riyaziyyat balı neçədir?', 'PISA 2022-də riyaziyyat üzrə orta bal 397-dir.', 'deepseek', 78, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (5, 'arti_user', 'Sertifikasiyadan keçən müəllim faizi?', 'Sertifikasiyadan keçən müəllimlərin faizi 78.5%-dir.', 'deepseek', 88, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (6, 'arti_user', 'Neçə doktorant var?', 'Hazırda 10 doktorant qeydiyyatdadır.', 'deepseek', 70, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (7, 'arti_user', 'Bu il neçə təlim qrupu açılıb?', '2024-cü ildə 10 təlim qrupu açılıb.', 'deepseek', 75, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (8, 'arti_user', 'Ən çox xərc hansı sahəyə gedib?', 'Ən çox xərc müəllim təlimlərinə (850 min AZN) gedib.', 'deepseek', 96, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (9, 'arti_user', 'Neçə beynəlxalq qiymətləndirmədə iştirak edirik?', '8 beynəlxalq qiymətləndirmə tsiklində iştirak var.', 'deepseek', 90, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (10, 'arti_user', 'Binaların ümumi sahəsi nə qədərdir?', 'Binaların ümumi sahəsi 7800 m²-dir.', 'deepseek', 82, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (11, 'arti_user', 'Neçə mərkəz var?', '(Demo rejim — API açarı yoxdur)
ARTİ ERP bazası: 10 mərkəz, 14 əməkdaş, 10 tədqiqat layihəsi, 10 sertifikasiya qeydi, ümumi büdcə 18805000 AZN.
Sual: "Neçə mərkəz var?"

Real AI cavabı üçün .env faylına DEEPSEEK_API_KEY (və ya OPENAI_API_KEY) əlavə edin.', 'demo', 0, '2026-09-09 19:58:37.371661+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (12, 'arti_user', 'Neçə mərkəz var?', '(Demo rejim — API açarı yoxdur)
ARTİ ERP bazası: 10 mərkəz, 14 əməkdaş, 10 tədqiqat layihəsi, 10 sertifikasiya qeydi, ümumi büdcə 18805000 AZN.
Sual: "Neçə mərkəz var?"

Real AI cavabı üçün .env faylına DEEPSEEK_API_KEY (və ya OPENAI_API_KEY) əlavə edin.', 'demo', 0, '2026-09-09 19:59:25.834778+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (13, 'arti_user', 'Neçə mərkəz var?', '(Demo rejim — API açarı yoxdur)
ARTİ ERP bazası: 10 mərkəz, 14 əməkdaş, 10 tədqiqat layihəsi, 10 sertifikasiya qeydi, ümumi büdcə 18805000 AZN.
Sual: "Neçə mərkəz var?"

Real AI cavabı üçün .env faylına DEEPSEEK_API_KEY (və ya OPENAI_API_KEY) əlavə edin.', 'demo', 0, '2026-09-09 20:04:56.44817+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (14, 'arti_user', 'Neçə mərkəz var?', '(Demo rejim — API açarı yoxdur)
ARTİ ERP bazası: 10 mərkəz, 14 əməkdaş, 10 tədqiqat layihəsi, 10 sertifikasiya qeydi, ümumi büdcə 18805000 AZN.
Sual: "Neçə mərkəz var?"

Real AI cavabı üçün .env faylına DEEPSEEK_API_KEY (və ya OPENAI_API_KEY) əlavə edin.', 'demo', 0, '2026-09-09 20:18:03.367561+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (15, 'arti_user', 'Neçə mərkəz var?', '(Demo rejim — API açarı yoxdur)
ARTİ ERP bazası: 10 mərkəz, 14 əməkdaş, 10 tədqiqat layihəsi, 10 sertifikasiya qeydi, ümumi büdcə 18805000 AZN.
Sual: "Neçə mərkəz var?"

Real AI cavabı üçün .env faylına DEEPSEEK_API_KEY (və ya OPENAI_API_KEY) əlavə edin.', 'demo', 0, '2026-09-09 20:19:30.462941+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (16, 'arti_user', 'Neçə mərkəz var?', '(Demo rejim — API açarı yoxdur)
ARTİ ERP bazası: 10 mərkəz, 14 əməkdaş, 10 tədqiqat layihəsi, 10 sertifikasiya qeydi, ümumi büdcə 18805000 AZN.
Sual: "Neçə mərkəz var?"

Real AI cavabı üçün .env faylına DEEPSEEK_API_KEY (və ya OPENAI_API_KEY) əlavə edin.', 'demo', 0, '2026-09-09 20:20:32.514967+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (17, 'arti_user', 'İnstitutda neçə mərkəz var?', '(Demo rejim — API açarı yoxdur)
ARTİ ERP bazası: 10 mərkəz, 14 əməkdaş, 10 tədqiqat layihəsi, 10 sertifikasiya qeydi, ümumi büdcə 18805000 AZN.
Sual: "İnstitutda neçə mərkəz var?"

Real AI cavabı üçün .env faylına DEEPSEEK_API_KEY (və ya OPENAI_API_KEY) əlavə edin.', 'demo', 0, '2026-09-09 20:32:25.761129+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (18, 'arti_user', 'İnstitutda neçə mərkəz var?', '(Demo rejim — API açarı yoxdur)
ARTİ ERP bazası: 10 mərkəz, 14 əməkdaş, 10 tədqiqat layihəsi, 10 sertifikasiya qeydi, ümumi büdcə 18805000 AZN.
Sual: "İnstitutda neçə mərkəz var?"

Real AI cavabı üçün .env faylına DEEPSEEK_API_KEY (və ya OPENAI_API_KEY) əlavə edin.', 'demo', 0, '2026-09-09 20:34:42.546567+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (19, 'arti_user', 'Neçə mərkəz var?', '(Demo rejim — API açarı yoxdur)
ARTİ ERP bazası: 10 mərkəz, 14 əməkdaş, 10 tədqiqat layihəsi, 10 sertifikasiya qeydi, ümumi büdcə 18805000 AZN.
Sual: "Neçə mərkəz var?"

Real AI cavabı üçün .env faylına DEEPSEEK_API_KEY (və ya OPENAI_API_KEY) əlavə edin.', 'demo', 0, '2026-09-09 20:35:53.340061+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (20, 'arti_user', 'Neçə mərkəz var?', '(Demo rejim — API açarı yoxdur)
ARTİ ERP bazası: 10 mərkəz, 14 əməkdaş, 10 tədqiqat layihəsi, 10 sertifikasiya qeydi, ümumi büdcə 18805000 AZN.
Sual: "Neçə mərkəz var?"

Real AI cavabı üçün .env faylına DEEPSEEK_API_KEY (və ya OPENAI_API_KEY) əlavə edin.', 'demo', 0, '2026-09-09 20:39:27.757707+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (21, 'arti_user', 'ARTİ nədir?', '[DEMO] API açarı təyin olunmayıb. Sualınız: "ARTİ nədir?". Bu cavab demo rejimdə yaradıldı — .env-də DEEPSEEK_API_KEY və ya OPENAI_API_KEY təyin edəndə real AI cavabı gələcək.', 'demo', 0, '2026-09-10 17:05:30.572014+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (22, 'arti_user', 'İnstitutda neçə şöbə var', 'İnstitutunuzun adını qeyd etmədiyiniz üçün hansı institutdan bəhs etdiyinizi bilmirəm. Azərbaycanda və dünyada çoxsaylı institutlar var və hər birinin şöbə sayı fərqlidir.

Zəhmət olmasa:
- **Hansı institutdan** bəhs etdiyinizi qeyd edin (məsələn, AMEA-nın hansı institutu, hansı universitetin nəzdindəki institut və s.)
- Və ya **institutun vebsaytını** paylaşın

O zaman sizə dəqiq məlumat verə bilərəm.', 'deepseek', 0, '2026-09-10 19:40:08.667454+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (23, 'arti_user', 'Təhsil institutu AI tətpiq etmək istəyirsə haradan və necə başlamalıdır', '# Təhsil İnstitutunda AI Tətbiqinə Başlamaq: Addım-addım Yol Xəritəsi

## 1. Strateji Hazırlıq (1-2 ay)

**Ehtiyacların müəyyənləşdirilməsi:**
- Hansı problemi həll etmək istədiyinizi dəqiqləşdirin (qiymətləndirmə, fərdiləşdirilmiş təlim, inzibati işlər, tələbə dəstəyi)
- Mövcud resursları və boşluqları qiymətləndirin
- Kiçik pilot layihə üçün sahə seçin (bütün institutu birdən əhatə etməyin)

**Rəhbərliyin dəstəyini qazanmaq:**
- Büdcə, komanda və vaxt tələb edən təklif hazırlayın
- ROI (investisiya gəliri) göstəricilərini müəyyən edin

## 2. Komanda və İnfrastruktur (1-2 ay)

**Komanda qurun:**
- Layihə rəhbəri
- IT mütəxəssisi / data engineer
- Pedaqoji ekspert (müəllim nümayəndəsi)
- Etika/hüquq məsləhətçisi

**Texniki baza:**
- Data toplama və saxlama sistemləri
- Bulud xidmətləri (AWS, Azure, Google Cloud) və ya yerli serverlər
- Təhlükəsizlik və məxfilik qaydaları (GDPR tipli normalar)

## 3. Təlim və İnkişaf (davamlı)

- Müəllimlər üçün AI savadlılığı kursları
- Prompt engineering və AI alətlərindən istifadə təlimi
- Tələbələr üçün AI-dan etik istifadə qaydaları

## 4. Pilot Layihə (3-6 ay)

**Tipik başlanğıc sahələri:**
| Sahə | Nümunə tətbiq |
|------|---------------|
| Qiymətləndirmə | Avtomatik sual generasiyası, esselərin ilkin yoxlanışı |
| Təlim | Fərdiləşdirilmiş öyrənmə yolları, ağıllı repetitorlar |
| İnzibati | Sənəd emalı, cədvəl optimallaşdırılması |
| Tələbə dəstəyi | 24/7 chatbot, erkən xəbərdarlıq sistemləri |

**Mövcud alətlər (başlamaq üçün):**
- ChatGPT / Claude / Gemini (müəllim hazırlığı üçün)
- Khan Academy Khanmigo, Duolingo kimi hazır platformalar
- Google Classroom + AI əlavələri
- Açıq mənbə: Moodle + AI plaqinləri, Open edX

## 5. Qiymətləndirmə və Genişləndirmə

- KPI-lar: tələbə nəticələri, müəllim vaxtına qənaət, məmnunluq
- Pilot nəticələrinə əsasən düzəlişlər
- Uğurlu sahələri miqyaslandırın

## 6. Kritik Prinsiplər (bunları unutmayın!)

✅ **Etika və şəffaflıq** — AI qərarları izah edilə bilən olmalı
✅ **Məlumat məxfiliyi** — tələbə dataları qorunmalı
✅ **İnsan nəzarəti** — AI köməkçi, qərar verən deyil
✅ **Bərabərlik** — heç bir qrupu kənarda qoymasın
✅ **Dəyişən tənzimləmə** — qanunvericiliyi izləyin

## Tövsiyə olunan ilk addım

**2 həftə ərzində:**
1. İnstitut daxilində maraqlı şəxsləri toplayın (işçi qrup)
2. 1 konkret problem seçin (məsələn: "müəllimlərin dərs hazırlığına sərf etdiyi vaxtı azaltmaq")
3. Pulsuz alətlərlə kiçik eksperiment aparın
4. Nəticələri rəhbərliyə təqdim edin

---

**Əlavə resurslar:**
- UNESCO AI in Education guidelines
- European Commission Ethical Guidelines on AI in Education
- Coursera/edX: "AI for Education" kursları

Hansı sahədə daha konkret kömək lazımdır — texniki seçim, büdcə planlaması, yoxsa müəllim təlimi?', 'deepseek', 0, '2026-09-10 19:41:38.660088+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (24, 'arti_user', 'ARTI nedir?', '[DEMO] API acari teyin olunmayib. Sualiniz: "ARTI nedir?". Bu cavab demo rejimde yaradildi — .env-de DEEPSEEK_API_KEY ve ya OPENAI_API_KEY teyin edende real AI cavabi gelecek.', 'demo', 0, '2026-09-14 11:32:40.029389+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (25, 'arti_user', 'ARTI nedir?', '[DEMO] API acari teyin olunmayib. Sualiniz: "ARTI nedir?". Bu cavab demo rejimde yaradildi — .env-de DEEPSEEK_API_KEY ve ya OPENAI_API_KEY teyin edende real AI cavabi gelecek.', 'demo', 0, '2026-09-14 11:33:33.318914+04');
INSERT INTO ai.ai_sorghular (id, istifadeci, sorghu, cavab, model, token_sayi, vaxt) VALUES (26, 'arti_user', 'ARTI nedir ve ne edir?', '[DEMO] API acari teyin olunmayib. Sualiniz: "ARTI nedir ve ne edir?". Bu cavab demo rejimde yaradildi — .env-de DEEPSEEK_API_KEY ve ya OPENAI_API_KEY teyin edende real AI cavabi gelecek.', 'demo', 0, '2026-09-14 11:37:51.339021+04');


--
-- Data for Name: embeddingler; Type: TABLE DATA; Schema: ai; Owner: -
--

INSERT INTO ai.embeddingler (id, cedvel_adi, sened_id, metn, vektor, yaradilma) VALUES (1, 'elm.neshrler', 1, 'Təhsilin nəzəriyyəsi və tarixi dərsliyi', NULL, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.embeddingler (id, cedvel_adi, sened_id, metn, vektor, yaradilma) VALUES (2, 'elm.neshrler', 3, 'Kurikulumun əsasları dərsliyi', NULL, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.embeddingler (id, cedvel_adi, sened_id, metn, vektor, yaradilma) VALUES (3, 'elm.meqaleler', 1, 'Kurikulum islahatlarının nəticələri məqaləsi', NULL, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.embeddingler (id, cedvel_adi, sened_id, metn, vektor, yaradilma) VALUES (4, 'qiymetlendirme.monitorinq_hesabatlari', 3, 'PISA 2022 nəticələrinin milli hesabatı', NULL, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.embeddingler (id, cedvel_adi, sened_id, metn, vektor, yaradilma) VALUES (5, 'metodika.metodik_vesaitler', 3, 'İnklüziv təhsil üzrə müəllim təlimatı', NULL, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.embeddingler (id, cedvel_adi, sened_id, metn, vektor, yaradilma) VALUES (6, 'tehsil.telim_proqramlari', 1, 'Müəllim sertifikasiyasına hazırlıq proqramı', NULL, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.embeddingler (id, cedvel_adi, sened_id, metn, vektor, yaradilma) VALUES (7, 'sened.emrler', 1, '2024-cü il iş planının təsdiqi əmri', NULL, '2026-09-09 15:51:08.340537+04');
INSERT INTO ai.embeddingler (id, cedvel_adi, sened_id, metn, vektor, yaradilma) VALUES (8, 'elm.doktorantura_proqramlari', 1, 'Təhsilin nəzəriyyəsi və tarixi ixtisas proqramı', NULL, '2026-09-09 15:51:08.340537+04');


--
-- Data for Name: audit_log; Type: TABLE DATA; Schema: audit; Owner: -
--

INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (1, 'kadrlar.emekdaslar', 'INSERT', '1', 'arti_user', '2026-09-09 15:51:08.340537+04', 'İlkin seed');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (2, 'kadrlar.emekdaslar', 'INSERT', '2', 'arti_user', '2026-09-09 15:51:08.340537+04', 'İlkin seed');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (3, 'struktur.merkezler', 'INSERT', '1', 'arti_user', '2026-09-09 15:51:08.340537+04', 'İlkin seed');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (4, 'struktur.shobeler', 'INSERT', '1', 'arti_user', '2026-09-09 15:51:08.340537+04', 'İlkin seed');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (5, 'maliyye.budce', 'INSERT', '1', 'arti_user', '2026-09-09 15:51:08.340537+04', 'İlkin seed');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (6, 'elm.tedqiqat_layiheleri', 'INSERT', '1', 'arti_user', '2026-09-09 15:51:08.340537+04', 'İlkin seed');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (7, 'tehsil.sertifikasiya', 'INSERT', '1', 'arti_user', '2026-09-09 15:51:08.340537+04', 'İlkin seed');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (8, 'sened.emrler', 'INSERT', '1', 'arti_user', '2026-09-09 15:51:08.340537+04', 'İlkin seed');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (9, 'audit.audit_log', 'INSERT', '1', 'arti_user', '2026-09-09 15:51:08.340537+04', 'Audit jurnalının başlanması');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (10, 'ai.ai_promptlar', 'INSERT', '1', 'arti_user', '2026-09-09 15:51:08.340537+04', 'İlkin seed');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (11, 'kadrlar.emekdaslar', 'INSERT', '15', 'arti_user', '2026-09-09 15:58:25.173556+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (12, 'kadrlar.emekdaslar', 'DELETE', '15', 'arti_user', '2026-09-09 15:58:25.176435+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (13, 'elm.tedqiqat_layiheleri', 'INSERT', '11', 'arti_user', '2026-09-10 16:18:26.136218+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (14, 'kadrlar.emekdaslar', 'INSERT', '15', 'arti_user', '2026-09-11 08:58:28.759005+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (15, 'auth', 'POST', NULL, 'namelum', '2026-09-14 11:37:21.62906+04', '/api/v1/auth/login');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (16, 'ai', 'POST', '26', 'admin@arti.edu.az', '2026-09-14 11:37:51.342252+04', '/api/v1/ai/sorgu');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (17, 'struktur', 'POST', '14', 'admin@arti.edu.az', '2026-09-14 11:38:08.144713+04', '/api/v1/struktur/merkezler');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (18, 'auth', 'POST', NULL, 'namelum', '2026-09-14 16:01:42.981852+04', '/api/v1/auth/login');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (19, 'auth', 'POST', NULL, 'namelum', '2026-09-14 16:01:44.465225+04', '/api/v1/auth/login');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (20, 'auth', 'POST', NULL, 'namelum', '2026-09-14 16:01:44.523579+04', '/api/v1/auth/login');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (21, 'auth', 'POST', NULL, 'namelum', '2026-09-14 16:24:46.801548+04', '/api/v1/auth/login');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (22, 'auth', 'POST', NULL, 'namelum', '2026-09-14 16:25:54.516976+04', '/api/v1/auth/login');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (122, 'kadrlar.emekdaslar', 'DELETE', '15', 'arti_user', '2026-09-19 10:36:41.950723+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (123, 'kadrlar.emekdaslar', 'UPDATE', '8', 'arti_user', '2026-09-19 10:37:06.244072+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (124, 'kadrlar.emekdaslar', 'UPDATE', '9', 'arti_user', '2026-09-19 10:37:06.244072+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (125, 'kadrlar.emekdaslar', 'UPDATE', '10', 'arti_user', '2026-09-19 10:37:06.244072+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (126, 'kadrlar.emekdaslar', 'UPDATE', '13', 'arti_user', '2026-09-19 10:37:06.244072+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (127, 'kadrlar.emekdaslar', 'UPDATE', '1', 'arti_user', '2026-09-19 10:37:06.244072+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (128, 'kadrlar.emekdaslar', 'UPDATE', '2', 'arti_user', '2026-09-19 10:37:06.244072+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (77, 'elm.tedqiqat_layiheleri', 'UPDATE', '1', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (78, 'elm.tedqiqat_layiheleri', 'UPDATE', '2', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (79, 'elm.tedqiqat_layiheleri', 'UPDATE', '3', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (80, 'elm.tedqiqat_layiheleri', 'UPDATE', '4', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (81, 'elm.tedqiqat_layiheleri', 'UPDATE', '5', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (82, 'elm.tedqiqat_layiheleri', 'UPDATE', '6', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (83, 'elm.tedqiqat_layiheleri', 'UPDATE', '7', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (84, 'elm.tedqiqat_layiheleri', 'UPDATE', '8', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (85, 'elm.tedqiqat_layiheleri', 'UPDATE', '9', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (86, 'elm.tedqiqat_layiheleri', 'UPDATE', '10', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (87, 'kadrlar.emekdaslar', 'UPDATE', '1', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (88, 'kadrlar.emekdaslar', 'UPDATE', '2', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (89, 'kadrlar.emekdaslar', 'UPDATE', '3', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (90, 'kadrlar.emekdaslar', 'UPDATE', '4', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (91, 'kadrlar.emekdaslar', 'UPDATE', '5', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (92, 'kadrlar.emekdaslar', 'UPDATE', '6', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (93, 'kadrlar.emekdaslar', 'UPDATE', '7', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (94, 'kadrlar.emekdaslar', 'UPDATE', '8', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (95, 'kadrlar.emekdaslar', 'UPDATE', '9', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (96, 'kadrlar.emekdaslar', 'UPDATE', '10', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (97, 'kadrlar.emekdaslar', 'UPDATE', '11', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (98, 'kadrlar.emekdaslar', 'UPDATE', '12', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (99, 'kadrlar.emekdaslar', 'UPDATE', '13', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (100, 'kadrlar.emekdaslar', 'UPDATE', '14', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (101, 'maliyye.satinalmalar', 'UPDATE', '1', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (102, 'maliyye.satinalmalar', 'UPDATE', '2', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (103, 'maliyye.satinalmalar', 'UPDATE', '3', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (104, 'maliyye.satinalmalar', 'UPDATE', '4', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (105, 'maliyye.satinalmalar', 'UPDATE', '5', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (106, 'maliyye.satinalmalar', 'UPDATE', '6', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (107, 'maliyye.satinalmalar', 'UPDATE', '7', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (108, 'maliyye.satinalmalar', 'UPDATE', '8', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (109, 'maliyye.satinalmalar', 'UPDATE', '9', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (110, 'maliyye.satinalmalar', 'UPDATE', '10', 'arti_user', '2026-09-19 10:35:02.868952+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (111, 'maliyye.budce', 'UPDATE', '1', 'arti_user', '2026-09-19 10:35:10.638841+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (112, 'maliyye.budce', 'UPDATE', '2', 'arti_user', '2026-09-19 10:35:26.907969+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (113, 'maliyye.budce', 'UPDATE', '3', 'arti_user', '2026-09-19 10:35:26.907969+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (114, 'maliyye.budce', 'UPDATE', '4', 'arti_user', '2026-09-19 10:35:26.907969+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (115, 'maliyye.budce', 'UPDATE', '5', 'arti_user', '2026-09-19 10:35:26.907969+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (116, 'maliyye.budce', 'UPDATE', '6', 'arti_user', '2026-09-19 10:35:26.907969+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (117, 'maliyye.budce', 'UPDATE', '7', 'arti_user', '2026-09-19 10:35:26.907969+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (118, 'maliyye.budce', 'UPDATE', '8', 'arti_user', '2026-09-19 10:35:26.907969+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (119, 'maliyye.budce', 'UPDATE', '9', 'arti_user', '2026-09-19 10:35:26.907969+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (120, 'maliyye.budce', 'UPDATE', '10', 'arti_user', '2026-09-19 10:35:26.907969+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (121, 'maliyye.budce', 'UPDATE', '1', 'arti_user', '2026-09-19 10:35:26.907969+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (129, 'kadrlar.emekdaslar', 'UPDATE', '3', 'arti_user', '2026-09-19 10:37:06.244072+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (130, 'kadrlar.emekdaslar', 'UPDATE', '4', 'arti_user', '2026-09-19 10:37:06.244072+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (131, 'kadrlar.emekdaslar', 'UPDATE', '5', 'arti_user', '2026-09-19 10:37:06.244072+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (132, 'kadrlar.emekdaslar', 'UPDATE', '6', 'arti_user', '2026-09-19 10:37:06.244072+04', 'Trigger ilə avtomatik qeyd');
INSERT INTO audit.audit_log (id, cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt, qeyd) VALUES (133, 'kadrlar.emekdaslar', 'UPDATE', '7', 'arti_user', '2026-09-19 10:37:06.244072+04', 'Trigger ilə avtomatik qeyd');


--
-- Data for Name: doktorantura_proqramlari; Type: TABLE DATA; Schema: elm; Owner: -
--

INSERT INTO elm.doktorantura_proqramlari (id, ad, ixtisas_kodu, seviyye, muddet_il, qeyd) VALUES (1, 'Təhsilin nəzəriyyəsi və tarixi', '5801.01', 'doktorantura', 3, NULL);
INSERT INTO elm.doktorantura_proqramlari (id, ad, ixtisas_kodu, seviyye, muddet_il, qeyd) VALUES (2, 'Ümumi pedaqogika', '5801.02', 'doktorantura', 3, NULL);
INSERT INTO elm.doktorantura_proqramlari (id, ad, ixtisas_kodu, seviyye, muddet_il, qeyd) VALUES (3, 'Pedaqoji psixologiya', '5802.01', 'doktorantura', 3, NULL);
INSERT INTO elm.doktorantura_proqramlari (id, ad, ixtisas_kodu, seviyye, muddet_il, qeyd) VALUES (4, 'Təhsilin idarə olunması', '5801.04', 'doktorantura', 3, NULL);
INSERT INTO elm.doktorantura_proqramlari (id, ad, ixtisas_kodu, seviyye, muddet_il, qeyd) VALUES (5, 'Təlimin metodikası', '5801.05', 'doktorantura', 3, NULL);
INSERT INTO elm.doktorantura_proqramlari (id, ad, ixtisas_kodu, seviyye, muddet_il, qeyd) VALUES (6, 'Xüsusi pedaqogika', '5801.06', 'doktorantura', 3, NULL);
INSERT INTO elm.doktorantura_proqramlari (id, ad, ixtisas_kodu, seviyye, muddet_il, qeyd) VALUES (7, 'Təhsilin nəzəriyyəsi və tarixi', '5801.01', 'dissertantura', 4, NULL);
INSERT INTO elm.doktorantura_proqramlari (id, ad, ixtisas_kodu, seviyye, muddet_il, qeyd) VALUES (8, 'Ümumi pedaqogika', '5801.02', 'dissertantura', 4, NULL);


--
-- Data for Name: cinsiyyet; Type: TABLE DATA; Schema: ortaq; Owner: -
--

INSERT INTO ortaq.cinsiyyet (id, ad, qisa_ad) VALUES (1, 'Kişi', 'K');
INSERT INTO ortaq.cinsiyyet (id, ad, qisa_ad) VALUES (2, 'Qadın', 'Q');
INSERT INTO ortaq.cinsiyyet (id, ad, qisa_ad) VALUES (3, 'Digər', 'D');


--
-- Data for Name: elmi_adlar; Type: TABLE DATA; Schema: ortaq; Owner: -
--

INSERT INTO ortaq.elmi_adlar (id, ad, qisa_ad) VALUES (1, 'Professor', 'prof.');
INSERT INTO ortaq.elmi_adlar (id, ad, qisa_ad) VALUES (2, 'Dosent', 'dos.');
INSERT INTO ortaq.elmi_adlar (id, ad, qisa_ad) VALUES (3, 'Böyük elmi işçi', 'b.e.i.');
INSERT INTO ortaq.elmi_adlar (id, ad, qisa_ad) VALUES (4, 'Elmi işçi', 'e.i.');


--
-- Data for Name: elmi_dereceler; Type: TABLE DATA; Schema: ortaq; Owner: -
--

INSERT INTO ortaq.elmi_dereceler (id, ad, qisa_ad) VALUES (1, 'Bakalavr', 'B');
INSERT INTO ortaq.elmi_dereceler (id, ad, qisa_ad) VALUES (2, 'Magistr', 'M');
INSERT INTO ortaq.elmi_dereceler (id, ad, qisa_ad) VALUES (3, 'Fəlsəfə doktoru', 'PhD');
INSERT INTO ortaq.elmi_dereceler (id, ad, qisa_ad) VALUES (4, 'Elmlər doktoru', 'Ed');


--
-- Data for Name: is_statuslari; Type: TABLE DATA; Schema: ortaq; Owner: -
--

INSERT INTO ortaq.is_statuslari (id, ad, tesvir, aktiv) VALUES (1, 'Aktiv', 'Hazırda işləyir', true);
INSERT INTO ortaq.is_statuslari (id, ad, tesvir, aktiv) VALUES (2, 'Məzuniyyətdə', 'İllik məzuniyyətdədir', true);
INSERT INTO ortaq.is_statuslari (id, ad, tesvir, aktiv) VALUES (3, 'Xəstəlik məzuniyyətində', 'Müvəqqəti əmək qabiliyyətini itirib', true);
INSERT INTO ortaq.is_statuslari (id, ad, tesvir, aktiv) VALUES (4, 'Ezamiyyətdə', 'Xidməti ezamiyyətdədir', true);
INSERT INTO ortaq.is_statuslari (id, ad, tesvir, aktiv) VALUES (5, 'Sınaq müddətində', 'Yeni işə qəbul olunub, sınaqda', true);
INSERT INTO ortaq.is_statuslari (id, ad, tesvir, aktiv) VALUES (6, 'İşdən çıxıb', 'Əmək müqaviləsinə xitam verilib', true);
INSERT INTO ortaq.is_statuslari (id, ad, tesvir, aktiv) VALUES (7, 'Təqaüddə', 'Yaşa görə əmək pensiyasındadır', true);
INSERT INTO ortaq.is_statuslari (id, ad, tesvir, aktiv) VALUES (8, 'Yarımştat', 'Yarım iş günü əsasında işləyir', true);


--
-- Data for Name: merkezler; Type: TABLE DATA; Schema: struktur; Owner: -
--

INSERT INTO struktur.merkezler (id, ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv) VALUES (1, 'Elmi katiblik', 'katiblik', 'Elmi Şuranın işinin təşkili və sənədləşdirilməsi', 'Zərifə Əliyeva 96, Bakı', '+994 12 599 08 08', 'elmi.katib@arti.edu.az', '2016-11-14', true);
INSERT INTO struktur.merkezler (id, ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv) VALUES (2, 'Elmi-pedaqoji tədqiqatlar mərkəzi', 'merkez', 'Təhsilin nəzəriyyəsi, tarixi, iqtisadiyyatı üzrə tədqiqatlar', 'Zərifə Əliyeva 96, Bakı', '+994 12 599 08 08', 'tedqiqat@arti.edu.az', '2016-11-14', true);
INSERT INTO struktur.merkezler (id, ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv) VALUES (3, 'Təhsilverənlərin peşəkar inkişafı mərkəzi', 'merkez', 'Müəllimlərin peşəkar inkişafı, MİQ və sertifikasiya', 'Mir Cəlal Paşayev 71, Bakı', '+994 12 599 08 08', 'inkişaf@arti.edu.az', '2016-11-14', true);
INSERT INTO struktur.merkezler (id, ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv) VALUES (4, 'Metodik dəstək mərkəzi', 'merkez', 'Metodik xidmətin təşkili, proqramları və əlaqələndirilməsi', 'Mir Cəlal Paşayev 71, Bakı', '+994 12 599 08 08', 'metodika@arti.edu.az', '2016-11-14', true);
INSERT INTO struktur.merkezler (id, ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv) VALUES (5, 'Təhsildə məzmun, kurikulum və standartlar mərkəzi', 'merkez', 'Təhsil proqramları (kurikulumlar), fənn proqramları, dərsliklər', 'Afiyəddin Cəlilov 86, Bakı', '+994 12 599 08 08', 'kurikulum@arti.edu.az', '2016-11-14', true);
INSERT INTO struktur.merkezler (id, ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv) VALUES (6, 'Qiymətləndirmə, təhlil və monitorinq mərkəzi', 'merkez', 'Milli və beynəlxalq qiymətləndirmə (PISA, TIMSS), monitorinq', 'Afiyəddin Cəlilov 86, Bakı', '+994 12 599 08 08', 'qiymet@arti.edu.az', '2016-11-14', true);
INSERT INTO struktur.merkezler (id, ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv) VALUES (7, 'Xüsusi istedadlı uşaqlarla iş mərkəzi', 'merkez', 'İstedadlı uşaqların aşkarlanması, olimpiadalar, STEAM', 'Afiyəddin Cəlilov 86, Bakı', '+994 12 599 08 08', 'istedad@arti.edu.az', '2016-11-14', true);
INSERT INTO struktur.merkezler (id, ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv) VALUES (8, 'Tədris resursları mərkəzi', 'merkez', 'Dərslik, metodik vəsait və təlim materiallarının hazırlanması', 'Afiyəddin Cəlilov 86, Bakı', '+994 12 599 08 08', 'resurs@arti.edu.az', '2016-11-14', true);
INSERT INTO struktur.merkezler (id, ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv) VALUES (9, 'Təhsil texnologiyaları mərkəzi', 'merkez', 'Rəqəmsal resurslar, e-learning, videotəlimatlar, İT infrastruktur', 'Fətəli Xan Xoyski 109, Bakı', '+994 12 599 08 08', 'it@arti.edu.az', '2016-11-14', true);
INSERT INTO struktur.merkezler (id, ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv) VALUES (10, 'Funksional şöbələr', 'funksional', 'İnzibati və dəstək şöbələri (HR, maliyyə, satınalma, ümumi)', 'Zərifə Əliyeva 96, Bakı', '+994 12 000 00 00', 'info@arti.edu.az', '2016-11-14', true);


--
-- Data for Name: shobeler; Type: TABLE DATA; Schema: struktur; Owner: -
--

INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (1, 2, 'Təhsilin nəzəriyyəsi və tarixi şöbəsi', 'TNT', 'Təhsilin nəzəriyyəsi və tarixi üzrə tədqiqatlar', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (2, 2, 'Təhsilin iqtisadiyyatı və idarə olunması şöbəsi', 'Tİİ', 'Təhsilin iqtisadiyyatı və idarəetmə tədqiqatları', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (3, 2, 'Təlimin nəzəriyyəsi və metodikası şöbəsi', 'TNM', 'Təlim metodikaları üzrə tədqiqatlar', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (4, 2, 'Psixologiya və xüsusi təhsil şöbəsi', 'PXT', 'Psixologiya, inklüziv və xüsusi təhsil', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (5, 2, 'Elmi kitabxana', 'EK', 'Elmi fond, kitabxana xidmətləri', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (6, 2, 'Təşkilati şöbə', 'TŞ', 'Elmi tədbirlərin və işlərin təşkili', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (7, 2, 'Elmi-pedaqoji kadrların hazırlanması şöbəsi', 'EPK', 'Doktorantura və elmi kadr hazırlığı', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (8, 3, 'Əlavə təhsilin proqramları və standartları şöbəsi', 'ƏPS', 'Əlavə təhsil proqramları və standartları', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (9, 3, 'Əlavə təhsil üzrə innovasiyalar və tədqiqatlar şöbəsi', 'ƏİT', 'Əlavə təhsildə innovasiya və tədqiqat', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (10, 3, 'Əlavə təhsil xidmətlərinin keyfiyyətinə nəzarət şöbəsi', 'ƏKN', 'Əlavə təhsilin keyfiyyət nəzarəti', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (11, 3, 'Əlavə təhsilin təşkili şöbəsi', 'ƏT', 'Əlavə təhsil prosesinin təşkili', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (12, 3, 'Təhsil işçilərinin qiymətləndirilməsi şöbəsi', 'TİQ', 'Müəllimlərin qiymətləndirilməsi (MİQ)', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (13, 3, 'Təhsil işçilərinin sertifikatlaşdırılması şöbəsi', 'TİS', 'Müəllimlərin sertifikasiyası', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (14, 4, 'Metodik xidmətin təşkili və monitorinqi şöbəsi', 'MTM', 'Metodik xidmətin təşkili və monitorinqi', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (15, 4, 'Metodik xidmət proqramları və standartları şöbəsi', 'MPS', 'Metodik xidmət proqramları', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (16, 4, 'Metodik xidmətin əlaqələndirilməsi şöbəsi', 'ME', 'Metodik xidmətin əlaqələndirilməsi', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (17, 5, 'Dil fənlərinin proqramları şöbəsi', 'DF', 'Dil fənlərinin kurikulumları', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (18, 5, 'Məktəbəqədər təhsilin proqramları şöbəsi', 'MTP', 'Məktəbəqədər təhsil proqramları', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (19, 5, 'Təbiət və texniki fənlərin proqramları şöbəsi', 'TTF', 'Təbiət və texniki fənn proqramları', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (20, 5, 'Sosial, humanitar və digər fənlərin proqramları şöbəsi', 'SHF', 'Sosial və humanitar fənn proqramları', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (21, 5, 'Peşə və ömürboyu təhsilin proqramları şöbəsi', 'PÖT', 'Peşə və ömürboyu təhsil proqramları', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (22, 5, 'Tədris resursları şöbəsi', 'TR', 'Dərslik və tədris resursları', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (23, 6, 'Təhsildə tətbiqi tədqiqatlar şöbəsi', 'TT', 'Tətbiqi tədqiqatlar', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (24, 6, 'Təhsildə nailiyyətlərin qiymətləndirilməsi şöbəsi', 'TNQ', 'Şagird nailiyyətlərinin qiymətləndirilməsi', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (25, 6, 'Milli və beynəlxalq qiymətləndirmə tədqiqatları şöbəsi', 'MBQ', 'PISA, TIMSS və milli qiymətləndirmə', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (26, 6, 'Statistik məlumatların təhlili şöbəsi', 'SM', 'Statistik məlumatların təhlili', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (27, 7, 'Məzmun və qiymətləndirmə şöbəsi', 'MQ', 'İstedadlı uşaqlar üçün məzmun', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (28, 7, 'Xüsusi istedadlı uşaqlarla işin təşkili şöbəsi', 'XİT', 'İstedadlı uşaqlarla işin təşkili', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (29, 10, 'Təhsildə əməkdaşlıq və layihələrin idarə olunması şöbəsi', 'ƏL', 'Beynəlxalq layihələr və əməkdaşlıq', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (30, 10, 'Təhsildə innovasiyalar şöbəsi', 'Tİ', 'Təhsildə innovasiyalar', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (31, 10, 'İctimaiyyətlə əlaqələr şöbəsi', 'İƏ', 'İctimaiyyətlə əlaqələr və media', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (32, 10, 'İnsan resursları şöbəsi', 'İR', 'İnsan resurslarının idarə olunması', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (33, 10, 'Maliyyə şöbəsi', 'MŞ', 'Maliyyə və mühasibat', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (34, 10, 'Təsərrüfat və texniki xidmət şöbəsi', 'TTX', 'Təsərrüfat və texniki xidmət', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (35, 10, 'Satınalmalar şöbəsi', 'SŞ', 'Satınalmaların təşkili', NULL, NULL, true);
INSERT INTO struktur.shobeler (id, merkez_id, ad, qisa_ad, tesvir, telefon, email, aktiv) VALUES (36, 10, 'Ümumi şöbə', 'ÜŞ', 'Ümumi (dəftərxana) işləri', NULL, NULL, true);


--
-- Data for Name: vezifeler; Type: TABLE DATA; Schema: struktur; Owner: -
--

INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (1, 'Direktor', 1, 'İnstitutun ali rəhbəri');
INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (2, 'Direktor müavini', 2, 'İnstitutun fəaliyyət sahələri üzrə müavinlər');
INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (3, 'Elmi katib', 3, 'Elmi Şuranın katibi');
INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (4, 'Mərkəz rəhbəri', 3, 'Mərkəzin rəhbəri');
INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (5, 'Şöbə müdiri', 4, 'Şöbənin müdiri');
INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (6, 'Baş mütəxəssis', 5, 'Baş mütəxəssis');
INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (7, 'Aparıcı mütəxəssis', 6, 'Aparıcı mütəxəssis');
INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (8, 'Mütəxəssis', 7, 'Mütəxəssis');
INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (9, 'Böyük elmi işçi', 5, 'Böyük elmi işçi');
INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (10, 'Elmi işçi', 6, 'Elmi işçi');
INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (11, 'Baş mühasib', 4, 'Baş mühasib');
INSERT INTO struktur.vezifeler (id, ad, seviyye, tesvir) VALUES (12, 'Mühasib', 6, 'Mühasib');


--
-- Data for Name: emekdaslar; Type: TABLE DATA; Schema: kadrlar; Owner: -
--

INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (1, 'Elnur', 'Əliyev', 'Qəzənfər', 1, '1978-04-12', 1, NULL, 1, 'elnur.eliyev@arti.edu.az', '+994 50 211 01 01', 1, 3, 2, '2018-11-14', 3500.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (2, 'Aydın', 'Əhmədov', 'Əhəd', 1, '1981-09-25', 2, 1, 2, 'aydin.ehmedov@arti.edu.az', '+994 50 211 01 02', 1, 3, 2, '2019-02-01', 2800.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (3, 'Fuad', 'Qarayev', 'Abdurahman', 1, '1979-06-30', 2, 8, 3, 'fuad.qarayev@arti.edu.az', '+994 50 211 01 03', 1, 3, 2, '2019-02-01', 2800.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (4, 'İlham', 'Cavadov', 'Ağaqardaş', 1, '1983-01-18', 2, 14, 4, 'ilham.cavadov@arti.edu.az', '+994 50 211 01 04', 1, 3, NULL, '2020-05-10', 2800.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (5, 'Kənan', 'Kərimli', 'Lətif', 1, '1985-11-05', 2, 17, 5, 'kenan.kerimli@arti.edu.az', '+994 50 211 01 05', 1, 2, NULL, '2021-03-15', 2600.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (6, 'Tariyel', 'Talıbov', 'İsmayıl', 1, '1969-07-22', 2, 23, 6, 'tariyel.talibov@arti.edu.az', '+994 50 211 01 06', 1, 4, 1, '2018-11-14', 3000.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (7, 'Faiq', 'Şahbazlı', 'Şaban', 1, '1982-03-14', 2, 27, 7, 'faiq.sahbazli@arti.edu.az', '+994 50 211 01 07', 1, 3, NULL, '2020-09-01', 2800.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (11, 'Tural', 'İsmayılov', 'Mübariz', 1, '1986-12-03', 5, 33, 10, 'tural.ismayilov@arti.edu.az', '+994 50 211 01 11', 1, 2, NULL, '2021-05-20', 1900.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (12, 'Sevinc', 'Əliyeva', 'Kamran', 2, '1989-04-16', 6, 32, 10, 'sevinc.eliyevam@arti.edu.az', '+994 50 211 01 12', 1, 2, NULL, '2022-02-03', 1400.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (14, 'Günel', 'Rzayeva', 'Azər', 2, '1992-05-30', 8, 31, 10, 'gunel.rzayeva@arti.edu.az', '+994 50 211 01 14', 1, 1, NULL, '2024-01-17', 1100.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (8, 'Aygün', 'Həsənova', 'Vahid', 2, '1984-10-08', 3, NULL, 1, 'aygun.hesenova@arti.edu.az', '+994 50 211 01 08', 1, 3, 2, '2019-06-01', 2200.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (9, 'Rəşad', 'Məmmədov', 'İlham', 1, '1975-02-19', 4, 1, 2, 'resad.memmedov@arti.edu.az', '+994 50 211 01 09', 1, 4, 1, '2018-11-14', 2400.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (10, 'Nərminə', 'Quliyeva', 'Fikrət', 2, '1983-08-27', 4, 23, 6, 'nermine.quliyeva@arti.edu.az', '+994 50 211 01 10', 1, 3, 2, '2020-01-10', 2400.00, true, '2026-09-09 15:21:33.86008+04');
INSERT INTO kadrlar.emekdaslar (id, ad, soyad, ata_adi, cinsiyyet_id, dogum_tarixi, vezife_id, shobe_id, merkez_id, email, telefon, is_status_id, elmi_derece_id, elmi_ad_id, ise_baslama, maas, aktiv, yaradilma) VALUES (13, 'Elçin', 'Babayev', 'Sərvər', 1, '1990-09-11', 7, NULL, 9, 'elcin.babayev@arti.edu.az', '+994 50 211 01 13', 1, 2, NULL, '2023-03-08', 1300.00, true, '2026-09-09 15:21:33.86008+04');


--
-- Data for Name: doktorantlar; Type: TABLE DATA; Schema: elm; Owner: -
--

INSERT INTO elm.doktorantlar (id, proqram_id, ad, soyad, ata_adi, status, qebul_tarixi, rehber_id, mudafie_tarixi, qeyd) VALUES (1, 1, 'Nigar', 'Hüseynli', 'Rəşid', 'tehsil alir', '2024-10-01', 9, NULL, NULL);
INSERT INTO elm.doktorantlar (id, proqram_id, ad, soyad, ata_adi, status, qebul_tarixi, rehber_id, mudafie_tarixi, qeyd) VALUES (2, 2, 'Murad', 'Ələkbərov', 'Vüqar', 'tehsil alir', '2024-10-01', 6, NULL, NULL);
INSERT INTO elm.doktorantlar (id, proqram_id, ad, soyad, ata_adi, status, qebul_tarixi, rehber_id, mudafie_tarixi, qeyd) VALUES (3, 3, 'Leyla', 'Süleymanova', 'Fərid', 'tehsil alir', '2025-10-01', 4, NULL, NULL);
INSERT INTO elm.doktorantlar (id, proqram_id, ad, soyad, ata_adi, status, qebul_tarixi, rehber_id, mudafie_tarixi, qeyd) VALUES (4, 4, 'Kamran', 'Nəbiyev', 'Zaur', 'tehsil alir', '2025-10-01', 6, NULL, NULL);
INSERT INTO elm.doktorantlar (id, proqram_id, ad, soyad, ata_adi, status, qebul_tarixi, rehber_id, mudafie_tarixi, qeyd) VALUES (5, 5, 'Aynur', 'Məmmədova', 'Şakir', 'mudafie', '2023-10-01', 3, NULL, NULL);
INSERT INTO elm.doktorantlar (id, proqram_id, ad, soyad, ata_adi, status, qebul_tarixi, rehber_id, mudafie_tarixi, qeyd) VALUES (6, 6, 'Rəvan', 'Qasımov', 'İlqar', 'tehsil alir', '2026-10-01', 8, NULL, NULL);
INSERT INTO elm.doktorantlar (id, proqram_id, ad, soyad, ata_adi, status, qebul_tarixi, rehber_id, mudafie_tarixi, qeyd) VALUES (7, 7, 'Sevda', 'Əliyeva', 'Natiq', 'mudafie', '2022-10-01', 9, NULL, NULL);
INSERT INTO elm.doktorantlar (id, proqram_id, ad, soyad, ata_adi, status, qebul_tarixi, rehber_id, mudafie_tarixi, qeyd) VALUES (8, 2, 'Elşən', 'Cəfərov', 'Bəhram', 'mezun', '2021-10-01', 6, NULL, NULL);
INSERT INTO elm.doktorantlar (id, proqram_id, ad, soyad, ata_adi, status, qebul_tarixi, rehber_id, mudafie_tarixi, qeyd) VALUES (9, 5, 'Zəhra', 'Həsənova', 'Mübariz', 'tehsil alir', '2026-10-01', 3, NULL, NULL);
INSERT INTO elm.doktorantlar (id, proqram_id, ad, soyad, ata_adi, status, qebul_tarixi, rehber_id, mudafie_tarixi, qeyd) VALUES (10, 8, 'Tərlan', 'İbrahimov', 'Oqtay', 'mudafie', '2021-10-01', 6, NULL, NULL);


--
-- Data for Name: elmi_tedbirler; Type: TABLE DATA; Schema: elm; Owner: -
--

INSERT INTO elm.elmi_tedbirler (id, ad, tip, tarix, yer, istirakci_sayi, qeyd) VALUES (1, 'Təhsil islahatları: nəticələr və perspektivlər', 'konfrans', '2026-03-14', 'ARTİ iclas zalı', 120, NULL);
INSERT INTO elm.elmi_tedbirler (id, ad, tip, tarix, yer, istirakci_sayi, qeyd) VALUES (2, 'Kurikulumun qiymətləndirilməsi seminarı', 'seminar', '2026-05-22', 'ARTİ iclas zalı', 60, NULL);
INSERT INTO elm.elmi_tedbirler (id, ad, tip, tarix, yer, istirakci_sayi, qeyd) VALUES (3, 'PISA 2025 hazırlıq simpoziumu', 'simpozium', '2026-09-10', 'ARTİ iclas zalı', 90, NULL);
INSERT INTO elm.elmi_tedbirler (id, ad, tip, tarix, yer, istirakci_sayi, qeyd) VALUES (4, 'İnklüziv təhsil üzrə dəyirmi masa', 'dəyirmi masa', '2026-04-05', 'ARTİ iclas zalı', 40, NULL);
INSERT INTO elm.elmi_tedbirler (id, ad, tip, tarix, yer, istirakci_sayi, qeyd) VALUES (5, 'Rəqəmsal təhsil konfransı', 'konfrans', '2026-11-20', 'Təhsil Texnologiyaları Mərkəzi', 150, NULL);
INSERT INTO elm.elmi_tedbirler (id, ad, tip, tarix, yer, istirakci_sayi, qeyd) VALUES (6, 'Müəllim hazırlığı üzrə seminar', 'seminar', '2026-02-12', 'ARTİ iclas zalı', 55, NULL);
INSERT INTO elm.elmi_tedbirler (id, ad, tip, tarix, yer, istirakci_sayi, qeyd) VALUES (7, 'Gənc tədqiqatçıların simpoziumu', 'simpozium', '2026-06-18', 'ARTİ iclas zalı', 80, NULL);
INSERT INTO elm.elmi_tedbirler (id, ad, tip, tarix, yer, istirakci_sayi, qeyd) VALUES (8, 'Doktorantura təhsili üzrə dəyirmi masa', 'dəyirmi masa', '2026-10-08', 'ARTİ iclas zalı', 35, NULL);
INSERT INTO elm.elmi_tedbirler (id, ad, tip, tarix, yer, istirakci_sayi, qeyd) VALUES (9, 'Beynəlxalq təhsil əməkdaşlığı konfransı', 'konfrans', '2026-12-05', 'ARTİ iclas zalı', 110, NULL);
INSERT INTO elm.elmi_tedbirler (id, ad, tip, tarix, yer, istirakci_sayi, qeyd) VALUES (10, 'Elmi nəşrlərin keyfiyyəti üzrə seminar', 'seminar', '2026-01-25', 'ARTİ iclas zalı', 45, NULL);


--
-- Data for Name: jurnallar; Type: TABLE DATA; Schema: elm; Owner: -
--

INSERT INTO elm.jurnallar (id, ad, tip, issn, tezlik, tesvir) VALUES (1, 'Azərbaycan Məktəbi', 'metodik', '0134-3289', 'aylıq', 'Pedaqoji-metodik jurnal (707+ say)');
INSERT INTO elm.jurnallar (id, ad, tip, issn, tezlik, tesvir) VALUES (2, 'Elmi əsərlər', 'elmi', '2306-1188', 'rüblük', 'Elmi-pedaqoji tədqiqatlar toplusu');
INSERT INTO elm.jurnallar (id, ad, tip, issn, tezlik, tesvir) VALUES (3, 'Pedaqoji fikir', 'elmi', '2306-1196', 'rüblük', 'Pedaqogika üzrə elmi məqalələr');
INSERT INTO elm.jurnallar (id, ad, tip, issn, tezlik, tesvir) VALUES (4, 'Təhsildə innovasiyalar', 'metodik', '2306-1200', 'rüblük', 'Təhsil innovasiyaları');
INSERT INTO elm.jurnallar (id, ad, tip, issn, tezlik, tesvir) VALUES (5, 'Kurikulum', 'elmi', '2306-1218', 'rüblük', 'Kurikulum və standartlar');
INSERT INTO elm.jurnallar (id, ad, tip, issn, tezlik, tesvir) VALUES (6, 'Psixologiya və təhsil', 'elmi', '2306-1226', 'illik', 'Təhsil psixologiyası');
INSERT INTO elm.jurnallar (id, ad, tip, issn, tezlik, tesvir) VALUES (7, 'Rəqəmsal təhsil', 'metodik', '2306-1234', 'illik', 'Rəqəmsal təhsil texnologiyaları');
INSERT INTO elm.jurnallar (id, ad, tip, issn, tezlik, tesvir) VALUES (8, 'Dil və ədəbiyyat tədrisi', 'metodik', '2306-1242', 'rüblük', 'Dil fənlərinin tədrisi metodikası');


--
-- Data for Name: meqaleler; Type: TABLE DATA; Schema: elm; Owner: -
--

INSERT INTO elm.meqaleler (id, jurnal_id, basliq, muellifler, il, cild, sehife, doi, qeyd) VALUES (1, 2, 'Kurikulum islahatlarının nəticələri', 'Quliyeva N., Qarayev F.', 2026, 'Cild 92', '5-18', NULL, NULL);
INSERT INTO elm.meqaleler (id, jurnal_id, basliq, muellifler, il, cild, sehife, doi, qeyd) VALUES (2, 1, 'Aktiv təlim metodlarının tətbiqi', 'Qarayev F.', 2026, 'Say 707', '12-20', NULL, NULL);
INSERT INTO elm.meqaleler (id, jurnal_id, basliq, muellifler, il, cild, sehife, doi, qeyd) VALUES (3, 2, 'Təhsildə qiymətləndirmə çərçivəsi', 'Quliyeva N.', 2025, 'Cild 91', '21-34', NULL, NULL);
INSERT INTO elm.meqaleler (id, jurnal_id, basliq, muellifler, il, cild, sehife, doi, qeyd) VALUES (4, 3, 'Şagird motivasiyasının psixoloji əsasları', 'Cavadov İ.', 2026, 'Cild 4', '40-52', NULL, NULL);
INSERT INTO elm.meqaleler (id, jurnal_id, basliq, muellifler, il, cild, sehife, doi, qeyd) VALUES (5, 5, 'Kurikulumun qiymətləndirilməsi modeli', 'Məmmədov R.', 2026, 'Cild 2', '8-19', NULL, NULL);
INSERT INTO elm.meqaleler (id, jurnal_id, basliq, muellifler, il, cild, sehife, doi, qeyd) VALUES (6, 6, 'İnklüziv təhsildə müəllim rolu', 'Həsənova A.', 2026, 'Cild 1', '33-45', NULL, NULL);
INSERT INTO elm.meqaleler (id, jurnal_id, basliq, muellifler, il, cild, sehife, doi, qeyd) VALUES (7, 7, 'E-learning platformaların müqayisəsi', 'Babayev E.', 2026, 'Cild 1', '15-27', NULL, NULL);
INSERT INTO elm.meqaleler (id, jurnal_id, basliq, muellifler, il, cild, sehife, doi, qeyd) VALUES (8, 8, 'Azərbaycan dili fənninin yeni kurikulumu', 'Kərimli K.', 2025, 'Cild 3', '50-61', NULL, NULL);
INSERT INTO elm.meqaleler (id, jurnal_id, basliq, muellifler, il, cild, sehife, doi, qeyd) VALUES (9, 2, 'Təhsil iqtisadiyyatının müasir problemləri', 'Talıbov T.', 2025, 'Cild 90', '70-82', NULL, NULL);
INSERT INTO elm.meqaleler (id, jurnal_id, basliq, muellifler, il, cild, sehife, doi, qeyd) VALUES (10, 4, 'Rəqəmsal məktəb konsepsiyası', 'Şahbazlı F.', 2026, 'Cild 5', '25-36', NULL, NULL);


--
-- Data for Name: neshrler; Type: TABLE DATA; Schema: elm; Owner: -
--

INSERT INTO elm.neshrler (id, ad, tip, muellif, il, isbn, say, qeyd) VALUES (1, 'Təhsilin nəzəriyyəsi və tarixi (dərslik)', 'dərslik', 'Məmmədov R.', 2025, '978-9952-000-01', 500, NULL);
INSERT INTO elm.neshrler (id, ad, tip, muellif, il, isbn, say, qeyd) VALUES (2, 'Müasir təlim metodları', 'vesait', 'Qarayev F.', 2026, '978-9952-000-02', 800, NULL);
INSERT INTO elm.neshrler (id, ad, tip, muellif, il, isbn, say, qeyd) VALUES (3, 'Kurikulumun əsasları', 'dərslik', 'Quliyeva N.', 2025, '978-9952-000-03', 600, NULL);
INSERT INTO elm.neshrler (id, ad, tip, muellif, il, isbn, say, qeyd) VALUES (4, 'İnklüziv təhsilə giriş', 'vesait', 'Həsənova A.', 2026, '978-9952-000-04', 400, NULL);
INSERT INTO elm.neshrler (id, ad, tip, muellif, il, isbn, say, qeyd) VALUES (5, 'PISA 2022 nəticələrinin təhlili', 'hesabat', 'Qiymətləndirmə qrupu', 2026, NULL, 200, NULL);
INSERT INTO elm.neshrler (id, ad, tip, muellif, il, isbn, say, qeyd) VALUES (6, 'Müəllim sertifikasiyasına hazırlıq', 'vesait', 'Əhmədov A.', 2026, '978-9952-000-05', 1000, NULL);
INSERT INTO elm.neshrler (id, ad, tip, muellif, il, isbn, say, qeyd) VALUES (7, 'Azərbaycan təhsil tarixi (1900-2020)', 'kitab', 'Talıbov T.', 2024, '978-9952-000-06', 300, NULL);
INSERT INTO elm.neshrler (id, ad, tip, muellif, il, isbn, say, qeyd) VALUES (8, 'Rəqəmsal təhsil resursları', 'vesait', 'Babayev E.', 2026, '978-9952-000-07', 450, NULL);
INSERT INTO elm.neshrler (id, ad, tip, muellif, il, isbn, say, qeyd) VALUES (9, 'STEAM təhsilinə yanaşmalar', 'vesait', 'İsmayılov T.', 2026, '978-9952-000-08', 350, NULL);
INSERT INTO elm.neshrler (id, ad, tip, muellif, il, isbn, say, qeyd) VALUES (10, 'Təhsil iqtisadiyyatı (monoqrafiya)', 'kitab', 'Talıbov T.', 2025, '978-9952-000-09', 250, NULL);


--
-- Data for Name: tedqiqat_istiqametleri; Type: TABLE DATA; Schema: elm; Owner: -
--

INSERT INTO elm.tedqiqat_istiqametleri (id, ad, tesvir, aktiv) VALUES (1, 'Təhsilin nəzəriyyəsi', 'Təhsilin fəlsəfi və nəzəri əsasları', true);
INSERT INTO elm.tedqiqat_istiqametleri (id, ad, tesvir, aktiv) VALUES (2, 'Təhsilin tarixi', 'Azərbaycan və dünya təhsil tarixi', true);
INSERT INTO elm.tedqiqat_istiqametleri (id, ad, tesvir, aktiv) VALUES (3, 'Təhsilin iqtisadiyyatı', 'Təhsilin maliyyələşdirilməsi və səmərəliliyi', true);
INSERT INTO elm.tedqiqat_istiqametleri (id, ad, tesvir, aktiv) VALUES (4, 'Təlimin metodikası', 'Fənlərin tədrisi metodikaları', true);
INSERT INTO elm.tedqiqat_istiqametleri (id, ad, tesvir, aktiv) VALUES (5, 'Təhsil psixologiyası', 'Təlim və inkişaf psixologiyası', true);
INSERT INTO elm.tedqiqat_istiqametleri (id, ad, tesvir, aktiv) VALUES (6, 'İnklüziv təhsil', 'Xüsusi təlim ehtiyaclı uşaqların təhsili', true);
INSERT INTO elm.tedqiqat_istiqametleri (id, ad, tesvir, aktiv) VALUES (7, 'Kurikulum nəzəriyyəsi', 'Təhsil proqramlarının nəzəriyyəsi', true);
INSERT INTO elm.tedqiqat_istiqametleri (id, ad, tesvir, aktiv) VALUES (8, 'Qiymətləndirmə nəzəriyyəsi', 'Nailiyyətlərin ölçülməsi və qiymətləndirmə', true);
INSERT INTO elm.tedqiqat_istiqametleri (id, ad, tesvir, aktiv) VALUES (9, 'Rəqəmsal təhsil', 'E-learning və rəqəmsal texnologiyalar', true);
INSERT INTO elm.tedqiqat_istiqametleri (id, ad, tesvir, aktiv) VALUES (10, 'Müəllim hazırlığı', 'Müəllimlərin peşəkar inkişafı', true);


--
-- Data for Name: tedqiqat_layiheleri; Type: TABLE DATA; Schema: elm; Owner: -
--

INSERT INTO elm.tedqiqat_layiheleri (id, istiqamet_id, ad, tesvir, status, rehber_id, baslama_tarixi, bitme_tarixi, qeyd) VALUES (11, 1, 'Yeni tədqiqat layihəsi', NULL, 'davam edir', NULL, NULL, NULL, NULL);
INSERT INTO elm.tedqiqat_layiheleri (id, istiqamet_id, ad, tesvir, status, rehber_id, baslama_tarixi, bitme_tarixi, qeyd) VALUES (1, 1, 'Təhsil fəlsəfəsinin müasir paradiqmaları', 'Təhsil nəzəriyyəsinin müasir istiqamətləri', 'davam edir', 9, '2026-01-15', '2027-12-30', NULL);
INSERT INTO elm.tedqiqat_layiheleri (id, istiqamet_id, ad, tesvir, status, rehber_id, baslama_tarixi, bitme_tarixi, qeyd) VALUES (2, 2, 'Azərbaycan təhsil tarixinin mərhələləri', 'Təhsil tarixinin dövrləşdirilməsi', 'tamamlanib', 9, '2025-01-10', '2026-06-30', NULL);
INSERT INTO elm.tedqiqat_layiheleri (id, istiqamet_id, ad, tesvir, status, rehber_id, baslama_tarixi, bitme_tarixi, qeyd) VALUES (3, 3, 'Təhsilin səmərəliliyinin ölçülməsi', 'Təhsilə qoyulan sərmayənin gəliri', 'davam edir', 6, '2026-03-01', '2027-03-01', NULL);
INSERT INTO elm.tedqiqat_layiheleri (id, istiqamet_id, ad, tesvir, status, rehber_id, baslama_tarixi, bitme_tarixi, qeyd) VALUES (4, 4, 'Yeni kurikulumda təlim metodikaları', 'Aktiv təlim metodlarının tətbiqi', 'tamamlanib', 3, '2025-09-01', '2026-05-31', NULL);
INSERT INTO elm.tedqiqat_layiheleri (id, istiqamet_id, ad, tesvir, status, rehber_id, baslama_tarixi, bitme_tarixi, qeyd) VALUES (5, 5, 'Şagirdlərin təlim motivasiyası', 'Motivasiya amillərinin tədqiqi', 'davam edir', 4, '2026-05-10', '2027-05-10', NULL);
INSERT INTO elm.tedqiqat_layiheleri (id, istiqamet_id, ad, tesvir, status, rehber_id, baslama_tarixi, bitme_tarixi, qeyd) VALUES (6, 6, 'İnklüziv təhsilin regionlarda vəziyyəti', 'İnklüziv təhsilin monitorinqi', 'planlanir', 10, '2027-02-01', '2028-02-01', NULL);
INSERT INTO elm.tedqiqat_layiheleri (id, istiqamet_id, ad, tesvir, status, rehber_id, baslama_tarixi, bitme_tarixi, qeyd) VALUES (7, 7, 'Kurikulumun qiymətləndirilməsi modeli', 'Kurikulum effektivliyinin ölçülməsi', 'davam edir', 10, '2026-06-01', '2027-06-01', NULL);
INSERT INTO elm.tedqiqat_layiheleri (id, istiqamet_id, ad, tesvir, status, rehber_id, baslama_tarixi, bitme_tarixi, qeyd) VALUES (8, 8, 'Milli qiymətləndirmə çərçivəsi', 'Qiymətləndirmə standartlarının qurulması', 'tamamlanib', 10, '2024-09-01', '2025-12-31', NULL);
INSERT INTO elm.tedqiqat_layiheleri (id, istiqamet_id, ad, tesvir, status, rehber_id, baslama_tarixi, bitme_tarixi, qeyd) VALUES (9, 9, 'Rəqəmsal təhsil resurslarının effektivliyi', 'E-learning platformaların təhlili', 'davam edir', 13, '2026-04-01', '2027-04-01', NULL);
INSERT INTO elm.tedqiqat_layiheleri (id, istiqamet_id, ad, tesvir, status, rehber_id, baslama_tarixi, bitme_tarixi, qeyd) VALUES (10, 10, 'Müəllim peşəkar inkişafının modelləşdirilməsi', 'Sertifikasiyanın təsiri', 'planlanir', 8, '2027-03-01', '2028-03-01', NULL);


--
-- Data for Name: is_tecrubesi; Type: TABLE DATA; Schema: kadrlar; Owner: -
--

INSERT INTO kadrlar.is_tecrubesi (id, emekdas_id, is_yeri, vezife, baslama_tarixi, bitme_tarixi, qeyd) VALUES (1, 1, 'Bakı Dövlət Universiteti', 'Baş müəllim', '2005-09-01', '2018-10-31', NULL);
INSERT INTO kadrlar.is_tecrubesi (id, emekdas_id, is_yeri, vezife, baslama_tarixi, bitme_tarixi, qeyd) VALUES (2, 2, 'Elm və Təhsil Nazirliyi', 'Şöbə müdiri', '2011-02-01', '2019-01-31', NULL);
INSERT INTO kadrlar.is_tecrubesi (id, emekdas_id, is_yeri, vezife, baslama_tarixi, bitme_tarixi, qeyd) VALUES (3, 3, 'Azərbaycan Dövlət Pedaqoji Universiteti', 'Dosent', '2010-09-01', '2019-01-31', NULL);
INSERT INTO kadrlar.is_tecrubesi (id, emekdas_id, is_yeri, vezife, baslama_tarixi, bitme_tarixi, qeyd) VALUES (4, 6, 'Təhsil Problemləri İnstitutu', 'Şöbə müdiri', '2007-01-10', '2018-11-13', NULL);
INSERT INTO kadrlar.is_tecrubesi (id, emekdas_id, is_yeri, vezife, baslama_tarixi, bitme_tarixi, qeyd) VALUES (5, 9, 'AMEA İqtisadiyyat İnstitutu', 'Elmi işçi', '2002-09-01', '2018-11-13', NULL);
INSERT INTO kadrlar.is_tecrubesi (id, emekdas_id, is_yeri, vezife, baslama_tarixi, bitme_tarixi, qeyd) VALUES (6, 10, 'Dövlət İmtahan Mərkəzi', 'Baş mütəxəssis', '2014-03-01', '2020-01-09', NULL);
INSERT INTO kadrlar.is_tecrubesi (id, emekdas_id, is_yeri, vezife, baslama_tarixi, bitme_tarixi, qeyd) VALUES (7, 11, 'Maliyyə Nazirliyi', 'Mühasib', '2013-07-01', '2021-05-19', NULL);
INSERT INTO kadrlar.is_tecrubesi (id, emekdas_id, is_yeri, vezife, baslama_tarixi, bitme_tarixi, qeyd) VALUES (8, 12, 'Özəl təlim şirkəti', 'HR mütəxəssisi', '2018-10-01', '2022-02-02', NULL);
INSERT INTO kadrlar.is_tecrubesi (id, emekdas_id, is_yeri, vezife, baslama_tarixi, bitme_tarixi, qeyd) VALUES (9, 14, 'Media agentliyi', 'Redaktor', '2021-06-01', '2024-01-16', NULL);


--
-- Data for Name: istifadeciler; Type: TABLE DATA; Schema: kadrlar; Owner: -
--

INSERT INTO kadrlar.istifadeciler (id, email, parol_hash, ad_soyad, rol, emekdas_id, aktiv, yaradilma) VALUES (2, 'admin@arti.edu.az', '$2b$10$oIesQsaJ4ahBc0vjhaRpN.xkamY6eC.SH2byHZThjU8YmVm5UMsOq', 'Elnur Əliyev', 'admin', NULL, true, '2026-09-09 17:23:13.495759+04');
INSERT INTO kadrlar.istifadeciler (id, email, parol_hash, ad_soyad, rol, emekdas_id, aktiv, yaradilma) VALUES (3, 'muhendis@arti.edu.az', '$2b$10$oIesQsaJ4ahBc0vjhaRpN.xkamY6eC.SH2byHZThjU8YmVm5UMsOq', 'Rəşad Məmmədov', 'muhendis', NULL, true, '2026-09-09 17:23:13.498814+04');
INSERT INTO kadrlar.istifadeciler (id, email, parol_hash, ad_soyad, rol, emekdas_id, aktiv, yaradilma) VALUES (4, 'maliyyeci@arti.edu.az', '$2b$10$oIesQsaJ4ahBc0vjhaRpN.xkamY6eC.SH2byHZThjU8YmVm5UMsOq', 'Tural İsmayılov', 'maliyyeci', NULL, true, '2026-09-09 17:23:13.499434+04');
INSERT INTO kadrlar.istifadeciler (id, email, parol_hash, ad_soyad, rol, emekdas_id, aktiv, yaradilma) VALUES (5, 'baxici@arti.edu.az', '$2b$10$oIesQsaJ4ahBc0vjhaRpN.xkamY6eC.SH2byHZThjU8YmVm5UMsOq', 'Günel Rzayeva', 'baxici', NULL, true, '2026-09-09 17:23:13.499922+04');


--
-- Data for Name: mezuniyyetler; Type: TABLE DATA; Schema: kadrlar; Owner: -
--

INSERT INTO kadrlar.mezuniyyetler (id, emekdas_id, mezuniyyet_tipi, baslama_tarixi, bitme_tarixi, gun_sayi, status, qeyd) VALUES (1, 1, 'illik', '2026-07-01', '2026-07-28', 28, 'tesdiqlendi', NULL);
INSERT INTO kadrlar.mezuniyyetler (id, emekdas_id, mezuniyyet_tipi, baslama_tarixi, bitme_tarixi, gun_sayi, status, qeyd) VALUES (2, 2, 'illik', '2026-07-15', '2026-08-11', 28, 'tesdiqlendi', NULL);
INSERT INTO kadrlar.mezuniyyetler (id, emekdas_id, mezuniyyet_tipi, baslama_tarixi, bitme_tarixi, gun_sayi, status, qeyd) VALUES (3, 5, 'xestelik', '2026-03-05', '2026-03-12', 8, 'tesdiqlendi', NULL);
INSERT INTO kadrlar.mezuniyyetler (id, emekdas_id, mezuniyyet_tipi, baslama_tarixi, bitme_tarixi, gun_sayi, status, qeyd) VALUES (4, 8, 'tehsil', '2026-09-02', '2026-09-15', 14, 'tesdiqlendi', NULL);
INSERT INTO kadrlar.mezuniyyetler (id, emekdas_id, mezuniyyet_tipi, baslama_tarixi, bitme_tarixi, gun_sayi, status, qeyd) VALUES (5, 9, 'illik', '2026-08-01', '2026-08-28', 28, 'tesdiqlendi', NULL);
INSERT INTO kadrlar.mezuniyyetler (id, emekdas_id, mezuniyyet_tipi, baslama_tarixi, bitme_tarixi, gun_sayi, status, qeyd) VALUES (6, 11, 'illik', '2026-06-10', '2026-06-23', 14, 'tesdiqlendi', NULL);
INSERT INTO kadrlar.mezuniyyetler (id, emekdas_id, mezuniyyet_tipi, baslama_tarixi, bitme_tarixi, gun_sayi, status, qeyd) VALUES (7, 12, 'sosial', '2026-10-01', '2026-10-14', 14, 'tesdiqlendi', NULL);
INSERT INTO kadrlar.mezuniyyetler (id, emekdas_id, mezuniyyet_tipi, baslama_tarixi, bitme_tarixi, gun_sayi, status, qeyd) VALUES (8, 14, 'illik', '2026-08-05', '2026-08-18', 14, 'gozlemede', NULL);


--
-- Data for Name: vezife_teyinatlari; Type: TABLE DATA; Schema: kadrlar; Owner: -
--

INSERT INTO kadrlar.vezife_teyinatlari (id, emekdas_id, vezife_id, shobe_id, "təyinat_tarixi", emr_no, status, qeyd) VALUES (1, 1, 1, NULL, '2018-11-14', 'K-2016-001', 'qüvvədədir', NULL);
INSERT INTO kadrlar.vezife_teyinatlari (id, emekdas_id, vezife_id, shobe_id, "təyinat_tarixi", emr_no, status, qeyd) VALUES (2, 2, 2, NULL, '2019-02-01', 'K-2017-010', 'qüvvədədir', NULL);
INSERT INTO kadrlar.vezife_teyinatlari (id, emekdas_id, vezife_id, shobe_id, "təyinat_tarixi", emr_no, status, qeyd) VALUES (3, 3, 2, NULL, '2019-02-01', 'K-2017-011', 'qüvvədədir', NULL);
INSERT INTO kadrlar.vezife_teyinatlari (id, emekdas_id, vezife_id, shobe_id, "təyinat_tarixi", emr_no, status, qeyd) VALUES (4, 8, 3, NULL, '2019-06-01', 'K-2017-040', 'qüvvədədir', NULL);
INSERT INTO kadrlar.vezife_teyinatlari (id, emekdas_id, vezife_id, shobe_id, "təyinat_tarixi", emr_no, status, qeyd) VALUES (5, 9, 4, NULL, '2018-11-14', 'K-2016-005', 'qüvvədədir', NULL);
INSERT INTO kadrlar.vezife_teyinatlari (id, emekdas_id, vezife_id, shobe_id, "təyinat_tarixi", emr_no, status, qeyd) VALUES (6, 11, 5, 33, '2021-05-20', 'K-2019-088', 'qüvvədədir', NULL);
INSERT INTO kadrlar.vezife_teyinatlari (id, emekdas_id, vezife_id, shobe_id, "təyinat_tarixi", emr_no, status, qeyd) VALUES (7, 12, 6, 32, '2022-02-03', 'K-2020-012', 'qüvvədədir', NULL);
INSERT INTO kadrlar.vezife_teyinatlari (id, emekdas_id, vezife_id, shobe_id, "təyinat_tarixi", emr_no, status, qeyd) VALUES (8, 13, 7, NULL, '2023-03-08', 'K-2021-030', 'qüvvədədir', NULL);


--
-- Data for Name: aktivler; Type: TABLE DATA; Schema: logistika; Owner: -
--

INSERT INTO logistika.aktivler (id, ad, tip, veziyyet, deyer, alinma_tarixi, qeyd) VALUES (1, 'Server (HP ProLiant)', 'avadanlıq', 'yaxşı', 45000.00, '2024-05-10', NULL);
INSERT INTO logistika.aktivler (id, ad, tip, veziyyet, deyer, alinma_tarixi, qeyd) VALUES (2, 'İş stansiyası kompyuterləri', 'kompyuter', 'yaxşı', 180000.00, '2026-02-15', NULL);
INSERT INTO logistika.aktivler (id, ad, tip, veziyyet, deyer, alinma_tarixi, qeyd) VALUES (3, 'Ofis mebeli dəsti', 'mebel', 'yaxşı', 65000.00, '2026-04-20', NULL);
INSERT INTO logistika.aktivler (id, ad, tip, veziyyet, deyer, alinma_tarixi, qeyd) VALUES (4, 'Proyektorlar (10 ədəd)', 'avadanlıq', 'yaxşı', 25000.00, '2025-09-12', NULL);
INSERT INTO logistika.aktivler (id, ad, tip, veziyyet, deyer, alinma_tarixi, qeyd) VALUES (5, 'Xidməti avtomobil', 'neqliyyat', 'qənaətbəxş', 30000.00, '2023-06-30', NULL);
INSERT INTO logistika.aktivler (id, ad, tip, veziyyet, deyer, alinma_tarixi, qeyd) VALUES (6, 'Noutbuklar (20 ədəd)', 'kompyuter', 'yaxşı', 50000.00, '2026-07-08', NULL);
INSERT INTO logistika.aktivler (id, ad, tip, veziyyet, deyer, alinma_tarixi, qeyd) VALUES (7, 'Kitabxana rəfləri', 'mebel', 'qənaətbəxş', 8000.00, '2022-03-15', NULL);
INSERT INTO logistika.aktivler (id, ad, tip, veziyyet, deyer, alinma_tarixi, qeyd) VALUES (8, 'Laboratoriya avadanlıqları', 'avadanlıq', 'təmirə ehtiyac', 95000.00, '2021-11-20', NULL);
INSERT INTO logistika.aktivler (id, ad, tip, veziyyet, deyer, alinma_tarixi, qeyd) VALUES (9, 'Kondisionerlər (15 ədəd)', 'avadanlıq', 'yaxşı', 30000.00, '2025-07-01', NULL);
INSERT INTO logistika.aktivler (id, ad, tip, veziyyet, deyer, alinma_tarixi, qeyd) VALUES (10, 'Skaner və printerlər', 'avadanlıq', 'qənaətbəxş', 15000.00, '2024-12-05', NULL);


--
-- Data for Name: binalar; Type: TABLE DATA; Schema: logistika; Owner: -
--

INSERT INTO logistika.binalar (id, ad, unvan, sahe_m2, mertebe, qeyd) VALUES (1, 'Elmi-pedaqoji tədqiqatlar mərkəzi binası', 'Zərifə Əliyeva 96, Bakı', 1800, 3, NULL);
INSERT INTO logistika.binalar (id, ad, unvan, sahe_m2, mertebe, qeyd) VALUES (2, 'Təhsilverənlərin peşəkar inkişafı binası', 'Mir Cəlal Paşayev 71, Bakı', 1500, 3, NULL);
INSERT INTO logistika.binalar (id, ad, unvan, sahe_m2, mertebe, qeyd) VALUES (3, 'Təhsildə məzmun və qiymətləndirmə binası', 'Afiyəddin Cəlilov 86, Bakı', 2000, 4, NULL);
INSERT INTO logistika.binalar (id, ad, unvan, sahe_m2, mertebe, qeyd) VALUES (4, 'Təhsil texnologiyaları mərkəzi binası', 'Fətəli Xan Xoyski 109, Bakı', 1200, 2, NULL);
INSERT INTO logistika.binalar (id, ad, unvan, sahe_m2, mertebe, qeyd) VALUES (5, 'Tədris resursları mərkəzi binası', 'Afiyəddin Cəlilov 86, Bakı', 900, 2, NULL);
INSERT INTO logistika.binalar (id, ad, unvan, sahe_m2, mertebe, qeyd) VALUES (6, 'Elmi kitabxana binası', 'Zərifə Əliyeva 96, Bakı', 400, 1, NULL);
INSERT INTO logistika.binalar (id, ad, unvan, sahe_m2, mertebe, qeyd) VALUES (7, 'İclas və konfrans zalı', 'Zərifə Əliyeva 96, Bakı', 350, 1, NULL);
INSERT INTO logistika.binalar (id, ad, unvan, sahe_m2, mertebe, qeyd) VALUES (8, 'Arxiv və anbar binası', 'Mir Cəlal Paşayev 71, Bakı', 250, 1, NULL);


--
-- Data for Name: it_sistemleri; Type: TABLE DATA; Schema: logistika; Owner: -
--

INSERT INTO logistika.it_sistemleri (id, ad, tip, tesvir, status, qeyd) VALUES (1, 'arti.edu.az rəsmi saytı', 'sayt', 'İnstitutun rəsmi internet saytı', 'aktiv', NULL);
INSERT INTO logistika.it_sistemleri (id, ad, tip, tesvir, status, qeyd) VALUES (2, 'Elmi jurnal platforması', 'portal', 'Elmi əsərlər jurnalının onlayn sistemi', 'aktiv', NULL);
INSERT INTO logistika.it_sistemleri (id, ad, tip, tesvir, status, qeyd) VALUES (3, 'ERP sistemi (ARTI_ERP)', 'erp', 'İnstitutun ERP sistemi', 'aktiv', NULL);
INSERT INTO logistika.it_sistemleri (id, ad, tip, tesvir, status, qeyd) VALUES (4, 'Doktorantura idarəetmə sistemi', 'portal', 'Doktorantların qeydiyyat sistemi', 'aktiv', NULL);
INSERT INTO logistika.it_sistemleri (id, ad, tip, tesvir, status, qeyd) VALUES (5, 'E-learning platforması', 'portal', 'Onlayn təlim platforması', 'aktiv', NULL);
INSERT INTO logistika.it_sistemleri (id, ad, tip, tesvir, status, qeyd) VALUES (6, 'Sertifikasiya portalı', 'portal', 'Müəllim sertifikasiyası portalı', 'aktiv', NULL);
INSERT INTO logistika.it_sistemleri (id, ad, tip, tesvir, status, qeyd) VALUES (7, 'PostgreSQL verilənlər bazası', 'db', 'Əsas verilənlər bazası serveri', 'aktiv', NULL);
INSERT INTO logistika.it_sistemleri (id, ad, tip, tesvir, status, qeyd) VALUES (8, 'Videoresurs arxivi', 'sayt', 'Videotəlimatlar arxivi', 'aktiv', NULL);


--
-- Data for Name: budce; Type: TABLE DATA; Schema: maliyye; Owner: -
--

INSERT INTO maliyye.budce (id, il, menbe, mebleg, qeyd) VALUES (2, 2026, 'qrant', 350000.00, 'Beynəlxalq qrant layihələri');
INSERT INTO maliyye.budce (id, il, menbe, mebleg, qeyd) VALUES (3, 2026, 'oz gelir', 120000.00, 'Təlim xidmətlərindən gəlir');
INSERT INTO maliyye.budce (id, il, menbe, mebleg, qeyd) VALUES (4, 2025, 'dovlet', 4200000.00, 'Dövlət büdcəsindən əsas maliyyələşmə');
INSERT INTO maliyye.budce (id, il, menbe, mebleg, qeyd) VALUES (5, 2025, 'qrant', 280000.00, 'Beynəlxalq qrant layihələri');
INSERT INTO maliyye.budce (id, il, menbe, mebleg, qeyd) VALUES (6, 2025, 'oz gelir', 105000.00, 'Təlim xidmətlərindən gəlir');
INSERT INTO maliyye.budce (id, il, menbe, mebleg, qeyd) VALUES (7, 2027, 'dovlet', 4800000.00, 'Planlaşdırılan dövlət büdcəsi');
INSERT INTO maliyye.budce (id, il, menbe, mebleg, qeyd) VALUES (8, 2027, 'qrant', 400000.00, 'Planlaşdırılan qrant');
INSERT INTO maliyye.budce (id, il, menbe, mebleg, qeyd) VALUES (9, 2027, 'oz gelir', 150000.00, 'Planlaşdırılan öz gəliri');
INSERT INTO maliyye.budce (id, il, menbe, mebleg, qeyd) VALUES (10, 2024, 'dovlet', 3900000.00, 'Dövlət büdcəsindən əsas maliyyələşmə');
INSERT INTO maliyye.budce (id, il, menbe, mebleg, qeyd) VALUES (1, 2026, 'dovlet', 4500000.00, 'Dövlət büdcəsindən əsas maliyyələşmə');


--
-- Data for Name: maliyye_emeliyyatlari; Type: TABLE DATA; Schema: maliyye; Owner: -
--

INSERT INTO maliyye.maliyye_emeliyyatlari (id, budce_id, nov, mebleg, tarix, tesvir, qeyd) VALUES (1, 1, 'xerc', 850000.00, '2026-03-15', 'Müəllim təlimlərinin təşkili', NULL);
INSERT INTO maliyye.maliyye_emeliyyatlari (id, budce_id, nov, mebleg, tarix, tesvir, qeyd) VALUES (2, 1, 'xerc', 620000.00, '2026-04-20', 'PISA 2025 hazırlıq xərcləri', NULL);
INSERT INTO maliyye.maliyye_emeliyyatlari (id, budce_id, nov, mebleg, tarix, tesvir, qeyd) VALUES (3, 1, 'xerc', 480000.00, '2026-06-10', 'Dərslik ekspertizası xərcləri', NULL);
INSERT INTO maliyye.maliyye_emeliyyatlari (id, budce_id, nov, mebleg, tarix, tesvir, qeyd) VALUES (4, 1, 'xerc', 390000.00, '2026-07-05', 'İT avadanlıqların alınması', NULL);
INSERT INTO maliyye.maliyye_emeliyyatlari (id, budce_id, nov, mebleg, tarix, tesvir, qeyd) VALUES (5, 2, 'gelir', 350000.00, '2026-02-01', 'Beynəlxalq qrantın daxil olması', NULL);
INSERT INTO maliyye.maliyye_emeliyyatlari (id, budce_id, nov, mebleg, tarix, tesvir, qeyd) VALUES (6, 3, 'gelir', 60000.00, '2026-05-12', 'Təlim kurslarından gəlir', NULL);
INSERT INTO maliyye.maliyye_emeliyyatlari (id, budce_id, nov, mebleg, tarix, tesvir, qeyd) VALUES (7, 1, 'xerc', 300000.00, '2026-09-01', 'Elmi tədbirlərin təşkili', NULL);
INSERT INTO maliyye.maliyye_emeliyyatlari (id, budce_id, nov, mebleg, tarix, tesvir, qeyd) VALUES (8, 1, 'xerc', 250000.00, '2026-10-15', 'Nəşrlərin çapı', NULL);
INSERT INTO maliyye.maliyye_emeliyyatlari (id, budce_id, nov, mebleg, tarix, tesvir, qeyd) VALUES (9, 3, 'gelir', 60000.00, '2026-11-01', 'Təlim kurslarından gəlir (II)', NULL);
INSERT INTO maliyye.maliyye_emeliyyatlari (id, budce_id, nov, mebleg, tarix, tesvir, qeyd) VALUES (10, 1, 'xerc', 210000.00, '2026-12-05', 'Beynəlxalq əməkdaşlıq xərcləri', NULL);


--
-- Data for Name: muqavileler; Type: TABLE DATA; Schema: maliyye; Owner: -
--

INSERT INTO maliyye.muqavileler (id, ad, qarsi_teref, mebleg, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (1, 'Dərslik çapı müqaviləsi', '"Azərbaycan Nəşriyyatı" MMC', 90000.00, '2026-03-10', '2026-06-30', 'bitdi', NULL);
INSERT INTO maliyye.muqavileler (id, ad, qarsi_teref, mebleg, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (2, 'İT xidmət müqaviləsi', '"Texnohub" MMC', 55000.00, '2026-05-01', '2027-05-01', 'qüvvədədir', NULL);
INSERT INTO maliyye.muqavileler (id, ad, qarsi_teref, mebleg, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (3, 'Təmir işləri müqaviləsi', '"Tikinti-Servis" MMC', 140000.00, '2026-06-20', '2026-09-30', 'bitdi', NULL);
INSERT INTO maliyye.muqavileler (id, ad, qarsi_teref, mebleg, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (4, 'Təlim xidməti müqaviləsi', '"EduConsult" MMC', 45000.00, '2026-07-01', '2026-12-31', 'qüvvədədir', NULL);
INSERT INTO maliyye.muqavileler (id, ad, qarsi_teref, mebleg, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (5, 'Server təchizatı müqaviləsi', '"NetStore" MMC', 120000.00, '2026-06-01', '2026-08-31', 'bitdi', NULL);
INSERT INTO maliyye.muqavileler (id, ad, qarsi_teref, mebleg, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (6, 'Beynəlxalq qrant sazişi', 'UNICEF', 350000.00, '2026-01-15', '2027-12-31', 'qüvvədədir', NULL);
INSERT INTO maliyye.muqavileler (id, ad, qarsi_teref, mebleg, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (7, 'Nəqliyyat xidməti müqaviləsi', '"AutoFleet" MMC', 30000.00, '2026-09-01', '2026-12-31', 'qüvvədədir', NULL);
INSERT INTO maliyye.muqavileler (id, ad, qarsi_teref, mebleg, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (8, 'Videotəlimat istehsalı', '"MediaProd" MMC', 50000.00, '2026-10-10', '2027-03-31', 'qüvvədədir', NULL);
INSERT INTO maliyye.muqavileler (id, ad, qarsi_teref, mebleg, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (9, 'Kitabxana təchizatı', '"KitabEvi" MMC', 40000.00, '2026-09-25', '2026-11-30', 'legv', NULL);
INSERT INTO maliyye.muqavileler (id, ad, qarsi_teref, mebleg, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (10, 'Laboratoriya avadanlığı', '"LabTech" MMC', 95000.00, '2026-11-05', '2027-02-28', 'qüvvədədir', NULL);


--
-- Data for Name: satinalmalar; Type: TABLE DATA; Schema: maliyye; Owner: -
--

INSERT INTO maliyye.satinalmalar (id, ad, nov, mebleg, tarix, status, qeyd) VALUES (1, 'Kompyuter avadanlıqları', 'mal', 180000.00, '2026-02-10', 'tamamlandi', NULL);
INSERT INTO maliyye.satinalmalar (id, ad, nov, mebleg, tarix, status, qeyd) VALUES (2, 'Çap xidmətləri (dərslik)', 'xidmet', 90000.00, '2026-03-05', 'muqavile', NULL);
INSERT INTO maliyye.satinalmalar (id, ad, nov, mebleg, tarix, status, qeyd) VALUES (3, 'Ofis mebeli', 'mal', 65000.00, '2026-04-18', 'tamamlandi', NULL);
INSERT INTO maliyye.satinalmalar (id, ad, nov, mebleg, tarix, status, qeyd) VALUES (4, 'Server avadanlığı', 'mal', 120000.00, '2026-05-22', 'qiymetlendirme', NULL);
INSERT INTO maliyye.satinalmalar (id, ad, nov, mebleg, tarix, status, qeyd) VALUES (5, 'Təlim zalının təmiri', 'is', 140000.00, '2026-06-15', 'muqavile', NULL);
INSERT INTO maliyye.satinalmalar (id, ad, nov, mebleg, tarix, status, qeyd) VALUES (6, 'Proqram təminatı lisenziyaları', 'mal', 55000.00, '2026-07-08', 'tamamlandi', NULL);
INSERT INTO maliyye.satinalmalar (id, ad, nov, mebleg, tarix, status, qeyd) VALUES (7, 'Nəqliyyat xidmətləri', 'xidmet', 30000.00, '2026-08-12', 'elan', NULL);
INSERT INTO maliyye.satinalmalar (id, ad, nov, mebleg, tarix, status, qeyd) VALUES (8, 'Kitabxana fondunun genişləndirilməsi', 'mal', 40000.00, '2026-09-20', 'elan', NULL);
INSERT INTO maliyye.satinalmalar (id, ad, nov, mebleg, tarix, status, qeyd) VALUES (9, 'Videotəlimat çəkilişləri', 'xidmet', 50000.00, '2026-10-05', 'qiymetlendirme', NULL);
INSERT INTO maliyye.satinalmalar (id, ad, nov, mebleg, tarix, status, qeyd) VALUES (10, 'Laboratoriya avadanlıqları', 'mal', 95000.00, '2026-11-01', 'elan', NULL);


--
-- Data for Name: metodik_vesaitler; Type: TABLE DATA; Schema: metodika; Owner: -
--

INSERT INTO metodika.metodik_vesaitler (id, ad, nov, fenn, il, muellif, say, qeyd) VALUES (1, 'Azərbaycan dili dərslik metodikası', 'vesait', 'Azərbaycan dili', 2026, 'Kərimli K.', 500, NULL);
INSERT INTO metodika.metodik_vesaitler (id, ad, nov, fenn, il, muellif, say, qeyd) VALUES (2, 'Riyaziyyat təlimində aktiv metodlar', 'vesait', 'Riyaziyyat', 2026, 'Quliyeva N.', 600, NULL);
INSERT INTO metodika.metodik_vesaitler (id, ad, nov, fenn, il, muellif, say, qeyd) VALUES (3, 'İnklüziv təhsil üzrə müəllim təlimatı', 'telimat', 'İnklüziv təhsil', 2026, 'Həsənova A.', 400, NULL);
INSERT INTO metodika.metodik_vesaitler (id, ad, nov, fenn, il, muellif, say, qeyd) VALUES (4, 'Müəllim sertifikasiyasına hazırlıq tövsiyələri', 'tovsiye', 'Ümumi', 2026, 'Əhmədov A.', 800, NULL);
INSERT INTO metodika.metodik_vesaitler (id, ad, nov, fenn, il, muellif, say, qeyd) VALUES (5, 'Fizika fənni üzrə laboratoriya işləri', 'vesait', 'Fizika', 2025, 'Babayev E.', 350, NULL);
INSERT INTO metodika.metodik_vesaitler (id, ad, nov, fenn, il, muellif, say, qeyd) VALUES (6, 'İbtidai sinifdə oxu bacarıqları', 'vesait', 'İbtidai təhsil', 2025, 'Qarayev F.', 450, NULL);
INSERT INTO metodika.metodik_vesaitler (id, ad, nov, fenn, il, muellif, say, qeyd) VALUES (7, 'STEAM dərs planları toplusu', 'vesait', 'STEAM', 2026, 'İsmayılov T.', 300, NULL);
INSERT INTO metodika.metodik_vesaitler (id, ad, nov, fenn, il, muellif, say, qeyd) VALUES (8, 'Məktəb rəhbərləri üçün idarəetmə təlimatı', 'telimat', 'İdarəetmə', 2026, 'Talıbov T.', 250, NULL);
INSERT INTO metodika.metodik_vesaitler (id, ad, nov, fenn, il, muellif, say, qeyd) VALUES (9, 'Qiymətləndirmə tapşırıqları bankı', 'vesait', 'Qiymətləndirmə', 2026, 'Quliyeva N.', 500, NULL);
INSERT INTO metodika.metodik_vesaitler (id, ad, nov, fenn, il, muellif, say, qeyd) VALUES (10, 'Kurikulum tətbiqi üzrə tövsiyələr', 'tovsiye', 'Kurikulum', 2026, 'Məmmədov R.', 400, NULL);


--
-- Data for Name: metodik_xidmetler; Type: TABLE DATA; Schema: metodika; Owner: -
--

INSERT INTO metodika.metodik_xidmetler (id, ad, tip, tesvir, status) VALUES (1, 'Metodik məsləhət xidməti', 'meslehet', 'Müəllimlərə fərdi metodik məsləhət', 'aktiv');
INSERT INTO metodika.metodik_xidmetler (id, ad, tip, tesvir, status) VALUES (2, 'Məktəblərin metodik monitorinqi', 'monitorinq', 'Məktəb metodik işinin monitorinqi', 'aktiv');
INSERT INTO metodika.metodik_xidmetler (id, ad, tip, tesvir, status) VALUES (3, 'Metodik təlimlərin təşkili', 'telim', 'Müəllimlər üçün metodik təlimlər', 'aktiv');
INSERT INTO metodika.metodik_xidmetler (id, ad, tip, tesvir, status) VALUES (4, 'Dərslik ekspertizası', 'monitorinq', 'Dərslik və vəsaitlərin ekspertizası', 'aktiv');
INSERT INTO metodika.metodik_xidmetler (id, ad, tip, tesvir, status) VALUES (5, 'Metodbirləşmələrə dəstək', 'meslehet', 'Məktəb metodbirləşmələrinə dəstək', 'aktiv');
INSERT INTO metodika.metodik_xidmetler (id, ad, tip, tesvir, status) VALUES (6, 'Açıq dərslərin təşkili', 'telim', 'Nümunəvi açıq dərslərin təşkili', 'aktiv');
INSERT INTO metodika.metodik_xidmetler (id, ad, tip, tesvir, status) VALUES (7, 'Gənc müəllimlərə mentorluq', 'meslehet', 'Yeni müəllimlərə mentorluq dəstəyi', 'aktiv');
INSERT INTO metodika.metodik_xidmetler (id, ad, tip, tesvir, status) VALUES (8, 'Metodik vəsaitlərin təqdimatı', 'telim', 'Yeni vəsaitlərin təqdimat seminarları', 'aktiv');


--
-- Data for Name: beynelxalq_qiymetlendirmeler; Type: TABLE DATA; Schema: qiymetlendirme; Owner: -
--

INSERT INTO qiymetlendirme.beynelxalq_qiymetlendirmeler (id, ad, qisa_ad, tsikl, il, istirakci_sayi, status, qeyd) VALUES (1, 'Programme for International Student Assessment', 'PISA', '2022', 2024, 6800, 'netice', NULL);
INSERT INTO qiymetlendirme.beynelxalq_qiymetlendirmeler (id, ad, qisa_ad, tsikl, il, istirakci_sayi, status, qeyd) VALUES (2, 'Programme for International Student Assessment', 'PISA', '2025', 2027, 7000, 'hazirlıq', NULL);
INSERT INTO qiymetlendirme.beynelxalq_qiymetlendirmeler (id, ad, qisa_ad, tsikl, il, istirakci_sayi, status, qeyd) VALUES (3, 'Trends in Mathematics and Science Study', 'TIMSS', '2023', 2025, 5400, 'icra', NULL);
INSERT INTO qiymetlendirme.beynelxalq_qiymetlendirmeler (id, ad, qisa_ad, tsikl, il, istirakci_sayi, status, qeyd) VALUES (4, 'Progress in Reading Literacy Study', 'PIRLS', '2026', 2028, 5000, 'hazirlıq', NULL);
INSERT INTO qiymetlendirme.beynelxalq_qiymetlendirmeler (id, ad, qisa_ad, tsikl, il, istirakci_sayi, status, qeyd) VALUES (5, 'Teaching and Learning International Survey', 'TALIS', '2024', 2026, 3600, 'netice', NULL);
INSERT INTO qiymetlendirme.beynelxalq_qiymetlendirmeler (id, ad, qisa_ad, tsikl, il, istirakci_sayi, status, qeyd) VALUES (6, 'International Computer and Information Literacy', 'ICILS', '2023', 2025, 2800, 'bitdi', NULL);
INSERT INTO qiymetlendirme.beynelxalq_qiymetlendirmeler (id, ad, qisa_ad, tsikl, il, istirakci_sayi, status, qeyd) VALUES (7, 'PISA — maliyyə savadlılığı modulu', 'PISA-FL', '2022', 2024, 1500, 'netice', NULL);
INSERT INTO qiymetlendirme.beynelxalq_qiymetlendirmeler (id, ad, qisa_ad, tsikl, il, istirakci_sayi, status, qeyd) VALUES (8, 'PIRLS — oxu bacarıqları pilotu', 'PIRLS-P', '2024', 2026, 1200, 'bitdi', NULL);


--
-- Data for Name: monitorinq_hesabatlari; Type: TABLE DATA; Schema: qiymetlendirme; Owner: -
--

INSERT INTO qiymetlendirme.monitorinq_hesabatlari (id, ad, nov, il, tesvir, status, hazirlayan_shobe_id, qeyd) VALUES (1, 'Ümumtəhsil müəssisələrinin illik hesabatı', 'illik', 2025, 'Məktəblərin fəaliyyət göstəriciləri', 'tamamlandi', 24, NULL);
INSERT INTO qiymetlendirme.monitorinq_hesabatlari (id, ad, nov, il, tesvir, status, hazirlayan_shobe_id, qeyd) VALUES (2, 'Müəllim sertifikasiyasının rüblük təhlili', 'rubluk', 2026, 'Sertifikasiya nəticələrinin təhlili', 'tamamlandi', 13, NULL);
INSERT INTO qiymetlendirme.monitorinq_hesabatlari (id, ad, nov, il, tesvir, status, hazirlayan_shobe_id, qeyd) VALUES (3, 'PISA 2022 nəticələrinin milli hesabatı', 'xususi', 2025, 'Beynəlxalq qiymətləndirmə nəticələri', 'tamamlandi', 25, NULL);
INSERT INTO qiymetlendirme.monitorinq_hesabatlari (id, ad, nov, il, tesvir, status, hazirlayan_shobe_id, qeyd) VALUES (4, 'Kurikulum tətbiqinin monitorinqi', 'illik', 2026, 'Yeni kurikulumun icra vəziyyəti', 'hazirlanir', 17, NULL);
INSERT INTO qiymetlendirme.monitorinq_hesabatlari (id, ad, nov, il, tesvir, status, hazirlayan_shobe_id, qeyd) VALUES (5, 'İnklüziv təhsilin vəziyyəti', 'illik', 2026, 'İnklüziv təhsilin regionlar üzrə təhlili', 'hazirlanir', 4, NULL);
INSERT INTO qiymetlendirme.monitorinq_hesabatlari (id, ad, nov, il, tesvir, status, hazirlayan_shobe_id, qeyd) VALUES (6, 'MİQ nəticələrinin statistik təhlili', 'rubluk', 2026, 'Müəllim qəbulu imtahanlarının təhlili', 'tamamlandi', 26, NULL);
INSERT INTO qiymetlendirme.monitorinq_hesabatlari (id, ad, nov, il, tesvir, status, hazirlayan_shobe_id, qeyd) VALUES (7, 'Dərslik keyfiyyətinin monitorinqi', 'xususi', 2026, 'Dərsliklərin ekspertiza nəticələri', 'hazirlanir', 22, NULL);
INSERT INTO qiymetlendirme.monitorinq_hesabatlari (id, ad, nov, il, tesvir, status, hazirlayan_shobe_id, qeyd) VALUES (8, 'Şagird nailiyyətlərinin illik hesabatı', 'illik', 2025, 'Milli qiymətləndirmə nəticələri', 'tamamlandi', 24, NULL);
INSERT INTO qiymetlendirme.monitorinq_hesabatlari (id, ad, nov, il, tesvir, status, hazirlayan_shobe_id, qeyd) VALUES (9, 'STEAM təhsilinin monitorinqi', 'xususi', 2026, 'STEAM layihələrinin vəziyyəti', 'hazirlanir', 28, NULL);
INSERT INTO qiymetlendirme.monitorinq_hesabatlari (id, ad, nov, il, tesvir, status, hazirlayan_shobe_id, qeyd) VALUES (10, 'Təhsilin rəqəmsallaşması hesabatı', 'illik', 2026, 'Rəqəmsal resursların təhlili', 'hazirlanir', 30, NULL);


--
-- Data for Name: statistik_gostericiler; Type: TABLE DATA; Schema: qiymetlendirme; Owner: -
--

INSERT INTO qiymetlendirme.statistik_gostericiler (id, gosterici, deyer, vahid, il, bolge, qeyd) VALUES (1, 'Ümumtəhsil məktəblərinin sayı', 4432.00, 'məktəb', 2026, 'Bütün ölkə', NULL);
INSERT INTO qiymetlendirme.statistik_gostericiler (id, gosterici, deyer, vahid, il, bolge, qeyd) VALUES (2, 'Şagird sayı', 1640000.00, 'nəfər', 2026, 'Bütün ölkə', NULL);
INSERT INTO qiymetlendirme.statistik_gostericiler (id, gosterici, deyer, vahid, il, bolge, qeyd) VALUES (3, 'Müəllim sayı', 152000.00, 'nəfər', 2026, 'Bütün ölkə', NULL);
INSERT INTO qiymetlendirme.statistik_gostericiler (id, gosterici, deyer, vahid, il, bolge, qeyd) VALUES (4, 'PISA riyaziyyat orta balı', 397.00, 'bal', 2024, 'Bütün ölkə', NULL);
INSERT INTO qiymetlendirme.statistik_gostericiler (id, gosterici, deyer, vahid, il, bolge, qeyd) VALUES (5, 'PISA oxu orta balı', 392.00, 'bal', 2024, 'Bütün ölkə', NULL);
INSERT INTO qiymetlendirme.statistik_gostericiler (id, gosterici, deyer, vahid, il, bolge, qeyd) VALUES (6, 'PISA elm orta balı', 390.00, 'bal', 2024, 'Bütün ölkə', NULL);
INSERT INTO qiymetlendirme.statistik_gostericiler (id, gosterici, deyer, vahid, il, bolge, qeyd) VALUES (7, 'Sertifikasiyadan keçən müəllim faizi', 78.50, '%', 2026, 'Bütün ölkə', NULL);
INSERT INTO qiymetlendirme.statistik_gostericiler (id, gosterici, deyer, vahid, il, bolge, qeyd) VALUES (8, 'Məktəblərin internetlə təminatı', 96.20, '%', 2026, 'Bütün ölkə', NULL);
INSERT INTO qiymetlendirme.statistik_gostericiler (id, gosterici, deyer, vahid, il, bolge, qeyd) VALUES (9, 'Bakı şəhəri üzrə şagird sayı', 380000.00, 'nəfər', 2026, 'Bakı', NULL);
INSERT INTO qiymetlendirme.statistik_gostericiler (id, gosterici, deyer, vahid, il, bolge, qeyd) VALUES (10, 'İnklüziv təhsilə cəlb olunanlar', 12800.00, 'nəfər', 2026, 'Bütün ölkə', NULL);


--
-- Data for Name: emrler; Type: TABLE DATA; Schema: sened; Owner: -
--

INSERT INTO sened.emrler (id, emr_no, tarix, movzu, imzalayan, qeyd) VALUES (1, 'K-2024-001', '2026-01-10', '2024-cü il üçün iş planının təsdiqi', 'Elnur Əliyev', NULL);
INSERT INTO sened.emrler (id, emr_no, tarix, movzu, imzalayan, qeyd) VALUES (2, 'K-2024-015', '2026-02-05', 'Elmi Şura tərkibinin yenilənməsi', 'Elnur Əliyev', NULL);
INSERT INTO sened.emrler (id, emr_no, tarix, movzu, imzalayan, qeyd) VALUES (3, 'K-2024-032', '2026-03-12', 'PISA 2025 işçi qrupunun yaradılması', 'Fuad Qarayev', NULL);
INSERT INTO sened.emrler (id, emr_no, tarix, movzu, imzalayan, qeyd) VALUES (4, 'K-2024-048', '2026-04-08', 'Doktorantura qəbulu komissiyasının təşkili', 'Aydın Əhmədov', NULL);
INSERT INTO sened.emrler (id, emr_no, tarix, movzu, imzalayan, qeyd) VALUES (5, 'K-2024-061', '2026-05-20', 'Müəllim sertifikasiyası qrafikinin təsdiqi', 'Aydın Əhmədov', NULL);
INSERT INTO sened.emrler (id, emr_no, tarix, movzu, imzalayan, qeyd) VALUES (6, 'K-2024-075', '2026-06-17', 'Yay təlimlərinin təşkili haqqında', 'Kənan Kərimli', NULL);
INSERT INTO sened.emrler (id, emr_no, tarix, movzu, imzalayan, qeyd) VALUES (7, 'K-2024-090', '2026-09-02', 'Yeni dərsliklərin ekspertiza komissiyası', 'Fuad Qarayev', NULL);
INSERT INTO sened.emrler (id, emr_no, tarix, movzu, imzalayan, qeyd) VALUES (8, 'K-2024-104', '2026-10-14', 'İllik hesabatların təqdim qaydası', 'İlham Cavadov', NULL);
INSERT INTO sened.emrler (id, emr_no, tarix, movzu, imzalayan, qeyd) VALUES (9, 'K-2024-118', '2026-11-18', 'Beynəlxalq əməkdaşlıq tədbirlərinin təsdiqi', 'Tariyel Talıbov', NULL);
INSERT INTO sened.emrler (id, emr_no, tarix, movzu, imzalayan, qeyd) VALUES (10, 'K-2024-130', '2026-12-16', '2025-ci il iş planının hazırlanması', 'Elnur Əliyev', NULL);


--
-- Data for Name: sened_novleri; Type: TABLE DATA; Schema: sened; Owner: -
--

INSERT INTO sened.sened_novleri (id, ad, tesvir) VALUES (1, 'Əmr', 'Rəhbərliyin əmrləri');
INSERT INTO sened.sened_novleri (id, ad, tesvir) VALUES (2, 'Məktub', 'Rəsmi yazışmalar');
INSERT INTO sened.sened_novleri (id, ad, tesvir) VALUES (3, 'Protokol', 'İclas protokolları');
INSERT INTO sened.sened_novleri (id, ad, tesvir) VALUES (4, 'Qərar', 'Elmi Şura və komissiya qərarları');
INSERT INTO sened.sened_novleri (id, ad, tesvir) VALUES (5, 'Hesabat', 'Dövrü hesabatlar');
INSERT INTO sened.sened_novleri (id, ad, tesvir) VALUES (6, 'Arayış', 'Verilən arayışlar');
INSERT INTO sened.sened_novleri (id, ad, tesvir) VALUES (7, 'Ərizə', 'Daxil olan ərizələr');
INSERT INTO sened.sened_novleri (id, ad, tesvir) VALUES (8, 'Müqavilə', 'Müqavilə sənədləri');


--
-- Data for Name: senedler; Type: TABLE DATA; Schema: sened; Owner: -
--

INSERT INTO sened.senedler (id, nov_id, nomre, tarix, movzu, gonderen, alan, status, qeyd) VALUES (1, 2, 'ÇX-2024-101', '2026-01-22', 'PISA 2025 iştirak təsdiqi', 'Elm və Təhsil Nazirliyi', 'ARTİ', 'icra', NULL);
INSERT INTO sened.senedler (id, nov_id, nomre, tarix, movzu, gonderen, alan, status, qeyd) VALUES (2, 2, 'DX-2024-205', '2026-02-14', 'Doktorantura yerləri barədə', 'ARTİ', 'Nazirlik', 'arxiv', NULL);
INSERT INTO sened.senedler (id, nov_id, nomre, tarix, movzu, gonderen, alan, status, qeyd) VALUES (3, 3, 'PR-2024-011', '2026-02-16', 'Elmi Şura iclas protokolu', 'Elmi katiblik', 'Rəhbərlik', 'arxiv', NULL);
INSERT INTO sened.senedler (id, nov_id, nomre, tarix, movzu, gonderen, alan, status, qeyd) VALUES (4, 6, 'AR-2024-033', '2026-03-05', 'Əməkdaşa iş yerindən arayış', 'ARTİ', 'Əməkdaş', 'arxiv', NULL);
INSERT INTO sened.senedler (id, nov_id, nomre, tarix, movzu, gonderen, alan, status, qeyd) VALUES (5, 7, 'ƏR-2024-087', '2026-04-11', 'Məzuniyyət ərizəsi', 'Əməkdaş', 'İnsan resursları', 'icra', NULL);
INSERT INTO sened.senedler (id, nov_id, nomre, tarix, movzu, gonderen, alan, status, qeyd) VALUES (6, 2, 'ÇX-2024-140', '2026-05-09', 'Sertifikasiya qrafiki barədə', 'ARTİ', 'Məktəblər', 'arxiv', NULL);
INSERT INTO sened.senedler (id, nov_id, nomre, tarix, movzu, gonderen, alan, status, qeyd) VALUES (7, 4, 'QR-2024-004', '2026-06-13', 'Elmi Şura qərarı (PISA qrupu)', 'Elmi Şura', 'Qiymətləndirmə mərkəzi', 'icra', NULL);
INSERT INTO sened.senedler (id, nov_id, nomre, tarix, movzu, gonderen, alan, status, qeyd) VALUES (8, 5, 'HS-2024-001', '2026-07-01', 'Yarımillik fəaliyyət hesabatı', 'Mərkəzlər', 'Rəhbərlik', 'arxiv', NULL);
INSERT INTO sened.senedler (id, nov_id, nomre, tarix, movzu, gonderen, alan, status, qeyd) VALUES (9, 2, 'ÇX-2024-178', '2026-08-19', 'Beynəlxalq tədbir dəvəti', 'TED Universiteti', 'ARTİ', 'icra', NULL);
INSERT INTO sened.senedler (id, nov_id, nomre, tarix, movzu, gonderen, alan, status, qeyd) VALUES (10, 8, 'MQ-2024-012', '2026-09-26', 'Kitabxana təchizatı müqaviləsi', 'ARTİ', 'KitabEvi MMC', 'qeydiyyatda', NULL);


--
-- Data for Name: elmi_shura_iclaslari; Type: TABLE DATA; Schema: struktur; Owner: -
--

INSERT INTO struktur.elmi_shura_iclaslari (id, iclas_tarixi, novu, gundelik, kecirildiyi_yer, protokol_no, qeyd) VALUES (1, '2026-02-15', 'novbeti', '2023-cü il üzrə illik hesabatın müzakirəsi', 'ARTİ iclas zalı', 'ES-2024-01', NULL);
INSERT INTO struktur.elmi_shura_iclaslari (id, iclas_tarixi, novu, gundelik, kecirildiyi_yer, protokol_no, qeyd) VALUES (2, '2026-04-18', 'novbeti', 'Doktorantura qəbulu planının təsdiqi', 'ARTİ iclas zalı', 'ES-2024-02', NULL);
INSERT INTO struktur.elmi_shura_iclaslari (id, iclas_tarixi, novu, gundelik, kecirildiyi_yer, protokol_no, qeyd) VALUES (3, '2026-06-12', 'novbedenkenar', 'Elmi əsərlər jurnalının növbəti sayı', 'ARTİ iclas zalı', 'ES-2024-03', NULL);
INSERT INTO struktur.elmi_shura_iclaslari (id, iclas_tarixi, novu, gundelik, kecirildiyi_yer, protokol_no, qeyd) VALUES (4, '2026-09-20', 'novbeti', 'Dərsliklərin ekspertiza nəticələri', 'ARTİ iclas zalı', 'ES-2024-04', NULL);
INSERT INTO struktur.elmi_shura_iclaslari (id, iclas_tarixi, novu, gundelik, kecirildiyi_yer, protokol_no, qeyd) VALUES (5, '2026-11-14', 'novbeti', 'Elmi kadr hazırlığının yol xəritəsi', 'ARTİ iclas zalı', 'ES-2024-05', NULL);
INSERT INTO struktur.elmi_shura_iclaslari (id, iclas_tarixi, novu, gundelik, kecirildiyi_yer, protokol_no, qeyd) VALUES (6, '2027-01-23', 'novbeti', '2024-cü il hesabatı və 2025-ci il planı', 'ARTİ iclas zalı', 'ES-2025-01', NULL);
INSERT INTO struktur.elmi_shura_iclaslari (id, iclas_tarixi, novu, gundelik, kecirildiyi_yer, protokol_no, qeyd) VALUES (7, '2027-03-27', 'novbeti', 'PISA 2025 hazırlıq işləri', 'ARTİ iclas zalı', 'ES-2025-02', NULL);
INSERT INTO struktur.elmi_shura_iclaslari (id, iclas_tarixi, novu, gundelik, kecirildiyi_yer, protokol_no, qeyd) VALUES (8, '2027-05-15', 'novbeti', 'Elmi fəaliyyətin stimullaşdırılması', 'ARTİ iclas zalı', 'ES-2025-03', NULL);


--
-- Data for Name: elmi_shura_qerarlari; Type: TABLE DATA; Schema: struktur; Owner: -
--

INSERT INTO struktur.elmi_shura_qerarlari (id, iclas_id, qerar_no, qerar_metni, icraci_shobe_id, son_tarix, status, qeyd) VALUES (1, 1, 'Q-2024-01/1', '2023-cü il hesabatı qəbul edilsin və Nazirliyə təqdim olunsun.', 6, '2026-03-01', 'yerine_yetirildi', NULL);
INSERT INTO struktur.elmi_shura_qerarlari (id, iclas_id, qerar_no, qerar_metni, icraci_shobe_id, son_tarix, status, qeyd) VALUES (2, 2, 'Q-2024-02/1', 'Doktoranturaya qəbul planı təsdiq edilsin (12 yer).', 7, '2026-05-01', 'yerine_yetirildi', NULL);
INSERT INTO struktur.elmi_shura_qerarlari (id, iclas_id, qerar_no, qerar_metni, icraci_shobe_id, son_tarix, status, qeyd) VALUES (3, 3, 'Q-2024-03/1', 'Elmi əsərlər jurnalının sayı apreldə çapa verilsin.', 1, '2026-04-30', 'yerine_yetirildi', NULL);
INSERT INTO struktur.elmi_shura_qerarlari (id, iclas_id, qerar_no, qerar_metni, icraci_shobe_id, son_tarix, status, qeyd) VALUES (4, 4, 'Q-2024-04/1', 'Yeni dərsliklərin ekspertizası üçün komissiya yaradılsın.', 22, '2026-10-15', 'yerine_yetirildi', NULL);
INSERT INTO struktur.elmi_shura_qerarlari (id, iclas_id, qerar_no, qerar_metni, icraci_shobe_id, son_tarix, status, qeyd) VALUES (5, 4, 'Q-2024-04/2', 'Ekspertiza nəticələri əsasında tövsiyələr hazırlansın.', 22, '2026-11-01', 'icrada', NULL);
INSERT INTO struktur.elmi_shura_qerarlari (id, iclas_id, qerar_no, qerar_metni, icraci_shobe_id, son_tarix, status, qeyd) VALUES (6, 5, 'Q-2024-05/1', 'Elmi kadr hazırlığı üzrə yol xəritəsi təsdiq edilsin.', 7, '2026-12-01', 'icrada', NULL);
INSERT INTO struktur.elmi_shura_qerarlari (id, iclas_id, qerar_no, qerar_metni, icraci_shobe_id, son_tarix, status, qeyd) VALUES (7, 6, 'Q-2025-01/1', '2024-cü il hesabatı qəbul edilsin, 2025-ci il planı təsdiqlənsin.', 6, '2027-02-15', 'yerine_yetirildi', NULL);
INSERT INTO struktur.elmi_shura_qerarlari (id, iclas_id, qerar_no, qerar_metni, icraci_shobe_id, son_tarix, status, qeyd) VALUES (8, 7, 'Q-2025-02/1', 'PISA 2025 üzrə işçi qrup yaradılsın və təlim cədvəli hazırlansın.', 25, '2027-04-30', 'icrada', NULL);
INSERT INTO struktur.elmi_shura_qerarlari (id, iclas_id, qerar_no, qerar_metni, icraci_shobe_id, son_tarix, status, qeyd) VALUES (9, 8, 'Q-2025-03/1', 'Elmi fəaliyyətin stimullaşdırılması meyarları hazırlansın.', 2, '2027-06-30', 'icrada', NULL);


--
-- Data for Name: elmi_shura_uzvleri; Type: TABLE DATA; Schema: struktur; Owner: -
--

INSERT INTO struktur.elmi_shura_uzvleri (id, emekdas_id, ad_soyad, vezife_id, elmi_derece_id, elmi_ad_id, status, qosulma_tarixi, aktiv) VALUES (1, 1, 'Əliyev Elnur Qəzənfər', 1, 3, 2, 'sedr', '2023-01-15', true);
INSERT INTO struktur.elmi_shura_uzvleri (id, emekdas_id, ad_soyad, vezife_id, elmi_derece_id, elmi_ad_id, status, qosulma_tarixi, aktiv) VALUES (2, 8, 'Həsənova Aygün Vahid', 3, 3, 2, 'katib', '2023-01-15', true);
INSERT INTO struktur.elmi_shura_uzvleri (id, emekdas_id, ad_soyad, vezife_id, elmi_derece_id, elmi_ad_id, status, qosulma_tarixi, aktiv) VALUES (3, 9, 'Məmmədov Rəşad İlham', 4, 4, 1, 'uzv', '2023-01-15', true);
INSERT INTO struktur.elmi_shura_uzvleri (id, emekdas_id, ad_soyad, vezife_id, elmi_derece_id, elmi_ad_id, status, qosulma_tarixi, aktiv) VALUES (4, 10, 'Quliyeva Nərminə Fikrət', 4, 3, 2, 'uzv', '2023-01-15', true);
INSERT INTO struktur.elmi_shura_uzvleri (id, emekdas_id, ad_soyad, vezife_id, elmi_derece_id, elmi_ad_id, status, qosulma_tarixi, aktiv) VALUES (5, 6, 'Talıbov Tariyel İsmayıl', 2, 4, 1, 'uzv', '2023-01-15', true);
INSERT INTO struktur.elmi_shura_uzvleri (id, emekdas_id, ad_soyad, vezife_id, elmi_derece_id, elmi_ad_id, status, qosulma_tarixi, aktiv) VALUES (6, 2, 'Əhmədov Aydın Əhəd', 2, 3, 2, 'uzv', '2023-01-15', true);
INSERT INTO struktur.elmi_shura_uzvleri (id, emekdas_id, ad_soyad, vezife_id, elmi_derece_id, elmi_ad_id, status, qosulma_tarixi, aktiv) VALUES (7, 3, 'Qarayev Fuad Abdurahman', 2, 3, 2, 'uzv', '2023-01-15', true);
INSERT INTO struktur.elmi_shura_uzvleri (id, emekdas_id, ad_soyad, vezife_id, elmi_derece_id, elmi_ad_id, status, qosulma_tarixi, aktiv) VALUES (8, NULL, 'Vəliyeva Zöhrə Nizami', 5, 4, 1, 'uzv', '2023-01-15', true);
INSERT INTO struktur.elmi_shura_uzvleri (id, emekdas_id, ad_soyad, vezife_id, elmi_derece_id, elmi_ad_id, status, qosulma_tarixi, aktiv) VALUES (9, NULL, 'Hüseynov Cahid Murad', 5, 3, 2, 'uzv', '2023-01-15', true);
INSERT INTO struktur.elmi_shura_uzvleri (id, emekdas_id, ad_soyad, vezife_id, elmi_derece_id, elmi_ad_id, status, qosulma_tarixi, aktiv) VALUES (10, NULL, 'Əsgərova Ləman Rasim', 5, 3, 2, 'uzv', '2024-03-10', true);


--
-- Data for Name: rehberlik; Type: TABLE DATA; Schema: struktur; Owner: -
--

INSERT INTO struktur.rehberlik (id, emekdas_id, vezife_id, merkez_id, sira, tesvir, aktiv) VALUES (1, 1, 1, NULL, 1, 'Direktor səlahiyyətlərini müvəqqəti icra edən', true);
INSERT INTO struktur.rehberlik (id, emekdas_id, vezife_id, merkez_id, sira, tesvir, aktiv) VALUES (2, 2, 2, NULL, 2, 'Elmi işlər üzrə direktor müavini', true);
INSERT INTO struktur.rehberlik (id, emekdas_id, vezife_id, merkez_id, sira, tesvir, aktiv) VALUES (3, 3, 2, NULL, 3, 'Təhsil proqramları üzrə direktor müavini', true);
INSERT INTO struktur.rehberlik (id, emekdas_id, vezife_id, merkez_id, sira, tesvir, aktiv) VALUES (4, 4, 2, NULL, 4, 'Qiymətləndirmə üzrə direktor müavini', true);
INSERT INTO struktur.rehberlik (id, emekdas_id, vezife_id, merkez_id, sira, tesvir, aktiv) VALUES (5, 5, 2, NULL, 5, 'Maliyyə və inzibati işlər üzrə direktor müavini', true);
INSERT INTO struktur.rehberlik (id, emekdas_id, vezife_id, merkez_id, sira, tesvir, aktiv) VALUES (6, 6, 2, NULL, 6, 'Beynəlxalq əlaqələr üzrə direktor müavini', true);
INSERT INTO struktur.rehberlik (id, emekdas_id, vezife_id, merkez_id, sira, tesvir, aktiv) VALUES (7, 7, 2, NULL, 7, 'Rəqəmsallaşma üzrə direktor müavini', true);


--
-- Data for Name: imtahanlar; Type: TABLE DATA; Schema: tehsil; Owner: -
--

INSERT INTO tehsil.imtahanlar (id, ad, tip, tarix, istirakci_sayi, qeyd) VALUES (1, 'Müəllim sertifikasiyası — I mərhələ', 'sertifikasiya', '2026-03-30', 2500, NULL);
INSERT INTO tehsil.imtahanlar (id, ad, tip, tarix, istirakci_sayi, qeyd) VALUES (2, 'Müəllim sertifikasiyası — II mərhələ', 'sertifikasiya', '2026-04-27', 2300, NULL);
INSERT INTO tehsil.imtahanlar (id, ad, tip, tarix, istirakci_sayi, qeyd) VALUES (3, 'MİQ — fənn imtahanı', 'miq', '2026-05-18', 5000, NULL);
INSERT INTO tehsil.imtahanlar (id, ad, tip, tarix, istirakci_sayi, qeyd) VALUES (4, 'MİQ — müsahibə mərhələsi', 'miq', '2026-06-22', 3200, NULL);
INSERT INTO tehsil.imtahanlar (id, ad, tip, tarix, istirakci_sayi, qeyd) VALUES (5, 'Məktəb direktorlarının sertifikasiyası', 'sertifikasiya', '2026-06-15', 400, NULL);
INSERT INTO tehsil.imtahanlar (id, ad, tip, tarix, istirakci_sayi, qeyd) VALUES (6, 'Metodist sertifikasiyası', 'sertifikasiya', '2026-05-10', 180, NULL);
INSERT INTO tehsil.imtahanlar (id, ad, tip, tarix, istirakci_sayi, qeyd) VALUES (7, 'Doktorantura qəbul imtahanı', 'qebul', '2026-07-06', 120, NULL);
INSERT INTO tehsil.imtahanlar (id, ad, tip, tarix, istirakci_sayi, qeyd) VALUES (8, 'Magistratura qəbulu (Sabah proqramı)', 'qebul', '2026-08-17', 800, NULL);


--
-- Data for Name: sertifikasiya; Type: TABLE DATA; Schema: tehsil; Owner: -
--

INSERT INTO tehsil.sertifikasiya (id, emekdas_id, ad_soyad, tip, imtahan_tarixi, bal, netice, sertifikat_no, qeyd) VALUES (1, NULL, 'Səbinə Rəhimova', 'müəllim', '2026-03-30', 72.5, 'keçdi', 'SER-2024-001', NULL);
INSERT INTO tehsil.sertifikasiya (id, emekdas_id, ad_soyad, tip, imtahan_tarixi, bal, netice, sertifikat_no, qeyd) VALUES (2, NULL, 'Orxan Quliyev', 'müəllim', '2026-03-30', 68.0, 'keçdi', 'SER-2024-002', NULL);
INSERT INTO tehsil.sertifikasiya (id, emekdas_id, ad_soyad, tip, imtahan_tarixi, bal, netice, sertifikat_no, qeyd) VALUES (3, NULL, 'Gülnar Əsgərova', 'müəllim', '2026-03-30', 54.0, 'qaldi', NULL, NULL);
INSERT INTO tehsil.sertifikasiya (id, emekdas_id, ad_soyad, tip, imtahan_tarixi, bal, netice, sertifikat_no, qeyd) VALUES (4, NULL, 'Eldar Hüseynov', 'müəllim', '2026-04-27', 75.5, 'keçdi', 'SER-2024-004', NULL);
INSERT INTO tehsil.sertifikasiya (id, emekdas_id, ad_soyad, tip, imtahan_tarixi, bal, netice, sertifikat_no, qeyd) VALUES (5, NULL, 'Nərgiz Babayeva', 'müəllim', '2026-04-27', 61.5, 'keçdi', 'SER-2024-005', NULL);
INSERT INTO tehsil.sertifikasiya (id, emekdas_id, ad_soyad, tip, imtahan_tarixi, bal, netice, sertifikat_no, qeyd) VALUES (6, 8, 'Aygün Həsənova', 'metodist', '2026-05-10', 88.0, 'keçdi', 'SER-2024-006', NULL);
INSERT INTO tehsil.sertifikasiya (id, emekdas_id, ad_soyad, tip, imtahan_tarixi, bal, netice, sertifikat_no, qeyd) VALUES (7, 10, 'Nərminə Quliyeva', 'metodist', '2026-05-10', 90.5, 'keçdi', 'SER-2024-007', NULL);
INSERT INTO tehsil.sertifikasiya (id, emekdas_id, ad_soyad, tip, imtahan_tarixi, bal, netice, sertifikat_no, qeyd) VALUES (8, NULL, 'Kamran Əliyev', 'direktor', '2026-06-15', 79.0, 'keçdi', 'SER-2024-008', NULL);
INSERT INTO tehsil.sertifikasiya (id, emekdas_id, ad_soyad, tip, imtahan_tarixi, bal, netice, sertifikat_no, qeyd) VALUES (9, NULL, 'Aynur Rzayeva', 'müəllim', '2026-06-15', 55.5, 'qaldi', NULL, NULL);
INSERT INTO tehsil.sertifikasiya (id, emekdas_id, ad_soyad, tip, imtahan_tarixi, bal, netice, sertifikat_no, qeyd) VALUES (10, NULL, 'Vüsal Məmmədov', 'müəllim', '2026-06-15', 70.0, 'keçdi', 'SER-2024-010', NULL);


--
-- Data for Name: telim_proqramlari; Type: TABLE DATA; Schema: tehsil; Owner: -
--

INSERT INTO tehsil.telim_proqramlari (id, ad, kateqoriya, saat, hedef_qrup, tesvir) VALUES (1, 'Müəllim sertifikasiyasına hazırlıq', 'sertifikasiya', 40, 'Ümumtəhsil müəllimləri', NULL);
INSERT INTO tehsil.telim_proqramlari (id, ad, kateqoriya, saat, hedef_qrup, tesvir) VALUES (2, 'Yeni kurikulum üzrə təlim', 'umumi', 30, 'Fənn müəllimləri', NULL);
INSERT INTO tehsil.telim_proqramlari (id, ad, kateqoriya, saat, hedef_qrup, tesvir) VALUES (3, 'MİQ (müəllimlərin işə qəbulu) hazırlığı', 'miq', 50, 'Gənc müəllimlər', NULL);
INSERT INTO tehsil.telim_proqramlari (id, ad, kateqoriya, saat, hedef_qrup, tesvir) VALUES (4, 'İnklüziv təhsil üzrə təlim', 'xususi', 25, 'Müəllimlər və psixoloqlar', NULL);
INSERT INTO tehsil.telim_proqramlari (id, ad, kateqoriya, saat, hedef_qrup, tesvir) VALUES (5, 'STEAM təhsili metodikası', 'xususi', 30, 'Təbiət fənn müəllimləri', NULL);
INSERT INTO tehsil.telim_proqramlari (id, ad, kateqoriya, saat, hedef_qrup, tesvir) VALUES (6, 'Rəqəmsal bacarıqlar üzrə təlim', 'umumi', 20, 'Bütün müəllimlər', NULL);
INSERT INTO tehsil.telim_proqramlari (id, ad, kateqoriya, saat, hedef_qrup, tesvir) VALUES (7, 'Məktəb rəhbərləri üçün idarəetmə', 'sertifikasiya', 35, 'Məktəb direktorları', NULL);
INSERT INTO tehsil.telim_proqramlari (id, ad, kateqoriya, saat, hedef_qrup, tesvir) VALUES (8, 'Qiymətləndirmə bacarıqları', 'umumi', 25, 'Müəllimlər', NULL);
INSERT INTO tehsil.telim_proqramlari (id, ad, kateqoriya, saat, hedef_qrup, tesvir) VALUES (9, 'İbtidai sinif müəllimləri üçün təlim', 'umumi', 30, 'İbtidai sinif müəllimləri', NULL);
INSERT INTO tehsil.telim_proqramlari (id, ad, kateqoriya, saat, hedef_qrup, tesvir) VALUES (10, 'Metodistlər üçün peşəkar inkişaf', 'xususi', 30, 'Metodistlər', NULL);


--
-- Data for Name: telim_qruplari; Type: TABLE DATA; Schema: tehsil; Owner: -
--

INSERT INTO tehsil.telim_qruplari (id, proqram_id, ad, telimci_id, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (1, 1, 'Sertifikasiya Qrup A', 8, '2026-03-04', '2026-03-29', 'bitdi', NULL);
INSERT INTO tehsil.telim_qruplari (id, proqram_id, ad, telimci_id, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (2, 1, 'Sertifikasiya Qrup B', 8, '2026-04-01', '2026-04-26', 'bitdi', NULL);
INSERT INTO tehsil.telim_qruplari (id, proqram_id, ad, telimci_id, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (3, 2, 'Kurikulum Qrup 1', 3, '2026-05-06', '2026-05-24', 'bitdi', NULL);
INSERT INTO tehsil.telim_qruplari (id, proqram_id, ad, telimci_id, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (4, 3, 'MİQ Qrup 1', 8, '2026-06-03', '2026-06-28', 'bitdi', NULL);
INSERT INTO tehsil.telim_qruplari (id, proqram_id, ad, telimci_id, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (5, 4, 'İnklüziv Qrup 1', 4, '2026-09-02', '2026-09-20', 'davam edir', NULL);
INSERT INTO tehsil.telim_qruplari (id, proqram_id, ad, telimci_id, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (6, 5, 'STEAM Qrup 1', 13, '2026-10-01', '2026-10-25', 'planlasdirilir', NULL);
INSERT INTO tehsil.telim_qruplari (id, proqram_id, ad, telimci_id, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (7, 6, 'Rəqəmsal Qrup 1', 13, '2026-11-04', '2026-11-22', 'planlasdirilir', NULL);
INSERT INTO tehsil.telim_qruplari (id, proqram_id, ad, telimci_id, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (8, 7, 'Direktorlar Qrup 1', 6, '2026-10-14', '2026-11-08', 'planlasdirilir', NULL);
INSERT INTO tehsil.telim_qruplari (id, proqram_id, ad, telimci_id, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (9, 9, 'İbtidai Qrup 1', 3, '2026-09-09', '2026-09-27', 'davam edir', NULL);
INSERT INTO tehsil.telim_qruplari (id, proqram_id, ad, telimci_id, baslama_tarixi, bitme_tarixi, status, qeyd) VALUES (10, 10, 'Metodist Qrup 1', 10, '2026-11-11', '2026-12-06', 'planlasdirilir', NULL);


--
-- Data for Name: telim_istirakcilari; Type: TABLE DATA; Schema: tehsil; Owner: -
--

INSERT INTO tehsil.telim_istirakcilari (id, qrup_id, ad, soyad, ata_adi, is_yeri, sertifikat_no, status, qeyd) VALUES (1, 1, 'Səbinə', 'Rəhimova', 'Nizami', 'Bakı ş. 6 nömrəli məktəb', 'SER-2024-001', 'bitirdi', NULL);
INSERT INTO tehsil.telim_istirakcilari (id, qrup_id, ad, soyad, ata_adi, is_yeri, sertifikat_no, status, qeyd) VALUES (2, 1, 'Orxan', 'Quliyev', 'Vaqif', 'Bakı ş. 20 nömrəli məktəb', 'SER-2024-002', 'bitirdi', NULL);
INSERT INTO tehsil.telim_istirakcilari (id, qrup_id, ad, soyad, ata_adi, is_yeri, sertifikat_no, status, qeyd) VALUES (3, 1, 'Gülnar', 'Əsgərova', 'Tofiq', 'Sumqayıt ş. 5 nömrəli məktəb', 'SER-2024-003', 'bitirdi', NULL);
INSERT INTO tehsil.telim_istirakcilari (id, qrup_id, ad, soyad, ata_adi, is_yeri, sertifikat_no, status, qeyd) VALUES (4, 2, 'Eldar', 'Hüseynov', 'Rafiq', 'Gəncə ş. 3 nömrəli məktəb', 'SER-2024-004', 'bitirdi', NULL);
INSERT INTO tehsil.telim_istirakcilari (id, qrup_id, ad, soyad, ata_adi, is_yeri, sertifikat_no, status, qeyd) VALUES (5, 2, 'Nərgiz', 'Babayeva', 'Şahin', 'Bakı ş. 44 nömrəli məktəb', 'SER-2024-005', 'bitirdi', NULL);
INSERT INTO tehsil.telim_istirakcilari (id, qrup_id, ad, soyad, ata_adi, is_yeri, sertifikat_no, status, qeyd) VALUES (6, 3, 'Fərid', 'Məmmədov', 'Əli', 'Şirvan ş. 2 nömrəli məktəb', 'KUR-2024-001', 'bitirdi', NULL);
INSERT INTO tehsil.telim_istirakcilari (id, qrup_id, ad, soyad, ata_adi, is_yeri, sertifikat_no, status, qeyd) VALUES (7, 3, 'Aysel', 'Cəfərova', 'Nadir', 'Bakı ş. 15 nömrəli lisey', 'KUR-2024-002', 'bitirdi', NULL);
INSERT INTO tehsil.telim_istirakcilari (id, qrup_id, ad, soyad, ata_adi, is_yeri, sertifikat_no, status, qeyd) VALUES (8, 4, 'Tural', 'Ələsgərov', 'Kamal', 'Xaçmaz r. 1 nömrəli məktəb', 'MIQ-2024-001', 'bitirdi', NULL);
INSERT INTO tehsil.telim_istirakcilari (id, qrup_id, ad, soyad, ata_adi, is_yeri, sertifikat_no, status, qeyd) VALUES (9, 5, 'Zeynəb', 'İsmayılova', 'Rəşad', 'Bakı ş. 8 nömrəli məktəb', 'INK-2024-001', 'bitirdi', NULL);
INSERT INTO tehsil.telim_istirakcilari (id, qrup_id, ad, soyad, ata_adi, is_yeri, sertifikat_no, status, qeyd) VALUES (10, 9, 'Rəşad', 'Nəbiyev', 'İlham', 'Lənkəran ş. 4 nömrəli məktəb', 'IBT-2024-001', 'bitirdi', NULL);


--
-- Name: ai_promptlar_id_seq; Type: SEQUENCE SET; Schema: ai; Owner: -
--

SELECT pg_catalog.setval('ai.ai_promptlar_id_seq', 8, true);


--
-- Name: ai_sorghular_id_seq; Type: SEQUENCE SET; Schema: ai; Owner: -
--

SELECT pg_catalog.setval('ai.ai_sorghular_id_seq', 26, true);


--
-- Name: embeddingler_id_seq; Type: SEQUENCE SET; Schema: ai; Owner: -
--

SELECT pg_catalog.setval('ai.embeddingler_id_seq', 8, true);


--
-- Name: audit_log_id_seq; Type: SEQUENCE SET; Schema: audit; Owner: -
--

SELECT pg_catalog.setval('audit.audit_log_id_seq', 133, true);


--
-- Name: doktorantlar_id_seq; Type: SEQUENCE SET; Schema: elm; Owner: -
--

SELECT pg_catalog.setval('elm.doktorantlar_id_seq', 10, true);


--
-- Name: doktorantura_proqramlari_id_seq; Type: SEQUENCE SET; Schema: elm; Owner: -
--

SELECT pg_catalog.setval('elm.doktorantura_proqramlari_id_seq', 8, true);


--
-- Name: elmi_tedbirler_id_seq; Type: SEQUENCE SET; Schema: elm; Owner: -
--

SELECT pg_catalog.setval('elm.elmi_tedbirler_id_seq', 10, true);


--
-- Name: jurnallar_id_seq; Type: SEQUENCE SET; Schema: elm; Owner: -
--

SELECT pg_catalog.setval('elm.jurnallar_id_seq', 8, true);


--
-- Name: meqaleler_id_seq; Type: SEQUENCE SET; Schema: elm; Owner: -
--

SELECT pg_catalog.setval('elm.meqaleler_id_seq', 10, true);


--
-- Name: neshrler_id_seq; Type: SEQUENCE SET; Schema: elm; Owner: -
--

SELECT pg_catalog.setval('elm.neshrler_id_seq', 10, true);


--
-- Name: tedqiqat_istiqametleri_id_seq; Type: SEQUENCE SET; Schema: elm; Owner: -
--

SELECT pg_catalog.setval('elm.tedqiqat_istiqametleri_id_seq', 10, true);


--
-- Name: tedqiqat_layiheleri_id_seq; Type: SEQUENCE SET; Schema: elm; Owner: -
--

SELECT pg_catalog.setval('elm.tedqiqat_layiheleri_id_seq', 11, true);


--
-- Name: emekdaslar_id_seq; Type: SEQUENCE SET; Schema: kadrlar; Owner: -
--

SELECT pg_catalog.setval('kadrlar.emekdaslar_id_seq', 15, true);


--
-- Name: is_tecrubesi_id_seq; Type: SEQUENCE SET; Schema: kadrlar; Owner: -
--

SELECT pg_catalog.setval('kadrlar.is_tecrubesi_id_seq', 9, true);


--
-- Name: istifadeciler_id_seq; Type: SEQUENCE SET; Schema: kadrlar; Owner: -
--

SELECT pg_catalog.setval('kadrlar.istifadeciler_id_seq', 17, true);


--
-- Name: mezuniyyetler_id_seq; Type: SEQUENCE SET; Schema: kadrlar; Owner: -
--

SELECT pg_catalog.setval('kadrlar.mezuniyyetler_id_seq', 8, true);


--
-- Name: vezife_teyinatlari_id_seq; Type: SEQUENCE SET; Schema: kadrlar; Owner: -
--

SELECT pg_catalog.setval('kadrlar.vezife_teyinatlari_id_seq', 8, true);


--
-- Name: aktivler_id_seq; Type: SEQUENCE SET; Schema: logistika; Owner: -
--

SELECT pg_catalog.setval('logistika.aktivler_id_seq', 10, true);


--
-- Name: binalar_id_seq; Type: SEQUENCE SET; Schema: logistika; Owner: -
--

SELECT pg_catalog.setval('logistika.binalar_id_seq', 8, true);


--
-- Name: it_sistemleri_id_seq; Type: SEQUENCE SET; Schema: logistika; Owner: -
--

SELECT pg_catalog.setval('logistika.it_sistemleri_id_seq', 8, true);


--
-- Name: budce_id_seq; Type: SEQUENCE SET; Schema: maliyye; Owner: -
--

SELECT pg_catalog.setval('maliyye.budce_id_seq', 10, true);


--
-- Name: maliyye_emeliyyatlari_id_seq; Type: SEQUENCE SET; Schema: maliyye; Owner: -
--

SELECT pg_catalog.setval('maliyye.maliyye_emeliyyatlari_id_seq', 10, true);


--
-- Name: muqavileler_id_seq; Type: SEQUENCE SET; Schema: maliyye; Owner: -
--

SELECT pg_catalog.setval('maliyye.muqavileler_id_seq', 10, true);


--
-- Name: satinalmalar_id_seq; Type: SEQUENCE SET; Schema: maliyye; Owner: -
--

SELECT pg_catalog.setval('maliyye.satinalmalar_id_seq', 10, true);


--
-- Name: metodik_vesaitler_id_seq; Type: SEQUENCE SET; Schema: metodika; Owner: -
--

SELECT pg_catalog.setval('metodika.metodik_vesaitler_id_seq', 10, true);


--
-- Name: metodik_xidmetler_id_seq; Type: SEQUENCE SET; Schema: metodika; Owner: -
--

SELECT pg_catalog.setval('metodika.metodik_xidmetler_id_seq', 8, true);


--
-- Name: cinsiyyet_id_seq; Type: SEQUENCE SET; Schema: ortaq; Owner: -
--

SELECT pg_catalog.setval('ortaq.cinsiyyet_id_seq', 3, true);


--
-- Name: elmi_adlar_id_seq; Type: SEQUENCE SET; Schema: ortaq; Owner: -
--

SELECT pg_catalog.setval('ortaq.elmi_adlar_id_seq', 4, true);


--
-- Name: elmi_dereceler_id_seq; Type: SEQUENCE SET; Schema: ortaq; Owner: -
--

SELECT pg_catalog.setval('ortaq.elmi_dereceler_id_seq', 4, true);


--
-- Name: is_statuslari_id_seq; Type: SEQUENCE SET; Schema: ortaq; Owner: -
--

SELECT pg_catalog.setval('ortaq.is_statuslari_id_seq', 8, true);


--
-- Name: beynelxalq_qiymetlendirmeler_id_seq; Type: SEQUENCE SET; Schema: qiymetlendirme; Owner: -
--

SELECT pg_catalog.setval('qiymetlendirme.beynelxalq_qiymetlendirmeler_id_seq', 8, true);


--
-- Name: monitorinq_hesabatlari_id_seq; Type: SEQUENCE SET; Schema: qiymetlendirme; Owner: -
--

SELECT pg_catalog.setval('qiymetlendirme.monitorinq_hesabatlari_id_seq', 10, true);


--
-- Name: statistik_gostericiler_id_seq; Type: SEQUENCE SET; Schema: qiymetlendirme; Owner: -
--

SELECT pg_catalog.setval('qiymetlendirme.statistik_gostericiler_id_seq', 10, true);


--
-- Name: emrler_id_seq; Type: SEQUENCE SET; Schema: sened; Owner: -
--

SELECT pg_catalog.setval('sened.emrler_id_seq', 10, true);


--
-- Name: sened_novleri_id_seq; Type: SEQUENCE SET; Schema: sened; Owner: -
--

SELECT pg_catalog.setval('sened.sened_novleri_id_seq', 8, true);


--
-- Name: senedler_id_seq; Type: SEQUENCE SET; Schema: sened; Owner: -
--

SELECT pg_catalog.setval('sened.senedler_id_seq', 10, true);


--
-- Name: elmi_shura_iclaslari_id_seq; Type: SEQUENCE SET; Schema: struktur; Owner: -
--

SELECT pg_catalog.setval('struktur.elmi_shura_iclaslari_id_seq', 8, true);


--
-- Name: elmi_shura_qerarlari_id_seq; Type: SEQUENCE SET; Schema: struktur; Owner: -
--

SELECT pg_catalog.setval('struktur.elmi_shura_qerarlari_id_seq', 9, true);


--
-- Name: elmi_shura_uzvleri_id_seq; Type: SEQUENCE SET; Schema: struktur; Owner: -
--

SELECT pg_catalog.setval('struktur.elmi_shura_uzvleri_id_seq', 10, true);


--
-- Name: merkezler_id_seq; Type: SEQUENCE SET; Schema: struktur; Owner: -
--

SELECT pg_catalog.setval('struktur.merkezler_id_seq', 14, true);


--
-- Name: rehberlik_id_seq; Type: SEQUENCE SET; Schema: struktur; Owner: -
--

SELECT pg_catalog.setval('struktur.rehberlik_id_seq', 7, true);


--
-- Name: shobeler_id_seq; Type: SEQUENCE SET; Schema: struktur; Owner: -
--

SELECT pg_catalog.setval('struktur.shobeler_id_seq', 36, true);


--
-- Name: vezifeler_id_seq; Type: SEQUENCE SET; Schema: struktur; Owner: -
--

SELECT pg_catalog.setval('struktur.vezifeler_id_seq', 12, true);


--
-- Name: imtahanlar_id_seq; Type: SEQUENCE SET; Schema: tehsil; Owner: -
--

SELECT pg_catalog.setval('tehsil.imtahanlar_id_seq', 8, true);


--
-- Name: sertifikasiya_id_seq; Type: SEQUENCE SET; Schema: tehsil; Owner: -
--

SELECT pg_catalog.setval('tehsil.sertifikasiya_id_seq', 10, true);


--
-- Name: telim_istirakcilari_id_seq; Type: SEQUENCE SET; Schema: tehsil; Owner: -
--

SELECT pg_catalog.setval('tehsil.telim_istirakcilari_id_seq', 10, true);


--
-- Name: telim_proqramlari_id_seq; Type: SEQUENCE SET; Schema: tehsil; Owner: -
--

SELECT pg_catalog.setval('tehsil.telim_proqramlari_id_seq', 10, true);


--
-- Name: telim_qruplari_id_seq; Type: SEQUENCE SET; Schema: tehsil; Owner: -
--

SELECT pg_catalog.setval('tehsil.telim_qruplari_id_seq', 10, true);


--
-- PostgreSQL database dump complete
--

\unrestrict abVJVP8RHGXGZG6dfWnh5vgW6nsaidUMpmi0AstdCNBp1gE2AR3cvRFfsmaLM8p

