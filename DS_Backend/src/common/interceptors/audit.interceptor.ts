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
