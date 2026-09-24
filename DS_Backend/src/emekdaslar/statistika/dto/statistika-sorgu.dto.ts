import { Type } from 'class-transformer';
import { IsIn, IsInt, IsOptional, Max, Min } from 'class-validator';

/** Statistika üçün ümumi sorğu parametrləri */
export class StatistikaSorguDto {
  /** Yalnız aktiv əməkdaşları say, yoxsa hamısını? */
  @IsOptional()
  @IsIn(['aktiv', 'hamisi'], {
    message: "aktiv yalnız 'aktiv' və ya 'hamisi' ola bilər",
  })
  aktiv: 'aktiv' | 'hamisi' = 'aktiv';

  /** Neçə sətirdən az olan qruplar göstərilməsin */
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'min_say tam ədəd olmalıdır' })
  @Min(1, { message: 'min_say ən azı 1 olmalıdır' })
  @Max(50, { message: 'min_say 50-dən çox ola bilməz' })
  min_say: number = 1;

  /** Sıralama: say üzrə, yoxsa ad üzrə? */
  @IsOptional()
  @IsIn(['say', 'ad', 'orta_maas'], {
    message: "siralama yalnız 'say', 'ad' və ya 'orta_maas' ola bilər",
  })
  siralama: 'say' | 'ad' | 'orta_maas' = 'say';
}
