import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import request from 'supertest';
import { App } from 'supertest/types';
import { AppModule } from '../src/app.module.js';
import { AllExceptionsFilter } from '../src/common/filters/all-exceptions.filter.js';

/**
 * BACKEND-2 e2e testleri.
 * Butun HTTP qatini sinaqdan kecirir: validasiya, filtr, sehifeleme,
 * CRUD, xeta formatlari.
 */
describe('Backend-2 (e2e)', () => {
  let app: INestApplication<App>;

  beforeAll(async () => {
    const modul: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = modul.createNestApplication();

    // main.ts ile EYNI konfiqurasiya — eks halda test real davranisi yoxlamir
    app.setGlobalPrefix('api/v1');
    app.useGlobalPipes(
      new ValidationPipe({
        whitelist: true,
        forbidNonWhitelisted: true,
        transform: true,
      }),
    );
    app.useGlobalFilters(new AllExceptionsFilter());

    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  const url = (yol: string) => `/api/v1${yol}`;

  // ── SAĞLAMLIQ ──
  describe('Saglamliq', () => {
    it('prefikssiz yol 404 qaytarir', () =>
      request(app.getHttpServer()).get('/struktur/merkezler').expect(404));

    it('GET /api/v1/saglamliq baza veziyyetini verir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/saglamliq'))
        .expect(200);

      expect(c.body.status).toBe('saglam');
      expect(c.body.baza.qosulub).toBe(true);
      expect(c.body.baza.cedvel_sayi).toBe(48);
      expect(typeof c.body.baza.gecikme_ms).toBe('number');
    });

    it('GET /api/v1 kok melumat verir', async () => {
      const c = await request(app.getHttpServer()).get(url('')).expect(200);
      expect(c.body.prefiks).toBe('/api/v1');
    });
  });

  // ── STRUKTUR: OXUMA ──
  describe('GET /struktur/merkezler', () => {
    it('sehifelenmis siyahi qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/struktur/merkezler?limit=3'))
        .expect(200);

      expect(Array.isArray(c.body.data)).toBe(true);
      expect(c.body.data.length).toBeLessThanOrEqual(3);
      expect(c.body.meta).toMatchObject({
        sehife: 1,
        limit: 3,
      });
      expect(typeof c.body.meta.cem).toBe('number');
      expect(typeof c.body.meta.sehife_sayi).toBe('number');
    });

    it('axtaris isleyir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/struktur/merkezler?axtar=elmi'))
        .expect(200);
      expect(c.body.meta.cem).toBeGreaterThan(0);
      for (const r of c.body.data) {
        const metn = `${r.ad} ${r.unvan ?? ''} ${r.email ?? ''}`.toLowerCase();
        expect(metn).toContain('elmi');
      }
    });

    it('yanlis limit 400 verir', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler?limit=999'))
        .expect(400));

    it('sehife=0 400 verir', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler?sehife=0'))
        .expect(400));
  });

  describe('GET /struktur/merkezler/:id', () => {
    it('movcud id 200', () =>
      request(app.getHttpServer()).get(url('/struktur/merkezler/1')).expect(200));

    it('movcud olmayan id 404', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler/999999'))
        .expect(404));

    it('reqem olmayan id 400', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler/abc'))
        .expect(400));
  });

  // ── STRUKTUR: CRUD ──
  describe('CRUD /struktur/merkezler', () => {
    let yeniId: number;

    it('POST yeni merkez yaradir (201)', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: `E2E Test Merkezi ${Date.now()}`, tip: 'merkez' })
        .expect(201);

      expect(c.body.id).toBeGreaterThan(0);
      yeniId = c.body.id;
    });

    it('PATCH qismen yenileyir', async () => {
      const c = await request(app.getHttpServer())
        .patch(url(`/struktur/merkezler/${yeniId}`))
        .send({ telefon: '+994 12 000 11 22' })
        .expect(200);
      expect(c.body.telefon).toBe('+994 12 000 11 22');
    });

    it('eyni adla ikinci POST 409 verir', async () => {
      const c1 = await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: `Tekrar Test ${Date.now()}` })
        .expect(201);

      await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: c1.body.ad })
        .expect(409);

      await request(app.getHttpServer())
        .delete(url(`/struktur/merkezler/${c1.body.id}`))
        .expect(200);
    });

    it('qisa ad 400 verir', () =>
      request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: 'AB' })
        .expect(400));

    it('yanlis e-poct 400 verir', () =>
      request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: 'Test Merkez', email: 'sehv' })
        .expect(400));

    it('DTO-da olmayan sahe 400 verir (mass assignment qorumasi)', () =>
      request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: 'Test Merkez', rol: 'admin' })
        .expect(400));

    it('bagli shobesi olan merkez silinmir (409)', () =>
      request(app.getHttpServer())
        .delete(url('/struktur/merkezler/2'))
        .expect(409));

    it('DELETE yaradilmis merkezi silir', () =>
      request(app.getHttpServer())
        .delete(url(`/struktur/merkezler/${yeniId}`))
        .expect(200));
  });

  // ── KADRLAR ──
  describe('GET /kadrlar/emekdaslar', () => {
    it('tam profil qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar?limit=2'))
        .expect(200);

      const r = c.body.data[0];
      expect(r).toHaveProperty('tam_adi');
      expect(r).toHaveProperty('merkez');
      expect(r).toHaveProperty('vezife');
      expect(typeof r.maas === 'number' || r.maas === null).toBe(true);
    });

    it('merkez_id filtri isleyir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar?merkez_id=10'))
        .expect(200);
      expect(c.body.meta.cem).toBeGreaterThan(0);
    });

    it('maas araligi filtri isleyir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar?min_maas=2000&max_maas=3000'))
        .expect(200);
      for (const r of c.body.data) {
        expect(r.maas).toBeGreaterThanOrEqual(2000);
        expect(r.maas).toBeLessThanOrEqual(3000);
      }
    });

    it('siralama=desc isleyir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar?siralama=desc&siralama_sah=maas&limit=5'))
        .expect(200);
      const maaslar = c.body.data.map((r: { maas: number }) => r.maas);
      const siralanmis = [...maaslar].sort((a, b) => b - a);
      expect(maaslar).toEqual(siralanmis);
    });

    it('yanlis siralama sahesi 400 verir', () =>
      request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar?siralama_sah=DROP TABLE'))
        .expect(400));

    it('icmal qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar/icmal'))
        .expect(200);
      expect(c.body).toHaveProperty('umumi_fond');
      expect(Array.isArray(c.body.merkez_uzre)).toBe(true);
    });
  });

  // ── HESABATLAR ──
  describe('GET /hesabatlar', () => {
    it('icmal 48 cedvel ve 8 view gosterir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/hesabatlar/icmal'))
        .expect(200);
      expect(c.body.cedvel_sayi).toBe(48);
      expect(c.body.gorunus_sayi).toBe(8);
    });

    it('8 view siyahilayir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/hesabatlar/gorunusler'))
        .expect(200);
      expect(c.body).toHaveLength(8);
    });

    it('budce ROLLUP yekunu verir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/hesabatlar/budce-icmali'))
        .expect(200);
      const cem = c.body.find((r: { il: string }) => r.il === 'CƏMİ');
      expect(cem).toBeDefined();
      expect(cem.mebleg).toBeGreaterThan(0);
    });

    it('funksiyalar netice qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/hesabatlar/funksiyalar'))
        .expect(200);
      expect(typeof c.body.maas_fondu).toBe('number');
    });
  });

  // ── XƏTA FORMATI ──
  describe('Vahid xeta formati', () => {
    it('404 formati duzgundur', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/struktur/merkezler/999999'))
        .expect(404);

      expect(c.body).toMatchObject({
        ugur: false,
        xeta: { kod: 'TAPILMADI' },
      });
      expect(c.body).toHaveProperty('yol');
      expect(c.body).toHaveProperty('vaxt');
    });

    it('validasiya xetasi detallar massivi verir', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: 'AB', email: 'sehv' })
        .expect(400);

      expect(c.body.ugur).toBe(false);
      expect(c.body.xeta.kod).toBe('YANLIS_SORGU');
      expect(Array.isArray(c.body.xeta.detallar)).toBe(true);
      expect(c.body.xeta.detallar.length).toBeGreaterThanOrEqual(2);
    });
  });
});
