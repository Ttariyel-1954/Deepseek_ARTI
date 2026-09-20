import { Controller, Get } from '@nestjs/common';
import { Public } from '../auth/decorators/public.decorator.js';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { PrismaService } from '../prisma/prisma.service.js';

@ApiTags('saglamliq')
@Controller()
export class SaglamliqController {
  constructor(private readonly prisma: PrismaService) {}

  @Public()
  @Get('saglamliq')
  @ApiOperation({ summary: 'Server ve baza saglamligi' })
  async yoxla() {
    const baslama = Date.now();

    const baza = await this.prisma.$queryRaw<{ cedvel: number }[]>`
      SELECT count(*)::int AS cedvel FROM information_schema.tables
       WHERE table_type = 'BASE TABLE'
         AND table_schema NOT IN ('pg_catalog', 'information_schema')`;

    return {
      status: 'saglam',
      baza: {
        qosulub: true,
        cedvel_sayi: baza[0]?.cedvel ?? 0,
        gecikme_ms: Date.now() - baslama,
      },
      versiya: process.env.npm_package_version ?? '0.0.1',
      vaxt: new Date().toISOString(),
    };
  }

  @Public()
  @Get()
  @ApiOperation({ summary: 'Kok — API melumati' })
  kok() {
    return {
      ad: 'Deepseek ARTI API',
      versiya: '1.0',
      sened: '/docs',
      prefiks: '/api/v1',
    };
  }
}
