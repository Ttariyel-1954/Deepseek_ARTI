import {
  BadRequestException, ConflictException, Injectable, NotFoundException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';
import { CreateMerkezDto } from './dto/create-merkez.dto.js';
import { UpdateMerkezDto } from './dto/update-merkez.dto.js';
import { MerkezFiltrDto } from './dto/merkez-filtr.dto.js';
import { Sehifelenmis } from '../common/dto/sehife.dto.js';

/** Bazadan gelen setir */
export interface Merkez {
  id: number;
  ad: string;
  tip: string | null;
  unvan: string | null;
  telefon: string | null;
  email: string | null;
  aktiv: boolean;
}

/**
 * SQL INJECTION QORUMASI.
 * Siralama sutunu birbasa SQL-e yazilir, ona gore YALNIZ
 * bu siyahidaki adlara icaze verilir.
 */
const SIRALAMA_ICAZELI = ['id', 'ad', 'tip', 'unvan'] as const;

const SAHELER = 'id::int, ad, tip, unvan, telefon, email, aktiv';

@Injectable()
export class StrukturService {
  constructor(private readonly prisma: PrismaService) {}

  /** Sehifelenmis, filtreli, siralanmis siyahi */
  async merkezler(dto: MerkezFiltrDto): Promise<Sehifelenmis<Merkez>> {
    const sutun = this.sutunYoxla(dto.siralama_sah);
    const istiqamet = dto.siralama === 'desc' ? 'DESC' : 'ASC';

    const axtar = dto.axtar?.trim() || null;
    const kimi = axtar ? `%${axtar}%` : null;

    const setirler = await this.prisma.$queryRawUnsafe<Merkez[]>(
      `SELECT ${SAHELER}
         FROM struktur.merkezler
        WHERE ($1::text IS NULL OR ad ILIKE $1 OR unvan ILIKE $1 OR email ILIKE $1)
          AND ($2::text IS NULL OR tip = $2)
          AND ($3::boolean IS NULL OR aktiv = $3)
        ORDER BY ${sutun} ${istiqamet}
        LIMIT $4 OFFSET $5`,
      kimi, dto.tip ?? null, dto.aktiv ?? null, dto.limit, dto.offset,
    );

    const cem = await this.prisma.$queryRawUnsafe<{ cem: number }[]>(
      `SELECT count(*)::int AS cem
         FROM struktur.merkezler
        WHERE ($1::text IS NULL OR ad ILIKE $1 OR unvan ILIKE $1 OR email ILIKE $1)
          AND ($2::text IS NULL OR tip = $2)
          AND ($3::boolean IS NULL OR aktiv = $3)`,
      kimi, dto.tip ?? null, dto.aktiv ?? null,
    );

    const umumi = cem[0]?.cem ?? 0;

    return {
      data: setirler,
      meta: {
        sehife: dto.sehife,
        limit: dto.limit,
        cem: umumi,
        sehife_sayi: Math.ceil(umumi / dto.limit) || 1,
      },
    };
  }

  /** Bir merkez */
  async merkez(id: number): Promise<Merkez> {
    const setirler = await this.prisma.$queryRaw<Merkez[]>`
      SELECT id::int, ad, tip, unvan, telefon, email, aktiv
      FROM struktur.merkezler WHERE id = ${id}`;

    if (!setirler.length) {
      throw new NotFoundException(`Merkez tapilmadi: id=${id}`);
    }
    return setirler[0];
  }

  /** Yeni merkez */
  async yarat(dto: CreateMerkezDto): Promise<Merkez> {
    await this.adYoxla(dto.ad);

    const setirler = await this.prisma.$queryRaw<Merkez[]>`
      INSERT INTO struktur.merkezler
        (ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv)
      VALUES
        (${dto.ad}, ${dto.tip ?? 'merkez'}, ${dto.tesvir ?? null},
         ${dto.unvan ?? null}, ${dto.telefon ?? null}, ${dto.email ?? null},
         ${dto.yaradilma_tarixi ?? null}, ${dto.aktiv ?? true})
      RETURNING id::int, ad, tip, unvan, telefon, email, aktiv`;

    return setirler[0];
  }

  /** Yenile — yalniz gonderilen saheler */
  async yenile(id: number, dto: UpdateMerkezDto): Promise<Merkez> {
    const movcud = await this.merkez(id);

    if (dto.ad && dto.ad !== movcud.ad) await this.adYoxla(dto.ad, id);

    const setirler = await this.prisma.$queryRaw<Merkez[]>`
      UPDATE struktur.merkezler
         SET ad      = COALESCE(${dto.ad ?? null}, ad),
             tip     = COALESCE(${dto.tip ?? null}, tip),
             tesvir  = COALESCE(${dto.tesvir ?? null}, tesvir),
             unvan   = COALESCE(${dto.unvan ?? null}, unvan),
             telefon = COALESCE(${dto.telefon ?? null}, telefon),
             email   = COALESCE(${dto.email ?? null}, email),
             aktiv   = COALESCE(${dto.aktiv ?? null}, aktiv)
       WHERE id = ${id}
      RETURNING id::int, ad, tip, unvan, telefon, email, aktiv`;

    return setirler[0];
  }

  /** Sil — bagli setir varsa 409 */
  async sil(id: number): Promise<{ silindi: true; id: number }> {
    await this.merkez(id);

    const bagli = await this.prisma.$queryRaw<{ say: number }[]>`
      SELECT count(*)::int AS say FROM struktur.shobeler WHERE merkez_id = ${id}`;

    const say = bagli[0]?.say ?? 0;
    if (say > 0) {
      throw new ConflictException(
        `Bu merkeze ${say} shobe baglidir — evvelce onlari kocurun`,
      );
    }

    await this.prisma.$executeRaw`DELETE FROM struktur.merkezler WHERE id = ${id}`;
    return { silindi: true, id };
  }

  /** Merkez + shobe sayi */
  async merkezStatistikasi() {
    return this.prisma.$queryRaw<
      { merkez: string; shobe_sayi: number; emekdas_sayi: number }[]
    >`
      SELECT m.ad AS merkez,
             count(DISTINCT s.id)::int AS shobe_sayi,
             count(DISTINCT e.id)::int AS emekdas_sayi
        FROM struktur.merkezler m
        LEFT JOIN struktur.shobeler  s ON s.merkez_id = m.id
        LEFT JOIN kadrlar.emekdaslar e ON e.merkez_id = m.id
       GROUP BY m.ad
       ORDER BY shobe_sayi DESC, emekdas_sayi DESC`;
  }

  /**
   * Siralama sutununu yoxlayir.
   * Sukutla 'id'-ye dusmek SƏHVDİR — istifadeci yazdiği sütunun
   * işlədiyini düşünər. Ona görə açıq xəta atiriq.
   */
  private sutunYoxla(sutun?: string): string {
    if (!sutun) return 'id';
    if (!(SIRALAMA_ICAZELI as readonly string[]).includes(sutun)) {
      throw new BadRequestException(
        `Bu sutun uzre siralama mumkun deyil: "${sutun}". ` +
        `Icazeli sutunlar: ${SIRALAMA_ICAZELI.join(', ')}`,
      );
    }
    return sutun;
  }

  /** Eyni adli merkez varmi? */
  private async adYoxla(ad: string, xaricId?: number): Promise<void> {
    const setirler = await this.prisma.$queryRaw<{ id: number }[]>`
      SELECT id::int FROM struktur.merkezler
       WHERE lower(ad) = lower(${ad})
         AND (${xaricId ?? null}::int IS NULL OR id <> ${xaricId ?? null})`;

    if (setirler.length) {
      throw new ConflictException(`Bu adla merkez artiq movcuddur: "${ad}"`);
    }
  }

  /** Id-nin musbet tam eded oldugunu yoxla */
  static idYoxla(id: number): void {
    if (!Number.isInteger(id) || id <= 0) {
      throw new BadRequestException('id musbet tam eded olmalidir');
    }
  }
}
