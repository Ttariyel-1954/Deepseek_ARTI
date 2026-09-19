import { describe, it, expect, vi, beforeEach } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import { StrukturService } from './struktur.service.js';
import { MerkezFiltrDto } from './dto/merkez-filtr.dto.js';

/** Saxta Prisma — real bazaya toxunmuruq */
function saxtaPrisma() {
  return {
    $queryRaw: vi.fn(),
    $queryRawUnsafe: vi.fn(),
    $executeRaw: vi.fn(),
  } as any;
}

function filtr(qismen: Partial<MerkezFiltrDto> = {}): MerkezFiltrDto {
  return Object.assign(new MerkezFiltrDto(), qismen);
}

describe('StrukturService', () => {
  let prisma: any;
  let service: StrukturService;

  beforeEach(() => {
    prisma = saxtaPrisma();
    service = new StrukturService(prisma);
  });

  // ── OXUMA ──
  describe('merkezler()', () => {
    it('sehifelenmis netice qaytarir', async () => {
      prisma.$queryRawUnsafe
        .mockResolvedValueOnce([{ id: 1, ad: 'Elmi katiblik', aktiv: true }])
        .mockResolvedValueOnce([{ cem: 10 }]);

      const n = await service.merkezler(filtr({ limit: 3 }));

      expect(n.data).toHaveLength(1);
      expect(n.meta).toEqual({ sehife: 1, limit: 3, cem: 10, sehife_sayi: 4 });
    });

    it('sehife_sayi sifir olanda 1 qaytarir', async () => {
      prisma.$queryRawUnsafe.mockResolvedValueOnce([]).mockResolvedValueOnce([{ cem: 0 }]);
      const n = await service.merkezler(filtr());
      expect(n.meta.sehife_sayi).toBe(1);
      expect(n.meta.cem).toBe(0);
    });

    it('offset duzgun hesablanir', async () => {
      const f = filtr({ sehife: 3, limit: 20 });
      expect(f.offset).toBe(40);
    });
  });

  describe('merkez()', () => {
    it('movcud merkezi qaytarir', async () => {
      prisma.$queryRaw.mockResolvedValue([{ id: 2, ad: 'Test', aktiv: true }]);
      const m = await service.merkez(2);
      expect(m.id).toBe(2);
    });

    it('tapilmayanda NotFoundException atir', async () => {
      prisma.$queryRaw.mockResolvedValue([]);
      await expect(service.merkez(999)).rejects.toThrow(NotFoundException);
    });
  });

  // ── YAZMA ──
  describe('yarat()', () => {
    it('ad yoxlamasindan sonra yaradir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([])                                   // ad yoxdur
        .mockResolvedValueOnce([{ id: 11, ad: 'Yeni Merkez', aktiv: true }]);

      const m = await service.yarat({ ad: 'Yeni Merkez' });
      expect(m.id).toBe(11);
    });

    it('eyni ad varsa ConflictException atir', async () => {
      prisma.$queryRaw.mockResolvedValue([{ id: 1 }]);

      await expect(service.yarat({ ad: 'Elmi katiblik' }))
        .rejects.toThrow(ConflictException);
    });
  });

  describe('yenile()', () => {
    it('movcud merkezi yenileyir', async () => {
      // yenile() UC sorgu isledir:
      //   1) merkez(id)  2) adYoxla()  3) UPDATE
      prisma.$queryRaw
        .mockResolvedValueOnce([{ id: 5, ad: 'Kohne ad', aktiv: true }])
        .mockResolvedValueOnce([])                                  // ad konflikti yox
        .mockResolvedValueOnce([{ id: 5, ad: 'Yeni ad', aktiv: true }]);

      const m = await service.yenile(5, { ad: 'Yeni ad' });
      expect(m.ad).toBe('Yeni ad');
      expect(prisma.$queryRaw).toHaveBeenCalledTimes(3);
    });

    it('yeni ad basqasinda varsa ConflictException', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([{ id: 5, ad: 'Kohne ad', aktiv: true }])
        .mockResolvedValueOnce([{ id: 8 }]);                        // ad tutulub

      await expect(service.yenile(5, { ad: 'Elmi katiblik' }))
        .rejects.toThrow(ConflictException);
    });

    it('ad deyismirse konflikt yoxlamasi kecirilir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([{ id: 5, ad: 'Eyni ad', aktiv: true }])
        .mockResolvedValueOnce([{ id: 5, ad: 'Eyni ad', aktiv: true }]);

      const m = await service.yenile(5, { ad: 'Eyni ad' });
      expect(m.ad).toBe('Eyni ad');
      expect(prisma.$queryRaw).toHaveBeenCalledTimes(2);   // adYoxla cagirilmadi
    });

    it('movcud olmayan id ucun NotFoundException', async () => {
      prisma.$queryRaw.mockResolvedValue([]);
      await expect(service.yenile(999, { ad: 'X' }))
        .rejects.toThrow(NotFoundException);
    });
  });

  describe('sil()', () => {
    it('bagli shobe varsa ConflictException', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([{ id: 2, ad: 'Test', aktiv: true }])  // merkez var
        .mockResolvedValueOnce([{ say: 7 }]);                          // 7 shobe bagli

      await expect(service.sil(2)).rejects.toThrow(ConflictException);
      expect(prisma.$executeRaw).not.toHaveBeenCalled();
    });

    it('bagli shobe yoxdursa silir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([{ id: 9, ad: 'Test', aktiv: true }])
        .mockResolvedValueOnce([{ say: 0 }]);
      prisma.$executeRaw.mockResolvedValue(1);

      const n = await service.sil(9);
      expect(n).toEqual({ silindi: true, id: 9 });
      expect(prisma.$executeRaw).toHaveBeenCalledTimes(1);
    });
  });

  // ── SQL INJECTION ──
  describe('siralama — SQL injection qorumasi', () => {
    it('icazeli sutun kecir', async () => {
      prisma.$queryRawUnsafe.mockResolvedValue([]);
      await expect(service.merkezler(filtr({ siralama_sah: 'ad' })))
        .resolves.toBeDefined();
    });

    it('icazesiz sutun BadRequestException atir', async () => {
      await expect(service.merkezler(filtr({ siralama_sah: 'DROP TABLE' })))
        .rejects.toThrow(BadRequestException);
      expect(prisma.$queryRawUnsafe).not.toHaveBeenCalled();
    });

    it('SQL fragment sizişi bloklanir', async () => {
      for (const hucum of ['ad; DROP TABLE', '1=1 --', 'ad) UNION SELECT']) {
        await expect(service.merkezler(filtr({ siralama_sah: hucum })))
          .rejects.toThrow(BadRequestException);
      }
    });
  });

  describe('merkezStatistikasi()', () => {
    it('merkez, shobe ve emekdas sayini qaytarir', async () => {
      prisma.$queryRaw.mockResolvedValue([
        { merkez: 'Elmi katiblik', shobe_sayi: 2, emekdas_sayi: 3 },
      ]);
      const n = await service.merkezStatistikasi();
      expect(n[0].shobe_sayi).toBe(2);
      expect(n[0].emekdas_sayi).toBe(3);
    });
  });
});
