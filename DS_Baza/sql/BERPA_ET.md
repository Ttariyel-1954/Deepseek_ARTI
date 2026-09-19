# Bazanın bərpası — `arti_baza`

Repo-da bazanın **tam bərpası** üçün iki fayl var:

| Fayl | Nə saxlayır |
|---|---|
| `00_TAM_DDL.sql` | Struktur: 12 sxem, 48 cədvəl, 8 view, 10 funksiya, 5 trigger, 35 xarici açar |
| `20_veriler.sql` | Məlumat: 48 cədvəlin bütün sətirləri (INSERT formatında) |

## 1. Rol və baza yarat

```bash
unset DATABASE_URL PGHOST

psql -U postgres -c "CREATE ROLE arti_user WITH LOGIN PASSWORD 'arti_secret_2025';"
psql -U postgres -c "CREATE DATABASE arti_baza OWNER arti_user;"
```

## 2. Strukturu yüklə

```bash
export PGPASSWORD=arti_secret_2025
psql -U arti_user -d arti_baza -f DS_Baza/sql/00_TAM_DDL.sql
```

## 3. Məlumatı yüklə

```bash
psql -U arti_user -d arti_baza -f DS_Baza/sql/20_veriler.sql
```

## 4. Yoxla

```bash
psql -U arti_user -d arti_baza -c "
SELECT 'sxem' AS nov, count(DISTINCT table_schema)::text AS say
  FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog','information_schema')
UNION ALL SELECT 'cədvəl', count(*)::text FROM information_schema.tables
  WHERE table_type='BASE TABLE' AND table_schema NOT IN ('pg_catalog','information_schema')
UNION ALL SELECT 'view', count(*)::text FROM information_schema.views
  WHERE table_schema NOT IN ('pg_catalog','information_schema')
UNION ALL SELECT 'trigger', count(*)::text FROM pg_trigger t
  JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace
  WHERE NOT t.tgisinternal AND n.nspname NOT IN ('pg_catalog','information_schema');"
```

**Gözlənilən:** sxem 12 · cədvəl 48 · view 8 · trigger 5

## 5. 40 sorğunu sına

```bash
psql -U arti_user -d arti_baza -f DS_Baza/sql/10_sorgular.sql
```

## Vacib qeyd

`.env` faylı repoda **yoxdur** — onu `DS_Backend/.env.example`-dən kopyalayın:

```bash
cd DS_Backend
cp .env.example .env
# .env içindəki DATABASE_URL-i yoxlayın
```
