import { describe, it, expect, vi, beforeEach } from 'vitest';
import { StrukturService } from './struktur.service.js';
import { NotFoundException } from '@nestjs/common';

/**
 * Saxta Prisma — real bazaya toxunmuruq.
 * Hər test öz nəticəsini mockResolvedValue ilə təyin edir.
 */
function saxtaPrisma() {
  return { $queryRaw: vi.fn() } as any;
}

describe('StrukturService', () => {
  let prisma: any;
  let service: StrukturService;

  beforeEach(() => {
    prisma = saxtaPrisma();
    service = new StrukturService(prisma);
  });

  it('merkezler siyahisini qaytarir', async () => {
    prisma.$queryRaw.mockResolvedValue([
      { id: 1, ad: 'Elmi katiblik', aktiv: true },
    ]);

    const netice = await service.merkezler();

    expect(netice).toHaveLength(1);
    expect(netice[0].ad).toBe('Elmi katiblik');
  });

  it('tapilmayan merkez ucun 404 atir', async () => {
    // BOŞ nəticə — servis NotFoundException atmalıdır
    prisma.$queryRaw.mockResolvedValue([]);

    await expect(service.merkez(999)).rejects.toThrow(NotFoundException);
  });

  it('tapilan merkezi qaytarir', async () => {
    prisma.$queryRaw.mockResolvedValue([
      { id: 2, ad: 'Elmi-pedaqoji tedqiqatlar merkezi', aktiv: true },
    ]);

    const netice = await service.merkez(2);

    expect(netice.id).toBe(2);
  });

  it('SQL-e parametr oturur (SQL injection qorumasi)', async () => {
    prisma.$queryRaw.mockResolvedValue([]);
    await service.merkez(5).catch(() => null);

    const cagiris = prisma.$queryRaw.mock.calls[0];
    // Prisma template literal: (strings, ...parametrler)
    expect(cagiris.length).toBeGreaterThan(1);
    expect(cagiris[1]).toBe(5);
  });
});
