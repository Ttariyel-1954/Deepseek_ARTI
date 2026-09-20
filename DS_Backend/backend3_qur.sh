#!/bin/bash
# ═══════════════════════════════════════════════════════════
#  DS_Backend-3 — JWT, rollar, audit: butun fayllar
#  Istifade:  bash backend3_qur.sh
# ═══════════════════════════════════════════════════════════
set -e

cd ~/Deepseek_ARTI/DS_Backend || { echo "XETA: DS_Backend tapilmadi"; exit 1; }
if [ ! -f package.json ]; then echo "XETA: package.json yoxdur"; exit 1; fi

echo "════ 1/5  Paketler ════"
unset DATABASE_URL PGHOST
npm install @nestjs/jwt@^12.0.0 @nestjs/passport@^12.0.0 \
  passport@^0.7.0 passport-jwt@^4.0.1 bcryptjs@^3.0.0 2>&1 | tail -2
npm install -D @types/passport-jwt@^4.0.1 @types/bcryptjs@^2.4.6 tsx@^4.19.0 2>&1 | tail -2

echo "════ 2/5  Qovluqlar ════"
mkdir -p "scripts"
mkdir -p "src"
mkdir -p "src/auth"
mkdir -p "src/auth/decorators"
mkdir -p "src/auth/dto"
mkdir -p "src/auth/guards"
mkdir -p "src/auth/strategies"
mkdir -p "src/common/interceptors"
mkdir -p "src/saglamliq"
mkdir -p "src/struktur"
mkdir -p "test"
echo "  11 qovluq hazirdir"

echo "════ 3/5  Fayllar ════"

cat > "src/auth/dto/login.dto.ts" <<'KODSON'
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
KODSON
echo "  ✓ src/auth/dto/login.dto.ts"

cat > "src/auth/dto/qeydiyyat.dto.ts" <<'KODSON'
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import {
  IsEmail, IsIn, IsInt, IsOptional, IsString,
  MaxLength, MinLength,
} from 'class-validator';

/** ROL — sistemde movcud olan 4 rol */
export const ROLLAR = ['admin', 'muhendis', 'maliyyeci', 'baxici'] as const;
export type Rol = (typeof ROLLAR)[number];

/** Yeni istifadeci yaratmaq ucun */
export class QeydiyyatDto {
  @ApiProperty({ example: 'yeni@arti.edu.az' })
  @IsEmail({}, { message: 'E-poçt ünvanı yanlışdır' })
  @MaxLength(120)
  email!: string;

  @ApiProperty({ example: 'guclu-sifre-2026', minLength: 8 })
  @IsString()
  @MinLength(8, { message: 'Şifrə ən azı 8 simvol olmalıdır' })
  @MaxLength(100)
  parol!: string;

  @ApiProperty({ example: 'Əliyev Kamran' })
  @IsString()
  @MinLength(3, { message: 'Ad-soyad ən azı 3 simvol olmalıdır' })
  @MaxLength(150)
  ad_soyad!: string;

  @ApiPropertyOptional({ enum: ROLLAR, default: 'baxici' })
  @IsOptional()
  @IsIn(ROLLAR as unknown as string[], {
    message: 'rol yalnız: admin, muhendis, maliyyeci, baxici',
  })
  rol?: Rol;

  @ApiPropertyOptional({ description: 'Bagli emekdas id (varsa)' })
  @IsOptional()
  @IsInt()
  emekdas_id?: number;
}
KODSON
echo "  ✓ src/auth/dto/qeydiyyat.dto.ts"

cat > "src/auth/decorators/roles.decorator.ts" <<'KODSON'
import { SetMetadata } from '@nestjs/common';
import { Rol } from '../dto/qeydiyyat.dto.js';

export const ROLLAR_ACARI = 'rollar';

/**
 * Endpoint-e hansi rollarin gire bileceyini teyin edir.
 *
 *   @Roles('admin', 'maliyyeci')
 *   @Get('hesabat')
 */
export const Roles = (...rollar: Rol[]) => SetMetadata(ROLLAR_ACARI, rollar);
KODSON
echo "  ✓ src/auth/decorators/roles.decorator.ts"

cat > "src/auth/decorators/public.decorator.ts" <<'KODSON'
import { SetMetadata } from '@nestjs/common';

export const PUBLIC_ACARI = 'publicdir';

/**
 * Endpoint-i autentifikasiyadan AZAD edir.
 *
 * Qlobal JwtAuthGuard butun endpoint-leri qoruyur.
 * Login ve saglamliq kimi endpoint-ler ucun bu lazimdir.
 *
 *   @Public()
 *   @Post('login')
 */
export const Public = () => SetMetadata(PUBLIC_ACARI, true);
KODSON
echo "  ✓ src/auth/decorators/public.decorator.ts"

cat > "src/auth/decorators/current-user.decorator.ts" <<'KODSON'
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

/** JWT-dən cixarilan istifadeci melumati */
export interface CariIstifadeci {
  id: number;
  email: string;
  ad_soyad: string;
  rol: string;
}

/**
 * Cari istifadecini controller metoduna oturur.
 *
 *   @Get('profil')
 *   profil(@CurrentUser() istifadeci: CariIstifadeci) { ... }
 */
export const CurrentUser = createParamDecorator(
  (sahe: keyof CariIstifadeci | undefined, ctx: ExecutionContext) => {
    const sorqu = ctx.switchToHttp().getRequest();
    const istifadeci = sorqu.user as CariIstifadeci | undefined;
    if (!istifadeci) return undefined;
    return sahe ? istifadeci[sahe] : istifadeci;
  },
);
KODSON
echo "  ✓ src/auth/decorators/current-user.decorator.ts"

cat > "src/auth/strategies/jwt.strategy.ts" <<'KODSON'
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from '@nestjs/config';
import { PrismaService } from '../../prisma/prisma.service.js';
import type { CariIstifadeci } from '../decorators/current-user.decorator.js';

/** JWT tokenin ichindeki melumat */
export interface JwtPayload {
  sub: number;      // istifadeci id
  email: string;
  rol: string;
}

