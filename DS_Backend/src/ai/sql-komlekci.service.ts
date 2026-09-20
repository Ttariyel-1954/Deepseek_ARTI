import { BadRequestException, Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

/**
 * TƏBİİ DİL -> SQL KÖMƏKÇİSİ
 *
 * ══════════════════════════════════════════════════════════════
 *  TƏHLÜKƏSİZLİK PRİNSİPİ
 * ══════════════════════════════════════════════════════════════
 *  AI HEÇ VAXT birbaşa SQL YAZMIR.
 *
 *  AI yalnız RESEPT ADI seçir (mes: 'en_cox_maas').
 *  SQL isə bu faylda SABİT yazılıb — dəyişdirilə bilməz.
 *
 *  Səbəb: AI-a SQL yazmaq hüququ versek, o:
 *    - DELETE / DROP yaza bilər
 *    - Başqa cədvəlləri oxuya bilər
 *    - Prompt injection ilə aldadıla bilər
 * ══════════════════════════════════════════════════════════════
 */

export interface Resept {
  ad: string;
  açarSözler: string[];
  izah: string;
  sql: string;
  parametrli?: boolean;
}

export interface SqlNetice {
  sual: string;
  resept: string;
  izah: string;
  sql: string;
  setirler: Record<string, unknown>[];
  setirSayi: number;
  icra_ms: number;
}

/** RESEPT REYESTRİ — butun SQL burada, SABİT */
const RESEPTLER: Resept[] = [
  {
    ad: 'emekdas_sayi',
    açarSözler: ['neçə əməkdaş', 'nece emekdas', 'işçi sayı', 'kadr sayı', 'əməkdaş sayı'],
    izah: 'Aktiv əməkdaşların ümumi sayı',
    sql: `SELECT count(*)::int AS emekdas_sayi
            FROM kadrlar.emekdaslar WHERE aktiv = true`,
  },
  {
    ad: 'en_cox_maas',
    açarSözler: ['ən çox maaş', 'en cox maas', 'yüksək maaş', 'bahalı işçi', 'top maaş'],
    izah: 'Ən yüksək maaş alan əməkdaşlar',
    sql: `SELECT e.soyad || ' ' || e.ad AS emekdas,
                 m.ad AS merkez,
                 e.maas::float8 AS maas
            FROM kadrlar.emekdaslar e
            LEFT JOIN struktur.merkezler m ON m.id = e.merkez_id
           WHERE e.aktiv = true
           ORDER BY e.maas DESC NULLS LAST
           LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'merkez_uzre',
    açarSözler: ['mərkəz üzrə', 'merkez uzre', 'mərkəzlər', 'şöbə sayı', 'mərkəz sayı'],
    izah: 'Hər mərkəz üzrə şöbə və əməkdaş sayı',
    sql: `SELECT m.ad AS merkez,
                 count(DISTINCT s.id)::int AS shobe_sayi,
                 count(DISTINCT e.id)::int AS emekdas_sayi
            FROM struktur.merkezler m
            LEFT JOIN struktur.shobeler  s ON s.merkez_id = m.id
            LEFT JOIN kadrlar.emekdaslar e ON e.merkez_id = m.id
           GROUP BY m.ad ORDER BY shobe_sayi DESC LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'maas_fondu',
    açarSözler: ['maaş fondu', 'maas fondu', 'ümumi maaş', 'ə/h fondu', 'əmək haqqı'],
    izah: 'Aylıq əmək haqqı fondu',
    sql: `SELECT count(*)::int                  AS emekdas,
                 sum(maas)::float8             AS aylıq_fond,
                 round(avg(maas), 2)::float8   AS orta_maas
            FROM kadrlar.emekdaslar WHERE aktiv = true`,
  },
  {
    ad: 'layiheler',
    açarSözler: ['layihə', 'layihe', 'tədqiqat', 'tedqiqat', 'elmi iş'],
    izah: 'Elmi-tədqiqat layihələri',
    sql: `SELECT l.ad AS layihe, i.ad AS istiqamet, l.status,
                 l.baslama_tarixi::text AS baslama
            FROM elm.tedqiqat_layiheleri l
            JOIN elm.tedqiqat_istiqametleri i ON i.id = l.istiqamet_id
           ORDER BY l.baslama_tarixi DESC NULLS LAST LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'budce',
    açarSözler: ['büdcə', 'budce', 'maliyyə', 'maliyye', 'xərc'],
    izah: 'İllər üzrə büdcə',
    sql: `SELECT il, menbe, mebleg::float8 AS mebleg
            FROM maliyye.budce ORDER BY il DESC, mebleg DESC LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'telim_qruplari',
    açarSözler: ['qrup', 'təlim', 'telim', 'kurs', 'iştirakçı'],
    izah: 'Təlim qrupları və iştirakçı sayı',
    sql: `SELECT q.ad AS qrup, p.ad AS proqram, q.status,
                 count(i.id)::int AS istirakci
            FROM tehsil.telim_qruplari q
            JOIN tehsil.telim_proqramlari p ON p.id = q.proqram_id
            LEFT JOIN tehsil.telim_istirakcilari i ON i.qrup_id = q.id
           GROUP BY q.ad, p.ad, q.status
           ORDER BY istirakci DESC LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'sertifikasiya',
    açarSözler: ['sertifikasiya', 'imtahan', 'bal', 'nəticə'],
    izah: 'Sertifikasiya nəticələri',
    sql: `SELECT ad_soyad, bal::float8 AS bal, netice,
                 imtahan_tarixi::text AS tarix
            FROM tehsil.sertifikasiya
           ORDER BY bal DESC NULLS LAST LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'son_emrler',
    açarSözler: ['əmr', 'emr', 'sənəd', 'sened'],
    izah: 'Son əmrlər',
    sql: `SELECT emr_no, tarix::text AS tarix, movzu, imzalayan
            FROM sened.emrler ORDER BY tarix DESC LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'logistika',
    açarSözler: ['aktiv', 'avadanlıq', 'inventar', 'logistika', 'avadanliq'],
    izah: 'Logistika aktivləri',
    sql: `SELECT ad, tip, veziyyet, deyer::float8 AS deyer,
                 alinma_tarixi::text AS alinma
            FROM logistika.aktivler ORDER BY deyer DESC NULLS LAST LIMIT $1`,
    parametrli: true,
  },
];

/**
 * AI-a gonderilecek resept siyahisi (yalniz ADLAR ve IZAHLAR).
 *
 * DİQQƏT: bu, STATİK METOD DEYİL — MODUL SƏVİYYƏLİ funksiyadır.
 *
 * Sebeb: esbuild (vitest) dekorator transformu statik metodları
 * sinifden cixarir. Kompilyasiya olunmus kodda isleyir, testde ise
 * 'undefined' olur. Modul funksiyasi ise HER IKI halda isleyir.
 */
export function reseptSiyahisi(): { ad: string; izah: string }[] {
  return RESEPTLER.map((r) => ({ ad: r.ad, izah: r.izah }));
}

@Injectable()
export class SqlKomlekciService {
  private readonly log = new Logger('SQL-KOMEKCI');

  constructor(private readonly prisma: PrismaService) {}

  /** Sualdan resept secir */
  reseptSec(sual: string): Resept | null {
    const kicik = sual.toLowerCase();

    // 1) Birbasa resept adi cekilirse
    const adIle = RESEPTLER.find((r) => kicik.includes(r.ad));
    if (adIle) return adIle;

    // 2) Acar sözler uzre — en cox uygun gelen
    let enYaxsi: Resept | null = null;
    let enCox = 0;

    for (const r of RESEPTLER) {
      const uygun = r.açarSözler.filter((a) => kicik.includes(a)).length;
      if (uygun > enCox) {
        enCox = uygun;
        enYaxsi = r;
      }
    }

    return enCox > 0 ? enYaxsi : null;
  }

  /** Sualı icra edir */
  async icraEt(sual: string, limit = 20): Promise<SqlNetice> {
    const resept = this.reseptSec(sual);

    if (!resept) {
      throw new BadRequestException(
        `Bu sualı SQL-ə çevirə bilmədim: "${sual}". ` +
        `Mövcud mövzular: ${RESEPTLER.map((r) => r.ad).join(', ')}`,
      );
    }

    const baslama = Date.now();
    const setirler = resept.parametrli
      ? await this.prisma.$queryRawUnsafe<Record<string, unknown>[]>(resept.sql, limit)
      : await this.prisma.$queryRawUnsafe<Record<string, unknown>[]>(resept.sql);

    const icra = Date.now() - baslama;
    this.log.log(`"${sual.slice(0, 40)}" -> ${resept.ad} (${setirler.length} setir, ${icra}ms)`);

    return {
      sual,
      resept: resept.ad,
      izah: resept.izah,
      sql: resept.sql.replace(/\s+/g, ' ').trim(),
      setirler,
      setirSayi: setirler.length,
      icra_ms: icra,
    };
  }
}
