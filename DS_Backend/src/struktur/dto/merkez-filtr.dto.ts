import { ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsBoolean, IsIn, IsOptional } from 'class-validator';
import { SehifeDto } from '../../common/dto/sehife.dto.js';

/** Merkez siyahisi ucun filtr — SehifeDto-dan miras alir */
export class MerkezFiltrDto extends SehifeDto {
  @ApiPropertyOptional({ enum: ['merkez', 'katiblik', 'sobe', 'sektor'] })
  @IsOptional()
  @IsIn(['merkez', 'katiblik', 'sobe', 'sektor'])
  tip?: string;

  @ApiPropertyOptional({ description: 'Yalniz aktiv merkezler' })
  @IsOptional()
  @Type(() => Boolean)
  @IsBoolean()
  aktiv?: boolean;
}
