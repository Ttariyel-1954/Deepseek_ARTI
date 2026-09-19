#!/bin/bash
# Deepseek_ARTI — sürətli vəziyyət yoxlaması
cd "$(dirname "$0")"
unset DATABASE_URL PGHOST
export PGPASSWORD=arti_secret_2025

echo "════════ Deepseek_ARTI VƏZİYYƏT ════════"
echo ""
echo "── Qovluqlar ──"
for d in DS_Baza DS_Backend DS_Frontend DS_Web DƏRSLƏR; do
  n=$(find "$d" -type f 2>/dev/null | wc -l | tr -d ' ')
  printf "  %-14s %s fayl\n" "$d" "$n"
done

echo ""
echo "── Dərslər ──"
if ls DƏRSLƏR/*.html >/dev/null 2>&1; then
  for f in DƏRSLƏR/*.html; do
    n=$(wc -l < "$f" | tr -d ' ')
    if [ "$n" -ge 1700 ]; then isare="OK  "; else isare="AZ  "; fi
    printf "  [%s] %-32s %5s setir\n" "$isare" "$(basename "$f")" "$n"
  done
else
  echo "  (hələ dərs yoxdur)"
fi

echo ""
echo "── PostgreSQL ──"
if lsof -ti :5432 >/dev/null 2>&1; then
  echo "  ✅ :5432 dinlənir"
else
  echo "  ❌ :5432 bağlıdır — brew services start postgresql@18"
fi

if psql -U arti_user -d arti_baza -tAc "SELECT 1" >/dev/null 2>&1; then
  echo "  ✅ arti_baza əlçatandır"
  psql -U arti_user -d arti_baza -tAc "
    SELECT '  sxem: '||count(DISTINCT table_schema) FROM information_schema.tables
      WHERE table_schema NOT IN ('pg_catalog','information_schema')
    UNION ALL SELECT '  cədvəl: '||count(*) FROM information_schema.tables
      WHERE table_type='BASE TABLE' AND table_schema NOT IN ('pg_catalog','information_schema')
    UNION ALL SELECT '  görünüş: '||count(*) FROM information_schema.views
      WHERE table_schema NOT IN ('pg_catalog','information_schema')
    UNION ALL SELECT '  funksiya: '||count(*) FROM pg_proc p
      JOIN pg_namespace n ON n.oid=p.pronamespace
      WHERE n.nspname NOT IN ('pg_catalog','information_schema')
    UNION ALL SELECT '  trigger: '||count(*) FROM pg_trigger t
      JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace
      WHERE NOT t.tgisinternal AND n.nspname NOT IN ('pg_catalog','information_schema')
    UNION ALL SELECT '  xarici açar: '||count(*) FROM pg_constraint
      WHERE contype='f' AND connamespace::regnamespace::text
            NOT IN ('pg_catalog','information_schema');"
else
  echo "  ❌ arti_baza əlçatan deyil"
fi

echo ""
echo "── Git ──"
if [ -d .git ]; then
  echo "  $(git log --oneline -1 2>/dev/null || echo 'commit yoxdur')"
  git status --short | head -5
else
  echo "  (git başladılmayıb)"
fi
echo ""
echo "════════ HAZIR ════════"
