import { Module } from '@nestjs/common';
import { EmekdaslarController } from './emekdaslar.controller.js';
import { EmekdaslarService } from './emekdaslar.service.js';

/**
 * ⚠️ DİQQƏT: `imports` bölməsində `PrismaModule` YOXDUR.
 *
 * Səbəb: 1A-nın ADDIM 7-də `PrismaModule`-u `@Global()` elan etdik.
 * Qlobal modulun `exports` etdiyi hər şey BÜTÜN modullara avtomatik
 * açıqdır. `EmekdaslarService` öz konstruktorunda `PrismaService`
 * istəyir və Nest onu tapır.
 *
 * `@Global()` olmasaydı, burada `imports: [PrismaModule]` yazmalı
 * olardıq.
 */
@Module({
  controllers: [EmekdaslarController],
  providers: [EmekdaslarService],
  // Başqa modul (məsələn hesabat modulu) bu servisi istəyə bilər
  exports: [EmekdaslarService],
})
export class EmekdaslarModule {}
