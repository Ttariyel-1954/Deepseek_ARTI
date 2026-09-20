import { Module } from '@nestjs/common';
import { IxracService } from './ixrac.service.js';
import { IxracController } from './ixrac.controller.js';

@Module({
  controllers: [IxracController],
  providers: [IxracService],
  exports: [IxracService],
})
export class IxracModule {}
