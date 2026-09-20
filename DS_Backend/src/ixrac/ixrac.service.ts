import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

/*
 * exceljs CommonJS moduludur.
 *
 * ESM-den:
 *   import * as ExcelJS from 'exceljs'   ->  ExcelJS.Workbook === undefined
 *   import ExcelJS from 'exceljs'        ->  ExcelJS.Workbook === function  ✅
 *
 * Sebeb: Node CJS modulunun butun module.exports-unu DEFAULT export kimi verir.
 */
import ExcelJS from 'exceljs';

export interface CedvelMelumati {
  basliq: string;
  sutunlar: { acar: string; ad: string; en?: number }[];
  setirler: Record<string, unknown>[];
}

@Injectable()
export class IxracService {
  private readonly log = new Logger('IXRAC');

  constructor(private readonly prisma: PrismaService) {}

  /** Excel fayli yaradir (Buffer) */
  async excel(cedvel: CedvelMelumati): Promise<Buffer> {
    const wb = new ExcelJS.Workbook();
    wb.creator = 'Deepseek ARTI';
    wb.created = new Date();

    const ws = wb.addWorksheet('Məlumat', {
      views: [{ state: 'frozen', ySplit: 3 }],
    });

    // 1) Basliq setri (birleshdirilmish)
    ws.mergeCells(1, 1, 1, cedvel.sutunlar.length);
    const basliqHucresi = ws.getCell(1, 1);
    basliqHucresi.value = cedvel.basliq;
    basliqHucresi.font = { bold: true, size: 14, color: { argb: 'FF1E3A5F' } };
    basliqHucresi.alignment = { horizontal: 'center', vertical: 'middle' };
    ws.getRow(1).height = 26;

    // 2) Tarix setri
    ws.mergeCells(2, 1, 2, cedvel.sutunlar.length);
    const tarixHucresi = ws.getCell(2, 1);
    tarixHucresi.value = `Yaradıldı: ${new Date().toLocaleString('az-AZ')}`;
    tarixHucresi.font = { italic: true, size: 9, color: { argb: 'FF808080' } };
    tarixHucresi.alignment = { horizontal: 'right' };

    // 3) Sutun basliqlari
    const basliqSetri = ws.getRow(3);
    cedvel.sutunlar.forEach((s, i) => {
      const h = basliqSetri.getCell(i + 1);
      h.value = s.ad;
      h.font = { bold: true, color: { argb: 'FFFFFFFF' } };
      h.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF2C5282' } };
      h.alignment = { horizontal: 'center', vertical: 'middle' };
      h.border = {
        top:    { style: 'thin', color: { argb: 'FF999999' } },
        left:   { style: 'thin', color: { argb: 'FF999999' } },
        bottom: { style: 'thin', color: { argb: 'FF999999' } },
        right:  { style: 'thin', color: { argb: 'FF999999' } },
      };
      ws.getColumn(i + 1).width = s.en ?? 22;
    });
    basliqSetri.height = 22;

    // 4) Melumat setirleri (zebra)
    cedvel.setirler.forEach((s, idx) => {
      const r = ws.addRow(cedvel.sutunlar.map((c) => s[c.acar] ?? ''));
      if (idx % 2 === 1) {
        r.eachCell((h) => {
          h.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF2F6FA' } };
        });
      }
      r.eachCell((h) => {
        h.border = {
          top:    { style: 'hair', color: { argb: 'FFDDDDDD' } },
          left:   { style: 'thin', color: { argb: 'FFDDDDDD' } },
          bottom: { style: 'hair', color: { argb: 'FFDDDDDD' } },
          right:  { style: 'thin', color: { argb: 'FFDDDDDD' } },
        };
      });
    });

    // 5) Avtofiltr
    if (cedvel.setirler.length) {
      ws.autoFilter = {
        from: { row: 3, column: 1 },
        to:   { row: 3, column: cedvel.sutunlar.length },
      };
    }

    const bufer = await wb.xlsx.writeBuffer();
    this.log.log(`Excel yaradildi: ${cedvel.setirler.length} setir`);
    return Buffer.from(bufer);
  }

