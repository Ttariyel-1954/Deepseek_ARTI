import { Controller, Get, Query, ParseIntPipe } from '@nestjs/common';
import { ApiOperation, ApiQuery, ApiTags } from '@nestjs/swagger';
import { HesabatlarService } from './hesabatlar.service.js';

@ApiTags('hesabatlar')
@Controller('hesabatlar')
export class HesabatlarController {
  constructor(private readonly hesabat: HesabatlarService) {}

  @Get('icmal')
  @ApiOperation({ summary: 'Dashboard ucun umumi icmal' })
  icmal() { return this.hesabat.umumiIcmal(); }

  @Get('gorunusler')
  @ApiOperation({ summary: 'Bazadaki butun view-lar' })
  gorunusler() { return this.hesabat.gorunusler(); }

  @Get('merkez-shobe')
  @ApiOperation({ summary: 'Merkez uzre shobe sayi (view)' })
  merkezShobe() { return this.hesabat.merkezShobe(); }

  @Get('emekdaslar')
  @ApiOperation({ summary: 'Emekdaslarin tam profili (view)' })
  @ApiQuery({ name: 'limit', required: false, example: 20 })
  emekdasTam(@Query('limit', new ParseIntPipe({ optional: true })) limit?: number) {
    return this.hesabat.emekdasTam(limit ?? 20);
  }

  @Get('budce')
  @ApiOperation({ summary: 'Budce istifadesi (view)' })
  budce() { return this.hesabat.budceIstifadesi(); }

  @Get('budce-icmali')
  @ApiOperation({ summary: 'Il uzre budce — ROLLUP yekunu ile' })
  budceIcmali() { return this.hesabat.budceIcmali(); }

  @Get('telim-qruplari')
  @ApiOperation({ summary: 'Telim qruplari ve istirakci sayi (view)' })
  telimQruplari() { return this.hesabat.telimQruplari(); }

  @Get('funksiyalar')
  @ApiOperation({ summary: 'Bazadaxili funksiyalarin neticeleri' })
  funksiyalar() { return this.hesabat.funksiyalar(); }

  @Get('audit')
  @ApiOperation({ summary: 'En son audit qeydleri' })
  @ApiQuery({ name: 'limit', required: false, example: 10 })
  audit(@Query('limit', new ParseIntPipe({ optional: true })) limit?: number) {
    return this.hesabat.sonAudit(limit ?? 10);
  }
}
