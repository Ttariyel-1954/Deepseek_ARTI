LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

npx tsx -e "
import { sehifelenmis } from './src/common/dto/sehife.dto.ts';
const cedvel = [[[], 0, 1, 20], [[], 10, 1, 3], [[], 21, 1, 20], [[], 100, 1, 20]] as const;
for (const [s, c, sh, l] of cedvel) {
  const n = sehifelenmis(s as never[], c, sh, l);
  console.log('cemi=' + c + ' limit=' + l + ' → sehife_sayi =', n.sehife_sayi);
}
"
)
