import { Injectable, Logger, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { PrismaPg } from '@prisma/adapter-pg';
import { PrismaClient } from '../generated/prisma/client.js';

/**
 * Baza bağlantısını idarə edən servis.
 *
 * Prisma 7-də "driver adapter" MÜTLƏQDİR — Prisma özü birbaşa
 * bağlanmır, `pg` paketini adapter vasitəsilə işlədir.
 */
@Injectable()
export class PrismaService
  extends PrismaClient
  implements OnModuleInit, OnModuleDestroy
{
  private readonly log = new Logger('BAZA');

  constructor() {
    const connectionString = process.env.DATABASE_URL;

    if (!connectionString) {
      throw new Error(
        'DATABASE_URL təyin olunmayıb — .env faylını yoxlayın',
      );
    }

    super({ adapter: new PrismaPg({ connectionString }) });
  }

  async onModuleInit(): Promise<void> {
    await this.$connect();
    this.log.log('Baza bağlantısı açıldı');
  }

  async onModuleDestroy(): Promise<void> {
    await this.$disconnect();
  }

  /** Baza həqiqətən cavab verirmi? — sağlamlıq yoxlaması üçün */
  async yoxla(): Promise<{ cedvelSayi: number; gecikmeMs: number }> {
    const baslama = Date.now();

    const netice = await this.$queryRaw<{ say: number }[]>`
      SELECT count(*)::int AS say
        FROM information_schema.tables
       WHERE table_type = 'BASE TABLE'
         AND table_schema NOT IN ('pg_catalog', 'information_schema')`;

    return {
      cedvelSayi: netice[0]?.say ?? 0,
      gecikmeMs: Date.now() - baslama,
    };
  }
}
