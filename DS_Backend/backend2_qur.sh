#!/bin/bash
# ═══════════════════════════════════════════════════════════
#  DS_Backend-2 — butun fayllari BIR EMRLE yaradir
#  Istifade:  bash backend2_qur.sh
# ═══════════════════════════════════════════════════════════
set -e

cd ~/Deepseek_ARTI/DS_Backend || { echo "XETA: DS_Backend tapilmadi"; exit 1; }

if [ ! -f package.json ]; then
  echo "XETA: package.json yoxdur — evvelce Backend-1-i icra edin";
  exit 1
fi

echo "════ 1/4  Qovluqlar ════"
mkdir -p "src"
mkdir -p "src/common/dto"
mkdir -p "src/common/filters"
mkdir -p "src/hesabatlar"
mkdir -p "src/kadrlar"
mkdir -p "src/kadrlar/dto"
mkdir -p "src/saglamliq"
mkdir -p "src/struktur"
mkdir -p "src/struktur/dto"
mkdir -p "test"

echo "  10 qovluq hazirdir"

echo "════ 2/4  Fayllar ════"

cat > "src/common/dto/sehife.dto.ts" <<'KODSON'
import { Type } from 'class-transformer';
import {
  IsIn, IsInt, IsOptional, IsString, Max, MaxLength, Min,
} from 'class-validator';
import { ApiPropertyOptional } from '@nestjs/swagger';

/**
 * Sehifelme + filtr + siralama ucun ORTAQ DTO.
 * Butun siyahi endpoint-leri bundan miras alir.
 */
export class SehifeDto {
  @ApiPropertyOptional({ default: 1, minimum: 1, description: 'Sehife nomresi' })
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'sehife tam eded olmalidir' })
  @Min(1, { message: 'sehife 1-den kicik ola bilmez' })
  sehife: number = 1;

  @ApiPropertyOptional({ default: 20, minimum: 1, maximum: 100 })
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'limit tam eded olmalidir' })
  @Min(1)
  @Max(100, { message: 'limit 100-den cox ola bilmez' })
  limit: number = 20;

  @ApiPropertyOptional({ description: 'Metn axtarisi (ad, soyad, e-mail)' })
  @IsOptional()
  @IsString()
  @MaxLength(100)
  axtar?: string;

  @ApiPropertyOptional({ enum: ['asc', 'desc'], default: 'asc' })
  @IsOptional()
  @IsIn(['asc', 'desc'], { message: 'siralama yalniz asc ve ya desc ola biler' })
  siralama: 'asc' | 'desc' = 'asc';

  @ApiPropertyOptional({ description: 'Siralama sutunu' })
  @IsOptional()
  @IsString()
  @MaxLength(40)
  siralama_sah?: string;

  /** SQL OFFSET — hesablanmis xassə (DTO-da sorgu parametri deyil) */
  get offset(): number {
    return (this.sehife - 1) * this.limit;
  }
}

/** Sehifelenmis cavabin standart formasi */
export interface Sehifelenmis<T> {
  data: T[];
  meta: {
    sehife: number;
    limit: number;
    cem: number;
    sehife_sayi: number;
  };
}
KODSON
echo "  ✓ src/common/dto/sehife.dto.ts"

cat > "src/main.ts" <<'KODSON'
import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module.js';
import { AllExceptionsFilter } from './common/filters/all-exceptions.filter.js';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.setGlobalPrefix('api/v1');
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,            // DTO-da olmayan saheleri sil
      forbidNonWhitelisted: true, // ...ve xeta ver
      transform: true,            // '5' -> 5
      transformOptions: { enableImplicitConversion: false },
    }),
  );
  app.enableCors();
  app.useGlobalFilters(new AllExceptionsFilter());

  const cfg = new DocumentBuilder()
    .setTitle('Deepseek ARTI API')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  SwaggerModule.setup('docs', app, SwaggerModule.createDocument(app, cfg));

  const port = process.env.PORT ?? 4000;
  await app.listen(port);
  console.log('API: http://localhost:' + port + '/api/v1');
}
bootstrap();
KODSON
echo "  ✓ src/main.ts"

cat > "src/struktur/dto/create-merkez.dto.ts" <<'KODSON'
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import {
  IsBoolean, IsEmail, IsIn, IsOptional, IsString,
  Matches, MaxLength, MinLength,
} from 'class-validator';

/** Yeni merkez yaratmaq ucun gelen melumat */
export class CreateMerkezDto {
  @ApiProperty({ example: 'Elmi-pedaqoji tedqiqatlar merkezi' })
  @IsString()
  @MinLength(3, { message: 'Ad ən azı 3 simvol olmalıdır' })
  @MaxLength(200)
  ad!: string;

  @ApiPropertyOptional({ enum: ['merkez', 'katiblik', 'sobe', 'sektor'] })
  @IsOptional()
  @IsIn(['merkez', 'katiblik', 'sobe', 'sektor'], {
    message: 'tip yalniz: merkez, katiblik, sobe, sektor',
  })
  tip?: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  @MaxLength(500)
  tesvir?: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  @MaxLength(300)
  unvan?: string;

  @ApiPropertyOptional({ example: '+994 12 599 08 08' })
  @IsOptional()
  @Matches(/^\+?[0-9\s()-]{7,25}$/, {
    message: 'Telefon formati yanlışdır (+994 12 599 08 08)',
  })
  telefon?: string;

  @ApiPropertyOptional({ example: 'tedqiqat@arti.edu.az' })
  @IsOptional()
  @IsEmail({}, { message: 'E-poçt ünvanı yanlışdır' })
  @MaxLength(120)
  email?: string;

  @ApiPropertyOptional({ example: '2024-02-15' })
  @IsOptional()
  @Matches(/^\d{4}-\d{2}-\d{2}$/, {
    message: 'Tarix IL-AY-GUN formatinda olmalidir (2024-02-15)',
  })
  yaradilma_tarixi?: string;

  @ApiPropertyOptional({ default: true })
  @IsOptional()
  @IsBoolean()
  aktiv?: boolean;
}
KODSON
echo "  ✓ src/struktur/dto/create-merkez.dto.ts"

cat > "src/struktur/dto/update-merkez.dto.ts" <<'KODSON'
import { PartialType } from '@nestjs/swagger';
import { CreateMerkezDto } from './create-merkez.dto.js';

/**
 * Yenileme DTO-su — butun saheler OPSIONALDIR.
 * PartialType CreateMerkezDto-nun butun qaydalarini miras alir,
 * lakin her saheni optional edir.
 */
export class UpdateMerkezDto extends PartialType(CreateMerkezDto) {}
KODSON
echo "  ✓ src/struktur/dto/update-merkez.dto.ts"

cat > "src/struktur/dto/merkez-filtr.dto.ts" <<'KODSON'
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
KODSON
echo "  ✓ src/struktur/dto/merkez-filtr.dto.ts"

cat > "src/common/filters/all-exceptions.filter.ts" <<'KODSON'
import {
  ArgumentsHost, Catch, ExceptionFilter, HttpException, HttpStatus, Logger,
} from '@nestjs/common';
import type { Request, Response } from 'express';

