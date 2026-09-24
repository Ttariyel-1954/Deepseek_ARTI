import { Test } from '@nestjs/testing';
import { SaglamliqService } from './saglamliq.service.js';
import { PrismaService } from '../prisma/prisma.service.js';

describe('SaglamliqService (unit)', () => {
  let servis: SaglamliqService;
  let prisma: { yoxla: ReturnType<typeof vi.fn> };

  beforeEach(async () => {
    prisma = { yoxla: vi.fn() };

    const modul = await Test.createTestingModule({
      providers: [
        SaglamliqService,
        { provide: PrismaService, useValue: prisma },
      ],
    }).compile();

    servis = modul.get(SaglamliqService);
  });

  it('baza cavab verəndə status "saglam" olur', async () => {
    prisma.yoxla.mockResolvedValue({ cedvelSayi: 48, gecikmeMs: 3 });

    const c = await servis.yoxla();

    expect(c.status).toBe('saglam');
    expect(c.baza.qosulub).toBe(true);
    expect(c.baza.cedvel_sayi).toBe(48);
    expect(c.baza.gecikme_ms).toBe(3);
  });

  it('cavabda ISO formatlı vaxt olur', async () => {
    prisma.yoxla.mockResolvedValue({ cedvelSayi: 48, gecikmeMs: 1 });

    const c = await servis.yoxla();

    expect(new Date(c.vaxt).toISOString()).toBe(c.vaxt);
  });

  it('baza xəta verəndə xəta YUXARI ötürülür (udulmur)', async () => {
    prisma.yoxla.mockRejectedValue(new Error('bağlantı yoxdur'));

    await expect(servis.yoxla()).rejects.toThrow('bağlantı yoxdur');
  });
});
