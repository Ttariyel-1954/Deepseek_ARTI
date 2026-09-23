LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

echo "── PrismaService faylı ──"
ls -l src/prisma/prisma.service.ts | sed 's/^/  /'

echo
echo "── Baza bağlantısını BİRBAŞA sınayırıq ──"
npx tsx -e "
import 'dotenv/config';
import { PrismaService } from './src/prisma/prisma.service.ts';
void (async () => {
  const s = new PrismaService({ get: () => process.env.DATABASE_URL } as never);
  await s.onModuleInit();
  const n = await s.yoxla();
  console.log('  qoşulub     :', n.qosulub);
  console.log('  cədvəl sayı :', n.cedvelSayi);
  console.log('  gecikmə     :', n.gecikmeMs, 'ms');
  await s.onModuleDestroy();
  console.log('  bağlantı düzgün bağlandı');
})();
"

echo
echo "── Adapter istifadə olunurmu? ──"
grep -nE 'PrismaPg|adapter|connectionString' src/prisma/prisma.service.ts | sed 's/^/  /'
)