/**
 * Butun xetalari VAHDİ formata salir.
 * Default NestJS formati: { statusCode, message, error }
 * Bizim format:            { ugur, xeta: { kod, mesaj, detallar }, yol, vaxt }
 */
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly log = new Logger('XETA');

  catch(xeta: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const cavab = ctx.getResponse<Response>();
    const sorgu = ctx.getRequest<Request>();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let mesaj: string | string[] = 'Daxili server xetasi';
    let kod = 'DAXILI_XETA';

    if (xeta instanceof HttpException) {
      status = xeta.getStatus();
      const cavabGovdesi = xeta.getResponse();

      if (typeof cavabGovdesi === 'string') {
        mesaj = cavabGovdesi;
      } else if (typeof cavabGovdesi === 'object' && cavabGovdesi !== null) {
        const g = cavabGovdesi as Record<string, unknown>;
        mesaj = (g.message as string | string[]) ?? xeta.message;
      }
      kod = KOD_XERITESI[status] ?? 'XETA';
    } else if (xeta instanceof Error) {
      mesaj = xeta.message;
      this.log.error(`${sorgu.method} ${sorgu.url} — ${xeta.message}`, xeta.stack);
    }

    const detallar = Array.isArray(mesaj) ? mesaj : undefined;

    cavab.status(status).json({
      ugur: false,
      xeta: {
        kod,
        mesaj: Array.isArray(mesaj) ? 'Validasiya xetasi' : mesaj,
        ...(detallar ? { detallar } : {}),
      },
      yol: sorgu.url,
      vaxt: new Date().toISOString(),
    });
  }
}

const KOD_XERITESI: Record<number, string> = {
  400: 'YANLIS_SORGU',
  401: 'AUTENTIFIKASIYA_LAZIM',
  403: 'ICAZE_YOXDUR',
  404: 'TAPILMADI',
  409: 'TOQQUSMA',
  422: 'EMAL_OLUNMADI',
  500: 'DAXILI_XETA',
};
KODSON
echo "  ✓ src/common/filters/all-exceptions.filter.ts"

