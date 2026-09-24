/**
 * skriptler/elaqeler_yoxla.ts — əlaqə sorğularını ÖLÇÜR.
 *
 * Bu skriptin xüsusiyyəti: Prisma-nın `query` loqunu dinləyir və
 * HƏQİQİ SQL sorğularının sayını sayır. «N+1 problemi» ifadəsini
 * oxumaq bir şeydir, rəqəmi görmək tamam başqa.
 *
 * İSTİFADƏ:  npx tsx skriptler/elaqeler_yoxla.ts
 */
import 'reflect-metadata';
import 'dotenv/config';

import { PrismaPg } from '@prisma/adapter-pg';
import { PrismaClient } from '../src/generated/prisma/client.js';
import type { PrismaService } from '../src/prisma/prisma.service.js';
import { ElaqelerService } from '../src/emekdaslar/elaqeler/elaqeler.service.js';

const ID = 6; // Tariyel Talıbov — ən çox əlaqəsi olan əməkdaş

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
  sert ? ok(ad, e) : xet(ad, e);
}

void (async () => {
  // Sorğu sayğacı olan ayrıca Prisma klienti
  const saygar = new PrismaClient({
    adapter: new PrismaPg({ connectionString: process.env.DATABASE_URL! }),
    log: [{ emit: 'event', level: 'query' }],
  });
  const sorgular: string[] = [];
  (saygar as unknown as { $on: (e: string, f: (x: { query: string }) => void) => void })
    .$on('query', (e) => sorgular.push(e.query.replace(/\s+/g, ' ')));

  const xidmet = new ElaqelerService(saygar as unknown as PrismaService);

  try {
    const movcud = await saygar.emekdaslar.findUnique({
      where: { id: BigInt(ID) },
      select: { soyad: true, ad: true, ata_adi: true, vezife_id: true },
    });
    console.log(`════════ ƏLAQƏLƏR: ID ${ID} — ${movcud?.soyad} ${movcud?.ad} ════════`);

    // ── 1. İcmal — YALNIZ saylar, BİR sorğu ───────────────────────
    basliq('1) icmal() — saylar, `_count` ilə');
    sorgular.length = 0;
    const icmal = await xidmet.icmal(ID);
    const icmalSorgu = sorgular.length;
    console.log(`      tam_ad     : ${icmal.tam_ad}`);
    console.log(`      saylar     : ${JSON.stringify(icmal.saylar)}`);
    console.log(`      cem əlaqə  : ${icmal.cem_elaqe}`);
    console.log(`      SORĞU SAYI : ${icmalSorgu}`);
    sorgular.forEach((q, i) => console.log(`        ${i + 1}) ${q.slice(0, 110)}…`));
    gozle('BİR sorğu ilə bütün saylar', icmalSorgu === 1, `${icmalSorgu} sorğu`);
    gozle('doktorant sayı = 4', icmal.saylar.doktorantlar === 4, String(icmal.saylar.doktorantlar));
    gozle('cem_elaqe hesablanıb',
      icmal.cem_elaqe === Object.values(icmal.saylar).reduce((a, b) => a + b, 0));

    // ── 2. Hamısı paralel ─────────────────────────────────────────
    basliq('2) hamisi() — altı əlaqə PARALEL (Promise.all)');
    sorgular.length = 0;
    const tam = await xidmet.hamisi(ID);
    const hamisiSorgu = sorgular.length;
    console.log(`      doktorantlar   : ${tam.doktorantlar.length}`);
    console.log(`      sertifikatlar  : ${tam.sertifikatlar.length}`);
    console.log(`      mezuniyyetler  : ${tam.mezuniyyetler.length}`);
    console.log(`      tecrube        : ${tam.tecrube.length}`);
    console.log(`      layiheler      : ${tam.layiheler.length}`);
    console.log(`      shura üzvlüyü  : ${tam.shura_uzvleri.length}`);
    console.log(`      çəkmə vaxtı    : ${tam.cekme_ms} ms`);
    console.log(`      SORĞU SAYI     : ${hamisiSorgu}`);
    console.log('      izahı: 1 (mövcudluq yoxlaması) + 6 (əlaqə) + 5 (iç-içə əlaqə)');
    gozle('saylar icmal() ilə üst-üstə düşür',
      tam.doktorantlar.length === icmal.saylar.doktorantlar &&
      tam.sertifikatlar.length === icmal.saylar.sertifikatlar &&
      tam.mezuniyyetler.length === icmal.saylar.mezuniyyetler &&
      tam.tecrube.length === icmal.saylar.tecrube &&
      tam.layiheler.length === icmal.saylar.layiheler &&
      tam.shura_uzvleri.length === icmal.saylar.shura_uzvleri);

    // ── 2b. Eyni nəticə, bir findUnique ilə ───────────────────────
    basliq('2b) birSorquda() — altı əlaqə bir findUnique içində');
    sorgular.length = 0;
    const bir = await xidmet.birSorquda(ID);
    const birSorgu = sorgular.length;
    console.log(`      nəticə: doktorantlar=${bir.doktorantlar.length}  layiheler=${bir.layiheler.length}  şura=${bir.shura_uzvleri.length}`);
    console.log(`      SORĞU SAYI: ${birSorgu}`);
    gozle('nəticə hamisi() ilə EYNİDİR',
      bir.doktorantlar.length === tam.doktorantlar.length &&
      bir.shura_uzvleri.length === tam.shura_uzvleri.length &&
      bir.tam_ad === tam.tam_ad);
    gozle('İKİ ÜSUL eyni sayda sorğu göndərir',
      hamisiSorgu === birSorgu,
      `${hamisiSorgu} = ${birSorgu} → sorğu sayını KOD ÜSLUBU yox, PRISMA STRATEGİYASI müəyyən edir`);
    gozle('icmal() qat-qat az sorğu işlədir',
      icmalSorgu < hamisiSorgu,
      `${icmalSorgu} < ${hamisiSorgu} → yalnız SAY lazımdırsa _count işlədin`);

    // ── 3. Ardıcıl vs paralel ─────────────────────────────────────
    basliq('3) Ardıcıl vs PARALEL — vaxt fərqi');
    console.log('      ⚠️ 14 sətirlik bazada fərq ÖLÇÜLMƏZ dərəcədə kiçikdir.');

    /**
     * ⚠️ TƏK ÖLÇMƏ ETİBARLI DEYİL!
     * Birinci sorğu həmişə yavaş olur (bağlantı, keş). Bir dəfə ölçüb
     * müqayisə etsək, nəticə TƏSADÜFİ olar — 6 ms vs 7 ms.
     * Ona görə 5 dəfə ölçüb ƏN YAXŞI (minimum) nəticəni götürürük.
     */
    async function olc(f: () => Promise<unknown>): Promise<number> {
      let en = Number.POSITIVE_INFINITY;
      for (let i = 0; i < 5; i += 1) {
        const t = Date.now();
        await f();
        en = Math.min(en, Date.now() - t);
      }
      return en;
    }

    const ardicillik = await olc(async () => {
      await xidmet.doktorantlar(ID);
      await xidmet.sertifikatlar(ID);
      await xidmet.mezuniyyetler(ID);
      await xidmet.tecrube(ID);
      await xidmet.layiheler(ID);
      await xidmet.shura(ID);
    });

    const paralel = await olc(() =>
      Promise.all([
        xidmet.doktorantlar(ID), xidmet.sertifikatlar(ID),
        xidmet.mezuniyyetler(ID), xidmet.tecrube(ID),
        xidmet.layiheler(ID), xidmet.shura(ID),
      ]));

    const suret = ardicillik > 0 ? (ardicillik / Math.max(paralel, 1)).toFixed(1) : '—';
    console.log(`      ardıcıl (await, await, …) : ${ardicillik} ms  (5 ölçmənin ən yaxşısı)`);
    console.log(`      paralel  (Promise.all)    : ${paralel} ms  (5 ölçmənin ən yaxşısı)`);
    console.log(`      sürət qazancı             : ${suret}×`);
    console.log('      ⚠️ Fərq real olaraq 10 000+ sətirdə və uzaq bazada görünür.');
    gozle('paralel ardıcıldan ƏHƏMİYYƏTLİ DƏRƏCƏDƏ pis deyil',
      paralel <= ardicillik * 2 + 10,
      `${ardicillik} vs ${paralel} ms (ölçmə küyünə dözümlü hədd)`);
    const ayr = await xidmet.doktorantlar(ID);
    const birg = (await xidmet.hamisi(ID)).doktorantlar;
    gozle('ayrı-ayrı və birlikdə çağırış EYNİ nəticə verir',
      ayr.length === birg.length &&
      ayr.map((d) => d.id).join(',') === birg.map((d) => d.id).join(','),
      `${ayr.length} doktorant`);

    // ── 4. Nəticələrin içi ────────────────────────────────────────
    basliq('4) Nəticələrin içi (mapper düzgün işləyir)');
    tam.doktorantlar.slice(0, 3).forEach((d) =>
      console.log(`      doktorant : ${d.ad_soyad} | ${d.status} | qəbul: ${d.qebul_tarixi} | ${d.proqram}`));
    tam.mezuniyyetler.forEach((m) =>
      console.log(`      məzuniyyət: ${m.mezuniyyet_tipi} | ${m.baslama_tarixi} → ${m.bitme_tarixi} | ${m.gun_sayi} gün`));
    tam.sertifikatlar.forEach((s) =>
      console.log(`      sertifikat: ${s.tip} | bal=${s.bal} | ${s.netice}`));
    tam.shura_uzvleri.forEach((s) =>
      console.log(`      şura      : ${s.ad_soyad} | ${s.vezife} | ${s.elmi_derece} | ${s.status}`));

    const dok = tam.doktorantlar[0];
    gozle('doktorantın tarixi YYYY-MM-DD-dir',
      dok === undefined || (dok.qebul_tarixi === null || dok.qebul_tarixi.length === 10));
    const mez = tam.mezuniyyetler[0];
    gozle('məzuniyyətin gün sayı tam ədəddir',
      mez === undefined || mez.gun_sayi === null || Number.isInteger(mez.gun_sayi));

    // ── 5. Baza funksiyası ────────────────────────────────────────
    basliq('5) bazaTamAd() — PL/pgSQL funksiyası ilə tam ad');
    const b = await xidmet.bazaTamAd(ID);
    console.log(`      TypeScript tərəfdə : ${tam.tam_ad}`);
    console.log(`      SQL funksiyası     : ${b.tam_ad}`);
    gozle('hər iki üsul EYNİ nəticə verir', b.tam_ad === tam.tam_ad,
      `${b.tam_ad}`);

    // ── 6. Xəta halları ───────────────────────────────────────────
    basliq('6) Mövcud olmayan ID');
    for (const metod of ['icmal', 'doktorantlar', 'hamisi'] as const) {
      try {
        await xidmet[metod](999999);
        xet(`${metod}(999999) xəta vermədi`);
      } catch (e) {
        gozle(`${metod}(999999) → ${(e as Error).constructor.name}`,
          (e as Error).constructor.name === 'NotFoundException');
      }
    }

    // ── 7. Boş əlaqə = boş massiv, null yox ───────────────────────
    basliq('7) Əlaqəsi OLMAYAN əməkdaş');
    const bos = await xidmet.hamisi(2);
    console.log(`      ID 2 — ${bos.tam_ad}`);
    console.log(`      doktorantlar: ${JSON.stringify(bos.doktorantlar)}`);
    console.log(`      sertifikatlar: ${JSON.stringify(bos.sertifikatlar)}`);
    gozle('boş əlaqə BOŞ MASSİV qaytarır (null yox)', Array.isArray(bos.doktorantlar));
    gozle('massiv boşdur', bos.doktorantlar.length === 0);
  } finally {
    await saygar.$disconnect();
  }

  console.log('\n════════ NƏTİCƏ ════════');
  console.log(`  keçdi: ${kecdi}   uğursuz: ${xeta}`);
  if (xeta === 0) {
    console.log('  ✓ ƏLAQƏ SORĞULARI DÜZGÜN İŞLƏYİR');
    process.exit(0);
  }
  console.log(`  ✗ ${xeta} YOXLAMA UĞURSUZ`);
  process.exit(1);
})();
