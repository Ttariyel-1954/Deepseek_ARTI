# ══════════════════════════════════════════════════════════════
#  DS_Backend — çoxmərhələli (multi-stage) Docker qurulusu
#  Nəticə: ~180 MB image (node_modules daxil deyil)
# ══════════════════════════════════════════════════════════════

# ─── MƏRHƏLƏ 1: asılılıqlar ───
FROM node:22-alpine AS asililiqlar
WORKDIR /app

# Yalniz manifestleri kocur — layer kesi saxlanilir
COPY package*.json ./
COPY prisma ./prisma
COPY prisma.config.ts ./

# npm ci — package-lock.json-a EYNIEN uygun qurur (npm install YOX)
RUN npm ci --ignore-scripts

# ─── MƏRHƏLƏ 2: qurulus ───
FROM node:22-alpine AS qurulus
WORKDIR /app

COPY --from=asililiqlar /app/node_modules ./node_modules
COPY . .

# Prisma musteri kodunu yarat
RUN npx prisma generate

# TypeScript -> JavaScript
RUN npm run build

# Yalniz istehsalat asililiqlari
RUN npm prune --omit=dev

# ─── MƏRHƏLƏ 3: istehsalat ───
FROM node:22-alpine AS istehsalat
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=4000

# Guvenlik: root olmayan istifadeci
RUN addgroup -g 1001 -S nodejs && adduser -S nestjs -u 1001

COPY --from=qurulus --chown=nestjs:nodejs /app/node_modules ./node_modules
COPY --from=qurulus --chown=nestjs:nodejs /app/dist         ./dist
COPY --from=qurulus --chown=nestjs:nodejs /app/prisma       ./prisma
COPY --from=qurulus --chown=nestjs:nodejs /app/package.json ./

USER nestjs

EXPOSE 4000

# Saglamliq yoxlamasi — konteyner "canli" sayilir?
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:4000/api/v1/saglamliq').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

CMD ["node", "dist/main.js"]
