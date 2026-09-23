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
const a = s.vektor('Elmi Şura protokolu haqqında sənəd');
const b = s.vektor('Elmi Şura protokolu haqqında sənəd');
const uzunluq = Math.sqrt(a.reduce((c: number, x: number) => c + x * x, 0));

console.log('vektorun uzunluğu  :', uzunluq.toFixed(6), '(≈ 1.0 olmalıdır)');
console.log('özü ilə kosinus    :', s.kosinus(a, b).toFixed(6), '(1.0-a çox yaxın)');
console.log();
console.log('⚠️ Normallaşdırma olmasaydı:');
const xam = a.map((x: number) => x * 10);
const xamUzunluq = Math.sqrt(xam.reduce((c: number, x: number) => c + x * x, 0));
console.log('  uzunluq        :', xamUzunluq.toFixed(4));
console.log('  kosinus        :', (xam.reduce((c: number, x: number, i: number) => c + x * xam[i]!, 0)).toFixed(4), '← 1-dən BÖYÜK!');
"
)
