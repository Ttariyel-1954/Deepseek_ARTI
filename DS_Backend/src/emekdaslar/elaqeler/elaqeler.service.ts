import { Injectable, NotFoundException } from '@nestjs/common';
import { Prisma } from '../../generated/prisma/client.js';
import { PrismaService } from '../../prisma/prisma.service.js';

/** `YYYY-MM-DD` — yalnız gün */
function tarix(d: Date | null): string | null {
  return d ? d.toISOString().slice(0, 10) : null;
}

/** `Prisma.Decimal | null` → mətn (pul dəqiqliyi qorunur) */
function pul(d: Prisma.Decimal | null): string | null {
  return d === null ? null : d.toFixed(2);
}

export interface DoktorantCavabi {
  id: number;
  ad_soyad: string;
  status: string;
  proqram: string | null;
  qebul_tarixi: string | null;
  mudafie_tarixi: string | null;
  qeyd: string | null;
}

export interface SertifikatCavabi {
  id: number;
  ad_soyad: string;
  tip: string;
  imtahan_tarixi: string | null;
  bal: string | null;
  netice: string;
  sertifikat_no: string | null;
}

export interface MezuniyyetCavabi {
  id: number;
  mezuniyyet_tipi: string;
  baslama_tarixi: string;
  bitme_tarixi: string;
  gun_sayi: number | null;
  status: string;
}

export interface TecrubeCavabi {
  id: number;
  is_yeri: string;
  vezife: string | null;
  baslama_tarixi: string | null;
  bitme_tarixi: string | null;
}

export interface LayiheCavabi {
  id: number;
  ad: string;
  status: string;
  istiqamet: string | null;
  baslama_tarixi: string | null;
  bitme_tarixi: string | null;
}

export interface ShuraCavabi {
  id: number;
  ad_soyad: string;
  vezife: string | null;
  elmi_derece: string | null;
  elmi_ad: string | null;
  status: string;
  qosulma_tarixi: string | null;
  aktiv: boolean;
}

export interface ElaqeIcmali {
  emekdas_id: string;
  tam_ad: string;
  aktiv: boolean;
  saylar: {
    doktorantlar: number;
    sertifikatlar: number;
    mezuniyyetler: number;
    tecrube: number;
    layiheler: number;
    shura_uzvleri: number;
  };
  cem_elaqe: number;
}

@Injectable()
export class ElaqelerService {
  constructor(private readonly prisma: PrismaService) {}

  /** Əvvəlcə əməkdaşın mövcud olduğunu yoxlayır */
  private async movcudYoxla(id: number): Promise<{ tam_ad: string; aktiv: boolean }> {
    const e = await this.prisma.emekdaslar.findUnique({
      where: { id: BigInt(id) },
      select: { id: true, ad: true, soyad: true, ata_adi: true, aktiv: true },
    });
    if (!e) throw new NotFoundException(`ID ${id} olan əməkdaş tapılmadı`);
    return { tam_ad: `${e.soyad} ${e.ad} ${e.ata_adi}`, aktiv: e.aktiv };
  }

  // ── 1. Yalnız SAYLAR — BİR sorğu ─────────────────────────────────
  /**
   * ⚠️ Bu, dərsin ən faydalı hiyləsidir.
   *
   * Əlaqələri `include` ilə götürsəydik, Prisma HƏR əlaqə üçün ayrı
   * SQL sorğusu göndərir (ölçdük: 1 sətir + 7 əlaqə = 8 sorğu).
   * Bizə isə yalnız SAY lazımdır — məlumatın özü yox.
   *
   * `_count` ilə Prisma bunu BİR sorğuda edir: SQL-də hər əlaqə
   * `(SELECT count(*) ...)` kimi alt sorğuya çevrilir.
   */
  async icmal(id: number): Promise<ElaqeIcmali> {
    const e = await this.prisma.emekdaslar.findUnique({
      where: { id: BigInt(id) },
      select: {
        id: true, ad: true, soyad: true, ata_adi: true, aktiv: true,
        _count: {
          select: {
            doktorantlar: true,
            sertifikasiya: true,
            mezuniyyetler: true,
            is_tecrubesi: true,
            tedqiqat_layiheleri: true,
            elmi_shura_uzvleri: true,
          },
        },
      },
    });

    if (!e) throw new NotFoundException(`ID ${id} olan əməkdaş tapılmadı`);

    const s = e._count;
    return {
      emekdas_id: String(e.id),
      tam_ad: `${e.soyad} ${e.ad} ${e.ata_adi}`,
      aktiv: e.aktiv,
      saylar: {
        doktorantlar: s.doktorantlar,
        sertifikatlar: s.sertifikasiya,
        mezuniyyetler: s.mezuniyyetler,
        tecrube: s.is_tecrubesi,
        layiheler: s.tedqiqat_layiheleri,
        shura_uzvleri: s.elmi_shura_uzvleri,
      },
      cem_elaqe:
        s.doktorantlar + s.sertifikasiya + s.mezuniyyetler +
        s.is_tecrubesi + s.tedqiqat_layiheleri + s.elmi_shura_uzvleri,
    };
  }

