# Deepseek_ARTI

**ARTİ — Azərbaycan Respublikasının Təhsil İnstitutu** üçün ERP sistemi.
Layihə qat-qat qurulur: əvvəlcə baza, sonra backend, sonra frontend və veb.
Hər qat **addım-addım** yazılır və hər addım canlı yoxlanılır.

---

## Layihə xəritəsi

```
~/Deepseek_ARTI/
│
├── DS_Baza/                 ← BAZA QATI
│   ├── sql/
│   │   ├── 00_TAM_DDL.sql       bütün sxem: 12 sxem · 48 cədvəl · 35 FK
│   │   ├── 10_view.sql          8 view
│   │   ├── 11_funksiya.sql      10 funksiya
│   │   ├── 12_trigger.sql       14 trigger
│   │   ├── 10_sorgular.sql      40 yoxlama sorğusu
│   │   ├── 20_veriler.sql       bütün məlumat (mərkəz, şöbə, əməkdaş)
│   │   └── BERPA_ET.md          bazanı sıfırdan bərpa təlimatı
│   ├── ders.css                 dərslərin ümumi görünüşü
│   └── ders_yarat.py            Baza dərsinin generatoru
│
├── DS_Backend/              ← BACKEND QATI (NestJS 12 + Prisma 7)
│   ├── src/
│   │   ├── main.ts              giriş nöqtəsi: prefiks, validasiya, Swagger
│   │   ├── app.module.ts        kök modul
│   │   ├── prisma/              baza bağlantısı (PrismaService, PrismaModule)
│   │   ├── common/filters/      vahid xəta formatı
│   │   ├── saglamliq/           sağlamlıq endpoint-i
│   │   └── generated/           Prisma müştərisi (git-ə düşmür)
│   ├── prisma/schema.prisma     48 model — bazadan çıxarılıb
│   ├── test/                    e2e testlər
│   ├── ds1_yarat.py             Backend-1 dərsinin generatoru
│   └── package.json
│
├── DƏRSLƏR/                 ← DƏRSLƏR (HTML)
│   ├── Deepseek_Baza.html       Baza — 40 sorğu (2260 sətir)
│   └── DS_Backend-1.html        Backend 1 — A/B/C/D (2240 sətir)
│
├── _hesabat/                ← generatorların işlətdiyi çıxışlar
│   └── sorgu_cixis.txt          40 sorğunun real nəticəsi
│
├── _arxiV/                  ← baza ehtiyat nüsxələri (git-ə düşmür)
│   └── arti_baza_TAM_*.sql
│
├── .githooks/pre-commit     ← gizli məlumat qoruyucusu
├── README.md                ← bu fayl
└── yoxla.sh                 ← vəziyyət yoxlaması
```

---

## Hazırkı vəziyyət

| Qat | Vəziyyət | Nə var |
|---|---|---|
| **Baza** | ✅ Hazır | 12 sxem · 48 cədvəl · 8 view · 10 funksiya · 14 trigger · 35 FK |
| **Backend** | 🟡 Davam edir | NestJS 12 · 2 endpoint · 7 test · Swagger. **Autentifikasiya yoxdur** |
| **Frontend** | ⬜ Başlamamış | — |
| **Web** | ⬜ Başlamamış | — |

### Dərslər

| # | Dərs | Sətir | Vəziyyət |
|---|---|---|---|
| 1 | `Deepseek_Baza.html` — baza və 40 sorğu | 2260 | ✅ |
| 2 | `DS_Backend-1.html` — sıfırdan ilk işləyən API | 2240 | ✅ |
| 3 | `DS_Backend-2.html` — struktur və kadrlar modulları | — | ⬜ |
| 4 | `DS_Backend-3.html` — autentifikasiya, rollar, audit | — | ⬜ |
| 5 | `DS_Backend-4.html` — AI qatı, ixrac, yerləşdirmə | — | ⬜ |
| 6 | `DS_Frontend-*.html` | — | ⬜ |
| 7 | `DS_Web-*.html` | — | ⬜ |

---

## Sürətli başlanğıc

```bash
# 1) Layihəni aç
cd ~/Deepseek_ARTI

# 2) Vəziyyəti yoxla
./yoxla.sh

# 3) Backend-i işə sal
cd DS_Backend
unset DATABASE_URL PGHOST        # ← VACİB: sistem dəyişəni başqa bazaya yönəldə bilər
npm run start:dev
```

İşlədiyini yoxla:

```bash
curl -s http://localhost:4000/api/v1/saglamliq | python3 -m json.tool
# {
#   "status": "saglam",
#   "baza": { "qosulub": true, "cedvel_sayi": 48, "gecikme_ms": 2 },
#   ...
# }
```

Swagger sənədləşdirməsi: <http://localhost:4000/docs>

---

## Baza

| Nə | Say |
|---|---|
| Sxem | 12 — `ai` `audit` `elm` `kadrlar` `logistika` `maliyye` `metodika` `ortaq` `qiymetlendirme` `sened` `struktur` `tehsil` |
| Cədvəl | 48 |
| View | 8 |
| Funksiya | 10 |
| Trigger | 14 |
| Xarici açar | 35 |

**Əsas məlumat:**

| Cədvəl | Sətir |
|---|---|
| `struktur.merkezler` | 10 |
| `struktur.shobeler` | 36 |
| `struktur.rehberlik` | 7 |
| `kadrlar.emekdaslar` | 14 |
| `kadrlar.istifadeciler` | 4 |

### Bağlantı

```
Baza       : arti_baza
İstifadəçi : arti_user
Şifrə      : arti_secret_2025
Port       : 5432
```

```bash
unset DATABASE_URL PGHOST
export PGPASSWORD=arti_secret_2025
psql -U arti_user -d arti_baza
```

