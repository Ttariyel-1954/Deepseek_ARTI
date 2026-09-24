import { Injectable, Logger, NotFoundException } from '@nestjs/common';
import { Prisma } from '../generated/prisma/client.js';
import { PrismaService } from '../prisma/prisma.service.js';
import { AuditSorguDto, AuditYazDto } from './dto/audit-sorgu.dto.js';

export interface AuditCavabi {
  id: string;
  cedvel_adi: string;
  emeliyyat: string;
  setir_id: string | null;
  istifadeci: string | null;
  vaxt: string;
  qeyd: string | null;
}

export interface AuditSehife {
  ugur: true;
  sehife: number;
  limit: number;
  cem: number;
  sehife_sayi: number;
  melumat: AuditCavabi[];
}

export interface AuditStatistikasi {
  cem_qeyd: number;
  cedvel_sayi: number;
  ilk_qeyd: string | null;
  son_qeyd: string | null;
  cedvel_uzre: { cedvel_adi: string; cem: number; insert: number; update: number; delete: number }[];
  emeliyyat_uzre: { emeliyyat: string; cem: number }[];
}

/** Xam sətri API cavabına çevirir */
function hazirla(e: {
  id: bigint;
  cedvel_adi: string;
  emeliyyat: string;
  setir_id: string | null;
  istifadeci: string | null;
  vaxt: Date;
  qeyd: string | null;
}): AuditCavabi {
  return {
    // ⚠️ `id` BigInt-dir — mətnə çevirməsək JSON cavabı 500 verər
    id: String(e.id),
    cedvel_adi: e.cedvel_adi,
    emeliyyat: e.emeliyyat,
    // `setir_id` bazada MƏTN sütunudur (bigint yox).
    // Səbəb: loq MÜXTƏLİF cədvəllərdən gəlir — bəzilərinin açarı
    // `int`, bəzilərinin `bigint`, bəzilərinin `uuid`-dir. Hamısını
    // bir sütunda saxlamaq üçün ən ümumi tip mətndir.
    setir_id: e.setir_id,
    istifadeci: e.istifadeci,
    vaxt: e.vaxt.toISOString(),
    qeyd: e.qeyd,
  };
}

@Injectable()
export class AuditService {
  private readonly log = new Logger('AUDIT');

  constructor(private readonly prisma: PrismaService) {}

  // ── 1. Oxuma — səhifələnmiş ─────────────────────────────────────
  async hamisi(sorgu: AuditSorguDto): Promise<AuditSehife> {
    const where: Prisma.audit_logWhereInput = {};

    if (sorgu.cedvel) where.cedvel_adi = { contains: sorgu.cedvel, mode: 'insensitive' };
    if (sorgu.emeliyyat) where.emeliyyat = sorgu.emeliyyat;
    if (sorgu.axtar) {
      where.OR = [
        { qeyd: { contains: sorgu.axtar, mode: 'insensitive' } },
        { setir_id: { contains: sorgu.axtar, mode: 'insensitive' } },
        { istifadeci: { contains: sorgu.axtar, mode: 'insensitive' } },
      ];
    }

    const [cem, setirler] = await this.prisma.$transaction([
      this.prisma.audit_log.count({ where }),
      this.prisma.audit_log.findMany({
        where,
        orderBy: { id: 'desc' },
        skip: (sorgu.seife - 1) * sorgu.limit,
        take: sorgu.limit,
      }),
    ]);

    return {
      ugur: true,
      sehife: sorgu.seife,
      limit: sorgu.limit,
      cem,
      sehife_sayi: Math.ceil(cem / sorgu.limit),
      melumat: setirler.map(hazirla),
    };
  }

  // ── 2. Bir qeyd ─────────────────────────────────────────────────
  async biri(id: number): Promise<AuditCavabi> {
    const setir = await this.prisma.audit_log.findUnique({
      where: { id: BigInt(id) },
    });
    if (!setir) throw new NotFoundException(`ID ${id} olan audit qeydi tapılmadı`);
    return hazirla(setir);
  }

