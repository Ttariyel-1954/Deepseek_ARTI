import { Injectable } from '@nestjs/common';
import { Prisma } from '../../generated/prisma/client.js';
import { PrismaService } from '../../prisma/prisma.service.js';

/** Bir mərkəz üzrə yekun göstəricilər */
export interface MerkezStatistikasi {
  merkez_id: number | null;
  merkez: string;
  emekdas_sayi: number;
  orta_maas: number;
  min_maas: number;
  maks_maas: number;
  maas_fondu: number;
}

/** Bir vəzifə üzrə yekun göstəricilər */
export interface VezifeStatistikasi {
  vezife_id: number;
  vezife: string;
  seviyye: number | null;
  emekdas_sayi: number;
}

/** Ümumi mənzərə */
export interface UmumiStatistika {
  emekdas: { cem: number; aktiv: number; passiv: number };
  maas: { fondu: number; orta: number; min: number; maks: number };
  elaqeler: {
    doktorant: number;
    sertifikat: number;
    mezuniyyet: number;
    tecrube: number;
    layihe: number;
    shura_uzvu: number;
  };
  baza_funksiyalari: { maas_fondu: number; sertifikasiya_ortalamasi: number };
  cedvel_sayi: number;
  hesablanma_ms: number;
}

/** `Prisma.Decimal` və ya `null` gələ bilər — təhlükəsiz ədədə çevirir */
function eded(d: Prisma.Decimal | number | null | undefined): number {
  if (d === null || d === undefined) return 0;
  const n = Number(d);
  return Number.isFinite(n) ? Math.round(n * 100) / 100 : 0;
}

@Injectable()
export class StatistikaService {
  constructor(private readonly prisma: PrismaService) {}

  // ── 1. Ümumi mənzərə ─────────────────────────────────────────────
  async umumi(): Promise<UmumiStatistika> {
    const baslama = Date.now();

    // ⚠️ Niyə `$transaction`? Çünki 9 fərqli sayğac BİR mənzərə yaratmalıdır.
    // Ayrı-ayrı göndərsəydik, hesabat çıxarıldığı anda biri yeni əməkdaş
    // əlavə edə bilərdi və rəqəmlər bir-birinə uyğun gəlməzdi.
    const [
      cem, aktiv, passiv,
      maasAqreqat,
      doktorant, sertifikat, mezuniyyet, tecrube, layihe, shura,
      maasFondu, sertOrt,
      cedvelSayi,
    ] = await this.prisma.$transaction([
      this.prisma.emekdaslar.count(),
      this.prisma.emekdaslar.count({ where: { aktiv: true } }),
      this.prisma.emekdaslar.count({ where: { aktiv: false } }),
      this.prisma.emekdaslar.aggregate({
        where: { aktiv: true },
        _sum: { maas: true },
        _avg: { maas: true },
        _min: { maas: true },
        _max: { maas: true },
      }),
      this.prisma.doktorantlar.count(),
      this.prisma.sertifikasiya.count(),
      this.prisma.mezuniyyetler.count(),
      this.prisma.is_tecrubesi.count(),
      this.prisma.tedqiqat_layiheleri.count(),
      this.prisma.elmi_shura_uzvleri.count(),
      // ⚠️ Bazada ARTIQ YAZILMIŞ PL/pgSQL funksiyasını çağırırıq.
      // `$queryRaw` şablon sətri (template literal) parametrləri
      // AVTOMATİK parametrləşdirir — SQL inyeksiyası mümkün deyil.
      this.prisma.$queryRaw<{ cem: Prisma.Decimal }[]>`
        SELECT kadrlar.fn_maas_fondu() AS cem`,
      this.prisma.$queryRaw<{ ort: Prisma.Decimal }[]>`
        SELECT tehsil.fn_sertifikasiya_ortalamasi() AS ort`,
      this.prisma.$queryRaw<{ say: bigint }[]>`
        SELECT count(*)::bigint AS say
          FROM information_schema.tables
         WHERE table_type = 'BASE TABLE'
           AND table_schema NOT IN ('pg_catalog', 'information_schema')`,
    ]);

    return {
      emekdas: { cem, aktiv, passiv },
      maas: {
        fondu: eded(maasAqreqat._sum.maas),
        orta: eded(maasAqreqat._avg.maas),
        min: eded(maasAqreqat._min.maas),
        maks: eded(maasAqreqat._max.maas),
      },
      elaqeler: {
        doktorant, sertifikat, mezuniyyet, tecrube, layihe, shura_uzvu: shura,
      },
      baza_funksiyalari: {
        maas_fondu: eded(maasFondu[0]?.cem),
        sertifikasiya_ortalamasi: eded(sertOrt[0]?.ort),
      },
      cedvel_sayi: Number(cedvelSayi[0]?.say ?? 0),
      hesablanma_ms: Date.now() - baslama,
    };
  }

