import { Controller, Get, Param, ParseIntPipe } from '@nestjs/common';
import { ElaqelerService } from './elaqeler.service.js';

/**
 * Əlaqələr controller-i — `emekdaslar` prefiksini paylaşır.
 *
 * ⚠️ Bütün yollar ƏN AZI 3 seqmentdir (`:id/...`), ona görə
 * `EmekdaslarController`-dəki `@Get(':id')` ilə TOQQUŞMUR:
 * Express-də `:id` yalnız BİR seqmenti tutur.
 *
 * Əgər burada `@Get(':id')` yazsaydıq — toqquşardı və sıra həlledici
 * olardı. Statistika controller-i məhz bu səbəbdən `:id`-dən əvvəl
 * qeydiyyatdan keçməlidir (ADDIM 26).
 */
@Controller('emekdaslar')
export class ElaqelerController {
  constructor(private readonly elaqeler: ElaqelerService) {}

  /** GET /api/v1/emekdaslar/6/icmal — yalnız SAYLAR (bir sorğu) */
  @Get(':id/icmal')
  icmal(@Param('id', ParseIntPipe) id: number) {
    return this.elaqeler.icmal(id);
  }

  /** GET /api/v1/emekdaslar/6/tam — bütün əlaqələr paralel */
  @Get(':id/tam')
  tam(@Param('id', ParseIntPipe) id: number) {
    return this.elaqeler.hamisi(id);
  }

  /** GET /api/v1/emekdaslar/6/tam-bir-sorqu — hamısı bir findUnique ilə */
  @Get(':id/tam-bir-sorqu')
  tamBirSorquda(@Param('id', ParseIntPipe) id: number) {
    return this.elaqeler.birSorquda(id);
  }

  /** GET /api/v1/emekdaslar/6/tam-ad — baza funksiyası ilə */
  @Get(':id/tam-ad')
  tamAd(@Param('id', ParseIntPipe) id: number) {
    return this.elaqeler.bazaTamAd(id);
  }

  @Get(':id/doktorantlar')
  doktorantlar(@Param('id', ParseIntPipe) id: number) {
    return this.elaqeler.doktorantlar(id);
  }

  @Get(':id/sertifikatlar')
  sertifikatlar(@Param('id', ParseIntPipe) id: number) {
    return this.elaqeler.sertifikatlar(id);
  }

  @Get(':id/mezuniyyetler')
  mezuniyyetler(@Param('id', ParseIntPipe) id: number) {
    return this.elaqeler.mezuniyyetler(id);
  }

  @Get(':id/tecrube')
  tecrube(@Param('id', ParseIntPipe) id: number) {
    return this.elaqeler.tecrube(id);
  }

  @Get(':id/layiheler')
  layiheler(@Param('id', ParseIntPipe) id: number) {
    return this.elaqeler.layiheler(id);
  }

  @Get(':id/shura')
  shura(@Param('id', ParseIntPipe) id: number) {
    return this.elaqeler.shura(id);
  }
}
