import { Controller, Get, Param, ParseIntPipe, Query } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { KadrlarService, EmekdasTam } from './kadrlar.service.js';
import { EmekdasFiltrDto } from './dto/emekdas-filtr.dto.js';
import { Sehifelenmis } from '../common/dto/sehife.dto.js';

@ApiTags('kadrlar')
@Controller('kadrlar/emekdaslar')
export class KadrlarController {
  constructor(private readonly kadrlar: KadrlarService) {}

  @Get()
  @ApiOperation({
    summary: 'Emekdaslarin siyahisi',
    description:
      'Tam profil (merkez, shobe, vezife, elmi derece) + sehifeleme, ' +
      'axtaris, filtr ve siralama.',
  })
  siyahi(@Query() filtr: EmekdasFiltrDto): Promise<Sehifelenmis<EmekdasTam>> {
    return this.kadrlar.emekdaslar(filtr);
  }

  @Get('icmal')
  @ApiOperation({ summary: 'Kadr icmali — merkez ve vezife uzre' })
  icmal() {
    return this.kadrlar.icmal();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Bir emekdasin tam profili' })
  bir(@Param('id', ParseIntPipe) id: number): Promise<EmekdasTam> {
    return this.kadrlar.emekdas(id);
  }
}
