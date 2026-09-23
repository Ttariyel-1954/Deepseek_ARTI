import {
  ArgumentsHost, Catch, ExceptionFilter, HttpException, HttpStatus, Logger,
} from '@nestjs/common';
import type { Request, Response } from 'express';

/** HTTP status kodunu oxunaqlı sabitə çevirir */
const KOD_XERITESI: Record<number, string> = {
  400: 'YANLIS_SORGU',
  401: 'AUTENTIFIKASIYA_LAZIM',
  403: 'ICAZE_YOXDUR',
  404: 'TAPILMADI',
  409: 'TOQQUSMA',
  422: 'EMAL_OLUNMADI',
  500: 'DAXILI_XETA',
};

/**
 * Bütün xətaları VAHDİ formata salır.
 *
 * NestJS-in default formatı:  { statusCode, message, error }
 * Bizim format:               { ugur, xeta: { kod, mesaj, detallar }, yol, vaxt }
 *
 * Niyə vacibdir? Frontend həmişə EYNİ formanı gözləyir — bir yerdə
 * `message`, başqa yerdə `xeta.mesaj` axtarmalı olmur.
 */
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly log = new Logger('XETA');

  catch(xeta: unknown, host: ArgumentsHost): void {
    const ctx = host.switchToHttp();
    const cavab = ctx.getResponse<Response>();
    const sorgu = ctx.getRequest<Request>();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let mesaj: string | string[] = 'Daxili server xətası';
    let kod = 'DAXILI_XETA';

    if (xeta instanceof HttpException) {
      status = xeta.getStatus();
      const govde = xeta.getResponse();

      if (typeof govde === 'string') {
        mesaj = govde;
      } else if (typeof govde === 'object' && govde !== null) {
        const g = govde as Record<string, unknown>;
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
        mesaj: Array.isArray(mesaj) ? 'Validasiya xətası' : mesaj,
        ...(detallar ? { detallar } : {}),
      },
      yol: sorgu.url,
      vaxt: new Date().toISOString(),
    });
  }
}
