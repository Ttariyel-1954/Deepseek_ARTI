import { createParamDecorator, ExecutionContext } from '@nestjs/common';

/** JWT-dən cixarilan istifadeci melumati */
export interface CariIstifadeci {
  id: number;
  email: string;
  ad_soyad: string;
  rol: string;
}

/**
 * Cari istifadecini controller metoduna oturur.
 *
 *   @Get('profil')
 *   profil(@CurrentUser() istifadeci: CariIstifadeci) { ... }
 */
export const CurrentUser = createParamDecorator(
  (sahe: keyof CariIstifadeci | undefined, ctx: ExecutionContext) => {
    const sorqu = ctx.switchToHttp().getRequest();
    const istifadeci = sorqu.user as CariIstifadeci | undefined;
    if (!istifadeci) return undefined;
    return sahe ? istifadeci[sahe] : istifadeci;
  },
);