### Bazanı sıfırdan bərpa etmək

```bash
cd ~/Deepseek_ARTI/DS_Baza/sql
unset DATABASE_URL PGHOST
export PGPASSWORD=arti_secret_2025

psql -U arti_user -d arti_baza -f 00_TAM_DDL.sql     # sxem + cədvəllər
psql -U arti_user -d arti_baza -f 10_view.sql        # view-lar
psql -U arti_user -d arti_baza -f 11_funksiya.sql    # funksiyalar
psql -U arti_user -d arti_baza -f 12_trigger.sql     # trigger-lər
psql -U arti_user -d arti_baza -f 20_veriler.sql     # məlumat
```

Ətraflı: [`DS_Baza/sql/BERPA_ET.md`](DS_Baza/sql/BERPA_ET.md)

---

## Backend

**Texnologiya:** NestJS 12.0.3 · Prisma 7.10 · TypeScript 6.0 · Vitest 4.1 · PostgreSQL

### Endpoint-lər

| Metod | Yol | Nə edir |
|---|---|---|
| `GET` | `/api/v1` | API haqqında qısa məlumat |
| `GET` | `/api/v1/saglamliq` | Sağlamlıq — bazaya **real** sorğu göndərir |

Sənədləşdirmə: `/docs`

### Əmrlər

```bash
cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST

npm run start:dev        # inkişaf — hər dəyişiklikdə özü yenilənir
npm run build            # TypeScript → JavaScript (dist/)
npm run start:prod       # istehsalat: node dist/main.js

npm test                 # unit testlər (baza lazım DEYİL) — 3 test
npx vitest run --config vitest.config.e2e.ts   # e2e (real baza) — 4 test

npm run db:yenile        # prisma db pull && prisma generate
```

### Vacib qaydalar

Bu layihədə aşağıdaki şeylər **məcburidir** — pozulsa kod işləmir:

| Qayda | Səbəb |
|---|---|
| `import ... from './x.js'` | ESM + `moduleResolution: nodenext`. `.js` olmasa `TS2307` |
| `schemas = [...]` bir sətirdə | Prisma çoxsətirli massivi qəbul etmir → `P1012` |
| `PrismaPg` adapter | Prisma 7-də adapter MÜTLƏQDİR |
| `@Global()` PrismaModule-da | Yoxsa `Nest can't resolve dependencies` |
| `JwtModule.registerAsync()` | `register()` `.env`-dən əvvəl işləyir (3-cü dərsdə) |
| SQL-də `::int` / `::float8` cast | Yoxsa `Do not know how to serialize a BigInt` |

---

## Dərslərin formatı — A / B / C / D

Hər dərs addımlara bölünüb və **hər addım 4 hissədən** ibarətdir:

| Hissə | Nə var | Nə üçün |
|---|---|---|
| **A** | Bu addım nəyə görədir — 3-4 cümlə | Kodu yazmadan **əvvəl** məqsədi anlamaq |
| **B** | Addıma aid kodun özü — tam | Olduğu kimi kopyalayıb işlətmək |
| **C** | Yoxlama əmrləri + ⚠️ **bu kod olmasa nə olardı** | Səhvi dərhal tutmaq |
| **D** | Bu koddan sonra **sistemin real durumu** | Nəticənin ölçülmüş olduğunu görmək |

**C və D hissələrindəki bütün çıxışlar realdır** — kodu bilərəkdən söndürüb
alınmış xətalar və canlı sistemdən götürülmüş nəticələr.

### Dərsləri yenidən yaratmaq

Dərs generatorları kodu **birbaşa işləyən layihədən** oxuyur — ona görə dərs
heç vaxt koddan ayrı düşə bilməz:

```bash
cd ~/Deepseek_ARTI
python3 DS_Baza/ders_yarat.py      # → DƏRSLƏR/Deepseek_Baza.html
python3 DS_Backend/ds1_yarat.py    # → DƏRSLƏR/DS_Backend-1.html
```

---

## Yoxlama

```bash
./yoxla.sh                # tam vəziyyət hesabatı
./yoxla.sh baza           # yalnız baza
./yoxla.sh backend        # yalnız backend
./yoxla.sh dersler        # yalnız dərslər
./yoxla.sh git            # yalnız git
./yoxla.sh test           # testləri də işlət
```

---

## Gizli məlumat qoruyucusu

Repo tarixçəsində bir dəfə DeepSeek API açarı commit edilmişdi.
Təkrarlanmasın deyə `pre-commit` hook qurulub:

```bash
git config core.hooksPath .githooks     # bir dəfə — artıq qurulub
```

Hook hər commit-dən əvvəl hazırlanmış faylları yoxlayır və
açar / parol / private key tapsa commit-i **dayandırır**.

⚠️ **Açarı `.env` və ya `Kodlar` faylında saxlayın** — hər ikisi
`.gitignore`-dadır və repoya düşmür.

---

## Vacib xəbərdarlıqlar

- ⚠️ **`unset DATABASE_URL PGHOST`** — hər `psql`, `npm` və server əmrindən əvvəl.
  Sistem dəyişəni başqa bazaya (`zarat_deepseek`) yönləndirə bilər.
- ⚠️ **`.env` git-ə düşmür** — yeni kompüterdə `.env.example`-dən kopyalayın.
- ⚠️ **`src/generated/` git-ə düşmür** — `npx prisma generate` ilə yaradılır.
- ⚠️ **`node_modules/` git-ə düşmür** — `npm install` lazımdır.

---

## Repo

```
git@github.com:Ttariyel-1954/Deepseek_ARTI.git
```

Layihə addım-addım qurulur: hər addım yazılır → canlı yoxlanılır → commit edilir.
