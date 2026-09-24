import { BadRequestException, Injectable, Logger } from '@nestjs/common';
import { Prisma } from '../../generated/prisma/client.js';
import { PrismaService } from '../../prisma/prisma.service.js';
import { TopluYaratDto } from './dto/toplu.dto.js';
import { TopluAktivlikDto } from './dto/toplu.dto.js';
import { MaasArtimDto } from './dto/toplu.dto.js';

export interface TopluYaratCavabi {
  ugur: true;
  gonderilen: number;
  yaradilan: number;
  atlanan: number;
  idler: string[];
  cedvel_adi: string;
}

export interface TopluDeyisiklikCavabi {
  ugur: true;
  gonderilen_id: number;
  deyisen: number;
  tapilmayan: number;
  melumat: string;
}

export interface AtomiklikCavabi {
  ugur: true;
  cehd_edilen: number;
  xeta: string;
  bazada_qalan: number;
  audit_artimi: number;
  izah: string;
}

@Injectable()
export class TopluService {
  private readonly log = new Logger('TOPLU');

  constructor(private readonly prisma: PrismaService) {}

  // ── 1. Toplu yaratma ────────────────────────────────────────────
  /**
   * ⚠️ `createMany` və `createManyAndReturn` BİR SQL sorğusudur
   * (`INSERT ... VALUES (...), (...), ...`).
   *
   * Üstünlükləri:
   *   • 50 əməkdaş = 1 sorğu (50 yerinə).
   *   • ATOMİKDİR: biri uğursuz olsa, HEÇ BİRİ yazılmır.
   *
   * Çatışmazlıqları:
   *   • Prisma-nın `@default(now())` kimi <em>tətbiq</em> səviyyəli
   *     dəyərləri işləmir — yalnız BAZA səviyyəli DEFAULT-lar işləyir
   *     (bizdə elə belədir).
   *   • Yaratma qarmaqları (`hooks`) çağırılmır. AMMA baza TRIGGER-ləri
   *     işləyir — audit qeydləri yenə yazılır.
   */
  async topluYarat(dto: TopluYaratDto): Promise<TopluYaratCavabi> {
    const data: Prisma.emekdaslarUncheckedCreateInput[] = dto.emekdaslar.map((e) => ({
      ad: e.ad.trim(),
      soyad: e.soyad.trim(),
      ata_adi: e.ata_adi.trim(),
      cinsiyyet_id: e.cinsiyyet_id,
      vezife_id: e.vezife_id,
      is_status_id: e.is_status_id ?? 1,
      aktiv: e.aktiv ?? true,
      email: e.email ?? null,
      telefon: e.telefon ?? null,
      shobe_id: e.shobe_id ?? null,
      merkez_id: e.merkez_id ?? null,
      elmi_derece_id: e.elmi_derece_id ?? null,
      elmi_ad_id: e.elmi_ad_id ?? null,
      maas: e.maas ?? null,
      dogum_tarixi: this.gun(e.dogum_tarixi),
      ise_baslama: this.gun(e.ise_baslama),
    }));

    try {
      const setirler = await this.prisma.emekdaslar.createManyAndReturn({
        data,
        select: { id: true, ad: true, soyad: true, email: true },
        skipDuplicates: dto.tekrarlariAtla ?? false,
      });

      const idler = setirler.map((s) => String(s.id));
      const atlanan = data.length - setirler.length;

      this.log.log(`Toplu yaratma: ${idler.length} sətir, ${atlanan} atlandı`);

      return {
        ugur: true,
        gonderilen: data.length,
        yaradilan: setirler.length,
        atlanan,
        // ⚠️ `id` BigInt-dir — MÜTLƏQ mətnə çevirin, yoxsa
        // JSON cavabı «Do not know how to serialize a BigInt» verər.
        idler,
        cedvel_adi: 'kadrlar.emekdaslar',
      };
    } catch (x) {
      throw this.cevir(x);
    }
  }

