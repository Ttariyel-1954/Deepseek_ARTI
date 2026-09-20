import { SetMetadata } from '@nestjs/common';
import { Rol } from '../dto/qeydiyyat.dto.js';

export const ROLLAR_ACARI = 'rollar';

/**
 * Endpoint-e hansi rollarin gire bileceyini teyin edir.
 *
 *   @Roles('admin', 'maliyyeci')
 *   @Get('hesabat')
 */
export const Roles = (...rollar: Rol[]) => SetMetadata(ROLLAR_ACARI, rollar);
