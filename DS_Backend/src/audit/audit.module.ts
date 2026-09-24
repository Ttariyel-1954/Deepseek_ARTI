import { Module } from '@nestjs/common';
import { PrismaModule } from '../prisma/prisma.module.js';
import { AuditController } from './audit.controller.js';
import { AuditService } from './audit.service.js';

/**
 * Audit modulu.
 *
 * `exports: [AuditService]` — vacibdir: 2C dərsində `EmekdaslarService`
 * bu servisi konstruktorunda istəyəcək və CRUD əməliyyatlarını
 * audit loquna yazacaq.
 *
 * ⚠️ `@Global()` ETMİRİK. Qlobal modullar kodu oxumağı çətinləşdirir:
 * «bu servis haradan gəldi?» sualına cavab tapmaq üçün bütün layihəni
 * gəzmək lazım gəlir. Açıq `imports` daha aydındır — bunu yalnız
 * həqiqətən hər yerdə lazım olan `PrismaModule` üçün etdik.
 */
@Module({
  imports: [PrismaModule],
  controllers: [AuditController],
  providers: [AuditService],
  exports: [AuditService],
})
export class AuditModule {}
