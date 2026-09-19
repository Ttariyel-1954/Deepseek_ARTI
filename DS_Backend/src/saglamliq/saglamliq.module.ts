import { Module } from '@nestjs/common';
import { SaglamliqController } from './saglamliq.controller.js';

@Module({ controllers: [SaglamliqController] })
export class SaglamliqModule {}