  // ── 2. Toplu aktivlik ───────────────────────────────────────────
  /**
   * ⚠️ `updateMany` `{ count }` qaytarır — YENİLƏNMİŞ SƏTİRLƏRİ yox.
   * Sətirləri görmək lazımdırsa, ayrıca `findMany` etmək gərəkdir.
   *
   * `count` ilə `idler.length` fərqi ƏHƏMİYYƏTLİDİR: bəzi ID-lər
   * mövcud deyilsə, `count` az olacaq. İstifadəçiyə bunu BİLDİRMƏK
   * lazımdır — «sükutla az iş görmək» ən pis davranışdır.
   */
  async topluAktivlik(dto: TopluAktivlikDto): Promise<TopluDeyisiklikCavabi> {
    const idler = dto.idler.map((i) => BigInt(i));

    const netice = await this.prisma.emekdaslar.updateMany({
      where: { id: { in: idler } },
      data: { aktiv: dto.aktiv },
    });

    const tapilmayan = dto.idler.length - netice.count;
    if (tapilmayan > 0) {
      this.log.warn(`${tapilmayan} ID tapılmadı: ${dto.idler.join(', ')}`);
    }

    return {
      ugur: true,
      gonderilen_id: dto.idler.length,
      deyisen: netice.count,
      tapilmayan,
      melumat: dto.aktiv
        ? `${netice.count} əməkdaş aktiv edildi`
        : `${netice.count} əməkdaş passiv edildi (sətirlər silinmədi)`,
    };
  }

  // ── 3. Toplu maaş artımı ────────────────────────────────────────
  /**
   * ⚠️ `maas: { multiply: 1.1 }` — bu, ATOMİK əməliyyatdır.
   *
   * Niyə vacibdir? Sadəlövh yol belə olardı:
   *   1) sətirləri oxu → 2) `maas * 1.1` hesabla → 3) yaz
   * Bu üç addım arasında başqa istifadəçi maaşı dəyişsə, onun
   * dəyişikliyi İTƏR («lost update» problemi).
   *
   * `multiply` ilə isə hesablama SQL-in İÇİNDƏ olur:
   *   UPDATE ... SET maas = maas * 1.1 WHERE ...
   * Yəni oxu-yaz arasında boşluq yoxdur.
   */
  async maasArtim(dto: MaasArtimDto): Promise<TopluDeyisiklikCavabi> {
    const filterler = [dto.idler, dto.merkez_id, dto.vezife_id].filter(
      (x) => x !== undefined,
    );

    if (filterler.length === 0) {
      throw new BadRequestException(
        'Filtrsiz toplu maaş dəyişikliyi qadağandır — ' +
          'idler, merkez_id və ya vezife_id göndərin',
      );
    }

    const where: Prisma.emekdaslarWhereInput = { maas: { not: null } };
    if (dto.idler) where.id = { in: dto.idler.map((i) => BigInt(i)) };
    if (dto.merkez_id !== undefined) where.merkez_id = dto.merkez_id;
    if (dto.vezife_id !== undefined) where.vezife_id = dto.vezife_id;

    const emsal = 1 + dto.faiz / 100;

    const netice = await this.prisma.emekdaslar.updateMany({
      where,
      data: { maas: { multiply: emsal } },
    });

    this.log.log(`Maaş artımı: ${dto.faiz}% → ${netice.count} sətir`);

    const gonderilen = dto.idler?.length ??
      (await this.prisma.emekdaslar.count({
        where: dto.merkez_id !== undefined
          ? { merkez_id: dto.merkez_id }
          : { vezife_id: dto.vezife_id },
      }));

    return {
      ugur: true,
      gonderilen_id: gonderilen,
      deyisen: netice.count,
      tapilmayan: Math.max(0, gonderilen - netice.count),
      melumat: `Maaşlar ${dto.faiz > 0 ? '+' : ''}${dto.faiz}% dəyişdirildi (əmsal ${emsal})`,
    };
  }

