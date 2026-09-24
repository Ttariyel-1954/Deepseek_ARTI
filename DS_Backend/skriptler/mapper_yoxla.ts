/**
 * skriptler/mapper_yoxla.ts — mapper-in nə etdiyini CANLI göstərir.
 *
 * Skript iki şeyi yan-yana qoyur:
 *   1) bazadan gələn XAM sətri JSON-a çevirməyə çalışır → XƏTA alır;
 *   2) həmin sətri `hazirla()`-dan keçirib yenidən çalışır → işləyir.
 *
 * İSTİFADƏ:  npx tsx skriptler/mapper_yoxla.ts
 */
import 'reflect-metadata';
import 'dotenv/config';

import { PrismaService } from '../src/prisma/prisma.service.js';
import {
  EMEKDAS_SECIM,
  hazirla,
  type EmekdasSetiri,
} from '../src/emekdaslar/dto/emekdas-cavab.dto.js';

void (async () => {
  const prisma = new PrismaService();
  await prisma.onModuleInit();

  try {
    const xam: EmekdasSetiri | null = await prisma.emekdaslar.findUnique({
      where: { id: 1n },
      select: EMEKDAS_SECIM,
    });

    if (!xam) throw new Error('ID 1 tapılmadı — baza boşdur?');

    console.log('════════ MAPPER: XAM SƏTİR ════════');
    console.log(`  id       tipi : ${typeof xam.id}`);
    console.log(`  id       dəyəri: ${String(xam.id)}n   ← BigInt literalı`);
    console.log(`  maas     tipi : ${typeof xam.maas}  (Prisma.Decimal obyekti)`);
    console.log(`  maas     dəyəri: ${String(xam.maas)}`);
    console.log(`  dogum_tarixi  : ${String(xam.dogum_tarixi)}  (Date obyekti)`);
    console.log(`  cinsiyyet     : ${JSON.stringify(xam.cinsiyyet)}  (əlaqə obyekti)`);

    console.log('\n── 1) XAM sətri JSON-a çeviririk ───────────────────────────');
    try {
      const n = JSON.stringify(xam);
      console.log(`  [XX] gözlənilməz: işlədi → ${n.slice(0, 80)}…`);
    } catch (x) {
      console.log(`  [OK] gözlənilən XƏTA: ${(x as Error).message}`);
      console.log('       ↑ məhz bu xəta API-də 500 qaytarır!');
    }

    console.log('\n── 2) `hazirla()`-dan keçirib yenidən çalışırıq ────────────');
    const cavab = hazirla(xam);
    console.log(`  id       tipi : ${typeof cavab.id}   dəyəri: "${cavab.id}"`);
    console.log(`  maas     tipi : ${typeof cavab.maas} dəyəri: "${cavab.maas}"`);
    console.log(`  dogum_tarixi  : "${cavab.dogum_tarixi}"  ← yalnız gün`);
    console.log(`  tam_ad        : "${cavab.tam_ad}"`);
    console.log(`  yas           : ${cavab.yas}`);
    console.log(`  vezife        : ${JSON.stringify(cavab.vezife)}  ← adı ilə`);

    const metn = JSON.stringify(cavab);
    console.log(`\n  [OK] JSON.stringify İŞLƏDİ (${metn.length} simvol)`);
    console.log(`       ${metn}`);

    console.log('\n── 3) Fərq cədvəli ─────────────────────────────────────────');
    console.log('  sahə          | xam baza        | API cavabı');
    console.log('  --------------|-----------------|------------------');
    console.log(`  id            | ${(typeof xam.id).padEnd(15)} | ${typeof cavab.id}`);
    console.log(`  maas          | ${(typeof xam.maas).padEnd(15)} | ${typeof cavab.maas}`);
    console.log(`  dogum_tarixi  | ${(typeof xam.dogum_tarixi).padEnd(15)} | ${typeof cavab.dogum_tarixi}`);
    console.log(`  cinsiyyet     | ${(typeof xam.cinsiyyet).padEnd(15)} | ${typeof cavab.cinsiyyet}`);
    console.log(`  vezife        | ${(typeof xam.vezifeler).padEnd(15)} | ${typeof cavab.vezife}`);
    console.log(`  yas           | ${'—'.padEnd(15)} | ${typeof cavab.yas}`);

    console.log('\n════════ NƏTİCƏ ════════');
    console.log('  ✓ MAPPER XAM BAZA SƏTRİNİ TƏHLÜKƏSİZ JSON-A ÇEVİRİR');
    console.log(`  ✓ cavab JSON-u: ${metn.length} simvol, BigInt yoxdur, Decimal yoxdur`);
  } finally {
    await prisma.onModuleDestroy();
  }
})();
