#!/bin/bash
set -e
cd ~/Deepseek_ARTI/DS_Backend || { echo "XETA"; exit 1; }
unset DATABASE_URL PGHOST

echo "════ 1/6  Paket ════"
npm install exceljs@^4.4.0 2>&1 | tail -1

echo "════ 2/6  .env ════"
if ! grep -q DEEPSEEK_API_KEY .env 2>/dev/null; then
cat >> .env <<'ENVSON'

# ── AI ── (acar olmadan da sistem isleyir — demo rejim)
DEEPSEEK_API_KEY=""
DEEPSEEK_MODEL="deepseek-chat"
DEEPSEEK_URL="https://api.deepseek.com"
ENVSON
  echo "  ✓ AI ayarlari elave edildi"
fi

echo "════ 3/6  Qovluqlar ════"
mkdir -p ".github/workflows"
mkdir -p "scripts"
mkdir -p "src/ai"
mkdir -p "src/ai/dto"
mkdir -p "src/ixrac"
mkdir -p "test"
echo "  6 qovluq"

echo "════ 4/6  Fayllar ════"

cat > "src/ai/dto/sual.dto.ts" <<'KODSON'
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsBoolean, IsInt, IsOptional, IsString, Max, MaxLength, Min, MinLength } from 'class-validator';

/** AI-a verilen sual */
export class SualDto {
  @ApiProperty({ example: 'ARTİ-də 2026-cı ildə neçə əməkdaş var?' })
  @IsString()
  @MinLength(3, { message: 'Sual ən azı 3 simvol olmalıdır' })
  @MaxLength(1000)
  sual!: string;

  @ApiPropertyOptional({ description: 'Prompt şablonunun adı' })
  @IsOptional()
  @IsString()
  @MaxLength(120)
  prompt?: string;

  @ApiPropertyOptional({ default: false, description: 'Verilənlər bazası kontekstini əlavə et' })
  @IsOptional()
  @IsBoolean()
  kontekst?: boolean;
}

/** Təbii dil → struktur niyyət (SQL YOX!) */
export class SqlSualDto {
  @ApiProperty({ example: 'Ən çox maaş alan 5 əməkdaşı göstər' })
  @IsString()
  @MinLength(3)
  @MaxLength(500)
  sual!: string;

  @ApiPropertyOptional({ default: 20, maximum: 100 })
  @IsOptional()
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number;
}
KODSON
echo "  ✓ src/ai/dto/sual.dto.ts"

cat > "src/ai/ai.service.ts" <<'KODSON'
import { Injectable, Logger, ServiceUnavailableException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';
import { RagService } from './rag.service.js';
import { SualDto } from './dto/sual.dto.js';

export interface AiCavabi {
  sual: string;
  cavab: string;
  model: string;
  token_sayi: number;
  menbe: 'api' | 'demo' | 'rag';
  kontekst?: { cedvel_adi: string; metn: string; oxsarliq: number }[];
  gecikme_ms: number;
}

/** DeepSeek API cavab formati */
interface DeepSeekCavabi {
  choices?: { message?: { content?: string } }[];
  usage?: { total_tokens?: number };
  error?: { message?: string };
}

@Injectable()
export class AiService {
  private readonly log = new Logger('AI');

  constructor(
    private readonly prisma: PrismaService,
    private readonly rag: RagService,
  ) {}

  /** API acari qurulubmu? */
  get apiHazir(): boolean {
    return Boolean(process.env.DEEPSEEK_API_KEY);
  }

  /** Prompt sablonunu ada gore tapir */
  async promptTap(ad?: string): Promise<string | null> {
    if (!ad) return null;
    const setirler = await this.prisma.$queryRaw<{ prompt_metni: string }[]>`
      SELECT prompt_metni FROM ai.ai_promptlar
       WHERE lower(ad) = lower(${ad}) AND aktiv = true
       LIMIT 1`;
    return setirler[0]?.prompt_metni ?? null;
  }

  /** Butun aktiv promptlar */
  async promptlar() {
    return this.prisma.$queryRaw<
      { id: number; ad: string; tip: string; prompt_metni: string }[]
    >`SELECT id::int, ad, tip, prompt_metni
        FROM ai.ai_promptlar WHERE aktiv = true ORDER BY id`;
  }

  /** Əsas metod — sual ver, cavab al */
  async sorush(dto: SualDto, istifadeci = 'anonim'): Promise<AiCavabi> {
    const baslama = Date.now();

    // 1) RAG — oxsar senedleri tap (kontekst teleb olunarsa)
    let kontekst: AiCavabi['kontekst'];
    let kontekstMetni = '';

    if (dto.kontekst) {
      const oxsar = await this.rag.oxsarTap(dto.sual, 3);
      kontekst = oxsar.map((o) => ({
        cedvel_adi: o.cedvel_adi,
        metn: o.metn,
        oxsarliq: o.oxsarliq,
      }));
      if (oxsar.length) {
        kontekstMetni =
          '\n\nKontekst (bazadan tapılmış sənədlər):\n' +
          oxsar.map((o, i) => `${i + 1}. ${o.metn}`).join('\n');
      }
    }

    // 2) Prompt sablonu
    const sablon = await this.promptTap(dto.prompt);
    const tamPrompt = (sablon ? sablon + '\n\n' : '') + dto.sual + kontekstMetni;

    // 3) API cagirisi
    let netice: AiCavabi;

    if (this.apiHazir) {
      netice = await this.apiCagir(dto.sual, tamPrompt, baslama);
    } else {
      netice = this.demoCavab(dto.sual, kontekst, baslama);
    }

    // 4) Jurnala yaz
    await this.jurnalaYaz(istifadeci, dto.sual, netice.cavab, netice.model, netice.token_sayi);

    return netice;
  }

  /** DeepSeek API cagirisi */
  private async apiCagir(sual: string, prompt: string, baslama: number): Promise<AiCavabi> {
    const acar = process.env.DEEPSEEK_API_KEY!;
    const model = process.env.DEEPSEEK_MODEL ?? 'deepseek-chat';
    const bazUrl = process.env.DEEPSEEK_URL ?? 'https://api.deepseek.com';

    try {
      const cavab = await fetch(`${bazUrl}/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${acar}`,
        },
        body: JSON.stringify({
          model,
          messages: [
            {
              role: 'system',
              content:
                'Sən ARTİ (Azərbaycan Respublikasının Təhsil İnstitutu) ERP ' +
                'sisteminin köməkçisisən. Yalnız Azərbaycan dilində, qısa və ' +
                'dəqiq cavab ver. Bilmədiyini de.',
            },
            { role: 'user', content: prompt },
          ],
          temperature: 0.3,
          max_tokens: 1000,
        }),
        signal: AbortSignal.timeout(30_000),
      });

      if (!cavab.ok) {
        const xetaMetni = await cavab.text();
        this.log.error(`API xetasi ${cavab.status}: ${xetaMetni.slice(0, 200)}`);
        throw new ServiceUnavailableException(
          `AI xidməti cavab vermədi (HTTP ${cavab.status})`,
        );
      }

      const govde = (await cavab.json()) as DeepSeekCavabi;

      return {
        sual,
        cavab: govde.choices?.[0]?.message?.content ?? '(boş cavab)',
        model: govde.usage ? model : model,
        token_sayi: govde.usage?.total_tokens ?? 0,
        menbe: 'api',
        gecikme_ms: Date.now() - baslama,
      };
    } catch (xeta) {
      if (xeta instanceof ServiceUnavailableException) throw xeta;
      this.log.error(`AI cagirisi ugursuz: ${(xeta as Error).message}`);
      throw new ServiceUnavailableException(
        `AI xidmətinə qoşulmaq mümkün olmadı: ${(xeta as Error).message}`,
      );
    }
  }

  /** API acari olmadan isleyen cavab */
  private demoCavab(
    sual: string,
    kontekst: AiCavabi['kontekst'],
    baslama: number,
  ): AiCavabi {
    const setirler = [
      '⚠️ DEEPSEEK_API_KEY qurulmamışdır — demo rejimdədir.',
      '',
      `Sualınız: "${sual}"`,
      '',
    ];

    if (kontekst?.length) {
      setirler.push('Bazadan tapılan uyğun sənədlər:');
      for (const k of kontekst) {
        setirler.push(`  • [${k.oxsarliq.toFixed(3)}] ${k.metn}`);
      }
      setirler.push('');
    }

    setirler.push(
      'Real cavab üçün .env faylına açarı əlavə edin:',
      '  DEEPSEEK_API_KEY="sk-..."',
      'Sonra serveri yenidən başladın.',
    );

    return {
      sual,
      cavab: setirler.join('\n'),
      model: 'demo',
      token_sayi: 0,
      menbe: kontekst?.length ? 'rag' : 'demo',
      kontekst,
      gecikme_ms: Date.now() - baslama,
    };
  }

  /** Sorgunu jurnala yaz */
  private async jurnalaYaz(
    istifadeci: string,
    sorghu: string,
    cavab: string,
    model: string,
    token: number,
  ): Promise<void> {
    try {
      await this.prisma.$executeRaw`
        INSERT INTO ai.ai_sorghular (istifadeci, sorghu, cavab, model, token_sayi)
        VALUES (${istifadeci}, ${sorghu}, ${cavab.slice(0, 4000)}, ${model}, ${token})`;
    } catch (x) {
      this.log.error(`Jurnal yazilmadi: ${(x as Error).message}`);
    }
  }

  /** Son sorğular */
  async tarixce(limit = 20) {
    return this.prisma.$queryRawUnsafe<
      { id: number; istifadeci: string | null; sorghu: string; model: string | null;
        token_sayi: number | null; vaxt: string }[]
    >(
      `SELECT id::int, istifadeci, sorghu, model, token_sayi, vaxt::text
         FROM ai.ai_sorghular ORDER BY vaxt DESC LIMIT $1`,
      limit,
    );
  }

  /** Statistika */
  async statistika() {
    const setirler = await this.prisma.$queryRaw<
      { cem: number; token: number; model_sayi: number }[]
    >`
      SELECT count(*)::int                                   AS cem,
             COALESCE(sum(token_sayi), 0)::int               AS token,
             count(DISTINCT model)::int                      AS model_sayi
        FROM ai.ai_sorghular`;

    return {
      ...(setirler[0] ?? { cem: 0, token: 0, model_sayi: 0 }),
      api_hazir: this.apiHazir,
      embedding_sayi: (await this.prisma.$queryRaw<{ say: number }[]>`
        SELECT count(*)::int AS say FROM ai.embeddingler`)[0]?.say ?? 0,
    };
  }
}
KODSON
echo "  ✓ src/ai/ai.service.ts"

