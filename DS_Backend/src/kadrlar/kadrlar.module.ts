import { Module } from '@nestjs/common';
import { KadrlarService } from './kadrlar.service.js';
import { KadrlarController } from './kadrlar.controller.js';

@Module({
  controllers: [KadrlarController],
  providers: [KadrlarService],
})
export class KadrlarModule {}
