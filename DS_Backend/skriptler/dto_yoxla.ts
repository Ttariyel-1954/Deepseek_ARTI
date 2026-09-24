/**
 * skriptler/dto_yoxla.ts — DTO-ların REAL validasiya matrisi.
 *
 * Bu skript `main.ts`-dəki EYNI `ValidationPipe`-ı işlədir:
 *   new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true })
 * Yəni burada gördüyünüz nəticə — canlı API-nin verəcəyi nəticədir.
 *
 * İSTİFADƏ:  npx tsx skriptler/dto_yoxla.ts
 */
import 'reflect-metadata';

import { ValidationPipe } from '@nestjs/common';
import { EmekdasYaratDto } from '../src/emekdaslar/dto/emekdas-yarat.dto.js';
import { EmekdasYenileDto } from '../src/emekdaslar/dto/emekdas-yenile.dto.js';
import { EmekdasSorguDto } from '../src/emekdaslar/dto/emekdas-sorgu.dto.js';

const boru = new ValidationPipe({
  whitelist: true,
  forbidNonWhitelisted: true,
  transform: true,
});

let kecdi = 0;
let xeta = 0;

/** Bir gövdəni DTO-dan keçirir və nəticəni çap edir */
async function cehd(
  ad: string,
  metatype: new () => object,
  govde: unknown,
  tip: 'body' | 'query',
  gozle: 'ok' | 'xeta',
): Promise<void> {
  try {
    const netice = await boru.transform(govde, { type: tip, metatype });
    const qisa = JSON.stringify(netice);
    if (gozle === 'ok') {
      kecdi += 1;
      console.log(`  [OK]  ${ad}`);
      console.log(`        → ${qisa.length > 160 ? qisa.slice(0, 160) + '…' : qisa}`);
    } else {
      xeta += 1;
      console.log(`  [XX]  ${ad} — QƏBUL EDİLDİ, halbuki RƏDD edilməli idi`);
      console.log(`        → ${qisa}`);
    }
  } catch (x) {
    const govde2 = (x as { getResponse?: () => unknown }).getResponse?.() as
      | { message?: string[] }
      | undefined;
    const mesajlar = govde2?.message ?? [(x as Error).message];

    if (gozle === 'xeta') {
      kecdi += 1;
      console.log(`  [OK]  ${ad} — RƏDD EDİLDİ`);
      (Array.isArray(mesajlar) ? mesajlar : [mesajlar])
        .slice(0, 3)
        .forEach((m) => console.log(`        · ${m}`));
    } else {
      xeta += 1;
      console.log(`  [XX]  ${ad} — RƏDD EDİLDİ, halbuki QƏBUL edilməli idi`);
      (Array.isArray(mesajlar) ? mesajlar : [mesajlar]).forEach((m) => console.log(`        · ${m}`));
    }
  }
}

const DUZ =
  '{"ad":"Kamran","soyad":"Məmmədli","ata_adi":"Vaqif","cinsiyyet_id":1,' +
  '"vezife_id":6,"merkez_id":1,"email":"kamran@arti.edu.az","maas":2200.5}';

