LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

echo "── Modulun hissələri ──"
ls -1 src/saglamliq/ | sed 's/^/  /'

echo
echo "── Endpoint-lər ──"
grep -nE '@(Get|Post|Controller)' src/saglamliq/saglamliq.controller.ts | sed 's/^/  /'

echo
echo "── Kök modula qoşulubmu? ──"
grep -c 'SaglamliqModule' src/app.module.ts 2>/dev/null | sed 's/^/  sayı: /'

echo
echo "── Sağlamlıq yoxlaması (birbaşa) ──"
npx tsx -e "
import 'dotenv/config';
import { PrismaService } from './src/prisma/prisma.service.ts';
import { SaglamliqService } from './src/saglamliq/saglamliq.service.ts';
void (async () => {
  const p = new PrismaService({ get: () => process.env.DATABASE_URL } as never);
  await p.onModuleInit();
  const c = await new SaglamliqService(p).yoxla();
  console.log('  status      :', c.status);
  console.log('  qoşulub     :', c.baza.qosulub);
  console.log('  cədvəl sayı :', c.baza.cedvel_sayi);
  console.log('  gecikmə     :', c.baza.gecikme_ms, 'ms');
  console.log('  versiya     :', c.versiya);
  await p.onModuleDestroy();
})();
"
)