cat > "src/ai/rag.service.ts" <<'KODSON'
import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

/** Vektor — JSONB-da saxlanilan eded massivi */
export type Vektor = number[];

export interface OxsarNetice {
  id: number;
  cedvel_adi: string;
  sened_id: number | null;
  metn: string;
  oxsarliq: number;
}

/**
 * RAG — Retrieval Augmented Generation.
 *
 * pgvector QURULMADIGI ucun oxsarliq TETBIQ QATINDA hesablanir:
 *   1. Sual vektora cevrilir
 *   2. Her sened ucun kosinus oxsarliği hesablanir
 *   3. En yaxin N sened secilir
 *
 * Bu, 10 000 senede qeder tamamilə kifayetdir.
 * Daha boyuk hecmde pgvector-e kecin (aşaği bax).
 */
@Injectable()
export class RagService {
  private readonly log = new Logger('RAG');

  /** Vektorun olcusu — butun embeddingler eyni olmali */
  static readonly OLCU = 64;

  constructor(private readonly prisma: PrismaService) {}

  /**
   * METN -> VEKTOR (deterministik hash embedding).
   *
   * Qeyd: bu, HEQIQI semantik embedding DEYIL. Sözləri hash ile
   * vektora cevirir — eyni sözler eyni mövqelere düşür.
   *
   * Real sistemde DeepSeek/OpenAI embedding API-si işledilir:
   *   POST /v1/embeddings  { input: "...", model: "..." }
   */
  vektorlastir(metn: string): Vektor {
    const vektor = new Array(RagService.OLCU).fill(0);
    const sozler = metn
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\s]/gu, ' ')
      .split(/\s+/)
      .filter((s) => s.length > 1);

    for (const soz of sozler) {
      // Iki musteqil hash — bir soz iki mövqeye töhfə verir
      const h1 = this.hash(soz, 0) % RagService.OLCU;
      const h2 = this.hash(soz, 1) % RagService.OLCU;
      vektor[h1] += 1;
      vektor[h2] += 0.5;
    }

    return this.normallashdir(vektor);
  }

  /** Kosinus oxsarliği — iki vektor arasindaki bucaq */
  oxsarliq(a: Vektor, b: Vektor): number {
    if (a.length !== b.length) return 0;

    let nokta = 0;
    let normA = 0;
    let normB = 0;

    for (let i = 0; i < a.length; i++) {
      nokta += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }

    const mexrec = Math.sqrt(normA) * Math.sqrt(normB);
    return mexrec === 0 ? 0 : nokta / mexrec;
  }

  /** Oxsar senedleri tap */
  async oxsarTap(sual: string, limit = 5, minOxsarliq = 0.1): Promise<OxsarNetice[]> {
    const sualVektoru = this.vektorlastir(sual);

    const setirler = await this.prisma.$queryRaw<
      { id: number; cedvel_adi: string; sened_id: number | null; metn: string | null; vektor: Vektor | null }[]
    >`
      SELECT id::int, cedvel_adi, sened_id, metn, vektor
        FROM ai.embeddingler
       WHERE metn IS NOT NULL`;

    const neticeler: OxsarNetice[] = [];

    for (const s of setirler) {
      // Vektor yoxdursa — yerinde hesabla (kowhnə setirler ucun)
      const v = Array.isArray(s.vektor) && s.vektor.length === RagService.OLCU
        ? s.vektor
        : this.vektorlastir(s.metn ?? '');

      const oxsarliq = this.oxsarliq(sualVektoru, v);
      if (oxsarliq >= minOxsarliq) {
        neticeler.push({
          id: s.id,
          cedvel_adi: s.cedvel_adi,
          sened_id: s.sened_id,
          metn: s.metn ?? '',
          oxsarliq: Number(oxsarliq.toFixed(4)),
        });
      }
    }

    neticeler.sort((a, b) => b.oxsarliq - a.oxsarliq);
    this.log.log(`"${sual.slice(0, 40)}" -> ${neticeler.length} netice`);
    return neticeler.slice(0, limit);
  }

  /** Butun senedleri vektorlashdir (bir defe isledilir) */
  async indeksle(): Promise<{ indekslendi: number }> {
    const setirler = await this.prisma.$queryRaw<
      { id: number; metn: string | null }[]
    >`SELECT id::int, metn FROM ai.embeddingler WHERE metn IS NOT NULL`;

    let say = 0;
    for (const s of setirler) {
      const vektor = this.vektorlastir(s.metn ?? '');
      await this.prisma.$executeRaw`
        UPDATE ai.embeddingler SET vektor = ${JSON.stringify(vektor)}::jsonb
         WHERE id = ${s.id}`;
      say++;
    }

    this.log.log(`${say} sened vektorlashdirildi`);
    return { indekslendi: say };
  }

  /** Vahid uzunluga getir — kosinusu sürətləndirir */
  private normallashdir(v: Vektor): Vektor {
    const uzunluq = Math.sqrt(v.reduce((c, x) => c + x * x, 0));
    return uzunluq === 0 ? v : v.map((x) => Number((x / uzunluq).toFixed(6)));
  }

  /** Sadə deterministik hash (FNV-1a) */
  private hash(soz: string, duz: number): number {
    let h = 2166136261 ^ duz;
    for (let i = 0; i < soz.length; i++) {
      h ^= soz.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return Math.abs(h);
  }
}
KODSON
echo "  ✓ src/ai/rag.service.ts"

