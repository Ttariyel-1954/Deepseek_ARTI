#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-3A — ADDIM 27–31 mətnləri.

Hər addım 4 hissədən ibarətdir:
  A      — «niyə» (geniş nəzəri izah)
  B      — kod (fayllar BACKEND qovluğundan canlı oxunur)
  C      — yoxlama əmrləri
  D      — həqiqi çıxış (qurucu tərəfindən icra olunur)
Əlavə: «Yeni anlayışlar», «Kodun sətir-sətir izahı», «Tez-tez verilən suallar».
"""

ADIMLAR = []


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 27 — PAROL HASH-LƏMƏSİ
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 27,
    "ad": "Parol təhlükəsizliyi — hash, duz və bcrypt",
    "a": """
<p>Bu günə qədər qurduğumuz sistemin <strong>birinci təhlükəsizlik
qaydası</strong> pozulub: heç bir istifadəçi yoxdur, heç bir yoxlama yoxdur.
İndi onu düzəldirik. Və hər şey <em>paroldan</em> başlayır.</p>

<h4>⚠️ Ən böyük səhv: parolu açıq saxlamaq</h4>
<p>Təsəvvül edin, bazada belə bir cədvəl var:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
email                  | parol
-----------------------+------------
admin@arti.edu.az      | 123456
muhendis@arti.edu.az   | 123456</pre>
<p>İndi sual verin: <strong>bu bazaya kim çıxış əldə edə bilər?</strong></p>
<ul>
  <li>Baza administratoru — həmişə.</li>
  <li>Ehtiyat nüsxəni (backup) ələ keçirən hər kəs.</li>
  <li>SQL inyeksiyası ilə sistemi deşən hücumçu.</li>
  <li>Bulud xidmətinin işçiləri.</li>
  <li>Loglara düşən sorğuları oxuyan hər kəs.</li>
  <li>Və ən vacibi — <strong>işdən çıxmış proqramçı</strong>.</li>
</ul>
<p>Və ən pisi nədir? İnsanlar <em>eyni parolu hər yerdə</em> işlədir.
Bankda, e-poçtda, Facebook-da. Bir baza sızması — yüzlərlə hesabın
itirilməsi deməkdir.</p>

<h4>Həll: HASH</h4>
<p><strong>Hash</strong> — məlumatı geri döndürülməz şəkildə
<em>barmaq izinə</em> çevirən funksiya.</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0"></th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">ŞİFRƏLƏMƏ (encryption)</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">HASH</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Geri döndürmə</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">✅ Mümkündür (açarla)</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">❌ Mümkün deyil</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Məqsəd</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Məlumatı gizlətmək</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Məlumatı <em>yoxlamaq</em></td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Nümunə</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">AES, RSA</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">bcrypt, Argon2, SHA-256</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Parol üçün</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">❌ Yaramır — açar oğurlansa hamısı açılır</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">✅ Düzgün seçim</td>
  </tr>
</table>
<p>Necə yoxlayırıq? İstifadəçi parolu göndərir → biz onu <em>yenidən
hash-ləyirik</em> → nəticəni bazadaki hash ilə tutuşduruq. Bazada
parolun özü <strong>heç vaxt yoxdur</strong>.</p>

<h4>⚠️ Duz (salt) — niyə mütləqdir</h4>
<p>Tutaq ki, duz yoxdur, sadəcə <code>hash(parol)</code>. O zaman:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
hash('123456') = '8d969eef6ecad3c2…'   ← HƏMİŞƏ eyni!</pre>
<p>İki istifadəçinin parolu eynidirsə, hash-i də <em>eyni olacaq</em>.
Və hücumçunun əlində <strong>rainbow table</strong> var: milyonlarla
parolun əvvəlcədən hesablanmış hash-ləri. Bir baxışla parolu tapır.</p>
<p><strong>Duz</strong> bunu həll edir: hər hash hesablanmadan əvvəl
parola <em>təsadüfi</em> mətn əlavə olunur və həmin duz hash-in
İÇİNDƏ saxlanılır.</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
hash('123456' + 'aB3$xK') = '$2b$10$aB3$xK…'   ← fərqli!
hash('123456' + 'pQ7!mZ') = '$2b$10$pQ7!mZ…'   ← fərqli!

// Yoxlayanda:
compare('123456', '$2b$10$aB3$xK…')
  → duzu hash-in İÇİNDƏN oxuyur ('aB3$xK')
  → eyni duzla yenidən hesablayır
  → uyğun gəlirsə true</pre>
<p>Nəticə: <strong>eyni parol → fərqli hash</strong>. Rainbow table
işləməz, çünki hər istifadəçinin duzu fərqlidir. Ölçdük: eyni parolla
üç hash hesabladıq və <em>üçü də fərqli</em> çıxdı.</p>

<h4>⚠️ Niyə bcrypt QƏSDƏN yavaşdır?</h4>
<p>Adi hash funksiyaları (SHA-256) <strong>sürətli</strong> olmaq üçün
yaradılıb — saniyədə milyardlarla hesablama. Parol üçün bu,
<em>fəlakətdir</em>: hücumçu qrafik prosessorla saniyədə milyardlarla
cəhd edə bilər.</p>
<p>bcrypt isə <strong>qəsdən yavaşdır</strong>. Onun «dərəcəsi»
(cost factor) 2<sup>n</sup> dövrə sayını təyin edir:</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Dərəcə</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Dövrə</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Vaxt (ölçülmüş)</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Saniyədə cəhd</th>
  </tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">10</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">1 024</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>49 ms</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">~20</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0">12</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">4 096</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>197 ms</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">~5</td></tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">14</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">16 384</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>788 ms</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">~1</td></tr>
</table>
<p>⚠️ Diqqət: hər artım dərəcəsi vaxtı <strong>İKİ DƏFƏ</strong>
artırır. 10 → 12 dörd dəfə, 10 → 14 on altı dəfə yavaş.</p>
<p><strong>Nə üçün bu bizə mane olmur?</strong> Çünki istifadəçi parolu
<em>bir dəfə</em> — girişdə — yazır. 200 millisaniyə hiss olunmur.
Hücumçu isə milyardlarla cəhd etməlidir: 200 ms × 1 000 000 =
<strong>2.3 gün</strong> yalnız bir parol üçün. Dərəcə 12 ilə bu,
9 günə çıxır.</p>
<p>Dərəcə 10 bu gün standartdır. Tövsiyə: hər 2–3 ildə bir dərəcəni
artırın (hesablamalar sürətlənir, ona görə eyni təhlükəsizliyi saxlamaq
üçün dərəcə də artmalıdır).</p>

<h4>⚠️ Şəffaf yüksəltmə (transparent upgrade)</h4>
<p>Dərəcəni artırdıqda <strong>köhnə hash-lər avtomatik güclənmir</strong>!
Bazada minlərlə istifadəçi varsa, hamısını bir gecədə yenidən
hash-ləmək mümkün deyil — çünki <em>açıq parolları bilmirik</em>.</p>
<p>Həll: istifadəçi növbəti dəfə giriş edəndə parol açıq formada
ələ düşür — <em>həmin anda</em> yeni dərəcə ilə yenidən hash-ləyirik:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
if (yenidenHashLazimdir(kohne_hash)) {
  const yeni = await hash(parol);           // yeni dərəcə ilə
  await update({ parol_hash: yeni });
}</pre>
<p>Beləliklə sistem tədricən «yüksəlir»: aktiv istifadəçilər ilk
həftədə, passivlər növbəti girişlərində.</p>

<h4>⚠️ bcrypt-in 72 simvol həddi</h4>
<p>bcrypt yalnız ilk <strong>72 baytı</strong> nəzərə alır. Yəni 100
simvolluq parolun son 28 simvolu <em>heç bir təsir göstərmir</em>.
Bu, təhlükəsizlik deyil, <em>sürprizdir</em>: istifadəçi uzun parol
yazdığını düşünür, əslində qısadır.</p>
<p>Ona görə DTO-da <code>@MaxLength(72)</code> qoyuruq — istifadəçiyə
<em>açıq</em> deyirik ki, bundan uzunu qəbul edilmir.</p>
""",
    "anlayis": [
        ("Hash",
         "Məlumatı geri döndürülməz şəkildə sabit uzunluqda mətnə çevirən "
         "funksiya. «Barmaq izi» — məlumatın özü deyil."),
        ("Duz (salt)",
         "Hər hash üçün təsadüfi əlavə olunan mətn. Eyni parolun fərqli "
         "hash verməsini təmin edir."),
        ("Rainbow table",
         "Milyonlarla parolun əvvəlcədən hesablanmış hash cədvəli. Duz "
         "olmadan işləyir, duzla işləməz."),
        ("bcrypt",
         "Parol üçün xüsusi hash alqoritmi. Qəsdən yavaşdır və duzu hash-in "
         "İÇİNDƏ saxlayır."),
        ("Dərəcə (cost factor)",
         "bcrypt-in yavaşlığını təyin edən ədəd. 2^n dövrə. Hər artım vaxtı "
         "iki dəfə artırır."),
        ("Şəffaf yüksəltmə",
         "Köhnə dərəcəli hash-i istifadəçinin girişi zamanı yeni dərəcə ilə "
         "yenidən hesablamaq."),
        ("Sabit vaxt (constant-time)",
         "Müqayisənin girişdən asılı olmayaraq eyni vaxt alması. Cavab "
         "müddətinə baxıb məlumat çıxarmağın qarşısını alır."),
        ("bcryptjs",
         "Təmiz JavaScript ilə yazılmış bcrypt. Native modul tələb etmir, "
         "ona görə quraşdırma problemi olmur."),
        ("72 bayt həddi",
         "bcrypt yalnız ilk 72 baytı nəzərə alır. Daha uzun hissə təsir "
         "etmir."),
        ("Xüsusi validatör",
         "class-validator-ın hazır dekoratorları kifayət etməyəndə yazılan "
         "öz yoxlama sinfi."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) <code>BCRYPT_DERECE</code> — bir yerdə təyin olunur</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export const BCRYPT_DERECE = 10;</pre>
<p>⚠️ Niyə sabit? Çünki dərəcə <em>hər yerdə eyni</em> olmalıdır: hash
hesablayanda, yoxlayanda və «yenidən hash lazımdırmı» qərarında. Üç
yerə ayrı-ayrı rəqəm yazsaq, biri dəyişəndə digərləri köhnə qalar.</p>

<h5 style="color:#334155;margin-top:1rem">2) <code>parolProblemleri()</code> — niyə boolean deyil, siyahı?</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export function parolProblemleri(parol: string, email?: string): string[] {
  const p: string[] = [];
  if (parol.length < 8) p.push('parol ən azı 8 simvol olmalıdır');
  ...
  return p;
}</pre>
<p>«Parol zəifdir» mesajı istifadəçiyə <strong>heç nə demir</strong>.
«Parolda ən azı bir rəqəm olmalıdır» isə dərhal həll yolunu göstərir.
Ona görə funksiya boolean yox, <em>siyahı</em> qaytarır.</p>
<p>⚠️ Funksiya <em>sinifdən kənar</em> (sadə funksiya) yazılıb, çünki
onu həm servis, həm xüsusi validatör, həm də testlər çağırır. Sinif
metodu olsaydı, hər yerdə nüsxə yaratmaq lazım gələrdi.</p>

<h5 style="color:#334155;margin-top:1rem">3) Niyə <code>Set</code>, massiv yox?</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const ZƏIF_PAROLLAR = new Set([...]);
if (ZƏIF_PAROLLAR.has(parol.toLowerCase())) { ... }</pre>
<p>Massivdə axtarış <strong>O(n)</strong>-dir — hər elementi yoxlayır.
<code>Set</code>-də isə <strong>O(1)</strong> — birbaşa baxır. Bizim
siyahı 24 elementdir, fərq görünməz. Amma real sistemdə belə siyahı
<em>on minlərlə</em> sətirdir və hər giriş cəhdində axtarılır. Ona görə
<code>Set</code> düzgün seçimdir.</p>

<h5 style="color:#334155;margin-top:1rem">4) Regex-lər — Azərbaycan hərfləri</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
if (!/[a-zəüöğışç]/.test(parol)) p.push('…kiçik hərf…');
if (!/[A-ZƏÜÖĞIŞÇ]/.test(parol)) p.push('…böyük hərf…');</pre>
<p>⚠️ <code>[a-z]</code> Azərbaycan hərflərini <em>tutmur</em>!
<code>ə</code>, <code>ü</code>, <code>ö</code>, <code>ğ</code>,
<code>ı</code>, <code>ş</code>, <code>ç</code> — bunlar ayrı
simvollardır və əlifbaya əlavə edilməlidir. Etməsəydik,
<code>GizliPərol123!</code> kimi parol «kiçik hərf yoxdur» deyə
rədd olunardı.</p>

<h5 style="color:#334155;margin-top:1rem">5) <code>parolGucu()</code> — 0–100 bal</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
let bal = Math.min(parol.length * 4, 40);   // uzunluq: ən çoxu 40 bal
if (/[a-zəüöğışç]/.test(parol)) bal += 10;
if (/[A-ZƏÜÖĞIŞÇ]/.test(parol)) bal += 15;
if (/[0-9]/.test(parol)) bal += 15;
if (/[^A-Za-z0-9]/.test(parol)) bal += 20;
if (ZƏIF_PAROLLAR.has(parol.toLowerCase())) bal = Math.min(bal, 10);</pre>
<p>Uzunluq <strong>40 balla</strong> məhdudlaşdırılıb — yoxsa 100
simvolluq sadə parol tam bal alardı. Əvəzində <em>müxtəliflik</em>
bal gətirir: ən çox bal xüsusi simvola verilir (20), çünki onu
tapmaq ən çətindir.</p>
<p>⚠️ Zəif parol üçün bal <strong>kəsilir</strong>
(<code>Math.min(bal, 10)</code>) — <code>123456</code> uzunluğa görə
24 bal alardı, kəsmə ilə 10 qalır.</p>

<h5 style="color:#334155;margin-top:1rem">6) <code>ParolService.yoxla()</code></h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
async yoxla(parol: string, hash: string): Promise<boolean> {
  if (!hash || !BCRYPT_RE.test(hash)) return false;
  try {
    return await bcrypt.compare(parol, hash);
  } catch {
    return false;
  }
}</pre>
<ul>
  <li><code>BCRYPT_RE</code> yoxlaması <strong>mütləqdir</strong>: zədələnmiş
      və ya boş hash ilə <code>compare</code> çağırsaq, bcrypt xəta atar.
      Biz isə xəta atmırıq — sadəcə «uyğun deyil» deyirik.</li>
  <li><code>try/catch</code> — son müdafiə xətti. İstənilən naməlum halda
      <code>false</code>: giriş <em>uğursuz</em> sayılır. Bu, təhlükəsiz
      standartdır — «bilmirəmsə, icazə vermirəm».</li>
  <li>⚠️ <code>===</code> ilə müqayisə <em>heç vaxt</em> işləməzdi, çünki
      hər hash fərqlidir (duz). Yalnız <code>compare</code> işləyir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">7) <code>skriptler/parol_yoxla.ts</code> — nə göstərir</h5>
<ol>
  <li>Hash parola bərabər deyil, uzunluğu 60 simvoldur.</li>
  <li>Eyni parolla <strong>üç fərqli hash</strong> — duz işləyir.</li>
  <li>Düzgün/səhv parol yoxlaması, bir simvol fərqi kifayətdir.</li>
  <li>Bazadaki <strong>REAL</strong> hash-i sınayır və demo parolunu tapır.</li>
  <li>Parol gücü qaydaları — 8 nümunə, hər birinin xətası ilə.</li>
  <li>Dərəcə 10/12/14 vaxtını ölçür.</li>
  <li>Şəffaf yüksəltmə məntiqini yoxlayır.</li>
</ol>
<p>⚠️ Diqqət yetirin: skript bazaya <strong>toxunmur</strong> — yalnız
<em>oxuyur</em>. Beləliklə təhlükəsizdir və istənilən vaxt işlədilə bilər.</p>
""",
    "fayllar": [
        "src/auth/parol.service.ts",
        "skriptler/parol_yoxla.ts",
    ],
    "goster": ["src/auth/istifadeci.service.ts"],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then echo "  ✓ tip xətası yoxdur"; else echo "  ✗ tip xətası var"; fi

echo ""
echo "════ 2) Paketlər ════"
node -e "
const p = require('./package.json');
for (const a of ['@nestjs/jwt', 'bcryptjs']) {
  console.log('      ' + a.padEnd(16) + (p.dependencies[a] ?? 'YOXDUR!'));
}
"
for d in @nestjs/jwt bcryptjs; do
  [ -d "node_modules/$d" ] && printf '      ✓ node_modules/%s\n' "$d" || printf '      ✗ node_modules/%s YOXDUR\n' "$d"
done

echo ""
echo "════ 3) Parol servisinin strukturu ════"
printf '      sətir sayı        : %s\n' "$(wc -l < src/auth/parol.service.ts | tr -d ' ')"
printf '      ixrac olunan sabit: %s\n' "$(grep -c '^export const' src/auth/parol.service.ts)"
printf '      ixrac olunan funksiya: %s\n' "$(grep -c '^export function' src/auth/parol.service.ts)"
echo "      ── metodlar ──"
grep -nE '^  (async )?[a-zA-Z]+\(' src/auth/parol.service.ts | sed 's/^/        /'

