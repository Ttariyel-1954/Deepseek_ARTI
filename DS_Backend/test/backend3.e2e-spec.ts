import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import request from 'supertest';
import { App } from 'supertest/types';
import { AppModule } from '../src/app.module.js';
import { AllExceptionsFilter } from '../src/common/filters/all-exceptions.filter.js';
import { Pool } from 'pg';

/**
 * BACKEND-3 e2e: autentifikasiya, RBAC ve audit.
 * APP_GUARD ile qeyd olunan qlobal guard-lar AppModule ile avtomatik gelir.
 */
describe('Backend-3 (e2e)', () => {
  let app: INestApplication<App>;

  const tokenlar: Record<string, string> = {};
  const YARADILANLAR: number[] = [];

  beforeAll(async () => {
    const modul: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = modul.createNestApplication();
    app.setGlobalPrefix('api/v1');
    app.useGlobalPipes(
      new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }),
    );
    app.useGlobalFilters(new AllExceptionsFilter());
    await app.init();

    // Butun rollar ucun token al
    for (const rol of ['admin', 'muhendis', 'maliyyeci', 'baxici']) {
      const c = await request(app.getHttpServer())
        .post('/api/v1/auth/login')
        .send({ email: `${rol}@arti.edu.az`, parol: '123456' });
      if (c.body?.token) tokenlar[rol] = c.body.token;
    }
  });

  afterAll(async () => {
    const admin = tokenlar.admin;

    // 1) Test zamani yaradilan merkezleri sil
    for (const id of YARADILANLAR) {
      await request(app.getHttpServer())
        .delete(`/api/v1/struktur/merkezler/${id}`)
        .set('Authorization', `Bearer ${admin}`);
    }

    /*
     * 2) Test istifadecilerini sil.
     * Qeydiyyat endpoint-i ile yaradilanlar bazada qalir —
     * onlari birbasa SQL ile temizleyirik, eks halda her test
     * buraxilisi yeni setirler elave eder.
     */
    const pool = new Pool({ connectionString: process.env.DATABASE_URL });
    await pool.query("DELETE FROM kadrlar.istifadeciler WHERE email LIKE 'e2e%'");
    await pool.end();

    await app.close();
  });

  const url = (y: string) => `/api/v1${y}`;
  const auth = (rol: string) => ({ Authorization: `Bearer ${tokenlar[rol]}` });

  // ── LOGIN ──
  describe('POST /auth/login', () => {
    it('duzgun melumatla token qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'admin@arti.edu.az', parol: '123456' })
        .expect(200);

      expect(c.body.token).toBeTypeOf('string');
      expect(c.body.token.split('.')).toHaveLength(3);     // JWT 3 hissedir
      expect(c.body.istifadeci.rol).toBe('admin');
      expect(c.body.istifadeci).not.toHaveProperty('parol_hash');
    });

    it('sehv sifre 401 verir', () =>
      request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'admin@arti.edu.az', parol: 'sehv-sifre' })
        .expect(401));

    it('movcud olmayan email 401 verir', () =>
      request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'yoxdur@arti.edu.az', parol: '123456' })
        .expect(401));

    it('qisa sifre 400 verir (validasiya)', () =>
      request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'admin@arti.edu.az', parol: '123' })
        .expect(400));

    it('yanlis email formati 400 verir', () =>
      request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'email-deyil', parol: '123456' })
        .expect(400));
  });

  // ── TOKEN ──
  describe('Token yoxlamasi', () => {
    it('tokensiz qorunan endpoint 401', () =>
      request(app.getHttpServer()).get(url('/struktur/merkezler')).expect(401));

    it('sehv token 401', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler'))
        .set('Authorization', 'Bearer sehv.token.deyeri')
        .expect(401));

    it('Bearer prefiksi olmadan 401', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler'))
        .set('Authorization', tokenlar.admin)
        .expect(401));

    it('duzgun token 200', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler'))
        .set(auth('admin'))
        .expect(200));
  });

  // ── PUBLIC ──
  describe('@Public() endpoint-ler', () => {
    it('saglamliq tokensiz isleyir', () =>
      request(app.getHttpServer()).get(url('/saglamliq')).expect(200));

    it('kok tokensiz isleyir', () =>
      request(app.getHttpServer()).get(url('')).expect(200));

    it('login tokensiz isleyir', () =>
      request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'admin@arti.edu.az', parol: '123456' })
        .expect(200));
  });

  // ── PROFIL ──
  describe('GET /auth/profil', () => {
    it('cari istifadecini qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/auth/profil'))
        .set(auth('maliyyeci'))
        .expect(200);

      expect(c.body.email).toBe('maliyyeci@arti.edu.az');
      expect(c.body.rol).toBe('maliyyeci');
      expect(c.body).not.toHaveProperty('parol_hash');
    });
  });

  // ── RBAC MATRİSİ ──
  describe('RBAC — rol icazeleri', () => {
    const yarat = (rol: string) =>
      request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .set(auth(rol))
        .send({ ad: `RBAC E2E ${rol} ${Date.now()}` });

    it('admin merkez yarada bilir', async () => {
      const c = await yarat('admin').expect(201);
      YARADILANLAR.push(c.body.id);
    });

    it('muhendis merkez yarada bilir', async () => {
      const c = await yarat('muhendis').expect(201);
      YARADILANLAR.push(c.body.id);
    });

    it('maliyyeci merkez yarada BILMIR (403)', () =>
      yarat('maliyyeci').expect(403));

    it('baxici merkez yarada BILMIR (403)', () =>
      yarat('baxici').expect(403));

    it('baxici OXUYA bilir (200)', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler'))
        .set(auth('baxici'))
        .expect(200));

    it('admin olmayan silmir (403)', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .set(auth('admin'))
        .send({ ad: `Silme testi ${Date.now()}` })
        .expect(201);

      await request(app.getHttpServer())
        .delete(url(`/struktur/merkezler/${c.body.id}`))
        .set(auth('muhendis'))
        .expect(403);

      await request(app.getHttpServer())
        .delete(url(`/struktur/merkezler/${c.body.id}`))
        .set(auth('admin'))
        .expect(200);
    });

    it('istifadeci siyahisi yalniz admin ucun', async () => {
      await request(app.getHttpServer())
        .get(url('/auth/istifadeciler')).set(auth('baxici')).expect(403);
      await request(app.getHttpServer())
        .get(url('/auth/istifadeciler')).set(auth('admin')).expect(200);
    });

    it('admin HER SEYE icazelidir (super-rol)', () =>
      request(app.getHttpServer())
        .get(url('/hesabatlar/icmal')).set(auth('admin')).expect(200));

    it('baxici hesabatlari oxuya bilir', () =>
      request(app.getHttpServer())
        .get(url('/hesabatlar/icmal')).set(auth('baxici')).expect(200));
  });

  // ── QEYDİYYAT ──
  describe('POST /auth/qeydiyyat', () => {
    const yeni = () => ({
      email: `e2e${Date.now()}_${Math.floor(Math.random() * 9999)}@arti.edu.az`,
      parol: 'guclu-sifre-2026',
      ad_soyad: 'E2E Test Istifadeci',
      rol: 'baxici',
    });

    it('admin yeni istifadeci yarada bilir', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/auth/qeydiyyat'))
        .set(auth('admin'))
        .send(yeni())
        .expect(201);

      expect(c.body.rol).toBe('baxici');
      expect(c.body).not.toHaveProperty('parol_hash');
    });

    it('qeydiyyatdan sonra HEMIN sifre ile giris isleyir', async () => {
      const m = yeni();
      await request(app.getHttpServer())
        .post(url('/auth/qeydiyyat')).set(auth('admin')).send(m).expect(201);

      const c = await request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: m.email, parol: m.parol })
        .expect(200);

      expect(c.body.token).toBeTypeOf('string');
    });

    it('qeydiyyat yalniz admin ucun (baxici 403)', () =>
      request(app.getHttpServer())
        .post(url('/auth/qeydiyyat')).set(auth('baxici')).send(yeni()).expect(403));

    it('qisa sifre 400 verir', () =>
      request(app.getHttpServer())
        .post(url('/auth/qeydiyyat')).set(auth('admin'))
        .send({ ...yeni(), parol: 'qisa' })
        .expect(400));

    it('yanlis rol 400 verir', () =>
      request(app.getHttpServer())
        .post(url('/auth/qeydiyyat')).set(auth('admin'))
        .send({ ...yeni(), rol: 'superadmin' })
        .expect(400));
  });

  // ── AUDIT ──
  describe('Audit jurnali', () => {
    it('yazma emeliyyati jurnala dusur', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .set(auth('admin'))
        .send({ ad: `Audit E2E ${Date.now()}` })
        .expect(201);
      YARADILANLAR.push(c.body.id);

      const audit = await request(app.getHttpServer())
        .get(url('/hesabatlar/audit?limit=1'))
        .set(auth('admin'))
        .expect(200);

      expect(audit.body[0].cedvel_adi).toBe('struktur.merkezler');
      expect(audit.body[0].emeliyyat).toBe('POST');
      expect(audit.body[0].istifadeci).toBe('admin@arti.edu.az');
    });

    it('oxuma emeliyyati jurnala DUSMUR', async () => {
      const evvel = await request(app.getHttpServer())
        .get(url('/hesabatlar/audit?limit=1'))
        .set(auth('admin'));

      await request(app.getHttpServer())
        .get(url('/struktur/merkezler')).set(auth('admin')).expect(200);
      await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar')).set(auth('admin')).expect(200);

      const sonra = await request(app.getHttpServer())
        .get(url('/hesabatlar/audit?limit=1'))
        .set(auth('admin'));

      // En son qeyd deyismeyib — GET yazilmir
      expect(sonra.body[0].id).toBe(evvel.body[0].id);
    });
  });

  // ── XƏTA FORMATI ──
  describe('Xeta formatlari', () => {
    it('401 formati duzgundur', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/struktur/merkezler')).expect(401);
      expect(c.body.xeta.kod).toBe('AUTENTIFIKASIYA_LAZIM');
    });

    it('403 formati duzgundur', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/struktur/merkezler')).set(auth('baxici'))
        .send({ ad: 'Test Merkez' })
        .expect(403);
      expect(c.body.xeta.kod).toBe('ICAZE_YOXDUR');
    });

    it('parol_hash HEÇ VAXT cavabda gelmir', async () => {
      const cavablar = await Promise.all([
        request(app.getHttpServer()).post(url('/auth/login'))
          .send({ email: 'admin@arti.edu.az', parol: '123456' }),
        request(app.getHttpServer()).get(url('/auth/profil')).set(auth('admin')),
        request(app.getHttpServer()).get(url('/auth/istifadeciler')).set(auth('admin')),
      ]);
      for (const c of cavablar) {
        expect(JSON.stringify(c.body)).not.toContain('$2b$');
        expect(JSON.stringify(c.body)).not.toContain('parol_hash');
      }
    });
  });
});
