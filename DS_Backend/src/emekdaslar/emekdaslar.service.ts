import {
  BadRequestException,
  ConflictException,
  Injectable,
  Logger,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '../generated/prisma/client.js';
import { PrismaService } from '../prisma/prisma.service.js';
import { EmekdasSorguDto } from './dto/emekdas-sorgu.dto.js';
import { EmekdasYaratDto } from './dto/emekdas-yarat.dto.js';
import { EmekdasYenileDto } from './dto/emekdas-yenile.dto.js';
import {
  EMEKDAS_SECIM,
  hazirla,
  type EmekdasCavabi,
  type EmekdasSetiri,
} from './dto/emekdas-cavab.dto.js';

/** Səhifələnmiş siyahı cavabı */
export interface SehifeCavabi {
  ugur: true;
  sehife: number;
  limit: number;
  cem: number;
  sehife_sayi: number;
  melumat: EmekdasCavabi[];
}

/** Silmə əməliyyatının nəticəsi */
export interface SilmeCavabi {
  ugur: true;
  id: string;
  nov: 'soft' | 'hard';
  mesaj: string;
  asili_qeydler: Record<string, number>;
}

@Injectable()
export class EmekdaslarService {
  private readonly log = new Logger('EMEKDASLAR');

  constructor(private readonly prisma: PrismaService) {}

  // ── READ (hamısı) ────────────────────────────────────────────────
  async hamisi(sorgu: EmekdasSorguDto): Promise<SehifeCavabi> {
    const sehife = sorgu.seife;
    const limit = sorgu.limit;

    const where: Prisma.emekdaslarWhereInput = {};

    if (sorgu.aktiv === 'aktiv') where.aktiv = true;
    else if (sorgu.aktiv === 'passiv') where.aktiv = false;

    if (sorgu.axtar) {
      where.OR = [
        { ad: { contains: sorgu.axtar, mode: 'insensitive' } },
        { soyad: { contains: sorgu.axtar, mode: 'insensitive' } },
        { ata_adi: { contains: sorgu.axtar, mode: 'insensitive' } },
        { email: { contains: sorgu.axtar, mode: 'insensitive' } },
      ];
    }

    if (sorgu.merkez_id !== undefined) where.merkez_id = sorgu.merkez_id;
    if (sorgu.shobe_id !== undefined) where.shobe_id = sorgu.shobe_id;

    const orderBy = {
      [sorgu.siralama]: sorgu.tertib,
    } as Prisma.emekdaslarOrderByWithRelationInput;

    // `$transaction` — say və siyahı BİR sorğuda gedir.
    // Ayrı-ayrı göndərsəydik, aralarında başqa istifadəçi sətir əlavə
    // edə bilərdi və `cem` ilə `melumat.length` uyğunsuz olardı.
    const [cem, setirler] = await this.prisma.$transaction([
      this.prisma.emekdaslar.count({ where }),
      this.prisma.emekdaslar.findMany({
        where,
        select: EMEKDAS_SECIM,
        orderBy,
        skip: (sehife - 1) * limit,
        take: limit,
      }),
    ]);

    return {
      ugur: true,
      sehife,
      limit,
      cem,
      sehife_sayi: Math.ceil(cem / limit),
      melumat: setirler.map(hazirla),
    };
  }

  // ── READ (biri) ──────────────────────────────────────────────────
  async biri(id: number): Promise<EmekdasCavabi> {
    const setir = await this.prisma.emekdaslar.findUnique({
      where: { id: BigInt(id) },
      select: EMEKDAS_SECIM,
    });

    if (!setir) {
      throw new NotFoundException(`ID ${id} olan əməkdaş tapılmadı`);
    }

    return hazirla(setir);
  }

  // ── CREATE ───────────────────────────────────────────────────────
  async yarat(dto: EmekdasYaratDto): Promise<EmekdasCavabi> {
    const data: Prisma.emekdaslarUncheckedCreateInput = {
      ad: dto.ad.trim(),
      soyad: dto.soyad.trim(),
      ata_adi: dto.ata_adi.trim(),
      cinsiyyet_id: dto.cinsiyyet_id,
      vezife_id: dto.vezife_id,
      is_status_id: dto.is_status_id ?? 1,
      aktiv: dto.aktiv ?? true,
      email: dto.email ?? null,
      telefon: dto.telefon ?? null,
      shobe_id: dto.shobe_id ?? null,
      merkez_id: dto.merkez_id ?? null,
      elmi_derece_id: dto.elmi_derece_id ?? null,
      elmi_ad_id: dto.elmi_ad_id ?? null,
      maas: dto.maas ?? null,
      dogum_tarixi: gun(dto.dogum_tarixi),
      ise_baslama: gun(dto.ise_baslama),
    };

    try {
      const setir = await this.prisma.emekdaslar.create({
        data,
        select: EMEKDAS_SECIM,
      });

      this.log.log(`Yeni əməkdaş yaradıldı: ID ${setir.id} — ${setir.ad} ${setir.soyad}`);
      return hazirla(setir);
    } catch (x) {
      throw this.cevir(x);
    }
  }

  // ── UPDATE (qismən) ──────────────────────────────────────────────
  async yenile(id: number, dto: EmekdasYenileDto): Promise<EmekdasCavabi> {
    // ⚠️ TƏLƏ: `Object.keys(dto)` KİFAYƏT DEYİL!
    //
    // `tsconfig.json`-da `target: ES2023`-dür və bu, TypeScript-in
    // `useDefineForClassFields` davranışını işə salır: sinifdə elan
    // olunan HƏR sahə, dəyəri `undefined` olsa da, obyektdə AÇAR kimi
    // mövcud olur. Yəni istifadəçi `{}` göndərsə belə,
    // `Object.keys(dto).length` 16 qaytarır — guard heç vaxt işləmir!
    //
    // Düzgün yol: yalnız `undefined` OLMAYAN sahələri say.
    const verilen = Object.entries(dto)
      .filter(([, deyer]) => deyer !== undefined)
      .map(([ad]) => ad);

    if (verilen.length === 0) {
      throw new BadRequestException(
        'Yeniləmək üçün ən azı bir sahə göndərilməlidir',
      );
    }

    const data: Prisma.emekdaslarUncheckedUpdateInput = {};

    if (dto.ad !== undefined) data.ad = dto.ad.trim();
    if (dto.soyad !== undefined) data.soyad = dto.soyad.trim();
    if (dto.ata_adi !== undefined) data.ata_adi = dto.ata_adi.trim();
    if (dto.cinsiyyet_id !== undefined) data.cinsiyyet_id = dto.cinsiyyet_id;
    if (dto.vezife_id !== undefined) data.vezife_id = dto.vezife_id;
    if (dto.is_status_id !== undefined) data.is_status_id = dto.is_status_id;
    if (dto.aktiv !== undefined) data.aktiv = dto.aktiv;
    if (dto.email !== undefined) data.email = dto.email;
    if (dto.telefon !== undefined) data.telefon = dto.telefon;
    if (dto.shobe_id !== undefined) data.shobe_id = dto.shobe_id;
    if (dto.merkez_id !== undefined) data.merkez_id = dto.merkez_id;
    if (dto.elmi_derece_id !== undefined) data.elmi_derece_id = dto.elmi_derece_id;
    if (dto.elmi_ad_id !== undefined) data.elmi_ad_id = dto.elmi_ad_id;
    if (dto.maas !== undefined) data.maas = dto.maas;
    if (dto.dogum_tarixi !== undefined) data.dogum_tarixi = gun(dto.dogum_tarixi);
    if (dto.ise_baslama !== undefined) data.ise_baslama = gun(dto.ise_baslama);

    try {
      const setir = await this.prisma.emekdaslar.update({
        where: { id: BigInt(id) },
        data,
        select: EMEKDAS_SECIM,
      });

      this.log.log(`Yeniləndi: ID ${id} — sahələr: ${verilen.join(', ')}`);
      return hazirla(setir);
    } catch (x) {
      throw this.cevir(x);
    }
  }

  // ── DELETE ───────────────────────────────────────────────────────
  /**
   * ⚠️ NİYƏ ADİ `delete` DEYİL?
   *
   * `emekdaslar` cədvəlinə 16 cədvəl bağlıdır. Onlardan 4-ü
   * (`doktorantlar`, `istifadeciler`, `elmi_shura_uzvleri`,
   * `sertifikasiya`) `onDelete: NoAction` ilə bağlıdır — yəni
   * PostgreSQL həmin sətirlər mövcud olduqca silməyə İCAZƏ VERMİR.
   *
   * Mesaj: «Silmək üçün əvvəlcə asılı qeydləri silin». Amma
   * real həyatda əməkdaş «işdən çıxır», məlumatı isə tarix üçün
   * saxlamaq lazımdır (hesabatlar, arxiv). Ona görə:
   *
   *   asılı qeyd VARSA → YUMŞAQ SİLMƏ (`aktiv = false`)
   *   asılı qeyd YOXDURSA → ADİ SİLMƏ (sətir bazadan çıxır)
   */
  async sil(id: number): Promise<SilmeCavabi> {
    const movcud = await this.prisma.emekdaslar.findUnique({
      where: { id: BigInt(id) },
      select: { id: true, ad: true, soyad: true, aktiv: true },
    });

    if (!movcud) {
      throw new NotFoundException(`ID ${id} olan əməkdaş tapılmadı`);
    }

    const asili = await this.asililariSay(id);
    const cem = Object.values(asili).reduce((a, b) => a + b, 0);

    if (cem > 0) {
      await this.prisma.emekdaslar.update({
        where: { id: BigInt(id) },
        data: { aktiv: false },
      });

      this.log.warn(`YUMŞAQ SİLMƏ: ID ${id} — ${cem} asılı qeyd var`);

      return {
        ugur: true,
        id: String(id),
        nov: 'soft',
        mesaj:
          `${movcud.ad} ${movcud.soyad} passiv edildi (aktiv = false). ` +
          `${cem} asılı qeyd olduğu üçün sətir bazadan SİLİNMƏDİ — ` +
          'tarixi məlumat qorunur.',
        asili_qeydler: asili,
      };
    }

    await this.prisma.emekdaslar.delete({ where: { id: BigInt(id) } });
    this.log.log(`ADİ SİLMƏ: ID ${id} — asılı qeyd yoxdur`);

    return {
      ugur: true,
      id: String(id),
      nov: 'hard',
      mesaj: `${movcud.ad} ${movcud.soyad} bazadan tamamilə silindi (asılı qeyd yox idi).`,
      asili_qeydler: {},
    };
  }

  /** Əməkdaşa bağlı sətirləri cədvəl-cədvəl sayır */
  private async asililariSay(id: number): Promise<Record<string, number>> {
    const b = BigInt(id);

    const [doktorant, istifadeci, shura_uzvu, sertifikat, mezuniyyet, teyinat, rehberlik] =
      await this.prisma.$transaction([
        this.prisma.doktorantlar.count({ where: { rehber_id: b } }),
        this.prisma.istifadeciler.count({ where: { emekdas_id: b } }),
        this.prisma.elmi_shura_uzvleri.count({ where: { emekdas_id: b } }),
        this.prisma.sertifikasiya.count({ where: { emekdas_id: b } }),
        this.prisma.mezuniyyetler.count({ where: { emekdas_id: b } }),
        this.prisma.vezife_teyinatlari.count({ where: { emekdas_id: b } }),
        this.prisma.rehberlik.count({ where: { emekdas_id: b } }),
      ]);

    return {
      doktorantlar: doktorant,
      istifadeciler: istifadeci,
      elmi_shura_uzvleri: shura_uzvu,
      sertifikasiya: sertifikat,
      mezuniyyetler: mezuniyyet,
      vezife_teyinatlari: teyinat,
      rehberlik,
    };
  }

  /** Prisma xətalarını HTTP xətalarına çevirir */
  private cevir(x: unknown): Error {
    if (x instanceof Prisma.PrismaClientKnownRequestError) {
      const hədəf = (x.meta as { target?: string[] } | undefined)?.target;

      if (x.code === 'P2002') {
        return new ConflictException(
          `Bu ${hədəf?.join(', ') ?? 'dəyər'} artıq başqa əməkdaşda qeydiyyatdadır`,
        );
      }
      if (x.code === 'P2003') {
        return new BadRequestException(
          'Göstərilən əlaqəli ID mövcud deyil (cinsiyyet / vəzifə / şöbə / mərkəz)',
        );
      }
      if (x.code === 'P2025') {
        return new NotFoundException('Qeyd tapılmadı');
      }

      this.log.error(`Prisma xətası ${x.code}`, x.message);
      return new BadRequestException(`Baza xətası: ${x.code}`);
    }

    this.log.error('Gözlənilməz xəta', x instanceof Error ? x.stack : String(x));
    return x instanceof Error ? x : new Error(String(x));
  }
}

/**
 * `YYYY-MM-DD` mətnini `Date` obyektinə çevirir.
 *
 * ⚠️ Niyə `new Date('1985-03-12')` yazmırıq? Çünki JavaScript onu
 * UTC kimi oxuyur, bazada isə `date` sütunudur və yerli saat qurşağında
 * bir gün geri/irəli sürüşə bilər. `T00:00:00Z` yazmaqla bunun qarşısını
 * alırıq — həmişə günün başlanğıcı götürülür.
 */
function gun(m: string | undefined): Date | null {
  return m ? new Date(`${m}T00:00:00Z`) : null;
}
