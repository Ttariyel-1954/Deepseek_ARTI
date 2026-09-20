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
  let token = '';

  /*
   * BACKEND-3 QEYDI:
   * Backend-3 qlobal JwtAuthGuard elave edir — butun endpoint-ler qorunur.
   * Ona gore bu testler artik TOKEN gondermelidir, eks halda 401 alirlar.
   */
  const api = () => request(app.getHttpServer());
  const publicApi = () => request(app.getHttpServer());

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

    // Admin tokeni al
    const girish = await publicApi()
      .post('/api/v1/auth/login').set('Authorization', `Bearer ${token}`)
      .send({ email: 'admin@arti.edu.az', parol: '123456' });

    token = girish.body?.token ?? '';
    expect(token).toBeTruthy();
  });

  afterAll(async () => {
    await app.close();
  });

  const url = (yol: string) => `/api/v1${yol}`;

  // ── SAĞLAMLIQ ──
  describe('Saglamliq', () => {
    it('prefikssiz yol 404 qaytarir', () =>
      publicApi().get('/struktur/merkezler').expect(404));

    it('GET /api/v1/saglamliq baza veziyyetini verir', async () => {
      const c = await api()
        .get(url('/saglamliq')).set('Authorization', `Bearer ${token}`)
        .expect(200);

      expect(c.body.status).toBe('saglam');
      expect(c.body.baza.qosulub).toBe(true);
      expect(c.body.baza.cedvel_sayi).toBe(48);
      expect(typeof c.body.baza.gecikme_ms).toBe('number');
    });

    it('GET /api/v1 kok melumat verir', async () => {
      const c = await api().get(url('')).set('Authorization', `Bearer ${token}`).expect(200);
      expect(c.body.prefiks).toBe('/api/v1');
    });
  });

  // ── STRUKTUR: OXUMA ──
  describe('GET /struktur/merkezler', () => {
    it('sehifelenmis siyahi qaytarir', async () => {
      const c = await api()
        .get(url('/struktur/merkezler?limit=3')).set('Authorization', `Bearer ${token}`)
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
      const c = await api()
        .get(url('/struktur/merkezler?axtar=elmi')).set('Authorization', `Bearer ${token}`)
        .expect(200);
      expect(c.body.meta.cem).toBeGreaterThan(0);
      for (const r of c.body.data) {
        const metn = `${r.ad} ${r.unvan ?? ''} ${r.email ?? ''}`.toLowerCase();
        expect(metn).toContain('elmi');
      }
    });

    it('yanlis limit 400 verir', () =>
      api()
        .get(url('/struktur/merkezler?limit=999')).set('Authorization', `Bearer ${token}`)
        .expect(400));

    it('sehife=0 400 verir', () =>
      api()
        .get(url('/struktur/merkezler?sehife=0')).set('Authorization', `Bearer ${token}`)
        .expect(400));
  });

  describe('GET /struktur/merkezler/:id', () => {
    it('movcud id 200', () =>
      api().get(url('/struktur/merkezler/1')).set('Authorization', `Bearer ${token}`).expect(200));

    it('movcud olmayan id 404', () =>
      api()
        .get(url('/struktur/merkezler/999999')).set('Authorization', `Bearer ${token}`)
        .expect(404));

    it('reqem olmayan id 400', () =>
      api()
        .get(url('/struktur/merkezler/abc')).set('Authorization', `Bearer ${token}`)
        .expect(400));
  });

  // ── STRUKTUR: CRUD ──
  describe('CRUD /struktur/merkezler', () => {
    let yeniId: number;

    it('POST yeni merkez yaradir (201)', async () => {
      const c = await api()
        .post(url('/struktur/merkezler')).set('Authorization', `Bearer ${token}`)
        .send({ ad: `E2E Test Merkezi ${Date.now()}`, tip: 'merkez' })
        .expect(201);

      expect(c.body.id).toBeGreaterThan(0);
      yeniId = c.body.id;
    });

    it('PATCH qismen yenileyir', async () => {
      const c = await api()
        .patch(url(`/struktur/merkezler/${yeniId}`)).set('Authorization', `Bearer ${token}`)
        .send({ telefon: '+994 12 000 11 22' })
        .expect(200);
      expect(c.body.telefon).toBe('+994 12 000 11 22');
    });

    it('eyni adla ikinci POST 409 verir', async () => {
      const c1 = await api()
        .post(url('/struktur/merkezler')).set('Authorization', `Bearer ${token}`)
        .send({ ad: `Tekrar Test ${Date.now()}` })
        .expect(201);

      await api()
        .post(url('/struktur/merkezler')).set('Authorization', `Bearer ${token}`)
        .send({ ad: c1.body.ad })
        .expect(409);

      await api()
        .delete(url(`/struktur/merkezler/${c1.body.id}`)).set('Authorization', `Bearer ${token}`)
        .expect(200);
    });

    it('qisa ad 400 verir', () =>
      api()
        .post(url('/struktur/merkezler')).set('Authorization', `Bearer ${token}`)
        .send({ ad: 'AB' })
        .expect(400));

    it('yanlis e-poct 400 verir', () =>
      api()
        .post(url('/struktur/merkezler')).set('Authorization', `Bearer ${token}`)
        .send({ ad: 'Test Merkez', email: 'sehv' })
        .expect(400));

    it('DTO-da olmayan sahe 400 verir (mass assignment qorumasi)', () =>
      api()
        .post(url('/struktur/merkezler')).set('Authorization', `Bearer ${token}`)
        .send({ ad: 'Test Merkez', rol: 'admin' })
        .expect(400));

    it('bagli shobesi olan merkez silinmir (409)', () =>
      api()
        .delete(url('/struktur/merkezler/2')).set('Authorization', `Bearer ${token}`)
        .expect(409));

    it('bagli EMEKDASI olan merkez de silinmir (409, 500 DEYIL)', async () => {
      /*
       * REAL XETA (reqressiya testi):
       * merkezler-e UC cedvel baglidir — shobeler, emekdaslar, rehberlik.
       * Evvelce yalniz shobeler yoxlanilirdi; digerleri FK pozuntusu
       * verirdi ve istifadeci 500 xetasi gorurdu.
       */
      const c = await api()
        .delete(url('/struktur/merkezler/1')).set('Authorization', `Bearer ${token}`)
        .expect(409);

      expect(c.body.xeta.kod).toBe('TOQQUSMA');
      expect(c.body.xeta.mesaj).toMatch(/bagli melumat var/);
    });

    it('DELETE yaradilmis merkezi silir', () =>
      api()
        .delete(url(`/struktur/merkezler/${yeniId}`)).set('Authorization', `Bearer ${token}`)
        .expect(200));
  });

  // ── KADRLAR ──
  describe('GET /kadrlar/emekdaslar', () => {
    it('tam profil qaytarir', async () => {
      const c = await api()
        .get(url('/kadrlar/emekdaslar?limit=2')).set('Authorization', `Bearer ${token}`)
        .expect(200);

      const r = c.body.data[0];
      expect(r).toHaveProperty('tam_adi');
      expect(r).toHaveProperty('merkez');
      expect(r).toHaveProperty('vezife');
      expect(typeof r.maas === 'number' || r.maas === null).toBe(true);
    });

    it('merkez_id filtri isleyir', async () => {
      const c = await api()
        .get(url('/kadrlar/emekdaslar?merkez_id=10')).set('Authorization', `Bearer ${token}`)
        .expect(200);
      expect(c.body.meta.cem).toBeGreaterThan(0);
    });

    it('maas araligi filtri isleyir', async () => {
      const c = await api()
        .get(url('/kadrlar/emekdaslar?min_maas=2000&max_maas=3000')).set('Authorization', `Bearer ${token}`)
        .expect(200);
      for (const r of c.body.data) {
        expect(r.maas).toBeGreaterThanOrEqual(2000);
        expect(r.maas).toBeLessThanOrEqual(3000);
      }
    });

    it('siralama=desc isleyir', async () => {
      const c = await api()
        .get(url('/kadrlar/emekdaslar?siralama=desc&siralama_sah=maas&limit=5')).set('Authorization', `Bearer ${token}`)
        .expect(200);
      const maaslar = c.body.data.map((r: { maas: number }) => r.maas);
      const siralanmis = [...maaslar].sort((a, b) => b - a);
      expect(maaslar).toEqual(siralanmis);
    });

    it('yanlis siralama sahesi 400 verir', () =>
      api()
        .get(url('/kadrlar/emekdaslar?siralama_sah=DROP TABLE')).set('Authorization', `Bearer ${token}`)
        .expect(400));

    it('icmal qaytarir', async () => {
      const c = await api()
        .get(url('/kadrlar/emekdaslar/icmal')).set('Authorization', `Bearer ${token}`)
        .expect(200);
      expect(c.body).toHaveProperty('umumi_fond');
      expect(Array.isArray(c.body.merkez_uzre)).toBe(true);
    });
  });

  // ── HESABATLAR ──
  describe('GET /hesabatlar', () => {
    it('icmal 48 cedvel ve 8 view gosterir', async () => {
      const c = await api()
        .get(url('/hesabatlar/icmal')).set('Authorization', `Bearer ${token}`)
        .expect(200);
      expect(c.body.cedvel_sayi).toBe(48);
      expect(c.body.gorunus_sayi).toBe(8);
    });

    it('8 view siyahilayir', async () => {
      const c = await api()
        .get(url('/hesabatlar/gorunusler')).set('Authorization', `Bearer ${token}`)
        .expect(200);
      expect(c.body).toHaveLength(8);
    });

    it('budce ROLLUP yekunu verir', async () => {
      const c = await api()
        .get(url('/hesabatlar/budce-icmali')).set('Authorization', `Bearer ${token}`)
        .expect(200);
      const cem = c.body.find((r: { il: string }) => r.il === 'CƏMİ');
      expect(cem).toBeDefined();
      expect(cem.mebleg).toBeGreaterThan(0);
    });

    it('funksiyalar netice qaytarir', async () => {
      const c = await api()
        .get(url('/hesabatlar/funksiyalar')).set('Authorization', `Bearer ${token}`)
        .expect(200);
      expect(typeof c.body.maas_fondu).toBe('number');
    });
  });

  // ── XƏTA FORMATI ──
  describe('Vahid xeta formati', () => {
    it('404 formati duzgundur', async () => {
      const c = await api()
        .get(url('/struktur/merkezler/999999')).set('Authorization', `Bearer ${token}`)
        .expect(404);

      expect(c.body).toMatchObject({
        ugur: false,
        xeta: { kod: 'TAPILMADI' },
      });
      expect(c.body).toHaveProperty('yol');
      expect(c.body).toHaveProperty('vaxt');
    });

    it('validasiya xetasi detallar massivi verir', async () => {
      const c = await api()
        .post(url('/struktur/merkezler')).set('Authorization', `Bearer ${token}`)
        .send({ ad: 'AB', email: 'sehv' })
        .expect(400);

      expect(c.body.ugur).toBe(false);
      expect(c.body.xeta.kod).toBe('YANLIS_SORGU');
      expect(Array.isArray(c.body.xeta.detallar)).toBe(true);
      expect(c.body.xeta.detallar.length).toBeGreaterThanOrEqual(2);
    });
  });
});
