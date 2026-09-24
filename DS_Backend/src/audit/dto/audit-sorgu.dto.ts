import { Type } from 'class-transformer';
import {
  IsIn, IsInt, IsOptional, IsString, Max, MaxLength, Min,
} from 'class-validator';

/** Audit loqunu oxumaq üçün sorğu parametrləri */
export class AuditSorguDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'seife tam ədəd olmalıdır' })
  @Min(1, { message: 'seife ən azı 1 olmalıdır' })
  seife: number = 1;

  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'limit tam ədəd olmalıdır' })
  @Min(1, { message: 'limit ən azı 1 olmalıdır' })
  @Max(200, { message: 'limit 200-dən çox ola bilməz' })
  limit: number = 50;

  /** Yalnız müəyyən cədvəlin qeydləri: `kadrlar.emekdaslar` */
  @IsOptional()
  @IsString({ message: 'cedvel mətn olmalıdır' })
  @MaxLength(80, { message: 'cedvel 80 simvoldan uzun ola bilməz' })
  cedvel?: string;

  /** Yalnız müəyyən əməliyyat: INSERT / UPDATE / DELETE */
  @IsOptional()
  @IsIn(['INSERT', 'UPDATE', 'DELETE'], {
    message: "emeliyyat yalnız 'INSERT', 'UPDATE' və ya 'DELETE' ola bilər",
  })
  emeliyyat?: 'INSERT' | 'UPDATE' | 'DELETE';

  /** `qeyd` və ya `setir_id` üzrə axtarış */
  @IsOptional()
  @IsString({ message: 'axtar mətn olmalıdır' })
  @MaxLength(50, { message: 'axtarış mətni 50 simvoldan uzun ola bilməz' })
  axtar?: string;
}

/** Əl ilə audit qeydi yazmaq üçün */
export class AuditYazDto {
  @IsString({ message: 'cedvel_adi mətn olmalıdır' })
  @MaxLength(80, { message: 'cedvel_adi 80 simvoldan uzun ola bilməz' })
  cedvel_adi!: string;

  @IsIn(['INSERT', 'UPDATE', 'DELETE'], {
    message: "emeliyyat yalnız 'INSERT', 'UPDATE' və ya 'DELETE' ola bilər",
  })
  emeliyyat!: 'INSERT' | 'UPDATE' | 'DELETE';

  @IsOptional()
  @IsString({ message: 'setir_id mətn olmalıdır' })
  @MaxLength(40, { message: 'setir_id 40 simvoldan uzun ola bilməz' })
  setir_id?: string;

  /** ⚠️ BURAYA ŞƏXSİ MƏLUMAT YAZMAYIN — parol, maaş, FIN kod yox! */
  @IsOptional()
  @IsString({ message: 'qeyd mətn olmalıdır' })
  @MaxLength(500, { message: 'qeyd 500 simvoldan uzun ola bilməz' })
  qeyd?: string;

  @IsOptional()
  @IsString({ message: 'istifadeci mətn olmalıdır' })
  @MaxLength(60, { message: 'istifadeci 60 simvoldan uzun ola bilməz' })
  istifadeci?: string;
}