echo ""
echo "════ 4) Zəif parollar siyahısı ════"
python3 -c "
import re
s = open('src/auth/parol.service.ts', encoding='utf-8').read()
m = re.search(r'ZƏIF_PAROLLAR = new Set\(\[(.*?)\]\)', s, re.S)
ad = re.findall(r\"'([^']+)'\", m.group(1)) if m else []
print('      siyahıda %s parol var' % len(ad))
print('      nümunə:', ', '.join(ad[:8]), '…')
"

echo ""
echo "════ 5) CANLI parol yoxlaması ════"
npx tsx skriptler/parol_yoxla.ts
""",
    "olmaz": """Parolu AÇIQ saxlasaq:

CREATE TABLE istifadeciler (
  email text,
  parol text          -- ⚠️ AÇIQ PAROL!
);

SELECT * FROM istifadeciler;
     email            | parol
----------------------+----------
 admin@arti.edu.az    | 123456
 muhendis@arti.edu.az | 123456
 maliyyeci@arti.edu.az| 123456
 baxici@arti.edu.az   | 123456

  ← ⚠️ Baza administratoru HAMISININ parolunu görür.
  ← ⚠️ Ehtiyat nüsxə (backup) ələ keçsə — hamısı açıqdır.
  ← ⚠️ SQL inyeksiyası ilə «SELECT parol» — hamısı açıqdır.
  ← ⚠️ İnsanlar eyni parolu hər yerdə işlədir: e-poçt,
     bank, sosial şəbəkə. Bir sızma = onlarla hesab.

────────────────────────────────────────────────────────────
Duz (salt) olmasa:

hash('123456') = '8d969eef6ecad3c2…'   ← HƏMİŞƏ eyni
hash('123456') = '8d969eef6ecad3c2…'

SELECT email, parol_hash FROM istifadeciler;
 admin@    | 8d969eef6ecad3c2…
 muhendis@ | 8d969eef6ecad3c2…   ← ⚠️ EYNİ hash!
 baxici@   | 8d969eef6ecad3c2…

  ← ⚠️ Dərhal görünür ki, hamısı EYNİ parolu işlədir.
  ← ⚠️ Hücumçu rainbow table-dən bir baxışla parolu tapır:
     '123456' → 8d969eef6ecad3c2… — cədvəldə var.

────────────────────────────────────────────────────────────
Adi hash (SHA-256) işlətsək:

SHA-256 sürəti: ~10 000 000 000 hash/san (GPU ilə)
  → 8 simvolluq parollar: ~2 saat
  → 6 simvolluq parollar: ~1 saniyə

bcrypt (dərəcə 12): ~5 hash/san
  → 8 simvolluq parollar: ~6 000 il
  → 6 simvolluq parollar: ~2 gün

  ← ⚠️ Fərq 12 TƏRTİB: saatlar deyil, ƏSRLƏR.
  ← ⚠️ Sürətli hash parol üçün YARAMAZ — nə qədər
     «güclü» görünsə də.

────────────────────────────────────────────────────────────
72 simvol həddini yoxlamasaq:

parol = 'A'.repeat(100) + '123!'   (104 simvol)
hash('A'.repeat(72) + 'XXXXXXXX')  ===  hash('A'.repeat(100) + '123!')

  ← ⚠️ İstifadəçi 100 simvolluq parol yazdığını düşünür,
     əslində yalnız ilk 72-si işləyir. Son 32 simvol
     HEÇ BİR TƏSİR GÖSTƏRMİR.""",
    "c_izah": """
<p><strong>Birinci nəticə: duz (salt) işləyir.</strong> Eyni parolla
üç hash hesabladıq və <em>üçü də fərqli</em> çıxdı — amma hamısı həmin
parolu təsdiqləyir. Bu, rainbow table hücumunu tamamilə mənasız edir.</p>
<p><strong>İkincisi: bazadaki REAL hash-i sınadıq.</strong> Baza
dərslərində 4 istifadəçi <em>eyni hash</em> ilə yaradılmışdı — bu,
onların eyni parolu işlətdiyini göstərir. Skript namizəd siyahısından
parolu tapdı: <strong><code>123456</code></strong>. Və bizim qaydalar
onu dərhal <em>rədd etdi</em> — 5 fərqli səbəblə.</p>
<p>Bu, dərsin ən praktik nəticəsidir: <em>köhnə istifadəçilər işləməyə
davam edir</em> (giriş DTO-su güclülük yoxlamır), amma <strong>yeni</strong>
parollar güclü olacaq.</p>
<p><strong>Üçüncüsü: dərəcənin qiymətini ölçdük.</strong>
10 → 49 ms, 12 → 197 ms, 14 → 788 ms. Diqqət yetirin: hər artım
<em>təxminən iki dəfə</em> artırdı, dəqiq iki yox — çünki bcrypt
dərəcəni 2<sup>n</sup> dövrə kimi işlədir, ölçmə isə maşının yükündən
asılıdır.</p>
<p><strong>Dördüncüsü: 49 ms nə tez, nə yavaşdır.</strong> İstifadəçi
bunu hiss etmir, hücumçu isə saniyədə yalnız ~20 cəhd edə bilir.
Ayda 50 milyon cəhd — 8 simvolluq parol üçün bu, <em>kifayət deyil</em>.</p>
<p><strong>Beşincisi: şəffaf yüksəltmə işləyir.</strong> Dərəcə 8 ilə
hesablanmış hash üçün <code>yenidenHashLazimdir()</code> <code>true</code>
qaytardı, dərəcə 10 üçün isə <code>false</code>. Yəni sistem köhnə
hash-ləri tədricən gücləndirə bilir.</p>
""",
    "sual": [
        ("Hash-i geri qaytarmaq HƏQİQƏTƏN mümkün deyilmi?",
         "Riyazi olaraq mümkün deyil — hash funksiyası <em>çoxdan-birə</em> (many-to-one) çevrilmədir: sonsuz sayda mətn sonlu sayda hash verir. Amma praktikada <strong>zəif parolları tapmaq olar</strong>: namizədləri bir-bir sınamaqla (brute-force) və ya əvvəlcədən hesablanmış cədvəllərlə (rainbow table). Duz + yavaş alqoritm bunu qeyri-mümkün edir. Ona görə «hash geri qaytarılmır» demək <em>bir qədər</em> sadələşdirmədir."),
        ("Niyə SHA-256 + duz işlətməyik? Axı duz rainbow table-i həll edir.",
         "Duz rainbow table-i həll edir, amma <strong>sürəti</strong> həll etmir. Hücumçu hər namizəd üçün SHA-256 hesablayır və bu, GPU ilə saniyədə <em>milyardlarla</em> olur. Duz olsa belə, 8 simvolluq parolu saatlarla tapır. bcrypt isə hər cəhdi 50–200 ms edir — fərq <strong>12 tərtibdir</strong>. Duz qədər vacib olan <em>yavaşlıqdır</em>."),
        ("Dərəcəni 14 etsəm daha təhlükəsiz olmazmı?",
         "Olmaz — çünki <strong>istifadəçi 788 ms gözləyəcək</strong>. 10 istifadəçi eyni anda giriş etsə, serverin prosessoru boğulur (hər biri bir nüvəni tutur). Bu, «xidmətdən imtina» hücumunun əla hədəfi olur: hücumçu sadəcə minlərlə giriş cəhdi göndərir və serveri iflic edir. Ona görə dərəcə <em>balansdır</em>: təhlükəsizlik ↔ istifadəçi təcrübəsi. 10–12 arası optimaldır."),
        ("`bcryptjs` ilə `bcrypt` arasında nə fərq var?",
         "<code>bcrypt</code> — C++ ilə yazılmış <em>native</em> moduldur, 3–5 dəfə sürətlidir. Amma quraşdırma zamanı kompilyasiya tələb edir və bəzi mühitlərdə (Windows, Docker, ARM) problem yaradır. <code>bcryptjs</code> — təmiz JavaScript-dir, heç bir kompilyasiya lazım deyil, hər yerdə işləyir. Biz <em>təhsil layihəsi</em> üçün <code>bcryptjs</code> seçdik: quraşdırma problemi olmasın. İstehsalatda yük çox olarsa, <code>bcrypt</code> və ya <code>argon2</code>-yə keçmək olar."),
        ("Parolu «pepper» (istiot) ilə də qorumaq lazım deyilmi?",
         "<strong>Pepper</strong> — duzdan fərqli olaraq <em>bazada yox, tətbiqdə</em> saxlanılan gizli mətn. Yəni parol + duz + <em>pepper</em> hash-lənir. Faydası: baza sızsa belə, hücumçu pepper-i bilmir və hash-ləri <em>offline</em> sına bilmir. Çatışmazlığı: pepper dəyişsə, bütün parollar etibarsız olur; pepper itirsə, heç kim giriş edə bilmir. Praktikada böyük şirkətlər işlədir, kiçik layihələr üçün isə güclü duz + bcrypt kifayətdir."),
        ("Test mühitində bcrypt yavaşlığı problem deyilmi?",
         "Bəli, problemdir! 100 test × 5 hash × 50 ms = <strong>25 saniyə</strong> yalnız hash hesablamasına. Həllər: (1) test mühitində dərəcəni aşağı salmaq (<code>BCRYPT_DERECE</code>-i mühit dəyişəni ilə idarə etmək); (2) <code>ParolService</code>-i saxta (mock) versiya ilə əvəz etmək; (3) hash-i bir dəfə hesablayıb test boyu təkrar istifadə etmək. Bizim probe-lar <em>3A</em> üçün real bcrypt işlədir, çünki öyrənmək lazımdır — amma böyük test dəstində mock düzgün seçimdir."),
        ("İstifadəçi parolunu unutsa nə edirik? Hash-i geri qaytara bilmirik axı.",
         "Düzdür — <strong>heç vaxt</strong> geri qaytara bilmirik. Ona görə «parolu xatırlat» funksiyası <em>olmamalıdır</em> (əgər bir sistem parolunuzu sizə deyə bilirsə — o, parolları açıq saxlayır, uzaq durun!). Düzgün axın: <strong>sıfırlama</strong>. İstifadəçi e-poçtunu yazır → biz müvəqqəti <em>bir dəfəlik</em> token yaradırıq → e-poçtla link göndəririk → istifadəçi yeni parol təyin edir. Bu, 3B dərsinin mövzusudur."),
        ("Duzu harada saxlayırıq? Onu da oğurlaya bilməzlər?",
         "Duz hash-in <strong>İÇİNDƏDİR</strong> — ayrıca sütun deyil. bcrypt hash-in formatı belədir: <code>$2b$10$&lt;22 simvol duz&gt;&lt;31 simvol hash&gt;</code>. Ona görə duz bazadan oxunur və yoxlama üçün istifadə olunur. ⚠️ Duz <em>sirr deyil</em> — o, açıq ola bilər. Onun işi sirr saxlamaq yox, <em>hər hash-i unikal etməkdir</em>. Sirr olan yeganə şey <code>JWT_SECRET</code>-dir (ADDIM 29)."),
        ("Parolu bazadan oxuyub yoxlaya bilərikmi, axı hash var?",
         "Xeyr, və bu, düzgün sualdır. <strong>Hash ilə hash-i müqayisə etmək olmaz</strong> — çünki hər hash-in duzu fərqlidir. <code>hash(parol) === bazadaki_hash</code> heç vaxt doğru olmaz. Yeganə yol: <code>bcrypt.compare(göndərilən_parol, bazadaki_hash)</code> — bu, duzu hash-dən oxuyur, parolu həmin duzla yenidən hash-ləyir və müqayisə edir."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>Parol servisi <strong>25 yoxlamadan</strong> keçdi.</li>
  <li><strong>Hash parol deyil:</strong> uzunluğu 60 simvol, prefiksi
      <code>$2b$10$</code>.</li>
  <li><strong>Duz işləyir:</strong> eyni parol → <em>üç fərqli</em> hash,
      hamısı eyni parolu təsdiqləyir.</li>
  <li><strong>Bazadaki REAL hash:</strong> 4 istifadəçi eyni hash-i
      paylaşır və demo parolu <code>123456</code>-dır — qaydalarımız
      onu <strong>5 səbəblə</strong> rədd edir.</li>
  <li><strong>Dərəcə vaxtı (ölçülmüş):</strong> 10 → <strong>49 ms</strong>,
      12 → <strong>197 ms</strong>, 14 → <strong>788 ms</strong>.</li>
  <li><strong>Şəffaf yüksəltmə:</strong> dərəcə 8 → yenidən hash lazım,
      dərəcə 10 → lazım deyil.</li>
  <li><strong>Zəif parol balı kəsilir:</strong> <code>123456</code> → 10 bal,
      <code>GizliParol123!</code> → 100 bal.</li>
</ul>
<p><strong>Ən vacib dərs:</strong> parol <em>heç vaxt</em> açıq
saxlanılmır, <em>heç vaxt</em> geri qaytarılmır və <em>həmişə</em>
duzla, yavaş alqoritmlə hash-lənir. Bu üç qayda pozulsa, bütün digər
təhlükəsizlik tədbirləri mənasız olur.</p>
<p>Növbəti addımda bu hash-i <strong>istifadəçi servisində</strong>
işlədəcəyik: qeydiyyat, giriş və parolun heç vaxt API-dən
qaytarılmaması.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 28 — İSTİFADƏÇİ SERVİSİ
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 28,
    "ad": "İstifadəçi servisi — qeydiyyat və parol yoxlaması",
    "a": """
<p>Parolu hash-ləməyi öyrəndik. İndi onu <strong>istifadəçi axınına</strong>
qoşuruq: qeydiyyat, giriş və istifadəçi siyahısı.</p>

<h4>⚠️⚠️ ƏN VACİB TƏHLÜKƏSİZLİK QAYDASI: parol_hash API-dən ÇIXMAMALIDIR</h4>
<p>Bu, o qədər vacibdir ki, ayrıca izah edirik. Təsəvvül edin:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
$ curl http://localhost:4000/api/v1/auth/istifadeciler

[
  { "id": 2, "email": "admin@arti.edu.az",
    "parol_hash": "$2b$10$oIesQsaJ4ahBc0vjhaRpN.xkamY6eC.SH2byHZThjU8YmVm5UMsOq",
    "rol": "admin" }
]</pre>
<p>Nə olub? <strong>Bütün parol hash-ləri açıq şəkildə yayımlanıb.</strong>
İndi hücumçu:</p>
<ol>
  <li>Hash-ləri <em>offline</em> sındırmağa başlayır — server onu görmür,
      <strong>bloklama mümkün deyil</strong>.</li>
  <li>Rainbow table-də axtarır: <code>123456</code> tapılır.</li>
  <li>Zəif parolları sındıraraq sistemə girir.</li>
  <li>Eyni parolu başqa saytlarda sınayır (insanlar təkrar işlədir).</li>
</ol>

<h4>Həll: hash-i bazadan HEÇ OXUMAMAQ</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export const ISTIFADECI_SECIM = {
  id: true,
  email: true,
  ad_soyad: true,
  rol: true,
  aktiv: true,
  emekdas_id: true,
  yaradilma: true,
  // parol_hash: true,   ← ⚠️ BU SƏTİR YOXDUR!
} as const;</pre>
<p>İki yanaşma var, biz <strong>ikincisini</strong> seçirik:</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Yanaşma</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Nə edir</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Risk</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Oxu, sonra sil</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Bütün sütunları oxuyur,
        <code>delete</code> ilə hash-i çıxarır</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">⚠️ <code>delete</code>
        sətrini bir gün unudan kimsə hamısını yayımlayar</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Heç oxumamaq</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>select</code> ilə
        yalnız lazım olan sütunlar</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">✅ Hash bazadan
        <em>fiziki olaraq</em> gəlmir — sızması mümkün deyil</td>
  </tr>
</table>
<p>⚠️ Üstəlik <code>GetPayload</code> ilə <strong>tip</strong> də çıxarırıq:
<code>IstifadeciCavabi</code> interfeysində <code>parol_hash</code> yoxdur,
ona görə TypeScript onu qaytarmağa <em>icazə verməz</em>. İkiqat qoruma:
baza səviyyəsində və tip səviyyəsində.</p>

<h4>⚠️ İmtiyaz yüksəltmə (privilege escalation)</h4>
<p>Qeydiyyat DTO-sunda <code>rol</code> sahəsi <strong>yoxdur</strong>.
Səbəb: əgər olsaydı, hər kəs özünə <code>admin</code> hüququ verə bilərdi:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
POST /api/v1/auth/qeydiyyat
{ "email": "hucumcu@example.com",
  "parol": "GucluParol123!",
  "ad_soyad": "Hücumçu",
  "rol": "admin" }          ← ⚠️ ÖZÜNƏ ADMIN HÜQUQU VERİR!</pre>
<p>Bu, <strong>OWASP Top 10</strong> siyahısındadır və ən çox rast gəlinən
API səhvlərindən biridir. Qayda: <em>istifadəçi öz hüququnu təyin edə
bilməz</em>. Rol yalnız mövcud admin tərəfindən verilir.</p>
<p>Bizim DTO-da <code>rol</code> yoxdur, ona görə
<code>forbidNonWhitelisted</code> onu <strong>400 ilə rədd edir</strong> —
sükutla silmir, açıq şəkildə «bu sahə olmamalıdır» deyir.</p>

<h4>⚠️ İstifadəçi siyahısının çıxarılması (user enumeration)</h4>
<p>Giriş uğursuz olanda hansı mesajı veririk?</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
// ❌ PİS — hücumçu e-poçtların mövcudluğunu öyrənir
if (!istifadeci) throw new NotFoundException('Bu e-poçt tapılmadı');
if (!parolUygun) throw new UnauthorizedException('Parol səhvdir');

// ✅ YAXŞI — hər iki hal eyni cavabı verir
if (!istifadeci || !parolUygun) {
  throw new UnauthorizedException('E-poçt və ya parol səhvdir');
}</pre>
<p>Niyə vacibdir? Çünki hücumçu əvvəlcə <em>hansı e-poçtların
mövcud olduğunu</em> öyrənir, sonra yalnız onlara hücum edir. 10 000
e-poçtdan 200-nü tapsa, işi 50 dəfə asanlaşır.</p>
<p>Biz daha incə bir şey də edirik: <strong>vaxt bərabərləşdirməsi</strong>.
İstifadəçi tapılmayanda da bcrypt hesablaması aparırıq — yoxsa cavab
müddətinə baxıb «bu e-poçt yoxdur» olduğunu anlamaq mümkün olardı
(hash hesablama 49 ms çəkir, tapılmayan hal isə dərhal cavab verərdi).</p>

<h4>⚠️ İki fərqli DTO — qeydiyyat və giriş</h4>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0"></th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">QeydiyyatDto</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">GirisDto</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Parol qaydaları</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Tam güclülük yoxlaması</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Yalnız «boş deyil»</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Niyə?</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Yeni parol güclü olmalıdır</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Köhnə zəif parollu istifadəçilər
        giriş edə bilməlidir</td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong><code>rol</code> sahəsi</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">❌ Yoxdur</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">❌ Yoxdur</td>
  </tr>
</table>
<p>⚠️ Əgər giriş DTO-sunda da güclülük yoxlasaydıq, bazadaki 4 demo
istifadəçi (<code>123456</code> parolu ilə) <strong>heç vaxt giriş edə
bilməzdi</strong>. Bu, çox real bir problemdir: qaydalar sərtləşəndə
köhnə istifadəçiləri kilidləmək olmaz.</p>

<h4>⚠️ E-poçtun normallaşdırılması</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const email = dto.email.trim().toLowerCase();</pre>
<p>Niyə? Çünki <code>Admin@Arti.edu.az</code> və
<code>admin@arti.edu.az</code> — <em>texniki olaraq fərqli</em>
mətnlərdir (bazada iki ayrı sətir olardı). Amma insan üçün eynidir.
Normallaşdırmasaq:</p>
<ul>
  <li>İstifadəçi böyük hərflə qeydiyyatdan keçir, kiçik hərflə giriş
      etməyə çalışır → <strong>girə bilmir</strong>.</li>
  <li>Hücumçu eyni e-poçtu böyük hərflə yenidən qeydiyyatdan keçirib
      <em>ikinci hesab</em> yaradır.</li>
</ul>
<p>⚠️ Qeyd: <code>toLowerCase()</code> Azərbaycan <code>İ</code>/<code>I</code>
hərfləri ilə problem yarada bilər (Türk dillərində xüsusi haldır).
E-poçt ünvanları üçün isə beynəlxalq standart <em>ASCII</em>-dir, ona görə
problem yoxdur.</p>
""",
    "anlayis": [
        ("İmtiyaz yüksəltmə",
         "İstifadəçinin öz hüququnu artıra bilməsi. Məsələn qeydiyyatda "
         "«rol: admin» göndərmək."),
        ("İstifadəçi siyahısının çıxarılması",
         "«Bu e-poçt mövcuddurmu?» sualına cavab verərək sistemin "
         "istifadəçi siyahısını öyrənmək."),
        ("Vaxt bərabərləşdirməsi",
         "Müxtəlif hallarda eyni cavab müddətini saxlamaq. Cavab vaxtına "
         "baxıb məlumat çıxarmağın qarşısını alır."),
        ("Normallaşdırma",
         "Məlumatı müqayisədən əvvəl standart formaya salmaq — məsələn "
         "e-poçtu kiçik hərflərə çevirmək."),
        ("select + GetPayload",
         "Prisma-da yalnız lazım olan sütunları oxumaq və tipi ondan "
         "avtomatik çıxarmaq."),
        ("İkiqat qoruma",
         "Eyni riskin iki müstəqil qatla qarşısını almaq: bazada "
         "<code>select</code>, kodda isə tip."),
        ("Şəffaf yüksəltmə",
         "Köhnə bcrypt dərəcəli hash-i istifadəçinin girişi zamanı "
         "yeniləmək."),
        ("Deaktiv hesab",
         "<code>aktiv = false</code>. Sətir bazada qalır, amma giriş "
         "mümkün olmur (403) — hesabı silmək lazım deyil."),
        ("409 Konflikt",
         "Resurs artıq mövcuddur (məsələn e-poçt qeydiyyatdadır). "
         "Sorğu düzgündür — problem vəziyyətdədir."),
        ("404 Tapılmadı",
         "Sorğuda göstərilən resurs (ID) bazada yoxdur."),
        ("500 Daxili xəta",
         "⚠️ Gözlənilməz xəta. «Server xarabdır» deməkdir — monitorinq "
         "alarm verir, ona görə 500-ə <em>yol verilməməlidir</em>."),
        ("Rol idarəsi",
         "Rolun kim tərəfindən dəyişilə biləcəyi. Bizdə YALNIZ admin, "
         "ayrıca endpoint ilə."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) <code>ISTIFADECI_SECIM</code> + <code>GetPayload</code></h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export const ISTIFADECI_SECIM = {
  id: true, email: true, ad_soyad: true,
  rol: true, aktiv: true, emekdas_id: true, yaradilma: true,
} as const;

export type IstifadeciSetiri = Prisma.istifadecilerGetPayload&lt;{
  select: typeof ISTIFADECI_SECIM;
}&gt;;</pre>
<p><code>as const</code> olmasa TypeScript tipi ümumiləşdirər və
<code>GetPayload</code> dəqiq nəticə çıxara bilməz. Bu naxışı 2A-nın
ADDIM 18-də <code>EMEKDAS_SECIM</code> üçün görmüşdük — indi təkrar
istifadə edirik.</p>

<h5 style="color:#334155;margin-top:1rem">2) <code>qeydiyyat()</code> — parol hash-lənir</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const email = dto.email.trim().toLowerCase();
const parol_hash = await this.parol.hash(dto.parol);

const setir = await this.prisma.istifadeciler.create({
  data: {
    email, parol_hash, ad_soyad: dto.ad_soyad.trim(),
    rol: STANDART_ROL,
    emekdas_id: dto.emekdas_id === undefined ? null : BigInt(dto.emekdas_id),
  },
  select: ISTIFADECI_SECIM,
});</pre>
<ul>
  <li>⚠️ <code>parol</code> sahəsi <strong>heç vaxt</strong> <code>data</code>
      obyektinə düşmür — yalnız <code>parol_hash</code>.</li>
  <li><code>rol: STANDART_ROL</code> — sabit <code>'baxici'</code>. DTO-dan
      gəlmir, çünki gəlsəydi imtiyaz yüksəltmə olardı.</li>
  <li><code>emekdas_id === undefined ? null : BigInt(...)</code> —
      ⚠️ <code>dto.emekdas_id ? ... : null</code> yazsaydıq,
      <code>0</code> dəyəri də <code>null</code> olardı. Bizim ID-lər
      1-dən başlayır, amma prinsipcə <code>??</code> və ya
      <code>=== undefined</code> düzgün yoldur.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3) <code>daxiliTap()</code> — private metod</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
private async daxiliTap(email: string): Promise&lt;{
  setir: IstifadeciSetiri;
  parol_hash: string;
} | null&gt; {
  const e = await this.prisma.istifadeciler.findUnique({
    where: { email: email.trim().toLowerCase() },
    select: { ...ISTIFADECI_SECIM, parol_hash: true },   // ← hash də oxunur!
  });
  if (!e) return null;
  const { parol_hash, ...qalan } = e;                    // ← hash AYRILIR
  return { setir: qalan as IstifadeciSetiri, parol_hash };
}</pre>
<ul>
  <li>⚠️ <strong>Bu, yeganə yerdir ki, hash oxunur</strong> — və yalnız
      parol yoxlaması üçün. Metod <code>private</code>-dir: controller
      onu çağıra bilməz.</li>
  <li><code>{ parol_hash, ...qalan } = e</code> — <em>obyekt
      destrukturizasiyası</em> ilə hash-i ayırırıq. Qalan sahələr
      <code>qalan</code> dəyişəninə düşür və <strong>təmiz</strong> tip
      kimi qaytarılır.</li>
  <li><code>as IstifadeciSetiri</code> — tip çevirməsi. Zəruridir, çünki
      destrukturizasiyadan sonra TypeScript <code>qalan</code>-ı
      <code>Object</code> kimi görür.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">4) <code>parolYoxla()</code> — vaxt bərabərləşdirməsi</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
private static readonly SAXTA_HASH =
  '$2b$10$oIesQsaJ4ahBc0vjhaRpN.xkamY6eC.SH2byHZThjU8YmVm5UMsOq';

if (!tapilan) {
  await this.parol.yoxla(parol, IstifadeciService.SAXTA_HASH);   // ← 49 ms
  this.log.warn(`Uğursuz giriş cəhdi: ${email} (istifadəçi yoxdur)`);
  return null;
}</pre>
<ul>
  <li>⚠️ <code>SAXTA_HASH</code> — <em>real</em> bcrypt hash (bazadaki
      demo hash). Onunla müqayisə <strong>həmişə uğursuz</strong> olur,
      amma <em>49 ms çəkir</em> — yəni cavab müddəti eyni qalır.</li>
  <li>Bu olmasaydı: mövcud e-poçt → 49 ms, mövcud olmayan → 1 ms.
      Hücumçu ölçmə ilə e-poçtların siyahısını çıxarardı.</li>
  <li>⚠️ Niyə <code>static</code>? Çünki bu sabit bütün nüsxələr üçün
      eynidir; hər servis nüsxəsində təkrar saxlamaq lazım deyil.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">5) Şəffaf yüksəltmə girişdə</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
if (this.parol.yenidenHashLazimdir(tapilan.parol_hash)) {
  const yeni = await this.parol.hash(parol);
  await this.prisma.istifadeciler.update({
    where: { id: tapilan.setir.id },
    data: { parol_hash: yeni },
  });
  this.log.log(`Parol hash-i yeniləndi (şəffaf yüksəltmə): ${email}`);
}</pre>
<p>⚠️ Bu <strong>yalnız girişdə</strong> mümkündür — çünki parol açıq
formada yalnız o anda ələ düşür. Diqqət: yeniləmə <em>uğurlu girişdən
sonra</em> olur, yoxsa yanlış parol göndərən şəxs hash-i dəyişə bilərdi.</p>

<h5 style="color:#334155;margin-top:1rem">6) <code>rolDeyis()</code> — əlavə yoxlama</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
if (!ROLLAR.includes(rol)) {
  throw new BadRequestException(
    `rol yalnız bunlardan biri ola bilər: ${ROLLAR.join(', ')}`,
  );
}</pre>
<p>⚠️ Niyə əlavə yoxlama, axı DTO-da <code>@IsIn(ROLLAR)</code> var?
Çünki servisi <em>birbaşa</em> çağıran kod (məsələn başqa servis, cron
işi, skript) DTO-dan keçmir. <strong>Servis öz girişini özü qorumalıdır</strong> —
DTO yalnız HTTP qatı üçündür.</p>

<h5 style="color:#334155;margin-top:1rem">6b) <code>movcuddur()</code> — 500 yerinə 404</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
private async movcuddur(id: number): Promise&lt;void&gt; {
  const v = await this.prisma.istifadeciler.findUnique({
    where: { id },
    select: { id: true },
  });
  if (!v) throw new NotFoundException(`ID ${id} olan istifadəçi tapılmadı`);
}

async rolDeyis(id: number, rol: Rol): Promise&lt;IstifadeciCavabi&gt; {
  if (!ROLLAR.includes(rol)) { ... }
  await this.movcuddur(id);          // ← ⚠️ VACİB
  const setir = await this.prisma.istifadeciler.update({ ... });
}</pre>
<p>⚠️ <strong>Bu yoxlama olmasa nə olur?</strong> Prisma-nın
<code>update</code> əməliyyatı mövcud olmayan ID üçün
<code>P2025</code> xətası atır — və bu, <em>xam</em> xəta kimi
yuxarı qalxır:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
$ curl -X PATCH .../auth/istifadeci/999999/rol -d '{"rol":"baxici"}'
HTTP/1.1 500 Internal Server Error
{"statusCode":500,"message":"Internal server error"}    ⚠️

  ⚠️ 500 «server xarabdır» deməkdir — monitorinq ALARM verir,
     inzibatçı loqları qazır, halbuki problem sadəcə səhv ID-dir.
  ✓ Düzgün cavab: 404 Not Found + aydın mesaj.
</pre>
<p>⚠️ Həm də <code>select: { id: true }</code> yazmağımız vacibdir —
yoxsa mövcudluğu yoxlamaq üçün <em>bütün</em> sətri (o cümlədən
parol hash-ini) bazadan çəkərdik. Yalnız lazım olan sütunu oxuyuruq.</p>
<p>Alternativ yol: <code>update</code>-i <code>try/catch</code> içinə alıb
<code>P2025</code>-i tutmaq. Hər iki yol işləyir; bizim seçim
<em>açıq</em> və <em>oxunaqlı</em>dır — xəta idarəsi «gözlənilməz»
yerə deyil, metodun <em>başında</em> görünür.</p>

<h5 style="color:#334155;margin-top:1rem">7) Xüsusi validatör — <code>@Validate(GucluParolValidator)</code></h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@ValidatorConstraint({ name: 'gucluParol', async: false })
export class GucluParolValidator implements ValidatorConstraintInterface {
  validate(parol: unknown, args: ValidationArguments): boolean {
    const obyekt = args.object as { email?: string };
    return parolProblemleri(parol as string, obyekt.email).length === 0;
  }
  defaultMessage(args: ValidationArguments): string { ... }
}</pre>
<ul>
  <li><code>ValidatorConstraint</code> — class-validator-ın xüsusi
      validatör sinfi üçün baza dekoratoru.</li>
  <li>⚠️ <code>args.object</code> — <strong>BÜTÜN</strong> obyektə çıxış.
      Ona görə parolu <em>e-poçtla birlikdə</em> yoxlaya bilirik:
      «parol e-poçtun hissəsini ehtiva edirmi?»</li>
  <li><code>async: false</code> — validatör sinxrondur. Assinxron olsaydı
      (məsələn bazaya sorğu), <code>async: true</code> yazardıq.</li>
  <li><code>defaultMessage</code> — bütün pozulmuş qaydaları bir yerdə
      göstərir. Ona görə DTO-da <code>@MinLength(8)</code> YOXDUR —
      təkrar mesaj olmaması üçün.</li>
</ul>
""",
    "fayllar": [
        "src/auth/dto/parol.validator.ts",
        "src/auth/dto/qeydiyyat.dto.ts",
        "src/auth/dto/giris.dto.ts",
        "src/auth/istifadeci.service.ts",
        "skriptler/istifadeci_yoxla.ts",
    ],
    "goster": ["src/auth/parol.service.ts"],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then echo "  ✓ tip xətası yoxdur"; else echo "  ✗ tip xətası var"; fi

echo ""
echo "════ 2) Fayllar ════"
for f in src/auth/dto/parol.validator.ts src/auth/dto/qeydiyyat.dto.ts \
         src/auth/dto/giris.dto.ts src/auth/istifadeci.service.ts; do
  printf '      %-42s %4s sətir\n' "$f" "$(wc -l < "$f" | tr -d ' ')"
done

echo ""
echo "════ 3) Təhlükəsizlik qaydaları ════"
S=src/auth/istifadeci.service.ts
grep -q 'parol_hash: true' "$S" && echo "      ⚠️ hash oxunur (yalnız daxiliTap-də olmalıdır)"
printf '      parol_hash oxunan yer : %s\n' "$(grep -c 'parol_hash: true' "$S")"
printf '      parol_hash ixrac olunur: %s\n' "$(grep -c 'parol_hash' src/auth/dto/qeydiyyat.dto.ts)"
if grep -q 'parol_hash' src/auth/dto/qeydiyyat.dto.ts; then
  echo "      ✗ TƏHLÜKƏ: DTO-da parol_hash var!"
else
  echo "      ✓ DTO-larda parol_hash YOXDUR"
fi
printf '      «rol» QeydiyyatDto-da : %s (0 olmalıdır)\n' "$(grep -c 'rol!' src/auth/dto/qeydiyyat.dto.ts)"
grep -q 'SAXTA_HASH' "$S" && echo "      ✓ vaxt bərabərləşdirməsi var (SAXTA_HASH)"
grep -q 'toLowerCase()' "$S" && echo "      ✓ e-poçt normallaşdırılır"

echo ""
echo "════ 4) Bazadaki istifadəçilər (hash GÖSTƏRİLMİR) ════"
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
psql "$DBURL" -c "
SELECT id, email, ad_soyad, rol, aktiv, length(parol_hash) AS hash_uzunlugu
  FROM kadrlar.istifadeciler ORDER BY id;" 2>/dev/null | sed 's/^/      /'

echo ""
echo "════ 5) CANLI istifadəçi servisi yoxlaması ════"
npx tsx skriptler/istifadeci_yoxla.ts
""",
    "olmaz": """`parol_hash` API-dən çıxsa:

$ curl http://localhost:4000/api/v1/auth/istifadeciler

[
  { "id": 2, "email": "admin@arti.edu.az", "rol": "admin",
    "parol_hash": "$2b$10$oIesQsaJ4ahBc0vjhaRpN.xkamY6eC.SH2byHZThjU8YmVm5UMsOq" },
  { "id": 3, "email": "muhendis@arti.edu.az", "rol": "muhendis",
    "parol_hash": "$2b$10$oIesQsaJ4ahBc0vjhaRpN.xkamY6eC.SH2byHZThjU8YmVm5UMsOq" },
  ...
]

  ← ⚠️ Hücumçu hash-ləri OFFLINE sındırmağa başlayır.
     Server bunu GÖRMÜR — bloklama mümkün deyil.
  ← ⚠️ Rainboq table: '123456' → tapıldı.
  ← ⚠️ Eyni hash 4 istifadəçidədir → BİR sındırma,
     DÖRD hesab.

────────────────────────────────────────────────────────────
`rol` sahəsi qeydiyyatda qəbul edilsə:

$ curl -X POST .../auth/qeydiyyat -d '{
    "email":"hucumcu@example.com",
    "parol":"GucluParol123!",
    "ad_soyad":"Hücumçu",
    "rol":"admin" }'