  // ── 2. Doktorantlar ──────────────────────────────────────────────
  async doktorantlar(id: number): Promise<DoktorantCavabi[]> {
    await this.movcudYoxla(id);
    return this.doktorantlarXam(id);
  }

  /** Eyni sorğu, AMMA mövcudluq yoxlaması OLMADAN.
   *  `hamisi()` bunu işlədir: əks halda altı əlaqə üçün altı dəfə
   *  eyni yoxlama təkrarlanar və altı LAZIMSIZ sorğu gedərdi. */
  private async doktorantlarXam(id: number): Promise<DoktorantCavabi[]> {

    const setirler = await this.prisma.doktorantlar.findMany({
      where: { rehber_id: BigInt(id) },
      select: {
        id: true, ad: true, soyad: true, ata_adi: true, status: true,
        qebul_tarixi: true, mudafie_tarixi: true, qeyd: true,
        doktorantura_proqramlari: { select: { ad: true } },
      },
      orderBy: { qebul_tarixi: 'desc' },
    });

    return setirler.map((d) => ({
      id: d.id,
      ad_soyad: `${d.soyad} ${d.ad} ${d.ata_adi}`,
      status: d.status,
      proqram: d.doktorantura_proqramlari?.ad ?? null,
      qebul_tarixi: tarix(d.qebul_tarixi),
      mudafie_tarixi: tarix(d.mudafie_tarixi),
      qeyd: d.qeyd,
    }));
  }

  // ── 3. Sertifikatlar ─────────────────────────────────────────────
  async sertifikatlar(id: number): Promise<SertifikatCavabi[]> {
    await this.movcudYoxla(id);
    return this.sertifikatlarXam(id);
  }

  /** Eyni sorğu, AMMA mövcudluq yoxlaması OLMADAN.
   *  `hamisi()` bunu işlədir: əks halda altı əlaqə üçün altı dəfə
   *  eyni yoxlama təkrarlanar və altı LAZIMSIZ sorğu gedərdi. */
  private async sertifikatlarXam(id: number): Promise<SertifikatCavabi[]> {

    const setirler = await this.prisma.sertifikasiya.findMany({
      where: { emekdas_id: BigInt(id) },
      select: {
        id: true, ad_soyad: true, tip: true, imtahan_tarixi: true,
        bal: true, netice: true, sertifikat_no: true,
      },
      orderBy: { imtahan_tarixi: 'desc' },
    });

    return setirler.map((s) => ({
      id: s.id,
      ad_soyad: s.ad_soyad,
      tip: s.tip,
      imtahan_tarixi: tarix(s.imtahan_tarixi),
      bal: pul(s.bal),
      netice: s.netice,
      sertifikat_no: s.sertifikat_no,
    }));
  }

  // ── 4. Məzuniyyətlər ─────────────────────────────────────────────
  async mezuniyyetler(id: number): Promise<MezuniyyetCavabi[]> {
    await this.movcudYoxla(id);
    return this.mezuniyyetlerXam(id);
  }

