import { Type } from 'class-transformer';
import {
  IsIn, IsInt, IsOptional, IsString, Max, MaxLength, Min,
} from 'class-validator';
import { ApiPropertyOptional } from '@nestjs/swagger';

/**
 * Sehifelme + filtr + siralama ucun ORTAQ DTO.
 * Butun siyahi endpoint-leri bundan miras alir.
 */
export class SehifeDto {
  @ApiPropertyOptional({ default: 1, minimum: 1, description: 'Sehife nomresi' })
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'sehife tam eded olmalidir' })
  @Min(1, { message: 'sehife 1-den kicik ola bilmez' })
  sehife: number = 1;

  @ApiPropertyOptional({ default: 20, minimum: 1, maximum: 100 })
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'limit tam eded olmalidir' })
  @Min(1)
  @Max(100, { message: 'limit 100-den cox ola bilmez' })
  limit: number = 20;

  @ApiPropertyOptional({ description: 'Metn axtarisi (ad, soyad, e-mail)' })
  @IsOptional()
  @IsString()
  @MaxLength(100)
  axtar?: string;

  @ApiPropertyOptional({ enum: ['asc', 'desc'], default: 'asc' })
  @IsOptional()
  @IsIn(['asc', 'desc'], { message: 'siralama yalniz asc ve ya desc ola biler' })
  siralama: 'asc' | 'desc' = 'asc';

  @ApiPropertyOptional({ description: 'Siralama sutunu' })
  @IsOptional()
  @IsString()
  @MaxLength(40)
  siralama_sah?: string;

  /** SQL OFFSET — hesablanmis xassə (DTO-da sorgu parametri deyil) */
  get offset(): number {
    return (this.sehife - 1) * this.limit;
  }
}

/** Sehifelenmis cavabin standart formasi */
export interface Sehifelenmis<T> {
  data: T[];
  meta: {
    sehife: number;
    limit: number;
    cem: number;
    sehife_sayi: number;
  };
}
