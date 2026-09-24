import { Body, Controller, Get, Patch, Post } from '@nestjs/common';
import { TopluService } from './toplu.service.js';
import { MaasArtimDto, TopluAktivlikDto, TopluYaratDto } from './dto/toplu.dto.js';

/**
 * Toplu əməliyyatlar controller-i.
 *
 * ⚠️ Bütün yollar ƏN AZI 3 seqmentdir (`toplu/...`), ona görə
 * `@Patch(':id')` ilə toqquşmur. Əgər `@Patch('toplu')` yazsaydıq —
 * 2 seqment olardı və `:id` kimi tutula bilərdi.
 */
@Controller('emekdaslar/toplu')
export class TopluController {
  constructor(private readonly toplu: TopluService) {}

  /** POST /api/v1/emekdaslar/toplu/yarat */
  @Post('yarat')
  yarat(@Body() dto: TopluYaratDto) {
    return this.toplu.topluYarat(dto);
  }

  /** PATCH /api/v1/emekdaslar/toplu/aktivlik */
  @Patch('aktivlik')
  aktivlik(@Body() dto: TopluAktivlikDto) {
    return this.toplu.topluAktivlik(dto);
  }

  /** PATCH /api/v1/emekdaslar/toplu/maas-artim */
  @Patch('maas-artim')
  maasArtim(@Body() dto: MaasArtimDto) {
    return this.toplu.maasArtim(dto);
  }

  /** GET /api/v1/emekdaslar/toplu/atomiklik — tranzaksiya sübutu */
  @Get('atomiklik')
  atomiklik() {
    return this.toplu.atomiklikYoxla();
  }
}
