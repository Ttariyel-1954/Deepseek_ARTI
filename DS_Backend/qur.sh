#!/bin/bash
# DS_Backend — tam qurulma skripti
# İstifadə: bash qur.sh
set -e

echo "════ 1/8  Mühit ════"
unset DATABASE_URL PGHOST
node --version
npm --version

echo "════ 2/8  NestJS layihəsi ════"
cd ~/Deepseek_ARTI
if [ ! -d DS_Backend ]; then
  npx @nestjs/cli@12 new ds_backend --package-manager npm --skip-git
  mv ds_backend ds_backend_tmp
  mv ds_backend_tmp DS_Backend
fi
cd DS_Backend

echo "════ 3/8  Paketlər ════"
npm install \
  @prisma/client@^7.10.0 @prisma/adapter-pg@^7.10.0 \
  @nestjs/config@^12.0.0 @nestjs/swagger@^12.0.0 \
  class-validator@^0.14.1 class-transformer@^0.5.1 \
  dotenv@^16.6.1 pg@^8.13.0

npm install -D prisma@^7.10.0 tsx@^4.19.0 vitest@^4.0.0

echo "════ 3.5/8  Prisma versiyasi ════"
npx prisma --version
PRISMA_VER=$(npx prisma --version | grep '^prisma' | awk '{print $3}')
case "$PRISMA_VER" in
  7.*) echo "OK — Prisma $PRISMA_VER" ;;
  *)   echo "XETA: Prisma $PRISMA_VER — 7.x lazimdir!"
       echo "Həll: npm install -D prisma@^7.10.0"
       echo "      npm uninstall -g prisma"
       exit 1 ;;
esac

echo "════ 4/8  .env ════"
cat > .env <<'EOF'
DATABASE_URL="postgresql://arti_user:arti_secret_2025@localhost:5432/arti_baza"
PORT=4000
NODE_ENV=development
JWT_SECRET="deepseek-arti-gizli-acar-2026"
JWT_MUDDET="8h"
EOF

cat > .gitignore <<'EOF'
.env
.env.*
node_modules/
dist/
src/generated/
*.log
EOF

echo "════ 5/8  tsconfig.build.json ════"
cat > tsconfig.build.json <<'EOF'
{
  "extends": "./tsconfig.json",
  "compilerOptions": { "rootDir": "./src" },
  "include": ["src"],
  "exclude": ["node_modules", "test", "dist", "**/*spec.ts"]
}
EOF

echo "════ 6/8  Prisma ════"
mkdir -p prisma
cat > prisma/schema.prisma <<'EOF'
generator client {
  provider = "prisma-client"
  output   = "../src/generated/prisma"
}

datasource db {
  provider = "postgresql"
  schemas  = ["ortaq", "struktur", "kadrlar", "elm", "tehsil", "qiymetlendirme", "metodika", "maliyye", "logistika", "sened", "audit", "ai"]
}
EOF

cat > prisma.config.ts <<'EOF'
import 'dotenv/config';
import { defineConfig, env } from 'prisma/config';

export default defineConfig({
  schema: 'prisma/schema.prisma',
  migrations: { path: 'prisma/migrations' },
  datasource: { url: env('DATABASE_URL') },
});
EOF

npx prisma db pull
npx prisma generate

echo "════ 7/8  Struktur ════"
mkdir -p src/prisma src/struktur

cat > src/prisma/prisma.service.ts <<'EOF'
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { PrismaClient } from '../generated/prisma/client.js';
import { PrismaPg } from '@prisma/adapter-pg';

@Injectable()
export class PrismaService
  extends PrismaClient
  implements OnModuleInit, OnModuleDestroy
{
  constructor() {
    const adapter = new PrismaPg({
      connectionString: process.env.DATABASE_URL!,
    });
    super({ adapter });
  }
  async onModuleInit() { await this.$connect(); }
  async onModuleDestroy() { await this.$disconnect(); }
}
EOF

cat > src/prisma/prisma.module.ts <<'EOF'
import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service.js';

@Global()
@Module({ providers: [PrismaService], exports: [PrismaService] })
export class PrismaModule {}
EOF

cat > src/struktur/struktur.service.ts <<'EOF'
import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

