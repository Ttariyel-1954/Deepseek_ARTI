import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module.js';
import { SaglamliqModule } from './saglamliq/saglamliq.module.js';
import { EmekdaslarModule } from './emekdaslar/emekdaslar.module.js';

@Module({
  imports: [
    // .env faylını oxuyur və BÜTÜN layihə üçün əlçatan edir.
    // isGlobal: true — hər modulda yenidən import etmək lazım deyil.
    ConfigModule.forRoot({ isGlobal: true }),

    PrismaModule,
    SaglamliqModule,
    EmekdaslarModule,
  ],
})
export class AppModule {}
