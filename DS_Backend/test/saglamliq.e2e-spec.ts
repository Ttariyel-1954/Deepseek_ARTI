import { INestApplication, ValidationPipe } from '@nestjs/common';
import { Test, TestingModule } from '@nestjs/testing';
import request from 'supertest';
import { AppModule } from '../src/app.module.js';
import { AllExceptionsFilter } from '../src/common/filters/all-exceptions.filter.js';

describe('Sağlamlıq (e2e)', () => {
  let app: INestApplication;

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
  });

  afterAll(async () => {
    await app.close();
  });

  it('GET /api/v1/saglamliq → 200, baza qoşulub, 48 cədvəl', async () => {
    const c = await request(app.getHttpServer())
      .get('/api/v1/saglamliq')
      .expect(200);

    expect(c.body.status).toBe('saglam');
    expect(c.body.baza.qosulub).toBe(true);
    expect(c.body.baza.cedvel_sayi).toBe(48);
  });

  it('GET /api/v1 → API məlumatı', async () => {
    const c = await request(app.getHttpServer()).get('/api/v1').expect(200);

    expect(c.body.prefiks).toBe('/api/v1');
    expect(c.body.ad).toContain('ERP');
  });

  it('prefikssiz yol → 404', async () => {
    await request(app.getHttpServer()).get('/saglamliq').expect(404);
  });

  it('olmayan yol → vahid xəta formatı', async () => {
    const c = await request(app.getHttpServer())
      .get('/api/v1/yoxdur')
      .expect(404);

    expect(c.body.ugur).toBe(false);
    expect(c.body.xeta.kod).toBe('TAPILMADI');
    expect(typeof c.body.vaxt).toBe('string');
  });
});
