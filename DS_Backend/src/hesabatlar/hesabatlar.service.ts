import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

/** Hesabat modulu — hazir view ve funksiyalari isledir */
@Injectable()
export class HesabatlarService {
  constructor(private readonly prisma: PrismaService) {}

  /** Bazadaki butun view-lar */
  async gorunusler() {
    return this.prisma.$queryRaw<{ sxem: string; gorunus: string }[]>`
      SELECT table_schema AS sxem, table_name AS gorunus
        FROM information_schema.views
       WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
       ORDER BY 1, 2`;
  }

  /** Merkez -> shobe sayi (view-dan) */
  async merkezShobe() {
    return this.prisma.$queryRaw<
      { merkez_id: number; merkez: string; shobe_sayi: number }[]
    >`
      SELECT merkez_id::int, merkez, shobe_sayi
        FROM struktur.v_merkez_shobe_sayi
       ORDER BY shobe_sayi DESC`;
  }

  /** Emekdasin tam profili (view-dan) */
  async emekdasTam(limit = 20) {
    return this.prisma.$queryRawUnsafe<
      {
        id: number; tam_adi: string; vezife: string | null;
        shobe: string | null; merkez: string | null;
        maas: number | null; status: string | null;
      }[]
    >(
      `SELECT id::int, tam_adi, vezife, shobe, merkez, maas::float8, status
         FROM kadrlar.v_emekdas_tam ORDER BY maas DESC NULLS LAST LIMIT $1`,
      limit,
    );
  }

  /** Budce istifadesi (view-dan) */
  async budceIstifadesi() {
    return this.prisma.$queryRaw<
      {
        budce_id: number; il: number; menbe: string;
        plan_mebleg: number; xerclenmis: number; qaliq: number;
      }[]
    >`
      SELECT budce_id::int, il, menbe,
             plan_mebleg::float8, xerclenmis::float8, qaliq::float8
        FROM maliyye.v_budce_istifadesi ORDER BY il DESC, plan_mebleg DESC`;
  }

  /** Telim qrupu -> istirakci sayi (view-dan) */
  async telimQruplari() {
    return this.prisma.$queryRaw<
      { qrup_id: number; qrup: string; proqram: string; status: string; istirakci_sayi: number }[]
    >`
      SELECT qrup_id::int, qrup, proqram, status, istirakci_sayi
        FROM tehsil.v_telim_qrup_istirakci_sayi
       ORDER BY istirakci_sayi DESC`;
  }

  /** Butun funksiyalari bir sorguda cagir */
  async funksiyalar() {
    const setirler = await this.prisma.$queryRaw<
      {
        maas_fondu: number; orta_bal: number; budce_2026: number;
        sertifikasiya_ortalamasi: number;
      }[]
    >`
      SELECT kadrlar.fn_maas_fondu()::float8              AS maas_fondu,
             tehsil.fn_sertifikasiya_ortalamasi()::float8 AS orta_bal,
             maliyye.fn_budce_il_cemi(2026)::float8       AS budce_2026,
             tehsil.fn_sertifikasiya_ortalamasi()::float8 AS sertifikasiya_ortalamasi`;
    return setirler[0];
  }

  /** Il uzre budce icmali — ROLLUP ile yekun */
  async budceIcmali() {
    return this.prisma.$queryRaw<
      { il: string; setir: number; mebleg: number }[]
    >`
      SELECT COALESCE(il::text, 'CƏMİ') AS il,
             count(*)::int              AS setir,
             sum(mebleg)::float8        AS mebleg
        FROM maliyye.budce
       GROUP BY ROLLUP (il)
       ORDER BY il NULLS LAST`;
  }

  /** En son audit qeydleri */
  async sonAudit(limit = 10) {
    return this.prisma.$queryRawUnsafe<
      { id: number; cedvel_adi: string; emeliyyat: string; istifadeci: string | null; vaxt: string }[]
    >(
      `SELECT id::int, cedvel_adi, emeliyyat, istifadeci, vaxt::text
         FROM audit.audit_log ORDER BY vaxt DESC LIMIT $1`,
      limit,
    );
  }

  /** Umumi baza icmali — dashboard ucun */
  async umumiIcmal() {
    const cedveller = await this.prisma.$queryRaw<{ cedvel: number; gorunus: number }[]>`
      SELECT count(*)::int AS cedvel FROM information_schema.tables
       WHERE table_type = 'BASE TABLE'
         AND table_schema NOT IN ('pg_catalog', 'information_schema')`;
    const gorunus = await this.prisma.$queryRaw<{ say: number }[]>`
      SELECT count(*)::int AS say FROM information_schema.views
       WHERE table_schema NOT IN ('pg_catalog', 'information_schema')`;
    const emekdas = await this.prisma.$queryRaw<{ say: number; fon: number }[]>`
      SELECT count(*)::int AS say, COALESCE(sum(maas), 0)::float8 AS fon
        FROM kadrlar.emekdaslar WHERE aktiv = true`;
    const layihe = await this.prisma.$queryRaw<{ say: number }[]>`
      SELECT count(*)::int AS say FROM elm.tedqiqat_layiheleri WHERE status = 'davam edir'`;

    return {
      cedvel_sayi: cedveller[0]?.cedvel ?? 0,
      gorunus_sayi: gorunus[0]?.say ?? 0,
      aktiv_emekdas: emekdas[0]?.say ?? 0,
      emek_haqqi_fondu: emekdas[0]?.fon ?? 0,
      davam_eden_layihe: layihe[0]?.say ?? 0,
    };
  }
}
