import { describe, it, expect, vi, beforeEach } from 'vitest';
import { RagService } from './rag.service.js';

function saxtaPrisma() {
  return { $queryRaw: vi.fn(), $executeRaw: vi.fn() } as any;
}

describe('RagService', () => {
  let prisma: any;
  let rag: RagService;

  beforeEach(() => {
    prisma = saxtaPrisma();
    rag = new RagService(prisma);
  });

  // ── VEKTORLASDIRMA ──
  describe('vektorlastir()', () => {
    it('duzgun olcude vektor qaytarir', () => {
      const v = rag.vektorlastir('kurikulum islahatı');
      expect(v).toHaveLength(RagService.OLCU);
    });

    it('vektor vahid uzunluga getirilir (norm = 1)', () => {
      const v = rag.vektorlastir('tehsil sistemi ve kurikulum');
      const uzunluq = Math.sqrt(v.reduce((c, x) => c + x * x, 0));
      expect(uzunluq).toBeCloseTo(1, 4);
    });

    it('eyni metn -> EYNI vektor (deterministik)', () => {
      const a = rag.vektorlastir('informatika telimi');
      const b = rag.vektorlastir('informatika telimi');
      expect(a).toEqual(b);
    });

    it('ferqli metn -> FERQLI vektor', () => {
      const a = rag.vektorlastir('kurikulum islahatı');
      const b = rag.vektorlastir('maliyye hesabati');
      expect(a).not.toEqual(b);
    });

    it('bos metn ucun sifir vektor', () => {
      const v = rag.vektorlastir('');
      expect(v.every((x) => x === 0)).toBe(true);
    });
  });

  // ── KOSINUS OXSARLIGI ──
  describe('oxsarliq()', () => {
    it('eyni vektor -> 1.0', () => {
      const v = rag.vektorlastir('kurikulum');
      expect(rag.oxsarliq(v, v)).toBeCloseTo(1, 5);
    });

    it('sifir vektor -> 0 (sifira bolme yoxdur)', () => {
      const sifir = new Array(RagService.OLCU).fill(0);
      const v = rag.vektorlastir('test');
      expect(rag.oxsarliq(sifir, v)).toBe(0);
      expect(rag.oxsarliq(sifir, sifir)).toBe(0);
    });

    it('ferqli olculu vektor -> 0', () => {
      expect(rag.oxsarliq([1, 2], [1, 2, 3])).toBe(0);
    });

    it('oxsar metnler yuksek bal alir', () => {
      const a = rag.vektorlastir('kurikulum islahatı tehsil');
      const b = rag.vektorlastir('kurikulum islahatı telim');
      const c = rag.vektorlastir('maliyye budce xerci');

      const yaxin = rag.oxsarliq(a, b);
      const uzaq = rag.oxsarliq(a, c);

      expect(yaxin).toBeGreaterThan(uzaq);
    });

    it('bal 0 ile 1 arasindadir', () => {
      const a = rag.vektorlastir('tehsil');
      const b = rag.vektorlastir('kurikulum');
      const bal = rag.oxsarliq(a, b);
      expect(bal).toBeGreaterThanOrEqual(0);
      expect(bal).toBeLessThanOrEqual(1);
    });
  });

  // ── OXSAR TAP ──
  describe('oxsarTap()', () => {
    it('neticeleri oxsarliq uzre azalan siralayir', async () => {
      prisma.$queryRaw.mockResolvedValue([
        { id: 1, cedvel_adi: 'a', sened_id: 1, metn: 'kurikulum islahatı tehsil', vektor: null },
        { id: 2, cedvel_adi: 'b', sened_id: 2, metn: 'maliyye budce hesabati', vektor: null },
        { id: 3, cedvel_adi: 'c', sened_id: 3, metn: 'kurikulum islahatı telim', vektor: null },
      ]);

      const n = await rag.oxsarTap('kurikulum', 3, 0.01);

      expect(n.length).toBeGreaterThan(1);
      for (let i = 1; i < n.length; i++) {
        expect(n[i - 1].oxsarliq).toBeGreaterThanOrEqual(n[i].oxsarliq);
      }
    });

    it('limit-e riayet edir', async () => {
      prisma.$queryRaw.mockResolvedValue(
        Array.from({ length: 10 }, (_, i) => ({
          id: i + 1, cedvel_adi: 'x', sened_id: i + 1,
          metn: `kurikulum sened ${i}`, vektor: null,
        })),
      );

      const n = await rag.oxsarTap('kurikulum', 3, 0.01);
      expect(n).toHaveLength(3);
    });

    it('minOxsarliq-dan asagi neticeleri suzur', async () => {
      prisma.$queryRaw.mockResolvedValue([
        { id: 1, cedvel_adi: 'a', sened_id: 1, metn: 'tamamilə fərqli mövzu', vektor: null },
      ]);

      const n = await rag.oxsarTap('kurikulum', 5, 0.9);
      expect(n).toHaveLength(0);
    });

    it('saxlanilan vektor varsa onu isledir', async () => {
      const hazir = rag.vektorlastir('kurikulum islahatı');
      prisma.$queryRaw.mockResolvedValue([
        { id: 1, cedvel_adi: 'a', sened_id: 1, metn: 'metn', vektor: hazir },
      ]);

      const n = await rag.oxsarTap('kurikulum islahatı', 1, 0.01);
      expect(n).toHaveLength(1);
      expect(n[0].oxsarliq).toBeCloseTo(1, 4);
    });
  });

  // ── INDEKSLEME ──
  describe('indeksle()', () => {
    it('butun senedleri vektorlashdirir', async () => {
      prisma.$queryRaw.mockResolvedValue([
        { id: 1, metn: 'birinci sened' },
        { id: 2, metn: 'ikinci sened' },
      ]);
      prisma.$executeRaw.mockResolvedValue(1);

      const n = await rag.indeksle();

      expect(n.indekslendi).toBe(2);
      expect(prisma.$executeRaw).toHaveBeenCalledTimes(2);
    });

    it('metn NULL olanlari kecir', async () => {
      prisma.$queryRaw.mockResolvedValue([{ id: 1, metn: 'sened' }]);
      prisma.$executeRaw.mockResolvedValue(1);

      const n = await rag.indeksle();
      expect(n.indekslendi).toBe(1);
    });
  });
});