  /** Eyni sorğu, AMMA mövcudluq yoxlaması OLMADAN.
   *  `hamisi()` bunu işlədir: əks halda altı əlaqə üçün altı dəfə
   *  eyni yoxlama təkrarlanar və altı LAZIMSIZ sorğu gedərdi. */
  private async mezuniyyetlerXam(id: number): Promise<MezuniyyetCavabi[]> {

    const setirler = await this.prisma.mezuniyyetler.findMany({
      where: { emekdas_id: BigInt(id) },
      select: {
        id: true, mezuniyyet_tipi: true, baslama_tarixi: true,
        bitme_tarixi: true, gun_sayi: true, status: true,
      },
      orderBy: { baslama_tarixi: 'desc' },
    });

    return setirler.map((m) => ({
      id: m.id,
      mezuniyyet_tipi: m.mezuniyyet_tipi,
      baslama_tarixi: tarix(m.baslama_tarixi)!,
      bitme_tarixi: tarix(m.bitme_tarixi)!,
      gun_sayi: m.gun_sayi,
      status: m.status,
    }));
  }

  // ── 5. İş təcrübəsi ──────────────────────────────────────────────
  async tecrube(id: number): Promise<TecrubeCavabi[]> {
    await this.movcudYoxla(id);
    return this.tecrubeXam(id);
  }

  /** Eyni sorğu, AMMA mövcudluq yoxlaması OLMADAN.
   *  `hamisi()` bunu işlədir: əks halda altı əlaqə üçün altı dəfə
   *  eyni yoxlama təkrarlanar və altı LAZIMSIZ sorğu gedərdi. */
  private async tecrubeXam(id: number): Promise<TecrubeCavabi[]> {

    const setirler = await this.prisma.is_tecrubesi.findMany({
      where: { emekdas_id: BigInt(id) },
      select: {
        id: true, is_yeri: true, vezife: true,
        baslama_tarixi: true, bitme_tarixi: true,
      },
      orderBy: { baslama_tarixi: 'desc' },
    });

    return setirler.map((t) => ({
      id: t.id,
      is_yeri: t.is_yeri,
      vezife: t.vezife,
      baslama_tarixi: tarix(t.baslama_tarixi),
      bitme_tarixi: tarix(t.bitme_tarixi),
    }));
  }

  // ── 6. Tədqiqat layihələri ───────────────────────────────────────
  async layiheler(id: number): Promise<LayiheCavabi[]> {
    await this.movcudYoxla(id);
    return this.layihelerXam(id);
  }

  /** Eyni sorğu, AMMA mövcudluq yoxlaması OLMADAN.
   *  `hamisi()` bunu işlədir: əks halda altı əlaqə üçün altı dəfə
   *  eyni yoxlama təkrarlanar və altı LAZIMSIZ sorğu gedərdi. */
  private async layihelerXam(id: number): Promise<LayiheCavabi[]> {

    const setirler = await this.prisma.tedqiqat_layiheleri.findMany({
      where: { rehber_id: BigInt(id) },
      select: {
        id: true, ad: true, status: true, baslama_tarixi: true,
        bitme_tarixi: true,
        tedqiqat_istiqametleri: { select: { ad: true } },
      },
      orderBy: { baslama_tarixi: 'desc' },
    });

    return setirler.map((l) => ({
      id: l.id,
      ad: l.ad,
      status: l.status,
      istiqamet: l.tedqiqat_istiqametleri?.ad ?? null,
      baslama_tarixi: tarix(l.baslama_tarixi),
      bitme_tarixi: tarix(l.bitme_tarixi),
    }));
  }

  // ── 7. Elmi şura üzvlüyü ─────────────────────────────────────────
  async shura(id: number): Promise<ShuraCavabi[]> {
    await this.movcudYoxla(id);
    return this.shuraXam(id);
  }

  /** Eyni sorğu, AMMA mövcudluq yoxlaması OLMADAN.
   *  `hamisi()` bunu işlədir: əks halda altı əlaqə üçün altı dəfə
   *  eyni yoxlama təkrarlanar və altı LAZIMSIZ sorğu gedərdi. */
  private async shuraXam(id: number): Promise<ShuraCavabi[]> {

    const setirler = await this.prisma.elmi_shura_uzvleri.findMany({
      where: { emekdas_id: BigInt(id) },
      select: {
        id: true, ad_soyad: true, status: true, qosulma_tarixi: true,
        aktiv: true,
        vezifeler: { select: { ad: true } },
        elmi_dereceler: { select: { ad: true } },
        elmi_adlar: { select: { ad: true } },
      },
      orderBy: { qosulma_tarixi: 'desc' },
    });

    return setirler.map((s) => ({
      id: s.id,
      ad_soyad: s.ad_soyad,
      vezife: s.vezifeler?.ad ?? null,
      elmi_derece: s.elmi_dereceler?.ad ?? null,
      elmi_ad: s.elmi_adlar?.ad ?? null,
      status: s.status,
      qosulma_tarixi: tarix(s.qosulma_tarixi),
      aktiv: s.aktiv,
    }));
  }

