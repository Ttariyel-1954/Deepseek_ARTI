import { Body, Controller, Get, Param, ParseIntPipe, Post, Query } from '@nestjs/common';
import { AuditService } from './audit.service.js';
import { AuditSorguDto, AuditYazDto } from './dto/audit-sorgu.dto.js';

/**
 * ⚠️ MARŞRUT SIRASI — bu dəfə EYNİ controller daxilində.
 *
 *   GET /api/v1/audit/statistika   ← 1 seqment
 *   GET /api/v1/audit/trigger-numayisi
 *   GET /api/v1/audit/:id          ← 1 seqment   ← TOQQUŞUR!
 *
 * `@Get(':id')` yuxarıda yazılsaydı, «statistika» sözü ID kimi tutular
 * və `ParseIntPipe` 400 qaytarardı. Ona görə KONKRET yollar həmişə
 * `:id`-dən ƏVVƏL yazılır.
 *
 * Faydalı vərdiş: `:id`-ni faylın ƏN SONUNA qoyun.
 */
@Controller('audit')
export class AuditController {
  constructor(private readonly audit: AuditService) {}

  /** GET /api/v1/audit?limit=10&cedvel=kadrlar.emekdaslar */
  @Get()
  hamisi(@Query() sorgu: AuditSorguDto) {
    return this.audit.hamisi(sorgu);
  }

  /** GET /api/v1/audit/statistika — cədvəl və əməliyyat üzrə paylanma */
  @Get('statistika')
  statistika() {
    return this.audit.statistika();
  }

  /** GET /api/v1/audit/trigger-numayisi — baza trigger-inin sübutu */
  @Get('trigger-numayisi')
  triggerNumayisi() {
    return this.audit.triggerNumayisi();
  }

  /** GET /api/v1/audit/tranzaksiya-numayisi — atomikliyin sübutu */
  @Get('tranzaksiya-numayisi')
  tranzaksiyaNumayisi() {
    return this.audit.tranzaksiyaNumayisi();
  }

  /** POST /api/v1/audit — əl ilə loq qeydi */
  @Post()
  yaz(@Body() dto: AuditYazDto) {
    return this.audit.yazTek(dto);
  }

  /** GET /api/v1/audit/123 — ƏN SORUNCU: `:id` həmişə axırda */
  @Get(':id')
  biri(@Param('id', ParseIntPipe) id: number) {
    return this.audit.biri(id);
  }
}
