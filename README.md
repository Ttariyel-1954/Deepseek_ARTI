# Deepseek_ARTI

**ARTİ (Azərbaycan Respublikasının Təhsil İnstitutu) üçün AI ilə idarə olunan ERP sistemi.**

Layihə 4 müstəqil blokdan ibarətdir. Hər blok ayrıca yenilənə və genişlənə bilər.

| Blok | Nə edir | Texnologiya | Vəziyyət |
|---|---|---|---|
| `DS_Baza` | Məlumatı saxlayır | PostgreSQL 18 | ✅ hazır |
| `DS_Backend` | API xidməti | NestJS 12 + Prisma 7 | ✅ Backend-1, -2 hazır |
| `DS_Frontend` | İstifadəçi interfeysi | Next.js 16 + React 19 | ⏳ plan |
| `DS_Web` | Xarici veb təqdimat | yenidən yazılır | ⏳ real məlumat gözlənilir |

## Baza

| Göstərici | Dəyər |
|---|---|
| Baza adı | `arti_baza` |
| İstifadəçi | `arti_user` |
| Port | 5432 |
| Sxem | 12 |
| Cədvəl | 48 |
| Görünüş (view) | 8 |
| Funksiya | 10 |
| Trigger | 5 |
| Xarici açar | 35 |

## Sürətli başlanğıc

```bash
cd ~/Deepseek_ARTI
unset DATABASE_URL PGHOST          # MÜTLƏQ!
export PGPASSWORD=arti_secret_2025

# Vəziyyəti yoxla
./yoxla.sh

# 40 sorğunu işlət
psql -U arti_user -d arti_baza -f DS_Baza/sql/10_sorgular.sql
```

## Dərslər

Bütün dərslər `DƏRSLƏR/` qovluğundadır. Brauzerdə açın:

```bash
open ~/Deepseek_ARTI/DƏRSLƏR/Deepseek_Baza.html
```

| # | Dərs | Sətir | Vəziyyət |
|---|---|---|---|
| 1 | `Deepseek_Baza.html` | 2261 | ✅ hazır |
| 2 | `DS_Backend-1.html` | 2145 | ✅ hazır |
| 3 | `DS_Backend-2.html` | 2879 | ✅ hazır |
| 4-5 | `DS_Backend-3..4.html` | — | ⏳ növbəti |
| 6-8 | `DS_Frontend-1..3.html` | — | ⏳ plan |
| 9-10 | `DS_Web-1..2.html` | — | ⏳ real məlumat gözlənilir |

## Qovluq strukturu

```
Deepseek_ARTI/
Deepseek_ARTI/
├── DS_Baza/                    baza bloku — PostgreSQL 18
│   ├── ders_yarat.py           dərs generatoru
│   └── sql/
│       ├── 00_TAM_DDL.sql      struktur: 12 sxem, 48 cədvəl, 8 view, 10 fn, 5 trigger
│       ├── 20_veriler.sql      məlumat: bütün sətirlər (INSERT formatında)
│       ├── BERPA_ET.md         bazanı sıfırdan bərpa təlimatı
│       ├── 10_sorgular.sql     40 vacib sorğu
│       ├── 10_view.sql         8 görünüş
│       ├── 11_funksiya.sql     10 funksiya
│       └── 12_trigger.sql      5 trigger
├── DS_Backend/                 NestJS 12 + Prisma 7
│   ├── qur.sh                  tam qurulma skripti (bir əmrlə)
│   └── ders2_yarat.py          Backend-2 dərs generatoru
├── DS_Frontend/                Next.js 16 + React 19 (plan)
├── DS_Web/                     xarici veb təqdimat (real məlumat gözlənilir)
├── DƏRSLƏR/                    bütün HTML dərslər
├── _hesabat/                   sınaq nəticələri
└── yoxla.sh                    sürətli vəziyyət yoxlaması
```

## Backend

```bash
cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST
npm run start:dev                 # :4000
curl http://localhost:4000/api/v1/struktur/merkezler
open http://localhost:4000/docs
```

