/**
 * skriptler/servis_yoxla.ts — SERVİS səviyyəsində yoxlama.
 *
 * NİYƏ LAZIMDIR? HTTP endpoint-i işləmirsə, səbəb iki yerdə ola bilər:
 * controller-də, ya da servisdə. Bu skript controller-i TAMAMİLƏ
 * kənarlaşdırır — servisi birbaşa çağırır. Beləliklə problem servisdədirsə,
 * dərhal görünür.
 *
 * ⚠️ TƏHLÜKƏSİZLİK: skript mövcud 14 əməkdaşa HEÇ BİR ZƏRƏR VERMİR:
 *   • Yeni sətirləri özü yaradır və sonda silir.
 *   • ID 1-i silməyə cəhd edir, AMMA `$transaction` içində və
 *     `throw` ilə — nəticə heç vaxt commit olunmur.
 *
 * İSTİFADƏ:
 *   npx tsx skriptler/servis_yoxla.ts
 */
import 'reflect-metadata';
import 'dotenv/config';

import { Prisma } from '../src/generated/prisma/client.js';
import { PrismaService } from '../src/prisma/prisma.service.js';
import { EmekdaslarService } from '../src/emekdaslar/emekdaslar.service.js';
import { EmekdasSorguDto } from '../src/emekdaslar/dto/emekdas-sorgu.dto.js';

let kecdi = 0;
let xeta = 0;

