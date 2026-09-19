import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import {
  IsBoolean, IsEmail, IsIn, IsOptional, IsString,
  Matches, MaxLength, MinLength,
} from 'class-validator';

/** Yeni merkez yaratmaq ucun gelen melumat */
export class CreateMerkezDto {
  @ApiProperty({ example: 'Elmi-pedaqoji tedqiqatlar merkezi' })
  @IsString()
  @MinLength(3, { message: 'Ad ən azı 3 simvol olmalıdır' })
  @MaxLength(200)
  ad!: string;

  @ApiPropertyOptional({ enum: ['merkez', 'katiblik', 'sobe', 'sektor'] })
  @IsOptional()
  @IsIn(['merkez', 'katiblik', 'sobe', 'sektor'], {
    message: 'tip yalniz: merkez, katiblik, sobe, sektor',
  })
  tip?: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  @MaxLength(500)
  tesvir?: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  @MaxLength(300)
  unvan?: string;

  @ApiPropertyOptional({ example: '+994 12 599 08 08' })
  @IsOptional()
  @Matches(/^\+?[0-9\s()-]{7,25}$/, {
    message: 'Telefon formati yanlışdır (+994 12 599 08 08)',
  })
  telefon?: string;

  @ApiPropertyOptional({ example: 'tedqiqat@arti.edu.az' })
  @IsOptional()
  @IsEmail({}, { message: 'E-poçt ünvanı yanlışdır' })
  @MaxLength(120)
  email?: string;

  @ApiPropertyOptional({ example: '2024-02-15' })
  @IsOptional()
  @Matches(/^\d{4}-\d{2}-\d{2}$/, {
    message: 'Tarix IL-AY-GUN formatinda olmalidir (2024-02-15)',
  })
  yaradilma_tarixi?: string;

  @ApiPropertyOptional({ default: true })
  @IsOptional()
  @IsBoolean()
  aktiv?: boolean;
}
