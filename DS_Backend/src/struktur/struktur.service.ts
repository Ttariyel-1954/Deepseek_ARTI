import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

/** Bazadan gelen setir — TypeScript tipi */
export interface Merkez {
  id: number;
  ad: string;
  tip: string | null;
  unvan: string | null;
  telefon: string | null;
  email: string | null;
  aktiv: boolean;
}

@Injectable()
export class StrukturService {
  constructor(private readonly prisma: PrismaService) {}

  /** Butun merkezler */
  async merkezler(): Promise<Merkez[]> {
    return this.prisma.$queryRaw<Merkez[]>`
      SELECT id::int, ad, tip, unvan, telefon, email, aktiv
      FROM struktur.merkezler
      ORDER BY id
    `;
  }

  /** Bir merkez — tapilmasa 404 */
  async merkez(id: number): Promise<Merkez> {
    const setirler = await this.prisma.$queryRaw<Merkez[]>`
      SELECT id::int, ad, tip, unvan, telefon, email, aktiv
      FROM struktur.merkezler
      WHERE id = ${id}
    `;
    if (!setirler.length) {
      throw new NotFoundException(`Merkez tapilmadi: id=${id}`);
    }
    return setirler[0];
  }

  /** Merkez uzre shobe sayi */
  async merkezStatistikasi() {
    return this.prisma.$queryRaw<
      { merkez: string; shobe_sayi: number }[]
    >`
      SELECT m.ad AS merkez, count(s.id)::int AS shobe_sayi
      FROM struktur.merkezler m
      LEFT JOIN struktur.shobeler s ON s.merkez_id = m.id
      GROUP BY m.ad
      ORDER BY shobe_sayi DESC
    `;
  }
}
