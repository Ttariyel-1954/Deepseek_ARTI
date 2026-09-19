import { PartialType } from '@nestjs/swagger';
import { CreateMerkezDto } from './create-merkez.dto.js';

/**
 * Yenileme DTO-su — butun saheler OPSIONALDIR.
 * PartialType CreateMerkezDto-nun butun qaydalarini miras alir,
 * lakin her saheni optional edir.
 */
export class UpdateMerkezDto extends PartialType(CreateMerkezDto) {}