  // ── 4. Atomikliyin SÜBUTU ───────────────────────────────────────
  /**
   * Tranzaksiya yarıda kəsilərsə nə olur? Bu metod bunu CANLI göstərir:
   * iki sətir yaradır, sonra QƏSDƏN xəta atır. Nəticədə:
   *   • HEÇ BİR sətir bazada qalmamalıdır (ROLLBACK),
   *   • audit loqunda da HEÇ BİR qeyd olmamalıdır — çünki trigger
   *     tranzaksiya COMMIT olmayanda işləmir.
   *
   * ⚠️ Metod heç nəyi DƏYİŞMİR — bu, təhlükəsiz nümayişdir.
   */
  async atomiklikYoxla(): Promise<AtomiklikCavabi> {
    const ep = `toplu.atomik.${Date.now()}@arti.edu.az`;

    const auditEvvel = await this.prisma.audit_log.count({
      where: { cedvel_adi: 'kadrlar.emekdaslar' },
    });

    let xetaMetni = '';
    let cehd = 0;

    try {
      await this.prisma.$transaction(async (tx) => {
        cehd = 1;
        await tx.emekdaslar.create({
          data: {
            ad: 'Atomik', soyad: 'Test', ata_adi: 'Sistem',
            cinsiyyet_id: 1, vezife_id: 6, email: `${ep}.1`,
          },
        });

        cehd = 2;
        await tx.emekdaslar.create({
          data: {
            ad: 'Atomik', soyad: 'Test', ata_adi: 'Sistem',
            cinsiyyet_id: 1, vezife_id: 6, email: `${ep}.2`,
          },
        });

        cehd = 3;
        // ⚠️ QƏSDƏN XƏTA — bütün tranzaksiya geri qaytarılmalıdır
        throw new Error('QƏSDƏN XƏTA: tranzaksiya geri qaytarılmalıdır');
      });
      xetaMetni = '(gözlənilməz: xəta atılmadı)';
    } catch (x) {
      xetaMetni = (x as Error).message;
    }

    const qalan = await this.prisma.emekdaslar.count({
      where: { email: { startsWith: ep } },
    });

    const auditSonra = await this.prisma.audit_log.count({
      where: { cedvel_adi: 'kadrlar.emekdaslar' },
    });

    this.log.log(`Atomiklik yoxlaması: bazada qalan ${qalan} sətir`);

    return {
      ugur: true,
      cehd_edilen: cehd,
      xeta: xetaMetni,
      bazada_qalan: qalan,
      audit_artimi: auditSonra - auditEvvel,
      izah:
        qalan === 0
          ? 'ROLLBACK işlədi: heç bir sətir qalmadı, audit loqu da artmadı'
          : 'XƏTA: tranzaksiya geri qaytarılmadı!',
    };
  }

  // ── Köməkçilər ──────────────────────────────────────────────────
  private gun(m: string | undefined): Date | null {
    return m ? new Date(`${m}T00:00:00Z`) : null;
  }

  private cevir(x: unknown): Error {
    if (x instanceof Prisma.PrismaClientKnownRequestError) {
      const h = (x.meta as { target?: string[] } | undefined)?.target;
      if (x.code === 'P2002') {
        return new BadRequestException(
          `Toplu yaratma ləğv edildi: ${h?.join(', ') ?? 'dəyər'} təkraralır. ` +
            'HEÇ BİR sətir yazılmadı. Təkrar olanları atlamaq üçün ' +
            '"tekrarlariAtla": true göndərin.',
        );
      }
      if (x.code === 'P2003') {
        return new BadRequestException(
          'Toplu yaratma ləğv edildi: əlaqəli ID-lərdən biri mövcud deyil. ' +
            'HEÇ BİR sətir yazılmadı.',
        );
      }
      this.log.error(`Prisma xətası ${x.code}`, x.message);
      return new BadRequestException(`Baza xətası: ${x.code}`);
    }
    this.log.error('Gözlənilməz xəta', x instanceof Error ? x.stack : String(x));
    return x instanceof Error ? x : new Error(String(x));
  }
}
