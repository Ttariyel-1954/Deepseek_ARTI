import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module.js';
import { SaglamliqModule } from './saglamliq/saglamliq.module.js';
import { EmekdaslarModule } from './emekdaslar/emekdaslar.module.js';
import { AuditModule } from './audit/audit.module.js';

/**
 * Kök modul — bütün funksional modullar burada AÇIQ şəkildə qoşulur.
 *
 * Modul qrafı:
 *   AppModule
 *   ├── ConfigModule (qlobal, .env oxuyur)
 *   ├── PrismaModule (@Global — baza bağlantısı)
 *   ├── SaglamliqModule (1A)
 *   ├── EmekdaslarModule (2A + 2B)
 *   │   ├── StatistikaModule
 *   │   ├── ElaqelerModule
 *   │   └── TopluModule
 *   └── AuditModule (2B)
 */
@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    SaglamliqModule,
    EmekdaslarModule,
    AuditModule,
  ],
})
export class AppModule {}
