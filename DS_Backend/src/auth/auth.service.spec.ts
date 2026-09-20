import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ConflictException, UnauthorizedException } from '@nestjs/common';

/*
 * bcryptjs-i MOCK edirik: namespace dondurulmus oldugu ucun
 * vi.spyOn() onun metodlarini evez ede bilmir.
 * vi.mock ise modul yuklenende isleyir ve metodlari evez edir.
 */
vi.mock('bcryptjs', async () => {
  const real = await vi.importActual<typeof import('bcryptjs')>('bcryptjs');
  return {
    ...real,
    compare: vi.fn(real.compare),
    hash: vi.fn(real.hash),
  };
});

import * as bcrypt from 'bcryptjs';
import { AuthService } from './auth.service.js';

function saxtaPrisma() {
  return {
    $queryRaw: vi.fn(),
    $executeRaw: vi.fn(),
  } as any;
}

function saxtaJwt() {
  return { signAsync: vi.fn().mockResolvedValue('saxta.token.deyeri') } as any;
}

/** Real bcrypt hash-i — testde de real olsun */
const HASH_123456 = bcrypt.hashSync('123456', 4);   // test ucun az raund

describe('AuthService', () => {
  let prisma: any;
  let jwt: any;
  let service: AuthService;

  beforeEach(() => {
    prisma = saxtaPrisma();
    jwt = saxtaJwt();
    service = new AuthService(prisma, jwt);
  });

  // ── LOGIN ──
  describe('login()', () => {
    const setir = {
      id: 2, email: 'admin@arti.edu.az', parol_hash: HASH_123456,
      ad_soyad: 'Elnur Əliyev', rol: 'admin', emekdas_id: 1, aktiv: true,
    };

    it('duzgun sifre ile token qaytarir', async () => {
      prisma.$queryRaw.mockResolvedValue([setir]);

      const n = await service.login({ email: 'admin@arti.edu.az', parol: '123456' });

      expect(n.token).toBe('saxta.token.deyeri');
      expect(n.istifadeci.email).toBe('admin@arti.edu.az');
      expect(n.istifadeci.rol).toBe('admin');
    });

    it('cavabda parol_hash YOXDUR', async () => {
      prisma.$queryRaw.mockResolvedValue([setir]);

      const n = await service.login({ email: 'admin@arti.edu.az', parol: '123456' });

      expect(n.istifadeci).not.toHaveProperty('parol_hash');
      expect(JSON.stringify(n)).not.toContain('$2b$');
    });

    it('sehv sifre ile UnauthorizedException atir', async () => {
      prisma.$queryRaw.mockResolvedValue([setir]);
      await expect(service.login({ email: 'admin@arti.edu.az', parol: 'sehv' }))
        .rejects.toThrow(UnauthorizedException);
    });

    it('movcud olmayan email ile EYNI xeta mesajini verir', async () => {
      prisma.$queryRaw.mockResolvedValue([]);

      await expect(service.login({ email: 'yox@arti.edu.az', parol: '123456' }))
        .rejects.toThrow('E-poçt və ya şifrə yanlışdır');
    });

    it('movcud olmayan email ucun de bcrypt MUQAYISESI aparilir (timing attack)', async () => {
      prisma.$queryRaw.mockResolvedValue([]);
      vi.mocked(bcrypt.compare).mockClear();

      await service.login({ email: 'yox@arti.edu.az', parol: '123456' }).catch(() => null);

      // Istifadeci tapilmasa da muqayise APARILIR — cavab vaxti ferqlenmesin
      expect(bcrypt.compare).toHaveBeenCalledTimes(1);
      const [, hash] = vi.mocked(bcrypt.compare).mock.calls[0];
      expect(String(hash).startsWith('$2b$')).toBe(true);   // saxta hash de REALDIR
    });

    it('deaktiv istifadeci daxil ola bilmir', async () => {
      prisma.$queryRaw.mockResolvedValue([{ ...setir, aktiv: false }]);
      await expect(service.login({ email: 'admin@arti.edu.az', parol: '123456' }))
        .rejects.toThrow('İstifadəçi deaktiv edilib');
    });

    it('JWT payload icinde rol var', async () => {
      prisma.$queryRaw.mockResolvedValue([setir]);
      await service.login({ email: 'admin@arti.edu.az', parol: '123456' });

      const payload = jwt.signAsync.mock.calls[0][0];
      expect(payload).toMatchObject({ sub: 2, rol: 'admin' });
    });
  });

  // ── QEYDIYYAT ──
  describe('qeydiyyat()', () => {
    it('yeni istifadeci yaradir ve sifreyi HASH edir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([])                         // email yoxdur
        .mockResolvedValueOnce([{ id: 9, email: 'yeni@arti.edu.az',
          parol_hash: HASH_123456, ad_soyad: 'Yeni Adam',
          rol: 'baxici', emekdas_id: null, aktiv: true }]);

      const n = await service.qeydiyyat({
        email: 'yeni@arti.edu.az', parol: 'guclu-sifre-1',
        ad_soyad: 'Yeni Adam',
      });

      expect(n.id).toBe(9);
      expect(n).not.toHaveProperty('parol_hash');
    });

    it('INSERT-e duz METN sifre GETMIR — hash gedir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([])
        .mockResolvedValueOnce([{ id: 9, email: 'y@arti.edu.az', parol_hash: 'x',
          ad_soyad: 'Y', rol: 'baxici', emekdas_id: null, aktiv: true }]);

      await service.qeydiyyat({ email: 'y@arti.edu.az', parol: 'guclu-sifre-1', ad_soyad: 'Y' });

      // SQL parametrleri: [email, hash, ...]
      const arqumentler = prisma.$queryRaw.mock.calls[1];
      const duzMetnVar = arqumentler.some((a: unknown) => a === 'guclu-sifre-1');
      expect(duzMetnVar).toBe(false);
    });

    it('eyni email ile ConflictException atir', async () => {
      prisma.$queryRaw.mockResolvedValue([{ id: 2 }]);
      await expect(service.qeydiyyat({
        email: 'admin@arti.edu.az', parol: 'guclu-sifre-1', ad_soyad: 'X',
      })).rejects.toThrow(ConflictException);
    });

    it('movcud olmayan emekdas_id ile xeta atir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([])          // email yoxdur
        .mockResolvedValueOnce([]);         // emekdas yoxdur

      await expect(service.qeydiyyat({
        email: 'y@arti.edu.az', parol: 'guclu-sifre-1',
        ad_soyad: 'Y', emekdas_id: 9999,
      })).rejects.toThrow(ConflictException);
    });
  });

  // ── PAROL DEYISME ──
  describe('parolDeyis()', () => {
    it('kohne sifre duzdurse yenileyir', async () => {
      prisma.$queryRaw.mockResolvedValue([{
        id: 2, email: 'a@b.az', parol_hash: HASH_123456,
        ad_soyad: 'A', rol: 'admin', emekdas_id: null, aktiv: true,
      }]);
      prisma.$executeRaw.mockResolvedValue(1);

      const n = await service.parolDeyis(2, '123456', 'yeni-sifre-2026');
      expect(n.deyisdirildi).toBe(true);
      expect(prisma.$executeRaw).toHaveBeenCalledTimes(1);
    });

    it('kohne sifre sehvdirse xeta atir', async () => {
      prisma.$queryRaw.mockResolvedValue([{
        id: 2, email: 'a@b.az', parol_hash: HASH_123456,
        ad_soyad: 'A', rol: 'admin', emekdas_id: null, aktiv: true,
      }]);

      await expect(service.parolDeyis(2, 'sehv', 'yeni-sifre-2026'))
        .rejects.toThrow('Köhnə şifrə yanlışdır');
    });
  });
});