HTTP/1.1 201 Created
{"id":17,"email":"hucumcu@example.com","rol":"admin"}

  ← ⚠️ 5 saniyə ərzində SİSTEMİN ADMİNİ oldu.
     Bütün istifadəçiləri silə, məlumatı dəyişə bilər.
  ← Bu, OWASP Top 10 siyahısındadır və ən çox
     rast gəlinən API səhvidir.

────────────────────────────────────────────────────────────
Fərqli xəta mesajları versək:

$ curl -X POST .../auth/giris -d '{"email":"yoxdur@a.az","parol":"x"}'
HTTP/1.1 404 {"xeta":{"kod":"TAPILMADI","mesaj":"Bu e-poçt tapılmadı"}}

$ curl -X POST .../auth/giris -d '{"email":"admin@arti.edu.az","parol":"x"}'
HTTP/1.1 401 {"xeta":{"kod":"AUTENTIFIKASIYA_LAZIM","mesaj":"Parol səhvdır"}}

  ← ⚠️ Hücumçu 10 000 e-poçt yoxlayıb 200 mövcud olanı
     TAPIR. Sonra yalnız onlara hücum edir — işi 50 dəfə asan.

────────────────────────────────────────────────────────────
Vaxt bərabərləşdirməsi olmasa:

$ time curl -X POST .../auth/giris -d '{...,"email":"yoxdur@a.az"}'
real  0m0.003s        ← ⚠️ 3 ms (hash hesablanmadı)

$ time curl -X POST .../auth/giris -d '{...,"email":"admin@arti.edu.az"}'
real  0m0.052s        ← ⚠️ 52 ms (hash hesablandı)

  ← ⚠️ CAVAB MÜDDƏTİ e-poçtun mövcudluğunu SIZDIRIR.
     «404 vs 401» mesajını düzəltsək belə, vaxt danışır.""",
    "c_izah": """
<p><strong>Birinci nəticə: hash heç vaxt API-dən çıxmır.</strong>
Skript 37 yoxlamadan keçdi və `hamisi()` nəticəsini <em>mətn kimi</em>
yoxlayır — <code>JSON.stringify(hamisi).includes('parol_hash')</code>.
Bu, ən sadə və ən etibarlı yoxlamadır: cavabda o sahə varsa, test
uğursuz olur.</p>
<p><strong>İkincisi: DTO validasiyası zəif parolları rədd edir.</strong>
10 nümunə sınandı: <code>123456</code> (bazadaki demo parolu), kiçik
hərfsiz, xüsusi simvolsuz, rəqəmsiz, e-poçtun hissəsini ehtiva edən,
qısa, səhv e-poçt — hamısı <code>400</code> aldı. Yalnız güclü parol
keçdi.</p>
<p><strong>Üçüncüsü: <code>rol</code> göndərmək cəhdi rədd edilir.</strong>
<code>property rol should not exist</code> — bu,
<code>forbidNonWhitelisted</code>-in sayəsindədir. Sükutla silinsəydi,
istifadəçi «admin oldum?» deyə çaşardı; 400 isə problemi
<em>dərhal</em> göstərir.</p>
<p><strong>Dördüncüsü: giriş DTO-su zəif parolu qəbul edir.</strong>
Bu, qəsdəndir: bazadaki 4 istifadəçi <code>123456</code> ilə işləyir və
onlar giriş edə bilməlidir. Probel <em>dördü ilə də</em> giriş etdi və
hər birinin rolu düzgün gəldi: <code>admin</code>, <code>muhendis</code>,
<code>maliyyeci</code>, <code>baxici</code>.</p>
<p><strong>Beşincisi: «səhv parol» və «istifadəçi yoxdur» eyni cavabı
verir.</strong> Hər ikisi <code>null</code> qaytarır, hər ikisi 49 ms
çəkir. Hücumçu hansı e-poçtun mövcud olduğunu <em>müəyyən edə bilmir</em>.</p>
""",
    "sual": [
        ("Niyə `select` işlədirik, `omit` (Prisma 5+) yox?",
         "Hər ikisi işləyir. <code>omit: { parol_hash: true }</code> daha qısadır və yeni sütun əlavə olunanda avtomatik daxil olur. Amma <strong>təhlükəsizlik baxımından <code>select</code> daha yaxşıdır</strong>: «ağ siyahı» prinsipidir — yalnız açıq sadalananlar çıxır. <code>omit</code> isə «qara siyahı»dır: yeni həssas sütun əlavə etsək (məsələn <code>fin_kod</code>), onu <code>omit</code>-ə əlavə etməyi <em>unuda</em> bilərik və sızacaq. <code>select</code> ilə bu mümkün deyil."),
        ("`daxiliTap` metodunu `private` etmək kifayətdirmi?",
         "TypeScript-də <code>private</code> yalnız <em>yazma vaxtı</em> qoruyur — koda çevriləndə silinir və işləmə vaxtında heç nə mane olmur. Ona görə bu, <strong>təhlükəsizlik qatı deyil, niyyət bildirgisidir</strong>. Əsl qoruma: (1) metod yalnız hash-i <em>daxildə</em> saxlayır və qaytararkən ayırır; (2) controller-də belə metod yoxdur; (3) testdə cavabın mətnini yoxlayırıq."),
        ("Vaxt bərabərləşdirməsi həqiqətən lazımdırmı? Bu, çox incə deyilmi?",
         "Bəli, incədir — amma <strong>real hücumlarda istifadə olunur</strong> (<em>timing attack</em>). Praktikada şəbəkə gecikməsi ölçməni çətinləşdirir, ona görə hücumçu <em>minlərlə</em> sorğu göndərib statistik ortalama götürür. 3 ms fərqi 1000 sorğuda aydın görünür. Ona görə <code>SAXTA_HASH</code> ucuz və effektiv müdafiədir — bir sətir kod."),
        ("E-poçtu kiçik hərflərə çevirmək `İ`/`I` problemini yaradırmı?",
         "Azərbaycan dilində <code>İ.toLowerCase()</code> → <code>i̇</code> (nöqtəli i + birləşdirici nöqtə) kimi qəribə nəticə verə bilər. Amma <strong>e-poçt ünvanları üçün bu problem deyil</strong>: RFC 5321 e-poçtun <em>yerli hissəsini</em> (şəxs adı) hərf böyüklüyünə həssas sayır, domen hissəsini isə yox. Praktikada bütün sistemlər e-poçtu tamamilə kiçik hərfə çevirir. Əgər istifadəçi adı kimi qeyri-ASCII mətn üzərində işləsək, <code>toLocaleLowerCase('az')</code> işlətmək lazım gələrdi."),
        ("İstifadəçi adını (`ad_soyad`) da yoxlamaq lazım deyilmi?",
         "Lazımdır və DTO-da var: <code>@MinLength(3)</code> + <code>@MaxLength(120)</code>. Amma ⚠️ <strong>ad üçün format yoxlaması yazmayın</strong> — insan adları çox müxtəlifdir: «Əli», «Məhəmməd oğlu», «Mary-Jane», «O'Brien», «李». Regex ilə ad yoxlamaq <em>hər zaman</em> yanlış insanları rədd edir. Yalnız uzunluq yoxlayın və <code>.trim()</code> edin."),
        ("`STANDART_ROL` sabitini dəyişsəm nə olar?",
         "Yalnız <em>yeni</em> istifadəçilər təsirlənir — köhnələrin rolu bazada qalır. Bu, düzgün davranışdır: sabit <em>standart dəyərdir</em>, məcburi dəyər deyil. Əgər bütün istifadəçilərin rolunu dəyişmək lazımdırsa, ayrıca miqrasiya (<code>UPDATE</code>) yazmaq gərəkdir — və bu, <em>şüurlu</em> qərar olmalıdır."),
        ("Bazadaki 4 istifadəçinin parolunu dəyişmək lazım deyilmi? `123456` çox zəifdir.",
         "<strong>Mütləq lazımdır</strong> — və bu, real dünyada ən çox yaranan sualdır: «qaydaları sərtləşdirdik, köhnə istifadəçilər nə olsun?». Praktikada belə edilir: (1) istifadəçiyə <code>parol_dəyişmə_lazımdır</code> bayrağı qoyulur; (2) növbəti girişdə yeni parol tələb olunur; (3) müəyyən müddət verilir (məsələn 30 gün), sonra hesab kilidlənir. Bizim dərsdə bu, 3B-nin mövzusudur. Hələlik demo istifadəçilər işləyir ki, rolları sınaqdan keçirə bilək."),
        ("Mövcud e-poçt üçün niyə 409, 400 yox?",
         "<strong>400</strong> «göndərdiyin məlumat səhvdir» deməkdir. Amma bizim halda məlumat <em>düzgündür</em> — sadəcə həmin e-poçt <strong>artıq mövcuddur</strong>. <strong>409 Conflict</strong> məhz bunun üçündür: «sorğun resursun cari vəziyyəti ilə konfliktə girir». ⚠️ Fərq praktikdir: 400 alanda frontend <em>formu</em> düzəltməyə çalışır, 409 alanda isə «bu e-poçt artıq qeydiyyatdadır» mesajı göstərir."),
        ("Deaktiv hesab üçün niyə 401 deyil, 403?",
         "<strong>401</strong> = «səni tanımıram» → istifadəçi yenidən giriş <em>etməlidir</em>. <strong>403</strong> = «tanıdım, amma icazən yoxdur» → yenidən giriş <em>heç nəyi dəyişməz</em>. Deaktiv hesabda parol <strong>düzgün</strong> idi, yəni istifadəçi tanındı; maneə parol deyil, hesabın <em>vəziyyətidir</em>. Ona görə 403 düzgündür. ⚠️ Frontend bu ayrımı bilməlidir: 401 → giriş səhifəsi, 403 → «hesabınız deaktivdir»."),
        ("Mövcud olmayan ID üçün niyə 500 yerinə 404?",
         "Prisma `update`/`delete` mövcud olmayan ID üçün <code>P2025</code> xətası atır və bu, <em>xam</em> halda <strong>500</strong> kimi çıxır. ⚠️ 500 «server xarabdır» siqnalıdır: monitorinq alarm verir, inzibatçı loqlara baxır, halbuki problem sadəcə səhv ID-dir. Ona görə yazmadan <em>əvvəl</em> mövcudluğu yoxlayırıq və <strong>404</strong> qaytarırıq. Bu, <em>səs-küyü azaldır</em> — 500 siqnalı həqiqi problemlər üçün qalır."),
        ("Niyə `parol_hash` üçün ayrıca `select` yazırıq, axı `ISTIFADECI_SECIM` var?",
         "Çünki <code>daxiliTap()</code>-ə hash <strong>lazımdır</strong> — parolu yoxlamaq üçün. Ona görə orada <code>{ ...ISTIFADECI_SECIM, parol_hash: true }</code> yazırıq: əsas seçimi genişləndiririk. Alternativ: ayrıca tam seçim sabiti yaratmaq. Ammo o zaman iki sabiti sinxron saxlamaq lazım gələrdi — biri dəyişəndə digərini unutmaq riski var. Yayma (<em>spread</em>) operatoru bu riski aradan qaldırır."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>İstifadəçi servisi <strong>37 yoxlamadan</strong> keçdi.</li>
  <li><strong>Hash API-dən çıxmır:</strong> <code>select</code> sayəsində
      parol hash-i bazadan <em>heç oxunmur</em>.</li>
  <li><strong>İmtiyaz yüksəltmə qapadıldı:</strong>
      <code>{"rol":"admin"}</code> göndərmək cəhdi <code>400</code> aldı.</li>
  <li><strong>Zəif parollar rədd edilir:</strong> 10 nümunənin 9-u,
      o cümlədən bazadaki <code>123456</code> parolu.</li>
  <li><strong>Giriş zəif parolu qəbul edir:</strong> 4 real istifadəçi
      <code>123456</code> ilə giriş etdi və rolları düzgün gəldi.</li>
  <li><strong>E-poçt mövcudluğu sızmır:</strong> «səhv parol» və
      «istifadəçi yoxdur» eyni cavabı və eyni müddəti verir.</li>
  <li><strong>Deaktiv hesab giriş edə bilmir</strong> — aydın mesajla
      və düzgün status kodu ilə (403).</li>
  <li><strong>Rol dəyişmə işləyir</strong> və yanlış rol adı rədd edilir.</li>
</ul>
<p>Növbəti addımda <strong>token</strong> yaradacağıq: istifadəçi bir
dəfə parol yazsın, sonra hər sorğuda token göndərsin.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 29 — TOKEN SERVİSİ (JWT)
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 29,
    "ad": "Token servisi — JWT ilə giriş sessiyası",
    "a": """
<p>İndiyə qədər istifadəçi hər sorğuda parol yazmalı idi. Bu, həm
yorucu, həm də <strong>təhlükəlidir</strong>: parol nə qədər çox
ötürülsə, o qədər çox yerdə qalır (loq, keş, brauzer tarixçəsi).</p>
<p>Həll: <strong>JWT (JSON Web Token)</strong>. İstifadəçi <em>bir dəfə</em>
parol yazır, server ona <em>imzalanmış</em> bilet verir. Sonra hər
sorğuda həmin bilet göstərilir.</p>

<h4>🎫 Bilet bənzətməsi</h4>
<p>Təsəvvür edin ki, instituta gəlirsiniz:</p>
<ol>
  <li><strong>Qapıda</strong> şəxsiyyət vəsiqənizi göstərirsiniz
      (→ e-poçt + parol).</li>
  <li>Keşikçi bazaya baxır, sizi tapır → <strong>qonaq kartı</strong>
      verir (→ <em>token</em>).</li>
  <li>Gün ərzində hər otağa girəndə kartı göstərirsiniz — keşikçi
      bazaya <em>yenidən zəng etmir</em>, karta baxır (→ token
      <em>yoxlanılır</em>, amma bazaya sorğu getmir).</li>
  <li>Kartın <strong>müddəti</strong> var: axşam saat 18:00-da
      bitir (→ <code>exp</code> sahəsi).</li>
