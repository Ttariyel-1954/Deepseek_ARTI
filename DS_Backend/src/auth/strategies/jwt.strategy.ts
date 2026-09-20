import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from '@nestjs/config';
import { PrismaService } from '../../prisma/prisma.service.js';
import type { CariIstifadeci } from '../decorators/current-user.decorator.js';

/** JWT tokenin ichindeki melumat */
export interface JwtPayload {
  sub: number;      // istifadeci id
  email: string;
  rol: string;
}

/** Bazadan oxunan istifadeci setri */
interface IstifadeciSetri {
  id: number;
  email: string;
  ad_soyad: string;
  rol: string;
  aktiv: boolean;
}

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy, 'jwt') {
  constructor(
    private readonly prisma: PrismaService,
    config: ConfigService,
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      // EYNI menbe — JwtModule ile: ConfigService
      secretOrKey: config.get<string>('JWT_SECRET')!,
    });
  }

  /**
   * Token DUZGUNDURSE bu metod cagirilir.
   * Burada istifadecinin HELE DE movcud ve aktiv oldugunu yoxlayiriq —
   * eks halda silinmis istifadecinin tokeni 8 saat isleyerdi.
   */
  async validate(payload: JwtPayload): Promise<CariIstifadeci> {
    const setirler = await this.prisma.$queryRaw<IstifadeciSetri[]>`
      SELECT id, email, ad_soyad, rol, aktiv
        FROM kadrlar.istifadeciler
       WHERE id = ${payload.sub}`;

    const istifadeci = setirler[0];

    if (!istifadeci) {
      throw new UnauthorizedException('İstifadəçi tapılmadı');
    }
    if (!istifadeci.aktiv) {
      throw new UnauthorizedException('İstifadəçi deaktiv edilib');
    }

    return {
      id: istifadeci.id,
      email: istifadeci.email,
      ad_soyad: istifadeci.ad_soyad,
      rol: istifadeci.rol,
    };
  }
}