  // ── 8. Hamısı PARALEL ────────────────────────────────────────────
  /**
   * Altı əlaqə bir-birindən ASILI DEYİL — hamısı eyni `id`-dən asılıdır.
   * Ona görə `await`-i ardıcıl yazmaq yerinə `Promise.all` işlədirik:
   * altı sorğu EYNİ ANDA gedir və ümumi vaxt ən yavaşının vaxtına
   * bərabər olur (cəminə yox).
   */
  async hamisi(id: number): Promise<{
    emekdas_id: string;
    tam_ad: string;
    doktorantlar: DoktorantCavabi[];
    sertifikatlar: SertifikatCavabi[];
    mezuniyyetler: MezuniyyetCavabi[];
    tecrube: TecrubeCavabi[];
    layiheler: LayiheCavabi[];
    shura_uzvleri: ShuraCavabi[];
    cekme_ms: number;
  }> {
    const baslama = Date.now();
    const e = await this.movcudYoxla(id);

    const [doktorantlar, sertifikatlar, mezuniyyetler, tecrube, layiheler, shura_uzvleri] =
      await Promise.all([
        this.doktorantlarXam(id),
        this.sertifikatlarXam(id),
        this.mezuniyyetlerXam(id),
        this.tecrubeXam(id),
        this.layihelerXam(id),
        this.shuraXam(id),
      ]);

    return {
      emekdas_id: String(id),
      tam_ad: e.tam_ad,
      doktorantlar,
      sertifikatlar,
      mezuniyyetler,
      tecrube,
      layiheler,
      shura_uzvleri,
      cekme_ms: Date.now() - baslama,
    };
  }

