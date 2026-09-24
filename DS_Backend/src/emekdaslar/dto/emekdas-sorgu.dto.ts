import { Type } from 'class-transformer';
import {
  IsIn,
  IsInt,
  IsOptional,
  IsString,
  Max,
  MaxLength,
  Min,
} from 'class-validator';

/** Sıralana bilən sütunlar — ağ siyahı (whitelist).
 *  ⚠️ Bu siyahı olmasa, istifadəçi istənilən sütun adını göndərib
 *  sorğunu poza bilərdi (SQL injection-un ORM versiyası). */
export const SIRALANA_BILEN = ['soyad', 'ad', 'ise_baslama', 'maas', 'id'] as const;

/**
 * GET /api/v1/emekdaslar üçün sorğu parametrləri.
 *
 * ⚠️ BÜTÜN sahələr istəyə bağlıdır və hər birinin STANDART dəyəri var.
 * Ona görə `GET /api/v1/emekdaslar` (heç bir parametrsiz) də işləyir.
 *
 * URL-dən gələn hər şey MƏTNDİR ("5", "aktiv"). `@Type(() => Number)`
 * onları ədədə çevirir; çevrilməsə `@IsInt()` xəta verir.
 */
export class EmekdasSorguDto {
  /** Neçənci səhifə — 1-dən başlayır */
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'seife tam ədəd olmalıdır' })
  @Min(1, { message: 'seife ən azı 1 olmalıdır' })
  seife: number = 1;

  /** Bir səhifədə neçə sətir — maksimum 100 */
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'limit tam ədəd olmalıdır' })
  @Min(1, { message: 'limit ən azı 1 olmalıdır' })
  @Max(100, { message: 'limit 100-dən çox ola bilməz' })
  limit: number = 20;

  /** Ad, soyad, ata adı və ya e-poçt üzrə axtarış (böyük-kiçik hərf fərqi yoxdur) */
  @IsOptional()
  @IsString({ message: 'axtar mətn olmalıdır' })
  @MaxLength(50, { message: 'axtarış mətni 50 simvoldan uzun ola bilməz' })
  axtar?: string;

  /** Hansı əməkdaşlar göstərilsin */
  @IsOptional()
  @IsIn(['aktiv', 'passiv', 'hamisi'], {
    message: "aktiv yalnız 'aktiv', 'passiv' və ya 'hamisi' ola bilər",
  })
  aktiv: 'aktiv' | 'passiv' | 'hamisi' = 'aktiv';

  /** Hansı sütun üzrə sıralansın */
  @IsOptional()
  @IsIn(SIRALANA_BILEN, {
    message: `siralama yalnız bunlardan biri ola bilər: ${SIRALANA_BILEN.join(', ')}`,
  })
  siralama: string = 'soyad';

  /** Sıralama istiqaməti */
  @IsOptional()
  @IsIn(['asc', 'desc'], { message: "tertib yalnız 'asc' və ya 'desc' ola bilər" })
  tertib: 'asc' | 'desc' = 'asc';

  /** Yalnız müəyyən mərkəzin əməkdaşları */
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'merkez_id tam ədəd olmalıdır' })
  @Min(1, { message: 'merkez_id ən azı 1 olmalıdır' })
  merkez_id?: number;

  /** Yalnız müəyyən şöbənin əməkdaşları */
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'shobe_id tam ədəd olmalıdır' })
  @Min(1, { message: 'shobe_id ən azı 1 olmalıdır' })
  shobe_id?: number;
}