</ol>
<p>Kartın üzərində <em>adınız və vəzifəniz</em> yazılıb — amma
<strong>şifrə yoxdur</strong>. Kartı itirsəniz, tapan şəxs oxuya bilər.
Buna görə kart <em>sirr deyil</em>.</p>

<h4>🔍 JWT-nin quruluşu — üç hissə, iki nöqtə</h4>
<pre style="background:#0f172a;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem;font-size:.85rem;overflow-x:auto">
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImVtYWlsIjoiYWRtaW5AYXJ0aS5lZHUuYXoiLCJyb2wiOiJhZG1pbiIsImlhdCI6MTc2NzIyMDAwMCwiZXhwIjoxNzY3MjIzNjAwfQ.dGhpcy1pcy1hLWZha2Utc2lnbmF0dXJl
└──────────── HEADER ───────────┘.└──────────────────── PAYLOAD ─────────────────────┘.└──── İMZA ────┘
</pre>
<table style="width:100%;border-collapse:collapse;font-size:.85rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Hissə</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Açılmış halı</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Nə üçündür</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>HEADER</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>{"alg":"HS256","typ":"JWT"}</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Hansı alqoritm</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>PAYLOAD</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>{"sub":2,"email":"…","rol":"admin","iat":…,"exp":…}</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Kim olduğu</td>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>İMZA</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><code>HMAC-SHA256(header + "." + payload, SİRR)</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Dəyişdirilmədiyinin zəmanəti</td>
  </tr>
</table>

<h4>⚠️⚠️ ƏN BÖYÜK YANLIŞ ANLAMA: «JWT şifrələnir»</h4>
<p><strong>XEYR!</strong> JWT <em>şifrələnmir</em>, yalnız
<em>imzalanır</em>. Bu, hər şeyi dəyişir:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
BASE64URL, ŞİFRƏLƏMƏ DEYİL!

Komanda sətrində yoxlayaq:
$ echo 'eyJzdWIiOjIsInJvbCI6ImFkbWluIn0' | base64 -d
{"sub":2,"rol":"admin"}      ← ⚠️ 1 saniyədə OXUNDU!
</pre>
<p>Ona görə <strong>JWT-yə heç vaxt bunlar yazılmır</strong>:</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">❌ YAZILMIR</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Niyə</th>
  </tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">parol, <code>parol_hash</code></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Biletin üzərində şifrə yazmaq kimi</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0">FIN kod, pasport nömrəsi</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Şəxsi məlumat — qanunla qorunur</td></tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">maaş, bank kartı</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Maliyyə məlumatı</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0">sessiya məlumatı, sirr açarlar</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Token özü onsuz da açıqdır</td></tr>
</table>
<p>✅ <strong>Yalnız identifikasiya:</strong> <code>sub</code> (kim),
<code>email</code>, <code>ad_soyad</code>, <code>rol</code> — yəni
«kim gəldi və hansı hüququ var».</p>

<h4>⚠️ İmza nə üçündür?</h4>
<p>İmza <strong>məzmunu gizlətmir</strong> — <em>dəyişdirilmədiyini
sübut edir</em>. Ssenari:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
İstifadəçi baxici-dir, əlində token var:
  {"sub":9,"rol":"baxici","exp":1767223600}

O, payload-u dəyişib yazır:  {"sub":9,"rol":"admin","exp":1767223600}
                              └────── əl ilə düzəldildi ──────┘

Serverə göndərir. Server İMZANI yoxlayır:
  gözlənilən = HMAC-SHA256(header + "." + yeni_payload, SİRR)
  gələn      = köhnə imza
  → UYĞUN GƏLMİR → 401 Unauthorized  ✅

Hücumçunun yeni imza hesablamaq üçün SİRRİ bilməsi lazımdır.
Sirr 32+ simvoldur və yalnız serverdədir.
</pre>
<p>⚠️ Amma diqqət: token <strong>ələ keçirilsə</strong>, hücumçunun
imza hesablaması lazım deyil — mövcud tokeni <em>olduğu kimi</em>
işlədir. Buna <strong>token oğurluğu</strong> deyilir və tokenin
müddətini qısa saxlamaqla azaldılır.</p>

<h4>⚠️ Sirr (JWT_SECRET) nə qədər güclü olmalıdır?</h4>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Sirr</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Sındırma vaxtı</th>
  </tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0"><code>secret</code></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">⚠️ Dərhal (lüğət siyahısında var)</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0"><code>arti2025</code></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">⚠️ Saniyələr</td></tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0"><code>openssl rand -base64 48</code></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">✅ Praktiki olaraq mümkün deyil</td></tr>
</table>
<p>Ona görə <code>sirr()</code> metodu <strong>uzunluğu yoxlayır</strong>
və qısadırsa server <em>ümumiyyətlə işə düşmür</em>. Bu,
«uğursuz təhlükəsiz» (<em>fail-safe</em>) prinsipidir: səhv
konfiqurasiya ilə <strong>işləməkdənsə, heç işləməmək yaxşıdır</strong>.</p>

<h4>⚠️ Token müddəti — nə qədər olmalıdır?</h4>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Müddət</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Üstünlük</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Çatışmazlıq</th>
  </tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">5 dəqiqə</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Oğurlansa ziyan azdır</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">⚠️ İstifadəçi tez-tez yenidən giriş edir</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0"><strong>1 saat</strong> ← bizim</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Balans yaxşıdır</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Orta risk</td></tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">30 gün</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Rahat</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">⚠️ Oğurlansa 30 gün giriş açıqdır</td></tr>
</table>
<p>⚠️ <strong>JWT-ni geri çağırmaq (revoke) mümkün deyil.</strong>
Token imzalanandan sonra server onu «ləğv etmək» üçün heç nə edə
bilmir — çünki yoxlama zamanı bazaya baxmır. Çıxış yolları:</p>
<ul>
  <li>Qısa müddət + <em>refresh token</em> (3B-nin mövzusu),</li>
  <li>Qara siyahı (blacklist) — JWT-nin üstünlüyünü azaldır,</li>
  <li>Sirri dəyişmək — <em>bütün</em> istifadəçiləri çıxarır, çox kobud.</li>
</ul>
""",
    "anlayis": [
        ("JWT",
         "JSON Web Token — imzalanmış, özü-özünü təsvir edən bilet. "
         "Server bazaya baxmadan kimliyi müəyyən edə bilir."),
        ("Payload (yük)",
         "Tokenin içindəki məlumat: kim, hansı rol, nə vaxt bitir."),
        ("İmza",
         "HMAC-SHA256 ilə hesablanan nəzarət kodu. Məzmunu "
         "<em>gizlətmir</em>, dəyişdirilmədiyini sübut edir."),
        ("Base64URL",
         "Kodlama üsulu. Şifrələmə DEYİL — hər kəs aça bilər."),
        ("HS256",
         "HMAC + SHA-256. Simmetrik alqoritm: imzalama və yoxlama "
         "eyni sirrlə aparılır."),
        ("`sub`",
         "«Subject» — JWT standartında istifadəçinin identifikatoru."),
        ("`iat` / `exp`",
         "«Issued at» / «expiration» — yaradılma və bitmə vaxtı "
         "(Unix vaxtı, saniyə)."),
        ("Bearer",
         "Tokenin ötürülmə sxemi: <code>Authorization: Bearer &lt;token&gt;</code>. "
         "«Bearer» = «daşıyıcı»; tokeni daşıyan hər kəs hüquqa malikdir."),
        ("Fail-safe",
         "«Uğursuz təhlükəsiz» — səhv konfiqurasiya varsa, sistem "
         "işləməkdənsə dayanır."),
        ("Token müddəti",
         "Tokenin etibarlı olduğu vaxt. Qısadırsa təhlükəsiz, amma "
         "istifadəçi tez-tez giriş edir."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) <code>sirr()</code> — fail-safe konfiqurasiya</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
sirr(): string {
  const s = this.config.get&lt;string&gt;('JWT_SECRET');
  if (!s || s.length &lt; MIN_SIRR_UZUNLUGU) {
    throw new Error(
      `JWT_SECRET təyin olunmayıb və ya çox qısadır ` +
        `(minimum ${MIN_SIRR_UZUNLUGU} simvol). ` +
        'Yaratmaq üçün: openssl rand -base64 48',
    );
  }
  return s;
}</pre>
<ul>
  <li>⚠️ <strong>Default dəyər YOXDUR.</strong>
      <code>this.config.get('JWT_SECRET') ?? 'gizli'</code> yazsaydıq,
      istehsalatda sirr unudulanda sistem <em>hamının bildiyi</em>
      sirrlə işləyərdi — və hər kəs admin tokeni yarada bilərdi.</li>
  <li>Xəta mesajı <strong>düzəltmə yolunu</strong> göstərir
      (<code>openssl rand -base64 48</code>) — yaxşı xəta mesajının
      xüsusiyyəti budur.</li>
  <li>⚠️ Bu metod <em>hər</em> <code>yarat</code>/<code>yoxla</code>
      çağırışında işləyir. Bu, kiçik gecikmədir (konfiqurasiya
      yaddaşdadır), amma qoruma dəyərlidir: sirr <em>işləmə vaxtında</em>
      dəyişsə belə, yoxlama davam edir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2) <code>muddetiSaniyeye()</code> — köməkçi funksiya</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export function muddetiSaniyeye(muddet: string): number {
  const uygun = /^(\\d+)\\s*([smhd])?$/.exec(muddet.trim().toLowerCase());
  if (!uygun) {
    throw new Error(
      `JWT_MUDDET formatı səhvdir: "${muddet}". ` +
        'Gözlənilən format: 3600, 30m, 1h, 7d',
    );
  }
  const say = Number(uygun[1]);
  const emsallar: Record&lt;string, number&gt; = { s: 1, m: 60, h: 3600, d: 86400 };
  return say * (emsallar[uygun[2] ?? 's'] ?? 1);
}</pre>
<ul>
  <li>⚠️ <strong>Niyə lazımdır?</strong> <code>@nestjs/jwt</code>-nin
      <code>expiresIn</code> parametri <em>rəqəm (saniyə)</em> və ya
      <code>ms</code> paketinin xüsusi şablon tipini qəbul edir. Adi
      <code>string</code> ötürsək:</li>
</ul>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:.8rem 1rem;font-size:.85rem">
error TS2769: No overload matches this call.
  Type 'string' is not assignable to type
  'number | StringValue | undefined'.
</pre>
<ul>
  <li>Özümüz çevirməklə həm tip problemi həll olunur, həm də formatı
      <strong>yoxlaya</strong> bilirik: <code>JWT_MUDDET=abc</code>
      yazsaq, server dərhal aydın xəta verir.</li>
  <li>Regex: <code>^(\\d+)\\s*([smhd])?$</code> — rəqəm, istəyə bağlı
      hərf. <code>?? 's'</code> — hərf yoxdursa saniyə say.</li>
  <li>⚠️ <code>Record&lt;string, number&gt;</code> — TypeScript-də
      «açarı söz, dəyəri ədəd olan obyekt» tipi. Sadə
      <code>Object</code> yazsaq, <code>emsallar[x]</code> tipi
      <code>any</code> olardı.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3) <code>yarat()</code> — token yaradılması</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const yuk: TokenYuku = {
  sub: istifadeci.id,
  email: istifadeci.email,
  ad_soyad: istifadeci.ad_soyad,
  rol: istifadeci.rol,
};

const saniye = muddetiSaniyeye(this.muddet());
const access_token = await this.jwt.signAsync(yuk, {
  secret: this.sirr(),
  expiresIn: saniye,
});</pre>
<ul>
  <li>⚠️ <code>istifadeci</code> — <code>IstifadeciCavabi</code> tipidir,
      yəni <strong>hash-siz</strong> obyekt. Ona görə tokenə hash düşə
      bilməz — <em>tip səviyyəsində</em> qorunur.</li>
  <li><code>signAsync</code> — asinxron variant. Sinxron <code>sign</code>
      da var, amma asinxron olan event loop-u bloklamır.</li>
  <li>⚠️ <strong>Payload-u özümüz <code>exp</code> ilə
      doldurmuruq.</strong> <code>@nestjs/jwt</code> <code>expiresIn</code>-dən
      <code>exp</code> və <code>iat</code>-ı <em>avtomatik</em> hesablayır.
      Özümüz yazsaq, kitabxana ilə toqquşardı.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">4) Cavabın qurulması</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const acilmis = this.ac(access_token);
const exp = Number(acilmis.payload.exp ?? 0);
const iat = Number(acilmis.payload.iat ?? 0);

return {
  ugur: true,
  access_token,
  token_novu: 'Bearer',
  muddet_saniye: exp - iat,
  bitme_vaxti: new Date(exp * 1000).toISOString(),
  istifadeci,
};</pre>
<ul>
  <li>⚠️ <code>exp * 1000</code> — Unix vaxtı <em>saniyədir</em>,
      JavaScript <code>Date</code> isə <em>millisaniyə</em> gözləyir.</li>
  <li><code>token_novu: 'Bearer'</code> — frontend bilir ki,
      <code>Authorization: Bearer &lt;token&gt;</code> yazmalıdır.</li>
  <li><code>muddet_saniye</code> — frontend tokenin nə vaxt bitəcəyini
      bilir və <em>əvvəlcədən</em> yeniləyə bilər.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">5) <code>yoxla()</code> — DÖRD yoxlama</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
async yoxla(token: string): Promise&lt;YoxlanilmisYuku | null&gt; {
  if (!token || typeof token !== 'string') return null;      // 1
  if (token.split('.').length !== 3) return null;            // 2

  try {
    const y = await this.jwt.verifyAsync&lt;YoxlanilmisYuku&gt;(token, {
      secret: this.sirr(),
    });
    if (typeof y?.sub !== 'number' || typeof y?.rol !== 'string') {
      this.log.warn('Token yükü gözlənilən formada deyil');   // 3
      return null;
    }
    return y;
  } catch {
    return null;                                              // 4
  }
}</pre>
<ul>
  <li><strong>1.</strong> Boş / səhv tip → dərhal <code>null</code>.
      <code>verifyAsync</code>-a <code>undefined</code> ötürsək,
      kitabxana <em>daxili xəta</em> verərdi — aydın olmayan 500.</li>
  <li><strong>2.</strong> Üç hissə yoxlaması. «<code>abc</code>» kimi
      mətn <code>verifyAsync</code>-da xəta verir, amma erkən yoxlama
      daha <em>sürətli</em> və daha <em>aydın</em>dır.</li>
  <li><strong>3.</strong> ⚠️ Yükün forması. Token düzgün imzalanmış ola
      bilər, amma içində gözlənilməz məlumat ola bilər (köhnə versiya,
      başqa servis eyni sirri işlədibsə). <code>sub</code> ədəd
      deyilsə, <code>where: { id: y.sub }</code> «NaN» göndərərdi.</li>
  <li><strong>4.</strong> ⚠️ <code>catch {}</code> — <strong>boş
      catch</strong>. Mesajı <em>qəsdən</em> uduruq: «imza səhvdir» vs
      «müddət bitib» fərqini sızdırsaq, hücumçu tokenin
      <em>düzgün imzalanıb-bitmədiyini</em> öyrənərdi.</li>
  <li>⚠️ <strong>Xəta atmır, <code>null</code> qaytarır.</strong> Səbəb:
      guard hər uğursuzluq üçün eyni 401-i verməlidir. Xəta atsaydıq,
      NestJS <em>avtomatik</em> cavab qurardı və biz mesajı idarə
      edə bilməzdik.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">6) <code>ac()</code> — YOXLAMADAN açmaq</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
ac(token: string): AcilmisToken {
  const hisseler = token.split('.');
  const coz = (s: string): Record&lt;string, unknown&gt; =&gt; {
    try {
      return JSON.parse(
        Buffer.from(s, 'base64url').toString('utf-8'),
      ) as Record&lt;string, unknown&gt;;
    } catch {
      return {};
    }
  };
  ...
}</pre>
<ul>
  <li>⚠️⚠️ <strong>BU METOD TOKENİ YOXLAMIR.</strong> Onu
      <em>heç vaxt</em> qərar vermək üçün işlətmək olmaz!</li>
  <li><code>base64url</code> — Base64-ün URL üçün təhlükəsiz variantı
      (<code>+</code> → <code>-</code>, <code>/</code> → <code>_</code>).
      ⚠️ Adi <code>'base64'</code> yazsaq, bəzi tokenlər xəta verərdi.</li>
  <li>İstifadə yeri: yalnız öyrətmə, debug, loq və «token nə vaxt
      bitir» göstərmək üçün.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">7) Modulda qeydiyyat — <code>JwtModule.registerAsync</code></h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
JwtModule.registerAsync({
  inject: [ConfigService],
  useFactory: (config: ConfigService) =&gt; {
    const sirr = config.get&lt;string&gt;('JWT_SECRET');
    if (!sirr || sirr.length &lt; MIN_SIRR_UZUNLUGU) {
      throw new Error('JWT_SECRET ... çox qısadır');
    }
    return { secret: sirr };      // ← SERVER AÇILANDA yoxlanılır!
  },
}),</pre>
<ul>
  <li>⚠️ <code>registerAsync</code> + <code>inject</code> —
      <code>ConfigService</code> hələ hazır olmadığı üçün
      <code>register</code> (statik) işləməz.</li>
  <li><strong>Server açılan anda</strong> yoxlanılır. Səhv konfiqurasiya
      ilə sistem <em>heç işə düşmür</em> — istifadəçilər 500 xətası
      görməzdən əvvəl admin dərhal bilir.</li>
  <li>⚠️ <code>TokenService.sirr()</code> də eyni yoxlamanı edir —
      bu, <em>təkrar</em> deyil. Birinci qat serverin
      <strong>açılmasını</strong>, ikinci qat isə <strong>işləməsini</strong>
      qoruyur.</li>
</ul>
""",
    "fayllar": [
        "src/auth/dto/token.dto.ts",
        "src/auth/token.service.ts",
        "src/auth/auth.module.ts",
        "skriptler/token_yoxla.ts",
    ],
    "goster": [],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then echo "  ✓ tip xətası yoxdur"; else echo "  ✗ tip xətası var"; fi

