import type { Prisma } from '../../generated/prisma/client.js';

/**
 * Bazadan oxunacaq sütunlar — BİR dəfə yazılır, hər yerdə istifadə olunur.
 *
 * `as const` sayəsində TypeScript bu obyektin dəqiq strukturunu yadda
 * saxlayır və `EmekdasSetiri` tipini ondan çıxara bilirik.
 *
 * `include` yerinə `select` işlədirik: `include` BÜTÜN sütunları gətirir
 * (o cümlədən lazımsızları), `select` isə yalnız istədiklərimizi.
 * 14 sətirlik cədvəldə fərq görünməz, 100 000 sətirdə isə həlledicidir.
 */
export const EMEKDAS_SECIM = {
  id: true,
  ad: true,
  soyad: true,
  ata_adi: true,
  dogum_tarixi: true,
  email: true,
  telefon: true,
  ise_baslama: true,
  maas: true,
  aktiv: true,
  yaradilma: true,
  cinsiyyet: { select: { id: true, ad: true } },
  vezifeler: { select: { id: true, ad: true } },
  shobeler: { select: { id: true, ad: true } },
  merkezler: { select: { id: true, ad: true } },
  is_statuslari: { select: { id: true, ad: true } },
  elmi_dereceler: { select: { id: true, ad: true } },
  elmi_adlar: { select: { id: true, ad: true } },
} as const;

/** Bazadan gələn XAM sətrin tipi — `EMEKDAS_SECIM`-dən avtomatik çıxarılır. */
export type EmekdasSetiri = Prisma.emekdaslarGetPayload<{ select: typeof EMEKDAS_SECIM }>;

/** API-dən çıxan cavabın tipi — bazadakı sütunlarla ÜST-ÜSTƏ DÜŞMÜR. */
export interface EmekdasCavabi {
  id: string;
  ad: string;
  soyad: string;
  ata_adi: string;
  tam_ad: string;
  cinsiyyet: { id: number; ad: string } | null;
  dogum_tarixi: string | null;
  yas: number | null;
  vezife: { id: number; ad: string } | null;
  shobe: { id: number; ad: string } | null;
  merkez: { id: number; ad: string } | null;
  email: string | null;
  telefon: string | null;
  is_statusu: { id: number; ad: string } | null;
  elmi_derece: { id: number; ad: string } | null;
  elmi_ad: { id: number; ad: string } | null;
  ise_baslama: string | null;
  maas: string | null;
  aktiv: boolean;
  yaradilma: string;
}

/** `YYYY-MM-DD` — tarixi saat olmadan göstərir */
function tarix(d: Date | null): string | null {
  return d ? d.toISOString().slice(0, 10) : null;
}

/** Doğum tarixindən yaşı hesablayır (tam ədəd, illə) */
function yasHesabla(d: Date | null): number | null {
  if (!d) return null;
  const indi = new Date();
  let yas = indi.getUTCFullYear() - d.getUTCFullYear();
  const ayFerqi = indi.getUTCMonth() - d.getUTCMonth();
  if (ayFerqi < 0 || (ayFerqi === 0 && indi.getUTCDate() < d.getUTCDate())) {
    yas -= 1;
  }
  return yas;
}

/**
 * XAM baza sətrini API cavabına çevirir — «mapper».
 *
 * ⚠️ BURADA ÜÇ VACİB ÇEVİRMƏ VAR:
 *
 *  1) `id`  — bazada BigInt-dir (`1n`), API-də isə MƏTN (`"1"`).
 *     Səbəb: `JSON.stringify(1n)` xəta verir — «Do not know how to
 *     serialize a BigInt». Üstəlik JavaScript ədədi 2^53-dən sonra
 *     dəqiqliyi itirir, BigInt isə itirmir. Ona görə MƏTN göndəririk.
 *
 *  2) `maas` — Prisma `Decimal` obyektidir. `String(decimal)` düzgün
 *     mətn verir, `Number(decimal)` isə böyük dəyərlərdə dəqiqliyi
 *     itirə bilər. Pul üçün həmişə MƏTN göndərilir.
 *
 *  3) `dogum_tarixi` / `ise_baslama` — `@db.Date` sütunudur. `toISOString()`
 *     tam vaxt verir (`1985-03-12T00:00:00.000Z`), bizə isə yalnız gün
 *     lazımdır. Ona görə ilk 10 simvolu götürürük.
 */
export function hazirla(e: EmekdasSetiri): EmekdasCavabi {
  return {
    id: String(e.id),
    ad: e.ad,
    soyad: e.soyad,
    ata_adi: e.ata_adi,
    tam_ad: `${e.soyad} ${e.ad} ${e.ata_adi}`,
    cinsiyyet: e.cinsiyyet ? { id: e.cinsiyyet.id, ad: e.cinsiyyet.ad } : null,
    dogum_tarixi: tarix(e.dogum_tarixi),
    yas: yasHesabla(e.dogum_tarixi),
    vezife: e.vezifeler ? { id: e.vezifeler.id, ad: e.vezifeler.ad } : null,
    shobe: e.shobeler ? { id: e.shobeler.id, ad: e.shobeler.ad } : null,
    merkez: e.merkezler ? { id: e.merkezler.id, ad: e.merkezler.ad } : null,
    email: e.email,
    telefon: e.telefon,
    is_statusu: e.is_statuslari
      ? { id: e.is_statuslari.id, ad: e.is_statuslari.ad }
      : null,
    elmi_derece: e.elmi_dereceler
      ? { id: e.elmi_dereceler.id, ad: e.elmi_dereceler.ad }
      : null,
    elmi_ad: e.elmi_adlar ? { id: e.elmi_adlar.id, ad: e.elmi_adlar.ad } : null,
    ise_baslama: tarix(e.ise_baslama),
    maas: e.maas === null ? null : e.maas.toFixed(2),
    aktiv: e.aktiv,
    yaradilma: e.yaradilma.toISOString(),
  };
}
