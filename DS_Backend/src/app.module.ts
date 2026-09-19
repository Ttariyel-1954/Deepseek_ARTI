import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module.js';
import { SaglamliqModule } from './saglamliq/saglamliq.module.js';
import { StrukturModule } from './struktur/struktur.module.js';
import { KadrlarModule } from './kadrlar/kadrlar.module.js';
import { HesabatlarModule } from './hesabatlar/hesabatlar.module.js';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    SaglamliqModule,
    StrukturModule,
    KadrlarModule,
    HesabatlarModule,
  ],
})
export class AppModule {}
