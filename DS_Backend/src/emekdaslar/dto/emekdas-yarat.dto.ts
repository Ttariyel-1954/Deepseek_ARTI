import { Type } from 'class-transformer';
import {
  IsBoolean,
  IsDateString,
  IsEmail,
  IsInt,
  IsNumber,
  IsOptional,
  IsString,
  Max,
  MaxLength,
  Min,
  MinLength,
} from 'class-validator';

/**
 * Yeni əməkdaş yaratmaq üçün məlumat (POST /api/v1/emekdaslar).
 *
 * `!` işarəsi TypeScript-ə «bu sahə mütləq doldurulacaq» deyir.
 * Biz onu burada doldurmuruq — dolduran `ValidationPipe`-dır.
 */
export class EmekdasYaratDto {
  @IsString({ message: 'ad mətn olmalıdır' })
  @MinLength(2, { message: 'ad ən azı 2 simvol olmalıdır' })
  @MaxLength(60, { message: 'ad 60 simvoldan uzun ola bilməz' })
  ad!: string;

  @IsString({ message: 'soyad mətn olmalıdır' })
  @MinLength(2, { message: 'soyad ən azı 2 simvol olmalıdır' })
  @MaxLength(60, { message: 'soyad 60 simvoldan uzun ola bilməz' })
  soyad!: string;

  @IsString({ message: 'ata_adi mətn olmalıdır' })
  @MinLength(2, { message: 'ata_adi ən azı 2 simvol olmalıdır' })
  @MaxLength(60, { message: 'ata_adi 60 simvoldan uzun ola bilməz' })
  ata_adi!: string;

  /** 1 = Kişi · 2 = Qadın · 3 = Digər (ortaq.cinsiyyet cədvəli) */
  @Type(() => Number)
  @IsInt({ message: 'cinsiyyet_id tam ədəd olmalıdır' })
  @Min(1, { message: 'cinsiyyet_id ən azı 1 olmalıdır' })
  @Max(3, { message: 'cinsiyyet_id ən çoxu 3 ola bilər' })
  cinsiyyet_id!: number;

  /** Struktur.vezifeler cədvəlindən */
  @Type(() => Number)
  @IsInt({ message: 'vezife_id tam ədəd olmalıdır' })
  @Min(1, { message: 'vezife_id ən azı 1 olmalıdır' })
  vezife_id!: number;

  /** ISO 8601 formatı: YYYY-MM-DD */
  @IsOptional()
  @IsDateString({}, { message: 'dogum_tarixi YYYY-MM-DD formatında olmalıdır' })
  dogum_tarixi?: string;

  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'shobe_id tam ədəd olmalıdır' })
  @Min(1, { message: 'shobe_id ən azı 1 olmalıdır' })
  shobe_id?: number;

  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'merkez_id tam ədəd olmalıdır' })
  @Min(1, { message: 'merkez_id ən azı 1 olmalıdır' })
  merkez_id?: number;

  /** Bazada UNIQUE-dir — təkrar e-poçt 409 xətası verəcək */
  @IsOptional()
  @IsEmail({}, { message: 'email düzgün e-poçt ünvanı olmalıdır' })
  @MaxLength(120, { message: 'email 120 simvoldan uzun ola bilməz' })
  email?: string;

  @IsOptional()
  @IsString({ message: 'telefon mətn olmalıdır' })
  @MaxLength(30, { message: 'telefon 30 simvoldan uzun ola bilməz' })
  telefon?: string;

  /** 1 = Aktiv · 2 = Məzuniyyətdə · … (ortaq.is_statuslari) */
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'is_status_id tam ədəd olmalıdır' })
  @Min(1, { message: 'is_status_id ən azı 1 olmalıdır' })
  @Max(8, { message: 'is_status_id ən çoxu 8 ola bilər' })
  is_status_id?: number;

  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'elmi_derece_id tam ədəd olmalıdır' })
  @Min(1, { message: 'elmi_derece_id ən azı 1 olmalıdır' })
  @Max(4, { message: 'elmi_derece_id ən çoxu 4 ola bilər' })
  elmi_derece_id?: number;

  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'elmi_ad_id tam ədəd olmalıdır' })
  @Min(1, { message: 'elmi_ad_id ən azı 1 olmalıdır' })
  @Max(4, { message: 'elmi_ad_id ən çoxu 4 ola bilər' })
  elmi_ad_id?: number;

  @IsOptional()
  @IsDateString({}, { message: 'ise_baslama YYYY-MM-DD formatında olmalıdır' })
  ise_baslama?: string;

  /** Bazada `maas >= 0` yoxlaması (CHECK constraint) var */
  @IsOptional()
  @Type(() => Number)
  @IsNumber({ maxDecimalPlaces: 2 }, { message: 'maas ədəd olmalıdır (ən çoxu 2 onluq)' })
  @Min(0, { message: 'maas mənfi ola bilməz' })
  @Max(9999999999.99, { message: 'maas həddindən böyükdür' })
  maas?: number;

  @IsOptional()
  @IsBoolean({ message: 'aktiv true və ya false olmalıdır' })
  aktiv?: boolean;
}
