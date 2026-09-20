import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

/** Vektor — JSONB-da saxlanilan eded massivi */
export type Vektor = number[];

export interface OxsarNetice {
  id: number;
  cedvel_adi: string;
  sened_id: number | null;
  metn: string;
  oxsarliq: number;
}

/**
 * RAG — Retrieval Augmented Generation.
 *
 * pgvector QURULMADIGI ucun oxsarliq TETBIQ QATINDA hesablanir:
 *   1. Sual vektora cevrilir
 *   2. Her sened ucun kosinus oxsarliği hesablanir
 *   3. En yaxin N sened secilir
 *
 * Bu, 10 000 senede qeder tamamilə kifayetdir.
 * Daha boyuk hecmde pgvector-e kecin (aşaği bax).
 */
@Injectable()
export class RagService {
  private readonly log = new Logger('RAG');

  /** Vektorun olcusu — butun embeddingler eyni olmali */
  static readonly OLCU = 64;

  constructor(private readonly prisma: PrismaService) {}

  /**
   * METN -> VEKTOR (deterministik hash embedding).
   *
   * Qeyd: bu, HEQIQI semantik embedding DEYIL. Sözləri hash ile
   * vektora cevirir — eyni sözler eyni mövqelere düşür.
   *
   * Real sistemde DeepSeek/OpenAI embedding API-si işledilir:
   *   POST /v1/embeddings  { input: "...", model: "..." }
   */
  vektorlastir(metn: string): Vektor {
    const vektor = new Array(RagService.OLCU).fill(0);
    const sozler = metn
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\s]/gu, ' ')
      .split(/\s+/)
      .filter((s) => s.length > 1);

    for (const soz of sozler) {
      // Iki musteqil hash — bir soz iki mövqeye töhfə verir
      const h1 = this.hash(soz, 0) % RagService.OLCU;
      const h2 = this.hash(soz, 1) % RagService.OLCU;
      vektor[h1] += 1;
      vektor[h2] += 0.5;
    }

    return this.normallashdir(vektor);
  }

  /** Kosinus oxsarliği — iki vektor arasindaki bucaq */
  oxsarliq(a: Vektor, b: Vektor): number {
    if (a.length !== b.length) return 0;

    let nokta = 0;
    let normA = 0;
    let normB = 0;

    for (let i = 0; i < a.length; i++) {
      nokta += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }

    const mexrec = Math.sqrt(normA) * Math.sqrt(normB);
    return mexrec === 0 ? 0 : nokta / mexrec;
  }

  /** Oxsar senedleri tap */
  async oxsarTap(sual: string, limit = 5, minOxsarliq = 0.1): Promise<OxsarNetice[]> {
    const sualVektoru = this.vektorlastir(sual);

    const setirler = await this.prisma.$queryRaw<
      { id: number; cedvel_adi: string; sened_id: number | null; metn: string | null; vektor: Vektor | null }[]
    >`
      SELECT id::int, cedvel_adi, sened_id, metn, vektor
        FROM ai.embeddingler
       WHERE metn IS NOT NULL`;

    const neticeler: OxsarNetice[] = [];

    for (const s of setirler) {
      // Vektor yoxdursa — yerinde hesabla (kowhnə setirler ucun)
      const v = Array.isArray(s.vektor) && s.vektor.length === RagService.OLCU
        ? s.vektor
        : this.vektorlastir(s.metn ?? '');

      const oxsarliq = this.oxsarliq(sualVektoru, v);
      if (oxsarliq >= minOxsarliq) {
        neticeler.push({
          id: s.id,
          cedvel_adi: s.cedvel_adi,
          sened_id: s.sened_id,
          metn: s.metn ?? '',
          oxsarliq: Number(oxsarliq.toFixed(4)),
        });
      }
    }

    neticeler.sort((a, b) => b.oxsarliq - a.oxsarliq);
    this.log.log(`"${sual.slice(0, 40)}" -> ${neticeler.length} netice`);
    return neticeler.slice(0, limit);
  }

  /** Butun senedleri vektorlashdir (bir defe isledilir) */
  async indeksle(): Promise<{ indekslendi: number }> {
    const setirler = await this.prisma.$queryRaw<
      { id: number; metn: string | null }[]
    >`SELECT id::int, metn FROM ai.embeddingler WHERE metn IS NOT NULL`;

    let say = 0;
    for (const s of setirler) {
      const vektor = this.vektorlastir(s.metn ?? '');
      await this.prisma.$executeRaw`
        UPDATE ai.embeddingler SET vektor = ${JSON.stringify(vektor)}::jsonb
         WHERE id = ${s.id}`;
      say++;
    }

    this.log.log(`${say} sened vektorlashdirildi`);
    return { indekslendi: say };
  }

  /** Vahid uzunluga getir — kosinusu sürətləndirir */
  private normallashdir(v: Vektor): Vektor {
    const uzunluq = Math.sqrt(v.reduce((c, x) => c + x * x, 0));
    return uzunluq === 0 ? v : v.map((x) => Number((x / uzunluq).toFixed(6)));
  }

  /** Sadə deterministik hash (FNV-1a) */
  private hash(soz: string, duz: number): number {
    let h = 2166136261 ^ duz;
    for (let i = 0; i < soz.length; i++) {
      h ^= soz.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return Math.abs(h);
  }
}
