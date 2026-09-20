import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import {
  IsEmail, IsIn, IsInt, IsOptional, IsString,
  MaxLength, MinLength,
} from 'class-validator';

/** ROL — sistemde movcud olan 4 rol */
export const ROLLAR = ['admin', 'muhendis', 'maliyyeci', 'baxici'] as const;
export type Rol = (typeof ROLLAR)[number];

/** Yeni istifadeci yaratmaq ucun */
export class QeydiyyatDto {
  @ApiProperty({ example: 'yeni@arti.edu.az' })
  @IsEmail({}, { message: 'E-poçt ünvanı yanlışdır' })
  @MaxLength(120)
  email!: string;

  @ApiProperty({ example: 'guclu-sifre-2026', minLength: 8 })
  @IsString()
  @MinLength(8, { message: 'Şifrə ən azı 8 simvol olmalıdır' })
  @MaxLength(100)
  parol!: string;

  @ApiProperty({ example: 'Əliyev Kamran' })
  @IsString()
  @MinLength(3, { message: 'Ad-soyad ən azı 3 simvol olmalıdır' })
  @MaxLength(150)
  ad_soyad!: string;

  @ApiPropertyOptional({ enum: ROLLAR, default: 'baxici' })
  @IsOptional()
  @IsIn(ROLLAR as unknown as string[], {
    message: 'rol yalnız: admin, muhendis, maliyyeci, baxici',
  })
  rol?: Rol;

  @ApiPropertyOptional({ description: 'Bagli emekdas id (varsa)' })
  @IsOptional()
  @IsInt()
  emekdas_id?: number;
}
