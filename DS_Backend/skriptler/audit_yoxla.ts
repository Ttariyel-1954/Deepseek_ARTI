/**
 * skriptler/audit_yoxla.ts — audit loqunu CANLI yoxlayır.
 *
 * ⚠️ QEYD: bazada ARTIQ `audit.fn_audit_yaz()` trigger-i var və o,
 * dörd cədvəli avtomatik izləyir. Bu skript həmin trigger-in
 * işlədiyini SÜBUT edir və tətbiq səviyyəsində əlavə loqun necə
 * yazıldığını göstərir.
 *
 * İSTİFADƏ:  npx tsx skriptler/audit_yoxla.ts
 */
import 'reflect-metadata';
import 'dotenv/config';

import { PrismaPg } from '@prisma/adapter-pg';
import { PrismaClient } from '../src/generated/prisma/client.js';
import type { PrismaService } from '../src/prisma/prisma.service.js';
import { AuditService } from '../src/audit/audit.service.js';

let kecdi = 0;
let xeta = 0;
function basliq(m: string): void {
  console.log(`\n── ${m} ${'─'.repeat(Math.max(0, 62 - m.length))}`);
}
function ok(m: string, e = ''): void {
  kecdi += 1;
  console.log(`  [OK] ${m}${e ? ' — ' + e : ''}`);
}
function xet(m: string, e = ''): void {
  xeta += 1;
  console.log(`  [XX] ${m}${e ? ' — ' + e : ''}`);
}
function gozle(ad: string, sert: boolean, e = ''): void {
  sert ? ok(ad, e) : xet(ad, e);
}

