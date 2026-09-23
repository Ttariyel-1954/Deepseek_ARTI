LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

npx tsx -e "
import { sehifeHesabla } from './src/common/dto/sehife.dto.ts';
const cedvel = [[3,15],[1,5000],[-7,20],[1,0],[2.7,33.9]] as const;
for (const [s, l] of cedvel)
  console.log('sehife=', s, ' limit=', l, ' →', JSON.stringify(sehifeHesabla(s, l)));
"
)