  /** Emekdaslari Excel-e cixarir */
  async emekdaslarExcel(): Promise<Buffer> {
    const setirler = await this.prisma.$queryRaw<Record<string, unknown>[]>`
      SELECT e.id::int                                    AS id,
             e.soyad || ' ' || e.ad || ' ' || e.ata_adi   AS tam_adi,
             v.ad                                         AS vezife,
             s.ad                                         AS shobe,
             m.ad                                         AS merkez,
             COALESCE(e.email, '—')                       AS email,
             COALESCE(e.telefon, '—')                     AS telefon,
             e.ise_baslama::text                          AS ise_baslama,
             e.maas::float8                               AS maas
        FROM kadrlar.emekdaslar e
        LEFT JOIN struktur.vezifeler v ON v.id = e.vezife_id
        LEFT JOIN struktur.shobeler  s ON s.id = e.shobe_id
        LEFT JOIN struktur.merkezler m ON m.id = e.merkez_id
       WHERE e.aktiv = true
       ORDER BY e.soyad`;

    return this.excel({
      basliq: 'ARTİ — Aktiv Əməkdaşlar',
      sutunlar: [
        { acar: 'id',           ad: 'ID',          en: 6 },
        { acar: 'tam_adi',      ad: 'Ad, Soyad',   en: 28 },
        { acar: 'vezife',       ad: 'Vəzifə',      en: 20 },
        { acar: 'shobe',        ad: 'Şöbə',        en: 24 },
        { acar: 'merkez',       ad: 'Mərkəz',      en: 32 },
        { acar: 'email',        ad: 'E-poçt',      en: 26 },
        { acar: 'telefon',      ad: 'Telefon',     en: 18 },
        { acar: 'ise_baslama',  ad: 'İşə başlama', en: 13 },
        { acar: 'maas',         ad: 'Maaş',        en: 12 },
      ],
      setirler,
    });
  }

  /** Budceni Excel-e cixarir */
  async budceExcel(): Promise<Buffer> {
    const setirler = await this.prisma.$queryRaw<Record<string, unknown>[]>`
      SELECT il, menbe, mebleg::float8 AS mebleg,
             COALESCE(qeyd, '—') AS qeyd
        FROM maliyye.budce ORDER BY il DESC, mebleg DESC`;

    return this.excel({
      basliq: 'ARTİ — Büdcə',
      sutunlar: [
        { acar: 'il',     ad: 'İl',      en: 8 },
        { acar: 'menbe',  ad: 'Mənbə',   en: 14 },
        { acar: 'mebleg', ad: 'Məbləğ',  en: 16 },
        { acar: 'qeyd',   ad: 'Qeyd',    en: 34 },
      ],
      setirler,
    });
  }

  /** HTML hesabat (brauzerde PDF kimi çap olunur) */
  async htmlHesabat(): Promise<string> {
    const emekdaslar = await this.prisma.$queryRaw<Record<string, unknown>[]>`
      SELECT m.ad AS merkez, count(e.id)::int AS say, COALESCE(sum(e.maas),0)::float8 AS fond
        FROM struktur.merkezler m
        LEFT JOIN kadrlar.emekdaslar e ON e.merkez_id = m.id
       GROUP BY m.ad ORDER BY fond DESC`;

    const umumi = await this.prisma.$queryRaw<{ say: number; fond: number }[]>`
      SELECT count(*)::int AS say, COALESCE(sum(maas),0)::float8 AS fond
        FROM kadrlar.emekdaslar WHERE aktiv = true`;

    const setirler = emekdaslar
      .map(
        (r) => `<tr>
          <td>${r.merkez}</td>
          <td class="reqem">${r.say}</td>
          <td class="reqem">${Number(r.fond).toLocaleString('az-AZ')} ₼</td>
        </tr>`,
      )
      .join('');

    return `<!DOCTYPE html>
<html lang="az"><head><meta charset="UTF-8">
<title>ARTİ — Kadr hesabatı</title>
<style>
  @page { size: A4; margin: 18mm; }
  body { font-family: -apple-system, 'Segoe UI', Roboto, sans-serif;
         color: #1e293b; font-size: 12pt; }
  h1 { color: #1e3a5f; border-bottom: 3px solid #2c5282;
       padding-bottom: 8px; font-size: 20pt; }
  .meta { color: #64748b; font-size: 9pt; text-align: right; margin-top: -8px; }
  table { width: 100%; border-collapse: collapse; margin-top: 16px; }
  th { background: #2c5282; color: #fff; padding: 8px; text-align: left; font-size: 10pt; }
  td { padding: 7px 8px; border-bottom: 1px solid #e2e8f0; }
  tr:nth-child(even) td { background: #f8fafc; }
  .reqem { text-align: right; font-variant-numeric: tabular-nums; }
  tfoot td { font-weight: bold; background: #eef2f7; border-top: 2px solid #2c5282; }
  .footer { margin-top: 24px; font-size: 9pt; color: #64748b;
            border-top: 1px solid #cbd5e1; padding-top: 8px; }
</style></head><body>
<h1>ARTİ — Kadr hesabatı</h1>
<p class="meta">Yaradıldı: ${new Date().toLocaleString('az-AZ')}</p>

<table>
  <thead><tr><th>Mərkəz</th><th class="reqem">Əməkdaş</th><th class="reqem">Aylıq fond</th></tr></thead>
  <tbody>${setirler}</tbody>
  <tfoot><tr>
    <td>CƏMİ</td>
    <td class="reqem">${umumi[0]?.say ?? 0}</td>
    <td class="reqem">${Number(umumi[0]?.fond ?? 0).toLocaleString('az-AZ')} ₼</td>
  </tr></tfoot>
</table>

<div class="footer">
  Azərbaycan Respublikasının Təhsil İnstitutu · Deepseek_ARTI ERP<br>
  Bu hesabat avtomatik yaradılmışdır.
</div>
</body></html>`;
  }
}
