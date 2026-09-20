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