### API göstəriciləri

| Göstərici | Dəyər |
|---|---|
| Endpoint | **20** |
| Unit test | 25 |
| e2e test | 30 |
| **Cəmi test** | **55** |
| Modul | 5 (sağlamlıq, struktur, kadrlar, hesabat, prisma) |

Təlimatlar real sınaqdan keçirilmişdir:

| Dərs | Nəticə |
|---|---|
| Backend-1 | 48 model, 3 marshrut, `int` tipləri — `_hesabat/backend1_sinag.txt` |
| Backend-2 | 20 marshrut, 55 test, SQL injection qoruması — `_hesabat/backend2_sinag.txt` |

### Əsas xüsusiyyətlər

- **DTO + class-validator** — bütün giriş məlumatı yoxlanılır
- **Vahid xəta formatı** — `{ ugur, xeta: { kod, mesaj, detallar }, yol, vaxt }`
- **SQL injection qoruması** — ağ siyahı (whitelist) prinsipi
- **Səhifələmə + filtr + sıralama** — `SehifeDto`-dan miras
- **Mass assignment qoruması** — `forbidNonWhitelisted`

## Vacib qaydalar

1. **`unset DATABASE_URL PGHOST`** — hər sessiyanın əvvəlində.
2. **PostgreSQL cast** — `id::int`, `maas::float8`, `count(*)::int`.
3. **Backend import** — `.js` MƏCBURİ; frontend-də YOX.
4. **Özünü təsdiqləmə** — "yəqin işləyir" yox, real sınaq.

## Baza bərpası

Repo-da bazanın tam bərpası üçün hər şey var:

```bash
psql -U postgres -c "CREATE ROLE arti_user WITH LOGIN PASSWORD 'arti_secret_2025';"
psql -U postgres -c "CREATE DATABASE arti_baza OWNER arti_user;"
export PGPASSWORD=arti_secret_2025
psql -U arti_user -d arti_baza -f DS_Baza/sql/00_TAM_DDL.sql
psql -U arti_user -d arti_baza -f DS_Baza/sql/20_veriler.sql
```

Ətraflı: [`DS_Baza/sql/BERPA_ET.md`](DS_Baza/sql/BERPA_ET.md)

## Git

Repo: <https://github.com/Ttariyel-1954/Deepseek_ARTI>

```bash
cd ~/Deepseek_ARTI
git add -A
git commit -m "<qat>: <qısa təsvir>"
git push
```

Commit mesajı formatı: `baza:` · `backend:` · `frontend:` · `ders:` · `sened:`

Push-dan əvvəl **mütləq** yoxla:

```bash
git status
git diff --cached | grep -iE 'sk-|api_key|password|secret'
```


---

## 🔐 Təhlükəsizlik qeydi

| Nə | Vəziyyət |
|---|---|
| `DS_Backend/.env` | ❌ **repoda yoxdur** (`.gitignore`-dadır) |
| `DS_Backend/.env.example` | ✅ repoda var — şifrəsiz nümunə |
| `node_modules/`, `dist/`, `src/generated/` | ❌ repoda yoxdur |
| API açarları | ✅ repo-da **yoxdur** |

**`arti_secret_2025`** — bu, **yalnız lokal inkişaf bazasının** şifrəsidir və
sənədlərdə (dərslər, `BERPA_ET.md`, `qur.sh`) copy-paste rahatlığı üçün açıq göstərilib.

> ⚠️ **İstehsala (production) çıxarmazdan əvvəl mütləq dəyişdirin:**
> ```bash
> psql -U postgres -c "ALTER ROLE arti_user WITH PASSWORD 'yeni-guclu-sifre';"
> ```
> Sonra `DS_Backend/.env`-i yeniləyin. `.env` repoya getmədiyi üçün
> şifrə dəyişikliyi repoya təsir etmir.

Push-dan əvvəl həmişə yoxlayın:

```bash
git diff --cached | grep -iE 'sk-|api_key|password|secret'
```
