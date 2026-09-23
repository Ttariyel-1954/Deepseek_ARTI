LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

npx tsx -e "
import { EmbeddingService } from './src/ai/embedding.service.ts';
const s = new EmbeddingService({} as any);
const v = (m: string) => s.vektor(m);
const c = (x: string, y: string) => s.kosinus(v(x), v(y)).toFixed(6);

console.log('eyni mətn              :', c('elmi şura iclası', 'elmi şura iclası'));
console.log('çox oxşar mətn         :', c('elmi şura iclası protokolu', 'elmi şura iclasının protokolu'));
console.log('qismən oxşar           :', c('elmi şura iclası', 'elmi jurnal nəşri'));
console.log('tamamilə fərqli         :', c('elmi şura iclası', 'idman yarışı nəticələri'));
console.log();
console.log('ballar 0..1 aralığındadır — müqayisə mənalıdır.');
"
)
