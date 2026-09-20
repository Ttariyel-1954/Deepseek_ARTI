import { Body, Controller, Get, HttpCode, HttpStatus, Post } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';
import { AuthService } from './auth.service.js';
import { LoginDto } from './dto/login.dto.js';
import { QeydiyyatDto } from './dto/qeydiyyat.dto.js';
import { Public } from './decorators/public.decorator.js';
import { Roles } from './decorators/roles.decorator.js';
import { CurrentUser } from './decorators/current-user.decorator.js';
import type { CariIstifadeci } from './decorators/current-user.decorator.js';

@ApiTags('auth')
@Controller('auth')
export class AuthController {
  constructor(private readonly auth: AuthService) {}

  @Public()
  @Post('login')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Giriş — JWT token al' })
  @ApiResponse({ status: 200, description: 'Token qaytarildi' })
  @ApiResponse({ status: 401, description: 'E-poçt və ya şifrə yanlışdır' })
  login(@Body() dto: LoginDto) {
    return this.auth.login(dto);
  }

  @Get('profil')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Cari istifadecinin profili' })
  profil(@CurrentUser() istifadeci: CariIstifadeci) {
    return istifadeci;
  }

  @Post('qeydiyyat')
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Yeni istifadeci yarat (yalniz admin)' })
  @ApiResponse({ status: 409, description: 'Bu e-poçt artıq var' })
  qeydiyyat(@Body() dto: QeydiyyatDto) {
    return this.auth.qeydiyyat(dto);
  }

  @Get('istifadeciler')
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Butun istifadeciler (yalniz admin)' })
  siyahi() {
    return this.auth.siyahi();
  }
}
