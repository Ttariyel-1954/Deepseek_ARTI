LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}" || exit 1
unset DATABASE_URL PGHOST

echo "── .env dəyişənləri (şifrələr gizlədilir) ──"
python3 -c "
import pathlib
for x in pathlib.Path('.env').read_text().splitlines():
    if not x.strip() or x.startswith('#'):
        continue
    a, _, d = x.partition('=')
    d = d.strip('\"')
    if any(k in a for k in ('URL', 'SECRET', 'PASSWORD', 'KEY')):
        print('  %-18s %s' % (a, '•' * 20))
    else:
        print('  %-18s %s' % (a, d))
"

echo
echo "── DATABASE_URL hissələri ──"
python3 -c "
import re, pathlib
m = re.search(r'DATABASE_URL=\"([^\"]+)\"', pathlib.Path('.env').read_text())
u = m.group(1)
sxem, _, qalan = u.partition('://')
kimlik, _, host = qalan.partition('@')
ist, _, sifre = kimlik.partition(':')
host, _, baza = host.partition('/')
print('  protokol   :', sxem)
print('  istifadəçi :', ist)
print('  şifrə      :', '•' * len(sifre), '(%d simvol)' % len(sifre))
print('  host:port  :', host)
print('  baza adı   :', baza)
"

echo
echo "── .gitignore nəyi qoruyur? ──"
grep -v '^#' .gitignore | grep -v '^$' | sed 's/^/  /'

echo
echo "── Şifrə koda yazılıbmı? ──"
if grep -rn 'arti_secret' src/ --include=*.ts 2>/dev/null; then
  echo "  ✗ ŞİFRƏ KODA YAZILIB!"
else
  echo "  ✓ şifrə koda yazılmayıb — yalnız .env-dədir"
fi

echo
echo "── Kod .env-i adı ilə oxuyurmu? ──"
grep -rn "DATABASE_URL" src/prisma/prisma.service.ts | sed 's/^/  /'
)
