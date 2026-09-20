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
