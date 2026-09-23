import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service.js';

/**
 * @Global() — bu modulu HƏR modulda yenidən import etmək lazım deyil.
 * PrismaService bütün layihədə bir dənədir (singleton).
 */
@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