cat > "src/struktur/struktur.service.ts" <<'KODSON'
import {
  BadRequestException, ConflictException, Injectable, NotFoundException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';
import { CreateMerkezDto } from './dto/create-merkez.dto.js';
import { UpdateMerkezDto } from './dto/update-merkez.dto.js';
import { MerkezFiltrDto } from './dto/merkez-filtr.dto.js';
import { Sehifelenmis } from '../common/dto/sehife.dto.js';

/** Bazadan gelen setir */
export interface Merkez {
  id: number;
  ad: string;
  tip: string | null;
  unvan: string | null;
  telefon: string | null;
  email: string | null;
  aktiv: boolean;
}

/**
 * SQL INJECTION QORUMASI.
 * Siralama sutunu birbasa SQL-e yazilir, ona gore YALNIZ
 * bu siyahidaki adlara icaze verilir.
 */
const SIRALAMA_ICAZELI = ['id', 'ad', 'tip', 'unvan'] as const;

const SAHELER = 'id::int, ad, tip, unvan, telefon, email, aktiv';

@Injectable()
export class StrukturService {
  constructor(private readonly prisma: PrismaService) {}

  /** Sehifelenmis, filtreli, siralanmis siyahi */
  async merkezler(dto: MerkezFiltrDto): Promise<Sehifelenmis<Merkez>> {
    const sutun = this.sutunYoxla(dto.siralama_sah);
    const istiqamet = dto.siralama === 'desc' ? 'DESC' : 'ASC';

    const axtar = dto.axtar?.trim() || null;
    const kimi = axtar ? `%${axtar}%` : null;

    const setirler = await this.prisma.$queryRawUnsafe<Merkez[]>(
      `SELECT ${SAHELER}
         FROM struktur.merkezler
        WHERE ($1::text IS NULL OR ad ILIKE $1 OR unvan ILIKE $1 OR email ILIKE $1)
          AND ($2::text IS NULL OR tip = $2)
          AND ($3::boolean IS NULL OR aktiv = $3)
        ORDER BY ${sutun} ${istiqamet}
        LIMIT $4 OFFSET $5`,
      kimi, dto.tip ?? null, dto.aktiv ?? null, dto.limit, dto.offset,
    );

    const cem = await this.prisma.$queryRawUnsafe<{ cem: number }[]>(
      `SELECT count(*)::int AS cem
         FROM struktur.merkezler
        WHERE ($1::text IS NULL OR ad ILIKE $1 OR unvan ILIKE $1 OR email ILIKE $1)
          AND ($2::text IS NULL OR tip = $2)
          AND ($3::boolean IS NULL OR aktiv = $3)`,
      kimi, dto.tip ?? null, dto.aktiv ?? null,
    );

    const umumi = cem[0]?.cem ?? 0;

    return {
      data: setirler,
      meta: {
        sehife: dto.sehife,
        limit: dto.limit,
        cem: umumi,
        sehife_sayi: Math.ceil(umumi / dto.limit) || 1,
      },
    };
  }

  /** Bir merkez */
  async merkez(id: number): Promise<Merkez> {
    const setirler = await this.prisma.$queryRaw<Merkez[]>`
      SELECT id::int, ad, tip, unvan, telefon, email, aktiv
      FROM struktur.merkezler WHERE id = ${id}`;

    if (!setirler.length) {
      throw new NotFoundException(`Merkez tapilmadi: id=${id}`);
    }
    return setirler[0];
  }

  /** Yeni merkez */
  async yarat(dto: CreateMerkezDto): Promise<Merkez> {
    await this.adYoxla(dto.ad);

    const setirler = await this.prisma.$queryRaw<Merkez[]>`
      INSERT INTO struktur.merkezler
        (ad, tip, tesvir, unvan, telefon, email, yaradilma_tarixi, aktiv)
      VALUES
        (${dto.ad}, ${dto.tip ?? 'merkez'}, ${dto.tesvir ?? null},
         ${dto.unvan ?? null}, ${dto.telefon ?? null}, ${dto.email ?? null},
         ${dto.yaradilma_tarixi ?? null}, ${dto.aktiv ?? true})
      RETURNING id::int, ad, tip, unvan, telefon, email, aktiv`;

    return setirler[0];
  }

  /** Yenile — yalniz gonderilen saheler */
  async yenile(id: number, dto: UpdateMerkezDto): Promise<Merkez> {
    const movcud = await this.merkez(id);

    if (dto.ad && dto.ad !== movcud.ad) await this.adYoxla(dto.ad, id);

    const setirler = await this.prisma.$queryRaw<Merkez[]>`
      UPDATE struktur.merkezler
         SET ad      = COALESCE(${dto.ad ?? null}, ad),
             tip     = COALESCE(${dto.tip ?? null}, tip),
             tesvir  = COALESCE(${dto.tesvir ?? null}, tesvir),
             unvan   = COALESCE(${dto.unvan ?? null}, unvan),
             telefon = COALESCE(${dto.telefon ?? null}, telefon),
             email   = COALESCE(${dto.email ?? null}, email),
             aktiv   = COALESCE(${dto.aktiv ?? null}, aktiv)
       WHERE id = ${id}
      RETURNING id::int, ad, tip, unvan, telefon, email, aktiv`;

    return setirler[0];
  }

  /** Sil — bagli setir varsa 409 */
  async sil(id: number): Promise<{ silindi: true; id: number }> {
    await this.merkez(id);

    const bagli = await this.prisma.$queryRaw<{ say: number }[]>`
      SELECT count(*)::int AS say FROM struktur.shobeler WHERE merkez_id = ${id}`;

    const say = bagli[0]?.say ?? 0;
    if (say > 0) {
      throw new ConflictException(
        `Bu merkeze ${say} shobe baglidir — evvelce onlari kocurun`,
      );
    }

    await this.prisma.$executeRaw`DELETE FROM struktur.merkezler WHERE id = ${id}`;
    return { silindi: true, id };
  }

  /** Merkez + shobe sayi */
  async merkezStatistikasi() {
    return this.prisma.$queryRaw<
      { merkez: string; shobe_sayi: number; emekdas_sayi: number }[]
    >`
      SELECT m.ad AS merkez,
             count(DISTINCT s.id)::int AS shobe_sayi,
             count(DISTINCT e.id)::int AS emekdas_sayi
        FROM struktur.merkezler m
        LEFT JOIN struktur.shobeler  s ON s.merkez_id = m.id
        LEFT JOIN kadrlar.emekdaslar e ON e.merkez_id = m.id
       GROUP BY m.ad
       ORDER BY shobe_sayi DESC, emekdas_sayi DESC`;
  }

  /**
   * Siralama sutununu yoxlayir.
   * Sukutla 'id'-ye dusmek SƏHVDİR — istifadeci yazdiği sütunun
   * işlədiyini düşünər. Ona görə açıq xəta atiriq.
   */
  private sutunYoxla(sutun?: string): string {
    if (!sutun) return 'id';
    if (!(SIRALAMA_ICAZELI as readonly string[]).includes(sutun)) {
      throw new BadRequestException(
        `Bu sutun uzre siralama mumkun deyil: "${sutun}". ` +
        `Icazeli sutunlar: ${SIRALAMA_ICAZELI.join(', ')}`,
      );
    }
    return sutun;
  }

  /** Eyni adli merkez varmi? */
  private async adYoxla(ad: string, xaricId?: number): Promise<void> {
    const setirler = await this.prisma.$queryRaw<{ id: number }[]>`
      SELECT id::int FROM struktur.merkezler
       WHERE lower(ad) = lower(${ad})
         AND (${xaricId ?? null}::int IS NULL OR id <> ${xaricId ?? null})`;

    if (setirler.length) {
      throw new ConflictException(`Bu adla merkez artiq movcuddur: "${ad}"`);
    }
  }

  /** Id-nin musbet tam eded oldugunu yoxla */
  static idYoxla(id: number): void {
    if (!Number.isInteger(id) || id <= 0) {
      throw new BadRequestException('id musbet tam eded olmalidir');
    }
  }
}
KODSON
echo "  ✓ src/struktur/struktur.service.ts"

cat > "src/struktur/struktur.controller.ts" <<'KODSON'
import {
  Body, Controller, Delete, Get, HttpCode, HttpStatus, Param,
  ParseIntPipe, Patch, Post, Query,
} from '@nestjs/common';
import {
  ApiOperation, ApiParam, ApiResponse, ApiTags,
} from '@nestjs/swagger';
import { StrukturService, Merkez } from './struktur.service.js';
import { CreateMerkezDto } from './dto/create-merkez.dto.js';
import { UpdateMerkezDto } from './dto/update-merkez.dto.js';
import { MerkezFiltrDto } from './dto/merkez-filtr.dto.js';
import { Sehifelenmis } from '../common/dto/sehife.dto.js';

@ApiTags('struktur')
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
  @ApiOperation({ summary: 'Yeni merkez yarat' })
  @ApiResponse({ status: 201, description: 'Yaradildi' })
  @ApiResponse({ status: 409, description: 'Bu adla merkez artiq var' })
  yarat(@Body() dto: CreateMerkezDto): Promise<Merkez> {
    return this.struktur.yarat(dto);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Merkezi yenile (yalniz gonderilen saheler)' })
  yenile(
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: UpdateMerkezDto,
  ): Promise<Merkez> {
    return this.struktur.yenile(id, dto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Merkezi sil' })
  @ApiResponse({ status: 409, description: 'Bagli shobeler var' })
  sil(@Param('id', ParseIntPipe) id: number) {
    return this.struktur.sil(id);
  }
}
KODSON
echo "  ✓ src/struktur/struktur.controller.ts"

cat > "src/kadrlar/dto/emekdas-filtr.dto.ts" <<'KODSON'
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
KODSON
echo "  ✓ src/kadrlar/dto/emekdas-filtr.dto.ts"

cat > "src/kadrlar/kadrlar.service.ts" <<'KODSON'
import {
  BadRequestException, Injectable, NotFoundException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';
import { EmekdasFiltrDto } from './dto/emekdas-filtr.dto.js';
import { Sehifelenmis } from '../common/dto/sehife.dto.js';

/** Tam profil — 5 cedvelin birlesmesi */
export interface EmekdasTam {
  id: number;
  tam_adi: string;
  vezife: string | null;
  shobe: string | null;
  merkez: string | null;
  cins: string | null;
  elmi_derece: string | null;
  elmi_ad: string | null;
  email: string | null;
  telefon: string | null;
  ise_baslama: string | null;
  maas: number | null;
  aktiv: boolean;
}

/** SQL injection qorumasi — siralama sutunlari */
const SIRALAMA_ICAZELI = [
  'id', 'tam_adi', 'vezife', 'merkez', 'maas', 'ise_baslama',
] as const;

const BIRLESME = `
  FROM kadrlar.emekdaslar e
  LEFT JOIN struktur.vezifeler   v  ON v.id  = e.vezife_id
  LEFT JOIN struktur.shobeler    s  ON s.id  = e.shobe_id
  LEFT JOIN struktur.merkezler   m  ON m.id  = e.merkez_id
  LEFT JOIN ortaq.cinsiyyet      c  ON c.id  = e.cinsiyyet_id
  LEFT JOIN ortaq.elmi_dereceler d  ON d.id  = e.elmi_derece_id
  LEFT JOIN ortaq.elmi_adlar     a  ON a.id  = e.elmi_ad_id
`;

const SAHELER = `
  e.id::int                                   AS id,
  e.soyad || ' ' || e.ad || ' ' || e.ata_adi AS tam_adi,
  v.ad                                        AS vezife,
  s.ad                                        AS shobe,
  m.ad                                        AS merkez,
  c.ad                                        AS cins,
  d.ad                                        AS elmi_derece,
  a.ad                                        AS elmi_ad,
  e.email,
  e.telefon,
  e.ise_baslama::text                         AS ise_baslama,
  e.maas::float8                              AS maas,
  e.aktiv
`;

@Injectable()
export class KadrlarService {
  constructor(private readonly prisma: PrismaService) {}

  /** Filtri SQL serti + parametrlere cevirir */
  private sertQur(dto: EmekdasFiltrDto): { where: string; parametrler: unknown[] } {
    const sertler: string[] = [];
    const parametrler: unknown[] = [];
    let n = 1;

    const axtar = dto.axtar?.trim();
    if (axtar) {
      sertler.push(
        `(e.ad ILIKE $${n} OR e.soyad ILIKE $${n} OR e.ata_adi ILIKE $${n}
          OR e.email ILIKE $${n} OR e.telefon ILIKE $${n})`,
      );
      parametrler.push(`%${axtar}%`);
      n++;
    }

    const sadə: [keyof EmekdasFiltrDto, string][] = [
      ['merkez_id', 'e.merkez_id'],
      ['shobe_id', 'e.shobe_id'],
      ['vezife_id', 'e.vezife_id'],
      ['elmi_derece_id', 'e.elmi_derece_id'],
    ];

    for (const [acar, sutun] of sadə) {
      const deyer = dto[acar];
      if (deyer !== undefined && deyer !== null) {
        sertler.push(`${sutun} = $${n}`);
        parametrler.push(deyer);
        n++;
      }
    }

    if (dto.aktiv !== undefined) {
      sertler.push(`e.aktiv = $${n}`);
      parametrler.push(dto.aktiv);
      n++;
    }

    if (dto.min_maas !== undefined) {
      sertler.push(`e.maas >= $${n}`);
      parametrler.push(dto.min_maas);
      n++;
    }

    if (dto.max_maas !== undefined) {
      sertler.push(`e.maas <= $${n}`);
      parametrler.push(dto.max_maas);
      n++;
    }

    const where = sertler.length ? `WHERE ${sertler.join(' AND ')}` : '';
    return { where, parametrler };
  }

  /** Sehifelenmis emekdas siyahisi */
  async emekdaslar(dto: EmekdasFiltrDto): Promise<Sehifelenmis<EmekdasTam>> {
    const { where, parametrler } = this.sertQur(dto);

    const sutun = this.sutunYoxla(dto.siralama_sah);
    const istiqamet = dto.siralama === 'desc' ? 'DESC' : 'ASC';

    const setirler = await this.prisma.$queryRawUnsafe<EmekdasTam[]>(
      `SELECT ${SAHELER} ${BIRLESME} ${where}
        ORDER BY ${sutun} ${istiqamet}
        LIMIT $${parametrler.length + 1} OFFSET $${parametrler.length + 2}`,
      ...parametrler, dto.limit, dto.offset,
    );

    const cemCavab = await this.prisma.$queryRawUnsafe<{ cem: number }[]>(
      `SELECT count(*)::int AS cem ${BIRLESME} ${where}`,
      ...parametrler,
    );

    const umumi = cemCavab[0]?.cem ?? 0;

    return {
      data: setirler,
      meta: {
        sehife: dto.sehife,
        limit: dto.limit,
        cem: umumi,
        sehife_sayi: Math.ceil(umumi / dto.limit) || 1,
      },
    };
  }

  /** Siralama sutununu yoxlayir — yanlis sutun 400 verir */
  private sutunYoxla(sutun?: string): string {
    if (!sutun) return 'id';
    if (!(SIRALAMA_ICAZELI as readonly string[]).includes(sutun)) {
      throw new BadRequestException(
        `Bu sutun uzre siralama mumkun deyil: "${sutun}". ` +
        `Icazeli sutunlar: ${SIRALAMA_ICAZELI.join(', ')}`,
      );
    }
    return sutun;
  }

  /** Bir emekdasin tam profili */
  async emekdas(id: number): Promise<EmekdasTam> {
    const setirler = await this.prisma.$queryRawUnsafe<EmekdasTam[]>(
      `SELECT ${SAHELER} ${BIRLESME} WHERE e.id = $1`, id,
    );
    if (!setirler.length) {
      throw new NotFoundException(`Emekdas tapilmadi: id=${id}`);
    }
    return setirler[0];
  }

  /** Merkez ve vezife uzre icmal */
  async icmal() {
    const merkezUzre = await this.prisma.$queryRaw<
      { merkez: string; emekdas: number; orta_maas: number; fond: number }[]
    >`
      SELECT m.ad AS merkez,
             count(e.id)::int                 AS emekdas,
             COALESCE(round(avg(e.maas), 2), 0)::float8 AS orta_maas,
             COALESCE(sum(e.maas), 0)::float8 AS fond
        FROM struktur.merkezler m
        LEFT JOIN kadrlar.emekdaslar e ON e.merkez_id = m.id
       GROUP BY m.ad ORDER BY fond DESC`;

    const vezifeUzre = await this.prisma.$queryRaw<
      { vezife: string; seviyye: number; emekdas: number }[]
    >`
      SELECT v.ad AS vezife, v.seviyye, count(e.id)::int AS emekdas
        FROM struktur.vezifeler v
        LEFT JOIN kadrlar.emekdaslar e ON e.vezife_id = v.id
       GROUP BY v.ad, v.seviyye ORDER BY v.seviyye`;

    const umumi = await this.prisma.$queryRaw<{ fond: number; say: number }[]>`
      SELECT COALESCE(sum(maas), 0)::float8 AS fond,
             count(*)::int AS say
        FROM kadrlar.emekdaslar WHERE aktiv = true`;

    return {
      merkez_uzre: merkezUzre,
      vezife_uzre: vezifeUzre,
      umumi_fond: umumi[0]?.fond ?? 0,
      aktiv_say: umumi[0]?.say ?? 0,
    };
  }
}
KODSON
echo "  ✓ src/kadrlar/kadrlar.service.ts"

cat > "src/kadrlar/kadrlar.controller.ts" <<'KODSON'
import { Controller, Get, Param, ParseIntPipe, Query } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { KadrlarService, EmekdasTam } from './kadrlar.service.js';
import { EmekdasFiltrDto } from './dto/emekdas-filtr.dto.js';
import { Sehifelenmis } from '../common/dto/sehife.dto.js';

@ApiTags('kadrlar')
@Controller('kadrlar/emekdaslar')
export class KadrlarController {
  constructor(private readonly kadrlar: KadrlarService) {}

  @Get()
  @ApiOperation({
    summary: 'Emekdaslarin siyahisi',
    description:
      'Tam profil (merkez, shobe, vezife, elmi derece) + sehifeleme, ' +
      'axtaris, filtr ve siralama.',
  })
  siyahi(@Query() filtr: EmekdasFiltrDto): Promise<Sehifelenmis<EmekdasTam>> {
    return this.kadrlar.emekdaslar(filtr);
  }

  @Get('icmal')
  @ApiOperation({ summary: 'Kadr icmali — merkez ve vezife uzre' })
  icmal() {
    return this.kadrlar.icmal();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Bir emekdasin tam profili' })
  bir(@Param('id', ParseIntPipe) id: number): Promise<EmekdasTam> {
    return this.kadrlar.emekdas(id);
  }
}
KODSON
echo "  ✓ src/kadrlar/kadrlar.controller.ts"

cat > "src/kadrlar/kadrlar.module.ts" <<'KODSON'
import { Module } from '@nestjs/common';
import { KadrlarService } from './kadrlar.service.js';
import { KadrlarController } from './kadrlar.controller.js';

@Module({
  controllers: [KadrlarController],
  providers: [KadrlarService],
})
export class KadrlarModule {}
KODSON
echo "  ✓ src/kadrlar/kadrlar.module.ts"

cat > "src/app.module.ts" <<'KODSON'
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module.js';
import { SaglamliqModule } from './saglamliq/saglamliq.module.js';
import { StrukturModule } from './struktur/struktur.module.js';
import { KadrlarModule } from './kadrlar/kadrlar.module.js';
import { HesabatlarModule } from './hesabatlar/hesabatlar.module.js';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    SaglamliqModule,
    StrukturModule,
    KadrlarModule,
    HesabatlarModule,
  ],
})
export class AppModule {}
KODSON
echo "  ✓ src/app.module.ts"

cat > "src/hesabatlar/hesabatlar.service.ts" <<'KODSON'
import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

/** Hesabat modulu — hazir view ve funksiyalari isledir */
@Injectable()
export class HesabatlarService {
  constructor(private readonly prisma: PrismaService) {}

  /** Bazadaki butun view-lar */
  async gorunusler() {
    return this.prisma.$queryRaw<{ sxem: string; gorunus: string }[]>`
      SELECT table_schema AS sxem, table_name AS gorunus
        FROM information_schema.views
       WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
       ORDER BY 1, 2`;
  }

  /** Merkez -> shobe sayi (view-dan) */
  async merkezShobe() {
    return this.prisma.$queryRaw<
      { merkez_id: number; merkez: string; shobe_sayi: number }[]
    >`
      SELECT merkez_id::int, merkez, shobe_sayi
        FROM struktur.v_merkez_shobe_sayi
       ORDER BY shobe_sayi DESC`;
  }

  /** Emekdasin tam profili (view-dan) */
  async emekdasTam(limit = 20) {
    return this.prisma.$queryRawUnsafe<
      {
        id: number; tam_adi: string; vezife: string | null;
        shobe: string | null; merkez: string | null;
        maas: number | null; status: string | null;
      }[]
    >(
      `SELECT id::int, tam_adi, vezife, shobe, merkez, maas::float8, status
         FROM kadrlar.v_emekdas_tam ORDER BY maas DESC NULLS LAST LIMIT $1`,
      limit,
    );
  }

  /** Budce istifadesi (view-dan) */
  async budceIstifadesi() {
    return this.prisma.$queryRaw<
      {
        budce_id: number; il: number; menbe: string;
        plan_mebleg: number; xerclenmis: number; qaliq: number;
      }[]
    >`
      SELECT budce_id::int, il, menbe,
             plan_mebleg::float8, xerclenmis::float8, qaliq::float8
        FROM maliyye.v_budce_istifadesi ORDER BY il DESC, plan_mebleg DESC`;
  }

  /** Telim qrupu -> istirakci sayi (view-dan) */
  async telimQruplari() {
    return this.prisma.$queryRaw<
      { qrup_id: number; qrup: string; proqram: string; status: string; istirakci_sayi: number }[]
    >`
      SELECT qrup_id::int, qrup, proqram, status, istirakci_sayi
        FROM tehsil.v_telim_qrup_istirakci_sayi
       ORDER BY istirakci_sayi DESC`;
  }

  /** Butun funksiyalari bir sorguda cagir */
  async funksiyalar() {
    const setirler = await this.prisma.$queryRaw<
      {
        maas_fondu: number; orta_bal: number; budce_2026: number;
        sertifikasiya_ortalamasi: number;
      }[]
    >`
      SELECT kadrlar.fn_maas_fondu()::float8              AS maas_fondu,
             tehsil.fn_sertifikasiya_ortalamasi()::float8 AS orta_bal,
             maliyye.fn_budce_il_cemi(2026)::float8       AS budce_2026,
             tehsil.fn_sertifikasiya_ortalamasi()::float8 AS sertifikasiya_ortalamasi`;
    return setirler[0];
  }

  /** Il uzre budce icmali — ROLLUP ile yekun */
  async budceIcmali() {
    return this.prisma.$queryRaw<
      { il: string; setir: number; mebleg: number }[]
    >`
      SELECT COALESCE(il::text, 'CƏMİ') AS il,
             count(*)::int              AS setir,
             sum(mebleg)::float8        AS mebleg
        FROM maliyye.budce
       GROUP BY ROLLUP (il)
       ORDER BY il NULLS LAST`;
  }

  /** En son audit qeydleri */
  async sonAudit(limit = 10) {
    return this.prisma.$queryRawUnsafe<
      { id: number; cedvel_adi: string; emeliyyat: string; istifadeci: string | null; vaxt: string }[]
    >(
      `SELECT id::int, cedvel_adi, emeliyyat, istifadeci, vaxt::text
         FROM audit.audit_log ORDER BY vaxt DESC LIMIT $1`,
      limit,
    );
  }

  /** Umumi baza icmali — dashboard ucun */
  async umumiIcmal() {
    const cedveller = await this.prisma.$queryRaw<{ cedvel: number; gorunus: number }[]>`
      SELECT count(*)::int AS cedvel FROM information_schema.tables
       WHERE table_type = 'BASE TABLE'
         AND table_schema NOT IN ('pg_catalog', 'information_schema')`;
    const gorunus = await this.prisma.$queryRaw<{ say: number }[]>`
      SELECT count(*)::int AS say FROM information_schema.views
       WHERE table_schema NOT IN ('pg_catalog', 'information_schema')`;
    const emekdas = await this.prisma.$queryRaw<{ say: number; fon: number }[]>`
      SELECT count(*)::int AS say, COALESCE(sum(maas), 0)::float8 AS fon
        FROM kadrlar.emekdaslar WHERE aktiv = true`;
    const layihe = await this.prisma.$queryRaw<{ say: number }[]>`
      SELECT count(*)::int AS say FROM elm.tedqiqat_layiheleri WHERE status = 'davam edir'`;

    return {
      cedvel_sayi: cedveller[0]?.cedvel ?? 0,
      gorunus_sayi: gorunus[0]?.say ?? 0,
      aktiv_emekdas: emekdas[0]?.say ?? 0,
      emek_haqqi_fondu: emekdas[0]?.fon ?? 0,
      davam_eden_layihe: layihe[0]?.say ?? 0,
    };
  }
}
KODSON
echo "  ✓ src/hesabatlar/hesabatlar.service.ts"

cat > "src/hesabatlar/hesabatlar.controller.ts" <<'KODSON'
import { Controller, Get, Query, ParseIntPipe } from '@nestjs/common';
import { ApiOperation, ApiQuery, ApiTags } from '@nestjs/swagger';
import { HesabatlarService } from './hesabatlar.service.js';

@ApiTags('hesabatlar')
@Controller('hesabatlar')
export class HesabatlarController {
  constructor(private readonly hesabat: HesabatlarService) {}

  @Get('icmal')
  @ApiOperation({ summary: 'Dashboard ucun umumi icmal' })
  icmal() { return this.hesabat.umumiIcmal(); }

  @Get('gorunusler')
  @ApiOperation({ summary: 'Bazadaki butun view-lar' })
  gorunusler() { return this.hesabat.gorunusler(); }

  @Get('merkez-shobe')
  @ApiOperation({ summary: 'Merkez uzre shobe sayi (view)' })
  merkezShobe() { return this.hesabat.merkezShobe(); }

  @Get('emekdaslar')
  @ApiOperation({ summary: 'Emekdaslarin tam profili (view)' })
  @ApiQuery({ name: 'limit', required: false, example: 20 })
  emekdasTam(@Query('limit', new ParseIntPipe({ optional: true })) limit?: number) {
    return this.hesabat.emekdasTam(limit ?? 20);
  }

  @Get('budce')
  @ApiOperation({ summary: 'Budce istifadesi (view)' })
  budce() { return this.hesabat.budceIstifadesi(); }

  @Get('budce-icmali')
  @ApiOperation({ summary: 'Il uzre budce — ROLLUP yekunu ile' })
  budceIcmali() { return this.hesabat.budceIcmali(); }

  @Get('telim-qruplari')
  @ApiOperation({ summary: 'Telim qruplari ve istirakci sayi (view)' })
  telimQruplari() { return this.hesabat.telimQruplari(); }

  @Get('funksiyalar')
  @ApiOperation({ summary: 'Bazadaxili funksiyalarin neticeleri' })
  funksiyalar() { return this.hesabat.funksiyalar(); }

  @Get('audit')
  @ApiOperation({ summary: 'En son audit qeydleri' })
  @ApiQuery({ name: 'limit', required: false, example: 10 })
  audit(@Query('limit', new ParseIntPipe({ optional: true })) limit?: number) {
    return this.hesabat.sonAudit(limit ?? 10);
  }
}
KODSON
echo "  ✓ src/hesabatlar/hesabatlar.controller.ts"

cat > "src/hesabatlar/hesabatlar.module.ts" <<'KODSON'
import { Module } from '@nestjs/common';
import { HesabatlarService } from './hesabatlar.service.js';
import { HesabatlarController } from './hesabatlar.controller.js';

@Module({
  controllers: [HesabatlarController],
  providers: [HesabatlarService],
})
export class HesabatlarModule {}
KODSON
echo "  ✓ src/hesabatlar/hesabatlar.module.ts"

cat > "src/saglamliq/saglamliq.controller.ts" <<'KODSON'
import { Controller, Get } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { PrismaService } from '../prisma/prisma.service.js';

@ApiTags('saglamliq')
@Controller()
export class SaglamliqController {
  constructor(private readonly prisma: PrismaService) {}

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

cat > "src/saglamliq/saglamliq.module.ts" <<'KODSON'
import { Module } from '@nestjs/common';
import { SaglamliqController } from './saglamliq.controller.js';

@Module({ controllers: [SaglamliqController] })
export class SaglamliqModule {}
KODSON
echo "  ✓ src/saglamliq/saglamliq.module.ts"

cat > "src/common/dto/sehife.dto.spec.ts" <<'KODSON'
import { describe, it, expect } from 'vitest';
import { plainToInstance } from 'class-transformer';
import { validate } from 'class-validator';
import { SehifeDto } from './sehife.dto.js';

/** DTO validasiyasini birbasa yoxlayiriq (HTTP olmadan) */
async function yoxla(xam: Record<string, unknown>) {
  const dto = plainToInstance(SehifeDto, xam);
  return validate(dto);
}

describe('SehifeDto', () => {
  it('bos obyekt ucun susmaya gore deyerler', () => {
    const dto = new SehifeDto();
    expect(dto.sehife).toBe(1);
    expect(dto.limit).toBe(20);
    expect(dto.siralama).toBe('asc');
    expect(dto.offset).toBe(0);
  });

  it('sehife=3, limit=20 -> offset 40', () => {
    const dto = Object.assign(new SehifeDto(), { sehife: 3, limit: 20 });
    expect(dto.offset).toBe(40);
  });

  it('sehife=0-etibarsizdir', async () => {
    const xetalar = await yoxla({ sehife: 0 });
    expect(xetalar.length).toBeGreaterThan(0);
    expect(Object.keys(xetalar[0].constraints ?? {})).toContain('min');
  });

  it('limit=101-etibarsizdir', async () => {
    const xetalar = await yoxla({ limit: 101 });
    expect(xetalar.length).toBeGreaterThan(0);
  });

  it('limit=100-etibarlidir', async () => {
    expect(await yoxla({ limit: 100 })).toHaveLength(0);
  });

  it('siralama=asc/desc etibarlidir', async () => {
    expect(await yoxla({ siralama: 'asc' })).toHaveLength(0);
    expect(await yoxla({ siralama: 'desc' })).toHaveLength(0);
  });

  it('siralama=xyz etibarsizdir', async () => {
    const xetalar = await yoxla({ siralama: 'xyz' });
    expect(xetalar.length).toBeGreaterThan(0);
    expect(Object.keys(xetalar[0].constraints ?? {})).toContain('isIn');
  });

  it('axtar 100 simvoldan uzun ola bilmez', async () => {
    const xetalar = await yoxla({ axtar: 'a'.repeat(101) });
    expect(xetalar.length).toBeGreaterThan(0);
  });
});
KODSON
echo "  ✓ src/common/dto/sehife.dto.spec.ts"

cat > "src/struktur/struktur.service.spec.ts" <<'KODSON'
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import { StrukturService } from './struktur.service.js';
import { MerkezFiltrDto } from './dto/merkez-filtr.dto.js';

/** Saxta Prisma — real bazaya toxunmuruq */
function saxtaPrisma() {
  return {
    $queryRaw: vi.fn(),
    $queryRawUnsafe: vi.fn(),
    $executeRaw: vi.fn(),
  } as any;
}

function filtr(qismen: Partial<MerkezFiltrDto> = {}): MerkezFiltrDto {
  return Object.assign(new MerkezFiltrDto(), qismen);
}

describe('StrukturService', () => {
  let prisma: any;
  let service: StrukturService;

  beforeEach(() => {
    prisma = saxtaPrisma();
    service = new StrukturService(prisma);
  });

  // ── OXUMA ──
  describe('merkezler()', () => {
    it('sehifelenmis netice qaytarir', async () => {
      prisma.$queryRawUnsafe
        .mockResolvedValueOnce([{ id: 1, ad: 'Elmi katiblik', aktiv: true }])
        .mockResolvedValueOnce([{ cem: 10 }]);

      const n = await service.merkezler(filtr({ limit: 3 }));

      expect(n.data).toHaveLength(1);
      expect(n.meta).toEqual({ sehife: 1, limit: 3, cem: 10, sehife_sayi: 4 });
    });

    it('sehife_sayi sifir olanda 1 qaytarir', async () => {
      prisma.$queryRawUnsafe.mockResolvedValueOnce([]).mockResolvedValueOnce([{ cem: 0 }]);
      const n = await service.merkezler(filtr());
      expect(n.meta.sehife_sayi).toBe(1);
      expect(n.meta.cem).toBe(0);
    });

    it('offset duzgun hesablanir', async () => {
      const f = filtr({ sehife: 3, limit: 20 });
      expect(f.offset).toBe(40);
    });
  });

  describe('merkez()', () => {
    it('movcud merkezi qaytarir', async () => {
      prisma.$queryRaw.mockResolvedValue([{ id: 2, ad: 'Test', aktiv: true }]);
      const m = await service.merkez(2);
      expect(m.id).toBe(2);
    });

    it('tapilmayanda NotFoundException atir', async () => {
      prisma.$queryRaw.mockResolvedValue([]);
      await expect(service.merkez(999)).rejects.toThrow(NotFoundException);
    });
  });

  // ── YAZMA ──
  describe('yarat()', () => {
    it('ad yoxlamasindan sonra yaradir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([])                                   // ad yoxdur
        .mockResolvedValueOnce([{ id: 11, ad: 'Yeni Merkez', aktiv: true }]);

      const m = await service.yarat({ ad: 'Yeni Merkez' });
      expect(m.id).toBe(11);
    });

    it('eyni ad varsa ConflictException atir', async () => {
      prisma.$queryRaw.mockResolvedValue([{ id: 1 }]);

      await expect(service.yarat({ ad: 'Elmi katiblik' }))
        .rejects.toThrow(ConflictException);
    });
  });

  describe('yenile()', () => {
    it('movcud merkezi yenileyir', async () => {
      // yenile() UC sorgu isledir:
      //   1) merkez(id)  2) adYoxla()  3) UPDATE
      prisma.$queryRaw
        .mockResolvedValueOnce([{ id: 5, ad: 'Kohne ad', aktiv: true }])
        .mockResolvedValueOnce([])                                  // ad konflikti yox
        .mockResolvedValueOnce([{ id: 5, ad: 'Yeni ad', aktiv: true }]);

      const m = await service.yenile(5, { ad: 'Yeni ad' });
      expect(m.ad).toBe('Yeni ad');
      expect(prisma.$queryRaw).toHaveBeenCalledTimes(3);
    });

    it('yeni ad basqasinda varsa ConflictException', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([{ id: 5, ad: 'Kohne ad', aktiv: true }])
        .mockResolvedValueOnce([{ id: 8 }]);                        // ad tutulub

      await expect(service.yenile(5, { ad: 'Elmi katiblik' }))
        .rejects.toThrow(ConflictException);
    });

    it('ad deyismirse konflikt yoxlamasi kecirilir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([{ id: 5, ad: 'Eyni ad', aktiv: true }])
        .mockResolvedValueOnce([{ id: 5, ad: 'Eyni ad', aktiv: true }]);

      const m = await service.yenile(5, { ad: 'Eyni ad' });
      expect(m.ad).toBe('Eyni ad');
      expect(prisma.$queryRaw).toHaveBeenCalledTimes(2);   // adYoxla cagirilmadi
    });

    it('movcud olmayan id ucun NotFoundException', async () => {
      prisma.$queryRaw.mockResolvedValue([]);
      await expect(service.yenile(999, { ad: 'X' }))
        .rejects.toThrow(NotFoundException);
    });
  });

  describe('sil()', () => {
    it('bagli shobe varsa ConflictException', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([{ id: 2, ad: 'Test', aktiv: true }])  // merkez var
        .mockResolvedValueOnce([{ say: 7 }]);                          // 7 shobe bagli

      await expect(service.sil(2)).rejects.toThrow(ConflictException);
      expect(prisma.$executeRaw).not.toHaveBeenCalled();
    });

    it('bagli shobe yoxdursa silir', async () => {
      prisma.$queryRaw
        .mockResolvedValueOnce([{ id: 9, ad: 'Test', aktiv: true }])
        .mockResolvedValueOnce([{ say: 0 }]);
      prisma.$executeRaw.mockResolvedValue(1);

      const n = await service.sil(9);
      expect(n).toEqual({ silindi: true, id: 9 });
      expect(prisma.$executeRaw).toHaveBeenCalledTimes(1);
    });
  });

  // ── SQL INJECTION ──
  describe('siralama — SQL injection qorumasi', () => {
    it('icazeli sutun kecir', async () => {
      prisma.$queryRawUnsafe.mockResolvedValue([]);
      await expect(service.merkezler(filtr({ siralama_sah: 'ad' })))
        .resolves.toBeDefined();
    });

    it('icazesiz sutun BadRequestException atir', async () => {
      await expect(service.merkezler(filtr({ siralama_sah: 'DROP TABLE' })))
        .rejects.toThrow(BadRequestException);
      expect(prisma.$queryRawUnsafe).not.toHaveBeenCalled();
    });

    it('SQL fragment sizişi bloklanir', async () => {
      for (const hucum of ['ad; DROP TABLE', '1=1 --', 'ad) UNION SELECT']) {
        await expect(service.merkezler(filtr({ siralama_sah: hucum })))
          .rejects.toThrow(BadRequestException);
      }
    });
  });

  describe('merkezStatistikasi()', () => {
    it('merkez, shobe ve emekdas sayini qaytarir', async () => {
      prisma.$queryRaw.mockResolvedValue([
        { merkez: 'Elmi katiblik', shobe_sayi: 2, emekdas_sayi: 3 },
      ]);
      const n = await service.merkezStatistikasi();
      expect(n[0].shobe_sayi).toBe(2);
      expect(n[0].emekdas_sayi).toBe(3);
    });
  });
});
KODSON
echo "  ✓ src/struktur/struktur.service.spec.ts"

