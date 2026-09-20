import { ExecutionContext, Injectable } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { AuthGuard } from '@nestjs/passport';
import { PUBLIC_ACARI } from '../decorators/public.decorator.js';

/**
 * QLOBAL autentifikasiya guard-i.
 *
 * Butun endpoint-ler qorunur. @Public() ile isarelenmisler istisnadir.
 * Bu, "guvenli susmaya gore" prinsipidir: yeni endpoint elave edende
 * onu qorumaq UCUN heç nə etmek lazim deyil — susmaya gore qorunur.
 */
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private readonly reflector: Reflector) {
    super();
  }

  canActivate(context: ExecutionContext) {
    const publicdir = this.reflector.getAllAndOverride<boolean>(PUBLIC_ACARI, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (publicdir) return true;      // @Public() — burax
    return super.canActivate(context);
  }
}