echo ""
echo "════ 2) JWT_SECRET vəziyyəti ════"
SR=$(grep '^JWT_SECRET=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
printff() { printf '%s' "$1"; }
if [ -z "$SR" ]; then
  echo "      ⚠️ JWT_SECRET yoxdur — yaradılır"
  SR=$(openssl rand -base64 48)
  printf '\nJWT_SECRET="%s"\nJWT_MUDDET="1h"\n' "$SR" >> .env
else
  echo "      ✓ JWT_SECRET mövcuddur (uzunluq: ${#SR}) — dəyər GÖSTƏRİLMİR"
fi
printf '      uzunluq kifayətdir : %s (min 32)\n' "$([ "${#SR}" -ge 32 ] && echo 'BƏLİ' || echo 'XEYR')"
MU=$(grep '^JWT_MUDDET=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
printf '      JWT_MUDDET         : %s\n' "${MU:-1h}"

echo ""
echo "════ 3) Fayllar ════"
for f in src/auth/dto/token.dto.ts src/auth/token.service.ts src/auth/auth.module.ts; do
  printf '      %-38s %4s sətir\n' "$f" "$(wc -l < "$f" | tr -d ' ')"
done

echo ""
echo "════ 4) Tokenin üç hissəsi (canlı) ════"
npx tsx -e '
import { TokenService, muddetiSaniyeye } from "./src/auth/token.service.ts";
const t = new TokenService(null as any, { get: (k: string) =>
  k === "JWT_SECRET" ? "x".repeat(48) : "1h" } as any);
console.log("      muddetiSaniyeye(3600) =", muddetiSaniyeye("3600"));
console.log("      muddetiSaniyeye(30m)  =", muddetiSaniyeye("30m"));
console.log("      muddetiSaniyeye(1h)   =", muddetiSaniyeye("1h"));
console.log("      muddetiSaniyeye(7d)   =", muddetiSaniyeye("7d"));
try { muddetiSaniyeye("abc"); } catch (e) { console.log("      abc → xəta:", (e as Error).message.slice(0, 60)); }
' 2>&1 | grep -v '^$' | sed 's/^/  /'

echo ""
echo "════ 5) Bazadaki istifadəçi ilə REAL token ════"
npx tsx skriptler/token_yoxla.ts
""",
    "olmaz": """Sirr default dəyərlə gəlsə:

export const JWT_SECRET = process.env.JWT_SECRET ?? 'gizli';

  ⚠️ İstehsalatda JWT_SECRET unudulub. Sistem 'gizli' ilə işləyir.
  ⚠️ Bu sirr GitHub-daki koddadır — HƏR KƏS bilir.

$ # Hücumçu özü üçün admin tokeni yaradır:
$ python3 -c "
import hmac,hashlib,base64,json
def b64(d): return base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b'=').decode()
h = b64({'alg':'HS256','typ':'JWT'})
p = b64({'sub':2,'email':'admin@arti.edu.az','rol':'admin','exp':9999999999})
s = base64.urlsafe_b64encode(hmac.new(b'gizli', f'{h}.{p}'.encode(), hashlib.sha256).digest()).rstrip(b'=').decode()
print(f'{h}.{p}.{s}')
"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImVtYWlsIjoiYWRtaW5AYXJ0aS5lZHUuYXoiLCJyb2wiOiJhZG1pbiIsImV4cCI6OTk5OTk5OTk5OX0.xxxxx

$ curl -H "Authorization: Bearer eyJ...xxxxx" .../auth/me
{"id":2,"email":"admin@arti.edu.az","rol":"admin"}   ← ⚠️⚠️ ADMİN OLDU!

────────────────────────────────────────────────────────────
Öz alqoritmini seçməyə icazə verilsə (alg confusion):

$ # Hücumçu header-i dəyişir: {"alg":"none"}
  ⚠️ 'none' = «imza yoxdur». Köhnə kitabxanalar qəbul edirdi!

$ # və ya HS256 → RS256 çevrilir, açıq açar imza kimi işlədilir

  → @nestjs/jwt bu hücumlara qarşı qorunur: alqoritm
    SİRRƏ görə yoxlanılır, tokenin header-inə görə DEYİL.
  → Amma özünüz yazsanız, MÜTLƏQ alqoritmi sabit seçin:
    jwt.verify(token, secret, { algorithms: ['HS256'] })

────────────────────────────────────────────────────────────
`yoxla()` xəta atsa:

catch (e) {
  throw new UnauthorizedException(
    e.message.includes('expired')
      ? 'Token müddəti bitib'          // ⚠️
      : 'İmza səhvdir',                 // ⚠️
  );
}

  ⚠️ Hücumçu iki fərqli mesajı görür və öyrənir:
     • «müddəti bitib» → deməli İMZA düzgün idi
       → token real və sirr düzgün seçilib, sadəcə vaxtı keçib
       → yeni token üçün parol oğurlamağa dəyər
     • «imza səhvdir» → saxta token
  → Belə məlumat verilməsi «information disclosure»-dur.
  → Bizim kod hər iki halda EYNİ 401 verir.

────────────────────────────────────────────────────────────
Tokenə parol hash-i yazsaq:

const yuk = {
  sub: u.id, email: u.email, rol: u.rol,
  parol_hash: u.parol_hash,      // ⚠️⚠️ FƏLAKƏT
};

$ echo 'eyJzdWIiOjIsInBhcm9sX2hhc2giOiIkMmIkMTAk...' | base64 -d
{"sub":2,"parol_hash":"$2b$10$oIesQsaJ4ahBc0vjhaRpN.xkamY..."}

  ⚠️ Tokeni görən HƏR KƏS hash-i oxuyur. Base64 şifrələmə deyil.
  ⚠️ Token loqlara, brauzer yaddaşına, proksi serverlərə düşür.
  ⚠️ Offline sındırma başlayır — server bunu GÖRMÜR.""",
    "c_izah": """
<p><strong>Birinci nəticə: <code>muddetiSaniyeye()</code> düzgün
işləyir.</strong> <code>3600</code> → 3600, <code>30m</code> → 1800,
<code>1h</code> → 3600, <code>7d</code> → 604800, <code>abc</code> isə
aydın xəta verir. ⚠️ Sonuncu vacibdir: səhv konfiqurasiya
<em>sükutla</em> qəbul olunsaydı, token 1 saniyəlik olardı və
istifadəçi «neden hər dəfə çıxıram?» deyə çaşardı.</p>

<p><strong>İkincisi: <code>JWT_SECRET</code> uzunluğu yoxlanılır.</strong>
Skript sirri <em>heç vaxt</em> çap etmir — yalnız uzunluğunu
(<code>${#SR}</code>). Bu, ekran paylaşımı və loq yazarkən vacibdir:
sirr loqa düşsə, <em>bütün</em> token sistemi sıradan çıxar.</p>

<p><strong>Üçüncüsü: token 3 hissədən ibarətdir.</strong> Probel
<code>token.split('.')</code> uzunluğunu yoxlayır və hər hissəni
<code>base64url</code> ilə açır. Payload-da <code>sub</code>,
<code>email</code>, <code>rol</code>, <code>iat</code>,
<code>exp</code> görünür — və <strong><code>parol_hash</code>
YOXDUR</strong>. Bu, ən vacib yoxlamadır.</p>

<p><strong>Dördüncüsü: saxtalaşdırma mümkün deyil.</strong> Probel
tokenin payload-unu dəyişib yeni imza <em>uydurur</em> və
<code>yoxla()</code> <code>null</code> qaytarır. Yəni hücumçunun
«rol: baxici» → «rol: admin» cəhdi <em>işləmir</em>.</p>

<p><strong>Beşincisi: müddəti bitmiş token rədd edilir.</strong>
Probel keçmiş <code>exp</code> ilə token yaradır və
<code>yoxla()</code> onu rədd edir. Bu olmasaydı, <em>birdəfəlik</em>
oğurlanmış token <strong>əbədi</strong> işləyərdi.</p>

<p><strong>Altıncısı: 4 real istifadəçinin hamısı üçün token
yaradıldı</strong> və hər birinin <code>rol</code> sahəsi düzgün
gəldi. Bu, RBAC-ın təməlidir — növbəti addımda guard-lar bu rola
əsaslanacaq.</p>
""",
    "sual": [
        ("JWT ilə sessiya (session) arasındaki fərq nədir?",
         "<strong>Sessiya:</strong> server yaddaşında (və ya bazada) <code>sessiya_id → istifadəçi</code> cədvəli saxlanılır. Brauzer yalnız <code>sessiya_id</code> göndərir. Üstünlük: <em>dərhal ləğv etmək</em> mümkündür. Çatışmazlıq: hər sorğuda server <em>paylaşılan yaddaşa</em> baxmalıdır — bir neçə server olsa, hamısı eyni yaddaşı görməlidir (Redis lazım).<br><br><strong>JWT:</strong> heç bir yaddaş lazım deyil — token <em>özü</em> məlumatı daşıyır. Üstünlük: miqyaslanır (10 server də olsa fərqi yoxdur). Çatışmazlıq: <em>ləğv etmək mümkün deyil</em>. Buna görə böyük sistemlər <strong>ikisini birlikdə</strong> işlədir: qısa JWT + uzun refresh token (3B)."),
        ("Bəs niyə sadəcə bazaya baxmırıq? Token lazım deyil də.",
         "Baxmaq <em>olar</em> — və bu, sessiya yanaşmasıdır. Amma JWT-nin iki real üstünlüyü var: (1) <strong>sürət</strong> — bazaya sorğu getmir, ona görə 1000 sorğu/saniyə asan qarşılanır; (2) <strong>miqyaslanma</strong> — servislər bir-birindən asılı olmur. ARTİ kimi sistemdə bu, o qədər də kritik deyil (istifadəçi sayı azdır) — amma <em>öyrənmə</em> baxımından JWT müasir standartdır və 3B-də refresh token ilə tam dövrə quracağıq."),
        ("`exp` və `iat` sahələrini biz yazmırıq, kim yazır?",
         "<code>@nestjs/jwt</code> (altında <code>jsonwebtoken</code>) <code>expiresIn</code> parametrindən istifadə edib <code>exp</code>-i, cari vaxtdan isə <code>iat</code>-ı <em>avtomatik</em> hesablayır. ⚠️ Bunu özümüz etsək, iki yer arasında <em>vaxt fərqi</em> yaranardı və token gözlənilməz vaxtda bitərdi. Kitabxanaya buraxmaq düzgün yoldur."),
        ("`base64url` ilə `base64` nə ilə fərqlənir?",
         "Adi Base64 <code>+</code> və <code>/</code> simvollarını işlədir, həm də <code>=</code> ilə doldurur. ⚠️ Bunlar <strong>URL-də problem yaradır</strong>: <code>+</code> boşluğa çevrilir, <code>/</code> isə yol ayırıcısıdır. <code>base64url</code> isə <code>+</code>→<code>-</code>, <code>/</code>→<code>_</code> və <code>=</code> işlətmirlər. JWT standartı <code>base64url</code> tələb edir. Node-da: <code>Buffer.from(s, 'base64url')</code>."),
        ("Bəs niyə sirri kodda saxlaya bilmirik? Kiçik layihədir də.",
         "Saxlaya <em>bilərsiniz</em> — amma iki risk var: (1) kod Git-ə düşür və <strong>bütün komanda</strong> (və repo açıqdırsa, bütün dünya) sirri bilir; (2) sirri dəyişmək üçün <em>yenidən deploy</em> lazımdır. <code>.env</code> faylı isə <code>.gitignore</code>-dadır. ⚠️ Diqqət: <code>.env.example</code> Git-ə <em>düşür</em> — ona görə orada <strong>yalnız nümunə</strong> olmalıdır, real sirr yox."),
        ("`signAsync` əvəzinə `sign` işlətsəm nə olar?",
         "İşləyər. Fərq: <code>sign</code> <em>sinxrondur</em> — hesablama bitənə qədər Node-un event loop-u <strong>bloklanır</strong>. HMAC-SHA256 çox sürətlidir (mikrosaniyələr), ona görə praktikada fərq yoxdur. Amma <code>bcrypt</code> kimi <em>ağır</em> əməliyyatlar üçün asinxron variant mütləqdir — yoxsa bir istifadəçinin girişi <em>bütün</em> serveri 49 ms dondurar. Ona görə biz hər yerdə <code>...Async</code> variantları işlədirik: vərdiş düzgün olsun."),
        ("Tokeni `localStorage`-da saxlamaq olarmı?",
         "⚠️ <strong>Riskli.</strong> <code>localStorage</code> JavaScript-dən oxunur — saytda XSS (zərərli skript) varsa, hücumçu tokeni <em>dərhal</em> oğurlayır. Daha yaxşı yol: <code>httpOnly</code> cookie — JS onu <em>oxuya bilmir</em>. Bizim API-də hər iki üsul dəstəklənəcək (3B-də <code>httpOnly</code> cookie əlavə edəcəyik), amma <em>hər iki</em> halda əsas qoruma — XSS-in özünün qarşısını almaqdır."),
        ("`JWT_MUDDET=1h` — `h` hərfi hardan gəlir?",
         "<code>ms</code> paketinin qısaltmalarıdır: <code>s</code>=saniyə, <code>m</code>=dəqiqə, <code>h</code>=saat, <code>d</code>=gün, <code>w</code>=həftə, <code>y</code>=il. Bizim <code>muddetiSaniyeye()</code> funksiyası bunlardan yalnız <code>s/m/h/d</code>-ni dəstəkləyir. ⚠️ <code>m</code>-i <em>ay</em> kimi oxumaq olmaz — <code>ms</code> paketində <code>m</code> <strong>dəqiqədir</strong>. Bu, çox yayılmış səhvdir."),
        ("`qalanMuddet()` metodu nə üçündür?",
         "Frontend-ə «tokenin nə qədər ömrü qalıb» demək üçün. Praktikada belə işlədilir: token bitməzdən əvvəl (məsələn 5 dəqiqə qalmış) frontend <em>avtomatik</em> yeniləmə sorğusu göndərir. Yoxsa istifadəçi gözlənilmədən «401» alır və işi yarımçıq qalır. ⚠️ Amma bu metod <code>ac()</code>-a əsaslanır, yəni <strong>yoxlama aparmır</strong> — qərar üçün yaramaz."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>Token servisi <strong>35 yoxlamadan</strong> keçdi.</li>
  <li><code>muddetiSaniyeye()</code> dörd formatı düzgün çevirdi,
      səhv formatı isə <em>aydın xəta</em> ilə rədd etdi.</li>
  <li>Token <strong>üç hissədən</strong> ibarətdir və payload-da
      yalnız <code>sub</code>, <code>email</code>, <code>ad_soyad</code>,
      <code>rol</code>, <code>iat</code>, <code>exp</code> var —
      <strong>heç bir həssas məlumat yoxdur</strong>.</li>
  <li><strong>Saxtalaşdırma işləmir:</strong> payload dəyişdirilib
      yeni imza uydurulsa, <code>yoxla()</code> <code>null</code>
      qaytarır.</li>
  <li><strong>Müddəti bitmiş token rədd edilir</strong> — «əbədi
      token» təhlükəsi yoxdur.</li>
  <li>4 real istifadəçinin hamısı üçün token yaradıldı və
      <code>rol</code> sahəsi düzgün gəldi.</li>
  <li><code>JWT_SECRET</code> minimium 32 simvol olmalıdır və
      <strong>heç vaxt loqa/ekrana çıxmır</strong>.</li>
</ul>
<p>İndi <strong>qoruyucuları</strong> (guard) yazırıq: tokeni
sorğudan çıxarıb yoxlayan və rola görə icazə verən qat.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 30 — QORUYUCULAR (GUARD) VƏ ROLLAR
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 30,
    "ad": "Qoruyucular — AuthGuard, RollerGuard və xüsusi dekoratorlar",
    "a": """
<p>Tokenimiz var. İndi onu <strong>istifadə edən</strong> qatı yazırıq:
sorğudan tokeni çıxaran, yoxlayan və rola görə icazə verən
<strong>qoruyucular</strong> (guard).</p>

<h4>🚪 Qoruyucu nədir?</h4>
<p>Təsəvvür edin ki, institutun binasındasınız. <strong>Qoruyucu</strong>
(guard) — qapıdaki nəzarətçidir: otağa <em>girməzdən əvvəl</em>
biletinizi yoxlayır. Bilet yoxsa — buraxmır.</p>
<p>NestJS-də sorğu controller metoduna çatmazdan əvvəl
<strong>dörd mərhələ</strong> var:</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">#</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Mərhələ</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Sual</th>
  </tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">1</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Middleware</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">«Sorğu hansı ünvana gəlir?»</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0"><strong>2</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Guard</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>«KİM GƏLİR və İCAZƏSİ VARMI?»</strong></td></tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">3</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Interceptor</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">«Sorğudan əvvəl/sonra nə edim?»</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0">4</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Pipe</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">«Məlumat düzgündürmü?»</td></tr>
</table>
<p>⚠️ <strong>Guard-ın Pipe-dan ƏVVƏL işləməsi çox vacibdir.</strong>
Əks sırada olsaydı: icazəsiz şəxs məlumat göndərir, sistem əvvəlcə
onu <em>yoxlayır</em> və «bu e-poçt artıq mövcuddur» kimi cavab verir.
Yəni qapı bağlanmazdan əvvəl <strong>məlumat sızır</strong>.</p>

<h4>⚠️ 401 ilə 403 fərqi — ən çox qarışdırılan mövzu</h4>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Kod</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Adı</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Mənası</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">İstifadəçi nə etməlidir?</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>401</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Unauthorized</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>«SƏN KİMSƏN, BİLMİRƏM»</strong><br>
        Token yoxdur, səhvdir, ya da müddəti bitib</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">✅ Yenidən giriş et — yeni token al</td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>403</strong></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Forbidden</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>«SƏNİ TANIDIM, AMMA İCAZƏN YOXDUR»</strong><br>
        Token düzgündür, rol kifayət etmir</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">❌ Yenidən giriş <em>heç nəyi dəyişməz</em>.
        Admin icazə verməlidir</td>
  </tr>
</table>
<p>⚠️ Bu fərq <strong>frontend üçün həlledicidir</strong>:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
if (cavab.status === 401) {
  localStorage.removeItem('token');
  window.location = '/giris';        // ← giriş səhifəsinə
}
if (cavab.status === 403) {
  gosterXeta('Bu əməliyyat üçün icazəniz yoxdur');   // ← mesaj göstər
}</pre>
<p>⚠️ İkisini qarışdırsaq, istifadəçi <strong>sonsuz döngədə</strong>
giriş edib çıxar: 403 alır → giriş səhifəsinə atılır → daxil olur →
yenə 403 → yenə giriş... Ona görə bu ayrım <em>zəruridir</em>.</p>

<h4>⚠️ «Təhlükəsiz standart» (secure by default)</h4>
<p>İki yanaşma var:</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Yanaşma</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Necə işləyir</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Risk</th>
  </tr>
  <tr>
    <td style="padding:.5rem;border:1px solid #e2e8f0">❌ <code>@Qorunan()</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Hər endpoint-i <em>əl ilə</em>
        işarələyirik</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">⚠️ Birini unutmaq kifayətdir —
        məlumat <strong>açıq qalır</strong></td>
  </tr>
  <tr style="background:#f8fafc">
    <td style="padding:.5rem;border:1px solid #e2e8f0">✅ <code>@Ictimai()</code></td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">Hər şey <em>standart olaraq</em>
        qorunur; açıq olanlar işarələnir</td>
    <td style="padding:.5rem;border:1px solid #e2e8f0">✅ Unutmaq → endpoint
        <em>işləmir</em> (təhlükəsiz uğursuzluq)</td>
  </tr>
</table>
<p>Fərq nəhəngdir: birinci halda səhv → <strong>məlumat sızması</strong>,
ikinci halda səhv → <strong>«işləmir»</strong>. Biz ikincini seçirik.</p>

<h4>⚠️ Incremental (mərhələli) keçid — niyə qlobal guard YOX</h4>
<p>NestJS-də guard-ı <code>APP_GUARD</code> ilə <strong>qlobal</strong>
etmək olar — o zaman <em>bütün</em> endpoint-lər qorunur. Bu, ən
təhlükəsiz yoldur. <strong>Amma biz bunu qəsdən ETMİRİK</strong>:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
{
  provide: APP_GUARD,
  useClass: AuthGuard,
}     ← ⚠️ Bu sətir 40 testi DƏRHAL SINDIRAR!</pre>
<p>Səbəb: 2A və 2B-də yazdığımız <strong>40 test</strong> token
göndərmir — onlar əməkdaş endpoint-lərini birbaşa çağırır. Qlobal guard
qoşulsa, hamısı <code>401</code> alar və testlər qırmızı olar.</p>
<p>Düzgün yol — <strong>tədricən keçid</strong>:</p>
<ol>
  <li><strong>3A (indi):</strong> guard yazılır, yalnız
      <code>AuthController</code>-ə qoşulur.
      <code>@UseGuards(AuthGuard, RollerGuard)</code>. Köhnə testlər
      <em>toxunulmaz</em> qalır. ✅</li>
  <li><strong>3B (növbəti):</strong> köhnə 40 testə token əlavə olunur
      (<code>Authorization</code> başlığı), sonra guard qlobal edilir.
      Hər şey yaşıl qalır.</li>
</ol>
<p>⚠️ Bu, real layihələrdə <em>həmişə</em> belə olur: böyük dəyişikliyi
bir addımda etmək <strong>heç nəyin işləmədiyi</strong> vəziyyət
yaradır və xətanın harada olduğunu tapmaq mümkün olmur. Kiçik addımlar
+ hər addımda yaşıl testlər = idarə oluna bilən keçid.</p>

<h4>⚠️ Guard-ın İKİ işi var</h4>
<p>Yeni başlayanlar tez-tez bunu qarışdırır:</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
async canActivate(ctx): Promise&lt;boolean&gt; {
  const yuk = await this.token.yoxla(token);
  if (!yuk) throw new UnauthorizedException(...);

  sorgu.istifadeci = yuk;    // ← ⚠️ BU SƏTİR ÇOX VACİBDİR!
  return true;
}</pre>
<p>Guard yalnız <em>yoxlamır</em> — nəticəni <strong>sorğu
obyektinə yazır</strong>. Bu sətir olmasa:</p>
<ul>
  <li><code>@CariIstifadeci()</code> <code>undefined</code> qaytarar,</li>
  <li><code>RollerGuard</code> rolu tapa bilməz → <em>hər</em>
      rol yoxlaması uğursuz olar.</li>
</ul>
<p>Məcazi desək: qapıdaki nəzarətçi biletə baxır, sonra qonağın
<em>sinəsinə nişan vurur</em> ki, daxildəki hər otaq bilə
kim gəldiyini.</p>

<h4>⚠️ Qoruyucuların SIRASI vacibdir</h4>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@UseGuards(AuthGuard, RollerGuard)     ← ✅ DÜZGÜN
@UseGuards(RollerGuard, AuthGuard)     ← ⚠️ Yanlış (işləyər, amma...)</pre>
<p>NestJS guard-ları <em>soldan sağa</em> işlədir. <code>RollerGuard</code>
əvvəl işləsəydi, <code>req.istifadeci</code> hələ yazılmamış olardı —
o da <code>401</code> atardı və istifadəçi <strong>403 əvəzinə
401</strong> alardı. Nəticə: istifadəçi icazəsi olmadığını deyil,
«tokenim səhvdir» düşünərdi və <em>yenidən giriş edərdi</em> — boş
yerə.</p>
""",
    "anlayis": [
        ("Qoruyucu (Guard)",
         "Controller metoduna çatmazdan əvvəl işləyən icazə yoxlaması. "
         "<code>true</code> qaytarır (keçir) və ya xəta atır (dayandırır)."),
        ("`CanActivate`",
         "NestJS interfeysi — guard sinfinin tətbiq etməli olduğu müqavilə. "
         "Tək metod: <code>canActivate()</code>."),
        ("`ExecutionContext`",
         "Sorğu haqqında hər şey: HTTP sorğusu, hansı controller, "
         "hansı metod."),
        ("`Reflector`",
         "Dekoratorlarla yazılmış metadatanı oxuyan köməkçi servis."),
        ("`SetMetadata`",
         "Funksiya və ya sinfə metadatanı əlavə edən dekorator "
         "yaradıcısı."),
        ("`getAllAndOverride`",
         "Metadatanı metodda, sonra sinifdə axtarır — metod "
         "üstün gəlir."),
        ("401 Unauthorized",
         "«Səni tanımıram» — token yoxdur/səhvdir. Yenidən giriş lazım."),
        ("403 Forbidden",
         "«Tanıdım, amma icazən yoxdur» — yenidən giriş kömək etmir."),
        ("`Bearer` sxemi",
         "RFC 6750 standartı: <code>Authorization: Bearer &lt;token&gt;</code>. "
         "«Bearer» = «daşıyıcı»."),
        ("Təhlükəsiz standart",
         "«Secure by default» — hər şey standart olaraq qorunur, "
         "açıq olanlar işarələnir."),
        ("`createParamDecorator`",
         "Xüsusi parametr dekoratoru yaratmaq: <code>@CariIstifadeci()</code>."),
        ("Fabrik funksiyası",
         "Dekoratorun əsl məntiqini saxlayan ayrı funksiya — "
         "test edilə bilən hissə."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) <code>Ictimai</code> — açıq endpoint işarəsi</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export const ICTIMAI_ACAR = 'qoruyucu:ictimai';
export const Ictimai = () =&gt; SetMetadata(ICTIMAI_ACAR, true);</pre>
<ul>
  <li>⚠️ Açar <strong>sabit</strong>-dir. Eyni mətni iki yerdə yazsaq,
      birində hərf səhvi etsək guard metadatanı <em>tapa bilməzdi</em>
      və endpoint sükutla açıq qalardı.</li>
  <li><code>SetMetadata(acar, deyer)</code> — NestJS-in daxili
      mexanizmi. Metadatanı sinfə/metoda <em>görünməz</em> şəkildə
      yazır.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2) <code>Roller</code> — rolların sadalanması</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export const ROLLER_ACAR = 'qoruyucu:roller';
export const Roller = (...roller: Rol[]) =&gt; SetMetadata(ROLLER_ACAR, roller);

export const ROL_IERARXIYASI: Record&lt;Rol, number&gt; = {
  admin: 100, muhendis: 60, maliyyeci: 50, baxici: 10,
};</pre>
<ul>
  <li><code>...roller: Rol[]</code> — <em>rest parametri</em>. İstənilən
      sayda arqument: <code>@Roller('admin')</code>,
      <code>@Roller('admin','muhendis')</code>.</li>
  <li>⚠️ <code>Rol</code> tipi sabitdən çıxarılır — <code>'superadmin'</code>
      yazsaq <strong>TypeScript dərhal xəta verir</strong>:</li>
</ul>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:.8rem 1rem;font-size:.85rem">
@Roller('superadmin')
✗ Argument of type '"superadmin"' is not assignable
  to parameter of type 'Rol'.
</pre>
<p>Bu naxış çox faydalıdır: <strong>hərf səhvi kompilyasiya vaxtında</strong>
tutulur, istehsalatda yox.</p>

<h5 style="color:#334155;margin-top:1rem">3) <code>AuthGuard.canActivate</code> — dörd addım</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const ictimai = this.reflector.getAllAndOverride&lt;boolean&gt;(ICTIMAI_ACAR, [
  ctx.getHandler(),     // ← metod
  ctx.getClass(),       // ← sinif
]);
if (ictimai) return true;                                    // 1

const sorgu = ctx.switchToHttp().getRequest&lt;IstifadeciRequest&gt;();
const token = this.tokenAyir(sorgu);                         // 2
if (!token) throw new UnauthorizedException(...);

const yuk = await this.token.yoxla(token);                   // 3
if (!yuk) throw new UnauthorizedException(...);

sorgu.istifadeci = yuk;                                      // 4
return true;</pre>
<ul>
  <li><strong>1.</strong> <code>getAllAndOverride</code> — metadatanı
      <em>ƏVVƏLCƏ metoddа</em>, sonra sinifdə axtarır. Yəni
      <code>@Ictimai()</code> metodda olsa, sinfin
      <code>@Roller('admin')</code>-i <em>üstələnir</em>.</li>
  <li>⚠️ <strong>Sıra vacibdir:</strong> <code>[getHandler(), getClass()]</code>.
      Tərsinə yazsaq, sinif metodu üstələyərdi — və
      «bu metod açıqdır» işarəsi <em>heç vaxt</em> işləməzdi.</li>
  <li><strong>2.</strong> Token başlıqdan çıxarılır,
      <strong>3.</strong> yoxlanılır,
      <strong>4.</strong> isə nəticə sorğuya yazılır — bu, sonrakı
      guard-lar və <code>@CariIstifadeci()</code> üçündür.</li>
  <li>⚠️ <strong>Hər iki xəta mesajı eyni 401-dir.</strong> «Token
      yoxdur» vs «token səhvdir» fərqini sızdırsaq, hücumçu hansı
      addımda olduğunu öyrənərdi.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">4) <code>tokenAyir()</code> — başlığın təhlili</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
private tokenAyir(sorgu: IstifadeciRequest): string | null {
  const basliq = sorgu.headers?.authorization;
  if (typeof basliq !== 'string') return null;

  const [nov, token] = basliq.split(' ');
  if (!nov || !/^Bearer$/i.test(nov)) return null;
  return token && token.length > 0 ? token : null;
}</pre>
<ul>
  <li>⚠️ <code>sorgu.headers?.authorization</code> — <em>kiçik
      hərflə</em>. HTTP başlıqları böyük/kiçik hərfə həssas deyil;
      Express hamısını kiçik hərfə çevirir.</li>
  <li><code>/^Bearer$/i</code> — <code>i</code> bayrağı «case-insensitive».
      <code>bearer</code>, <code>BEARER</code>, <code>Bearer</code> —
      hamısı qəbul olunur (RFC belə deyir).</li>
  <li>⚠️ <code>basliq.split(' ')</code> — <code>token</code> massiv
      elementidir. Tokenin özündə boşluq ola bilməz (base64url),
      ona görə parçalama təhlükəsizdir.</li>
  <li>⚠️ Niyə <code>typeof basliq !== 'string'</code>? Çünki Express
      eyni başlıq iki dəfə göndərilsə <em>massiv</em> qaytarır.
      Yoxlamasaq, <code>.split</code> xəta verərdi (500) — aydın
      olmayan xəta.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">5) <code>RollerGuard</code> — 403 məntiqi</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
const teleb = this.reflector.getAllAndOverride&lt;Rol[]&gt;(ROLLER_ACAR, [
  ctx.getHandler(), ctx.getClass(),
]);
if (!teleb || teleb.length === 0) return true;        // ← rol tələb olunmur

if (!istifadeci) throw new UnauthorizedException('Giriş tələb olunur');

if (!teleb.includes(istifadeci.rol as Rol)) {
  this.log.warn(`İcazəsiz cəhd: ${istifadeci.email} ...`);
  throw new ForbiddenException(
    `Bu əməliyyat üçün icazəniz yoxdur. ` +
    `Tələb olunan rol: ${teleb.join(' və ya ')}. ` +
    `Sizin rolunuz: ${istifadeci.rol}`,
  );
}
return true;</pre>
<ul>
  <li>⚠️ <code>if (!teleb || teleb.length === 0) return true;</code> —
      bu sətir olmasa, <code>@Roller()</code> <em>yazılmayan</em>
      endpoint-lər <code>undefined.includes(...)</code> ilə
      <strong>500 xətası</strong> verərdi.</li>
  <li>⚠️ <code>!istifadeci</code> halı: normalda baş vermir (AuthGuard
      əvvəl işləyir), amma <code>RollerGuard</code> <em>təkbaşına</em>
      da qoşula bilər. Müdafiə məqsədi ilə yoxlayırıq — bu,
      <em>qat-qat müdafiə</em> prinsipidir.</li>
  <li>⚠️ <strong>403 mesajı faydalı məlumat verir:</strong> hansı rol
      lazım olduğunu və istifadəçinin rolunu göstərir. Bu,
      <em>qəsdəndir</em>: rol adları <strong>sirr deyil</strong> —
      onlar frontend-də də görünür. Amma <em>loq</em> da yazırıq:
      kim, nə vaxt, nəyə cəhd etdi. Bu, təhlükəsizlik auditinin
      əsasıdır.</li>
  <li><code>istifadeci.rol as Rol</code> — tip çevirməsi. Yük
      <code>rol: string</code> saxlayır (token xarici mənbədən gəlir),
      amma yoxlamadan əvvəl <code>Rol</code> tipinə çevirmək lazımdır.
      Bu, <em>təhlükəsizdir</em>, çünki yalnız <code>includes</code>
      yoxlamasında işlənir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">6) <code>cariIstifadeciFabriki</code> — test edilə bilən məntiq</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
export function cariIstifadeciFabriki(
  data: keyof YoxlanilmisYuku | undefined,
  ctx: ExecutionContext,
): unknown {
  const sorgu = ctx.switchToHttp().getRequest&lt;{ istifadeci?: YoxlanilmisYuku }&gt;();
  const istifadeci = sorgu.istifadeci;
  if (!istifadeci) return undefined;
  return data ? istifadeci[data] : istifadeci;
}

export const CariIstifadeci = createParamDecorator(cariIstifadeciFabriki);</pre>
<ul>
  <li>⚠️ <strong>Niyə ayrıca funksiya?</strong>
      <code>createParamDecorator</code> bizə yalnız
      <code>(data?) =&gt; ParameterDecorator</code> qaytarır — onu
      çağıranda Nest üçün <em>metadata</em> yaranır, dəyər yox.
      Əsl məntiq içəridə gizlənir və yalnız sorğu gələndə Nest-in
      özü tərəfindən çağırılır.</li>
  <li>Nəticədə həmin məntiqi <strong>test etmək mümkün olmur</strong>.
      Ona görə onu ayrı funksiya kimi yazıb ixrac edirik: həm
      dekorator ondan istifadə edir, həm də testlər birbaşa çağıra
      bilir (26 testin bir hissəsi məhz bunu yoxlayır).</li>
  <li>Bu, ümumi prinsipdir: <strong>məntiqi «çərçivə» kodundan
      ayır</strong>.</li>
  <li><code>@CariIstifadeci('rol')</code> yazsaq, yalnız
      <code>rol</code> sahəsi qaytarılır — <code>data</code>
      parametri bunun üçündür.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">7) Controller-ə qoşulma</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Controller('auth')
@UseGuards(AuthGuard, RollerGuard)      // ← SİNİF səviyyəsində
export class AuthController {

  @Post('giris')
  @Ictimai()                            // ← bu metod AÇIQDIR
  @HttpCode(200)
  giris(@Body() dto: GirisDto) { ... }
}</pre>
<ul>
  <li>⚠️ <code>@UseGuards</code> sinif səviyyəsindədir: <em>bütün</em>
      metodlar qorunur. Açıq olması lazım olanlar <code>@Ictimai()</code>
      ilə işarələnir.</li>
  <li>Bu, <strong>təhlükəsiz standart</strong> prinsipinin praktik
      tətbiqidir: unutmaq → endpoint <em>işləmir</em> (təhlükəsiz),
      açıq qalmır.</li>
</ul>
""",
    "fayllar": [
        "src/auth/qoruyucu/ictimai.dekorator.ts",
        "src/auth/qoruyucu/roller.dekorator.ts",
        "src/auth/qoruyucu/cari-istifadeci.dekorator.ts",
        "src/auth/qoruyucu/auth.guard.ts",
        "src/auth/qoruyucu/roller.guard.ts",
        "skriptler/qoruyucu_yoxla.ts",
    ],
    "goster": [],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then echo "  ✓ tip xətası yoxdur"; else echo "  ✗ tip xətası var"; fi

echo ""
echo "════ 2) Fayllar ════"
for f in src/auth/qoruyucu/ictimai.dekorator.ts \
         src/auth/qoruyucu/roller.dekorator.ts \
         src/auth/qoruyucu/cari-istifadeci.dekorator.ts \
         src/auth/qoruyucu/auth.guard.ts \
         src/auth/qoruyucu/roller.guard.ts; do
  printf '      %-46s %4s sətir\n' "$f" "$(wc -l < "$f" | tr -d ' ')"
done

echo ""
echo "════ 3) Guard sırası və qlobal guard YOXLAMASI ════"
grep -n 'UseGuards' src/auth/auth.controller.ts | sed 's/^/      /'
printf '      APP_GUARD istifadəsi : %s (0 olmalıdır — 3B-də əlavə olunacaq)\n' \
  "$(grep -rc 'APP_GUARD' src/ 2>/dev/null | awk -F: '{s+=$2} END{print s+0}')"
printf '      AuthGuard qoşulub   : %s\n' "$(grep -c 'AuthGuard' src/auth/auth.controller.ts)"
printf '      RollerGuard qoşulub : %s\n' "$(grep -c 'RollerGuard' src/auth/auth.controller.ts)"

echo ""
echo "════ 4) 401 vs 403 — hansı guard hansı xətanı atır ════"
printf '      UnauthorizedException (401): %s yer\n' "$(grep -c 'UnauthorizedException' src/auth/qoruyucu/auth.guard.ts src/auth/qoruyucu/roller.guard.ts | awk -F: '{s+=$2} END{print s}')"
printf '      ForbiddenException    (403): %s yer\n' "$(grep -c 'ForbiddenException' src/auth/qoruyucu/roller.guard.ts)"
printf '      qoruyucu qovluğu     : %s fayl\n' "$(ls src/auth/qoruyucu/*.ts | wc -l | tr -d ' ')"

echo ""
echo "════ 5) CANLI qoruyucu yoxlaması ════"
npx tsx skriptler/qoruyucu_yoxla.ts
""",
    "olmaz": """Guard sırası səhv olsa (`@UseGuards(RollerGuard, AuthGuard)`):

$ curl .../auth/admin-yoxlama          # admin tokeni İLƏ
HTTP/1.1 401 Unauthorized
{"xeta":{"mesaj":"Giriş tələb olunur"}}    ← ⚠️ 401! Halbuki token DÜZGÜNDÜR

  ⚠️ RollerGuard əvvəl işləyir, `req.istifadeci` hələ YAZILMAYIB
     (onu AuthGuard yazır). Ona görə RollerGuard «istifadəçi yoxdur»
     deyib 401 atır.
  ⚠️ Nəticə: istifadəçi «tokenim səhvdir» düşünür və YENİDƏN GİRİŞ
     EDİR — boş yerə. Əslində isə rolu kifayət etmirdi (403 olmalıydı).

────────────────────────────────────────────────────────────
`if (!teleb || teleb.length === 0) return true;` sətri olmasa:

$ curl .../auth/me -H "Authorization: Bearer <düzgün token>"
HTTP/1.1 500 Internal Server Error
{
  "statusCode": 500,
  "message": "Cannot read properties of undefined (reading 'includes')"
}                                       ← ⚠️ 500 — aydın olmayan xəta

  ⚠️ @Roller() yazılmayan HƏR endpoint 500 verir.
  ⚠️ İstifadəçi «server xarabdır» düşünür, admin loqları qazır.
  ⚠️ Düzgün davranış: rol tələb olunmursa KEÇİR (return true).

────────────────────────────────────────────────────────────
Guard nəticəni sorğuya yazmasa (`sorgu.istifadeci = yuk;` olmasa):

@Get('me')
me(@CariIstifadeci() ist: YoxlanilmisYuku) {
  return ist;      // ← undefined qaytarır
}

$ curl .../auth/me -H "Authorization: Bearer <düzgün token>"
{}                                       ← ⚠️ BOŞ CAVAB!

  ⚠️ Token düzgündür, guard keçdi, amma məlumat İTİR.
  ⚠️ RollerGuard da rolu tapa bilmir → HƏR rol yoxlaması uğursuz.
  ⚠️ Guard-ın İKİ işi var: yoxlamaq VƏ nəticəni ötürmək.

────────────────────────────────────────────────────────────
`@Ictimai()` metodu üstələməsə (getAllAndOverride sırası tərs olsa):

@Controller('auth')
@UseGuards(AuthGuard)
@Roller('admin')                  // ← SİNİF səviyyəsində
export class AuthController {

  @Post('giris')
  @Ictimai()                      // ← metod səviyyəsində AÇIQ
  giris(@Body() dto: GirisDto) { ... }
}

$ curl -X POST .../auth/giris -d '{...}'
HTTP/1.1 401 Unauthorized               ← ⚠️⚠️ GİRİŞ MÜMKÜN DEYİL!

  ⚠️ Heç kim sistemə girə bilmir — çünki giriş endpoint-i də
     token tələb edir. «Yumurtamı toyuqdan, toyuqmu yumurtadan?»
  ⚠️ `getAllAndOverride([getHandler(), getClass()])` sırası
     MÜTLƏQ metod-əvvəl olmalıdır.

────────────────────────────────────────────────────────────
Token başlığı massiv olsa (typeof yoxlaması olmasa):

$ curl .../auth/me -H "Authorization: Bearer a" -H "Authorization: Bearer b"
HTTP/1.1 500 Internal Server Error
Cannot read properties of undefined (reading 'split')   ⚠️

  ⚠️ Express eyni başlıq iki dəfə göndərilsə MASSİV qaytarır:
     basliq = ['Bearer a', 'Bearer b']
  ⚠️ `basliq.split` → TypeError → 500. Aydın olmayan xəta.
  ⚠️ `typeof basliq !== 'string'` yoxlaması bunun qarşısını alır.""",
    "c_izah": """
<p><strong>Birinci nəticə: 26 yoxlama keçdi.</strong> Onlar üç
qrupa bölünür: <em>AuthGuard</em>, <em>RollerGuard</em> və
<em>dekoratorlar</em>.</p>

<p><strong>AuthGuard (12 yoxlama):</strong> token yoxdur → 401; səhv
imza → 401; müddəti bitmiş → 401; <code>Basic</code> sxemi →
401; boş token → 401; düzgün token → keçir və
<code>sorgu.istifadeci</code> doldurulur. ⚠️ Sonuncu vacibdir:
guard <em>yalnız</em> keçirmir, həm də nəticəni ötürür.</p>

<p><strong>RollerGuard (9 yoxlama):</strong> rol tələb olunmayan
endpoint keçir; <code>admin</code> tələb olunan endpoint-də
<code>baxici</code> → <strong>403</strong>; <code>admin</code> →
keçir; <code>@Roller('admin','muhendis')</code> iki rolu da qəbul edir;
<code>maliyyeci</code> → 403. Önəmlisi: 403 mesajını yoxlayırıq —
orada istifadəçinin rolu və tələb olunan rol var.</p>

<p><strong>Dekoratorlar (5 yoxlama):</strong>
<code>cariIstifadeciFabriki</code> birbaşa çağırılır —
<code>@CariIstifadeci()</code> bütün yükü qaytarır,
<code>@CariIstifadeci('rol')</code> yalnız rolu.
⚠️ Bu, <em>ayrıca funksiya</em> yazmağımızın bəhrəsidir: əks halda
bu məntiqi test etmək <strong>mümkün olmazdı</strong>.</p>

<p><strong>İkincisi: qlobal guard QƏSDƏN yoxdur.</strong>
Skript <code>APP_GUARD</code>-ı <code>src/</code> içində axtarır və
0 tapır. Bu, təsadüf deyil — <em>planlı qərardır</em>. Köhnə 40 test
token göndərmir; qlobal guard onların hamısını sındırardı.
3B-də testlər yenilənəndən <em>sonra</em> qlobal ediləcək.</p>

<p><strong>Üçüncüsü: guard yalnız <code>AuthController</code>-ə
qoşulub.</strong> Skript bunu <code>grep</code> ilə təsdiqləyir:
<code>@UseGuards(AuthGuard, RollerGuard)</code> — <em>bir</em> yerdə,
düzgün sıra ilə. Bu yoxlama vacibdir, çünki sıra dəyişsə 401/403
məntiqi pozulur (yuxarıdaki «olmaz» bölməsinə bax).</p>

<p><strong>Dördüncüsü: 401 və 403 ayrı-ayrı siniflərdir.</strong>
<code>UnauthorizedException</code> hər iki guard-da var (keçid
yoxlamaları), <code>ForbiddenException</code> isə <strong>yalnız</strong>
<code>RollerGuard</code>-dadır. Yəni <em>«kim gəldi»</em> sualı 401,
<em>«icazəsi varmı»</em> sualı 403 verir — qarışmır.</p>
""",
    "sual": [
        ("Guard ilə Middleware fərqi nədir?",
         "<strong>Middleware</strong> marşrutlaşdırmadan <em>əvvəl</em> işləyir və <code>next()</code> çağırmaqla sorğunu ötürür — hansı controller/metodun işləyəcəyini <em>bilmir</em>. <strong>Guard</strong> isə artıq <em>bilir</em> (çünki <code>ExecutionContext</code> var) və ona görə <code>Reflector</code> ilə dekorator metadatasını oxuya bilir. Bu, qərar vermək üçün həlledicidir: middleware-də <code>@Roller('admin')</code>-i oxuya bilməzdik."),
        ("Guard əvəzinə Interceptor işlətmək olarmı?",
         "Texniki olaraq olar, amma <strong>yanlış yerdir</strong>. Guard <em>Pipe-dan əvvəl</em> işləyir; interceptor isə sonra. Fərq: interceptor işlədikdə məlumat artıq <em>yoxlanılıb</em> — yəni icazəsiz şəxs «bu e-poçt artıq var» kimi cavab alır. Bu, məlumat sızmasıdır. Qayda: <strong>icazə = guard</strong>."),
        ("`Reflector` nədir və nə üçün lazımdır?",
         "<code>Reflector</code> — dekoratorlarla yazılan <em>metadatanı</em> oxuyan NestJS servisidir. <code>SetMetadata('acar', dəyər)</code> yazanda dəyər sinfin/metodun üzərinə görünməz şəkildə yazılır; <code>Reflector.get</code> onu oxuyur. Bu, guard-ın «bu endpoint açıqdırmı? hansı rollar lazımdır?» suallarına cavab verməsinin <em>yeganə</em> yoludur."),
        ("`getAllAndOverride` ilə `getAll` fərqi nədir?",
         "<code>getAll</code> <em>hamısını</em> massiv kimi qaytarır: <code>[[metod], [sinif]]</code>. <code>getAllAndOverride</code> isə <strong>ilk tapılanı</strong> qaytarır — metod varsa onu, yoxsa sinifi. Bizə <em>override</em> lazımdır: metod səviyyəsindəki <code>@Ictimai()</code> sinif səviyyəsindəki rolu üstələməlidir. Əks halda giriş endpoint-i <em>heç vaxt</em> açıq olmazdı."),
        ("403 mesajında rol adlarını göstərmək təhlükəsizdirmi?",
         "Bəli. Rol adları (<code>admin</code>, <code>muhendis</code>, ...) <strong>sirr deyil</strong> — onlar frontend kodunda, sənədləşmədə, hətta URL-lərdə görünür. ⚠️ Amma <em>istifadəçi sayı</em>, <em>başqa istifadəçilərin rolu</em>, <em>daxili ID-lər</em> göstərilməməlidir. Bizim mesaj yalnız «sənin rolun» və «lazım olan rol» deyir — bu, istifadəçiyə <em>kömək edir</em> və zərər vermir."),
        ("Niyə `sorgu.istifadeci` yazırıq, `req`-ə başqa ad vermirik?",
         "Ad seçimi sərbəstdir, amma <strong>ardıcıl olmalıdır</strong>: guard yazır, <code>@CariIstifadeci()</code> oxuyur, <code>RollerGuard</code> oxuyur. ⚠️ Yaxşı vərdiş: xüsusi ad işlətmək (<code>istifadeci</code>, <code>user</code>) — ümumi ad (<code>data</code>, <code>info</code>) başqa kitabxanalarla <em>toqquşa</em> bilər. Həm də <code>req.user</code> adı Passport kitabxanası tərəfindən işlədilir; ondan fərqlənmək üçün <code>istifadeci</code> seçdik."),
        ("`Rol` tipini necə çıxarırıq?",
         "<code>ROLLAR</code> massivini <code>as const</code> elan edirik, sonra:<br><code>export type Rol = (typeof ROLLAR)[number];</code><br>Bu, «massivin elementlərinin birliyi» tipini yaradır: <code>'admin' | 'muhendis' | 'maliyyeci' | 'baxici'</code>. ⚠️ Faydası: rolu <em>bir yerdə</em> dəyişirik, TypeScript-in yoxladığı hər yer avtomatik yenilənir. Yeni rol əlavə etsək, <code>ROL_IERARXIYASI</code> cədvəlində onu unutsaq <strong>kompilyasiya xətası</strong> alarıq."),
        ("`ROL_IERARXIYASI` cədvəlini guard işlədirmi?",
         "⚠️ <strong>Xeyr, işlətmirk.</strong> Bizim guard <em>yalnız açıq sadalanan</em> rollara icazə verir. İerarxiya cədvəli isə <em>köməkçi məlumatdır</em>: frontend «admin hər şeyi görür» məntiqini qurarkən və ya gələcəkdə «muhendis baxicinin hüquqlarını da alır» kimi qayda lazım olanda işlədilir. ⚠️ Səbəb: ierarxiyanı guard-a salsaq, <code>@Roller('baxici')</code> yazanda admin də keçər — bu, <em>gözlənilməz</em> ola bilər. Açıq siyahı daha aydındır."),
        ("`@Ictimai()` niyə token yoxlamasını tamamilə atlayır? Bəlkə token varsa yoxlayaq?",
         "Maraqlı sualdır — və bəzi sistemlər belə edir («yumşaq autentifikasiya»): token varsa istifadəçini tanı, yoxsa da davam et. Bu, məsələn məhsul siyahısında «sənin sevimlilərin» göstərmək üçün lazımdır. ⚠️ Amma riski var: səhv token göndərilsə <em>sükutla</em> açıq endpoint kimi işləyir və istifadəçi «giriş etmişəm?» deyə çaşır. Bizim sadə yanaşma daha aydındır: açıq = tamamilə açıq."),
    ],
    "d_izah": """
<p><strong>Nə öyrəndik:</strong></p>
<ul>
  <li>Qoruyucular <strong>26 yoxlamadan</strong> keçdi.</li>
  <li><strong>401 vs 403 ayrımı işləyir:</strong> token səhvdirsə
      401, rol kifayət etmirsə 403. Bu, frontend üçün həlledicidir.</li>
  <li><strong>Guard nəticəni ötürür:</strong>
      <code>sorgu.istifadeci</code> doldurulur, ona görə
      <code>@CariIstifadeci()</code> və <code>RollerGuard</code>
      işləyir.</li>
  <li><strong>Metod örtmə işləyir:</strong> sinif səviyyəsindəki
      rolu <code>@Ictimai()</code> üstələyir.</li>
  <li><strong>Qoruyucular yalnız <code>AuthController</code>-ə
      qoşulub</strong> və <code>APP_GUARD</code> <em>yoxdur</em> —
      bu, planlı qərardır, köhnə 40 testi qoruyur.</li>
  <li><strong>Dekorator məntiqi test edilə bilir</strong> — çünki
      ayrı funksiya (<code>cariIstifadeciFabriki</code>) kimi
      yazılıb.</li>
</ul>
<p>Son addımda <strong>controller</strong>-i yazıb hər şeyi
birləşdirəcəyik: endpoint-lər, modul, <code>.env.example</code> və
<code>3a_yoxla.sh</code> — canlı serverin tam yoxlaması.</p>
""",
})


# ══════════════════════════════════════════════════════════════════════
#  ADDIM 31 — CONTROLLER, MODUL VƏ CANLI YOXLAMA
# ══════════════════════════════════════════════════════════════════════
ADIMLAR.append({
    "no": 31,
    "ad": "AuthController, modul qeydiyyatı və canlı uçdan-uca yoxlama",
    "a": """
<p>Bütün parçalar hazırdır. İndi onları <strong>birləşdiririk</strong>:
HTTP endpoint-lər, modul qeydiyyatı və <code>.env.example</code>.
Sonunda <em>canlı serveri</em> qaldırıb uçdan-uca yoxlayacağıq.</p>

<h4>🌐 Hansı endpoint-lər olacaq?</h4>
<table style="width:100%;border-collapse:collapse;font-size:.85rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Metod</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Yol</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Rol</th>
    <th style="text-align:left;padding:.45rem;border:1px solid #e2e8f0">Nə edir</th>
  </tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0">POST</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/auth/qeydiyyat</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">🔓 açıq</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">Yeni istifadəçi (rol <code>baxici</code>) → 201</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0">POST</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/auth/giris</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">🔓 açıq</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">E-poçt + parol → token → 200</td></tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0">GET</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/auth/me</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">🔒 giriş</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">Tokenin içindəki məlumat</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0">GET</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/auth/admin-yoxlama</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">admin</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">RBAC nümunəsi</td></tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0">GET</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/auth/muhendis-yoxlama</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">admin, mühendis</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">İki rollu endpoint</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0">GET</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/auth/istifadeciler</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">admin</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">Bütün istifadəçilər</td></tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0">PATCH</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/auth/istifadeci/:id/rol</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">admin</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">Rol dəyişmə</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.45rem;border:1px solid #e2e8f0">PATCH</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/auth/istifadeci/:id/aktivlik</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">admin</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">Aktiv/deaktiv</td></tr>
  <tr><td style="padding:.45rem;border:1px solid #e2e8f0">GET</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0"><code>/auth/yoxlama</code></td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">🔓 açıq</td>
      <td style="padding:.45rem;border:1px solid #e2e8f0">Sağlamlıq (monitorinq)</td></tr>
</table>

<h4>⚠️ Status kodları — «201 vs 200» incəliyi</h4>
<p>Yeni başlayanlar tez-tez bunu səhv edir. HTTP-də status kodunun
<strong>mənası</strong> var:</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Kod</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Mənası</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Bizdə</th>
  </tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0"><strong>200</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Uğurlu, <em>yeni resurs yaradılmadı</em></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Giriş, oxuma, yeniləmə</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0"><strong>201</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Uğurlu, <strong>yeni resurs yaradıldı</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Qeydiyyat</td></tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0"><strong>400</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Məlumat səhvdir (validasiya)</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Zəif parol, səhv e-poçt formatı, qısa <code>ad_soyad</code>, səhv tip</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0"><strong>401</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Tanınmadı <em>(kim olduğunu bilmirəm)</em></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Token yoxdur/səhvdir, parol səhvdir</td></tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0"><strong>403</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">İcazə yoxdur <em>(tanıdım, amma olmaz)</em></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Rol kifayət etmir, <strong>hesab deaktivdir</strong></td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0"><strong>404</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Tapılmadı</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">İstifadəçi ID-si yoxdur</td></tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0"><strong>409</strong></td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Konflikt — resurs artıq mövcuddur</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Mövcud e-poçtla qeydiyyat</td></tr>
</table>
<p>⚠️ <strong>NestJS POST üçün standart olaraq 201 qaytarır.</strong>
Giriş endpoint-i isə yeni resurs <em>yaratmır</em> — sadəcə token
verir. Ona görə <code>@HttpCode(200)</code> ilə düzəldirik. Bu
düzəliş olmasa:</p>
<pre style="background:#7f1d1d;color:#fff;border-radius:8px;padding:1rem 1.1rem">
$ curl -X POST .../auth/giris -d '{...}'
HTTP/1.1 201 Created                    ← ⚠️ yanıltıcı!
{"access_token": "..."}

⚠️ Frontend «201» görüb «yeni istifadəçi yaradıldı?» düşünür.
⚠️ Bəzi API monitorinq alətləri 201-i «resurs yaradıldı» kimi
   sayır və statistikalar səhv olur.
⚠️ 「201」 cavabında `Location` başlığı gözlənilir — bizdə yoxdur.</pre>

<h4>⚠️ Controller-də biznes məntiqi OLMAMALIDIR</h4>
<p>Diqqət edin: controller metodları <strong>qısadır</strong>.</p>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Post('giris')
@Ictimai()
@HttpCode(200)
async giris(@Body() dto: GirisDto) {
  const istifadeci = await this.istifadeci.parolYoxla(dto.email, dto.parol);
  if (!istifadeci) {
    throw new UnauthorizedException('E-poçt və ya parol səhvdir');
  }
  return this.token.yarat(istifadeci);
}</pre>
<p>Bu, <strong>düzgün</strong> bölgüdür:</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Qat</th>
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Məsuliyyəti</th>
  </tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">Guard</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">İcazə</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0">Pipe (DTO)</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0">Məlumatın forması</td></tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">Controller</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Yönləndirmə</strong> — HTTP ↔ servis tərcüməsi</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0">Service</td>
      <td style="padding:.5rem;border:1px solid #e2e8f0"><strong>Biznes məntiqi</strong> + baza</td></tr>
</table>
<p>⚠️ Niyə bu ayrım vacibdir? Çünki <em>eyni məntiq</em> başqa yerdən
də çağırıla bilər: cron işi, CLI skript, başqa servis, test. Əgər
məntiq controller-də olsaydı, onu təkrar yazmaq lazım gələrdi — və
<em>iki nüsxə</em> zamanla bir-birindən uzaqlaşardı.</p>

<h4>⚠️ Uçdan-uca test niyə zəruridir?</h4>
<p>Bütün hissələri ayrı-ayrı yoxladıq: parol (25), istifadəçi (37),
token (35), qoruyucu (26) — cəmi <strong>123 yoxlama</strong>. Amma
bu, <em>kifayət deyil</em>! Ayrı-ayrı işləyən hissələr
<strong>birlikdə işləməyə bilər</strong>:</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;margin:.8rem 0">
  <tr style="background:#f1f5f9">
    <th style="text-align:left;padding:.5rem;border:1px solid #e2e8f0">Yalnız hissə testi ilə tutulmayan xəta</th>
  </tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">Guard <code>AuthController</code>-ə <em>qoşulmayıb</em> — hər şey işləyir, amma <strong>heç nə qorunmur</strong></td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0">Modulda <code>providers</code> siyahısında servis unudulub → Nest <code>Nest can't resolve dependencies</code> xətası verir</td></tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0">Guard sırası səhvdir → 403 yerinə 401 gəlir</td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0"><code>@HttpCode(200)</code> unudulub → giriş 201 qaytarır</td></tr>
  <tr><td style="padding:.5rem;border:1px solid #e2e8f0"><code>@Ictimai()</code> giriş endpoint-də yoxdur → <strong>heç kim girə bilmir</strong></td></tr>
  <tr style="background:#f8fafc"><td style="padding:.5rem;border:1px solid #e2e8f0"><code>JWT_SECRET</code> yoxdur → server açılmır (bu, düzgün davranışdır, amma bilmək lazımdır)</td></tr>
</table>
<p>Ona görə <code>3a_yoxla.sh</code> <strong>real serveri qaldırır</strong>
və <code>curl</code> ilə 30 yoxlama aparır — <em>tam istifadəçi
axınını</em> təqlid edərək.</p>

<h4>⚠️ Testin istifadəçi yaratması — təmizlik qaydası</h4>
<p>Test qeydiyyat endpoint-ini yoxlamalıdır, yəni <em>istifadəçi
yaratmalıdır</em>. Bu, bazaya yazı deməkdir. İki qayda:</p>
<ol>
  <li><strong>Xüsusi prefiks:</strong> yalnız
      <code>test.3a.&lt;vaxt&gt;@arti.edu.az</code> formatında e-poçtlar.
      Real 4 istifadəçiyə (admin, mühendis, maliyyeci, baxici)
      <em>toxunulmur</em>.</li>
  <li><strong>Mütləq təmizlik:</strong> <code>trap ... EXIT INT TERM</code> —
      skript <em>necə bitirsə də</em> (uğurla, xəta ilə, yoxsa
      Ctrl+C ilə) təmizləmə funksiyası işləyir.</li>
</ol>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
temizle() {
  [ -n "$PID" ] &amp;&amp; kill "$PID" 2&gt;/dev/null      # serveri dayandır
  ...
  psql "$DBURL" -At -c "DELETE FROM kadrlar.istifadeciler
    WHERE email LIKE 'test.3a.%@arti.edu.az';"
  rm -rf "$TMP"
}
trap temizle EXIT INT TERM</pre>
<p>⚠️ <code>trap</code> olmasa, skript yarıda kəsilsə test
istifadəçiləri bazada <strong>əbədi qalar</strong> və növbəti
işlədilmədə «bu e-poçt artıq mövcuddur» xətası yaranar. Bu,
<em>klassik</em> test problemidir: testlər bir-birini
çirkləndirir.</p>
""",
    "anlayis": [
        ("Controller",
         "HTTP sorğularını qarşılayan sinif. Marşrutları servislərə "
         "bağlayır — biznes məntiqi saxlamır."),
        ("`@HttpCode`",
         "Standart status kodunu dəyişir. Nest POST üçün 201, "
         "digərləri üçün 200 işlədir."),
        ("`@Param`",
         "URL-dəki dəyişəni metod parametrinə ötürür: "
         "<code>:id</code> → <code>id</code>."),
        ("`ParseIntPipe`",
         "Mətn formasındaki URL dəyişənini ədədə çevirir; "
         "mümkün deyilsə 400 verir."),
        ("`@UseGuards`",
         "Guard-ı controller və ya metod səviyyəsində qoşur."),
        ("`providers`",
         "Modulun DI konteynerinə qeydiyyatdan keçən siniflər — "
         "Nest onların nüsxələrini özü yaradır."),
        ("`exports`",
         "Başqa modulların istifadə edə biləcəyi servislər. "
         "İxrac etməsək, digər modul <em>tapa bilməz</em>."),
        ("`registerAsync`",
         "Modulun konfiqurasiyasını asinxron hazırlayır — "
         "<code>ConfigService</code> kimi asılılıqları gözləyir."),
        (".env.example",
         "Nümunə konfiqurasiya faylı. Git-ə <em>yazılır</em>, ona görə "
         "orada sirr olmamalıdır."),
        ("Uçdan-uca test",
         "«End-to-end» — bütün qatları birlikdə, real serverlə yoxlama."),
        ("`trap`",
         "Shell-də siqnal tutucusu. Skript necə bitirsə də "
         "təmizləmə işləyir."),
        ("Test izolyasiyası",
         "Hər test öz məlumatını yaradır və silir; başqalarına "
         "toxunmur."),
    ],
    "kod_izah": """
<h5 style="color:#334155;margin-top:.3rem">1) Controller sinfi və guard-ın qoşulması</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Controller('auth')
@UseGuards(AuthGuard, RollerGuard)
export class AuthController {
  constructor(
    private readonly istifadeci: IstifadeciService,
    private readonly token: TokenService,
  ) {}
}</pre>
<ul>
  <li><code>@Controller('auth')</code> — prefiks. <code>main.ts</code>-də
      qlobal prefiks <code>api/v1</code> olduğu üçün tam yol:
      <code>/api/v1/auth/...</code>.</li>
  <li>⚠️ <strong>Guard sırası:</strong> əvvəlcə <code>AuthGuard</code>
      («kim gəldi?»), sonra <code>RollerGuard</code> («nə edə bilər?»).
      Tərsinə olsa, <code>RollerGuard</code> <code>req.istifadeci</code>-ni
      boş tapar və <em>403 yerinə 401</em> verər.</li>
  <li>⚠️ <strong>Constructor ilə asılılıq inyeksiyası:</strong> Nest
      <code>AuthController</code>-i yaradanda servisləri
      <em>özü</em> ötürür. Ona görə modulda
      <code>providers</code> siyahısında olmalıdırlar — yoxsa
      <code>Nest can't resolve dependencies</code> xətası.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">2) Qeydiyyat — 201 və <code>@Ictimai()</code></h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Post('qeydiyyat')
@Ictimai()
@HttpCode(201)
qeydiyyat(@Body() dto: QeydiyyatDto) {
  return this.istifadeci.qeydiyyat(dto);
}</pre>
<ul>
  <li><code>@HttpCode(201)</code> — Nest POST üçün <em>onsuz da</em> 201
      verir. Açıq yazmağımız <strong>sənədləşdirmə</strong> məqsədi
      daşıyır: oxuyan dərhal görür ki, bu, resurs yaradır.</li>
  <li>⚠️ <code>@Ictimai()</code> olmasa, qeydiyyat endpoint-i də token
      tələb edərdi → <strong>heç kim qeydiyyatdan keçə bilməzdi</strong>.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">3) Giriş — iki servisin birləşməsi</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Post('giris')
@Ictimai()
@HttpCode(200)
async giris(@Body() dto: GirisDto) {
  const istifadeci = await this.istifadeci.parolYoxla(dto.email, dto.parol);
  if (!istifadeci) {
    throw new UnauthorizedException('E-poçt və ya parol səhvdir');
  }
  return this.token.yarat(istifadeci);
}</pre>
<ul>
  <li>⚠️ <strong>İki addım:</strong> əvvəlcə <em>autentifikasiya</em>
      (parol yoxlanılır), sonra <em>avtorizasiya bileti</em> (token)
      verilir. Bu ayrımı qarışdırmaq olmaz — parol yoxlaması
      <code>IstifadeciService</code>-in, token isə
      <code>TokenService</code>-in işidir.</li>
  <li><code>parolYoxla()</code> uğursuz olsa <code>null</code> qaytarır
      (xəta <em>atmır</em>). Səbəb: servis qərar vermir,
      <em>məlumat</em> qaytarır; qərarı controller verir. Bu,
      test edilə bilənliyi artırır.</li>
  <li>⚠️ Mesaj <strong>ümumidir</strong>: «E-poçt və ya
      parol səhvdir». Ayrı-ayrı desəydik, hücumçu hansı e-poçtların
      mövcud olduğunu öyrənərdi.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">4) <code>@CariIstifadeci()</code> və <code>me</code></h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Get('me')
me(@CariIstifadeci() cari: YoxlanilmisYuku) {
  return {
    sub: cari.sub,
    email: cari.email,
    ad_soyad: cari.ad_soyad,
    rol: cari.rol,
    token_verildi: new Date(cari.iat * 1000).toISOString(),
    token_bitir: new Date(cari.exp * 1000).toISOString(),
  };
}</pre>
<ul>
  <li>⚠️ Bu endpoint-də <code>@Roller(...)</code> <strong>yoxdur</strong> —
      yəni hər hansı <em>giriş etmiş</em> istifadəçi görə bilər.
      Səbəb: bu, öz profilidir, başqasının deyil.</li>
  <li>⚠️ <code>* 1000</code> — <code>iat</code>/<code>exp</code> Unix
      <em>saniyə</em>dir, JS <code>Date</code> isə <em>millisaniyə</em>
      gözləyir. Vurmasaq, tarix <strong>1970-ci ili</strong> göstərərdi.</li>
  <li>Diqqət: <code>parol_hash</code> yoxdur — çünki tokenin içində
      <em>heç vaxt</em> olmur.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">5) RBAC nümunə endpoint-ləri</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Get('admin-yoxlama')
@Roller('admin')
adminYoxlama(@CariIstifadeci() cari: YoxlanilmisYuku) { ... }

@Get('muhendis-yoxlama')
@Roller('admin', 'muhendis')
muhendisYoxlama(@CariIstifadeci() cari: YoxlanilmisYuku) { ... }

@Get('istifadeciler')
@Roller('admin')
istifadeciler() { return this.istifadeci.hamisi(); }</pre>
<ul>
  <li>Bu iki <code>-yoxlama</code> endpoint-i sırf <strong>təlim
      məqsədi</strong> daşıyır: rol məntiqini canlı sınamaq üçün.
      Real layihədə belə endpoint-lər ya olmur, ya da yalnız
      inkişaf mühitində olur.</li>
  <li>⚠️ <code>@Roller('admin', 'muhendis')</code> — <em>İKİSİNDƏN
      BİRİ</em> kifayətdir (OR məntiqi). Əgər <em>hər ikisi</em> lazım
      olsaydı (AND), bu, fərqli bir dekorator olardı — və praktikada
      çox nadir hallarda lazım olur.</li>
  <li><code>istifadeciler()</code> — <code>@Roller('admin')</code>
      sayəsində yalnız admin bütün istifadəçi siyahısını görür.
      ⚠️ Cavabda <code>parol_hash</code> yoxdur (ADDIM 28-də
      həll etdik).</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">6) <code>ParseIntPipe</code> — URL-dən ədəd</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Patch('istifadeci/:id/rol')
@Roller('admin')
rolDeyis(
  @Param('id', ParseIntPipe) id: number,
  @Body() dto: RolDeyisDto,
) {
  return this.istifadeci.rolDeyis(id, dto.rol);
}</pre>
<ul>
  <li>⚠️ URL-dəki <strong>hər şey mətndir</strong>. <code>id</code>
      avtomatik <code>number</code> olmur!</li>
  <li><code>ParseIntPipe</code> olmasa: <code>Number('abc')</code> →
      <code>NaN</code> → <code>where: { id: NaN }</code> → Prisma
      <em>anlaşılmaz</em> xəta verər (500).</li>
  <li><code>ParseIntPipe</code> ilə: <code>/istifadeci/abc/rol</code> →
      <strong>400 Bad Request</strong> — aydın cavab.</li>
  <li>⚠️ Bizim versiyada yalnız <code>ParseIntPipe</code> var, yəni
      <code>-5</code> və <code>0</code> da <em>keçir</em>. Sonra
      servis «istifadəçi tapılmadı» deyir. Daha sərt yoxlama üçün
      <code>ParseIntPipe({ errorHttpStatusCode: 400 })</code> və
      ya xüsusi pipe yazmaq olar.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">7) <code>JwtModule.registerAsync</code> — «uğursuz-erkən»</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
JwtModule.registerAsync({
  imports: [ConfigModule],
  inject: [ConfigService],
  useFactory: (config: ConfigService) =&gt; {
    const sirr = config.get&lt;string&gt;('JWT_SECRET');
    if (!sirr || sirr.length &lt; MIN_SIRR_UZUNLUGU) {
      throw new Error('JWT_SECRET ... çox qısadır ...');
    }
    return {
      secret: sirr,
      signOptions: {
        expiresIn: muddurSaniyeye(config.get('JWT_MUDDET') ?? STANDART_MUDDET),
      },
    };
  },
}),</pre>
<ul>
  <li>⚠️ <strong>Niyə <code>register</code> deyil?</strong>
      <code>JwtModule.register({ secret: process.env.JWT_SECRET })</code>
      yazsaq, o zaman <code>.env</code> <em>hələ oxunmamış</em> olardı —
      <code>register</code> fayl yüklənəndə işləyir, <code>ConfigModule</code>
      isə sonra. Nəticə: <code>secret: undefined</code> və
      <strong>heç bir token yoxlanıla bilməzdi</strong>. Bu, çox
      məkrli bir xətadır, çünki server <em>açılır</em> və yalnız
      giriş cəhdində problem çıxır.</li>
  <li>⚠️ <strong>Uğursuz-erkən (fail-early):</strong> server
      <em>açılmır</em>. Bu, düzgün davranışdır: səhv konfiqurasiya ilə
      işləyən sistem, <em>işləməyən</em> sistemdən qat-qat
      təhlükəlidir.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">8) <code>app.module.ts</code> — modulun qoşulması</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    SaglamliqModule,
    EmekdaslarModule,
    AuditModule,
    AuthModule,          // ← YENİ
  ],
})
export class AppModule {}</pre>
<ul>
  <li>⚠️ <strong>Bu bir sətir olmasa, heç nə işləməz.</strong> Nest
      yalnız <em>qeydiyyatdan keçmiş</em> modulların controller-lərini
      tanıyır.</li>
  <li><code>isGlobal: true</code> — <code>ConfigService</code> hər
      yerdə əlçatan olur, ayrıca import lazım deyil.</li>
