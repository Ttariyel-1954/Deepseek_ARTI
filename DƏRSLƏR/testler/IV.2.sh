LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export npm_config_cache=/tmp/npmcache

npx tsx -e "
import { EmbeddingService, OLCU } from './src/ai/embedding.service.ts';
const s = new EmbeddingService({} as any);
const a = s.vektor('Elmi Şura protokolu');
const b = s.vektor('Elmi Şura protokolu');
const c = s.vektor('idman yarışı');

console.log('OLCU sabiti        :', OLCU);
console.log('vektorun ölçüsü    :', a.length);
console.log('deterministik      :', JSON.stringify(a) === JSON.stringify(b));
console.log('fərqli mətn fərqli  :', JSON.stringify(a) !== JSON.stringify(c));
console.log();
console.log('vektorun ilk 8 elementi:');
console.log('  ', a.slice(0, 8).map((x: number) => x.toFixed(4)).join('  '));
console.log('sıfırdan fərqli element sayı:', a.filter((x: number) => x !== 0).length);
"
)
