import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

export interface SaglamliqCavabi {
  status: string;
  baza: { qosulub: boolean; cedvel_sayi: number; gecikme_ms: number };
  versiya: string;
  vaxt: string;
}

@Injectable()
export class SaglamliqService {
  constructor(private readonly prisma: PrismaService) {}

  /**
   * Sistemin canlı olub-olmadığını yoxlayır.
   * Sadəcə "işləyirəm" demir — BAZAYA da sorğu göndərir.
   */
  async yoxla(): Promise<SaglamliqCavabi> {
    const { cedvelSayi, gecikmeMs } = await this.prisma.yoxla();

    return {
      status: 'saglam',
      baza: {
        qosulub: true,
        cedvel_sayi: cedvelSayi,
        gecikme_ms: gecikmeMs,
      },
      versiya: '0.1.0',
      vaxt: new Date().toISOString(),
    };
  }
}
