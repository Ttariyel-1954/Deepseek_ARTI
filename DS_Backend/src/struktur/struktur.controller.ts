import { Controller, Get, Param, ParseIntPipe } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { StrukturService, Merkez } from './struktur.service.js';

@ApiTags('struktur')
@Controller('struktur/merkezler')
export class StrukturController {
  constructor(private readonly struktur: StrukturService) {}

  @Get()
  @ApiOperation({ summary: 'Butun merkezlerin siyahisi' })
  siyahi(): Promise<Merkez[]> {
    return this.struktur.merkezler();
  }

  @Get('statistika')
  @ApiOperation({ summary: 'Merkez uzre shobe sayi' })
  statistika() {
    return this.struktur.merkezStatistikasi();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Bir merkez — id ile' })
  bir(@Param('id', ParseIntPipe) id: number): Promise<Merkez> {
    return this.struktur.merkez(id);
  }
}
