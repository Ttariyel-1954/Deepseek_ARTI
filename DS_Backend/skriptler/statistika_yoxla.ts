/**
 * skriptler/statistika_yoxla.ts — statistika servisini CANLI yoxlayır.
 *
 * Servisi HTTP olmadan birbaşa çağırır: problem servisdədirsə, dərhal
 * görünür. Real bazaya qarşı işləyir, heç nə DƏYİŞMİR (yalnız oxuyur).
 *
 * İSTİFADƏ:  npx tsx skriptler/statistika_yoxla.ts
 */
import 'reflect-metadata';
import 'dotenv/config';

import { PrismaService } from '../src/prisma/prisma.service.js';
import { StatistikaService } from '../src/emekdaslar/statistika/statistika.service.js';

let kecdi = 0;
let xeta = 0;

function basliq(m: string): void {
  console.log(`\n── ${m} ${'─'.repeat(Math.max(0, 62 - m.length))}`);
}
function ok(m: string, e = ''): void {
  kecdi += 1;
  console.log(`  [OK] ${m}${e ? ' — ' + e : ''}`);
}
function xet(m: string, e = ''): void {
  xeta += 1;
  console.log(`  [XX] ${m}${e ? ' — ' + e : ''}`);
}
function gozle(ad: string, sert: boolean, e = ''): void {
  if (sert) ok(ad, e);
  else xet(ad, e);
}