/** Bazadan oxunan istifadeci setri */
interface IstifadeciSetri {
  id: number;
  email: string;
  ad_soyad: string;
  rol: string;
  aktiv: boolean;
}

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy, 'jwt') {
  constructor(
    private readonly prisma: PrismaService,
    config: ConfigService,
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      // EYNI menbe — JwtModule ile: ConfigService
      secretOrKey: config.get<string>('JWT_SECRET')!,
    });
  }

  /**
   * Token DUZGUNDURSE bu metod cagirilir.
   * Burada istifadecinin HELE DE movcud ve aktiv oldugunu yoxlayiriq —
   * eks halda silinmis istifadecinin tokeni 8 saat isleyerdi.
   */
  async validate(payload: JwtPayload): Promise<CariIstifadeci> {
    const setirler = await this.prisma.$queryRaw<IstifadeciSetri[]>`
      SELECT id, email, ad_soyad, rol, aktiv
        FROM kadrlar.istifadeciler
       WHERE id = ${payload.sub}`;

    const istifadeci = setirler[0];

    if (!istifadeci) {
      throw new UnauthorizedException('İstifadəçi tapılmadı');
    }
    if (!istifadeci.aktiv) {
      throw new UnauthorizedException('İstifadəçi deaktiv edilib');
    }

    return {
      id: istifadeci.id,
      email: istifadeci.email,
      ad_soyad: istifadeci.ad_soyad,
      rol: istifadeci.rol,
    };
  }
}
KODSON
echo "  ✓ src/auth/strategies/jwt.strategy.ts"

cat > "src/auth/guards/jwt-auth.guard.ts" <<'KODSON'
import { ExecutionContext, Injectable } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { AuthGuard } from '@nestjs/passport';
import { PUBLIC_ACARI } from '../decorators/public.decorator.js';

/**
 * QLOBAL autentifikasiya guard-i.
 *
 * Butun endpoint-ler qorunur. @Public() ile isarelenmisler istisnadir.
 * Bu, "guvenli susmaya gore" prinsipidir: yeni endpoint elave edende
 * onu qorumaq UCUN heç nə etmek lazim deyil — susmaya gore qorunur.
 */
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private readonly reflector: Reflector) {
    super();
  }

  canActivate(context: ExecutionContext) {
    const publicdir = this.reflector.getAllAndOverride<boolean>(PUBLIC_ACARI, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (publicdir) return true;      // @Public() — burax
    return super.canActivate(context);
  }
}
KODSON
echo "  ✓ src/auth/guards/jwt-auth.guard.ts"

cat > "src/auth/guards/roles.guard.ts" <<'KODSON'
import {
  CanActivate, ExecutionContext, ForbiddenException, Injectable,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { ROLLAR_ACARI } from '../decorators/roles.decorator.js';
import { Rol } from '../dto/qeydiyyat.dto.js';

/**
 * RBAC — Role-Based Access Control.
 * @Roles(...) ile isarelenmis endpoint-e yalniz hemin rollar gire biler.
 */
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const teleb = this.reflector.getAllAndOverride<Rol[]>(ROLLAR_ACARI, [
      context.getHandler(),
      context.getClass(),
    ]);

    // @Roles yoxdursa — her bir autentifikasiya olunmus istifadeci gire biler
    if (!teleb || teleb.length === 0) return true;

    const sorqu = context.switchToHttp().getRequest();
    const istifadeci = sorqu.user as { rol?: string } | undefined;

    if (!istifadeci?.rol) {
      throw new ForbiddenException('İstifadəçi rolu müəyyən deyil');
    }

    // 'admin' HER SEYE icazelidir — super-rol
    if (istifadeci.rol === 'admin') return true;

    if (!teleb.includes(istifadeci.rol as Rol)) {
      throw new ForbiddenException(
        `Bu əməliyyat üçün icazəniz yoxdur. ` +
        `Tələb olunan rol: ${teleb.join(' və ya ')}. Sizin rol: ${istifadeci.rol}`,
      );
    }

    return true;
  }
}
KODSON
echo "  ✓ src/auth/guards/roles.guard.ts"

cat > "src/auth/auth.module.ts" <<'KODSON'
import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { AuthService } from './auth.service.js';
import { AuthController } from './auth.controller.js';
import { JwtStrategy } from './strategies/jwt.strategy.js';
import type { SignOptions } from 'jsonwebtoken';

@Module({
  imports: [
    PassportModule,
    /*
     * registerAsync MÜTLƏQDİR — register() YOX.
     *
     * Sebeb: JwtModule.register({...}) modul YUKLENENDE icra olunur,
     * yeni .env hele oxunmamis olur. Netice: acar "undefined" olur ve
     * fallback deyer istifade olunur.
     *
     * registerAsync ise ConfigModule hazir olandan SONRA isleyir.
     */
    JwtModule.registerAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        secret: config.get<string>('JWT_SECRET'),
        signOptions: {
          expiresIn: (config.get<string>('JWT_MUDDET') ?? '8h') as SignOptions['expiresIn'],
        },
      }),
    }),
  ],
  controllers: [AuthController],
  providers: [AuthService, JwtStrategy],
})
export class AuthModule {}
KODSON
echo "  ✓ src/auth/auth.module.ts"

