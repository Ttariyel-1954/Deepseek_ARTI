import {
  BadRequestException, Injectable, NotFoundException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';
import { EmekdasFiltrDto } from './dto/emekdas-filtr.dto.js';
import { Sehifelenmis } from '../common/dto/sehife.dto.js';

/** Tam profil — 5 cedvelin birlesmesi */
export interface EmekdasTam {
  id: number;
  tam_adi: string;
  vezife: string | null;
  shobe: string | null;
  merkez: string | null;
  cins: string | null;
  elmi_derece: string | null;
  elmi_ad: string | null;
  email: string | null;
  telefon: string | null;
  ise_baslama: string | null;
  maas: number | null;
  aktiv: boolean;
}

/** SQL injection qorumasi — siralama sutunlari */
const SIRALAMA_ICAZELI = [
  'id', 'tam_adi', 'vezife', 'merkez', 'maas', 'ise_baslama',
] as const;

const BIRLESME = `
  FROM kadrlar.emekdaslar e
  LEFT JOIN struktur.vezifeler   v  ON v.id  = e.vezife_id
  LEFT JOIN struktur.shobeler    s  ON s.id  = e.shobe_id
  LEFT JOIN struktur.merkezler   m  ON m.id  = e.merkez_id
  LEFT JOIN ortaq.cinsiyyet      c  ON c.id  = e.cinsiyyet_id
  LEFT JOIN ortaq.elmi_dereceler d  ON d.id  = e.elmi_derece_id
  LEFT JOIN ortaq.elmi_adlar     a  ON a.id  = e.elmi_ad_id
`;

const SAHELER = `
  e.id::int                                   AS id,
  e.soyad || ' ' || e.ad || ' ' || e.ata_adi AS tam_adi,
  v.ad                                        AS vezife,
  s.ad                                        AS shobe,
  m.ad                                        AS merkez,
  c.ad                                        AS cins,
  d.ad                                        AS elmi_derece,
  a.ad                                        AS elmi_ad,
  e.email,
  e.telefon,
  e.ise_baslama::text                         AS ise_baslama,
  e.maas::float8                              AS maas,
  e.aktiv
`;

@Injectable()
export class KadrlarService {
  constructor(private readonly prisma: PrismaService) {}

  /** Filtri SQL serti + parametrlere cevirir */
  private sertQur(dto: EmekdasFiltrDto): { where: string; parametrler: unknown[] } {
    const sertler: string[] = [];
    const parametrler: unknown[] = [];
    let n = 1;

    const axtar = dto.axtar?.trim();
    if (axtar) {
      sertler.push(
        `(e.ad ILIKE $${n} OR e.soyad ILIKE $${n} OR e.ata_adi ILIKE $${n}
          OR e.email ILIKE $${n} OR e.telefon ILIKE $${n})`,
      );
      parametrler.push(`%${axtar}%`);
      n++;
    }

    const sadə: [keyof EmekdasFiltrDto, string][] = [
      ['merkez_id', 'e.merkez_id'],
      ['shobe_id', 'e.shobe_id'],
      ['vezife_id', 'e.vezife_id'],
      ['elmi_derece_id', 'e.elmi_derece_id'],
    ];

    for (const [acar, sutun] of sadə) {
      const deyer = dto[acar];
      if (deyer !== undefined && deyer !== null) {
        sertler.push(`${sutun} = $${n}`);
        parametrler.push(deyer);
        n++;
      }
    }

    if (dto.aktiv !== undefined) {
      sertler.push(`e.aktiv = $${n}`);
      parametrler.push(dto.aktiv);
      n++;
    }

    if (dto.min_maas !== undefined) {
      sertler.push(`e.maas >= $${n}`);
      parametrler.push(dto.min_maas);
      n++;
    }

    if (dto.max_maas !== undefined) {
      sertler.push(`e.maas <= $${n}`);
      parametrler.push(dto.max_maas);
      n++;
    }

    const where = sertler.length ? `WHERE ${sertler.join(' AND ')}` : '';
    return { where, parametrler };
  }

  /** Sehifelenmis emekdas siyahisi */
  async emekdaslar(dto: EmekdasFiltrDto): Promise<Sehifelenmis<EmekdasTam>> {
    const { where, parametrler } = this.sertQur(dto);

    const sutun = this.sutunYoxla(dto.siralama_sah);
    const istiqamet = dto.siralama === 'desc' ? 'DESC' : 'ASC';

    const setirler = await this.prisma.$queryRawUnsafe<EmekdasTam[]>(
      `SELECT ${SAHELER} ${BIRLESME} ${where}
        ORDER BY ${sutun} ${istiqamet}
        LIMIT $${parametrler.length + 1} OFFSET $${parametrler.length + 2}`,
      ...parametrler, dto.limit, dto.offset,
    );

    const cemCavab = await this.prisma.$queryRawUnsafe<{ cem: number }[]>(
      `SELECT count(*)::int AS cem ${BIRLESME} ${where}`,
      ...parametrler,
    );

    const umumi = cemCavab[0]?.cem ?? 0;

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

  /** Siralama sutununu yoxlayir — yanlis sutun 400 verir */
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

  /** Bir emekdasin tam profili */
  async emekdas(id: number): Promise<EmekdasTam> {
    const setirler = await this.prisma.$queryRawUnsafe<EmekdasTam[]>(
      `SELECT ${SAHELER} ${BIRLESME} WHERE e.id = $1`, id,
    );
    if (!setirler.length) {
      throw new NotFoundException(`Emekdas tapilmadi: id=${id}`);
    }
    return setirler[0];
  }

  /** Merkez ve vezife uzre icmal */
  async icmal() {
    const merkezUzre = await this.prisma.$queryRaw<
      { merkez: string; emekdas: number; orta_maas: number; fond: number }[]
    >`
      SELECT m.ad AS merkez,
             count(e.id)::int                 AS emekdas,
             COALESCE(round(avg(e.maas), 2), 0)::float8 AS orta_maas,
             COALESCE(sum(e.maas), 0)::float8 AS fond
        FROM struktur.merkezler m
        LEFT JOIN kadrlar.emekdaslar e ON e.merkez_id = m.id
       GROUP BY m.ad ORDER BY fond DESC`;

    const vezifeUzre = await this.prisma.$queryRaw<
      { vezife: string; seviyye: number; emekdas: number }[]
    >`
      SELECT v.ad AS vezife, v.seviyye, count(e.id)::int AS emekdas
        FROM struktur.vezifeler v
        LEFT JOIN kadrlar.emekdaslar e ON e.vezife_id = v.id
       GROUP BY v.ad, v.seviyye ORDER BY v.seviyye`;

    const umumi = await this.prisma.$queryRaw<{ fond: number; say: number }[]>`
      SELECT COALESCE(sum(maas), 0)::float8 AS fond,
             count(*)::int AS say
        FROM kadrlar.emekdaslar WHERE aktiv = true`;

    return {
      merkez_uzre: merkezUzre,
      vezife_uzre: vezifeUzre,
      umumi_fond: umumi[0]?.fond ?? 0,
      aktiv_say: umumi[0]?.say ?? 0,
    };
  }
}
