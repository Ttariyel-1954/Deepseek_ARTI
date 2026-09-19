import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module.js';
import { StrukturModule } from './struktur/struktur.module.js';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),   // .env oxuyur
    PrismaModule,                                // @Global() — baza
    StrukturModule,                              // <- YENI MODUL
  ],
})
export class AppModule {}