  // ── 2. Mərkəzlər üzrə ────────────────────────────────────────────
  async merkezler(aktiv: 'aktiv' | 'hamisi', minSay: number,
                  siralama: 'say' | 'ad' | 'orta_maas'): Promise<MerkezStatistikasi[]> {
    const where: Prisma.emekdaslarWhereInput =
      aktiv === 'aktiv' ? { aktiv: true } : {};

    const qruplar = await this.prisma.emekdaslar.groupBy({
      by: ['merkez_id'],
      where,
      _count: { _all: true },
      _avg: { maas: true },
      _min: { maas: true },
      _max: { maas: true },
      _sum: { maas: true },
    });

    const idler = qruplar
      .map((q) => q.merkez_id)
      .filter((id): id is number => id !== null);

    const merkezler = await this.prisma.merkezler.findMany({
      where: { id: { in: idler } },
      select: { id: true, ad: true },
    });
    const adlar = new Map(merkezler.map((m) => [m.id, m.ad]));

    const netice: MerkezStatistikasi[] = qruplar
      .filter((q) => q._count._all >= minSay)
      .map((q) => ({
        merkez_id: q.merkez_id,
        merkez: q.merkez_id === null
          ? '(mərkəz təyin olunmayıb)'
          : (adlar.get(q.merkez_id) ?? `ID ${q.merkez_id}`),
        emekdas_sayi: q._count._all,
        orta_maas: eded(q._avg.maas),
        min_maas: eded(q._min.maas),
        maks_maas: eded(q._max.maas),
        maas_fondu: eded(q._sum.maas),
      }));

    if (siralama === 'ad') {
      netice.sort((a, b) => a.merkez.localeCompare(b.merkez, 'az'));
    } else if (siralama === 'orta_maas') {
      netice.sort((a, b) => b.orta_maas - a.orta_maas);
    } else {
      netice.sort((a, b) => b.emekdas_sayi - a.emekdas_sayi);
    }

    return netice;
  }

  // ── 3. Vəzifələr üzrə ────────────────────────────────────────────
  async vezifeler(aktiv: 'aktiv' | 'hamisi', minSay: number,
                  siralama: 'say' | 'ad' | 'orta_maas'): Promise<VezifeStatistikasi[]> {
    const qruplar = await this.prisma.emekdaslar.groupBy({
      by: ['vezife_id'],
      where: aktiv === 'aktiv' ? { aktiv: true } : {},
      _count: { _all: true },
    });

    const vezifeler = await this.prisma.vezifeler.findMany({
      select: { id: true, ad: true, seviyye: true },
    });
    const xerite = new Map(vezifeler.map((v) => [v.id, v]));

    const netice: VezifeStatistikasi[] = qruplar
      .filter((q) => q._count._all >= minSay)
      .map((q) => ({
        vezife_id: q.vezife_id,
        vezife: xerite.get(q.vezife_id)?.ad ?? `ID ${q.vezife_id}`,
        seviyye: xerite.get(q.vezife_id)?.seviyye ?? null,
        emekdas_sayi: q._count._all,
      }));

    if (siralama === 'ad') {
      netice.sort((a, b) => a.vezife.localeCompare(b.vezife, 'az'));
    } else {
      netice.sort((a, b) => b.emekdas_sayi - a.emekdas_sayi);
    }

    return netice;
  }

  // ── 4. Şöbə sayı — parametrli baza funksiyası ────────────────────
  async merkezShobeSayi(merkezId: number): Promise<{ merkez_id: number; shobe_sayi: number }> {
    const netice = await this.prisma.$queryRaw<{ say: number }[]>`
      SELECT struktur.fn_shobe_sayi(${merkezId}::int) AS say`;

    return { merkez_id: merkezId, shobe_sayi: Number(netice[0]?.say ?? 0) };
  }

  // ── 5. Bütün mərkəzlər + şöbə sayı (N+1 problemi) ────────────────
  async butunMerkezler(): Promise<
    { id: number; ad: string; tip: string; shobe_sayi: number; emekdas_sayi: number }[]
  > {
    const merkezler = await this.prisma.merkezler.findMany({
      select: { id: true, ad: true, tip: true },
      orderBy: { ad: 'asc' },
    });

    // ⚠️ N+1 PROBLEMİ: hər mərkəz üçün ayrı sorğu göndərsəydik,
    // 10 mərkəz = 20 sorğu olardı. Biz əvəzinə İKİ sorğu göndəririk
    // və nəticələri yaddaşda birləşdiririk.
    const [shobeSaylari, emekdasSaylari] = await Promise.all([
      this.prisma.shobeler.groupBy({ by: ['merkez_id'], _count: { _all: true } }),
      this.prisma.emekdaslar.groupBy({
        by: ['merkez_id'],
        where: { aktiv: true },
        _count: { _all: true },
      }),
    ]);

    const shobeXerite = new Map(
      shobeSaylari.map((s) => [s.merkez_id, s._count._all]),
    );
    const emekdasXerite = new Map(
      emekdasSaylari
        .filter((e) => e.merkez_id !== null)
        .map((e) => [e.merkez_id as number, e._count._all]),
    );

    return merkezler.map((m) => ({
      id: m.id,
      ad: m.ad,
      tip: m.tip,
      shobe_sayi: shobeXerite.get(m.id) ?? 0,
      emekdas_sayi: emekdasXerite.get(m.id) ?? 0,
    }));
  }
}
