import { Controller, Get, Param, ParseIntPipe, Query } from '@nestjs/common';
import { StatistikaService } from './statistika.service.js';
import { StatistikaSorguDto } from './dto/statistika-sorgu.dto.js';

/**
 * ⚠️ BU CONTROLLER `emekdaslar` YOLUNU `EmekdaslarController` İLƏ
 * PAYLAŞIR. Nest iki controller-i eyni prefikslə qeydiyyatdan keçirməyə
 * icazə verir — marşrutlar birləşdirilir.
 *
 * ⚠️ VACİB: modulda bu controller `EmekdaslarController`-dən ƏVVƏL
 * yazılmalıdır! Səbəb:
 *
 *   GET /api/v1/emekdaslar/statistika   ← 2 seqment
 *   GET /api/v1/emekdaslar/:id          ← 2 seqment  ← TOQQUŞUR!
 *
 * Express marşrutları ELAN SIRASI ilə yoxlayır. `:id` əvvəl gəlsəydi,
 * «statistika» sözü ID kimi tutular və `ParseIntPipe` 400 qaytarardı.
 * ADDIM 26-da bunu canlı nümayiş etdirəcəyik.
 */
@Controller('emekdaslar')
export class StatistikaController {
  constructor(private readonly statistika: StatistikaService) {}

  /** GET /api/v1/emekdaslar/statistika — ümumi mənzərə */
  @Get('statistika')
  umumi() {
    return this.statistika.umumi();
  }

  /** GET /api/v1/emekdaslar/statistika/merkezler */
  @Get('statistika/merkezler')
  merkezler(@Query() sorgu: StatistikaSorguDto) {
    return this.statistika.merkezler(sorgu.aktiv, sorgu.min_say, sorgu.siralama);
  }

  /** GET /api/v1/emekdaslar/statistika/vezifeler */
  @Get('statistika/vezifeler')
  vezifeler(@Query() sorgu: StatistikaSorguDto) {
    return this.statistika.vezifeler(sorgu.aktiv, sorgu.min_say, sorgu.siralama);
  }

  /** GET /api/v1/emekdaslar/statistika/merkezler-tam */
  @Get('statistika/merkezler-tam')
  butunMerkezler() {
    return this.statistika.butunMerkezler();
  }

  /** GET /api/v1/emekdaslar/statistika/shobe-sayi/5 */
  @Get('statistika/shobe-sayi/:merkezId')
  shobeSayi(@Param('merkezId', ParseIntPipe) merkezId: number) {
    return this.statistika.merkezShobeSayi(merkezId);
  }
}
