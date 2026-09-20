/**
 * İstifadəçiləri yaradır / yeniləyir.
 *
 *   npm run seed:auth
 *
 * İdempotentdir: ikinci dəfə işlətsəniz, mövcud istifadəçilərin
 * şifrəsini yeniləyir — dublikat yaratmır.
 */
import 'dotenv/config';
import * as bcrypt from 'bcryptjs';
import { Pool } from 'pg';

interface SeedIstifadeci {
  email: string;
  parol: string;
  ad_soyad: string;
  rol: 'admin' | 'muhendis' | 'maliyyeci' | 'baxici';
}

const ISTIFADECILER: SeedIstifadeci[] = [
  { email: 'admin@arti.edu.az',     parol: '123456', ad_soyad: 'Elnur Əliyev',    rol: 'admin' },
  { email: 'muhendis@arti.edu.az',  parol: '123456', ad_soyad: 'Rəşad Məmmədov',  rol: 'muhendis' },
  { email: 'maliyyeci@arti.edu.az', parol: '123456', ad_soyad: 'Tural İsmayılov', rol: 'maliyyeci' },
  { email: 'baxici@arti.edu.az',    parol: '123456', ad_soyad: 'Günel Rzayeva',   rol: 'baxici' },
];

const BCRYPT_RAUND = 10;

async function main() {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });

  console.log('════ İstifadəçilər yaradılır ════\n');

  for (const i of ISTIFADECILER) {
    const hash = await bcrypt.hash(i.parol, BCRYPT_RAUND);

    const netice = await pool.query(
      `INSERT INTO kadrlar.istifadeciler (email, parol_hash, ad_soyad, rol, aktiv)
       VALUES (lower($1), $2, $3, $4, true)
       ON CONFLICT (email) DO UPDATE
         SET parol_hash = EXCLUDED.parol_hash,
             ad_soyad   = EXCLUDED.ad_soyad,
             rol        = EXCLUDED.rol,
             aktiv      = true
       RETURNING id, email, rol`,
      [i.email, hash, i.ad_soyad, i.rol],
    );

    const s = netice.rows[0];
    console.log(`  ✓ id=${String(s.id).padStart(2)}  ${s.email.padEnd(24)} ${s.rol.padEnd(10)} şifrə: ${i.parol}`);
  }

  const cem = await pool.query('SELECT count(*)::int AS say FROM kadrlar.istifadeciler');
  console.log(`\n════ CƏMİ: ${cem.rows[0].say} istifadəçi ════`);

  await pool.end();
}

main().catch((xeta) => {
  console.error('XƏTA:', xeta.message);
  process.exit(1);
});
