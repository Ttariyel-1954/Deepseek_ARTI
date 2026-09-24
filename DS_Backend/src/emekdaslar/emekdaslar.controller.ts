import {
  Body,
  Controller,
  Delete,
  Get,
  HttpCode,
  Param,
  ParseIntPipe,
  Patch,
  Post,
  Query,
} from '@nestjs/common';
import { EmekdaslarService } from './emekdaslar.service.js';
import { EmekdasSorguDto } from './dto/emekdas-sorgu.dto.js';
import { EmekdasYaratDto } from './dto/emekdas-yarat.dto.js';
import { EmekdasYenileDto } from './dto/emekdas-yenile.dto.js';

/**
 * `@Controller('emekdaslar')` + qlobal `setGlobalPrefix('api/v1')`
 * → bütün yollar `/api/v1/emekdaslar...` ilə başlayır.
 *
 * ⚠️ METOD SIRASI VACİBDİR! `@Get(':id')` `@Get('statistika')`-dan
 * ƏVVƏL yazılsaydı, `/emekdaslar/statistika` sorğusu `:id` kimi
 * tutulardı və `ParseIntPipe` «statistika» mətnini ədədə çevirə
 * bilməyib 400 qaytarardı. Ona görə konkret yollar (:id-dən əvvəl)
 * yuxarıda yazılır. Bizdə hələ konkret yol yoxdur — amma 2B-də
 * `statistika` əlavə edəndə bu qayda lazım olacaq.
 */
@Controller('emekdaslar')
export class EmekdaslarController {
  constructor(private readonly xidmet: EmekdaslarService) {}

  /** GET /api/v1/emekdaslar?seife=1&limit=20&axtar=Əli&aktiv=aktiv */
  @Get()
  hamisi(@Query() sorgu: EmekdasSorguDto) {
    return this.xidmet.hamisi(sorgu);
  }

  /** GET /api/v1/emekdaslar/5 */
  @Get(':id')
  biri(@Param('id', ParseIntPipe) id: number) {
    return this.xidmet.biri(id);
  }

  /** POST /api/v1/emekdaslar — 201 Created qaytarır */
  @Post()
  @HttpCode(201)
  yarat(@Body() dto: EmekdasYaratDto) {
    return this.xidmet.yarat(dto);
  }

  /** PATCH /api/v1/emekdaslar/5 — yalnız göndərilən sahələri dəyişir */
  @Patch(':id')
  yenile(@Param('id', ParseIntPipe) id: number, @Body() dto: EmekdasYenileDto) {
    return this.xidmet.yenile(id, dto);
  }

  /** DELETE /api/v1/emekdaslar/5 — yumşaq və ya adi silmə */
  @Delete(':id')
  sil(@Param('id', ParseIntPipe) id: number) {
    return this.xidmet.sil(id);
  }
}