</ul>

<h5 style="color:#334155;margin-top:1rem">9) <code>.env.example</code> — sirr olmayan nümunə</h5>
<pre style="background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.1rem">
# ⚠️ Bu fayl GIT-Ə YAZILIR — burada HEÇ BİR SİRR OLMAMALIDIR.
JWT_SECRET="bu-yerine-oz-tesadufi-sirrinizi-yazin-en-azi-32-simvol"
JWT_MUDDET="1h"</pre>
<ul>
  <li>⚠️ <code>.env</code> <code>.gitignore</code>-dadır, amma
      <code>.env.example</code> <strong>git-ə yazılır</strong> —
      komandaya «hansı dəyişənlər lazımdır» demək üçün.</li>
  <li>Ona görə orada <em>real</em> sirr olmaz. Bu dərsdə bir dəfə
      səhv etdik və düzəltdik — bunu <strong>3A-nın
      problemlər bölməsində</strong> ətraflı yazmışıq.</li>
  <li>Şərhdə sirrin <em>necə yaradılacağı</em> göstərilir:
      <code>openssl rand -base64 48</code>.</li>
</ul>
""",
    "fayllar": [
        "src/auth/dto/rol.dto.ts",
        "src/auth/auth.controller.ts",
        "src/auth/auth.module.ts",
        "src/app.module.ts",
        ".env.example",
        "skriptler/3a_yoxla.sh",
    ],
    "goster": [],
    "c": r"""
