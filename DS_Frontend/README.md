# DS_Frontend

**Next.js 16 + React 19 + Tailwind 4** — ARTİ ERP istifadəçi interfeysi.

## Vəziyyət

⏳ **Plan mərhələsində** — 3 dərs nəzərdə tutulub:

| # | Dərs | Mövzu |
|---|---|---|
| 1 | `DS_Frontend-1.html` | Next.js qurulumu, App Router, layout, Tailwind 4 |
| 2 | `DS_Frontend-2.html` | API körpüsü, autentifikasiya, CRUD səhifələri |
| 3 | `DS_Frontend-3.html` | Dashboard, qrafiklər, Excel/PDF ixracı |

## Əsas texnologiyalar

| Alət | Versiya |
|---|---|
| Next.js | 16.3 |
| React | 19.2 |
| Tailwind CSS | 4 |
| TypeScript | 5.7+ |

## Vacib qayda

Frontend import-larında **`.js` yazılmır** (backend-də isə mütləqdir):

```typescript
import { apiGet } from '@/lib/api';        // ✅ frontend
import { apiGet } from '@/lib/api.js';     // ❌ səhv
```

Backend API: `http://localhost:4000/api/v1`
