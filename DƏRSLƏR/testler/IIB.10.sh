LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.
(
unset DATABASE_URL PGHOST
cd "$LAYIHE" || { echo "  ✗ Layihə qovluğu yoxdur: $LAYIHE"; exit 1; }
[ -f package.json ] || { echo "  ✗ package.json yoxdur: $(pwd)"; exit 1; }
[ -f .env ] || { echo "  ✗ .env yoxdur"; exit 1; }
DBURL=$(grep '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | sed 's/^"//; s/"$//')
[ -n "$DBURL" ] || { echo "  ✗ .env-də DATABASE_URL yoxdur"; exit 1; }
say() { psql "$DBURL" -At -c "$1" 2>/dev/null | tr -d ' '; }

[ -f skriptler/2b_yoxla.sh ] \
  || { echo "  ✗ skriptler/2b_yoxla.sh yoxdur — ADDIM 26-nı işlədin"; exit 1; }

echo "  → 1) Skriptin sintaksisi"
bash -n skriptler/2b_yoxla.sh || { echo "  ✗ bash sintaksisi səhvdir"; exit 1; }
printf '      ✓ düzgündür (%s sətir)\n' "$(wc -l < skriptler/2b_yoxla.sh | tr -d ' ')"

echo ""
echo "  → 2) Modul qrafı"
grep -q 'EmekdaslarModule' src/app.module.ts || { echo "  ✗ EmekdaslarModule qoşulmayıb!"; exit 1; }
grep -q 'AuditModule' src/app.module.ts || { echo "  ✗ AuditModule qoşulmayıb!"; exit 1; }
echo "      ✓ hər iki modul app.module.ts-dədir"
python3 - <<'PSON'
import pathlib, re
s = pathlib.Path('src/emekdaslar/emekdaslar.module.ts').read_text(encoding='utf-8')
m = re.search(r'controllers:\s*\[(.*?)\]', s, re.S)
adlar = re.findall(r'(\w+Controller)', m.group(1))
print('      controller sırası: %s' % ' → '.join(adlar))
if adlar[-1] != 'EmekdaslarController':
    raise SystemExit('✗ :id controller ƏN SONDA deyil!')
if 'StatistikaController' not in adlar[:2]:
    raise SystemExit('✗ StatistikaController əvvəldə deyil!')
print('      ✓ StatistikaController əvvəldə, EmekdaslarController axırda')
PSON
[ $? -eq 0 ] || { echo "  ✗ controller sırası səhvdir"; exit 1; }

echo ""
echo "  → 3) Bazanın vəziyyəti (əvvəl)"
EVVEL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
AUDIT_EVVEL=$(say "SELECT count(*) FROM audit.audit_log;")
printf '      emekdaş: %s   audit: %s\n' "$EVVEL" "$AUDIT_EVVEL"

echo ""
echo "  → 4) TAM 2B YOXLAMASI (48 yoxlama)"
bash skriptler/2b_yoxla.sh
CIXIS=$?
echo ""
printf '      skriptin çıxış kodu: %s\n' "$CIXIS"
[ "$CIXIS" -eq 0 ] || { echo "  ✗ 2b_yoxla.sh uğursuz oldu"; exit 1; }

echo ""
echo "  → 5) Simmetriya yoxlaması"
SONRA=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
ZIBIL=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'b%.%@arti.edu.az' OR email LIKE 'toplu.%' OR email LIKE 'audit.%' OR email LIKE 'iib%';")
AUDIT_SONRA=$(say "SELECT count(*) FROM audit.audit_log;")
printf '      emekdaş : %s → %s   zibil: %s\n' "$EVVEL" "$SONRA" "$ZIBIL"
printf '      audit   : %s → %s (+%s)\n' "$AUDIT_EVVEL" "$AUDIT_SONRA" "$((AUDIT_SONRA - AUDIT_EVVEL))"
[ "$EVVEL" = "$SONRA" ] || { echo "  ✗ sətir sayı dəyişdi!"; exit 1; }
[ "$ZIBIL" = "0" ] || { echo "  ✗ test zibili qaldı: $ZIBIL"; exit 1; }
echo "      ✓ baza toxunulmaz qaldı"
[ "$AUDIT_SONRA" -ge "$AUDIT_EVVEL" ] || { echo "  ✗ audit loqu azaldı — bu mümkün deyil"; exit 1; }
echo "      ✓ audit loqu yalnız ARTDIRILIR (append-only)"

echo ""
echo "  → 6) OPTİMALLAŞDIRMA — indeks və plan yoxlaması"
echo "      ── indekslər ──"
IDX=$(say "SELECT count(*) FROM pg_indexes WHERE schemaname='kadrlar' AND tablename='emekdaslar';")
printf '      emekdaslar üzrə indeks sayı: %s\n' "$IDX"
[ "$IDX" -ge 4 ] || { echo "  ✗ indekslər azdır"; exit 1; }
say "SELECT indexname FROM pg_indexes WHERE schemaname='kadrlar' AND tablename='emekdaslar';" | sed 's/^/        /'

echo "      ── EXPLAIN ANALYZE: audit_log ──"
for sorqu in \
  "SELECT count(*) FROM audit.audit_log WHERE cedvel_adi = 'kadrlar.emekdaslar'" \
  "SELECT count(*) FROM audit.audit_log WHERE istifadeci = 'arti_user'" \
  "SELECT id, soyad FROM kadrlar.emekdaslar ORDER BY soyad LIMIT 5"; do
  printf '        %s\n' "$sorqu"
  psql "$DBURL" -c "EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF, SUMMARY OFF) $sorqu" 2>/dev/null \
    | grep -E 'Scan|Rows Removed' | sed 's/^/          /'
done
echo "      ✓ indeks işlədilən və işlədilməyən hallar görüldü"
echo "        (indeksin OLMASI onun İŞLƏDİLƏCƏYİ demək deyil — planner qərar verir)"

echo ""
echo "  → 7) YEKUN: bütün yoxlama alətləri bir yerdə"
printf '      a) tip yoxlaması      : '
npx tsc --noEmit && echo "✓ təmiz"
printf '      b) DTO matrisi (2A)   : '
npx tsx skriptler/dto_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      c) mapper (2A)        : '
npx tsx skriptler/mapper_yoxla.ts 2>&1 | grep -c 'JSON.stringify İŞLƏDİ' >/dev/null && echo "✓ işləyir"
printf '      d) servis (2A)        : '
npx tsx skriptler/servis_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      e) statistika (2B)    : '
npx tsx skriptler/statistika_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      f) əlaqələr (2B)      : '
npx tsx skriptler/elaqeler_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      g) toplu (2B)         : '
npx tsx skriptler/toplu_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'
printf '      h) audit (2B)         : '
npx tsx skriptler/audit_yoxla.ts 2>&1 | grep 'keçdi:' | sed 's/^ *//'

echo ""
echo "  → 8) Son vəziyyət"
TOTAL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
CEDVEL=$(say "SELECT count(*) FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog','information_schema');")
FAYL=$(find src -name '*.ts' | wc -l | tr -d ' ')
SKRIPT=$(ls -1 skriptler/ | wc -l | tr -d ' ')
printf '      bazada əməkdaş : %s\n' "$TOTAL"
printf '      bazada cədvəl  : %s\n' "$CEDVEL"
printf '      TypeScript     : %s fayl\n' "$FAYL"
printf '      yoxlama aləti  : %s\n' "$SKRIPT"
[ "$TOTAL" = "14" ] || { echo "  ✗ baza vəziyyəti dəyişdi: $TOTAL"; exit 1; }

echo ""
echo "  ✓ IIB.10 KEÇDİ — Dərs 2B-nin bütün nəticələri təsdiqləndi"
)