cat > "test/backend2.e2e-spec.ts" <<'KODSON'
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import request from 'supertest';
import { App } from 'supertest/types';
import { AppModule } from '../src/app.module.js';
import { AllExceptionsFilter } from '../src/common/filters/all-exceptions.filter.js';

/**
 * BACKEND-2 e2e testleri.
 * Butun HTTP qatini sinaqdan kecirir: validasiya, filtr, sehifeleme,
 * CRUD, xeta formatlari.
 */
describe('Backend-2 (e2e)', () => {
  let app: INestApplication<App>;

  beforeAll(async () => {
    const modul: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = modul.createNestApplication();

    // main.ts ile EYNI konfiqurasiya — eks halda test real davranisi yoxlamir
    app.setGlobalPrefix('api/v1');
    app.useGlobalPipes(
      new ValidationPipe({
        whitelist: true,
        forbidNonWhitelisted: true,
        transform: true,
      }),
    );
    app.useGlobalFilters(new AllExceptionsFilter());

    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  const url = (yol: string) => `/api/v1${yol}`;

  // ── SAĞLAMLIQ ──
  describe('Saglamliq', () => {
    it('prefikssiz yol 404 qaytarir', () =>
      request(app.getHttpServer()).get('/struktur/merkezler').expect(404));

    it('GET /api/v1/saglamliq baza veziyyetini verir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/saglamliq'))
        .expect(200);

      expect(c.body.status).toBe('saglam');
      expect(c.body.baza.qosulub).toBe(true);
      expect(c.body.baza.cedvel_sayi).toBe(48);
      expect(typeof c.body.baza.gecikme_ms).toBe('number');
    });

    it('GET /api/v1 kok melumat verir', async () => {
      const c = await request(app.getHttpServer()).get(url('')).expect(200);
      expect(c.body.prefiks).toBe('/api/v1');
    });
  });

  // ── STRUKTUR: OXUMA ──
  describe('GET /struktur/merkezler', () => {
    it('sehifelenmis siyahi qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/struktur/merkezler?limit=3'))
        .expect(200);

      expect(Array.isArray(c.body.data)).toBe(true);
      expect(c.body.data.length).toBeLessThanOrEqual(3);
      expect(c.body.meta).toMatchObject({
        sehife: 1,
        limit: 3,
      });
      expect(typeof c.body.meta.cem).toBe('number');
      expect(typeof c.body.meta.sehife_sayi).toBe('number');
    });

    it('axtaris isleyir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/struktur/merkezler?axtar=elmi'))
        .expect(200);
      expect(c.body.meta.cem).toBeGreaterThan(0);
      for (const r of c.body.data) {
        const metn = `${r.ad} ${r.unvan ?? ''} ${r.email ?? ''}`.toLowerCase();
        expect(metn).toContain('elmi');
      }
    });

    it('yanlis limit 400 verir', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler?limit=999'))
        .expect(400));

    it('sehife=0 400 verir', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler?sehife=0'))
        .expect(400));
  });

  describe('GET /struktur/merkezler/:id', () => {
    it('movcud id 200', () =>
      request(app.getHttpServer()).get(url('/struktur/merkezler/1')).expect(200));

    it('movcud olmayan id 404', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler/999999'))
        .expect(404));

    it('reqem olmayan id 400', () =>
      request(app.getHttpServer())
        .get(url('/struktur/merkezler/abc'))
        .expect(400));
  });

  // ── STRUKTUR: CRUD ──
  describe('CRUD /struktur/merkezler', () => {
    let yeniId: number;

    it('POST yeni merkez yaradir (201)', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: `E2E Test Merkezi ${Date.now()}`, tip: 'merkez' })
        .expect(201);

      expect(c.body.id).toBeGreaterThan(0);
      yeniId = c.body.id;
    });

    it('PATCH qismen yenileyir', async () => {
      const c = await request(app.getHttpServer())
        .patch(url(`/struktur/merkezler/${yeniId}`))
        .send({ telefon: '+994 12 000 11 22' })
        .expect(200);
      expect(c.body.telefon).toBe('+994 12 000 11 22');
    });

    it('eyni adla ikinci POST 409 verir', async () => {
      const c1 = await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: `Tekrar Test ${Date.now()}` })
        .expect(201);

      await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: c1.body.ad })
        .expect(409);

      await request(app.getHttpServer())
        .delete(url(`/struktur/merkezler/${c1.body.id}`))
        .expect(200);
    });

    it('qisa ad 400 verir', () =>
      request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: 'AB' })
        .expect(400));

    it('yanlis e-poct 400 verir', () =>
      request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: 'Test Merkez', email: 'sehv' })
        .expect(400));

    it('DTO-da olmayan sahe 400 verir (mass assignment qorumasi)', () =>
      request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: 'Test Merkez', rol: 'admin' })
        .expect(400));

    it('bagli shobesi olan merkez silinmir (409)', () =>
      request(app.getHttpServer())
        .delete(url('/struktur/merkezler/2'))
        .expect(409));

    it('DELETE yaradilmis merkezi silir', () =>
      request(app.getHttpServer())
        .delete(url(`/struktur/merkezler/${yeniId}`))
        .expect(200));
  });

  // ── KADRLAR ──
  describe('GET /kadrlar/emekdaslar', () => {
    it('tam profil qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar?limit=2'))
        .expect(200);

      const r = c.body.data[0];
      expect(r).toHaveProperty('tam_adi');
      expect(r).toHaveProperty('merkez');
      expect(r).toHaveProperty('vezife');
      expect(typeof r.maas === 'number' || r.maas === null).toBe(true);
    });

    it('merkez_id filtri isleyir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar?merkez_id=10'))
        .expect(200);
      expect(c.body.meta.cem).toBeGreaterThan(0);
    });

    it('maas araligi filtri isleyir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar?min_maas=2000&max_maas=3000'))
        .expect(200);
      for (const r of c.body.data) {
        expect(r.maas).toBeGreaterThanOrEqual(2000);
        expect(r.maas).toBeLessThanOrEqual(3000);
      }
    });

    it('siralama=desc isleyir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar?siralama=desc&siralama_sah=maas&limit=5'))
        .expect(200);
      const maaslar = c.body.data.map((r: { maas: number }) => r.maas);
      const siralanmis = [...maaslar].sort((a, b) => b - a);
      expect(maaslar).toEqual(siralanmis);
    });

    it('yanlis siralama sahesi 400 verir', () =>
      request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar?siralama_sah=DROP TABLE'))
        .expect(400));

    it('icmal qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/kadrlar/emekdaslar/icmal'))
        .expect(200);
      expect(c.body).toHaveProperty('umumi_fond');
      expect(Array.isArray(c.body.merkez_uzre)).toBe(true);
    });
  });

  // ── HESABATLAR ──
  describe('GET /hesabatlar', () => {
    it('icmal 48 cedvel ve 8 view gosterir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/hesabatlar/icmal'))
        .expect(200);
      expect(c.body.cedvel_sayi).toBe(48);
      expect(c.body.gorunus_sayi).toBe(8);
    });

    it('8 view siyahilayir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/hesabatlar/gorunusler'))
        .expect(200);
      expect(c.body).toHaveLength(8);
    });

    it('budce ROLLUP yekunu verir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/hesabatlar/budce-icmali'))
        .expect(200);
      const cem = c.body.find((r: { il: string }) => r.il === 'CƏMİ');
      expect(cem).toBeDefined();
      expect(cem.mebleg).toBeGreaterThan(0);
    });

    it('funksiyalar netice qaytarir', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/hesabatlar/funksiyalar'))
        .expect(200);
      expect(typeof c.body.maas_fondu).toBe('number');
    });
  });

  // ── XƏTA FORMATI ──
  describe('Vahid xeta formati', () => {
    it('404 formati duzgundur', async () => {
      const c = await request(app.getHttpServer())
        .get(url('/struktur/merkezler/999999'))
        .expect(404);

      expect(c.body).toMatchObject({
        ugur: false,
        xeta: { kod: 'TAPILMADI' },
      });
      expect(c.body).toHaveProperty('yol');
      expect(c.body).toHaveProperty('vaxt');
    });

    it('validasiya xetasi detallar massivi verir', async () => {
      const c = await request(app.getHttpServer())
        .post(url('/struktur/merkezler'))
        .send({ ad: 'AB', email: 'sehv' })
        .expect(400);

      expect(c.body.ugur).toBe(false);
      expect(c.body.xeta.kod).toBe('YANLIS_SORGU');
      expect(Array.isArray(c.body.xeta.detallar)).toBe(true);
      expect(c.body.xeta.detallar.length).toBeGreaterThanOrEqual(2);
    });
  });
});
KODSON
echo "  ✓ test/backend2.e2e-spec.ts"

