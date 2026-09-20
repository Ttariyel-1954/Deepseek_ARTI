import { Body, Controller, Get, Post, Query, ParseIntPipe } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { AiService } from './ai.service.js';
import { RagService } from './rag.service.js';
import { SqlKomlekciService, reseptSiyahisi } from './sql-komlekci.service.js';
import { SualDto, SqlSualDto } from './dto/sual.dto.js';
import { CurrentUser } from '../auth/decorators/current-user.decorator.js';
import { Roles } from '../auth/decorators/roles.decorator.js';
import type { CariIstifadeci } from '../auth/decorators/current-user.decorator.js';

@ApiTags('ai')
@ApiBearerAuth()
@Controller('ai')
export class AiController {
  constructor(
    private readonly ai: AiService,
    private readonly rag: RagService,
    private readonly sql: SqlKomlekciService,
  ) {}

  @Get('statistika')
  @ApiOperation({ summary: 'AI istifade statistikasi' })
  statistika() {
    return this.ai.statistika();
  }

  @Get('promptlar')
  @ApiOperation({ summary: 'Prompt sablonlari' })
  promptlar() {
    return this.ai.promptlar();
  }

  @Post('sorush')
  @ApiOperation({ summary: 'AI-a sual ver' })
  sorush(@Body() dto: SualDto, @CurrentUser() istifadeci: CariIstifadeci) {
    return this.ai.sorush(dto, istifadeci?.email ?? 'anonim');
  }

  @Get('tarixce')
  @Roles('admin')
  @ApiOperation({ summary: 'Son AI sorgulari (yalniz admin)' })
  tarixce(@Query('limit', new ParseIntPipe({ optional: true })) limit?: number) {
    return this.ai.tarixce(limit ?? 20);
  }

  // ── RAG ──
  @Get('oxsar')
  @ApiOperation({ summary: 'RAG — oxsar senedleri tap' })
  oxsar(
    @Query('sual') sual: string,
    @Query('limit', new ParseIntPipe({ optional: true })) limit?: number,
  ) {
    return this.rag.oxsarTap(sual ?? '', limit ?? 5);
  }

  @Post('indeksle')
  @Roles('admin')
  @ApiOperation({ summary: 'Embeddingleri vektorlashdir (yalniz admin)' })
  indeksle() {
    return this.rag.indeksle();
  }

  // ── TƏBİİ DİL -> SQL ──
  @Get('reseptler')
  @ApiOperation({ summary: 'Mövcud SQL reseptleri' })
  reseptler() {
    return reseptSiyahisi();
  }

  @Post('sql')
  @ApiOperation({
    summary: 'Tebii dil -> SQL',
    description:
      'AI birbasa SQL YAZMIR — yalniz movcud reseptlerden birini secir. ' +
      'Butun SQL kodu sabit yazilib ve yalniz OXUMA sorgularidir.',
  })
  sqlSorush(@Body() dto: SqlSualDto) {
    return this.sql.icraEt(dto.sual, dto.limit ?? 20);
  }
}
