import { describe, it, expect } from 'vitest';
import { plainToInstance } from 'class-transformer';
import { validate } from 'class-validator';
import { SehifeDto } from './sehife.dto.js';

/** DTO validasiyasini birbasa yoxlayiriq (HTTP olmadan) */
async function yoxla(xam: Record<string, unknown>) {
  const dto = plainToInstance(SehifeDto, xam);
  return validate(dto);
}

describe('SehifeDto', () => {
  it('bos obyekt ucun susmaya gore deyerler', () => {
    const dto = new SehifeDto();
    expect(dto.sehife).toBe(1);
    expect(dto.limit).toBe(20);
    expect(dto.siralama).toBe('asc');
    expect(dto.offset).toBe(0);
  });

  it('sehife=3, limit=20 -> offset 40', () => {
    const dto = Object.assign(new SehifeDto(), { sehife: 3, limit: 20 });
    expect(dto.offset).toBe(40);
  });

  it('sehife=0-etibarsizdir', async () => {
    const xetalar = await yoxla({ sehife: 0 });
    expect(xetalar.length).toBeGreaterThan(0);
    expect(Object.keys(xetalar[0].constraints ?? {})).toContain('min');
  });

  it('limit=101-etibarsizdir', async () => {
    const xetalar = await yoxla({ limit: 101 });
    expect(xetalar.length).toBeGreaterThan(0);
  });

  it('limit=100-etibarlidir', async () => {
    expect(await yoxla({ limit: 100 })).toHaveLength(0);
  });

  it('siralama=asc/desc etibarlidir', async () => {
    expect(await yoxla({ siralama: 'asc' })).toHaveLength(0);
    expect(await yoxla({ siralama: 'desc' })).toHaveLength(0);
  });

  it('siralama=xyz etibarsizdir', async () => {
    const xetalar = await yoxla({ siralama: 'xyz' });
    expect(xetalar.length).toBeGreaterThan(0);
    expect(Object.keys(xetalar[0].constraints ?? {})).toContain('isIn');
  });

  it('axtar 100 simvoldan uzun ola bilmez', async () => {
    const xetalar = await yoxla({ axtar: 'a'.repeat(101) });
    expect(xetalar.length).toBeGreaterThan(0);
  });
});
