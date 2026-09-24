import { Type } from 'class-transformer';
import {
  ArrayMaxSize,
  ArrayMinSize,
  IsArray,
  IsBoolean,
  IsInt,
  IsNumber,
  IsOptional,
  Max,
  Min,
  ValidateNested,
} from 'class-validator';
import { EmekdasYaratDto } from '../../dto/emekdas-yarat.dto.js';

/**
 * Bir sorğuda bir neçə əməkdaş yaratmaq.
 *
 * ⚠️ `@ValidateNested({ each: true })` + `@Type(() => ...)` CÜTLÜYÜ
 * mütləqdir:
 *   • `@Type` — xam JSON massivini `EmekdasYaratDto` NÜSXƏLƏRİNƏ çevirir.
 *   • `@ValidateNested({ each: true })` — hər nüsxəni AYRICA yoxlayır.
 * Yalnız `@IsArray()` yazsaq, massivin elementləri yoxlanılmaz və
 * bazaya zibil düşər.
 */
export class TopluYaratDto {
  @IsArray({ message: 'emekdaslar massiv olmalıdır' })
  @ArrayMinSize(1, { message: 'ən azı 1 əməkdaş göndərilməlidir' })
  @ArrayMaxSize(50, { message: 'bir sorğuda ən çoxu 50 əməkdaş ola bilər' })
  @ValidateNested({ each: true })
  @Type(() => EmekdasYaratDto)
  emekdaslar!: EmekdasYaratDto[];

  /** E-poçtu təkrar olan sətirləri xəta vermədən ATLA */
  @IsOptional()
  @IsBoolean({ message: 'tekrarlariAtla true və ya false olmalıdır' })
  tekrarlariAtla?: boolean;
}

/**
 * Bir neçə əməkdaşın aktivliyini dəyişmək.
 *
 * ⚠️ `idler` MÜTLƏQdir və boş ola bilməz. Bu, qoruyucu dizayn qərarıdır:
 * «filtrsiz toplu əməliyyat» təsadüfən BÜTÜN cədvəli dəyişə bilər.
 */
export class TopluAktivlikDto {
  @IsArray({ message: 'idler massiv olmalıdır' })
  @ArrayMinSize(1, { message: 'ən azı 1 ID göndərilməlidir' })
  @ArrayMaxSize(100, { message: 'bir sorğuda ən çoxu 100 ID ola bilər' })
  @IsInt({ each: true, message: 'hər ID tam ədəd olmalıdır' })
  @Min(1, { each: true, message: 'hər ID ən azı 1 olmalıdır' })
  @Type(() => Number)
  idler!: number[];

  @IsBoolean({ message: 'aktiv true və ya false olmalıdır' })
  aktiv!: boolean;
}

/**
 * Toplu maaş artımı.
 *
 * ⚠️ `idler`, `merkez_id` və `vezife_id` — üçündən ƏN AZI BİRİ
 * verilməlidir. Bu yoxlama servisdədir (DTO-da «ən azı biri» qaydası
 * yazmaq olar, amma mesaj daha aydın olur servisdə).
 */
export class MaasArtimDto {
  /** Neçə faiz? Mənfi də ola bilər (endirim), amma -50-dən aşağı yox */
  @Type(() => Number)
  @IsNumber({ maxDecimalPlaces: 2 }, { message: 'faiz ədəd olmalıdır' })
  @Min(-50, { message: 'faiz -50-dən kiçik ola bilməz' })
  @Max(100, { message: 'faiz 100-dən böyük ola bilməz' })
  faiz!: number;

  @IsOptional()
  @IsArray({ message: 'idler massiv olmalıdır' })
  @ArrayMinSize(1, { message: 'idler boş ola bilməz' })
  @ArrayMaxSize(100, { message: 'bir sorğuda ən çoxu 100 ID ola bilər' })
  @IsInt({ each: true, message: 'hər ID tam ədəd olmalıdır' })
  @Min(1, { each: true, message: 'hər ID ən azı 1 olmalıdır' })
  @Type(() => Number)
  idler?: number[];

  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'merkez_id tam ədəd olmalıdır' })
  @Min(1, { message: 'merkez_id ən azı 1 olmalıdır' })
  merkez_id?: number;

  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'vezife_id tam ədəd olmalıdır' })
  @Min(1, { message: 'vezife_id ən azı 1 olmalıdır' })
  vezife_id?: number;
}
