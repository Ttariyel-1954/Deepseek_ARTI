import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import request from 'supertest';
import { App } from 'supertest/types';
import { AppModule } from '../src/app.module.js';
import { AllExceptionsFilter } from '../src/common/filters/all-exceptions.filter.js';

/**
 * BACKEND-4 e2e: AI qatı, RAG, tebii dil -> SQL, Excel ixracı.
 */
describe('Backend-4 (e2e)', () => {
  let app: INestApplication<App>;
  let token = '';
  let baxiciToken = '';

  /*
   * supertest-de .set() YALNIZ verb-den SONRA cagirila bilir:
   *   request(server).set(...)          -> TypeError: set is not a function
   *   request(server).get(url).set(...) -> DOGRU
   *
   * Ona gore verb metodlarini sarib tokeni OZUDE elave eden komekci yaziriq.
   */
  type Verb = 'get' | 'post' | 'patch' | 'put' | 'delete';

  const agent = (tokenAl?: () => string) => {
    const a = request(app.getHttpServer());
    const netice = {} as Record<Verb, (yol: string) => request.Test>;
    for (const m of ['get', 'post', 'patch', 'put', 'delete'] as Verb[]) {
      netice[m] = (yol: string) => {
        const sorqu = a[m](yol);
        const t = tokenAl?.();
        return t ? sorqu.set('Authorization', `Bearer ${t}`) : sorqu;
      };
    }
    return netice;
  };

  const api = () => agent(() => token);
  const baxici = () => agent(() => baxiciToken);
  const publicApi = () => agent();

  /*
   * IKLİ (binary) fayl ucun komekci.
   *
   * supertest susmaya gore yalniz tanidigi tipleri buffer edir.
   * XLSX ucun content-type qeyri-adi oldugu ucun body BOS gelir.
   * Ona gore buffer(true) + oz parser-imizi veririk.
   */
  const ikili = (yol: string) =>
    api()
      .get(yol)
      .buffer(true)
      .parse((cavab, geriCagiris) => {
        const parcalar: Buffer[] = [];
        cavab.on('data', (p: Buffer) => parcalar.push(p));
        cavab.on('end', () => geriCagiris(null, Buffer.concat(parcalar)));
      });

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

    for (const [rol, hedef] of [['admin', 'token'], ['baxici', 'baxiciToken']] as const) {
      const c = await publicApi()
        .post('/api/v1/auth/login')
        .send({ email: `${rol}@arti.edu.az`, parol: '123456' });
      if (hedef === 'token') token = c.body.token;
      else baxiciToken = c.body.token;
    }
  });

  afterAll(async () => {
    // Test zamani yaranan AI sorgularini temizle
    const pool = new (await import('pg')).Pool({
      connectionString: process.env.DATABASE_URL,
    });
    await pool.query("DELETE FROM ai.ai_sorghular WHERE istifadeci = 'admin@arti.edu.az' AND vaxt > now() - interval '1 hour'");
    await pool.end();
    await app.close();
  });

  const url = (y: string) => `/api/v1${y}`;

  // ── AI ──
  describe('GET /ai/statistika', () => {
    it('AI statistikasini qaytarir', async () => {
      const c = await api().get(url('/ai/statistika')).expect(200);
      expect(c.body).toHaveProperty('cem');
      expect(c.body).toHaveProperty('embedding_sayi');
      expect(typeof c.body.api_hazir).toBe('boolean');
    });
  });

  describe('GET /ai/promptlar', () => {
    it('prompt sablonlarini qaytarir', async () => {
      const c = await api().get(url('/ai/promptlar')).expect(200);
      expect(Array.isArray(c.body)).toBe(true);
      expect(c.body.length).toBeGreaterThan(0);
      expect(c.body[0]).toHaveProperty('prompt_metni');
    });
  });

  describe('POST /ai/sorush', () => {
    it('demo rejimde cavab qaytarir', async () => {
      const c = await api()
        .post(url('/ai/sorush'))
        .send({ sual: 'ARTİ-də neçə əməkdaş var?' })
        .expect(201);

      expect(c.body).toHaveProperty('cavab');
      expect(c.body.menbe).toBeTypeOf('string');
      expect(c.body.gecikme_ms).toBeGreaterThanOrEqual(0);
    });

    it('qisa sual 400 verir', () =>
      api().post(url('/ai/sorush')).send({ sual: 'ab' }).expect(400));

    it('bos sual 400 verir', () =>
      api().post(url('/ai/sorush')).send({}).expect(400));

    it('kontekst=true ile RAG isledilir', async () => {
      const c = await api()
        .post(url('/ai/sorush'))
        .send({ sual: 'kurikulum islahatı', kontekst: true })
        .expect(201);

      expect(Array.isArray(c.body.kontekst)).toBe(true);
    });
  });

  describe('GET /ai/tarixce', () => {
    it('admin tarixceye baxa bilir', () =>
      api().get(url('/ai/tarixce?limit=5')).expect(200));

    it('baxici baxa BILMIR (403)', () =>
      baxici().get(url('/ai/tarixce')).expect(403));
  });

  // ── RAG ──
  describe('RAG', () => {
    it('POST /ai/indeksle vektorlashdirir', async () => {
      const c = await api().post(url('/ai/indeksle')).expect(201);
      expect(c.body.indekslendi).toBeGreaterThan(0);
    });

    it('GET /ai/oxsar oxsar senedleri tapir', async () => {
      const c = await api()
        .get(url('/ai/oxsar?sual=kurikulum&limit=3'))
        .expect(200);

      expect(Array.isArray(c.body)).toBe(true);
      expect(c.body.length).toBeGreaterThan(0);
      expect(c.body[0]).toHaveProperty('oxsarliq');
      expect(c.body[0].oxsarliq).toBeGreaterThan(0);
    });

    it('oxsarliq bali azalan sira ile gelir', async () => {
      const c = await api().get(url('/ai/oxsar?sual=tehsil&limit=5')).expect(200);
      const ballar = c.body.map((r: { oxsarliq: number }) => r.oxsarliq);
      const siralanmis = [...ballar].sort((a, b) => b - a);
      expect(ballar).toEqual(siralanmis);
    });

    it('baxici indeksleye BILMIR (403)', () =>
      baxici().post(url('/ai/indeksle')).expect(403));
  });

  // ── TƏBİİ DİL -> SQL ──
  describe('POST /ai/sql', () => {
    it('resept siyahisini qaytarir', async () => {
      const c = await api().get(url('/ai/reseptler')).expect(200);
      expect(c.body.length).toBe(10);
    });

    const hallar: [string, string][] = [
      ['Neçə əməkdaş var?', 'emekdas_sayi'],
      ['Ən çox maaş alan 3 nəfər', 'en_cox_maas'],
      ['Mərkəzlər üzrə bölgü', 'merkez_uzre'],
      ['Büdcə nə qədərdir', 'budce'],
      ['Təlim qrupları göstər', 'telim_qruplari'],
    ];

    for (const [sual, gozlenilen] of hallar) {
      it(`"${sual}" -> ${gozlenilen}`, async () => {
        const c = await api()
          .post(url('/ai/sql'))
          .send({ sual, limit: 3 })
          .expect(201);
        expect(c.body.resept).toBe(gozlenilen);
        expect(Array.isArray(c.body.setirler)).toBe(true);
      });
    }

    it('namelum sual 400 verir', async () => {
      const c = await api()
        .post(url('/ai/sql'))
        .send({ sual: 'Sabah hava necə olacaq?' })
        .expect(400);
      expect(c.body.xeta.kod).toBe('YANLIS_SORGU');
    });

    it('limit maksimum 100', () =>
      api().post(url('/ai/sql'))
        .send({ sual: 'Neçə əməkdaş var', limit: 500 })
        .expect(400));

    it('SQL injection cehdi bloklanir', async () => {
      await api()
        .post(url('/ai/sql'))
        .send({ sual: "'; DROP TABLE kadrlar.emekdaslar--" })
        .expect(400);
    });

    it('cavabda SQL gosterilir (seffaflıq)', async () => {
      const c = await api()
        .post(url('/ai/sql'))
        .send({ sual: 'Neçə əməkdaş var?' })
        .expect(201);

      expect(c.body.sql.trim().toUpperCase().startsWith('SELECT')).toBe(true);
      expect(c.body.sql.toUpperCase()).not.toContain('DELETE');
    });
  });

  // ── İXRAC ──
  describe('İxrac', () => {
    it('emekdaslar.xlsx yuklenir', async () => {
      const c = await ikili(url('/ixrac/emekdaslar.xlsx')).expect(200);
      expect(Buffer.isBuffer(c.body)).toBe(true);
      expect(c.headers['content-type']).toContain('spreadsheetml');
      expect(c.headers['content-disposition']).toContain('emekdaslar.xlsx');
      expect(c.body.length).toBeGreaterThan(1000);
      // XLSX ZIP faylidir — ilk 2 bayt 'PK'
      expect(c.body[0]).toBe(0x50);
      expect(c.body[1]).toBe(0x4b);
    });

    it('budce.xlsx admin ucun isleyir', async () => {
      const c = await ikili(url('/ixrac/budce.xlsx')).expect(200);
      expect(Buffer.isBuffer(c.body)).toBe(true);
      expect(c.body[0]).toBe(0x50);
    });

    it('budce.xlsx baxici ucun 403', () =>
      baxici().get(url('/ixrac/budce.xlsx')).expect(403));

    it('hesabat.html qaytarir', async () => {
      const c = await api().get(url('/ixrac/hesabat.html')).expect(200);
      expect(c.headers['content-type']).toContain('text/html');
      expect(c.text).toContain('ARTİ');
      expect(c.text).toContain('<table>');
    });

    it('ixrac tokensiz islemir', () =>
      publicApi().get(url('/ixrac/emekdaslar.xlsx')).expect(401));
  });

  // ── XƏTA FORMATI ──
  describe('Xeta formatlari', () => {
    it('AI xetasi vahid formatdadir', async () => {
      const c = await api()
        .post(url('/ai/sql')).send({ sual: 'namelum sual bu' }).expect(400);
      expect(c.body).toMatchObject({ ugur: false, xeta: { kod: 'YANLIS_SORGU' } });
    });
  });
});
