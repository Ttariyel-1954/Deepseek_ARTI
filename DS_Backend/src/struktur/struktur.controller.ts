import {
  Body, Controller, Delete, Get, HttpCode, HttpStatus, Param,
  ParseIntPipe, Patch, Post, Query,
} from '@nestjs/common';
import {
  ApiBearerAuth, ApiOperation, ApiParam, ApiResponse, ApiTags,
} from '@nestjs/swagger';
import { Roles } from '../auth/decorators/roles.decorator.js';
import { StrukturService, Merkez } from './struktur.service.js';
import { CreateMerkezDto } from './dto/create-merkez.dto.js';
import { UpdateMerkezDto } from './dto/update-merkez.dto.js';
import { MerkezFiltrDto } from './dto/merkez-filtr.dto.js';
import { Sehifelenmis } from '../common/dto/sehife.dto.js';

@ApiTags('struktur')
@ApiBearerAuth()
@Controller('struktur/merkezler')
export class StrukturController {
  constructor(private readonly struktur: StrukturService) {}

  @Get()
  @ApiOperation({
    summary: 'Merkezlerin siyahisi',
    description: 'Sehifeleme, axtaris, filtr ve siralama desteklenir.',
  })
  @ApiResponse({ status: 200, description: 'Sehifelenmis siyahi' })
  siyahi(@Query() filtr: MerkezFiltrDto): Promise<Sehifelenmis<Merkez>> {
    return this.struktur.merkezler(filtr);
  }

  @Get('statistika')
  @ApiOperation({ summary: 'Merkez uzre shobe ve emekdas sayi' })
  statistika() {
    return this.struktur.merkezStatistikasi();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Bir merkez' })
  @ApiParam({ name: 'id', example: 2 })
  @ApiResponse({ status: 404, description: 'Merkez tapilmadi' })
  bir(@Param('id', ParseIntPipe) id: number): Promise<Merkez> {
    return this.struktur.merkez(id);
  }

  @Post()
  @Roles('admin', 'muhendis')
  @ApiOperation({ summary: 'Yeni merkez yarat (admin, muhendis)' })
  @ApiResponse({ status: 201, description: 'Yaradildi' })
  @ApiResponse({ status: 409, description: 'Bu adla merkez artiq var' })
  yarat(@Body() dto: CreateMerkezDto): Promise<Merkez> {
    return this.struktur.yarat(dto);
  }

  @Patch(':id')
  @Roles('admin', 'muhendis')
  @ApiOperation({ summary: 'Merkezi yenile (admin, muhendis)' })
  yenile(
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: UpdateMerkezDto,
  ): Promise<Merkez> {
    return this.struktur.yenile(id, dto);
  }

  @Delete(':id')
  @Roles('admin')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Merkezi sil (yalniz admin)' })
  @ApiResponse({ status: 409, description: 'Bagli shobeler var' })
  sil(@Param('id', ParseIntPipe) id: number) {
    return this.struktur.sil(id);
  }
}
