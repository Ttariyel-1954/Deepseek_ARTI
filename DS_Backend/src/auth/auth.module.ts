import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { AuthService } from './auth.service.js';
import { AuthController } from './auth.controller.js';
import { JwtStrategy } from './strategies/jwt.strategy.js';
import type { SignOptions } from 'jsonwebtoken';

@Module({
  imports: [
    PassportModule,
    /*
     * registerAsync MÜTLƏQDİR — register() YOX.
     *
     * Sebeb: JwtModule.register({...}) modul YUKLENENDE icra olunur,
     * yeni .env hele oxunmamis olur. Netice: acar "undefined" olur ve
     * fallback deyer istifade olunur.
     *
     * registerAsync ise ConfigModule hazir olandan SONRA isleyir.
     */
    JwtModule.registerAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        secret: config.get<string>('JWT_SECRET'),
        signOptions: {
          expiresIn: (config.get<string>('JWT_MUDDET') ?? '8h') as SignOptions['expiresIn'],
        },
      }),
    }),
  ],
  controllers: [AuthController],
  providers: [AuthService, JwtStrategy],
})
export class AuthModule {}