cat > "src/auth/auth.service.ts" <<'KODSON'
import {
  ConflictException, Injectable, Logger, UnauthorizedException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcryptjs';
import { PrismaService } from '../prisma/prisma.service.js';
import { LoginDto } from './dto/login.dto.js';
import { QeydiyyatDto } from './dto/qeydiyyat.dto.js';
import type { JwtPayload } from './strategies/jwt.strategy.js';

/** Bazadan oxunan istifadeci setri (parol_hash DAXIL) */
interface IstifadeciSetri {
  id: number;
  email: string;
  parol_hash: string;
  ad_soyad: string;
  rol: string;
  emekdas_id: number | null;
  aktiv: boolean;
}

/** Xarice qaytarilan istifadeci melumati (parol YOX) */
export interface IstifadeciCavabi {
  id: number;
  email: string;
  ad_soyad: string;
  rol: string;
  emekdas_id: number | null;
}

export interface LoginCavabi {
  token: string;
  istifadeci: IstifadeciCavabi;
  bitme: string;
}

/** bcrypt "cost" — ne qeder boyukdurse, o qeder yavas ve guvenli */
const BCRYPT_RAUND = 10;

@Injectable()
export class AuthService {
  private readonly log = new Logger('AUTH');

  constructor(
    private readonly prisma: PrismaService,
    private readonly jwt: JwtService,
  ) {}

  /** E-poçt + şifrə ile giriş */
  async login(dto: LoginDto): Promise<LoginCavabi> {
    const setirler = await this.prisma.$queryRaw<IstifadeciSetri[]>`
      SELECT id, email, parol_hash, ad_soyad, rol, emekdas_id, aktiv
        FROM kadrlar.istifadeciler
       WHERE lower(email) = lower(${dto.email})`;

    const istifadeci = setirler[0];

    /*
     * TEHLUKESIZLIK: e-poct tapilmasa da, sifre yoxlamasi APARILIR.
     * Sebeb: cavab vaxtina gore "bu email movcuddurmu?" oyrenile biler
     * (timing attack). Ona gore saxta hash ile muqayise edirik.
     */
    const hash = istifadeci?.parol_hash ?? SAXTA_HASH;
    const duzdur = await bcrypt.compare(dto.parol, hash);

    if (!istifadeci || !duzdur) {
      this.log.warn(`Ugursuz giris cehdi: ${dto.email}`);
      /*
       * EYNI mesaj — hem "email yoxdur", hem "sifre sehvdir" ucun.
       * Eks halda istifadeci siyahisi oyrenile biler (user enumeration).
       */
      throw new UnauthorizedException('E-poçt və ya şifrə yanlışdır');
    }

    if (!istifadeci.aktiv) {
      throw new UnauthorizedException('İstifadəçi deaktiv edilib');
    }

    const payload: JwtPayload = {
      sub: istifadeci.id,
      email: istifadeci.email,
      rol: istifadeci.rol,
    };

    const token = await this.jwt.signAsync(payload);
    const muddet = process.env.JWT_MUDDET ?? '8h';

    this.log.log(`Giris ugurlu: ${istifadeci.email} (${istifadeci.rol})`);

    return {
      token,
      istifadeci: this.temizle(istifadeci),
      bitme: muddet,
    };
  }

  /** Yeni istifadeci yarat */
  async qeydiyyat(dto: QeydiyyatDto): Promise<IstifadeciCavabi> {
    const movcud = await this.prisma.$queryRaw<{ id: number }[]>`
      SELECT id::int FROM kadrlar.istifadeciler
       WHERE lower(email) = lower(${dto.email})`;

    if (movcud.length) {
      throw new ConflictException(`Bu e-poçt artıq qeydiyyatdadır: ${dto.email}`);
    }

    if (dto.emekdas_id) {
      const e = await this.prisma.$queryRaw<{ id: number }[]>`
        SELECT id::int FROM kadrlar.emekdaslar WHERE id = ${dto.emekdas_id}`;
      if (!e.length) {
        throw new ConflictException(`Əməkdaş tapılmadı: id=${dto.emekdas_id}`);
      }
    }

    const hash = await bcrypt.hash(dto.parol, BCRYPT_RAUND);

    const setirler = await this.prisma.$queryRaw<IstifadeciSetri[]>`
      INSERT INTO kadrlar.istifadeciler
        (email, parol_hash, ad_soyad, rol, emekdas_id, aktiv)
      VALUES
        (lower(${dto.email}), ${hash}, ${dto.ad_soyad},
         ${dto.rol ?? 'baxici'}, ${dto.emekdas_id ?? null}, true)
      RETURNING id, email, parol_hash, ad_soyad, rol, emekdas_id, aktiv`;

    this.log.log(`Yeni istifadeci: ${dto.email} (${dto.rol ?? 'baxici'})`);
    return this.temizle(setirler[0]);
  }

  /** Şifrəni dəyiş */
  async parolDeyis(id: number, kohne: string, yeni: string) {
    const setirler = await this.prisma.$queryRaw<IstifadeciSetri[]>`
      SELECT id, email, parol_hash, ad_soyad, rol, emekdas_id, aktiv
        FROM kadrlar.istifadeciler WHERE id = ${id}`;

    const istifadeci = setirler[0];
    if (!istifadeci) throw new UnauthorizedException('İstifadəçi tapılmadı');

    const duzdur = await bcrypt.compare(kohne, istifadeci.parol_hash);
    if (!duzdur) throw new UnauthorizedException('Köhnə şifrə yanlışdır');

    const yeniHash = await bcrypt.hash(yeni, BCRYPT_RAUND);
    await this.prisma.$executeRaw`
      UPDATE kadrlar.istifadeciler SET parol_hash = ${yeniHash} WHERE id = ${id}`;

    this.log.log(`Parol deyisdirildi: ${istifadeci.email}`);
    return { deyisdirildi: true };
  }

  /** Butun istifadeciler (parolsuz) — yalniz admin ucun */
  async siyahi(): Promise<IstifadeciCavabi[]> {
    const setirler = await this.prisma.$queryRaw<IstifadeciSetri[]>`
      SELECT id, email, parol_hash, ad_soyad, rol, emekdas_id, aktiv
        FROM kadrlar.istifadeciler ORDER BY id`;
    return setirler.map((s) => this.temizle(s));
  }

  /** Shaheleri temizle — parol_hash heç vaxt xarice cixmasin */
  private temizle(s: IstifadeciSetri): IstifadeciCavabi {
    return {
      id: s.id,
      email: s.email,
      ad_soyad: s.ad_soyad,
      rol: s.rol,
      emekdas_id: s.emekdas_id,
    };
  }
}

/**
 * Saxta hash — istifadeci tapilmayanda muqayise ucun.
 * "123456" sifresinin hash-idir, lakin heç bir hesaba aid deyil.
 */
const SAXTA_HASH =
  '$2b$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy';
KODSON
echo "  ✓ src/auth/auth.service.ts"

cat > "src/auth/auth.controller.ts" <<'KODSON'
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
KODSON
echo "  ✓ src/auth/auth.controller.ts"

cat > "src/auth/auth.module.ts" <<'KODSON'
import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { AuthService } from './auth.service.js';
import { AuthController } from './auth.controller.js';
import { JwtStrategy } from './strategies/jwt.strategy.js';
import type { SignOptions } from 'jsonwebtoken';

@Module({
  imports: [
    PassportModule,
    /*
     * registerAsync MÜTLƏQDİR — register() YOX.
     *
     * Sebeb: JwtModule.register({...}) modul YUKLENENDE icra olunur,
     * yeni .env hele oxunmamis olur. Netice: acar "undefined" olur ve
     * fallback deyer istifade olunur.
     *
     * registerAsync ise ConfigModule hazir olandan SONRA isleyir.
     */
    JwtModule.registerAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        secret: config.get<string>('JWT_SECRET'),
        signOptions: {
          expiresIn: (config.get<string>('JWT_MUDDET') ?? '8h') as SignOptions['expiresIn'],
        },
      }),
    }),
  ],
  controllers: [AuthController],
  providers: [AuthService, JwtStrategy],
})
export class AuthModule {}
KODSON
echo "  ✓ src/auth/auth.module.ts"

