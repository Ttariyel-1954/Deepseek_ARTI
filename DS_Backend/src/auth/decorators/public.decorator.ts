import { SetMetadata } from '@nestjs/common';

export const PUBLIC_ACARI = 'publicdir';

/**
 * Endpoint-i autentifikasiyadan AZAD edir.
 *
 * Qlobal JwtAuthGuard butun endpoint-leri qoruyur.
 * Login ve saglamliq kimi endpoint-ler ucun bu lazimdir.
 *
 *   @Public()
 *   @Post('login')
 */
export const Public = () => SetMetadata(PUBLIC_ACARI, true);
