import { Module } from '@nestjs/common';
import { StrukturService } from './struktur.service.js';
import { StrukturController } from './struktur.controller.js';

@Module({
  controllers: [StrukturController],
  providers: [StrukturService],
})
export class StrukturModule {}