echo "════ 1) Tip yoxlaması ════"
if npx tsc --noEmit; then echo "  ✓ tip xətası yoxdur"; else echo "  ✗ tip xətası var"; fi

echo ""
echo "════ 2) Modul qrafı ════"
grep -n 'Module' src/app.module.ts | grep -E '^\s*[0-9]+:\s+[A-Z]' | sed 's/^/      /'
printf '      app.module-də modul sayı: %s\n' "$(grep -cE '^\s+[A-Z][A-Za-z]+Module,' src/app.module.ts)"

echo ""
echo "════ 3) Endpoint siyahısı (controller-dən) ════"
grep -nE "@(Get|Post|Patch|Delete)\(" src/auth/auth.controller.ts | sed 's/^/      /'

echo ""
echo "════ 4) Fayllar ════"
for f in src/auth/dto/rol.dto.ts src/auth/auth.controller.ts src/auth/auth.module.ts \
         src/app.module.ts .env.example skriptler/3a_yoxla.sh; do
  printf '      %-38s %4s sətir\n' "$f" "$(wc -l < "$f" | tr -d ' ')"
done

echo ""
echo "════ 5) 3A fayl strukturu (cəmi) ════"
printf '      src/auth/            : %2s fayl, %4s sətir\n' \
  "$(find src/auth -name '*.ts' | wc -l | tr -d ' ')" \
  "$(cat $(find src/auth -name '*.ts') | wc -l | tr -d ' ')"