  // ── 9. Hamısı BİR `findUnique` ilə ──────────────────────────────
  /**
   * Eyni nəticə, AMMA fərqli üsul: altı əlaqəni bir `findUnique`
   * sorğusunun içində istəyirik.
   *
   * ⚠️ MÜHÜM MÜŞAHİDƏ: Prisma-nın standart strategiyası
   * (`relationLoadStrategy: 'query'`) hər əlaqə üçün AYRI SQL sorğusu
   * göndərir. Ona görə sorğu sayı EYNİ qalır: 1 + 6 = 7.
   *
   * Yəni bu üsul sorğu sayını azaltmır — sadəcə kodu qısaldır.
   * Sorğu sayını HƏQİQƏTƏN azaltmağın yolu `icmal()`-dır: yalnız
   * SAY lazımdırsa `_count` BİR sorğu göndərir.
   */
  async birSorquda(id: number): Promise<{
    emekdas_id: string;
    tam_ad: string;
    doktorantlar: DoktorantCavabi[];
    sertifikatlar: SertifikatCavabi[];
    mezuniyyetler: MezuniyyetCavabi[];
    tecrube: TecrubeCavabi[];
    layiheler: LayiheCavabi[];
    shura_uzvleri: ShuraCavabi[];
  }> {
    const e = await this.prisma.emekdaslar.findUnique({
      where: { id: BigInt(id) },
      select: {
        id: true, ad: true, soyad: true, ata_adi: true,
        doktorantlar: {
          select: {
            id: true, ad: true, soyad: true, ata_adi: true, status: true,
            qebul_tarixi: true, mudafie_tarixi: true, qeyd: true,
            doktorantura_proqramlari: { select: { ad: true } },
          },
          orderBy: { qebul_tarixi: 'desc' },
        },
        sertifikasiya: {
          select: {
            id: true, ad_soyad: true, tip: true, imtahan_tarixi: true,
            bal: true, netice: true, sertifikat_no: true,
          },
          orderBy: { imtahan_tarixi: 'desc' },
        },
        mezuniyyetler: {
          select: {
            id: true, mezuniyyet_tipi: true, baslama_tarixi: true,
            bitme_tarixi: true, gun_sayi: true, status: true,
          },
          orderBy: { baslama_tarixi: 'desc' },
        },
        is_tecrubesi: {
          select: {
            id: true, is_yeri: true, vezife: true,
            baslama_tarixi: true, bitme_tarixi: true,
          },
          orderBy: { baslama_tarixi: 'desc' },
        },
        tedqiqat_layiheleri: {
          select: {
            id: true, ad: true, status: true, baslama_tarixi: true,
            bitme_tarixi: true,
            tedqiqat_istiqametleri: { select: { ad: true } },
          },
          orderBy: { baslama_tarixi: 'desc' },
        },
        elmi_shura_uzvleri: {
          select: {
            id: true, ad_soyad: true, status: true, qosulma_tarixi: true,
            aktiv: true,
            vezifeler: { select: { ad: true } },
            elmi_dereceler: { select: { ad: true } },
            elmi_adlar: { select: { ad: true } },
          },
          orderBy: { qosulma_tarixi: 'desc' },
        },
      },
    });

    if (!e) throw new NotFoundException(`ID ${id} olan əməkdaş tapılmadı`);

    return {
      emekdas_id: String(e.id),
      tam_ad: `${e.soyad} ${e.ad} ${e.ata_adi}`,
      doktorantlar: e.doktorantlar.map((d) => ({
        id: d.id,
        ad_soyad: `${d.soyad} ${d.ad} ${d.ata_adi}`,
        status: d.status,
        proqram: d.doktorantura_proqramlari?.ad ?? null,
        qebul_tarixi: tarix(d.qebul_tarixi),
        mudafie_tarixi: tarix(d.mudafie_tarixi),
        qeyd: d.qeyd,
      })),
      sertifikatlar: e.sertifikasiya.map((x) => ({
        id: x.id,
        ad_soyad: x.ad_soyad,
        tip: x.tip,
        imtahan_tarixi: tarix(x.imtahan_tarixi),
        bal: pul(x.bal),
        netice: x.netice,
        sertifikat_no: x.sertifikat_no,
      })),
      mezuniyyetler: e.mezuniyyetler.map((m) => ({
        id: m.id,
        mezuniyyet_tipi: m.mezuniyyet_tipi,
        baslama_tarixi: tarix(m.baslama_tarixi)!,
        bitme_tarixi: tarix(m.bitme_tarixi)!,
        gun_sayi: m.gun_sayi,
        status: m.status,
      })),
      tecrube: e.is_tecrubesi.map((t) => ({
        id: t.id,
        is_yeri: t.is_yeri,
        vezife: t.vezife,
        baslama_tarixi: tarix(t.baslama_tarixi),
        bitme_tarixi: tarix(t.bitme_tarixi),
      })),
      layiheler: e.tedqiqat_layiheleri.map((l) => ({
        id: l.id,
        ad: l.ad,
        status: l.status,
        istiqamet: l.tedqiqat_istiqametleri?.ad ?? null,
        baslama_tarixi: tarix(l.baslama_tarixi),
        bitme_tarixi: tarix(l.bitme_tarixi),
      })),
      shura_uzvleri: e.elmi_shura_uzvleri.map((x) => ({
        id: x.id,
        ad_soyad: x.ad_soyad,
        vezife: x.vezifeler?.ad ?? null,
        elmi_derece: x.elmi_dereceler?.ad ?? null,
        elmi_ad: x.elmi_adlar?.ad ?? null,
        status: x.status,
        qosulma_tarixi: tarix(x.qosulma_tarixi),
        aktiv: x.aktiv,
      })),
    };
  }

  // ── 10. Baza funksiyası ilə tam ad ───────────────────────────────
  /**
   * Bazada ARTIQ YAZILMIŞ `kadrlar.fn_emekdas_tam_adi(bigint)` funksiyasını
   * çağırır. Niyə? Çünki həmin məntiq artıq SQL-də var və BAŞQA
   * hesabatlarda da işlədilir. Eyni məntiqi iki yerdə yazmaq
   * (bir dəfə SQL-də, bir dəfə TypeScript-də) uyğunsuzluğa səbəb olar.
   */
  async bazaTamAd(id: number): Promise<{ emekdas_id: number; tam_ad: string }> {
    await this.movcudYoxla(id);

    const netice = await this.prisma.$queryRaw<{ tam_ad: string }[]>`
      SELECT kadrlar.fn_emekdas_tam_adi(${BigInt(id)}::bigint) AS tam_ad`;

    return { emekdas_id: id, tam_ad: netice[0]?.tam_ad ?? 'Tapılmadı' };
  }
}
