import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, IsString, MaxLength, MinLength } from 'class-validator';

/** Login ucun gelen melumat */
export class LoginDto {
  @ApiProperty({ example: 'admin@arti.edu.az' })
  @IsEmail({}, { message: 'E-poçt ünvanı yanlışdır' })
  @MaxLength(120)
  email!: string;

  @ApiProperty({ example: '123456', minLength: 6 })
  @IsString()
  @MinLength(6, { message: 'Şifrə ən azı 6 simvol olmalıdır' })
  @MaxLength(100)
  parol!: string;
}
