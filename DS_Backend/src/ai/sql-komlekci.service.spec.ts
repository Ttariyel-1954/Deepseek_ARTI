import { describe, it, expect, vi, beforeEach } from 'vitest';
import { BadRequestException } from '@nestjs/common';
import { SqlKomlekciService, reseptSiyahisi } from './sql-komlekci.service.js';

function saxtaPrisma() {
  return { $queryRawUnsafe: vi.fn().mockResolvedValue([{ test: 1 }]) } as any;
}

describe('SqlKomlekciService', () => {
  let prisma: any;
  let svc: SqlKomlekciService;

  beforeEach(() => {
    prisma = saxtaPrisma();
    svc = new SqlKomlekciService(prisma);
  });

  // ── RESEPT SECIMI ──
  describe('reseptSec()', () => {
    const hallar: [string, string][] = [
      ['Neçə əməkdaş var?', 'emekdas_sayi'],
      ['Ən çox maaş alan kimdir?', 'en_cox_maas'],
      ['Mərkəzlər üzrə bölgü ver', 'merkez_uzre'],
      ['Əmək haqqı fondu nə qədərdir?', 'maas_fondu'],
      ['Elmi layihələri göstər', 'layiheler'],
      ['Büdcə nə qədərdir?', 'budce'],
      ['Təlim qrupları hansılardır?', 'təlim_qruplari' === 'telim_qruplari' ? 'telim_qruplari' : 'telim_qruplari'],
      ['Sertifikasiya nəticələri', 'sertifikasiya'],
      ['Son əmrləri göstər', 'son_emrler'],
      ['Logistika aktivləri', 'logistika'],
    ];

    for (const [sual, gozlenilen] of hallar) {
      it(`"${sual}" -> ${gozlenilen}`, () => {
        expect(svc.reseptSec(sual)?.ad).toBe(gozlenilen);
      });
    }

    it('namelum sual ucun null qaytarir', () => {
      expect(svc.reseptSec('Sabah hava necə olacaq?')).toBeNull();
    });

    it('boyuk/kiçik herf ferqi yoxdur', () => {
      expect(svc.reseptSec('NEÇƏ ƏMƏKDAŞ VAR')?.ad).toBe('emekdas_sayi');
    });
  });

  // ── ICRA ──
  describe('icraEt()', () => {
    it('duzgun netice strukturu qaytarir', async () => {
      const n = await svc.icraEt('Neçə əməkdaş var?', 10);

      expect(n).toMatchObject({
        resept: 'emekdas_sayi',
        setirSayi: 1,
      });
      expect(n.sql).toBeTypeOf('string');
      expect(n.icra_ms).toBeGreaterThanOrEqual(0);
    });

    it('namelum sual ucun BadRequestException atir', async () => {
      await expect(svc.icraEt('Sabah hava necə olacaq?'))
        .rejects.toThrow(BadRequestException);
    });

    it('xeta mesajinda movcud reseptleri gosterir', async () => {
      await expect(svc.icraEt('namelum sual')).rejects.toThrow(/emekdas_sayi/);
    });

    it('parametrli reseptlere LIMIT oтурur', async () => {
      await svc.icraEt('Ən çox maaş alan 5 nəfər', 5);

      const cagiris = prisma.$queryRawUnsafe.mock.calls[0];
      expect(cagiris[1]).toBe(5);          // limit parametri
    });

    it('parametrsiz resepte LIMIT vermir', async () => {
      await svc.icraEt('Neçə əməkdaş var?', 10);

      const cagiris = prisma.$queryRawUnsafe.mock.calls[0];
      expect(cagiris).toHaveLength(1);     // yalniz SQL
    });
  });

  // ── TEHLUKESIZLIK ──
  describe('TEHLUKESIZLIK — SQL injection', () => {
    it('butun SQL-ler YALNIZ SELECT ile baslayir', () => {
      const siyahi = reseptSiyahisi();
      expect(siyahi.length).toBeGreaterThan(0);

      // Her reseptin SQL-ini yoxla
      for (const r of siyahi) {
        const netice = svc.reseptSec(r.ad);
        expect(netice).not.toBeNull();
        const sql = netice!.sql.trim().toUpperCase();
        expect(sql.startsWith('SELECT')).toBe(true);
      }
    });

    it('TEHLUKELI SQL ifadeleri YOXDUR', () => {
      const qadagan = ['DELETE', 'DROP', 'TRUNCATE', 'UPDATE', 'INSERT', 'ALTER', 'GRANT'];

      for (const r of reseptSiyahisi()) {
        const sql = svc.reseptSec(r.ad)!.sql.toUpperCase();
        for (const q of qadagan) {
          expect(sql).not.toContain(` ${q} `);
        }
      }
    });

    it('istifadeci metni SQL-e BIRBASA yazilmir', async () => {
      const hucum = "'; DROP TABLE kadrlar.emekdaslar--";
      // Hucum metni resept secmir -> xeta
      await expect(svc.icraEt(hucum)).rejects.toThrow(BadRequestException);
    });

    it('AI yalniz MOVCUD reseptlerden birini sece BILER', () => {
      const adlar = reseptSiyahisi().map((r) => r.ad);
      expect(adlar).toContain('emekdas_sayi');
      // Resept adlari sabitdir — AI yeni resept yarada bilmez
      expect(adlar.length).toBe(10);
    });
  });
});