printf '      skriptler/           : %2s fayl\n' "$(ls skriptler/*.ts skriptler/*.sh 2>/dev/null | wc -l | tr -d ' ')"

echo ""
echo "════ 6) CANLI SERVER — uçdan-uca yoxlama (30 yoxlama) ════"
PORT=4111 bash skriptler/3a_yoxla.sh
""",
    "olmaz": """`AuthModule` `app.module.ts`-ə əlavə olunmasa:

$ curl -X POST .../api/v1/auth/giris -d '{...}'
HTTP/1.1 404 Not Found
{"message":"Cannot POST /api/v1/auth/giris", "error":"Not Found"}

  ⚠️ Nest auth modulunu ÜMUMİYYƏTLƏ tanımır.
  ⚠️ Server AÇILIR, sağlamlıq yoxlaması İŞLƏYİR, köhnə endpoint-lər
     İŞLƏYİR — yalnız auth yoxdur. Ən çaşdırıcı xəta növü.
  ⚠️ Axtarış yeri: app.module.ts-in `imports` massivi.

────────────────────────────────────────────────────────────
Guard `@UseGuards` ilə qoşulmasa:

$ curl .../auth/me                   # TOKEN OLMADAN
HTTP/1.1 200 OK
{"sub":2,"email":"admin@arti.edu.az","rol":"admin", ...}
                            ↑ ⚠️⚠️ TOKEN GÖNDƏRMƏDƏN CAVAB GƏLDİ!

  ⚠️ Kod işləyir, testlər keçir, heç bir xəta yoxdur —
     AMMA SİSTEM TAMAMİLƏ AÇIQDIR.
  ⚠️ Bu, ən TƏHLÜKƏLİ xəta növüdür: «sükutlu təhlükəsizlik
     pozuntusu». Heç nə qırmızı olmur, sadəcə qoruma yoxdur.
  ⚠️ Ona görə uçdan-uca test MÜTLƏQ «401 gözlənilir» yoxlaması
     etməlidir — yalnız «200 gəlir» yox.

────────────────────────────────────────────────────────────
`@Ictimai()` giriş endpoint-də olmasa:

$ curl -X POST .../auth/giris -d '{...}'
HTTP/1.1 401 Unauthorized
{"message":"Giriş tələb olunur — Authorization: Bearer <token> ..."}
                            ↑ ⚠️ GİRİŞ ÜÇÜN TOKEN TƏLƏB OLUNUR!

  ⚠️ «Yumurtamı toyuqdan, toyuqmu yumurtadan?» problemi.
  ⚠️ HEÇ KİM sistemə girə bilmir — o cümlədən admin.
  ⚠️ Əl ilə bazaya girib token yaratmaq lazım gəlir.

────────────────────────────────────────────────────────────
`@HttpCode(200)` girişdə olmasa:

$ curl -X POST .../auth/giris -d '{...}'
HTTP/1.1 201 Created                  ← ⚠️ YANLIŞ status
{"access_token":"...", "istifadeci": {...}}

  ⚠️ Giriş yeni resurs YARATMIR — sadəcə token verir.
  ⚠️ Frontend «201» görüb «yeni istifadəçi yaradıldı?» düşünür.
  ⚠️ Monitorinq alətləri 201-i «resurs yaradıldı» kimi sayır.

────────────────────────────────────────────────────────────
`providers`-də servis unudulsa:

$ npm run build && npm start
[Nest] ERROR [ExceptionHandler] Nest can't resolve dependencies of
the AuthController (?, TokenService). Please make sure that the
argument IstifadeciService at index [0] is available in the
AuthModule context.

  ✓ Bu, YAXŞI xəta növüdür: aydın, dəqiq, index göstərir.
  ⚠️ Ən azı server AÇILMIR — sükutla sınıq işləmir.

────────────────────────────────────────────────────────────
`JWT_SECRET` olmasa:

$ npm start
Error: JWT_SECRET təyin olunmayıb və ya çox qısadır (minimum 32 simvol).
Yaratmaq üçün: openssl rand -base64 48

  ✓ «Uğursuz-erkən» prinsipi işləyir: server QALXMIR.
  ⚠️ Alternativ (səhv) yanaşma: default dəyər qoysaq, sistem
     hamının bildiyi sirrlə işləyərdi və hər kəs admin tokeni
     yarada bilərdi.""",
    "c_izah": """
<p><strong>Bu, dərsin ən vacib yoxlamasıdır</strong> — çünki burada
bütün qatlar <em>birlikdə</em> işləyir.</p>

<p><strong>1. Açıq endpoint-lər işləyir.</strong> Qeydiyyat 201
qaytarır, giriş 200 qaytarır və gələn cavabda
<code>access_token</code>, <code>token_novu: "Bearer"</code>,
<code>muddet_saniye</code> var. Sağlamlıq endpoint-i sirrin
<em>uzunluğunu</em> göstərir, dəyərini yox.</p>

<p><strong>2. Zəif parol rədd edilir (400).</strong>
<code>123456</code> parolu ilə qeydiyyat cəhdi keçmir — ADDIM 27-də
yazdığımız validatör işləyir. Bu, ən vacib təhlükəsizlik
qatıdır.</p>

<p><strong>3. Rol inyeksiyası qapadılıb.</strong>
<code>{"rol":"admin"}</code> göndərmək <strong>400</strong> verir —
DTO-da <code>forbidNonWhitelisted</code> sayəsində. Yoxlasaydıq
<em>heç nə</em> görməzdik, çünki bu, sükutlu bir sızma olardı.</p>

<p><strong>4. Mövcud e-poçt 409 verir.</strong> Eyni e-poçtu
ikinci dəfə qeydiyyatdan keçirmək mümkün deyil — bazada
<code>unique</code> məhdudiyyəti var və Prisma-nın
<code>P2002</code> xətası <code>ConflictException</code>-a çevrilir.
⚠️ <strong>409, 400 yox</strong> — çünki sorğunun özü
<em>düzgündür</em>; problem <strong>resursun artıq mövcud
olmasıdır</strong>. «400» yazsaq, frontend «məlumatı düzəlt»
kimi başa düşərdi; «409» isə «bu artıq var» deməkdir.</p>

<p><strong>5. Səhv parol 401 verir, düzgün parol token verir.</strong>
⚠️ İkisinin cavabı <em>eyni formadadır</em> — bu, istifadəçi
siyahısının çıxarılmasının qarşısını alır.</p>

<p><strong>6. Tokenin quruluşu sınaqdan keçir.</strong> Skript
tokeni üç hissəyə bölür, <code>base64url</code> ilə açır və
payload-da <strong>yalnız</strong> <code>sub</code>,
<code>email</code>, <code>ad_soyad</code>, <code>rol</code>,
<code>iat</code>, <code>exp</code> olduğunu yoxlayır.
<code>parol_hash</code> <em>yoxdur</em>.</p>

<p><strong>7. Saxtalaşdırma işləmir.</strong> Skript tokenin
payload-unu açır, <code>rol</code>-u <code>admin</code>-ə dəyişir,
yenidən kodlayır və <em>köhnə imzanı</em> saxlayır. Server
<strong>401</strong> verir. Yəni imza öz işini görür.</p>

<p><strong>8. RBAC düzgün işləyir.</strong> Dörd real istifadəçi ilə
giriş edilir və hər birinin <code>/admin-yoxlama</code> və
<code>/muhendis-yoxlama</code> cavabları gözlənilən kimidir:</p>
<ul>
  <li><code>admin</code> → hər ikisinə <em>200</em>,</li>
  <li><code>muhendis</code> → admin-yoxlama <em>403</em>,
      muhendis-yoxlama <em>200</em>,</li>
  <li><code>maliyyeci</code> → hər ikisinə <em>403</em>,</li>
  <li><code>baxici</code> → hər ikisinə <em>403</em>.</li>
</ul>
<p>⚠️ <strong>403, 401 yox</strong> — bu, kritik fərqdir. Yəni
istifadəçi <em>tanınır</em>, sadəcə icazəsi yoxdur. Test bunu
<em>ayrıca</em> yoxlayır.</p>

<p><strong>9. Admin istifadəçi idarəsi işləyir.</strong> Yeni test
istifadəçisinin rolu <code>baxici</code> → <code>muhendis</code>
dəyişdirilir və dərhal <code>muhendis-yoxlama</code>
<em>200</em> verir. Sonra <code>aktiv=false</code> edilir və giriş
<em>403</em> olur — <strong>deaktiv hesab giriş edə bilmir</strong>.
⚠️ Diqqət: <strong>403</strong>, 401 yox — çünki parol
<em>düzgün</em> idi, yəni istifadəçi tanındı; sadəcə hesabın
<em>istifadəsinə icazə yoxdur</em>. Frontend bu halda «hesabınız
deaktivdir» mesajı göstərməlidir, giriş səhifəsinə atmamalıdır.</p>

<p><strong>10. Təmizlik işləyir.</strong> Sonda bazadaki istifadəçi
sayı <strong>4-ə qayıdır</strong> — test heç bir iz qoymur. Bu,
<code>trap</code>-ın bəhrəsidir.</p>
""",
    "sual": [
        ("Controller-də `@Res()` işlədib cavabı əl ilə yazmaq olarmı?",
         "Olar, amma ⚠️ <strong>tövsiyə olunmur</strong>. <code>@Res()</code> işlətdikdə Nest-in cavab idarəsi <em>söndürülür</em>: interceptor-lar, exception filter-lər, status kodu məntiqi — heç biri işləmir. Siz <code>res.json()</code>, <code>res.status()</code> və səhvləri <em>əl ilə</em> yazmalısınız. Yalnız xüsusi halda (fayl yükləmə, SSE, streaming) lazımdır. Bizim bütün endpoint-lər adi JSON qaytarır — <code>@Res()</code> lazım deyil."),
        ("Niyə `hamisi()` servisdə, controller-də filtr yoxdur?",
         "Filtr <em>servisdə</em> olmalıdır — çünki filtr <strong>biznes qaydasıdır</strong>, HTTP detalları deyil. Əgər filtr controller-də olsaydı, eyni məntiqi CLI skriptdə və ya cron işində <em>təkrar</em> yazmalı olardıq. ⚠️ Amma <strong>icazə</strong> filtrini controller/guard səviyyəsində saxlamaq düzgündür: «kim görə bilər» HTTP qatının qərarıdır, «nə göstərilir» isə biznes qatının."),
        ("`@Roller()` çoxlu rol yazanda OR, yoxsa AND məntiqi işləyir?",
         "<strong>OR</strong> — <code>@Roller('admin','muhendis')</code> yazsaq, <em>ikisindən biri</em> kifayətdir. Guard kodu buna aydın dəlildir: <code>teleb.includes(istifadeci.rol)</code> — massivdə <em>varsa</em> keçir. ⚠️ AND məntiqi praktikada çox nadir hallarda lazım olur (bir istifadəçinin iki rolu olsaydı). Lazım olsaydı, ayrıca dekorator yazardıq: <code>@ButunRoller('admin','muhendis')</code>."),
        ("`ParseIntPipe` ilə mənfi ədədləri necə bloklayım?",
         "İki yol var: (1) <code>ParseIntPipe</code> yalnız <em>tam ədəd</em> yoxlayır, mənfiliyi yox — servisdə <code>id &lt; 1</code> yoxlaması əlavə edin; (2) xüsusi pipe yazın: <code>@Injectable() class MusbetIdPipe implements PipeTransform</code> — <code>transform</code>-da həm ədəd, həm müsbət olduğunu yoxlayın. ⚠️ Bizim halda birinci yol kifayətdir, çünki ID-lər bazada <code>serial</code>-dır (1-dən başlayır) və mənfi ID sadəcə «tapılmadı» verir."),
        ("`.env.example` faylında sirr olsa nə olar?",
         "⚠️ <strong>Real problemdir</strong> və bizim dərsdə bir dəfə baş verdi. <code>.env.example</code> Git-ə yazılır, ona görə oradaki sirr <em>bütün komandaya</em> və repo açıqdırsa, <strong>bütün dünyaya</strong> görünür. Nəticə: hər kəs istənilən istifadəçi üçün etibarlı token yarada bilər. Əgər sirr sızıbsa, düzəltmə yolu: (1) dərhal <em>yeni</em> sirr yarat, (2) köhnəni ləğv et, (3) Git tarixçəsindən təmizlə (<code>git filter-repo</code>), (4) <em>bütün</em> istifadəçiləri çıxar (sirr dəyişdi, köhnə tokenlər etibarsızdır)."),
        ("Test üçün ayrıca baza yaratmaq lazım deyilmi?",
         "İdeal dünyada — bəli. Praktikada iki yanaşma var: (1) <strong>ayrı test bazası</strong> (<code>arti_baza_test</code>) — təmiz, amma saxlamaq əlavə iş tələb edir; (2) <strong>prefiksli məlumat + məcburi təmizlik</strong> — bizim seçimimiz. ⚠️ İkincisinin riski: <code>trap</code> işləməsə məlumat qalır. Ona görə skript <em>əvvəlində də</em> təmizlik edir və sonda sayı yoxlayır (4). Böyük layihələrdə isə Docker ilə <em>hər dəfə təzə</em> baza qaldırılır."),
        ("Niyə PORT=4111 işlədirik, 4000 yox?",
         "Çünki istifadəçinin <em>artıq işləyən</em> serveri ola bilər (məsələn əvvəlki dərsdən). 4000 məşğuldursa, <code>EADDRINUSE</code> xətası yaranar və test <em>köhnə</em> serverə qoşular — nəticə yanıltıcı olar. Ayrıca port işlətməklə test <strong>öz təcrid olunmuş mühitində</strong> işləyir. ⚠️ Skript buna görə <code>PORT=\"${PORT:-4000}\"</code> yazır: standart 4000, amma <em>dəyişmək olar</em>."),
        ("`kill \"$PID\"` niyə `wait` ilə birlikdə işlədilir?",
         "<code>kill</code> <em>siqnal göndərir</em>, amma proses dərhal ölmür — əvvəlcə açıq bağlantıları bağlayır, faylları yazır. <code>wait</code> isə <em>gözləyir</em> ki, proses həqiqətən bitsin. ⚠️ <code>wait</code> olmasa, skript davam edir və baza bağlantısı hələ açıq olduğu üçün <code>DELETE</code> sorğusu <em>gözləyə</em> bilər və ya sıradan çıxa bilər. Kiçik detaldır, amma testlərin <em>etibarlılığını</em> təmin edir."),
        ("`3a_yoxla.sh`-ı hər dəfə işlətmək lazımdır?",
         "Bəli — hər dəyişiklikdən sonra. Bu, <strong>reqressiya testi</strong> adlanır: köhnə funksionallığın hələ də işlədiyini yoxlayır. ⚠️ Xüsusilə vacibdir ki, sonrakı dərslərdə (3B, Frontend) nəyisə dəyişəndə <em>dərhal</em> biləsən. Peşəkar komandalarda bu, <strong>CI/CD</strong> ilə avtomatik edilir: hər <code>git push</code>-da testlər işləyir və qırmızı olsa, dəyişiklik qəbul edilmir."),
    ],
    "d_izah": """
<p><strong>Dərs 3A tamamlandı!</strong> Addım 31 <em>hər şeyi</em>
birləşdirdi və canlı serverdə yoxladı.</p>

<p><strong>Nəticə: 30/30 yoxlama keçdi.</strong> Bu o deməkdir ki,
tam istifadəçi axını işləyir:</p>
<pre style="background:#064e3b;color:#d1fae5;border-radius:8px;padding:1rem 1.1rem">
1.  Qeydiyyat (açıq)           → 201 + istifadəçi (hash-siz)
2.  Zəif parol                 → 400 ✗ rədd edildi
3.  Rol inyeksiyası            → 400 ✗ rədd edildi
4.  Mövcud e-poçt              → 409 ✗ rədd edildi (konflikt)
5.  Səhv parol                 → 401 ✗ rədd edildi
6.  Düzgün parol               → 200 + access_token
7.  Token quruluşu             → 3 hissə, parol_hash YOXDUR
8.  Saxta token                → 401 ✗ rədd edildi
9.  Token olmadan qorunan yol  → 401 ✗ rədd edildi
10. admin  /admin-yoxlama      → 200 ✓
11. mühendis /admin-yoxlama    → 403 ✗ (icazə yoxdur — 401 DEYİL)
12. mühendis /muhendis-yoxlama → 200 ✓
13. maliyyeci /admin-yoxlama   → 403 ✗
14. baxici  /muhendis-yoxlama  → 403 ✗
15. admin istifadəçi siyahısı  → 200 ✓
16. admin rol dəyişmə          → 200 ✓ → yeni rol işləyir
17. admin aktivlik             → 200 ✓ → giriş 401 olur
18. Təmizlik                   → istifadəçi sayı 4-ə qayıtdı
</pre>

<p><strong>Texniki nəticələr:</strong></p>
<ul>
  <li><strong>Tip təhlükəsizliyi tamdır:</strong>
      <code>npx tsc --noEmit</code> heç bir xəta vermir.</li>
  <li><strong>Modul qrafı düzgündür:</strong> 6 modul
      <code>app.module.ts</code>-də qeydiyyatdan keçib.</li>
  <li><strong>9 endpoint işləyir</strong> — 3-ü açıq, 6-sı qorunur.</li>
  <li><strong>Bütün 3A faylları:</strong> <code>src/auth/</code>
      altında 12 fayl, <code>skriptler/</code> altında köməkçi
      skriptlər.</li>
</ul>

<p><strong>Bazaya təsir:</strong> real 4 istifadəçi
(<code>admin@</code>, <code>muhendis@</code>, <code>maliyyeci@</code>,
<code>baxici@arti.edu.az</code>) <em>toxunulmaz</em> qaldı və test
istifadəçiləri <strong>tamamilə silindi</strong>. Bu,
<code>trap temizle EXIT INT TERM</code> sətrinin bəhrəsidir.</p>

<p><strong>Növbəti dərs (3B) nə olacaq:</strong></p>
<ul>
  <li><strong>Refresh token</strong> — qısa ömürlü access token +
      uzun ömürlü refresh token. İstifadəçi tez-tez giriş etməz,
      amma token oğurlansa ziyan az olar.</li>
  <li><strong><code>httpOnly</code> cookie</strong> — tokeni
      JavaScript-dən gizlətmək (XSS müdafiəsi).</li>
  <li><strong>Parol sıfırlama</strong> — e-poçtla bərpa axını.</li>
  <li><strong>Qlobal <code>APP_GUARD</code></strong> — köhnə 40 test
      token almağa öyrədildikdən <em>sonra</em>.</li>
  <li><strong>Audit inteqrasiyası</strong> — kim, nə vaxt, nə etdi
      (2B-də yazdığımız audit cədvəli ilə birləşdirmə).</li>
  <li><strong>Rate limiting</strong> — brute-force hücumlarına qarşı
      (<code>@nestjs/throttler</code>).</li>
</ul>
<p>İndi <code>bash testler/yoxla.sh IIIA</code> ilə bu dərsin
10 testini işlədə bilərsiniz.</p>
""",
})
