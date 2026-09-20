import { Controller, Get } from '@nestjs/common';
import { ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';
import { SaglamliqService } from './saglamliq.service.js';
import type { SaglamliqCavabi } from './saglamliq.service.js';

@ApiTags('saglamliq')
@Controller()
export class SaglamliqController {
  constructor(private readonly saglamliq: SaglamliqService) {}

  @Get()
  @ApiOperation({ summary: 'API haqqında qısa məlumat' })
  kok() {
    return {
      ad: 'ARTİ ERP API',
      versiya: '0.1.0',
      prefiks: '/api/v1',
      senedlesdirme: '/docs',
    };
  }

  @Get('saglamliq')
  @ApiOperation({ summary: 'Sağlamlıq yoxlaması — baza ilə birlikdə' })
  @ApiResponse({ status: 200, description: 'Sistem sağlamdır' })
  @ApiResponse({ status: 503, description: 'Baza əlçatmazdır' })
  yoxla(): Promise<SaglamliqCavabi> {
    return this.saglamliq.yoxla();
  }
}
