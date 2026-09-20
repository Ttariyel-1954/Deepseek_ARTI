import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsBoolean, IsInt, IsOptional, IsString, Max, MaxLength, Min, MinLength } from 'class-validator';

/** AI-a verilen sual */
export class SualDto {
  @ApiProperty({ example: 'ARTİ-də 2026-cı ildə neçə əməkdaş var?' })
  @IsString()
  @MinLength(3, { message: 'Sual ən azı 3 simvol olmalıdır' })
  @MaxLength(1000)
  sual!: string;

  @ApiPropertyOptional({ description: 'Prompt şablonunun adı' })
  @IsOptional()
  @IsString()
  @MaxLength(120)
  prompt?: string;

  @ApiPropertyOptional({ default: false, description: 'Verilənlər bazası kontekstini əlavə et' })
  @IsOptional()
  @IsBoolean()
  kontekst?: boolean;
}

/** Təbii dil → struktur niyyət (SQL YOX!) */
export class SqlSualDto {
  @ApiProperty({ example: 'Ən çox maaş alan 5 əməkdaşı göstər' })
  @IsString()
  @MinLength(3)
  @MaxLength(500)
  sual!: string;

  @ApiPropertyOptional({ default: 20, maximum: 100 })
  @IsOptional()
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number;
}
