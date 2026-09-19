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
