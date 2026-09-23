import { Module } from '@nestjs/common';
import { SaglamliqController } from './saglamliq.controller.js';
import { SaglamliqService } from './saglamliq.service.js';

@Module({
  controllers: [SaglamliqController],
  providers: [SaglamliqService],
})
export class SaglamliqModule {}