cat > "src/ai/sql-komlekci.service.ts" <<'KODSON'
import { BadRequestException, Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

/**
 * TƏBİİ DİL -> SQL KÖMƏKÇİSİ
 *
 * ══════════════════════════════════════════════════════════════
 *  TƏHLÜKƏSİZLİK PRİNSİPİ
 * ══════════════════════════════════════════════════════════════
 *  AI HEÇ VAXT birbaşa SQL YAZMIR.
 *
 *  AI yalnız RESEPT ADI seçir (mes: 'en_cox_maas').
 *  SQL isə bu faylda SABİT yazılıb — dəyişdirilə bilməz.
 *
 *  Səbəb: AI-a SQL yazmaq hüququ versek, o:
 *    - DELETE / DROP yaza bilər
 *    - Başqa cədvəlləri oxuya bilər
 *    - Prompt injection ilə aldadıla bilər
 * ══════════════════════════════════════════════════════════════
 */

export interface Resept {
  ad: string;
  açarSözler: string[];
  izah: string;
  sql: string;
  parametrli?: boolean;
}

export interface SqlNetice {
  sual: string;
  resept: string;
  izah: string;
  sql: string;
  setirler: Record<string, unknown>[];
  setirSayi: number;
  icra_ms: number;
}

/** RESEPT REYESTRİ — butun SQL burada, SABİT */
const RESEPTLER: Resept[] = [
  {
    ad: 'emekdas_sayi',
    açarSözler: ['neçə əməkdaş', 'nece emekdas', 'işçi sayı', 'kadr sayı', 'əməkdaş sayı'],
    izah: 'Aktiv əməkdaşların ümumi sayı',
    sql: `SELECT count(*)::int AS emekdas_sayi
            FROM kadrlar.emekdaslar WHERE aktiv = true`,
  },
  {
    ad: 'en_cox_maas',
    açarSözler: ['ən çox maaş', 'en cox maas', 'yüksək maaş', 'bahalı işçi', 'top maaş'],
    izah: 'Ən yüksək maaş alan əməkdaşlar',
    sql: `SELECT e.soyad || ' ' || e.ad AS emekdas,
                 m.ad AS merkez,
                 e.maas::float8 AS maas
            FROM kadrlar.emekdaslar e
            LEFT JOIN struktur.merkezler m ON m.id = e.merkez_id
           WHERE e.aktiv = true
           ORDER BY e.maas DESC NULLS LAST
           LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'merkez_uzre',
    açarSözler: ['mərkəz üzrə', 'merkez uzre', 'mərkəzlər', 'şöbə sayı', 'mərkəz sayı'],
    izah: 'Hər mərkəz üzrə şöbə və əməkdaş sayı',
    sql: `SELECT m.ad AS merkez,
                 count(DISTINCT s.id)::int AS shobe_sayi,
                 count(DISTINCT e.id)::int AS emekdas_sayi
            FROM struktur.merkezler m
            LEFT JOIN struktur.shobeler  s ON s.merkez_id = m.id
            LEFT JOIN kadrlar.emekdaslar e ON e.merkez_id = m.id
           GROUP BY m.ad ORDER BY shobe_sayi DESC LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'maas_fondu',
    açarSözler: ['maaş fondu', 'maas fondu', 'ümumi maaş', 'ə/h fondu', 'əmək haqqı'],
    izah: 'Aylıq əmək haqqı fondu',
    sql: `SELECT count(*)::int                  AS emekdas,
                 sum(maas)::float8             AS aylıq_fond,
                 round(avg(maas), 2)::float8   AS orta_maas
            FROM kadrlar.emekdaslar WHERE aktiv = true`,
  },
  {
    ad: 'layiheler',
    açarSözler: ['layihə', 'layihe', 'tədqiqat', 'tedqiqat', 'elmi iş'],
    izah: 'Elmi-tədqiqat layihələri',
    sql: `SELECT l.ad AS layihe, i.ad AS istiqamet, l.status,
                 l.baslama_tarixi::text AS baslama
            FROM elm.tedqiqat_layiheleri l
            JOIN elm.tedqiqat_istiqametleri i ON i.id = l.istiqamet_id
           ORDER BY l.baslama_tarixi DESC NULLS LAST LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'budce',
    açarSözler: ['büdcə', 'budce', 'maliyyə', 'maliyye', 'xərc'],
    izah: 'İllər üzrə büdcə',
    sql: `SELECT il, menbe, mebleg::float8 AS mebleg
            FROM maliyye.budce ORDER BY il DESC, mebleg DESC LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'telim_qruplari',
    açarSözler: ['qrup', 'təlim', 'telim', 'kurs', 'iştirakçı'],
    izah: 'Təlim qrupları və iştirakçı sayı',
    sql: `SELECT q.ad AS qrup, p.ad AS proqram, q.status,
                 count(i.id)::int AS istirakci
            FROM tehsil.telim_qruplari q
            JOIN tehsil.telim_proqramlari p ON p.id = q.proqram_id
            LEFT JOIN tehsil.telim_istirakcilari i ON i.qrup_id = q.id
           GROUP BY q.ad, p.ad, q.status
           ORDER BY istirakci DESC LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'sertifikasiya',
    açarSözler: ['sertifikasiya', 'imtahan', 'bal', 'nəticə'],
    izah: 'Sertifikasiya nəticələri',
    sql: `SELECT ad_soyad, bal::float8 AS bal, netice,
                 imtahan_tarixi::text AS tarix
            FROM tehsil.sertifikasiya
           ORDER BY bal DESC NULLS LAST LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'son_emrler',
    açarSözler: ['əmr', 'emr', 'sənəd', 'sened'],
    izah: 'Son əmrlər',
    sql: `SELECT emr_no, tarix::text AS tarix, movzu, imzalayan
            FROM sened.emrler ORDER BY tarix DESC LIMIT $1`,
    parametrli: true,
  },
  {
    ad: 'logistika',
    açarSözler: ['aktiv', 'avadanlıq', 'inventar', 'logistika', 'avadanliq'],
    izah: 'Logistika aktivləri',
    sql: `SELECT ad, tip, veziyyet, deyer::float8 AS deyer,
                 alinma_tarixi::text AS alinma
            FROM logistika.aktivler ORDER BY deyer DESC NULLS LAST LIMIT $1`,
    parametrli: true,
  },
];

/**
 * AI-a gonderilecek resept siyahisi (yalniz ADLAR ve IZAHLAR).
 *
 * DİQQƏT: bu, STATİK METOD DEYİL — MODUL SƏVİYYƏLİ funksiyadır.
 *
 * Sebeb: esbuild (vitest) dekorator transformu statik metodları
 * sinifden cixarir. Kompilyasiya olunmus kodda isleyir, testde ise
 * 'undefined' olur. Modul funksiyasi ise HER IKI halda isleyir.
 */
export function reseptSiyahisi(): { ad: string; izah: string }[] {
  return RESEPTLER.map((r) => ({ ad: r.ad, izah: r.izah }));
}

@Injectable()
export class SqlKomlekciService {
  private readonly log = new Logger('SQL-KOMEKCI');

  constructor(private readonly prisma: PrismaService) {}

  /** Sualdan resept secir */
  reseptSec(sual: string): Resept | null {
    const kicik = sual.toLowerCase();

    // 1) Birbasa resept adi cekilirse
    const adIle = RESEPTLER.find((r) => kicik.includes(r.ad));
    if (adIle) return adIle;

    // 2) Acar sözler uzre — en cox uygun gelen
    let enYaxsi: Resept | null = null;
    let enCox = 0;

    for (const r of RESEPTLER) {
      const uygun = r.açarSözler.filter((a) => kicik.includes(a)).length;
      if (uygun > enCox) {
        enCox = uygun;
        enYaxsi = r;
      }
    }

    return enCox > 0 ? enYaxsi : null;
  }

  /** Sualı icra edir */
  async icraEt(sual: string, limit = 20): Promise<SqlNetice> {
    const resept = this.reseptSec(sual);

    if (!resept) {
      throw new BadRequestException(
        `Bu sualı SQL-ə çevirə bilmədim: "${sual}". ` +
        `Mövcud mövzular: ${RESEPTLER.map((r) => r.ad).join(', ')}`,
      );
    }

    const baslama = Date.now();
    const setirler = resept.parametrli
      ? await this.prisma.$queryRawUnsafe<Record<string, unknown>[]>(resept.sql, limit)
      : await this.prisma.$queryRawUnsafe<Record<string, unknown>[]>(resept.sql);

    const icra = Date.now() - baslama;
    this.log.log(`"${sual.slice(0, 40)}" -> ${resept.ad} (${setirler.length} setir, ${icra}ms)`);

    return {
      sual,
      resept: resept.ad,
      izah: resept.izah,
      sql: resept.sql.replace(/\s+/g, ' ').trim(),
      setirler,
      setirSayi: setirler.length,
      icra_ms: icra,
    };
  }
}
KODSON
echo "  ✓ src/ai/sql-komlekci.service.ts"

cat > "src/ai/ai.controller.ts" <<'KODSON'
import { Body, Controller, Get, Post, Query, ParseIntPipe } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { AiService } from './ai.service.js';
import { RagService } from './rag.service.js';
import { SqlKomlekciService, reseptSiyahisi } from './sql-komlekci.service.js';
import { SualDto, SqlSualDto } from './dto/sual.dto.js';
import { CurrentUser } from '../auth/decorators/current-user.decorator.js';
import { Roles } from '../auth/decorators/roles.decorator.js';
import type { CariIstifadeci } from '../auth/decorators/current-user.decorator.js';

@ApiTags('ai')
@ApiBearerAuth()
@Controller('ai')
export class AiController {
  constructor(
    private readonly ai: AiService,
    private readonly rag: RagService,
    private readonly sql: SqlKomlekciService,
  ) {}

  @Get('statistika')
  @ApiOperation({ summary: 'AI istifade statistikasi' })
  statistika() {
    return this.ai.statistika();
  }

  @Get('promptlar')
  @ApiOperation({ summary: 'Prompt sablonlari' })
  promptlar() {
    return this.ai.promptlar();
  }

  @Post('sorush')
  @ApiOperation({ summary: 'AI-a sual ver' })
  sorush(@Body() dto: SualDto, @CurrentUser() istifadeci: CariIstifadeci) {
    return this.ai.sorush(dto, istifadeci?.email ?? 'anonim');
  }

  @Get('tarixce')
  @Roles('admin')
  @ApiOperation({ summary: 'Son AI sorgulari (yalniz admin)' })
  tarixce(@Query('limit', new ParseIntPipe({ optional: true })) limit?: number) {
    return this.ai.tarixce(limit ?? 20);
  }

  // ── RAG ──
  @Get('oxsar')
  @ApiOperation({ summary: 'RAG — oxsar senedleri tap' })
  oxsar(
    @Query('sual') sual: string,
    @Query('limit', new ParseIntPipe({ optional: true })) limit?: number,
  ) {
    return this.rag.oxsarTap(sual ?? '', limit ?? 5);
  }

  @Post('indeksle')
  @Roles('admin')
  @ApiOperation({ summary: 'Embeddingleri vektorlashdir (yalniz admin)' })
  indeksle() {
    return this.rag.indeksle();
  }

  // ── TƏBİİ DİL -> SQL ──
  @Get('reseptler')
  @ApiOperation({ summary: 'Mövcud SQL reseptleri' })
  reseptler() {
    return reseptSiyahisi();
  }

  @Post('sql')
  @ApiOperation({
    summary: 'Tebii dil -> SQL',
    description:
      'AI birbasa SQL YAZMIR — yalniz movcud reseptlerden birini secir. ' +
      'Butun SQL kodu sabit yazilib ve yalniz OXUMA sorgularidir.',
  })
  sqlSorush(@Body() dto: SqlSualDto) {
    return this.sql.icraEt(dto.sual, dto.limit ?? 20);
  }
}
KODSON
echo "  ✓ src/ai/ai.controller.ts"

cat > "src/ai/ai.module.ts" <<'KODSON'
import { Module } from '@nestjs/common';
import { AiService } from './ai.service.js';
import { RagService } from './rag.service.js';
import { SqlKomlekciService } from './sql-komlekci.service.js';
import { AiController } from './ai.controller.js';

@Module({
  controllers: [AiController],
  providers: [AiService, RagService, SqlKomlekciService],
  exports: [AiService, RagService],
})
export class AiModule {}
KODSON
echo "  ✓ src/ai/ai.module.ts"

cat > "src/ixrac/ixrac.service.ts" <<'KODSON'
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
KODSON
echo "  ✓ src/ixrac/ixrac.service.ts"

cat > "src/ixrac/ixrac.controller.ts" <<'KODSON'
import { Controller, Get, Header, Res } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import type { Response } from 'express';
import { IxracService } from './ixrac.service.js';
import { Roles } from '../auth/decorators/roles.decorator.js';

@ApiTags('ixrac')
@ApiBearerAuth()
@Controller('ixrac')
export class IxracController {
  constructor(private readonly ixrac: IxracService) {}

  @Get('emekdaslar.xlsx')
  @ApiOperation({ summary: 'Emekdaslari Excel-e cixar' })
  @Header('Content-Type',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  async emekdaslar(@Res() cavab: Response) {
    const bufer = await this.ixrac.emekdaslarExcel();
    cavab.setHeader('Content-Disposition',
      'attachment; filename="emekdaslar.xlsx"');
    cavab.send(bufer);
  }

  @Get('budce.xlsx')
  @ApiOperation({ summary: 'Budceni Excel-e cixar' })
  @Roles('admin', 'maliyyeci')
  @Header('Content-Type',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  async budce(@Res() cavab: Response) {
    const bufer = await this.ixrac.budceExcel();
    cavab.setHeader('Content-Disposition', 'attachment; filename="budce.xlsx"');
    cavab.send(bufer);
  }

  @Get('hesabat.html')
  @ApiOperation({
    summary: 'HTML hesabat — brauzerde Ctrl+P ile PDF kimi saxlanilir',
  })
  @Header('Content-Type', 'text/html; charset=utf-8')
  async hesabat(@Res() cavab: Response) {
    cavab.send(await this.ixrac.htmlHesabat());
  }
}
KODSON
echo "  ✓ src/ixrac/ixrac.controller.ts"

cat > "src/ixrac/ixrac.module.ts" <<'KODSON'
import { Module } from '@nestjs/common';
import { IxracService } from './ixrac.service.js';
import { IxracController } from './ixrac.controller.js';

@Module({
  controllers: [IxracController],
  providers: [IxracService],
  exports: [IxracService],
})
export class IxracModule {}
KODSON
echo "  ✓ src/ixrac/ixrac.module.ts"

cat > "Dockerfile" <<'KODSON'
# ══════════════════════════════════════════════════════════════
#  DS_Backend — çoxmərhələli (multi-stage) Docker qurulusu
#  Nəticə: ~180 MB image (node_modules daxil deyil)
# ══════════════════════════════════════════════════════════════

# ─── MƏRHƏLƏ 1: asılılıqlar ───
FROM node:22-alpine AS asililiqlar
WORKDIR /app

# Yalniz manifestleri kocur — layer kesi saxlanilir
COPY package*.json ./
COPY prisma ./prisma
COPY prisma.config.ts ./

# npm ci — package-lock.json-a EYNIEN uygun qurur (npm install YOX)
RUN npm ci --ignore-scripts

# ─── MƏRHƏLƏ 2: qurulus ───
FROM node:22-alpine AS qurulus
WORKDIR /app

COPY --from=asililiqlar /app/node_modules ./node_modules
COPY . .

# Prisma musteri kodunu yarat
RUN npx prisma generate

# TypeScript -> JavaScript
RUN npm run build

# Yalniz istehsalat asililiqlari
RUN npm prune --omit=dev

# ─── MƏRHƏLƏ 3: istehsalat ───
FROM node:22-alpine AS istehsalat
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=4000

# Guvenlik: root olmayan istifadeci
RUN addgroup -g 1001 -S nodejs && adduser -S nestjs -u 1001

COPY --from=qurulus --chown=nestjs:nodejs /app/node_modules ./node_modules
COPY --from=qurulus --chown=nestjs:nodejs /app/dist         ./dist
COPY --from=qurulus --chown=nestjs:nodejs /app/prisma       ./prisma
COPY --from=qurulus --chown=nestjs:nodejs /app/package.json ./

USER nestjs

EXPOSE 4000

# Saglamliq yoxlamasi — konteyner "canli" sayilir?
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:4000/api/v1/saglamliq').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

CMD ["node", "dist/main.js"]
KODSON
echo "  ✓ Dockerfile"

cat > "docker-compose.yml" <<'KODSON'
# ══════════════════════════════════════════════════════════════
#  DS_Backend + PostgreSQL — butun sistem bir emrle
#  Istifade:  docker compose up -d
# ══════════════════════════════════════════════════════════════
services:

  baza:
    image: postgres:18-alpine
    container_name: ds_baza
    restart: unless-stopped
    environment:
      POSTGRES_DB: arti_baza
      POSTGRES_USER: arti_user
      POSTGRES_PASSWORD: ${DB_PASSWORD:-arti_secret_2025}
    ports:
      - "5433:5432"          # 5433 — lokal PostgreSQL ile toqqusmasin
    volumes:
      - baza_melumat:/var/lib/postgresql/data
      # Strukturu ILK defe yaradanda yuklenir
      - ./prisma/init:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U arti_user -d arti_baza"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ds_api
    restart: unless-stopped
    depends_on:
      baza:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://arti_user:${DB_PASSWORD:-arti_secret_2025}@baza:5432/arti_baza
      PORT: 4000
      NODE_ENV: production
      JWT_SECRET: ${JWT_SECRET:?JWT_SECRET teyin olunmalidir}
      JWT_MUDDET: 8h
      DEEPSEEK_API_KEY: ${DEEPSEEK_API_KEY:-}
      DEEPSEEK_MODEL: deepseek-chat
    ports:
      - "4000:4000"

volumes:
  baza_melumat:
    name: ds_baza_melumat
KODSON
echo "  ✓ docker-compose.yml"

cat > ".dockerignore" <<'KODSON'
node_modules
dist
.git
.github
.env
.env.*
!.env.example
*.log
coverage
src/generated
*.tsbuildinfo
.DS_Store
_hesabat
DƏRSLƏR
KODSON
echo "  ✓ .dockerignore"

cat > ".github/workflows/ci.yml" <<'KODSON'
# ══════════════════════════════════════════════════════════════
#  GitHub Actions — CI (Continuous Integration)
#  Her push ve PR-da: build + test + docker
# ══════════════════════════════════════════════════════════════
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # ── 1. TEST ──
  test:
    name: Qurulus ve testler
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:18-alpine
        env:
          POSTGRES_DB: arti_baza
          POSTGRES_USER: arti_user
          POSTGRES_PASSWORD: arti_secret_2025
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U arti_user -d arti_baza"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    env:
      DATABASE_URL: postgresql://arti_user:arti_secret_2025@localhost:5432/arti_baza
      JWT_SECRET: ci-test-acari-deyil
      JWT_MUDDET: 8h
      PORT: 4000

    steps:
      - name: Kodu gotur
        uses: actions/checkout@v4

      - name: Node.js qur
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Paketleri qur
        run: npm ci

      - name: Strukturu yukle
        run: |
          psql "$DATABASE_URL" -f ../../DS_Baza/sql/00_TAM_DDL.sql 2>/dev/null || \
          psql "$DATABASE_URL" -f prisma/init/01_struktur.sql

      - name: Prisma musterisini yarat
        run: npx prisma generate

      - name: Build
        run: npm run build

      - name: Unit testler
        run: npm test

      - name: e2e testler
        run: npx vitest run --config vitest.config.e2e.ts

  # ── 2. DOCKER ──
  docker:
    name: Docker image
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - name: Buildx qur
        uses: docker/setup-buildx-action@v3

      - name: Image qur (push etmeden)
        uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: ds-backend:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ── 3. KEYFIYYET ──
  keyfiyyet:
    name: Kod keyfiyyeti
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - run: npm ci
      - name: Lint
        run: npx oxlint src/ || true
      - name: Format yoxlamasi
        run: npx prettier --check "src/**/*.ts" || true
KODSON
echo "  ✓ .github/workflows/ci.yml"

cat > "scripts/ehtiyat.sh" <<'KODSON'
#!/bin/bash
# ══════════════════════════════════════════════════════════════
#  Ehtiyat nusxe (backup) — pg_dump + sıxılmış arxiv + kohne temizleme
#
#  Istifade:  bash scripts/ehtiyat.sh
#  Cron:      0 2 * * * cd ~/Deepseek_ARTI/DS_Backend && bash scripts/ehtiyat.sh
# ══════════════════════════════════════════════════════════════
set -e

unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"

BAZA="${BAZA:-arti_baza}"
ISTIFADECI="${ISTIFADECI:-arti_user}"
QOVLUQ="${QOVLUQ:-$HOME/Deepseek_ARTI/_arxiV/ehtiyat}"
SAXLAMA_GUN="${SAXLAMA_GUN:-30}"

mkdir -p "$QOVLUQ"
VAXT=$(date +%Y%m%d_%H%M%S)
FAYL="$QOVLUQ/${BAZA}_${VAXT}.sql.gz"

echo "════ Ehtiyat nusxe ════"
echo "  Baza  : $BAZA"
echo "  Hedef : $FAYL"

# 1) Dump + sixma
pg_dump -U "$ISTIFADECI" -d "$BAZA" --no-owner --no-privileges | gzip > "$FAYL"

OLCU=$(du -h "$FAYL" | cut -f1)
echo "  Olcu  : $OLCU"

# 2) Yoxla — fayl bos deyil?
if [ ! -s "$FAYL" ]; then
  echo "  XETA: ehtiyat faylı BOSDUR!"
  exit 1
fi

# 3) Yoxla — bərpa oluna bilermi? (strukturu say)
# QEYD: macOS-un zcat-i BSD versiyasidir ve .Z fayl gozleyir.
#       gunzip -c HER platformada isleyir.
SETIR=$(gunzip -c "$FAYL" | grep -c 'CREATE TABLE' || true)
echo "  CREATE TABLE: $SETIR"
if [ "$SETIR" -lt 40 ]; then
  echo "  XEBERDARLIQ: gozlenilenden az cedvel ($SETIR < 40)"
fi

# 4) Kohne ehtiyatlari temizle
SILINEN=$(find "$QOVLUQ" -name "${BAZA}_*.sql.gz" -mtime "+$SAXLAMA_GUN" | wc -l | tr -d ' ')
find "$QOVLUQ" -name "${BAZA}_*.sql.gz" -mtime "+$SAXLAMA_GUN" -delete
echo "  Silinen kohne: $SILINEN (${SAXLAMA_GUN} gunden kohne)"

# 5) İcmal
CEMI=$(find "$QOVLUQ" -name "${BAZA}_*.sql.gz" | wc -l | tr -d ' ')
UMUMI=$(du -sh "$QOVLUQ" | cut -f1)
echo "  Arxivde: $CEMI fayl, $UMUMI"
echo "════ HAZIR ════"
KODSON
echo "  ✓ scripts/ehtiyat.sh"

cat > "src/ai/rag.service.spec.ts" <<'KODSON'
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { RagService } from './rag.service.js';

function saxtaPrisma() {
  return { $queryRaw: vi.fn(), $executeRaw: vi.fn() } as any;
}

describe('RagService', () => {
  let prisma: any;
  let rag: RagService;

  beforeEach(() => {
    prisma = saxtaPrisma();
    rag = new RagService(prisma);
  });

  // ── VEKTORLASDIRMA ──
  describe('vektorlastir()', () => {
    it('duzgun olcude vektor qaytarir', () => {
      const v = rag.vektorlastir('kurikulum islahatı');
      expect(v).toHaveLength(RagService.OLCU);
    });

    it('vektor vahid uzunluga getirilir (norm = 1)', () => {
      const v = rag.vektorlastir('tehsil sistemi ve kurikulum');
      const uzunluq = Math.sqrt(v.reduce((c, x) => c + x * x, 0));
      expect(uzunluq).toBeCloseTo(1, 4);
    });

    it('eyni metn -> EYNI vektor (deterministik)', () => {
      const a = rag.vektorlastir('informatika telimi');
      const b = rag.vektorlastir('informatika telimi');
      expect(a).toEqual(b);
    });

    it('ferqli metn -> FERQLI vektor', () => {
      const a = rag.vektorlastir('kurikulum islahatı');
      const b = rag.vektorlastir('maliyye hesabati');
      expect(a).not.toEqual(b);
    });

    it('bos metn ucun sifir vektor', () => {
      const v = rag.vektorlastir('');
      expect(v.every((x) => x === 0)).toBe(true);
    });
  });

  // ── KOSINUS OXSARLIGI ──
  describe('oxsarliq()', () => {
    it('eyni vektor -> 1.0', () => {
      const v = rag.vektorlastir('kurikulum');
      expect(rag.oxsarliq(v, v)).toBeCloseTo(1, 5);
    });

    it('sifir vektor -> 0 (sifira bolme yoxdur)', () => {
      const sifir = new Array(RagService.OLCU).fill(0);
      const v = rag.vektorlastir('test');
      expect(rag.oxsarliq(sifir, v)).toBe(0);
      expect(rag.oxsarliq(sifir, sifir)).toBe(0);
    });

    it('ferqli olculu vektor -> 0', () => {
      expect(rag.oxsarliq([1, 2], [1, 2, 3])).toBe(0);
    });

    it('oxsar metnler yuksek bal alir', () => {
      const a = rag.vektorlastir('kurikulum islahatı tehsil');
      const b = rag.vektorlastir('kurikulum islahatı telim');
      const c = rag.vektorlastir('maliyye budce xerci');

      const yaxin = rag.oxsarliq(a, b);
      const uzaq = rag.oxsarliq(a, c);

      expect(yaxin).toBeGreaterThan(uzaq);
    });

    it('bal 0 ile 1 arasindadir', () => {
      const a = rag.vektorlastir('tehsil');
      const b = rag.vektorlastir('kurikulum');
      const bal = rag.oxsarliq(a, b);
      expect(bal).toBeGreaterThanOrEqual(0);
      expect(bal).toBeLessThanOrEqual(1);
    });
  });

  // ── OXSAR TAP ──
  describe('oxsarTap()', () => {
    it('neticeleri oxsarliq uzre azalan siralayir', async () => {
      prisma.$queryRaw.mockResolvedValue([
        { id: 1, cedvel_adi: 'a', sened_id: 1, metn: 'kurikulum islahatı tehsil', vektor: null },
        { id: 2, cedvel_adi: 'b', sened_id: 2, metn: 'maliyye budce hesabati', vektor: null },
        { id: 3, cedvel_adi: 'c', sened_id: 3, metn: 'kurikulum islahatı telim', vektor: null },
      ]);

      const n = await rag.oxsarTap('kurikulum', 3, 0.01);

      expect(n.length).toBeGreaterThan(1);
      for (let i = 1; i < n.length; i++) {
        expect(n[i - 1].oxsarliq).toBeGreaterThanOrEqual(n[i].oxsarliq);
      }
    });

    it('limit-e riayet edir', async () => {
      prisma.$queryRaw.mockResolvedValue(
        Array.from({ length: 10 }, (_, i) => ({
          id: i + 1, cedvel_adi: 'x', sened_id: i + 1,
          metn: `kurikulum sened ${i}`, vektor: null,
        })),
      );

      const n = await rag.oxsarTap('kurikulum', 3, 0.01);
      expect(n).toHaveLength(3);
    });

    it('minOxsarliq-dan asagi neticeleri suzur', async () => {
      prisma.$queryRaw.mockResolvedValue([
        { id: 1, cedvel_adi: 'a', sened_id: 1, metn: 'tamamilə fərqli mövzu', vektor: null },
      ]);

      const n = await rag.oxsarTap('kurikulum', 5, 0.9);
      expect(n).toHaveLength(0);
    });

    it('saxlanilan vektor varsa onu isledir', async () => {
      const hazir = rag.vektorlastir('kurikulum islahatı');
      prisma.$queryRaw.mockResolvedValue([
        { id: 1, cedvel_adi: 'a', sened_id: 1, metn: 'metn', vektor: hazir },
      ]);

      const n = await rag.oxsarTap('kurikulum islahatı', 1, 0.01);
      expect(n).toHaveLength(1);
      expect(n[0].oxsarliq).toBeCloseTo(1, 4);
    });
  });

  // ── INDEKSLEME ──
  describe('indeksle()', () => {
    it('butun senedleri vektorlashdirir', async () => {
      prisma.$queryRaw.mockResolvedValue([
        { id: 1, metn: 'birinci sened' },
        { id: 2, metn: 'ikinci sened' },
      ]);
      prisma.$executeRaw.mockResolvedValue(1);

      const n = await rag.indeksle();

      expect(n.indekslendi).toBe(2);
      expect(prisma.$executeRaw).toHaveBeenCalledTimes(2);
    });

    it('metn NULL olanlari kecir', async () => {
      prisma.$queryRaw.mockResolvedValue([{ id: 1, metn: 'sened' }]);
      prisma.$executeRaw.mockResolvedValue(1);

      const n = await rag.indeksle();
      expect(n.indekslendi).toBe(1);
    });
  });
});
KODSON
echo "  ✓ src/ai/rag.service.spec.ts"

cat > "src/ai/sql-komlekci.service.spec.ts" <<'KODSON'
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { BadRequestException } from '@nestjs/common';
import { SqlKomlekciService, reseptSiyahisi } from './sql-komlekci.service.js';

function saxtaPrisma() {
  return { $queryRawUnsafe: vi.fn().mockResolvedValue([{ test: 1 }]) } as any;
}

describe('SqlKomlekciService', () => {
  let prisma: any;
  let svc: SqlKomlekciService;

  beforeEach(() => {
    prisma = saxtaPrisma();
    svc = new SqlKomlekciService(prisma);
  });

  // ── RESEPT SECIMI ──
  describe('reseptSec()', () => {
    const hallar: [string, string][] = [
      ['Neçə əməkdaş var?', 'emekdas_sayi'],
      ['Ən çox maaş alan kimdir?', 'en_cox_maas'],
      ['Mərkəzlər üzrə bölgü ver', 'merkez_uzre'],
      ['Əmək haqqı fondu nə qədərdir?', 'maas_fondu'],
      ['Elmi layihələri göstər', 'layiheler'],
      ['Büdcə nə qədərdir?', 'budce'],
      ['Təlim qrupları hansılardır?', 'təlim_qruplari' === 'telim_qruplari' ? 'telim_qruplari' : 'telim_qruplari'],
      ['Sertifikasiya nəticələri', 'sertifikasiya'],
      ['Son əmrləri göstər', 'son_emrler'],
      ['Logistika aktivləri', 'logistika'],
    ];

    for (const [sual, gozlenilen] of hallar) {
      it(`"${sual}" -> ${gozlenilen}`, () => {
        expect(svc.reseptSec(sual)?.ad).toBe(gozlenilen);
      });
    }

    it('namelum sual ucun null qaytarir', () => {
      expect(svc.reseptSec('Sabah hava necə olacaq?')).toBeNull();
    });

    it('boyuk/kiçik herf ferqi yoxdur', () => {
      expect(svc.reseptSec('NEÇƏ ƏMƏKDAŞ VAR')?.ad).toBe('emekdas_sayi');
    });
  });

  // ── ICRA ──
  describe('icraEt()', () => {
    it('duzgun netice strukturu qaytarir', async () => {
      const n = await svc.icraEt('Neçə əməkdaş var?', 10);

      expect(n).toMatchObject({
        resept: 'emekdas_sayi',
        setirSayi: 1,
      });
      expect(n.sql).toBeTypeOf('string');
      expect(n.icra_ms).toBeGreaterThanOrEqual(0);
    });

    it('namelum sual ucun BadRequestException atir', async () => {
      await expect(svc.icraEt('Sabah hava necə olacaq?'))
        .rejects.toThrow(BadRequestException);
    });

    it('xeta mesajinda movcud reseptleri gosterir', async () => {
      await expect(svc.icraEt('namelum sual')).rejects.toThrow(/emekdas_sayi/);
    });

    it('parametrli reseptlere LIMIT oтурur', async () => {
      await svc.icraEt('Ən çox maaş alan 5 nəfər', 5);

      const cagiris = prisma.$queryRawUnsafe.mock.calls[0];
      expect(cagiris[1]).toBe(5);          // limit parametri
    });

    it('parametrsiz resepte LIMIT vermir', async () => {
      await svc.icraEt('Neçə əməkdaş var?', 10);

      const cagiris = prisma.$queryRawUnsafe.mock.calls[0];
      expect(cagiris).toHaveLength(1);     // yalniz SQL
    });
  });

  // ── TEHLUKESIZLIK ──
  describe('TEHLUKESIZLIK — SQL injection', () => {
    it('butun SQL-ler YALNIZ SELECT ile baslayir', () => {
      const siyahi = reseptSiyahisi();
      expect(siyahi.length).toBeGreaterThan(0);

      // Her reseptin SQL-ini yoxla
      for (const r of siyahi) {
        const netice = svc.reseptSec(r.ad);
        expect(netice).not.toBeNull();
        const sql = netice!.sql.trim().toUpperCase();
        expect(sql.startsWith('SELECT')).toBe(true);
      }
    });

    it('TEHLUKELI SQL ifadeleri YOXDUR', () => {
      const qadagan = ['DELETE', 'DROP', 'TRUNCATE', 'UPDATE', 'INSERT', 'ALTER', 'GRANT'];

      for (const r of reseptSiyahisi()) {
        const sql = svc.reseptSec(r.ad)!.sql.toUpperCase();
        for (const q of qadagan) {
          expect(sql).not.toContain(` ${q} `);
        }
      }
    });

    it('istifadeci metni SQL-e BIRBASA yazilmir', async () => {
      const hucum = "'; DROP TABLE kadrlar.emekdaslar--";
      // Hucum metni resept secmir -> xeta
      await expect(svc.icraEt(hucum)).rejects.toThrow(BadRequestException);
    });

    it('AI yalniz MOVCUD reseptlerden birini sece BILER', () => {
      const adlar = reseptSiyahisi().map((r) => r.ad);
      expect(adlar).toContain('emekdas_sayi');
      // Resept adlari sabitdir — AI yeni resept yarada bilmez
      expect(adlar.length).toBe(10);
    });
  });
});
KODSON
echo "  ✓ src/ai/sql-komlekci.service.spec.ts"

cat > "test/backend4.e2e-spec.ts" <<'KODSON'
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import request from 'supertest';
import { App } from 'supertest/types';
import { AppModule } from '../src/app.module.js';
import { AllExceptionsFilter } from '../src/common/filters/all-exceptions.filter.js';

/**
 * BACKEND-4 e2e: AI qatı, RAG, tebii dil -> SQL, Excel ixracı.
 */
describe('Backend-4 (e2e)', () => {
  let app: INestApplication<App>;
  let token = '';
  let baxiciToken = '';

  /*
   * supertest-de .set() YALNIZ verb-den SONRA cagirila bilir:
   *   request(server).set(...)          -> TypeError: set is not a function
   *   request(server).get(url).set(...) -> DOGRU
   *
   * Ona gore verb metodlarini sarib tokeni OZUDE elave eden komekci yaziriq.
   */
  type Verb = 'get' | 'post' | 'patch' | 'put' | 'delete';

  const agent = (tokenAl?: () => string) => {
    const a = request(app.getHttpServer());
    const netice = {} as Record<Verb, (yol: string) => request.Test>;
    for (const m of ['get', 'post', 'patch', 'put', 'delete'] as Verb[]) {
      netice[m] = (yol: string) => {
        const sorqu = a[m](yol);
        const t = tokenAl?.();
        return t ? sorqu.set('Authorization', `Bearer ${t}`) : sorqu;
      };
    }
    return netice;
  };

  const api = () => agent(() => token);
  const baxici = () => agent(() => baxiciToken);
  const publicApi = () => agent();

  /*
   * IKLİ (binary) fayl ucun komekci.
   *
   * supertest susmaya gore yalniz tanidigi tipleri buffer edir.
   * XLSX ucun content-type qeyri-adi oldugu ucun body BOS gelir.
   * Ona gore buffer(true) + oz parser-imizi veririk.
   */
  const ikili = (yol: string) =>
    api()
      .get(yol)
      .buffer(true)
      .parse((cavab, geriCagiris) => {
        const parcalar: Buffer[] = [];
        cavab.on('data', (p: Buffer) => parcalar.push(p));
        cavab.on('end', () => geriCagiris(null, Buffer.concat(parcalar)));
      });

  beforeAll(async () => {
    const modul: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = modul.createNestApplication();
    app.setGlobalPrefix('api/v1');
    app.useGlobalPipes(
      new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }),
    );
    app.useGlobalFilters(new AllExceptionsFilter());
    await app.init();

    for (const [rol, hedef] of [['admin', 'token'], ['baxici', 'baxiciToken']] as const) {
      const c = await publicApi()
        .post('/api/v1/auth/login')
        .send({ email: `${rol}@arti.edu.az`, parol: '123456' });
      if (hedef === 'token') token = c.body.token;
      else baxiciToken = c.body.token;
    }
  });

  afterAll(async () => {
    // Test zamani yaranan AI sorgularini temizle
    const pool = new (await import('pg')).Pool({
      connectionString: process.env.DATABASE_URL,
    });
    await pool.query("DELETE FROM ai.ai_sorghular WHERE istifadeci = 'admin@arti.edu.az' AND vaxt > now() - interval '1 hour'");
    await pool.end();
    await app.close();
  });

  const url = (y: string) => `/api/v1${y}`;

  // ── AI ──
  describe('GET /ai/statistika', () => {
    it('AI statistikasini qaytarir', async () => {
      const c = await api().get(url('/ai/statistika')).expect(200);
      expect(c.body).toHaveProperty('cem');
      expect(c.body).toHaveProperty('embedding_sayi');
      expect(typeof c.body.api_hazir).toBe('boolean');
    });
  });

  describe('GET /ai/promptlar', () => {
    it('prompt sablonlarini qaytarir', async () => {
      const c = await api().get(url('/ai/promptlar')).expect(200);
      expect(Array.isArray(c.body)).toBe(true);
      expect(c.body.length).toBeGreaterThan(0);
      expect(c.body[0]).toHaveProperty('prompt_metni');
    });
  });

  describe('POST /ai/sorush', () => {
    it('demo rejimde cavab qaytarir', async () => {
      const c = await api()
        .post(url('/ai/sorush'))
        .send({ sual: 'ARTİ-də neçə əməkdaş var?' })
        .expect(201);

      expect(c.body).toHaveProperty('cavab');
      expect(c.body.menbe).toBeTypeOf('string');
      expect(c.body.gecikme_ms).toBeGreaterThanOrEqual(0);
    });

    it('qisa sual 400 verir', () =>
      api().post(url('/ai/sorush')).send({ sual: 'ab' }).expect(400));

    it('bos sual 400 verir', () =>
      api().post(url('/ai/sorush')).send({}).expect(400));

    it('kontekst=true ile RAG isledilir', async () => {
      const c = await api()
        .post(url('/ai/sorush'))
        .send({ sual: 'kurikulum islahatı', kontekst: true })
        .expect(201);

      expect(Array.isArray(c.body.kontekst)).toBe(true);
    });
  });

  describe('GET /ai/tarixce', () => {
    it('admin tarixceye baxa bilir', () =>
      api().get(url('/ai/tarixce?limit=5')).expect(200));

    it('baxici baxa BILMIR (403)', () =>
      baxici().get(url('/ai/tarixce')).expect(403));
  });

  // ── RAG ──
  describe('RAG', () => {
    it('POST /ai/indeksle vektorlashdirir', async () => {
      const c = await api().post(url('/ai/indeksle')).expect(201);
      expect(c.body.indekslendi).toBeGreaterThan(0);
    });

    it('GET /ai/oxsar oxsar senedleri tapir', async () => {
      const c = await api()
        .get(url('/ai/oxsar?sual=kurikulum&limit=3'))
        .expect(200);

      expect(Array.isArray(c.body)).toBe(true);
      expect(c.body.length).toBeGreaterThan(0);
      expect(c.body[0]).toHaveProperty('oxsarliq');
      expect(c.body[0].oxsarliq).toBeGreaterThan(0);
    });

    it('oxsarliq bali azalan sira ile gelir', async () => {
      const c = await api().get(url('/ai/oxsar?sual=tehsil&limit=5')).expect(200);
      const ballar = c.body.map((r: { oxsarliq: number }) => r.oxsarliq);
      const siralanmis = [...ballar].sort((a, b) => b - a);
      expect(ballar).toEqual(siralanmis);
    });

    it('baxici indeksleye BILMIR (403)', () =>
      baxici().post(url('/ai/indeksle')).expect(403));
  });

  // ── TƏBİİ DİL -> SQL ──
  describe('POST /ai/sql', () => {
    it('resept siyahisini qaytarir', async () => {
      const c = await api().get(url('/ai/reseptler')).expect(200);
      expect(c.body.length).toBe(10);
    });

    const hallar: [string, string][] = [
      ['Neçə əməkdaş var?', 'emekdas_sayi'],
      ['Ən çox maaş alan 3 nəfər', 'en_cox_maas'],
      ['Mərkəzlər üzrə bölgü', 'merkez_uzre'],
      ['Büdcə nə qədərdir', 'budce'],
      ['Təlim qrupları göstər', 'telim_qruplari'],
    ];

    for (const [sual, gozlenilen] of hallar) {
      it(`"${sual}" -> ${gozlenilen}`, async () => {
        const c = await api()
          .post(url('/ai/sql'))
          .send({ sual, limit: 3 })
          .expect(201);
        expect(c.body.resept).toBe(gozlenilen);
        expect(Array.isArray(c.body.setirler)).toBe(true);
      });
    }

    it('namelum sual 400 verir', async () => {
      const c = await api()
        .post(url('/ai/sql'))
        .send({ sual: 'Sabah hava necə olacaq?' })
        .expect(400);
      expect(c.body.xeta.kod).toBe('YANLIS_SORGU');
    });

    it('limit maksimum 100', () =>
      api().post(url('/ai/sql'))
        .send({ sual: 'Neçə əməkdaş var', limit: 500 })
        .expect(400));

    it('SQL injection cehdi bloklanir', async () => {
      await api()
        .post(url('/ai/sql'))
        .send({ sual: "'; DROP TABLE kadrlar.emekdaslar--" })
        .expect(400);
    });

    it('cavabda SQL gosterilir (seffaflıq)', async () => {
      const c = await api()
        .post(url('/ai/sql'))
        .send({ sual: 'Neçə əməkdaş var?' })
        .expect(201);

      expect(c.body.sql.trim().toUpperCase().startsWith('SELECT')).toBe(true);
      expect(c.body.sql.toUpperCase()).not.toContain('DELETE');
    });
  });

  // ── İXRAC ──
  describe('İxrac', () => {
    it('emekdaslar.xlsx yuklenir', async () => {
      const c = await ikili(url('/ixrac/emekdaslar.xlsx')).expect(200);
      expect(Buffer.isBuffer(c.body)).toBe(true);
      expect(c.headers['content-type']).toContain('spreadsheetml');
      expect(c.headers['content-disposition']).toContain('emekdaslar.xlsx');
      expect(c.body.length).toBeGreaterThan(1000);
      // XLSX ZIP faylidir — ilk 2 bayt 'PK'
      expect(c.body[0]).toBe(0x50);
      expect(c.body[1]).toBe(0x4b);
    });

    it('budce.xlsx admin ucun isleyir', async () => {
      const c = await ikili(url('/ixrac/budce.xlsx')).expect(200);
      expect(Buffer.isBuffer(c.body)).toBe(true);
      expect(c.body[0]).toBe(0x50);
    });

    it('budce.xlsx baxici ucun 403', () =>
      baxici().get(url('/ixrac/budce.xlsx')).expect(403));

    it('hesabat.html qaytarir', async () => {
      const c = await api().get(url('/ixrac/hesabat.html')).expect(200);
      expect(c.headers['content-type']).toContain('text/html');
      expect(c.text).toContain('ARTİ');
      expect(c.text).toContain('<table>');
    });

    it('ixrac tokensiz islemir', () =>
      publicApi().get(url('/ixrac/emekdaslar.xlsx')).expect(401));
  });

  // ── XƏTA FORMATI ──
  describe('Xeta formatlari', () => {
    it('AI xetasi vahid formatdadir', async () => {
      const c = await api()
        .post(url('/ai/sql')).send({ sual: 'namelum sual bu' }).expect(400);
      expect(c.body).toMatchObject({ ugur: false, xeta: { kod: 'YANLIS_SORGU' } });
    });
  });
});
KODSON
echo "  ✓ test/backend4.e2e-spec.ts"

echo "════ 5/6  Docker init + app.module ════"
mkdir -p prisma/init
[ -f ~/Deepseek_ARTI/DS_Baza/sql/00_TAM_DDL.sql ] && cp ~/Deepseek_ARTI/DS_Baza/sql/00_TAM_DDL.sql prisma/init/01_struktur.sql && echo "  ✓ prisma/init/01_struktur.sql"
python3 - <<'PYEOF'
from pathlib import Path
p = Path('src/app.module.ts')
s = p.read_text()
if 'AiModule' not in s:
    s = s.replace("import { HesabatlarModule } from './hesabatlar/hesabatlar.module.js';",
                  "import { HesabatlarModule } from './hesabatlar/hesabatlar.module.js';\n"
                  "import { AiModule } from './ai/ai.module.js';\n"
                  "import { IxracModule } from './ixrac/ixrac.module.js';")
    s = s.replace('    HesabatlarModule,\n', '    HesabatlarModule,\n    AiModule,\n    IxracModule,\n')
    p.write_text(s); print('  ✓ AiModule + IxracModule')
else: print('  = modullar movcuddur')
PYEOF

echo "════ 6/6  Yoxlama ════"
chmod +x scripts/ehtiyat.sh
npm run build
echo ""; echo "HAZIR"