cat > "src/common/interceptors/audit.interceptor.ts" <<'KODSON'
import {
  CallHandler, ExecutionContext, Injectable, Logger, NestInterceptor,
} from '@nestjs/common';
import { Observable, tap } from 'rxjs';
import { PrismaService } from '../../prisma/prisma.service.js';
import { CariIstifadeci } from '../../auth/decorators/current-user.decorator.js';

/** Yalniz bu HTTP metodlari jurnala yazilir */
const IZLENEN_METODLAR = ['POST', 'PATCH', 'PUT', 'DELETE'];

@Injectable()
export class AuditInterceptor implements NestInterceptor {
  private readonly log = new Logger('AUDIT');

  constructor(private readonly prisma: PrismaService) {}

  intercept(context: ExecutionContext, novbeti: CallHandler): Observable<unknown> {
    const sorqu = context.switchToHttp().getRequest();
    const metod: string = sorqu.method;

    if (!IZLENEN_METODLAR.includes(metod)) {
      return novbeti.handle();          // oxuma emeliyyatlarini yazmiriq
    }

    const istifadeci = sorqu.user as CariIstifadeci | undefined;
    const baslama = Date.now();
    const cedvel = this.cedvelAdi(sorqu.route?.path ?? sorqu.url);

    return novbeti.handle().pipe(
      tap({
        next: () => this.yaz(cedvel, metod, istifadeci, sorqu, Date.now() - baslama, null),
        error: (xeta: Error) =>
          this.yaz(cedvel, metod, istifadeci, sorqu, Date.now() - baslama, xeta.message),
      }),
    );
  }

  /**
   * URL-den cedvel adini cixarir.
   * /api/v1/struktur/merkezler/:id  ->  struktur.merkezler
   */
  private cedvelAdi(yol: string): string {
    const temiz = yol
      .replace(/^\/api\/v\d+\//, '')     // qlobal prefiksi sil
      .replace(/^\//, '')
      .replace(/\/:[^/]+.*$/, '')          // :id kimi parametrleri sil
      .replace(/\/+$/, '')
      .replace(/\//g, '.');
    return temiz || 'namelum';
  }

  private async yaz(
    cedvel: string,
    metod: string,
    istifadeci: CariIstifadeci | undefined,
    sorqu: { params?: Record<string, string>; url: string },
    gecikme: number,
    xeta: string | null,
  ): Promise<void> {
    const setirId = sorqu.params?.id ? Number(sorqu.params.id) : null;
    const istifadeciAdi = istifadeci?.email ?? 'anonim';

    const qeyd = xeta
      ? `XETA: ${xeta} | ${gecikme}ms`
      : `Ugurlu | ${gecikme}ms`;

    try {
      await this.prisma.$executeRaw`
        INSERT INTO audit.audit_log (cedvel_adi, emeliyyat, setir_id, istifadeci, qeyd)
        VALUES (${cedvel}, ${metod}, ${setirId}, ${istifadeciAdi}, ${qeyd})`;
    } catch (x) {
      // Audit yazilmamasi esas emeliyyati POZMASIN
      this.log.error(`Audit yazilmadi: ${(x as Error).message}`);
    }

    this.log.log(`${metod} ${sorqu.url} — ${istifadeciAdi} — ${qeyd}`);
  }
}
KODSON
echo "  ✓ src/common/interceptors/audit.interceptor.ts"

cat > "src/app.module.ts" <<'KODSON'
import { Module } from '@nestjs/common';
import { APP_GUARD, APP_INTERCEPTOR } from '@nestjs/core';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module.js';
import { SaglamliqModule } from './saglamliq/saglamliq.module.js';
import { AuthModule } from './auth/auth.module.js';
import { StrukturModule } from './struktur/struktur.module.js';
import { KadrlarModule } from './kadrlar/kadrlar.module.js';
import { HesabatlarModule } from './hesabatlar/hesabatlar.module.js';
import { JwtAuthGuard } from './auth/guards/jwt-auth.guard.js';
import { RolesGuard } from './auth/guards/roles.guard.js';
import { AuditInterceptor } from './common/interceptors/audit.interceptor.js';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    SaglamliqModule,
    AuthModule,
    StrukturModule,
    KadrlarModule,
    HesabatlarModule,
  ],
  providers: [
    // SIRA VACIBDIR: evvelce "kim oldugunu" yoxla, sonra "icazen varmi"
    { provide: APP_GUARD, useClass: JwtAuthGuard },
    { provide: APP_GUARD, useClass: RolesGuard },
    // Butun yazma emeliyyatlarini jurnala yaz
    { provide: APP_INTERCEPTOR, useClass: AuditInterceptor },
  ],
})
export class AppModule {}
KODSON
echo "  ✓ src/app.module.ts"

cat > "src/struktur/struktur.controller.ts" <<'KODSON'
import {
  Body, Controller, Delete, Get, HttpCode, HttpStatus, Param,
  ParseIntPipe, Patch, Post, Query,
} from '@nestjs/common';
import {
  ApiBearerAuth, ApiOperation, ApiParam, ApiResponse, ApiTags,
} from '@nestjs/swagger';
import { Roles } from '../auth/decorators/roles.decorator.js';
import { StrukturService, Merkez } from './struktur.service.js';
import { CreateMerkezDto } from './dto/create-merkez.dto.js';
import { UpdateMerkezDto } from './dto/update-merkez.dto.js';
import { MerkezFiltrDto } from './dto/merkez-filtr.dto.js';
import { Sehifelenmis } from '../common/dto/sehife.dto.js';

@ApiTags('struktur')
@ApiBearerAuth()
@Controller('struktur/merkezler')
export class StrukturController {
  constructor(private readonly struktur: StrukturService) {}

