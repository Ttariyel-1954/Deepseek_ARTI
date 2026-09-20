import { Module } from '@nestjs/common';
import { APP_GUARD, APP_INTERCEPTOR } from '@nestjs/core';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module.js';
import { SaglamliqModule } from './saglamliq/saglamliq.module.js';
import { AuthModule } from './auth/auth.module.js';
import { StrukturModule } from './struktur/struktur.module.js';
import { KadrlarModule } from './kadrlar/kadrlar.module.js';
import { HesabatlarModule } from './hesabatlar/hesabatlar.module.js';
import { AiModule } from './ai/ai.module.js';
import { IxracModule } from './ixrac/ixrac.module.js';
import { JwtAuthGuard } from './auth/guards/jwt-auth.guard.js';
import { RolesGuard } from './auth/guards/roles.guard.js';
import { AuditInterceptor } from './common/interceptors/audit.interceptor.js';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    SaglamliqModule,
    AuthModule,
    StrukturModule,
    KadrlarModule,
    HesabatlarModule,
    AiModule,
    IxracModule,
  ],
  providers: [
    // SIRA VACIBDIR: evvelce "kim oldugunu" yoxla, sonra "icazen varmi"
    { provide: APP_GUARD, useClass: JwtAuthGuard },
    { provide: APP_GUARD, useClass: RolesGuard },
    // Butun yazma emeliyyatlarini jurnala yaz
    { provide: APP_INTERCEPTOR, useClass: AuditInterceptor },
  ],
})
export class AppModule {}
