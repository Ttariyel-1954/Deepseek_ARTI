import { Module } from '@nestjs/common';
import { HesabatlarService } from './hesabatlar.service.js';
import { HesabatlarController } from './hesabatlar.controller.js';

@Module({
  controllers: [HesabatlarController],
  providers: [HesabatlarService],
})
export class HesabatlarModule {}
