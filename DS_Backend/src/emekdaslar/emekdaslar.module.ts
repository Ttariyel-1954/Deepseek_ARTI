import { Module } from '@nestjs/common';
import { PrismaModule } from '../prisma/prisma.module.js';
import { EmekdaslarController } from './emekdaslar.controller.js';
import { EmekdaslarService } from './emekdaslar.service.js';
import { StatistikaController } from './statistika/statistika.controller.js';
import { StatistikaService } from './statistika/statistika.service.js';
import { ElaqelerController } from './elaqeler/elaqeler.controller.js';
import { ElaqelerService } from './elaqeler/elaqeler.service.js';
import { TopluController } from './toplu/toplu.controller.js';
import { TopluService } from './toplu/toplu.service.js';

/**
 * `emekdaslar` — 2A + 2B dərslərinin TAM modulu.
 *
 * ══════════════════════════════════════════════════════════════════
 *  ⚠️ MARŞRUT SIRASI — DƏRSİN ƏN İNCƏ YERİ
 * ══════════════════════════════════════════════════════════════════
 *
 * Dörd controller `emekdaslar` prefiksini paylaşır. Toqquşma YALNIZ
 * İKİ seqmentli yollarda olur:
 *
 *   GET /api/v1/emekdaslar/statistika   ← StatistikaController
 *   GET /api/v1/emekdaslar/:id          ← EmekdaslarController
 *
 * Express marşrutları ELAN SIRASI ilə yoxlayır — BİRİNCİ uyğun gələn
 * qalib gəlir. `:id` əvvəl gəlsəydi, «statistika» sözü ID kimi
 * tutular və `ParseIntPipe` belə cavab verərdi:
 *
 *   HTTP 400
 *   {"xeta":{"mesaj":"Validation failed (numeric string is expected)"}}
 *
 * Bu, ÇOX məkrli səhvidir: statistika endpointi heç vaxt çağırılmır və
 * heç bir xəta mesajı səbəbi demir. Ona görə:
 *
 *   ► KONKRET yollar həmişə `:id`-dən ƏVVƏL yazılır.
 *   ► `:id` olan controller ƏN SONDA gəlir.
 *
 * ⚠️ Niyyə saxlayın: `StatistikaController`-i `StatistikaModule` kimi
 * ayrı modula salıb `imports`-a əlavə etmək KİFAYƏT ETMİR. Nest əvvəlcə
 * modulun ÖZ controller-lərini, sonra import olunanlarınkını qeydiyyatdan
 * keçirir — yəni `:id` yenə qabağa düşər. Sıra yalnız BİR modulun
 * `controllers` massivində AÇIQ şəkildə təyin olunur.
 */
@Module({
  imports: [PrismaModule],
  controllers: [
    StatistikaController, // «statistika»  →  :id-dən ƏVVƏL
    ElaqelerController,   // «:id/...»     →  3 seqment, toqquşmur
    TopluController,      // «toplu/...»   →  3 seqment, toqquşmur
    EmekdaslarController, // «:id»         →  ƏN SONDA!
  ],
  providers: [
    EmekdaslarService,
    StatistikaService,
    ElaqelerService,
    TopluService,
  ],
  exports: [
    EmekdaslarService,
    StatistikaService,
    ElaqelerService,
    TopluService,
  ],
})
export class EmekdaslarModule {}