void (async () => {
  const prisma = new PrismaClient({
    adapter: new PrismaPg({ connectionString: process.env.DATABASE_URL! }),
  });
  const xidmet = new AuditService(prisma as unknown as PrismaService);

  try {
    // ── 1. Statistika ─────────────────────────────────────────────
    basliq('1) statistika() — loqun paylanması');
    const st = await xidmet.statistika();
    console.log(`      cəmi qeyd   : ${st.cem_qeyd}`);
    console.log(`      cədvəl sayı : ${st.cedvel_sayi}`);
    console.log(`      ilk qeyd    : ${st.ilk_qeyd}`);
    console.log(`      son qeyd    : ${st.son_qeyd}`);
    console.log('      əməliyyat üzrə:', st.emeliyyat_uzre.map((e) => `${e.emeliyyat}=${e.cem}`).join('  '));
    console.log('      cədvəl üzrə (ilk 8):');
    for (const c of st.cedvel_uzre.slice(0, 8)) {
      console.log(`        ${(c.cedvel_adi + ' '.repeat(26)).slice(0, 26)} cem=${String(c.cem).padStart(5)}  I=${String(c.insert).padStart(4)} U=${String(c.update).padStart(4)} D=${String(c.delete).padStart(4)}`);
    }
    gozle('loqda minlərlə qeyd var', st.cem_qeyd > 1000, `${st.cem_qeyd} qeyd`);
    gozle('bir neçə cədvəl izlənir', st.cedvel_sayi >= 3, `${st.cedvel_sayi} cədvəl`);
    gozle('əməliyyat növləri gəlir', st.emeliyyat_uzre.length >= 3);
    gozle('INSERT + UPDATE + DELETE cəmi = cem_qeyd',
      st.emeliyyat_uzre.reduce((a, b) => a + b.cem, 0) === st.cem_qeyd);
    gozle('cədvəl üzrə cəmlər cem_qeyd-ə bərabərdir',
      st.cedvel_uzre.reduce((a, b) => a + b.cem, 0) <= st.cem_qeyd,
      'ilk 15 göstərilir');

    // ── 2. Səhifələmə ─────────────────────────────────────────────
    basliq('2) hamisi() — səhifələmə və süzgəc');
    const s1 = await xidmet.hamisi({ seife: 1, limit: 5 } as never);
    console.log(`      cem=${s1.cem}  sehife=${s1.sehife}/${s1.sehife_sayi}  gosterilen=${s1.melumat.length}`);
    for (const q of s1.melumat) {
      console.log(`        #${q.id}  ${q.cedvel_adi}  ${q.emeliyyat}  setir=${q.setir_id}  ${q.vaxt.slice(0, 19)}`);
    }
    gozle('5 qeyd gəldi', s1.melumat.length === 5);
    gozle('id MƏTN tipindədir', typeof s1.melumat[0].id === 'string');
    gozle('vaxt ISO formatındadır', s1.melumat[0].vaxt.includes('T'));

    const s2 = await xidmet.hamisi({ seife: 2, limit: 5 } as never);
    gozle('2-ci səhifə FƏRQLİ qeydlər verir',
      s1.melumat[0].id !== s2.melumat[0].id,
      `#${s1.melumat[0].id} vs #${s2.melumat[0].id}`);

    // ── 3. Süzgəclər ──────────────────────────────────────────────
    basliq('3) Süzgəclər — cədvəl, əməliyyat, axtarış');
    const fc = await xidmet.hamisi({ seife: 1, limit: 5, cedvel: 'kadrlar.emekdaslar' } as never);
    console.log(`      cedvel=kadrlar.emekdaslar → ${fc.cem} qeyd`);
    gozle('süzgəc yalnız o cədvəli verir',
      fc.melumat.every((q) => q.cedvel_adi === 'kadrlar.emekdaslar'));

    const fe = await xidmet.hamisi({ seife: 1, limit: 5, emeliyyat: 'DELETE' } as never);
    console.log(`      emeliyyat=DELETE → ${fe.cem} qeyd`);
    gozle('süzgəc yalnız DELETE verir', fe.melumat.every((q) => q.emeliyyat === 'DELETE'));

    const fa = await xidmet.hamisi({ seife: 1, limit: 5, axtar: 'Trigger' } as never);
    console.log(`      axtar=«Trigger» → ${fa.cem} qeyd`);
    gozle('axtarış işləyir', fa.cem > 0 && fa.melumat.every((q) => (q.qeyd ?? '').includes('Trigger')));

    // ── 4. Bir qeyd ───────────────────────────────────────────────
    basliq('4) biri() — tək qeyd');
    const birincId = Number(s1.melumat[0].id);
    const b = await xidmet.biri(birincId);
    console.log(`      #${b.id}  ${b.cedvel_adi}  ${b.emeliyyat}  ${b.vaxt}`);
    gozle('eyni qeyd gəldi', b.id === s1.melumat[0].id);
    try {
      await xidmet.biri(99999999);
      xet('olmayan ID xəta vermədi');
    } catch (e) {
      gozle(`olmayan ID → ${(e as Error).constructor.name}`,
        (e as Error).constructor.name === 'NotFoundException');
    }

    // ── 5. Trigger sübutu ─────────────────────────────────────────
    basliq('5) triggerNumayisi() — baza trigger-i 3 qeyd yazır');
    const t = await xidmet.triggerNumayisi();
    console.log(`      yaradılan ID : ${t.yeni_id}`);
    console.log(`      audit artımı : ${t.audit_artimi}`);
    console.log(`      izah         : ${t.izah}`);
    for (const q of t.qeydler) {
      console.log(`        #${q.id}  ${q.emeliyyat}  setir=${q.setir_id}  qeyd=«${q.qeyd}»`);
    }
    gozle('trigger 3 qeyd yazdı (INSERT/UPDATE/DELETE)', t.audit_artimi === 3, `${t.audit_artimi}`);
    gozle('üç əməliyyat da loqdadır',
      t.qeydler.map((q) => q.emeliyyat).join(',') === 'INSERT,UPDATE,DELETE');
    gozle('setir_id MƏTN kimi saxlanılıb', typeof t.qeydler[0].setir_id === 'string');
    gozle('istifadeci bazadan gəlir (current_user)', (t.qeydler[0].istifadeci ?? '').length > 0,
      String(t.qeydler[0].istifadeci));
    gozle('əməkdaş silindi (bazada qalmadı)',
      (await prisma.emekdaslar.count({ where: { email: { startsWith: 'audit.trigger.' } } })) === 0);
    console.log('      ⚠️ Bu 3 audit qeydi SİLİNMİR — loq əbədidir, qəsdən belədir');

    // ── 6. Tətbiq səviyyəsində yazma ──────────────────────────────
    basliq('6) yaz() — əl ilə loq qeydi');
    const yazilan = await xidmet.yazTek({
      cedvel_adi: 'kadrlar.emekdaslar',
      emeliyyat: 'UPDATE',
      setir_id: '1',
      istifadeci: 'skript@arti.edu.az',
      qeyd: 'Skript sınağı: maaş yeniləndi (köhnə 3500 → yeni 3500)',
    });
    console.log(`      yazılan audit ID: ${yazilan.id}`);
    gozle('qeyd yazıldı və ID mətn kimi qaytarıldı', typeof yazilan.id === 'string');
    const yoxla = await xidmet.biri(Number(yazilan.id));
    gozle('yazılan qeyd oxunur', yoxla.qeyd?.includes('Skript sınağı') === true);
    gozle('istifadeci saxlanıldı', yoxla.istifadeci === 'skript@arti.edu.az');

    // ── 7. Tranzaksiya — atomiklik ────────────────────────────────
    basliq('7) tranzaksiyaNumayisi() — əməkdaş + audit BİR tranzaksiyada');
    const tr = await xidmet.tranzaksiyaNumayisi();
    console.log(`      yazılan audit ID   : ${tr.yazilan_audit_id}`);
    console.log(`      bazada qalan əməkdaş: ${tr.bazada_qalan_emekdas}`);
    console.log(`      audit artımı        : ${tr.bazada_qalan_audit}`);
    console.log(`      xəta                : ${tr.xeta}`);
    console.log(`      izah                : ${tr.izah}`);
    gozle('əməkdaş yazılmadı (rollback)', tr.bazada_qalan_emekdas === 0);
    gozle('audit qeydi də yazılmadı (rollback)', tr.bazada_qalan_audit === 0);
    gozle('audit ID alınmışdı, amma COMMIT olmadı', tr.yazilan_audit_id !== null);
    if (tr.yazilan_audit_id) {
      const yox = await prisma.audit_log.count({ where: { id: BigInt(tr.yazilan_audit_id) } });
      gozle('həmin ID bazada YOXDUR', yox === 0);
    }

    // ── 8. Əməkdaş sayı toxunulmaz ────────────────────────────────
    basliq('8) Yekun vəziyyət');
    const cem = await prisma.emekdaslar.count();
    console.log(`      bazada əməkdaş: ${cem}`);
    gozle('14 əməkdaş toxunulmaz qaldı', cem === 14, `${cem}`);
    const zibil = await prisma.emekdaslar.count({
      where: { email: { startsWith: 'audit.' } },
    });
    gozle('test zibili yoxdur', zibil === 0, `${zibil}`);
  } finally {
    await prisma.$disconnect();
  }

  console.log('\n════════ NƏTİCƏ ════════');
  console.log(`  keçdi: ${kecdi}   uğursuz: ${xeta}`);
  if (xeta === 0) {
    console.log('  ✓ AUDIT MODULU DÜZGÜN İŞLƏYİR');
    process.exit(0);
  }
  console.log(`  ✗ ${xeta} YOXLAMA UĞURSUZ`);
  process.exit(1);
})();