export interface Merkez {
  id: number; ad: string; tip: string | null;
  unvan: string | null; telefon: string | null;
  email: string | null; aktiv: boolean;
}

@Injectable()
export class StrukturService {
  constructor(private readonly prisma: PrismaService) {}

  async merkezler(): Promise<Merkez[]> {
    return this.prisma.$queryRaw<Merkez[]>`
      SELECT id::int, ad, tip, unvan, telefon, email, aktiv
      FROM struktur.merkezler ORDER BY id`;
  }

  async merkez(id: number): Promise<Merkez> {
    const s = await this.prisma.$queryRaw<Merkez[]>`
      SELECT id::int, ad, tip, unvan, telefon, email, aktiv
      FROM struktur.merkezler WHERE id = ${id}`;
    if (!s.length) throw new NotFoundException(`Merkez tapilmadi: id=${id}`);
    return s[0];
  }
}
EOF

cat > src/struktur/struktur.controller.ts <<'EOF'
import { Controller, Get, Param, ParseIntPipe } from '@nestjs/common';
import { StrukturService, Merkez } from './struktur.service.js';

@Controller('struktur/merkezler')
export class StrukturController {
  constructor(private readonly struktur: StrukturService) {}

  @Get()
  siyahi(): Promise<Merkez[]> { return this.struktur.merkezler(); }

  @Get(':id')
  bir(@Param('id', ParseIntPipe) id: number): Promise<Merkez> {
    return this.struktur.merkez(id);
  }
}
EOF

cat > src/struktur/struktur.module.ts <<'EOF'
import { Module } from '@nestjs/common';
import { StrukturService } from './struktur.service.js';
import { StrukturController } from './struktur.controller.js';

@Module({
  controllers: [StrukturController],
  providers: [StrukturService],
})
export class StrukturModule {}
EOF

cat > src/app.module.ts <<'EOF'
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module.js';
import { StrukturModule } from './struktur/struktur.module.js';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    StrukturModule,
  ],
})
export class AppModule {}
EOF

cat > src/main.ts <<'EOF'
import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module.js';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.setGlobalPrefix('api/v1');
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.enableCors();

  const cfg = new DocumentBuilder()
    .setTitle('Deepseek ARTI API').setVersion('1.0').addBearerAuth().build();
  SwaggerModule.setup('docs', app, SwaggerModule.createDocument(app, cfg));

  const port = process.env.PORT ?? 4000;
  await app.listen(port);
  console.log('API: http://localhost:' + port + '/api/v1');
}
bootstrap();
EOF

echo "════ 7.5/8  Test ════"
cat > vitest.config.ts <<'EOF'
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['**/*.spec.ts'],
    exclude: ['**/*.e2e-spec.ts', 'node_modules/**'],
  },
});
EOF

cat > src/struktur/struktur.service.spec.ts <<'EOF'
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { NotFoundException } from '@nestjs/common';
import { StrukturService } from './struktur.service.js';

function saxtaPrisma() {
  return { $queryRaw: vi.fn() } as any;
}

describe('StrukturService', () => {
  let prisma: any;
  let service: StrukturService;

  beforeEach(() => {
    prisma = saxtaPrisma();
    service = new StrukturService(prisma);
  });

  it('merkezler siyahisini qaytarir', async () => {
    prisma.$queryRaw.mockResolvedValue([
      { id: 1, ad: 'Elmi katiblik', aktiv: true },
    ]);
    const netice = await service.merkezler();
    expect(netice).toHaveLength(1);
    expect(netice[0].ad).toBe('Elmi katiblik');
  });

  it('tapilmayan merkez ucun 404 atir', async () => {
    prisma.$queryRaw.mockResolvedValue([]);
    await expect(service.merkez(999)).rejects.toThrow(NotFoundException);
  });

  it('SQL-e parametr oturur', async () => {
    prisma.$queryRaw.mockResolvedValue([]);
    await service.merkez(5).catch(() => null);
    const cagiris = prisma.$queryRaw.mock.calls[0];
    expect(cagiris.length).toBeGreaterThan(1);
    expect(cagiris[1]).toBe(5);
  });
});
EOF

npm test

echo "════ 8/8  Yoxlama ════"
npm run build
echo ""
echo "HAZIR. Serveri ise salmaq ucun: npm run start:dev"