function basliq(m: string): void {
  const xett = '─'.repeat(Math.max(0, 62 - m.length));
  console.log(`\n── ${m} ${xett}`);
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
  const xidmet = new EmekdaslarService(prisma);

  const temizlik: string[] = [];

  try {
    // ── 1. hamisi() ────────────────────────────────────────────────
    basliq('1) hamisi() — səhifələmə və mapper');

    const s1 = await xidmet.hamisi(
      Object.assign(new EmekdasSorguDto(), { limit: 3, seife: 1, siralama: 'soyad' }),
    );
    console.log(`      cem=${s1.cem} · sehife=${s1.sehife}/${s1.sehife_sayi} · gosterilen=${s1.melumat.length}`);
    gozle('cem = 14', s1.cem === 14, `cem=${s1.cem}`);
    gozle('bir səhifədə 3 sətir', s1.melumat.length === 3);
    gozle('id MƏTN tipindədir (BigInt yox)', typeof s1.melumat[0].id === 'string', typeof s1.melumat[0].id);
    gozle('maas MƏTN tipindədir (Decimal yox)', typeof s1.melumat[0].maas === 'string', typeof s1.melumat[0].maas);
    gozle('tam_ad hesablanıb', s1.melumat[0].tam_ad.length > 5, s1.melumat[0].tam_ad);
    console.log('      JSON (ilk sətir):');
    console.log('      ' + JSON.stringify(s1.melumat[0]));
    console.log('      ↑ mapper-dən sonra JSON.stringify İŞLƏYİR');

    // ── 1. biri() ──────────────────────────────────────────────────
    basliq('2) biri() — bir əməkdaş');

    const e1 = await xidmet.biri(1);
    ok('ID 1 oxundu', `${e1.tam_ad} · ${e1.vezife?.ad} · ${e1.maas} AZN`);
    gozle('yaş hesablanıb', typeof e1.yas === 'number' && e1.yas! > 0, `${e1.yas} yaş`);
    gozle('əlaqələr obyekt kimi gəlib', e1.vezife !== null && typeof e1.vezife.ad === 'string');

    // ── 1. Tapılmayan ──────────────────────────────────────────────
    basliq('3) biri() — mövcud olmayan ID');

    try {
      await xidmet.biri(999999);
      xet('biri(999999) xəta vermədi');
    } catch (x) {
      const ad = (x as Error).constructor.name;
      gozle('NotFoundException atıldı', ad === 'NotFoundException', ad);
      console.log(`      mesaj: ${(x as Error).message}`);
    }

    // ── 1. yarat() ─────────────────────────────────────────────────
    basliq('4) yarat() — yeni əməkdaş');

    const epost = `servis.test.${Date.now()}@arti.edu.az`;
    const yeni = await xidmet.yarat({
      ad: 'Servis',
      soyad: 'Yoxlaması',
      ata_adi: 'Avtomatik',
      cinsiyyet_id: 1,
      vezife_id: 6,
      merkez_id: 1,
      email: epost,
      ise_baslama: '2026-02-01',
      maas: 1500.5,
    });
    temizlik.push(yeni.id);
    ok('yeni əməkdaş yaradıldı', `ID ${yeni.id} · ${yeni.tam_ad}`);
    gozle('ID mətn kimi qaytarıldı', typeof yeni.id === 'string');
    gozle('maaş düzgün formatdadır', yeni.maas === '1500.50', String(yeni.maas));
    gozle('tarix YYYY-MM-DD formatındadır', yeni.ise_baslama === '2026-02-01', String(yeni.ise_baslama));
    gozle('standart status verildi', yeni.is_statusu?.id === 1, String(yeni.is_statusu?.ad));

    // ── 1. yenile() ────────────────────────────────────────────────
    basliq('5) yenile() — qismən dəyişiklik');

    const deyismis = await xidmet.yenile(Number(yeni.id), { vezife_id: 4, maas: 2750 });
    ok('yeniləndi', `${deyismis.vezife?.ad} · ${deyismis.maas}`);
    gozle('vezife dəyişdi', deyismis.vezife?.id === 4);
    gozle('maaş dəyişdi', deyismis.maas === '2750.00', String(deyismis.maas));
    gozle('ad DƏYİŞMƏDİ', deyismis.ad === 'Servis');

    try {
      await xidmet.yenile(Number(yeni.id), {});
      xet('boş gövdə qəbul edildi');
    } catch (x) {
      gozle('boş gövdə rədd edildi', (x as Error).constructor.name === 'BadRequestException');
    }

    // ── 1. sil() — ADİ silmə ───────────────────────────────────────
    basliq('6) sil() — asılı qeyd YOXDURSA adi silmə');

    const s7 = await xidmet.sil(Number(yeni.id));
    temizlik.length = 0;
    gozle("növ 'hard'", s7.nov === 'hard', s7.nov);
    console.log(`      mesaj: ${s7.mesaj}`);
    gozle('sətir bazadan çıxdı', (await prisma.emekdaslar.count({ where: { id: BigInt(yeni.id) } })) === 0);

    // ── 1. sil() — YUMŞAQ silmə ────────────────────────────────────
    basliq('7) sil() — asılı qeyd VARSA yumşaq silmə');

    const ikinci = await xidmet.yarat({
      ad: 'Asılı',
      soyad: 'Testi',
      ata_adi: 'Müvəqqəti',
      cinsiyyet_id: 2,
      vezife_id: 6,
    });
    const ikinciId = Number(ikinci.id);
    temizlik.push(ikinci.id);

    const uzv = await prisma.elmi_shura_uzvleri.create({
      data: { emekdas_id: BigInt(ikinciId), ad_soyad: 'Asılı Testi Müvəqqəti' },
      select: { id: true },
    });
    ok('asılı qeyd yaradıldı', `elmi_shura_uzvleri ID ${uzv.id}`);

    const s8 = await xidmet.sil(ikinciId);
    gozle("növ 'soft'", s8.nov === 'soft', s8.nov);
    console.log(`      mesaj: ${s8.mesaj}`);
    console.log(`      asılı qeydlər: ${JSON.stringify(s8.asili_qeydler)}`);
    gozle('sətir bazada QALIR', (await prisma.emekdaslar.count({ where: { id: BigInt(ikinciId) } })) === 1);
    const passiv = await prisma.emekdaslar.findUnique({ where: { id: BigInt(ikinciId) }, select: { aktiv: true } });
    gozle('aktiv = false oldu', passiv?.aktiv === false);

    // təmizlik: əvvəl asılı qeyd, sonra əməkdaş
    await prisma.elmi_shura_uzvleri.delete({ where: { id: uzv.id } });
    await prisma.emekdaslar.delete({ where: { id: BigInt(ikinciId) } });
    temizlik.length = 0;
    ok('təmizlik edildi', 'asılı qeyd və müvəqqəti əməkdaş silindi');

    // ── 1. FK bazadan silməyə icazə verirmi? ───────────────────────
    basliq('8) ID 1-i bazadan silmək cəhdi (transaction içində)');

    try {
      await prisma.$transaction(async (tx) => {
        await tx.emekdaslar.delete({ where: { id: 1n } });
        // ⚠️ Bu sətrə ÇATSAQ da nəticə commit olunmayacaq:
        throw new Error('QƏSDƏN GERİ QAYTARMA — heç nə dəyişməməlidir');
      });
      xet('transaction gözlənilmədən uğurlu oldu');
    } catch (x) {
      const kod = x instanceof Prisma.PrismaClientKnownRequestError ? x.code : '?';
      gozle('baza silməyə İCAZƏ VERMƏDİ', kod === 'P2003', `Prisma kodu: ${kod}`);
      console.log(`      mesaj: ${(x as Error).message.split('\n').filter(Boolean).slice(-1)[0]}`);
    }

    const qalan = await prisma.emekdaslar.count();
    gozle('ID 1 yerindədir — heç nə silinmədi', qalan === 14, `bazada ${qalan} əməkdaş`);

    // ── 1. Axtarış ────────────────────────────────────────────────
    basliq('9) axtar() — hərf böyüklüyündən asılı olmayan axtarış');

    const a1 = await xidmet.hamisi(Object.assign(new EmekdasSorguDto(), { axtar: 'əliyev' }));
    const a2 = await xidmet.hamisi(Object.assign(new EmekdasSorguDto(), { axtar: 'ƏLİYEV' }));
    gozle('kiçik hərflə tapıldı', a1.cem === 2, `cem=${a1.cem}`);
    gozle('böyük hərflə də tapıldı', a2.cem === 2, `cem=${a2.cem}`);
    a1.melumat.forEach((e) => console.log(`      · ${e.tam_ad}`));

    // ── 11. Filtr ──────────────────────────────────────────────────
    basliq('10) filtr — merkez və aktivlik');

    const f1 = await xidmet.hamisi(Object.assign(new EmekdasSorguDto(), { merkez_id: 1 }));
    const f2 = await xidmet.hamisi(Object.assign(new EmekdasSorguDto(), { aktiv: 'passiv' }));
    const f3 = await xidmet.hamisi(Object.assign(new EmekdasSorguDto(), { aktiv: 'hamisi' }));
    ok('merkez_id=1', `${f1.cem} əməkdaş`);
    ok('aktiv=passiv', `${f2.cem} əməkdaş`);
    ok('aktiv=hamisi', `${f3.cem} əməkdaş`);
    gozle('hamisi >= aktiv', f3.cem >= f1.cem);
  } finally {
    // Nə olursa olsun, müvəqqəti sətirləri təmizlə
    for (const id of temizlik) {
      await prisma.elmi_shura_uzvleri.deleteMany({ where: { emekdas_id: BigInt(id) } });
      await prisma.emekdaslar.deleteMany({ where: { id: BigInt(id) } });
    }
    await prisma.onModuleDestroy();
  }

  console.log('\n════════ NƏTİCƏ ════════');
  console.log(`  keçdi: ${kecdi}   uğursuz: ${xeta}`);
  if (xeta === 0) {
    console.log('  ✓ SERVİSİN BÜTÜN ƏMƏLİYYATLARI DÜZGÜN İŞLƏYİR');
    process.exit(0);
  }
  console.log(`  ✗ ${xeta} YOXLAMA UĞURSUZ`);
  process.exit(1);
})();