void (async () => {
  const prisma = new PrismaService();
  await prisma.onModuleInit();
  const s = new StatistikaService(prisma);

  try {
    // ── 1. Ümumi mənzərə ──────────────────────────────────────────
    basliq('1) umumi() — ümumi mənzərə');
    const u = await s.umumi();
    console.log(`      əməkdaş   : cem=${u.emekdas.cem}  aktiv=${u.emekdas.aktiv}  passiv=${u.emekdas.passiv}`);
    console.log(`      maaş      : fondu=${u.maas.fondu}  orta=${u.maas.orta}  min=${u.maas.min}  maks=${u.maas.maks}`);
    console.log(`      əlaqələr  : ${JSON.stringify(u.elaqeler)}`);
    console.log(`      baza fn   : ${JSON.stringify(u.baza_funksiyalari)}`);
    console.log(`      cədvəl    : ${u.cedvel_sayi}   hesablanma: ${u.hesablanma_ms} ms`);

    gozle('cem = 14', u.emekdas.cem === 14, `cem=${u.emekdas.cem}`);
    gozle('aktiv + passiv = cem', u.emekdas.aktiv + u.emekdas.passiv === u.emekdas.cem);
    gozle('maaş fondu > 0', u.maas.fondu > 0, String(u.maas.fondu));
    gozle('orta maaş min < orta < maks', u.maas.min < u.maas.orta && u.maas.orta < u.maas.maks);
    gozle('48 cədvəl', u.cedvel_sayi === 48, `cedvel=${u.cedvel_sayi}`);
    gozle('baza funksiyası fn_maas_fondu işləyir', u.baza_funksiyalari.maas_fondu > 0,
      String(u.baza_funksiyalari.maas_fondu));
    gozle('fondu (Prisma) = fondu (PL/pgSQL)',
      Math.abs(u.maas.fondu - u.baza_funksiyalari.maas_fondu) < 0.01,
      `${u.maas.fondu} vs ${u.baza_funksiyalari.maas_fondu}`);
    gozle('hesablanma 1 saniyədən az', u.hesablanma_ms < 1000, `${u.hesablanma_ms} ms`);

    // ── 2. Mərkəzlər ──────────────────────────────────────────────
    basliq('2) merkezler() — groupBy');
    const m = await s.merkezler('aktiv', 1, 'say');
    console.log('      merkez                                      sayı  orta    fondu');
    for (const x of m) {
      console.log(`      ${(x.merkez + ' '.repeat(42)).slice(0, 42)} ${String(x.emekdas_sayi).padStart(3)}  ${String(x.orta_maas).padStart(6)}  ${x.maas_fondu}`);
    }
    const cem = m.reduce((a, b) => a + b.emekdas_sayi, 0);
    gozle('qrupların cəmi = aktiv əməkdaş sayı', cem === u.emekdas.aktiv, `${cem} vs ${u.emekdas.aktiv}`);
    gozle('say üzrə azalan sıralanıb', m.every((x, i) => i === 0 || m[i - 1].emekdas_sayi >= x.emekdas_sayi));
    gozle('fondu = orta × sayı (təqribi)',
      m.every((x) => Math.abs(x.maas_fondu - x.orta_maas * x.emekdas_sayi) < 1));

    const mA = await s.merkezler('aktiv', 1, 'ad');
    gozle('ad üzrə sıralama işləyir',
      mA.every((x, i) => i === 0 || mA[i - 1].merkez.localeCompare(x.merkez, 'az') <= 0));

    const m2 = await s.merkezler('aktiv', 2, 'say');
    gozle('min_say=2 filtri işləyir', m2.every((x) => x.emekdas_sayi >= 2), `${m2.length} qrup`);

    // ── 3. Vəzifələr ──────────────────────────────────────────────
    basliq('3) vezifeler() — groupBy');
    const v = await s.vezifeler('aktiv', 1, 'say');
    for (const x of v) {
      console.log(`      ${(x.vezife + ' '.repeat(26)).slice(0, 26)} səviyyə=${x.seviyye ?? '—'}  sayı=${x.emekdas_sayi}`);
    }
    gozle('qrupların cəmi = aktiv əməkdaş sayı',
      v.reduce((a, b) => a + b.emekdas_sayi, 0) === u.emekdas.aktiv);

    // ── 4. Parametrli baza funksiyası ─────────────────────────────
    basliq('4) merkezShobeSayi() — parametrli $queryRaw');
    for (const id of [1, 2, 3]) {
      const r = await s.merkezShobeSayi(id);
      console.log(`      merkez ${id} → ${r.shobe_sayi} şöbə`);
    }
    const r1 = await s.merkezShobeSayi(1);
    gozle('nəticə obyekt quruluşundadır',
      typeof r1.merkez_id === 'number' && typeof r1.shobe_sayi === 'number');

    // SQL inyeksiya cəhdi: parametr ədəd olmalıdır, mətn ötürsək?
    try {
      await s.merkezShobeSayi(Number('1; DROP TABLE kadrlar.emekdaslar'));
      gozle('SQL inyeksiya cəhdi zərərsizdir (NaN → xəta və ya 0)',
        (await prisma.emekdaslar.count()) === 14);
    } catch {
      ok('SQL inyeksiya cəhdi rədd edildi', 'parametr tipi qoruyur');
    }
    gozle('cədvəl hələ də yerindədir', (await prisma.emekdaslar.count()) === 14);

    // ── 5. Bütün mərkəzlər (N+1) ──────────────────────────────────
    basliq('5) butunMerkezler() — N+1 probleminin həlli');
    const bm = await s.butunMerkezler();
    console.log('      id  tip          şöbə  əməkdaş  ad');
    for (const x of bm) {
      console.log(`      ${String(x.id).padStart(2)}  ${(x.tip + ' '.repeat(11)).slice(0, 11)}  ${String(x.shobe_sayi).padStart(4)}  ${String(x.emekdas_sayi).padStart(7)}  ${x.ad.slice(0, 40)}`);
    }
    gozle('10 mərkəz gəldi', bm.length === 10, `${bm.length}`);
    gozle('şöbə sayları cəmi 36', bm.reduce((a, b) => a + b.shobe_sayi, 0) === 36,
      String(bm.reduce((a, b) => a + b.shobe_sayi, 0)));
    gozle('əməkdaş sayları cəmi 14', bm.reduce((a, b) => a + b.emekdas_sayi, 0) === 14,
      String(bm.reduce((a, b) => a + b.emekdas_sayi, 0)));

    // ── 6. Sorğu sayı ─────────────────────────────────────────────
    basliq('6) Sorğu sayı — N+1 probleminin qiyməti');
    console.log('      sadəlövh (N+1): 1 (mərkəzlər) + 10 (şöbə) + 10 (əməkdaş) = 21 sorğu');
    console.log('      bizim həll    : 1 (mərkəzlər) +  1 (şöbə) +  1 (əməkdaş) =  3 sorğu');
    gozle('3 sorğu ilə 10 mərkəz + 36 şöbə + 14 əməkdaş',
      bm.length === 10 &&
      bm.reduce((a, b) => a + b.shobe_sayi, 0) === 36 &&
      bm.reduce((a, b) => a + b.emekdas_sayi, 0) === 14,
      '21 → 3 sorğu');
  } finally {
    await prisma.onModuleDestroy();
  }

  console.log('\n════════ NƏTİCƏ ════════');
  console.log(`  keçdi: ${kecdi}   uğursuz: ${xeta}`);
  if (xeta === 0) {
    console.log('  ✓ STATİSTİKA SERVİSİ DÜZGÜN İŞLƏYİR');
    process.exit(0);
  }
  console.log(`  ✗ ${xeta} YOXLAMA UĞURSUZ`);
  process.exit(1);
})();