void (async () => {
  console.log('════════ DTO VAHİD VALİDASİYA MATRİSİ ════════');

  console.log('\n── 1) POST gövdəsi (EmekdasYaratDto) ──────────────────────');
  await cehd('düzgün tam gövdə', EmekdasYaratDto, JSON.parse(DUZ), 'body', 'ok');
  await cehd('mətn rəqəmi özü ədədə çevirir', EmekdasYaratDto,
    { ad: 'Ali', soyad: 'Vəliyev', ata_adi: 'Vaqif', cinsiyyet_id: '2', vezife_id: '5' },
    'body', 'ok');
  await cehd('çatışmayan mütləq sahələr', EmekdasYaratDto, {}, 'body', 'xeta');
  await cehd('ad çox qısadır', EmekdasYaratDto,
    { ad: 'A', soyad: 'Vəliyev', ata_adi: 'Vaqif', cinsiyyet_id: 1, vezife_id: 6 },
    'body', 'xeta');
  await cehd('cinsiyyet_id 99 (DTO həddindən kənar)', EmekdasYaratDto,
    { ad: 'Ali', soyad: 'Vəliyev', ata_adi: 'Vaqif', cinsiyyet_id: 99, vezife_id: 6 },
    'body', 'xeta');
  await cehd('email səhv formatdadır', EmekdasYaratDto,
    { ad: 'Ali', soyad: 'Vəliyev', ata_adi: 'Vaqif', cinsiyyet_id: 1, vezife_id: 6, email: 'ali@' },
    'body', 'xeta');
  await cehd('tarix səhv formatdadır', EmekdasYaratDto,
    { ad: 'Ali', soyad: 'Vəliyev', ata_adi: 'Vaqif', cinsiyyet_id: 1, vezife_id: 6,
      dogum_tarixi: '12.05.1990' },
    'body', 'xeta');
  await cehd('maaş mənfidir', EmekdasYaratDto,
    { ad: 'Ali', soyad: 'Vəliyev', ata_adi: 'Vaqif', cinsiyyet_id: 1, vezife_id: 6, maas: -5 },
    'body', 'xeta');
  await cehd('maaşda 3 onluq rəqəm', EmekdasYaratDto,
    { ad: 'Ali', soyad: 'Vəliyev', ata_adi: 'Vaqif', cinsiyyet_id: 1, vezife_id: 6, maas: 10.555 },
    'body', 'xeta');
  await cehd('gövdədə YAD sahə (yoluxucu)', EmekdasYaratDto,
    { ad: 'Ali', soyad: 'Vəliyev', ata_adi: 'Vaqif', cinsiyyet_id: 1, vezife_id: 6, yoluxucu: true },
    'body', 'xeta');

  console.log('\n── 2) PATCH gövdəsi (EmekdasYenileDto) ────────────────────');
  await cehd('boş gövdə QƏBUL EDİLİR (yoxlama servisdədir)', EmekdasYenileDto, {}, 'body', 'ok');
  await cehd('yalnız bir sahə', EmekdasYenileDto, { maas: 3000 }, 'body', 'ok');
  await cehd('iki sahə', EmekdasYenileDto, { vezife_id: 4, aktiv: false }, 'body', 'ok');
  await cehd('səhv tip (mətn ədəd yerinə)', EmekdasYenileDto, { maas: 'çox' }, 'body', 'xeta');
  await cehd('ad çox qısadır', EmekdasYenileDto, { ad: 'A' }, 'body', 'xeta');

  console.log('\n── 3) GET sorğusu (EmekdasSorguDto) ───────────────────────');
  await cehd('parametrsiz', EmekdasSorguDto, {}, 'query', 'ok');
  await cehd('mətn rəqəmə çevrilir', EmekdasSorguDto, { limit: '5', seife: '2' }, 'query', 'ok');
  await cehd('limit = 0', EmekdasSorguDto, { limit: '0' }, 'query', 'xeta');
  await cehd('limit = 500', EmekdasSorguDto, { limit: '500' }, 'query', 'xeta');
  await cehd('limit ədəd deyil', EmekdasSorguDto, { limit: 'abc' }, 'query', 'xeta');
  await cehd('axtar çox uzundur', EmekdasSorguDto, { axtar: 'x'.repeat(60) }, 'query', 'xeta');
  await cehd('aktiv səhv dəyər', EmekdasSorguDto, { aktiv: 'yox' }, 'query', 'xeta');
  await cehd('siralama icazəsiz sütun', EmekdasSorguDto, { siralama: 'parol' }, 'query', 'xeta');
  await cehd('tertib səhv dəyər', EmekdasSorguDto, { tertib: 'yuxari' }, 'query', 'xeta');
  await cehd('yad parametr', EmekdasSorguDto, { yoluxucu: '1' }, 'query', 'xeta');

  console.log('\n════════ NƏTİCƏ ════════');
  console.log(`  keçdi: ${kecdi}   uğursuz: ${xeta}`);
  if (xeta === 0) {
    console.log('  ✓ BÜTÜN VALİDASİYA QAYDALARI GÖZLƏNİLDİYİ KİMİ İŞLƏYİR');
    process.exit(0);
  }
  console.log(`  ✗ ${xeta} YOXLAMA UĞURSUZ`);
  process.exit(1);
})();