  // ── 3. Statistika ───────────────────────────────────────────────
  async statistika(): Promise<AuditStatistikasi> {
    const [cem, cedvelUzre, emeliyyatUzre, ilk, son] = await this.prisma.$transaction([
      this.prisma.audit_log.count(),
      this.prisma.audit_log.groupBy({
        by: ['cedvel_adi', 'emeliyyat'],
        _count: { _all: true },
      }),
      this.prisma.audit_log.groupBy({ by: ['emeliyyat'], _count: { _all: true } }),
      this.prisma.audit_log.findFirst({ orderBy: { id: 'asc' }, select: { vaxt: true } }),
      this.prisma.audit_log.findFirst({ orderBy: { id: 'desc' }, select: { vaxt: true } }),
    ]);

    // groupBy iki sütun üzrə gəldiyi üçün nəticəni cədvəl üzrə yığırıq
    const xerite = new Map<
      string,
      { cedvel_adi: string; cem: number; insert: number; update: number; delete: number }
    >();

    for (const q of cedvelUzre) {
      const m = xerite.get(q.cedvel_adi) ??
        { cedvel_adi: q.cedvel_adi, cem: 0, insert: 0, update: 0, delete: 0 };
      const say = q._count._all;
      m.cem += say;
      if (q.emeliyyat === 'INSERT') m.insert += say;
      else if (q.emeliyyat === 'UPDATE') m.update += say;
      else if (q.emeliyyat === 'DELETE') m.delete += say;
      xerite.set(q.cedvel_adi, m);
    }

    const cedvelList = [...xerite.values()].sort((a, b) => b.cem - a.cem);

    return {
      cem_qeyd: cem,
      cedvel_sayi: cedvelList.length,
      ilk_qeyd: ilk?.vaxt.toISOString() ?? null,
      son_qeyd: son?.vaxt.toISOString() ?? null,
      cedvel_uzre: cedvelList.slice(0, 15),
      emeliyyat_uzre: emeliyyatUzre
        .map((q) => ({ emeliyyat: q.emeliyyat, cem: q._count._all }))
        .sort((a, b) => b.cem - a.cem),
    };
  }

  // ── 4. Tətbiq səviyyəsində loq yazmaq ───────────────────────────
  /**
   * ⚠️ NİYƏ BAZA TRIGGER-İ KİFAYƏT ETMİR?
   *
   * `audit.fn_audit_yaz()` trigger-i yalnız DÖRD cədvəli izləyir
   * (`kadrlar.emekdaslar`, `elm.tedqiqat_layiheleri`, `maliyye.budce`,
   * `maliyye.satinalmalar`) və yalnız bunları yazır:
   *   cedvel_adi, emeliyyat, setir_id, istifadeci, vaxt
   *
   * Trigger BİLMİR:
   *   • hansı istifadəçi (IP, sessiya, rol)
   *   • NƏYİ dəyişdirdi (köhnə → yeni dəyər)
   *   • NİYƏ (əmrin nömrəsi, səbəb)
   *
   * Bunları TƏTBİQ səviyyəsində əlavə edirik — və MÜTLƏQ həmin
   * tranzaksiyanın İÇİNDƏ, ki dəyişiklik geri qaytarılarsa, loq da
   * qaytarılsın.
   */
  async yaz(
    klient: Prisma.TransactionClient,
    melumat: AuditYazDto,
  ): Promise<{ id: string }> {
    const setir = await klient.audit_log.create({
      data: {
        cedvel_adi: melumat.cedvel_adi,
        emeliyyat: melumat.emeliyyat,
        setir_id: melumat.setir_id ?? null,
        qeyd: melumat.qeyd ?? null,
        istifadeci: melumat.istifadeci ?? null,
      },
      select: { id: true },
    });
    return { id: String(setir.id) };
  }

  /** Tranzaksiyasız yazma — yalnız loq üçün */
  async yazTek(melumat: AuditYazDto): Promise<{ id: string }> {
    return this.prisma.$transaction((tx) => this.yaz(tx, melumat));
  }

