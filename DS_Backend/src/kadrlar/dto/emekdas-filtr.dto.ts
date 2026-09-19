import { ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import {
  IsBoolean, IsInt, IsNumber, IsOptional, Max, Min,
} from 'class-validator';
import { SehifeDto } from '../../common/dto/sehife.dto.js';

/** Emekdas siyahisi ucun filtr */
export class EmekdasFiltrDto extends SehifeDto {
  @ApiPropertyOptional({ description: 'Merkez id' })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  merkez_id?: number;

  @ApiPropertyOptional({ description: 'Shobe id' })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  shobe_id?: number;

  @ApiPropertyOptional({ description: 'Vezife id' })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  vezife_id?: number;

  @ApiPropertyOptional({ description: 'Elmi derece id' })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  elmi_derece_id?: number;

  @ApiPropertyOptional({ description: 'Yalniz aktiv emekdaslar' })
  @IsOptional()
  @Type(() => Boolean)
  @IsBoolean()
  aktiv?: boolean;

  @ApiPropertyOptional({ description: 'Minimum maas', example: 1500 })
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  @Min(0)
  min_maas?: number;

  @ApiPropertyOptional({ description: 'Maksimum maas', example: 4000 })
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  @Min(0)
  @Max(100000)
  max_maas?: number;
}