echo "════ 2.5/4  Backend-1 fayllari (yoxdursa) ════"
mkdir -p src/struktur

if [ ! -f src/struktur/struktur.module.ts ]; then
cat > src/struktur/struktur.module.ts <<'KODSON'
import { Module } from '@nestjs/common';
import { StrukturService } from './struktur.service.js';
import { StrukturController } from './struktur.controller.js';

@Module({
  controllers: [StrukturController],
  providers: [StrukturService],
})
export class StrukturModule {}
KODSON
echo "  ✓ src/struktur/struktur.module.ts (yeni)"
else
echo "  = src/struktur/struktur.module.ts (movcud)"
fi

if [ ! -f src/prisma/prisma.service.ts ]; then
  echo "XETA: src/prisma/prisma.service.ts yoxdur!"
  echo "      Evvelce Backend-1 dersini icra edin."
  exit 1
fi

echo "════ 3/4  Kohnə fayllar silinir ════"
rm -f src/app.controller.ts src/app.service.ts src/app.controller.spec.ts
rm -f test/app.e2e-spec.ts
echo "  ✓ default NestJS fayllari silindi"

echo "════ 4/4  Yoxlama ════"
unset DATABASE_URL PGHOST
npm run build
echo ""
echo "HAZIR. Testleri isletmek ucun:"
echo "  npm test"
echo "  npx vitest run --config vitest.config.e2e.ts"