  // ── 5. NÜMAYİŞ: əməkdaş + audit BİR tranzaksiyada ───────────────
  /**
   * Yeni əməkdaş yaradır VƏ həmin əməliyyatı audit loquna yazır —
   * HƏR İKİSİ bir tranzaksiyada. Sonda QƏSDƏN xəta atır ki,
   * rollback-i görək: nə əməkdaş, nə də loq qalmalıdır.
   */
  async tranzaksiyaNumayisi(): Promise<{
    ugur: true;
    yazilan_audit_id: string | null;
    bazada_qalan_emekdas: number;
    bazada_qalan_audit: number;
    xeta: string;
    izah: string;
  }> {
    const ep = `audit.demo.${Date.now()}@arti.edu.az`;
    let auditId: string | null = null;
    let xetaMetni = '';

    const auditEvvel = await this.prisma.audit_log.count();

    try {
      await this.prisma.$transaction(async (tx) => {
        const e = await tx.emekdaslar.create({
          data: {
            ad: 'Audit', soyad: 'Numayis', ata_adi: 'Sistem',
            cinsiyyet_id: 1, vezife_id: 6, email: ep,
          },
          select: { id: true },
        });

        const a = await this.yaz(tx, {
          cedvel_adi: 'kadrlar.emekdaslar',
          emeliyyat: 'INSERT',
          setir_id: String(e.id),
          istifadeci: 'api@arti.edu.az',
          qeyd: 'Nümayiş: əməkdaş yaradıldı (tranzaksiya sınağı)',
        });
        auditId = a.id;

        throw new Error('QƏSDƏN XƏTA: hər ikisi geri qaytarılmalıdır');
      });
      xetaMetni = '(gözlənilməz: xəta atılmadı)';
    } catch (x) {
      xetaMetni = (x as Error).message;
    }

    const qalanEmekdas = await this.prisma.emekdaslar.count({
      where: { email: ep },
    });
    const auditSonra = await this.prisma.audit_log.count();

    this.log.log(
      `Tranzaksiya nümayişi: əməkdaş=${qalanEmekdas}, audit artımı=${auditSonra - auditEvvel}`,
    );

    return {
      ugur: true,
      yazilan_audit_id: auditId,
      bazada_qalan_emekdas: qalanEmekdas,
      bazada_qalan_audit: auditSonra - auditEvvel,
      xeta: xetaMetni,
      izah:
        qalanEmekdas === 0 && auditSonra === auditEvvel
          ? 'ROLLBACK: nə əməkdaş, nə audit qeydi qaldı — ikisi ATOMİKDİR'
          : 'XƏTA: tranzaksiya tam geri qaytarılmadı!',
    };
  }

  // ── 6. Trigger-in işlədiyini SÜBUT ET ───────────────────────────
  /**
   * Müvəqqəti əməkdaş yaradır, dəyişir və silir. Hər üç əməliyyat
   * baza TRIGGER-İ tərəfindən audit loquna yazılır.
   *
   * ⚠️ Bu qeydlər SONRADAN SİLİNMİR — audit loqu əbədidir. Bu, qəsdən
   * belədir: loq silinə bilsəydi, izləmə mənasını itirərdi.
   */
  async triggerNumayisi(): Promise<{
    ugur: true;
    yeni_id: string;
    audit_artimi: number;
    qeydler: AuditCavabi[];
    izah: string;
  }> {
    const ep = `audit.trigger.${Date.now()}@arti.edu.az`;
    const evvel = await this.prisma.audit_log.count();

    const e = await this.prisma.emekdaslar.create({
      data: {
        ad: 'Trigger', soyad: 'Numayis', ata_adi: 'Sistem',
        cinsiyyet_id: 1, vezife_id: 6, email: ep, maas: 1000,
      },
      select: { id: true },
    });

    await this.prisma.emekdaslar.update({
      where: { id: e.id },
      data: { maas: 2000 },
    });

    await this.prisma.emekdaslar.delete({ where: { id: e.id } });

    const sonra = await this.prisma.audit_log.count();

    const qeydler = await this.prisma.audit_log.findMany({
      where: { cedvel_adi: 'kadrlar.emekdaslar', setir_id: String(e.id) },
      orderBy: { id: 'asc' },
    });

    return {
      ugur: true,
      yeni_id: String(e.id),
      audit_artimi: sonra - evvel,
      qeydler: qeydler.map(hazirla),
      izah:
        sonra - evvel === 3
          ? 'Trigger hər üç əməliyyatı (INSERT/UPDATE/DELETE) avtomatik yazdı'
          : `Gözlənilirdi 3 qeyd, alındı ${sonra - evvel}`,
    };
  }
}