  @Get()
  @ApiOperation({
    summary: 'Merkezlerin siyahisi',
    description: 'Sehifeleme, axtaris, filtr ve siralama desteklenir.',
  })
  @ApiResponse({ status: 200, description: 'Sehifelenmis siyahi' })
  siyahi(@Query() filtr: MerkezFiltrDto): Promise<Sehifelenmis<Merkez>> {
    return this.struktur.merkezler(filtr);
  }

  @Get('statistika')
  @ApiOperation({ summary: 'Merkez uzre shobe ve emekdas sayi' })
  statistika() {
    return this.struktur.merkezStatistikasi();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Bir merkez' })
  @ApiParam({ name: 'id', example: 2 })
  @ApiResponse({ status: 404, description: 'Merkez tapilmadi' })
  bir(@Param('id', ParseIntPipe) id: number): Promise<Merkez> {
    return this.struktur.merkez(id);
  }

  @Post()
  @Roles('admin', 'muhendis')
  @ApiOperation({ summary: 'Yeni merkez yarat (admin, muhendis)' })
  @ApiResponse({ status: 201, description: 'Yaradildi' })
  @ApiResponse({ status: 409, description: 'Bu adla merkez artiq var' })
  yarat(@Body() dto: CreateMerkezDto): Promise<Merkez> {
    return this.struktur.yarat(dto);
  }

  @Patch(':id')
  @Roles('admin', 'muhendis')
  @ApiOperation({ summary: 'Merkezi yenile (admin, muhendis)' })
  yenile(
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: UpdateMerkezDto,
  ): Promise<Merkez> {
    return this.struktur.yenile(id, dto);
  }

  @Delete(':id')
  @Roles('admin')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Merkezi sil (yalniz admin)' })
  @ApiResponse({ status: 409, description: 'Bagli shobeler var' })
  sil(@Param('id', ParseIntPipe) id: number) {
    return this.struktur.sil(id);
  }
}
KODSON
echo "  ✓ src/struktur/struktur.controller.ts"

cat > "src/saglamliq/saglamliq.controller.ts" <<'KODSON'
import { Controller, Get } from '@nestjs/common';
import { Public } from '../auth/decorators/public.decorator.js';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { PrismaService } from '../prisma/prisma.service.js';

@ApiTags('saglamliq')
@Controller()
export class SaglamliqController {
  constructor(private readonly prisma: PrismaService) {}

  @Public()
  @Get('saglamliq')
  @ApiOperation({ summary: 'Server ve baza saglamligi' })
  async yoxla() {
    const baslama = Date.now();

    const baza = await this.prisma.$queryRaw<{ cedvel: number }[]>`
      SELECT count(*)::int AS cedvel FROM information_schema.tables
       WHERE table_type = 'BASE TABLE'
         AND table_schema NOT IN ('pg_catalog', 'information_schema')`;

    return {
      status: 'saglam',
      baza: {
        qosulub: true,
        cedvel_sayi: baza[0]?.cedvel ?? 0,
        gecikme_ms: Date.now() - baslama,
      },
      versiya: process.env.npm_package_version ?? '0.0.1',
      vaxt: new Date().toISOString(),
    };
  }

  @Public()
  @Get()
  @ApiOperation({ summary: 'Kok — API melumati' })
  kok() {
    return {
      ad: 'Deepseek ARTI API',
      versiya: '1.0',
      sened: '/docs',
      prefiks: '/api/v1',
    };
  }
}
KODSON
echo "  ✓ src/saglamliq/saglamliq.controller.ts"

cat > "scripts/seed-auth.ts" <<'KODSON'
/**
 * İstifadəçiləri yaradır / yeniləyir.
 *
 *   npm run seed:auth
 *
 * İdempotentdir: ikinci dəfə işlətsəniz, mövcud istifadəçilərin
 * şifrəsini yeniləyir — dublikat yaratmır.
 */
import 'dotenv/config';
import * as bcrypt from 'bcryptjs';
import { Pool } from 'pg';

interface SeedIstifadeci {
  email: string;
  parol: string;
  ad_soyad: string;
  rol: 'admin' | 'muhendis' | 'maliyyeci' | 'baxici';
}

const ISTIFADECILER: SeedIstifadeci[] = [
  { email: 'admin@arti.edu.az',     parol: '123456', ad_soyad: 'Elnur Əliyev',    rol: 'admin' },
  { email: 'muhendis@arti.edu.az',  parol: '123456', ad_soyad: 'Rəşad Məmmədov',  rol: 'muhendis' },
  { email: 'maliyyeci@arti.edu.az', parol: '123456', ad_soyad: 'Tural İsmayılov', rol: 'maliyyeci' },
  { email: 'baxici@arti.edu.az',    parol: '123456', ad_soyad: 'Günel Rzayeva',   rol: 'baxici' },
];

const BCRYPT_RAUND = 10;

async function main() {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });

  console.log('════ İstifadəçilər yaradılır ════\n');

  for (const i of ISTIFADECILER) {
    const hash = await bcrypt.hash(i.parol, BCRYPT_RAUND);

    const netice = await pool.query(
      `INSERT INTO kadrlar.istifadeciler (email, parol_hash, ad_soyad, rol, aktiv)
       VALUES (lower($1), $2, $3, $4, true)
       ON CONFLICT (email) DO UPDATE
         SET parol_hash = EXCLUDED.parol_hash,
             ad_soyad   = EXCLUDED.ad_soyad,
             rol        = EXCLUDED.rol,
             aktiv      = true
       RETURNING id, email, rol`,
      [i.email, hash, i.ad_soyad, i.rol],
    );

    const s = netice.rows[0];
    console.log(`  ✓ id=${String(s.id).padStart(2)}  ${s.email.padEnd(24)} ${s.rol.padEnd(10)} şifrə: ${i.parol}`);
  }

  const cem = await pool.query('SELECT count(*)::int AS say FROM kadrlar.istifadeciler');
  console.log(`\n════ CƏMİ: ${cem.rows[0].say} istifadəçi ════`);

  await pool.end();
}

main().catch((xeta) => {
  console.error('XƏTA:', xeta.message);
  process.exit(1);
});
KODSON
echo "  ✓ scripts/seed-auth.ts"

cat > "src/auth/auth.service.spec.ts" <<'KODSON'
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ConflictException, UnauthorizedException } from '@nestjs/common';

/*
 * bcryptjs-i MOCK edirik: namespace dondurulmus oldugu ucun
 * vi.spyOn() onun metodlarini evez ede bilmir.
 * vi.mock ise modul yuklenende isleyir ve metodlari evez edir.
 */
