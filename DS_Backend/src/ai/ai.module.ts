import { Module } from '@nestjs/common';
import { AiService } from './ai.service.js';
import { RagService } from './rag.service.js';
import { SqlKomlekciService } from './sql-komlekci.service.js';
import { AiController } from './ai.controller.js';

@Module({
  controllers: [AiController],
  providers: [AiService, RagService, SqlKomlekciService],
  exports: [AiService, RagService],
})
export class AiModule {}
