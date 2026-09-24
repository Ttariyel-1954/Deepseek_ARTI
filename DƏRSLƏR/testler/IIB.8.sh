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

echo "  → 1) Audit faylları"
catmadi=0
for f in src/audit/dto/audit-sorgu.dto.ts src/audit/audit.service.ts \
         src/audit/audit.controller.ts src/audit/audit.module.ts \
         skriptler/audit_yoxla.ts; do
  if [ -f "$f" ]; then printf '      ✓ %s\n' "$f"; else printf '      ✗ %s YOXDUR\n' "$f"; catmadi=1; fi
done
[ "$catmadi" -eq 0 ] || { echo "  ✗ fayllar natamamdır — ADDIM 25-i işlədin"; exit 1; }

echo ""
echo "  → 2) Bazadaki trigger-lər (tətbiq kodundan asılı olmayaraq)"
psql "$DBURL" -c "
SELECT event_object_schema || '.' || event_object_table AS cedvel, trigger_name
  FROM information_schema.triggers
 WHERE trigger_schema NOT IN ('pg_catalog','information_schema')
 GROUP BY 1, trigger_name ORDER BY 1;" 2>/dev/null | sed 's/^/      /'
N=$(say "SELECT count(DISTINCT event_object_table) FROM information_schema.triggers WHERE trigger_schema NOT IN ('pg_catalog','information_schema') AND trigger_name LIKE '%audit%';")
printf '      audit trigger-i olan cədvəl: %s\n' "$N"
[ "$N" -ge 4 ] || { echo "  ✗ audit trigger-ləri tapılmadı"; exit 1; }
echo "      ✓ trigger-lər bazadadır (Baza dərslərindən)"

echo ""
echo "  → 3) Loqun həcmi və paylanması"
CEM=$(say "SELECT count(*) FROM audit.audit_log;")
CEDVEL=$(say "SELECT count(DISTINCT cedvel_adi) FROM audit.audit_log;")
printf '      cəmi qeyd   : %s\n' "$CEM"
printf '      cədvəl sayı : %s\n' "$CEDVEL"
[ "$CEM" -ge 1000 ] || { echo "  ✗ loq gözləniləndən kiçikdir"; exit 1; }
[ "$CEDVEL" -ge 3 ] || { echo "  ✗ ən azı 3 cədvəl gözlənilirdi"; exit 1; }
psql "$DBURL" -c "
SELECT cedvel_adi, emeliyyat, count(*) AS say FROM audit.audit_log
 GROUP BY 1,2 ORDER BY say DESC LIMIT 5;" 2>/dev/null | sed 's/^/      /'

echo ""
echo "  → 4) Sxem yoxlaması"
printf '      setir_id tipi  : %s (mətn olmalıdır!)\n' "$(say "SELECT data_type FROM information_schema.columns WHERE table_schema='audit' AND table_name='audit_log' AND column_name='setir_id';")"
[ "$(say "SELECT data_type FROM information_schema.columns WHERE table_schema='audit' AND table_name='audit_log' AND column_name='setir_id';")" = "text" ] \
  || { echo "  ✗ setir_id text deyil!"; exit 1; }
VAXT_TIP=$(say "SELECT data_type FROM information_schema.columns WHERE table_schema='audit' AND table_name='audit_log' AND column_name='vaxt';")
printf '      vaxt tipi      : %s\n' "$VAXT_TIP"
[ "$VAXT_TIP" = "timestampwithtimezone" ] \
  || { echo "  ✗ vaxt timestamptz deyil (say() boşluqları silir): $VAXT_TIP"; exit 1; }
echo "      ✓ sxem düzgündür"

echo ""
echo "  → 5) CANLI audit yoxlaması (28 yoxlama)"
EVVEL=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
npx tsx skriptler/audit_yoxla.ts
[ $? -eq 0 ] || { echo "  ✗ audit probe uğursuz oldu"; exit 1; }

echo ""
echo "  → 6) Təmizlik və yekun"
SONRA=$(say "SELECT count(*) FROM kadrlar.emekdaslar;")
ZIBIL=$(say "SELECT count(*) FROM kadrlar.emekdaslar WHERE email LIKE 'audit.%' OR email LIKE 'toplu.%';")
printf '      emekdaş: %s → %s   zibil: %s\n' "$EVVEL" "$SONRA" "$ZIBIL"
[ "$EVVEL" = "$SONRA" ] || { echo "  ✗ sətir sayı dəyişdi!"; exit 1; }
[ "$ZIBIL" = "0" ] || { echo "  ✗ test zibili qaldı"; exit 1; }
printf '      audit loqu: %s → %s (artdı — gözlənilən)\n' "$CEM" "$(say "SELECT count(*) FROM audit.audit_log;")"

echo ""
echo "  ✓ IIB.8 KEÇDİ — audit loqu və trigger düzgün işləyir"
)
