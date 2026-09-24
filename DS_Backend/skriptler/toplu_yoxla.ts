/**
 * skriptler/toplu_yoxla.ts — toplu əməliyyatları CANLI yoxlayır.
 *
 * ⚠️ TƏHLÜKƏSİZLİK: skript YALNIZ özü yaratdığı sətirlərə toxunur.
 * Mövcud 14 əməkdaşın maaşı, aktivliyi DƏYİŞMİR.
 *
 * İSTİFADƏ:  npx tsx skriptler/toplu_yoxla.ts
 */
import 'reflect-metadata';
import 'dotenv/config';

import { PrismaPg } from '@prisma/adapter-pg';
import { PrismaClient } from '../src/generated/prisma/client.js';
import type { PrismaService } from '../src/prisma/prisma.service.js';
import { TopluService } from '../src/emekdaslar/toplu/toplu.service.js';

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
  const prisma = new PrismaClient({
    adapter: new PrismaPg({ connectionString: process.env.DATABASE_URL! }),
    log: [{ emit: 'event', level: 'query' }],
  });
  const sorgular: string[] = [];
  (prisma as unknown as { $on: (e: string, f: (x: { query: string }) => void) => void })
    .$on('query', (e) => sorgular.push(e.query.replace(/\s+/g, ' ')));

  const xidmet = new TopluService(prisma as unknown as PrismaService);
  const setir = (ad: string, soyad: string, ep: string, maas: number) => ({
    ad, soyad, ata_adi: 'Sistem', cinsiyyet_id: 1, vezife_id: 6,
    merkez_id: 1, email: ep, maas,
  });

  const EPOX = Date.now();
  const P = `toplu.${EPOX}`;
  const yaradilanIdler: number[] = [];

  try {
    const EVVEL = await prisma.emekdaslar.count();
    console.log(`════════ TOPLU ƏMƏLİYYATLAR (bazada ${EVVEL} əməkdaş) ════════`);

    // ── 1. Toplu yaratma ──────────────────────────────────────────
    basliq('1) topluYarat() — 3 sətir BİR sorğuda');
    sorgular.length = 0;
    const r1 = await xidmet.topluYarat({
      emekdaslar: [
        setir('Toplu1', 'Test', `${P}a@arti.edu.az`, 1000),
        setir('Toplu2', 'Test', `${P}b@arti.edu.az`, 2000),
        setir('Toplu3', 'Test', `${P}c@arti.edu.az`, 3000),
      ],
    });
    const sorguSayi = sorgular.length;
    console.log(`      göndərilən: ${r1.gonderilen}  yaradılan: ${r1.yaradilan}  atlanan: ${r1.atlanan}`);
    console.log(`      ID-lər    : ${r1.idler.join(', ')}`);
    console.log(`      SORĞU SAYI: ${sorguSayi}`);
    console.log('      izahı     : 1 × INSERT ... VALUES (…),(…),(…) + 1 × SELECT geri qaytarma');
    r1.idler.forEach((i) => yaradilanIdler.push(Number(i)));

    gozle('3 sətir yaradıldı', r1.yaradilan === 3);
    gozle('atlanan yoxdur', r1.atlanan === 0);
    gozle('ID-lər MƏTN kimi qaytarıldı (BigInt deyil)',
      r1.idler.every((i) => typeof i === 'string'));
    gozle('sorğu sayı 3-dən çox deyil', sorguSayi <= 3, `${sorguSayi} sorğu`);

    // ── 2. Təkrar → ATOMİK uğursuzluq ─────────────────────────────
    basliq('2) Təkrar e-poçt → BÜTÜN partiya ləğv olunur');
    const evvelSay = await prisma.emekdaslar.count({ where: { email: { startsWith: P } } });
    try {
      await xidmet.topluYarat({
        emekdaslar: [
          setir('Yeni', 'Test', `${P}d@arti.edu.az`, 1500),
          setir('Tekrar', 'Test', `${P}a@arti.edu.az`, 1500),
        ],
      });
      xet('təkrar e-poçt xəta vermədi');
    } catch (e) {
      const ad = (e as Error).constructor.name;
      gozle(`xəta atıldı (${ad})`, ad === 'BadRequestException');
      console.log(`      mesaj: ${(e as Error).message.slice(0, 130)}`);
    }
    const sonraSay = await prisma.emekdaslar.count({ where: { email: { startsWith: P } } });
    gozle('ATOMİKLİK: yeni sətir YAZILMADI', sonraSay === evvelSay, `${evvelSay} → ${sonraSay}`);

    // ── 3. skipDuplicates ─────────────────────────────────────────
    basliq('3) tekrarlariAtla: true — təkrar olanlar ATLANIR');
    const r3 = await xidmet.topluYarat({
      tekrarlariAtla: true,
      emekdaslar: [
        setir('Yeni4', 'Test', `${P}d@arti.edu.az`, 1500),
        setir('Tekrar', 'Test', `${P}a@arti.edu.az`, 1500),
        setir('Yeni5', 'Test', `${P}e@arti.edu.az`, 1600),
      ],
    });
    console.log(`      göndərilən: ${r3.gonderilen}  yaradılan: ${r3.yaradilan}  atlanan: ${r3.atlanan}`);
    r3.idler.forEach((i) => yaradilanIdler.push(Number(i)));
    gozle('2 sətir yaradıldı, 1 atlandı', r3.yaradilan === 2 && r3.atlanan === 1,
      `${r3.yaradilan} yaradıldı, ${r3.atlanan} atlandı`);

    // ── 4. Toplu aktivlik ─────────────────────────────────────────
    basliq('4) topluAktivlik() — updateMany');
    const r4 = await xidmet.topluAktivlik({ idler: yaradilanIdler, aktiv: false });
    console.log(`      ${r4.melumat}`);
    gozle('hamısı passiv edildi', r4.deyisen === yaradilanIdler.length,
      `${r4.deyisen} / ${yaradilanIdler.length}`);
    gozle('tapılmayan yoxdur', r4.tapilmayan === 0);

    const passiv = await prisma.emekdaslar.count({
      where: { id: { in: yaradilanIdler.map((i) => BigInt(i)) }, aktiv: false },
    });
    gozle('bazada təsdiqləndi', passiv === yaradilanIdler.length, `${passiv} sətir aktiv=false`);

    const r4b = await xidmet.topluAktivlik({ idler: yaradilanIdler, aktiv: true });
    gozle('geri aktiv edildi', r4b.deyisen === yaradilanIdler.length);

    // ── 5. Mövcud olmayan ID ──────────────────────────────────────
    basliq('5) Mövcud olmayan ID → tapilmayan sayılır');
    const r5 = await xidmet.topluAktivlik({ idler: [yaradilanIdler[0], 999999], aktiv: true });
    console.log(`      göndərilən: ${r5.gonderilen_id}  dəyişən: ${r5.deyisen}  tapılmayan: ${r5.tapilmayan}`);
    gozle('tapılmayan 1-dir', r5.tapilmayan === 1);

    // ── 6. Toplu maaş artımı ──────────────────────────────────────
    basliq('6) maasArtim() — atomik multiply');
    const idlerB = yaradilanIdler.map((i) => BigInt(i));
    const oxu = () => prisma.emekdaslar.findMany({
      where: { id: { in: idlerB } },
      select: { id: true, maas: true }, orderBy: { id: 'asc' },
    });

    const evvel = await oxu();
    console.log('      başlanğıc :', evvel.map((x) => String(x.maas)).join(', '));

    const r6 = await xidmet.maasArtim({ faiz: 10, idler: yaradilanIdler });
    console.log(`      ${r6.melumat}  (dəyişən: ${r6.deyisen})`);
    gozle(`hamısı dəyişdi (${yaradilanIdler.length} sətir)`,
      r6.deyisen === yaradilanIdler.length, String(r6.deyisen));

    const artmis = await oxu();
    console.log('      +10%      :', artmis.map((x) => String(x.maas)).join(', '));
    gozle('hər maaş TAM 10% artdı',
      evvel.every((e, i) => Math.abs(Number(artmis[i].maas) - Number(e.maas) * 1.1) < 0.01));

    // ── 6a. DÜZGÜN geri qaytarma: BÖLMƏK lazımdır ─────────────────
    basliq('6a) Düzgün geri qaytarma — ÷1.1 (×0.9 YOX)');
    await prisma.emekdaslar.updateMany({
      where: { id: { in: idlerB } },
      data: { maas: { divide: 1.1 } },
    });
    const duz = await oxu();
    console.log('      ÷1.1      :', duz.map((x) => String(x.maas)).join(', '));
    gozle('əvvəlki vəziyyət TAM bərpa olundu',
      evvel.every((e, i) => Math.abs(Number(duz[i].maas) - Number(e.maas)) < 0.01));

    // ── 6b. FAİZ TƏLƏSİ: +10% sonra -10% geri qaytarmır ──────────
    basliq('6b) FAİZ TƏLƏSİ — +10% sonra -10% geri qaytarmır');
    await xidmet.maasArtim({ faiz: 10, idler: yaradilanIdler });
    await xidmet.maasArtim({ faiz: -10, idler: yaradilanIdler });
    const teleden = await oxu();
    console.log('      əvvəl     :', evvel.map((x) => String(x.maas)).join(', '));
    console.log('      +10%      :', artmis.map((x) => String(x.maas)).join(', '));
    console.log('      sonra -10%:', teleden.map((x) => String(x.maas)).join(', '));
    evvel.forEach((e, i) => {
      const a = Number(e.maas), b = Number(teleden[i].maas);
      if (Math.abs(a - b) > 0.01) {
        console.log(`        ID ${e.id}: ${a} → ${b}   (İTKİ: ${(a - b).toFixed(2)} AZN)`);
      }
    });
    const berpa = evvel.every((e, i) =>
      Math.abs(Number(teleden[i].maas) - Number(e.maas)) < 0.01);
    gozle('RİYAZİ: faiz artımı geri qaytarıla BİLMƏZ', !berpa,
      '3000 × 1.1 = 3300,  3300 × 0.9 = 2970 ≠ 3000  → 30 AZN İTKİ');

    // Əvvəlki vəziyyətə dəqiq qaytaraq (qalan testlər üçün)
    for (const e of evvel) {
      await prisma.emekdaslar.update({
        where: { id: e.id }, data: { maas: e.maas },
      });
    }
    const berpa2 = await oxu();
    gozle('dəqiq qiymət yazmaqla bərpa olundu',
      evvel.every((e, i) => Number(berpa2[i].maas) === Number(e.maas)));

    // ── 7. Filtrsiz maaş artımı QADAĞANDIR ────────────────────────
    basliq('7) Filtrsiz maaş artımı → qadağan');
    const butunEvvel = await prisma.emekdaslar.aggregate({ _sum: { maas: true } });
    try {
      await xidmet.maasArtim({ faiz: 50 } as never);
      xet('filtrsiz artım QƏBUL EDİLDİ — bu TƏHLÜKƏLİDİR!');
    } catch (e) {
      const ad = (e as Error).constructor.name;
      gozle(`rədd edildi (${ad})`, ad === 'BadRequestException');
      console.log(`      mesaj: ${(e as Error).message}`);
    }
    const butunSonra = await prisma.emekdaslar.aggregate({ _sum: { maas: true } });
    gozle('ÜMUMİ MAAŞ FONDU dəyişmədi',
      String(butunEvvel._sum.maas) === String(butunSonra._sum.maas),
      `${butunEvvel._sum.maas} = ${butunSonra._sum.maas}`);

    // ── 8. Atomikliyin sübutu ─────────────────────────────────────
    basliq('8) atomiklikYoxla() — ROLLBACK canlı sübut');
    const r8 = await xidmet.atomiklikYoxla();
    console.log(`      cəhd edilən     : ${r8.cehd_edilen} sətir`);
    console.log(`      xəta            : ${r8.xeta}`);
    console.log(`      bazada qalan    : ${r8.bazada_qalan}`);
    console.log(`      audit artımı    : ${r8.audit_artimi}`);
    console.log(`      izah            : ${r8.izah}`);
    gozle('bazada HEÇ NƏ qalmadı', r8.bazada_qalan === 0);
    gozle('audit loqu da artmadı (trigger COMMIT-də işləyir)', r8.audit_artimi === 0);
  } finally {
    // Təmizlik: yalnız BİZİM yaratdığımız sətirlər
    const silindi = await prisma.emekdaslar.deleteMany({
      where: { email: { startsWith: 'toplu.' } },
    });
    const qalan = await prisma.emekdaslar.count();
    console.log(`\n  → təmizlik: ${silindi.count} test sətri silindi, bazada ${qalan} əməkdaş`);
    await prisma.$disconnect();
  }

  console.log('\n════════ NƏTİCƏ ════════');
  console.log(`  keçdi: ${kecdi}   uğursuz: ${xeta}`);
  if (xeta === 0) {
    console.log('  ✓ TOPLU ƏMƏLİYYATLAR DÜZGÜN İŞLƏYİR');
    process.exit(0);
  }
  console.log(`  ✗ ${xeta} YOXLAMA UĞURSUZ`);
  process.exit(1);
})();