vi.mock('bcryptjs', async () => {
  const real = await vi.importActual<typeof import('bcryptjs')>('bcryptjs');
  return {
    ...real,
    compare: vi.fn(real.compare),
    hash: vi.fn(real.hash),
  };
});

import * as bcrypt from 'bcryptjs';
import { AuthService } from './auth.service.js';

function saxtaPrisma() {
  return {
    $queryRaw: vi.fn(),
    $executeRaw: vi.fn(),
  } as any;
}

function saxtaJwt() {
  return { signAsync: vi.fn().mockResolvedValue('saxta.token.deyeri') } as any;
}

/** Real bcrypt hash-i — testde de real olsun */
const HASH_123456 = bcrypt.hashSync('123456', 4);   // test ucun az raund

describe('AuthService', () => {
  let prisma: any;
  let jwt: any;
  let service: AuthService;

  beforeEach(() => {
    prisma = saxtaPrisma();
    jwt = saxtaJwt();
    service = new AuthService(prisma, jwt);
  });

  // ── LOGIN ──
  describe('login()', () => {
    const setir = {
      id: 2, email: 'admin@arti.edu.az', parol_hash: HASH_123456,
      ad_soyad: 'Elnur Əliyev', rol: 'admin', emekdas_id: 1, aktiv: true,
    };

    it('duzgun sifre ile token qaytarir', async () => {
      prisma.$queryRaw.mockResolvedValue([setir]);

      const n = await service.login({ email: 'admin@arti.edu.az', parol: '123456' });

      expect(n.token).toBe('saxta.token.deyeri');
      expect(n.istifadeci.email).toBe('admin@arti.edu.az');
      expect(n.istifadeci.rol).toBe('admin');
    });

    it('cavabda parol_hash YOXDUR', async () => {
      prisma.$queryRaw.mockResolvedValue([setir]);

      const n = await service.login({ email: 'admin@arti.edu.az', parol: '123456' });

      expect(n.istifadeci).not.toHaveProperty('parol_hash');
      expect(JSON.stringify(n)).not.toContain('$2b$');
    });

    it('sehv sifre ile UnauthorizedException atir', async () => {
      prisma.$queryRaw.mockResolvedValue([setir]);
      await expect(service.login({ email: 'admin@arti.edu.az', parol: 'sehv' }))
        .rejects.toThrow(UnauthorizedException);
    });

    it('movcud olmayan email ile EYNI xeta mesajini verir', async () => {
      prisma.$queryRaw.mockResolvedValue([]);

      await expect(service.login({ email: 'yox@arti.edu.az', parol: '123456' }))
        .rejects.toThrow('E-poçt və ya şifrə yanlışdır');
    });

    it('movcud olmayan email ucun de bcrypt MUQAYISESI aparilir (timing attack)', async () => {
      prisma.$queryRaw.mockResolvedValue([]);
      vi.mocked(bcrypt.compare).mockClear();

      await service.login({ email: 'yox@arti.edu.az', parol: '123456' }).catch(() => null);

      // Istifadeci tapilmasa da muqayise APARILIR — cavab vaxti ferqlenmesin
      expect(bcrypt.compare).toHaveBeenCalledTimes(1);
      const [, hash] = vi.mocked(bcrypt.compare).mock.calls[0];
      expect(String(hash).startsWith('$2b$')).toBe(true);   // saxta hash de REALDIR
    });

    it('deaktiv istifadeci daxil ola bilmir', async () => {
      prisma.$queryRaw.mockResolvedValue([{ ...setir, aktiv: false }]);
      await expect(service.login({ email: 'admin@arti.edu.az', parol: '123456' }))
        .rejects.toThrow('İstifadəçi deaktiv edilib');
    });

    it('JWT payload icinde rol var', async () => {
      prisma.$queryRaw.mockResolvedValue([setir]);
      await service.login({ email: 'admin@arti.edu.az', parol: '123456' });

      const payload = jwt.signAsync.mock.calls[0][0];
      expect(payload).toMatchObject({ sub: 2, rol: 'admin' });
    });
  });

  // ── QEYDIYYAT ──
  describe('qeydiyyat()', () => {
    it('yeni istifadeci yaradir ve sifreyi HASH edir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([])                         // email yoxdur
        .mockResolvedValueOnce([{ id: 9, email: 'yeni@arti.edu.az',
          parol_hash: HASH_123456, ad_soyad: 'Yeni Adam',
          rol: 'baxici', emekdas_id: null, aktiv: true }]);

      const n = await service.qeydiyyat({
        email: 'yeni@arti.edu.az', parol: 'guclu-sifre-1',
        ad_soyad: 'Yeni Adam',
      });

      expect(n.id).toBe(9);
      expect(n).not.toHaveProperty('parol_hash');
    });

    it('INSERT-e duz METN sifre GETMIR — hash gedir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([])
        .mockResolvedValueOnce([{ id: 9, email: 'y@arti.edu.az', parol_hash: 'x',
          ad_soyad: 'Y', rol: 'baxici', emekdas_id: null, aktiv: true }]);

      await service.qeydiyyat({ email: 'y@arti.edu.az', parol: 'guclu-sifre-1', ad_soyad: 'Y' });

      // SQL parametrleri: [email, hash, ...]
      const arqumentler = prisma.$queryRaw.mock.calls[1];
      const duzMetnVar = arqumentler.some((a: unknown) => a === 'guclu-sifre-1');
      expect(duzMetnVar).toBe(false);
    });

    it('eyni email ile ConflictException atir', async () => {
      prisma.$queryRaw.mockResolvedValue([{ id: 2 }]);
      await expect(service.qeydiyyat({
        email: 'admin@arti.edu.az', parol: 'guclu-sifre-1', ad_soyad: 'X',
      })).rejects.toThrow(ConflictException);
    });

    it('movcud olmayan emekdas_id ile xeta atir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([])          // email yoxdur
        .mockResolvedValueOnce([]);         // emekdas yoxdur

      await expect(service.qeydiyyat({
        email: 'y@arti.edu.az', parol: 'guclu-sifre-1',
        ad_soyad: 'Y', emekdas_id: 9999,
      })).rejects.toThrow(ConflictException);
    });
  });

  // ── PAROL DEYISME ──
  describe('parolDeyis()', () => {
    it('kohne sifre duzdurse yenileyir', async () => {
      prisma.$queryRaw.mockResolvedValue([{
        id: 2, email: 'a@b.az', parol_hash: HASH_123456,
        ad_soyad: 'A', rol: 'admin', emekdas_id: null, aktiv: true,
      }]);
      prisma.$executeRaw.mockResolvedValue(1);

      const n = await service.parolDeyis(2, '123456', 'yeni-sifre-2026');
      expect(n.deyisdirildi).toBe(true);
      expect(prisma.$executeRaw).toHaveBeenCalledTimes(1);
    });

    it('kohne sifre sehvdirse xeta atir', async () => {
      prisma.$queryRaw.mockResolvedValue([{
        id: 2, email: 'a@b.az', parol_hash: HASH_123456,
        ad_soyad: 'A', rol: 'admin', emekdas_id: null, aktiv: true,
      }]);

      await expect(service.parolDeyis(2, 'sehv', 'yeni-sifre-2026'))
        .rejects.toThrow('Köhnə şifrə yanlışdır');
    });
  });
});
KODSON
echo "  ✓ src/auth/auth.service.spec.ts"

cat > "test/backend3.e2e-spec.ts" <<'KODSON'
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import request from 'supertest';
import { App } from 'supertest/types';
import { AppModule } from '../src/app.module.js';
import { AllExceptionsFilter } from '../src/common/filters/all-exceptions.filter.js';
import { Pool } from 'pg';

/**
 * BACKEND-3 e2e: autentifikasiya, RBAC ve audit.
 * APP_GUARD ile qeyd olunan qlobal guard-lar AppModule ile avtomatik gelir.
 */
describe('Backend-3 (e2e)', () => {
  let app: INestApplication<App>;

  const tokenlar: Record<string, string> = {};
  const YARADILANLAR: number[] = [];

  beforeAll(async () => {
    const modul: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = modul.createNestApplication();
    app.setGlobalPrefix('api/v1');
    app.useGlobalPipes(
      new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }),
    );
    app.useGlobalFilters(new AllExceptionsFilter());
    await app.init();

    // Butun rollar ucun token al
    for (const rol of ['admin', 'muhendis', 'maliyyeci', 'baxici']) {
      const c = await request(app.getHttpServer())
        .post('/api/v1/auth/login')
        .send({ email: `${rol}@arti.edu.az`, parol: '123456' });
      if (c.body?.token) tokenlar[rol] = c.body.token;
    }
  });

  afterAll(async () => {
    const admin = tokenlar.admin;

    // 1) Test zamani yaradilan merkezleri sil
    for (const id of YARADILANLAR) {
      await request(app.getHttpServer())
        .delete(`/api/v1/struktur/merkezler/${id}`)
        .set('Authorization', `Bearer ${admin}`);
    }

    /*
     * 2) Test istifadecilerini sil.
     * Qeydiyyat endpoint-i ile yaradilanlar bazada qalir —
     * onlari birbasa SQL ile temizleyirik, eks halda her test
     * buraxilisi yeni setirler elave eder.
     */
    const pool = new Pool({ connectionString: process.env.DATABASE_URL });
    await pool.query("DELETE FROM kadrlar.istifadeciler WHERE email LIKE 'e2e%'");
    await pool.end();

    await app.close();
  });

  const url = (y: string) => `/api/v1${y}`;
  const auth = (rol: string) => ({ Authorization: `Bearer ${tokenlar[rol]}` });

  // ── LOGIN ──
  describe('POST /auth/login', () => {
    it('duzgun melumatla token qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'admin@arti.edu.az', parol: '123456' })
        .expect(200);

      expect(c.body.token).toBeTypeOf('string');
      expect(c.body.token.split('.')).toHaveLength(3);     // JWT 3 hissedir
      expect(c.body.istifadeci.rol).toBe('admin');
      expect(c.body.istifadeci).not.toHaveProperty('parol_hash');
    });

    it('sehv sifre 401 verir', () =>
      request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'admin@arti.edu.az', parol: 'sehv-sifre' })
        .expect(401));

    it('movcud olmayan email 401 verir', () =>
      request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'yoxdur@arti.edu.az', parol: '123456' })
        .expect(401));

    it('qisa sifre 400 verir (validasiya)', () =>
      request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'admin@arti.edu.az', parol: '123' })
        .expect(400));

    it('yanlis email formati 400 verir', () =>
      request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'email-deyil', parol: '123456' })
        .expect(400));
  });

  // ── TOKEN ──
  describe('Token yoxlamasi', () => {
    it('tokensiz qorunan endpoint 401', () =>
      request(app.getHttpServer()).get(url('/struktur/merkezler')).expect(401));

    it('sehv token 401', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler'))
        .set('Authorization', 'Bearer sehv.token.deyeri')
        .expect(401));

    it('Bearer prefiksi olmadan 401', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler'))
        .set('Authorization', tokenlar.admin)
        .expect(401));

    it('duzgun token 200', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler'))
        .set(auth('admin'))
        .expect(200));
  });

  // ── PUBLIC ──
  describe('@Public() endpoint-ler', () => {
    it('saglamliq tokensiz isleyir', () =>
      request(app.getHttpServer()).get(url('/saglamliq')).expect(200));

    it('kok tokensiz isleyir', () =>
      request(app.getHttpServer()).get(url('')).expect(200));

    it('login tokensiz isleyir', () =>
      request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: 'admin@arti.edu.az', parol: '123456' })
        .expect(200));
  });

  // ── PROFIL ──
  describe('GET /auth/profil', () => {
    it('cari istifadecini qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/auth/profil'))
        .set(auth('maliyyeci'))
        .expect(200);

      expect(c.body.email).toBe('maliyyeci@arti.edu.az');
      expect(c.body.rol).toBe('maliyyeci');
      expect(c.body).not.toHaveProperty('parol_hash');
    });
  });

  // ── RBAC MATRİSİ ──
  describe('RBAC — rol icazeleri', () => {
    const yarat = (rol: string) =>
      request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .set(auth(rol))
        .send({ ad: `RBAC E2E ${rol} ${Date.now()}` });

    it('admin merkez yarada bilir', async () => {
      const c = await yarat('admin').expect(201);
      YARADILANLAR.push(c.body.id);
    });

    it('muhendis merkez yarada bilir', async () => {
      const c = await yarat('muhendis').expect(201);
      YARADILANLAR.push(c.body.id);
    });

    it('maliyyeci merkez yarada BILMIR (403)', () =>
      yarat('maliyyeci').expect(403));

    it('baxici merkez yarada BILMIR (403)', () =>
      yarat('baxici').expect(403));

    it('baxici OXUYA bilir (200)', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler'))
        .set(auth('baxici'))
        .expect(200));

    it('admin olmayan silmir (403)', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .set(auth('admin'))
        .send({ ad: `Silme testi ${Date.now()}` })
        .expect(201);

      await request(app.getHttpServer())
        .delete(url(`/struktur/merkezler/${c.body.id}`))
        .set(auth('muhendis'))
        .expect(403);

      await request(app.getHttpServer())
        .delete(url(`/struktur/merkezler/${c.body.id}`))
        .set(auth('admin'))
        .expect(200);
    });

    it('istifadeci siyahisi yalniz admin ucun', async () => {
      await request(app.getHttpServer())
        .get(url('/auth/istifadeciler')).set(auth('baxici')).expect(403);
      await request(app.getHttpServer())
        .get(url('/auth/istifadeciler')).set(auth('admin')).expect(200);
    });

    it('admin HER SEYE icazelidir (super-rol)', () =>
      request(app.getHttpServer())
        .get(url('/hesabatlar/icmal')).set(auth('admin')).expect(200));

    it('baxici hesabatlari oxuya bilir', () =>
      request(app.getHttpServer())
        .get(url('/hesabatlar/icmal')).set(auth('baxici')).expect(200));
  });

  // ── QEYDİYYAT ──
  describe('POST /auth/qeydiyyat', () => {
    const yeni = () => ({
      email: `e2e${Date.now()}_${Math.floor(Math.random() * 9999)}@arti.edu.az`,
      parol: 'guclu-sifre-2026',
      ad_soyad: 'E2E Test Istifadeci',
      rol: 'baxici',
    });

    it('admin yeni istifadeci yarada bilir', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/auth/qeydiyyat'))
        .set(auth('admin'))
        .send(yeni())
        .expect(201);

      expect(c.body.rol).toBe('baxici');
      expect(c.body).not.toHaveProperty('parol_hash');
    });

    it('qeydiyyatdan sonra HEMIN sifre ile giris isleyir', async () => {
      const m = yeni();
      await request(app.getHttpServer())
        .post(url('/auth/qeydiyyat')).set(auth('admin')).send(m).expect(201);

      const c = await request(app.getHttpServer())
        .post(url('/auth/login'))
        .send({ email: m.email, parol: m.parol })
        .expect(200);

      expect(c.body.token).toBeTypeOf('string');
    });

    it('qeydiyyat yalniz admin ucun (baxici 403)', () =>
      request(app.getHttpServer())
        .post(url('/auth/qeydiyyat')).set(auth('baxici')).send(yeni()).expect(403));

    it('qisa sifre 400 verir', () =>
      request(app.getHttpServer())
        .post(url('/auth/qeydiyyat')).set(auth('admin'))
        .send({ ...yeni(), parol: 'qisa' })
        .expect(400));

    it('yanlis rol 400 verir', () =>
      request(app.getHttpServer())
        .post(url('/auth/qeydiyyat')).set(auth('admin'))
        .send({ ...yeni(), rol: 'superadmin' })
        .expect(400));
  });

  // ── AUDIT ──
  describe('Audit jurnali', () => {
    it('yazma emeliyyati jurnala dusur', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .set(auth('admin'))
        .send({ ad: `Audit E2E ${Date.now()}` })
        .expect(201);
      YARADILANLAR.push(c.body.id);

      const audit = await request(app.getHttpServer())
        .get(url('/hesabatlar/audit?limit=1'))
        .set(auth('admin'))
        .expect(200);

      expect(audit.body[0].cedvel_adi).toBe('struktur.merkezler');
      expect(audit.body[0].emeliyyat).toBe('POST');
      expect(audit.body[0].istifadeci).toBe('admin@arti.edu.az');
    });

    it('oxuma emeliyyati jurnala DUSMUR', async () => {
      const evvel = await request(app.getHttpServer())
        .get(url('/hesabatlar/audit?limit=1'))
        .set(auth('admin'));

      await request(app.getHttpServer())
        .get(url('/struktur/merkezler')).set(auth('admin')).expect(200);
      await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar')).set(auth('admin')).expect(200);

      const sonra = await request(app.getHttpServer())
        .get(url('/hesabatlar/audit?limit=1'))
        .set(auth('admin'));

      // En son qeyd deyismeyib — GET yazilmir
      expect(sonra.body[0].id).toBe(evvel.body[0].id);
    });
  });

  // ── XƏTA FORMATI ──
  describe('Xeta formatlari', () => {
    it('401 formati duzgundur', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/struktur/merkezler')).expect(401);
      expect(c.body.xeta.kod).toBe('AUTENTIFIKASIYA_LAZIM');
    });

    it('403 formati duzgundur', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/struktur/merkezler')).set(auth('baxici'))
        .send({ ad: 'Test Merkez' })
        .expect(403);
      expect(c.body.xeta.kod).toBe('ICAZE_YOXDUR');
    });

    it('parol_hash HEÇ VAXT cavabda gelmir', async () => {
      const cavablar = await Promise.all([
        request(app.getHttpServer()).post(url('/auth/login'))
          .send({ email: 'admin@arti.edu.az', parol: '123456' }),
        request(app.getHttpServer()).get(url('/auth/profil')).set(auth('admin')),
        request(app.getHttpServer()).get(url('/auth/istifadeciler')).set(auth('admin')),
      ]);
      for (const c of cavablar) {
        expect(JSON.stringify(c.body)).not.toContain('$2b$');
        expect(JSON.stringify(c.body)).not.toContain('parol_hash');
      }
    });
  });
});
KODSON
echo "  ✓ test/backend3.e2e-spec.ts"

echo "════ 4/5  package.json skripti ════"
npm pkg set scripts.seed:auth="tsx scripts/seed-auth.ts" >/dev/null
echo "  ✓ npm run seed:auth"

echo "════ 5/5  Yoxlama ════"
unset DATABASE_URL PGHOST
npm run build
echo ""
echo "HAZIR. Testleri isletmek ucun:"
echo "  npm test"
echo "  npx vitest run --config vitest.config.e2e.ts"
