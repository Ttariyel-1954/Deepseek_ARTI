#!/bin/bash
# ══════════════════════════════════════════════════════════════════════
#  DS_Backend-3 — ADDIM-ADDIM YOXLAMA
#
#  Hər addım İKİ ŞEYİ yoxlayır:
#    1) LOKAL — bu addımda qurduğumuz şey işləyirmi?
#    2) TAM   — bütün Backend hələ də işləyirmi? (reqressiya)
#
#  İSTİFADƏ:
#    bash scripts/yoxla_addim.sh              # bütün addımlar
#    bash scripts/yoxla_addim.sh 7            # yalnız 7-ci addım
#    bash scripts/yoxla_addim.sh 7 12         # 7-dən 12-yə qədər
#    bash scripts/yoxla_addim.sh siyahi       # addımların siyahısı
#
#  Server lazımdır (11-ci addımdan sonrası üçün):
#    npm run start:dev          # ayrı terminalda
#    API=http://localhost:4001/api/v1 bash scripts/yoxla_addim.sh
# ══════════════════════════════════════════════════════════════════════

unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"

BAZA="${BAZA:-arti_baza}"
DB_ISTIFADECI="${DB_ISTIFADECI:-arti_user}"
API="${API:-http://localhost:4000/api/v1}"
TOKEN_FAYLI="${TOKEN_FAYLI:-/tmp/arti_token.txt}"

YASIL=$'\033[32m'; QIRMIZI=$'\033[31m'; SARI=$'\033[33m'
MAVI=$'\033[36m';   BOZ=$'\033[90m';     SIFIR=$'\033[0m'

KECDI=0; XETA=0; ATLANDI=0
SERVER_VAR=0

# ── KÖMƏKÇİLƏR ────────────────────────────────────────────────────────

yoxla() {   # yoxla "ad" "gözlənilən" "faktiki"
  if [ "$2" = "$3" ]; then
    printf "    ${YASIL}✓${SIFIR} %-44s ${BOZ}%s${SIFIR}\n" "$1" "$3"
    KECDI=$((KECDI + 1))
  else
    printf "    ${QIRMIZI}✗${SIFIR} %-44s ${QIRMIZI}%s${SIFIR} ${BOZ}(gözlənilən: %s)${SIFIR}\n" \
      "$1" "$3" "$2"
    XETA=$((XETA + 1))
  fi
}

daxildir() {   # daxildir "ad" "axtarılan" "mətn"
  if printf '%s' "$3" | grep -q -- "$2"; then
    printf "    ${YASIL}✓${SIFIR} %-44s ${BOZ}mövcuddur${SIFIR}\n" "$1"
    KECDI=$((KECDI + 1))
  else
    printf "    ${QIRMIZI}✗${SIFIR} %-44s ${QIRMIZI}tapılmadı: %s${SIFIR}\n" "$1" "$2"
    XETA=$((XETA + 1))
  fi
}

yoxdur() {   # yoxdur "ad" "axtarılmaz" "mətn"
  if printf '%s' "$3" | grep -q -- "$2"; then
    printf "    ${QIRMIZI}✗${SIFIR} %-44s ${QIRMIZI}VAR OLMAMALIDIR: %s${SIFIR}\n" "$1" "$2"
    XETA=$((XETA + 1))
  else
    printf "    ${YASIL}✓${SIFIR} %-44s ${BOZ}yoxdur${SIFIR}\n" "$1"
    KECDI=$((KECDI + 1))
  fi
}

fayl_var() {   # fayl_var "yol" "ad"
  if [ -e "$1" ]; then
    printf "    ${YASIL}✓${SIFIR} %-44s ${BOZ}%s${SIFIR}\n" "$2" "$1"
    KECDI=$((KECDI + 1))
  else
    printf "    ${QIRMIZI}✗${SIFIR} %-44s ${QIRMIZI}YOXDUR: %s${SIFIR}\n" "$2" "$1"
    XETA=$((XETA + 1))
  fi
}

bashliq() {
  printf "\n${MAVI}══════════════════════════════════════════════════════════════${SIFIR}\n"
  printf "${MAVI}  ADDIM %s — %s${SIFIR}\n" "$1" "$2"
  printf "${BOZ}  Dərs bölməsi: %s${SIFIR}\n" "$3"
  printf "${MAVI}══════════════════════════════════════════════════════════════${SIFIR}\n"
}

alt() { printf "\n  ${SARI}▸ %s${SIFIR}\n" "$1"; }

server_lazim() {
  if [ "$SERVER_VAR" -eq 0 ]; then
    printf "    ${SARI}⚠${SIFIR}  Server işləmir — atlanır\n"
    printf "    ${BOZ}   Ayrı terminalda: npm run start:dev${SIFIR}\n"
    ATLANDI=$((ATLANDI + 1))
    return 1
  fi
  return 0
}

# ── TOKEN: AL və YADDA SAXLA ──────────────────────────────────────────

token_al() {   # token_al [rol]  → TOKEN dəyişəninə yazır, həm də fayla
  local rol="${1:-admin}"
  TOKEN=$(curl -s -X POST "$API/auth/login" \
    -H 'Content-Type: application/json' \
    -d "{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}" 2>/dev/null \
    | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('token',''))" 2>/dev/null)

  if [ -n "$TOKEN" ]; then
    printf '%s' "$TOKEN" > "$TOKEN_FAYLI"    # YADDA SAXLA
    return 0
  fi
  return 1
}

token_oxu() { TOKEN=$(cat "$TOKEN_FAYLI" 2>/dev/null || echo ""); }

kod() {   # kod "metod" "yol" [token]
  if [ -n "${3:-}" ]; then
    curl -s -o /dev/null -w '%{http_code}' -X "$1" "$API$2" \
      -H "Authorization: Bearer $3" 2>/dev/null
  else
    curl -s -o /dev/null -w '%{http_code}' -X "$1" "$API$2" 2>/dev/null
  fi
}

kod_cisim() {   # kod_cisim "metod" "yol" "cisim" [token]
  if [ -n "${4:-}" ]; then
    curl -s -o /dev/null -w '%{http_code}' -X "$1" "$API$2" \
      -H 'Content-Type: application/json' \
      -H "Authorization: Bearer $4" -d "$3" 2>/dev/null
  else
    curl -s -o /dev/null -w '%{http_code}' -X "$1" "$API$2" \
      -H 'Content-Type: application/json' -d "$3" 2>/dev/null
  fi
}

test_sayi() {   # test_sayi "fayl" → keçən test sayı
  NO_COLOR=1 npx vitest run --config vitest.config.e2e.ts "$1" 2>&1 \
    | grep -E '^\s*Tests\s' | grep -oE '[0-9]+ passed' | grep -oE '^[0-9]+' | head -1
}

# ══════════════════════════════════════════════════════════════════════
addim_1() {
  bashliq 1 "Mühit hazırdır?" "§2 (başlanğıc)"

  alt "Node 22+"
  local node_ok
  node_ok=$(node -e 'process.exit(parseInt(process.versions.node)>=22?0:1)' 2>/dev/null && echo 1 || echo 0)
  yoxla "Node 22+ quraşdırılıb" "1" "$node_ok"
  printf "    ${BOZ}   → node %s / npm %s${SIFIR}\n" "$(node -v 2>/dev/null)" "$(npm -v 2>/dev/null)"

  alt "PostgreSQL 5432"
  yoxla "5432 portu dinlənir" "ok" "$(pg_isready -h localhost -p 5432 >/dev/null 2>&1 && echo ok || echo yox)"

  alt "Baza əlçatandır"
  local cedvel
  cedvel=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT count(*)::int FROM information_schema.tables WHERE table_type='BASE TABLE'
       AND table_schema NOT IN ('pg_catalog','information_schema')" 2>/dev/null || echo 0)
  yoxla "Bazada 48 cədvəl var" "48" "$cedvel"

  local sxem
  sxem=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT count(*)::int FROM information_schema.schemata
      WHERE schema_name NOT LIKE 'pg_%'
        AND schema_name NOT IN ('information_schema','public')" 2>/dev/null || echo 0)
  yoxla "12 tətbiq sxemi var" "12" "$sxem"

  alt "Auth üçün lazım olan cədvəl"
  local ist
  ist=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT count(*)::int FROM information_schema.columns WHERE table_schema='kadrlar'
       AND table_name='istifadeciler' AND column_name IN ('email','parol_hash','rol','aktiv')" 2>/dev/null || echo 0)
  yoxla "istifadeciler: 4 sütun (email, parol_hash, rol, aktiv)" "4" "$ist"

  alt "Audit cədvəli"
  local aud
  aud=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT count(*)::int FROM information_schema.columns WHERE table_schema='audit'
       AND table_name='audit_log' AND column_name IN ('cedvel_adi','emeliyyat','setir_id','istifadeci','vaxt','qeyd')" 2>/dev/null || echo 0)
  yoxla "audit.audit_log: 6 sütun" "6" "$aud"
}

# ══════════════════════════════════════════════════════════════════════
addim_2() {
  bashliq 2 "Auth paketləri quraşdırıldı?" "§2"

  alt "Lokal paketlər (node_modules)"
  for p in "@nestjs/jwt" "@nestjs/passport" "passport" "passport-jwt" "bcryptjs"; do
    if [ -e "node_modules/$p/package.json" ]; then
      local v
      v=$(python3 -c "import json;print(json.load(open('node_modules/$p/package.json'))['version'])" 2>/dev/null || echo "?")
      yoxla "$p v$v" "var" "var"
    else
      yoxla "$p" "var" "YOXDUR"
    fi
  done

  alt "package.json-da qeydiyyat"
  local pj; pj=$(cat package.json 2>/dev/null)
  daxildir "@nestjs/jwt dependencies-də" '"@nestjs/jwt"' "$pj"
  daxildir "@nestjs/passport dependencies-də" '"@nestjs/passport"' "$pj"
  daxildir "bcryptjs dependencies-də" '"bcryptjs"' "$pj"
  daxildir "tsx devDependencies-də" '"tsx"' "$pj"

  alt "TAM BACKEND — köhnə paketlər yerindədir?"
  for p in "@nestjs/core" "@prisma/client" "exceljs" "class-validator"; do
    yoxla "$p" "var" "$([ -e "node_modules/$p/package.json" ] && echo var || echo YOXDUR)"
  done
}

# ══════════════════════════════════════════════════════════════════════
addim_4() {
  bashliq 4 "JWT tokenin strukturu düzgündür?" "§4 (offline — server lazım deyil)"

  alt "Nümunə token yarat"
  local n
  n=$(node -e "
    const c=Buffer.from(JSON.stringify({alg:'HS256',typ:'JWT'})).toString('base64url');
    const p=Buffer.from(JSON.stringify({sub:2,email:'admin@arti.edu.az',rol:'admin',exp:9999999999})).toString('base64url');
    console.log(c+'.'+p+'.imza');" 2>/dev/null)

  yoxla "Token 3 hissədən ibarətdir" "3" "$(printf '%s' "$n" | awk -F. '{print NF}')"

  alt "Header oxunur"
  local alg
  alg=$(printf '%s' "$n" | cut -d. -f1 | python3 -c "
import sys,base64,json
s=sys.stdin.read().strip(); s+='='*(-len(s)%4)
print(json.loads(base64.urlsafe_b64decode(s)).get('alg',''))" 2>/dev/null)
  yoxla "Header-də alg=HS256" "HS256" "$alg"

  alt "Payload oxunur"
  local rol exp
  rol=$(printf '%s' "$n" | cut -d. -f2 | python3 -c "
import sys,base64,json
s=sys.stdin.read().strip(); s+='='*(-len(s)%4)
print(json.loads(base64.urlsafe_b64decode(s)).get('rol',''))" 2>/dev/null)
  exp=$(printf '%s' "$n" | cut -d. -f2 | python3 -c "
import sys,base64,json
s=sys.stdin.read().strip(); s+='='*(-len(s)%4)
print(json.loads(base64.urlsafe_b64decode(s)).get('exp',0))" 2>/dev/null)
  yoxla "Payload-da rol var" "admin" "$rol"
  yoxla "Payload-da exp var" "1" "$([ "${exp:-0}" -gt 0 ] && echo 1 || echo 0)"

  alt "⚠️ Token OXUNA BİLƏR, AMMA İMZASIZ DƏYİŞDİRİLƏ BİLMƏZ"
  printf "    ${BOZ}   payload base64-dür — şifrəli DEYİL, imza ilə qorunur${SIFIR}\n"
  yoxla "Payload şifrələnməyib (base64-dür)" "admin" "$rol"

  alt "TAM BACKEND — strategiya faylları yerindədir"
  fayl_var "src/auth/strategies/jwt.strategy.ts" "JwtStrategy faylı"
  fayl_var "src/auth/auth.module.ts" "AuthModule faylı"
}

# ══════════════════════════════════════════════════════════════════════
addim_6() {
  bashliq 6 "bcrypt hash və compare işləyir?" "§6 (offline)"

  alt "Hash yaradılır və yoxlanılır"
  local r
  r=$(node -e "
    const b=require('bcryptjs');
    const h=b.hashSync('123456',10);
    console.log([h.length,h.slice(0,4),b.compareSync('123456',h),b.compareSync('654321',h)].join('|'));" 2>/dev/null)

  yoxla "Hash uzunluğu 60 simvol" "60" "$(printf '%s' "$r" | cut -d'|' -f1)"
  yoxla "Hash formatı \$2b\$" '$2b$' "$(printf '%s' "$r" | cut -d'|' -f2)"
  yoxla "Doğru şifrə → true" "true" "$(printf '%s' "$r" | cut -d'|' -f3)"
  yoxla "Səhv şifrə → false" "false" "$(printf '%s' "$r" | cut -d'|' -f4)"

  alt "Hər hash FƏRQLİDİR (duz işləyir)"
  yoxla "Eyni şifrə → fərqli hash" "FERQLI" "$(node -e "
    const b=require('bcryptjs');
    console.log(b.hashSync('123456',10)===b.hashSync('123456',10)?'EYNI':'FERQLI');" 2>/dev/null)"

  alt "TAM BACKEND — bazadakı hash-lər etibarlıdır"
  local bh y
  bh=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT parol_hash FROM kadrlar.istifadeciler WHERE email='admin@arti.edu.az'" 2>/dev/null)
  y=$(node -e "console.log(require('bcryptjs').compareSync('123456',process.argv[1])?'DUZ':'SEHV')" "$bh" 2>/dev/null)
  yoxla "Bazadakı şifrə '123456'-dır" "DUZ" "$y"

  alt "⚠️ Sütun adı 'parol_hash'-dır ('parol' YOX)"
  yoxdur "istifadeciler cədvəlində 'parol' sütunu yoxdur" "(^| )parol( |$)" \
    "$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
       "SELECT string_agg(column_name,' ') FROM information_schema.columns
         WHERE table_schema='kadrlar' AND table_name='istifadeciler'" 2>/dev/null)"
}

# ══════════════════════════════════════════════════════════════════════
addim_7() {
  bashliq 7 "DTO faylları və validasiya qaydaları hazırdır?" "§7 (offline)"

  fayl_var "src/auth/dto/login.dto.ts" "LoginDto"
  fayl_var "src/auth/dto/qeydiyyat.dto.ts" "QeydiyyatDto"

  alt "LoginDto qaydaları"
  local m; m=$(cat src/auth/dto/login.dto.ts 2>/dev/null)
  daxildir "email üçün @IsEmail" "@IsEmail" "$m"
  daxildir "parol üçün @MinLength(6)" "@MinLength(6" "$m"
  daxildir "parol üçün @MaxLength" "@MaxLength" "$m"

  alt "QeydiyyatDto qaydaları"
  m=$(cat src/auth/dto/qeydiyyat.dto.ts 2>/dev/null)
  daxildir "parol üçün @MinLength(8)" "@MinLength(8" "$m"
  daxildir "rol üçün @IsIn" "@IsIn" "$m"
  daxildir "ROLLAR sabiti (4 rol)" "ROLLAR" "$m"
  daxildir "ad_soyad sahəsi" "ad_soyad" "$m"

  alt "⚠️ ROLLAR — dəqiq 4 rol olmalıdır"
  local say
  say=$(printf '%s' "$m" | grep -oE "'(admin|muhendis|maliyyeci|baxici)'" | sort -u | wc -l | tr -d ' ')
  yoxla "4 unikal rol" "4" "$say"

  alt "TAM BACKEND — bütün DTO-lar yerindədir"
  local cemi
  cemi=$(find src -name '*.dto.ts' | wc -l | tr -d ' ')
  yoxla "DTO fayl sayı ≥ 6" "1" "$([ "$cemi" -ge 6 ] && echo 1 || echo 0)"
  printf "    ${BOZ}   → %s DTO faylı${SIFIR}\n" "$cemi"
}

# ══════════════════════════════════════════════════════════════════════
addim_9() {
  bashliq 9 "Dekoratorlar yaradıldı və build keçir?" "§9"

  fayl_var "src/auth/decorators/roles.decorator.ts" "@Roles"
  fayl_var "src/auth/decorators/public.decorator.ts" "@Public"
  fayl_var "src/auth/decorators/current-user.decorator.ts" "@CurrentUser"

  alt "Dekorator məzmunu"
  daxildir "@Roles → SetMetadata" "SetMetadata" "$(cat src/auth/decorators/roles.decorator.ts 2>/dev/null)"
  daxildir "@Public → SetMetadata" "SetMetadata" "$(cat src/auth/decorators/public.decorator.ts 2>/dev/null)"
  daxildir "@CurrentUser → createParamDecorator" "createParamDecorator" "$(cat src/auth/decorators/current-user.decorator.ts 2>/dev/null)"
  daxildir "⚠️ PUBLIC_ACARI sabiti" "PUBLIC_ACARI" "$(cat src/auth/decorators/public.decorator.ts 2>/dev/null)"
  daxildir "⚠️ ROLLAR_ACARI sabiti" "ROLLAR_ACARI" "$(cat src/auth/decorators/roles.decorator.ts 2>/dev/null)"

  alt "⚠️ CariIstifadeci 'import type' ilə gəlir (TS1272)"
  daxildir "import type { CariIstifadeci }" "import type" \
    "$(cat src/auth/auth.controller.ts 2>/dev/null)"

  alt "TAM BACKEND — build keçir"
  if npm run build >/dev/null 2>&1; then
    yoxla "npm run build" "exit 0" "exit 0"
  else
    yoxla "npm run build" "exit 0" "XƏTA"
  fi

  fayl_var "dist/main.js" "dist/main.js yaradıldı"
}

# ══════════════════════════════════════════════════════════════════════
addim_10() {
  bashliq 10 "JwtStrategy hazırdır?" "§10"

  fayl_var "src/auth/strategies/jwt.strategy.ts" "JwtStrategy"
  local m; m=$(cat src/auth/strategies/jwt.strategy.ts 2>/dev/null)
  daxildir "Bearer token oxunur" "fromAuthHeaderAsBearerToken" "$m"
  daxildir "⚠️ Bazadan istifadəçi oxunur (validate)" "kadrlar.istifadeciler" "$m"
  daxildir "Deaktiv istifadəçi bloklanır" "aktiv" "$m"
  daxildir "⚠️ ConfigService işlədilir (açar uyğunluğu)" "ConfigService" "$m"
  daxildir "PassportStrategy(Strategy)" "PassportStrategy" "$m"

  alt "TAM BACKEND — build hələ də keçir"
  if npm run build >/dev/null 2>&1; then
    yoxla "npm run build" "exit 0" "exit 0"
  else
    yoxla "npm run build" "exit 0" "XƏTA"
  fi
}

# ══════════════════════════════════════════════════════════════════════
addim_11() {
  bashliq 11 "JwtAuthGuard — tokensiz 401 verir?" "§11"

  server_lazim || return

  fayl_var "src/auth/guards/jwt-auth.guard.ts" "JwtAuthGuard"

  alt "LOKAL — qorunan endpoint-lər TOKENSİZ 401 verməlidir"
  yoxla "GET /struktur/merkezler"   "401" "$(kod GET /struktur/merkezler)"
  yoxla "GET /kadrlar/emekdaslar"   "401" "$(kod GET /kadrlar/emekdaslar)"
  yoxla "GET /hesabatlar/icmal"     "401" "$(kod GET /hesabatlar/icmal)"
  yoxla "GET /auth/profil"          "401" "$(kod GET /auth/profil)"
  yoxla "POST /struktur/merkezler"  "401" "$(kod_cisim POST /struktur/merkezler '{"ad":"x"}')"

  alt "@Public() istisnaları AÇIQ olmalıdır"
  yoxla "GET /saglamliq (public)" "200" "$(kod GET /saglamliq)"
  yoxla "GET / (public)"          "200" "$(kod GET /)"
  local lg
  lg="{\"email\":\"admin@arti.edu.az\",\"parol\":\"123456\"}"
  yoxla "POST /auth/login (public) TOKENSİZ 200" "200" "$(kod_cisim POST /auth/login "$lg")"

  alt "⚠️ Səhv token də 401 verməlidir"
  yoxla "Bearer sehv.token.deyeri" "401" "$(kod GET /struktur/merkezler 'sehv.token.deyeri')"
  yoxla "Bearer (boş)" "401" "$(kod GET /struktur/merkezler '')"

  alt "TAM BACKEND — qlobal prefiks"
  local prefiks
  prefiks=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:4000/struktur/merkezler 2>/dev/null)
  printf "    ${BOZ}   prefikssiz /struktur/merkezler → %s (404 gözlənilir)${SIFIR}\n" "$prefiks"
  yoxla "GET /saglamliq hələ də 200" "200" "$(kod GET /saglamliq)"
}

# ══════════════════════════════════════════════════════════════════════
addim_12() {
  bashliq 12 "RolesGuard — rol yoxlaması işləyir?" "§12"

  server_lazim || return

  fayl_var "src/auth/guards/roles.guard.ts" "RolesGuard"
  local m; m=$(cat src/auth/guards/roles.guard.ts 2>/dev/null)
  daxildir "admin super-rol qaydası" "admin" "$m"
  daxildir "⚠️ @Public() yoxlanılır (PUBLIC_ACARI)" "PUBLIC_ACARI" \
    "$(cat src/auth/guards/jwt-auth.guard.ts 2>/dev/null)"
  daxildir "⚠️ ROLLAR_ACARI oxunur" "ROLLAR_ACARI" "$m"
  daxildir "getAllAndOverride işlədilir" "getAllAndOverride" "$m"

  alt "Hər rol üçün token AL"
  for rol in admin muhendis maliyyeci baxici; do
    if token_al "$rol"; then
      yoxla "$rol@arti.edu.az → token" "var" "var"
    else
      yoxla "$rol@arti.edu.az → token" "var" "YOXDUR"
    fi
  done

  alt "Yönləndirmə (GET) — bütün rollar üçün AÇIQ"
  token_al baxici
  yoxla "baxici GET /struktur/merkezler" "200" "$(kod GET /struktur/merkezler "$TOKEN")"
  yoxla "baxici GET /kadrlar/emekdaslar"  "200" "$(kod GET /kadrlar/emekdaslar "$TOKEN")"
  yoxla "baxici GET /hesabatlar/icmal"    "200" "$(kod GET /hesabatlar/icmal "$TOKEN")"

  alt "⚠️ ROLLAR BOŞ OLANDA — hamı buraxılır"
  yoxla "baxici GET /ai/statistika" "200" "$(kod GET /ai/statistika "$TOKEN")"
}

# ══════════════════════════════════════════════════════════════════════
addim_13() {
  bashliq 13 "JWT açarı uyğundur? (real xətanın yoxlaması)" "§13"

  server_lazim || return

  alt "Token AL və YADDA SAXLA"
  if token_al admin; then
    yoxla "Token alındı" "var" "var"
    yoxla "Token fayla yazıldı ($TOKEN_FAYLI)" "var" \
      "$([ -s "$TOKEN_FAYLI" ] && echo var || echo YOXDUR)"
    local uz
    uz=$(printf '%s' "$TOKEN" | wc -c | tr -d ' ')
    yoxla "Token uzunluğu 150+" "1" "$([ "$uz" -ge 150 ] && echo 1 || echo 0)"
    printf "    ${BOZ}   → %s simvol${SIFIR}\n" "$uz"
  else
    yoxla "Token alındı" "var" "YOXDUR"
    return
  fi

  alt "⚠️ ƏSAS YOXLAMA — token 401 YOX, 200 verməlidir"
  yoxla "GET /struktur/merkezler"  "200" "$(kod GET /struktur/merkezler "$TOKEN")"
  yoxla "GET /kadrlar/emekdaslar"  "200" "$(kod GET /kadrlar/emekdaslar "$TOKEN")"
  yoxla "GET /hesabatlar/icmal"    "200" "$(kod GET /hesabatlar/icmal "$TOKEN")"
  printf "    ${BOZ}   401 olsa: JWT_SECRET .env-də təyin olunmayıb,${SIFIR}\n"
  printf "    ${BOZ}   JwtModule.register() əvəzinə registerAsync() işlədin${SIFIR}\n"

  alt "Token FAYLDAN oxunur (yadda saxlama işləyir)"
  token_oxu
  yoxla "Fayldan oxunan token işləyir" "200" "$(kod GET /struktur/merkezler "$TOKEN")"

  alt "TAM BACKEND — bütün əsas endpoint-lər 200"
  for yol in struktur/merkezler struktur/merkezler/statistika kadrlar/emekdaslar \
             hesabatlar/icmal ai/statistika; do
    yoxla "GET /$yol" "200" "$(kod GET "/$yol" "$TOKEN")"
  done
}

# ══════════════════════════════════════════════════════════════════════
addim_14() {
  bashliq 14 "AuthService — login və timing attack qoruması" "§14"

  server_lazim || return

  alt "LOKAL — düzgün giriş"
  local cavab
  cavab=$(curl -s -X POST "$API/auth/login" -H 'Content-Type: application/json' \
    -d '{"email":"admin@arti.edu.az","parol":"123456"}' 2>/dev/null)
  daxildir "Token qaytarılır" '"token"' "$cavab"
  daxildir "İstifadəçi məlumatı gəlir" '"istifadeci"' "$cavab"
  daxildir "Rol gəlir" '"rol"' "$cavab"

  alt "⚠️ parol_hash SIZMIR"
  yoxdur "Cavabda bcrypt hash yoxdur" '\$2[aby]\$' "$cavab"
  yoxdur "Cavabda 'parol_hash' açarı yoxdur" 'parol_hash' "$cavab"

  alt "Səhv şifrə → 401"
  yoxla "Səhv şifrə" "401" \
    "$(kod_cisim POST /auth/login '{"email":"admin@arti.edu.az","parol":"sehv-sifre-2026"}')"

  alt "⚠️ TIMING ATTACK QORUMASI — mesaj EYNİ olmalıdır"
  local m1 m2
  m1=$(curl -s -X POST "$API/auth/login" -H 'Content-Type: application/json' \
    -d '{"email":"yoxdur@arti.edu.az","parol":"sehv-sifre-2026"}' 2>/dev/null \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['xeta']['mesaj'])" 2>/dev/null)
  m2=$(curl -s -X POST "$API/auth/login" -H 'Content-Type: application/json' \
    -d '{"email":"admin@arti.edu.az","parol":"sehv-sifre-2026"}' 2>/dev/null \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['xeta']['mesaj'])" 2>/dev/null)
  yoxla "Mövcud olmayan email = səhv şifrə mesajı" "$m1" "$m2"
  printf "    ${BOZ}   → \"%s\"${SIFIR}\n" "$m1"

  alt "Validasiya — qısa şifrə / pis email"
  yoxla "parol='123' → 400" "400" \
    "$(kod_cisim POST /auth/login '{"email":"admin@arti.edu.az","parol":"123"}')"
  yoxla "email='pis' → 400" "400" \
    "$(kod_cisim POST /auth/login '{"email":"pis","parol":"123456"}')"
  yoxla "boş cisim → 400" "400" "$(kod_cisim POST /auth/login '{}')"

  alt "TAM BACKEND — bütün 4 rol giriş edə bilir"
  # ⚠️ JSON cismi MÜTLƏQ dəyişənə yazılmalıdır — nested $( ) içində \" pozulur
  local cisim
  for rol in admin muhendis maliyyeci baxici; do
    cisim="{\"email\":\"$rol@arti.edu.az\",\"parol\":\"123456\"}"
    yoxla "$rol girişi" "200" "$(kod_cisim POST /auth/login "$cisim")"
  done
}

# ══════════════════════════════════════════════════════════════════════
addim_15() {
  bashliq 15 "AuthController — 4 endpoint" "§15"

  server_lazim || return

  fayl_var "src/auth/auth.controller.ts" "AuthController"

  token_al admin
  local ta="$TOKEN"

  alt "GET /auth/profil — cari istifadəçi"
  local profil
  profil=$(curl -s -H "Authorization: Bearer $ta" "$API/auth/profil" 2>/dev/null)
  daxildir "email gəlir" "admin@arti.edu.az" "$profil"
  daxildir "rol gəlir" "admin" "$profil"

  alt "⚠️ POST /auth/login → 200 (201 DEYİL — @HttpCode)"
  yoxla "Login kodu 200" "200" \
    "$(kod_cisim POST /auth/login '{"email":"admin@arti.edu.az","parol":"123456"}')"

  alt "GET /auth/istifadeciler — yalnız admin"
  yoxla "admin → 200" "200" "$(kod GET /auth/istifadeciler "$ta")"
  token_al baxici
  yoxla "baxici → 403" "403" "$(kod GET /auth/istifadeciler "$TOKEN")"
  token_al muhendis
  yoxla "muhendis → 403" "403" "$(kod GET /auth/istifadeciler "$TOKEN")"

  alt "POST /auth/qeydiyyat — yalnız admin"
  yoxla "baxici → 403" "403" \
    "$(kod_cisim POST /auth/qeydiyyat '{"email":"x@arti.edu.az","parol":"12345678","ad_soyad":"Test Testov"}' "$TOKEN")"

  alt "TAM BACKEND — /auth/profil tokensiz 401"
  yoxla "GET /auth/profil tokensiz" "401" "$(kod GET /auth/profil)"
}

# ══════════════════════════════════════════════════════════════════════
addim_16() {
  bashliq 16 "AuthModule — registerAsync işlədilir?" "§16"

  fayl_var "src/auth/auth.module.ts" "AuthModule"
  local m; m=$(cat src/auth/auth.module.ts 2>/dev/null)
  daxildir "registerAsync işlədilir" "registerAsync" "$m"
  daxildir "ConfigService işlədilir" "ConfigService" "$m"
  daxildir "JwtStrategy providers-də" "JwtStrategy" "$m"
  daxildir "⚠️ secret ConfigService-dən gəlir" "config.get" "$m"

  alt "⚠️ Köhnə register() işlədilmir (açar uyğunsuzluğu xətası)"
  # Şərhləri çıxar — şərhlərdə 'register()' sözü keçə bilər
  local kodsuz
  kodsuz=$(printf '%s' "$m" \
    | grep -v '^[[:space:]]*\*' \
    | grep -v '^[[:space:]]*//' \
    | grep -v '^[[:space:]]*/\*')
  yoxdur "Kodda JwtModule.register( YOXDUR" 'JwtModule\.register(' "$kodsuz"
  daxildir "Kodda JwtModule.registerAsync( VAR" 'JwtModule\.registerAsync(' "$kodsuz"

  alt "⚠️ .env-də JWT_SECRET var"
  daxildir "JWT_SECRET təyin olunub" 'JWT_SECRET=' "$(cat .env 2>/dev/null)"
  daxildir "JWT_MUDDET təyin olunub" 'JWT_MUDDET=' "$(cat .env 2>/dev/null)"
  yoxdur "JWT_SECRET boş deyil" 'JWT_SECRET=""' "$(cat .env 2>/dev/null)"

  alt "TAM BACKEND — build"
  if npm run build >/dev/null 2>&1; then
    yoxla "npm run build" "exit 0" "exit 0"
  else
    yoxla "npm run build" "exit 0" "XƏTA"
  fi
}

# ══════════════════════════════════════════════════════════════════════
addim_17() {
  bashliq 17 "AuditInterceptor — jurnal yazır?" "§17"

  fayl_var "src/common/interceptors/audit.interceptor.ts" "AuditInterceptor"
  local m; m=$(cat src/common/interceptors/audit.interceptor.ts 2>/dev/null)
  daxildir "Yalnız POST/PATCH/PUT/DELETE izlənir" "'POST'" "$m"
  daxildir "Oxuma əməliyyatları buraxılır" "IZLENEN_METODLAR" "$m"
  daxildir "Xəta da jurnala yazılır" "error:" "$m"
  daxildir "⚠️ Audit xətası əsas əməliyyatı pozmur" "catch" "$m"

  server_lazim || return

  token_al admin
  local ta="$TOKEN" evvel sonra yeni_id

  evvel=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT count(*)::int FROM audit.audit_log" 2>/dev/null || echo 0)

  alt "Yazma əməliyyatı et (POST /struktur/merkezler)"
  yeni_id=$(curl -s -X POST "$API/struktur/merkezler" \
    -H "Authorization: Bearer $ta" -H 'Content-Type: application/json' \
    -d "{\"ad\":\"Audit Yoxlama $(date +%s)\"}" 2>/dev/null \
    | python3 -c "import json,sys;print(json.load(sys.stdin).get('id',''))" 2>/dev/null)

  sleep 1
  sonra=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT count(*)::int FROM audit.audit_log" 2>/dev/null || echo 0)
  yoxla "Audit qeydi əlavə olundu" "1" "$([ "$sonra" -gt "$evvel" ] && echo 1 || echo 0)"

  alt "Jurnalda düzgün məlumat"
  local q
  q=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT cedvel_adi||'|'||emeliyyat||'|'||COALESCE(istifadeci,'?')
       FROM audit.audit_log ORDER BY id DESC LIMIT 1" 2>/dev/null)
  daxildir "Cədvəl adı 'struktur.merkezler'" "struktur.merkezler" "$q"
  daxildir "Əməliyyat 'POST'" "POST" "$q"
  daxildir "İstifadəçi email-i yazılıb" "admin@arti.edu.az" "$q"

  alt "⚠️ Oxuma (GET) jurnala DÜŞMÜR"
  evvel=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT count(*)::int FROM audit.audit_log" 2>/dev/null || echo 0)
  kod GET /struktur/merkezler "$ta" >/dev/null
  kod GET /kadrlar/emekdaslar "$ta" >/dev/null
  kod GET /hesabatlar/icmal "$ta" >/dev/null
  sleep 1
  sonra=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT count(*)::int FROM audit.audit_log" 2>/dev/null || echo 0)
  yoxla "3 GET sorğusu jurnala yazılmadı" "$evvel" "$sonra"

  # Təmizlik
  if [ -n "$yeni_id" ]; then
    curl -s -o /dev/null -X DELETE "$API/struktur/merkezler/$yeni_id" \
      -H "Authorization: Bearer $ta" 2>/dev/null
    printf "    ${BOZ}   → test mərkəzi #%s silindi${SIFIR}\n" "$yeni_id"
  fi
}

# ══════════════════════════════════════════════════════════════════════
addim_18() {
  bashliq 18 "app.module.ts — guard sırası düzgündür?" "§18"

  fayl_var "src/app.module.ts" "app.module.ts"
  local m; m=$(cat src/app.module.ts 2>/dev/null)
  daxildir "APP_GUARD işlədilir" "APP_GUARD" "$m"
  daxildir "APP_INTERCEPTOR işlədilir" "APP_INTERCEPTOR" "$m"
  daxildir "JwtAuthGuard qeydiyyatda" "JwtAuthGuard" "$m"
  daxildir "RolesGuard qeydiyyatda" "RolesGuard" "$m"
  daxildir "AuditInterceptor qeydiyyatda" "AuditInterceptor" "$m"
  daxildir "AuthModule import olunub" "AuthModule" "$m"

  alt "⚠️ GUARD SIRASI — JwtAuthGuard ƏVVƏL olmalıdır"
  local s1 s2 s3
  s1=$(grep -n 'JwtAuthGuard' src/app.module.ts | head -1 | cut -d: -f1)
  s2=$(grep -n 'RolesGuard'    src/app.module.ts | head -1 | cut -d: -f1)
  s3=$(grep -n 'AuditInterceptor' src/app.module.ts | head -1 | cut -d: -f1)
  yoxla "JwtAuthGuard → RolesGuard sırası" "1" \
    "$([ -n "$s1" ] && [ -n "$s2" ] && [ "$s1" -lt "$s2" ] && echo 1 || echo 0)"
  printf "    ${BOZ}   → JwtAuthGuard: sətir %s | RolesGuard: %s | Audit: %s${SIFIR}\n" "$s1" "$s2" "$s3"

  alt "TAM BACKEND — bütün modullar import olunub"
  for mod in PrismaModule SaglamliqModule AuthModule StrukturModule KadrlarModule \
             HesabatlarModule AiModule IxracModule; do
    daxildir "$mod" "$mod" "$m"
  done
}

# ══════════════════════════════════════════════════════════════════════
addim_19() {
  bashliq 19 "RBAC matrisi — rol icazələri" "§19"

  server_lazim || return

  token_al admin;     local T_admin="$TOKEN"
  token_al muhendis;  local T_muhendis="$TOKEN"
  token_al maliyyeci; local T_maliyyeci="$TOKEN"
  token_al baxici;    local T_baxici="$TOKEN"

  local YARADILANLAR=""

  alt "POST /struktur/merkezler → admin, muhendis: 201 | maliyyeci, baxici: 403"
  local cisim t c id
  for rol in admin muhendis; do
    eval "t=\$T_$rol"
    cisim="{\"ad\":\"RBAC $rol $(date +%s)\"}"
    c=$(curl -s -X POST "$API/struktur/merkezler" -H "Authorization: Bearer $t" \
      -H 'Content-Type: application/json' -d "$cisim" 2>/dev/null)
    id=$(printf '%s' "$c" | python3 -c "import json,sys;print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
    [ -n "$id" ] && YARADILANLAR="$YARADILANLAR $id"
    yoxla "$rol → 201" "201" "$([ -n "$id" ] && echo 201 || echo XƏTA)"
  done
  for rol in maliyyeci baxici; do
    eval "t=\$T_$rol"
    cisim="{\"ad\":\"RBAC $rol $(date +%s)\"}"
    yoxla "$rol → 403" "403" "$(kod_cisim POST /struktur/merkezler "$cisim" "$t")"
  done

  alt "DELETE /struktur/merkezler/:id → yalnız admin: 200 | digərləri: 403"
  set -- $YARADILANLAR
  local ilk="${1:-}"
  if [ -n "$ilk" ]; then
    yoxla "muhendis → 403" "403" "$(kod DELETE "/struktur/merkezler/$ilk" "$T_muhendis")"
    yoxla "maliyyeci → 403" "403" "$(kod DELETE "/struktur/merkezler/$ilk" "$T_maliyyeci")"
    yoxla "admin → 200" "200" "$(kod DELETE "/struktur/merkezler/$ilk" "$T_admin")"
  else
    yoxla "Test mərkəzi yaradıldı" "var" "YOXDUR"
  fi

  alt "⚠️ BAĞLI mərkəz 409 verməlidir (500 DEYİL)"
  yoxla "DELETE /merkezler/1 → 409" "409" "$(kod DELETE /struktur/merkezler/1 "$T_admin")"
  printf "    ${BOZ}   500 olsa: sil() bütün 3 FK-nı yoxlamır${SIFIR}\n"

  alt "GET /auth/istifadeciler → yalnız admin"
  for rol in admin muhendis maliyyeci baxici; do
    eval "local t=\$T_$rol"
    local goz="403"; [ "$rol" = "admin" ] && goz="200"
    yoxla "$rol → $goz" "$goz" "$(kod GET /auth/istifadeciler "$t")"
  done

  alt "TAM BACKEND — bütün oxuma endpoint-ləri baxici ilə açıqdır"
  for yol in struktur/merkezler struktur/merkezler/statistika \
             kadrlar/emekdaslar kadrlar/emekdaslar/icmal \
             hesabatlar/icmal ai/statistika; do
    yoxla "baxici GET /$yol" "200" "$(kod GET "/$yol" "$T_baxici")"
  done

  alt "TAM BACKEND — yazma əməliyyatları bağlıdır"
  yoxla "maliyyeci POST /struktur/merkezler" "403" \
    "$(kod_cisim POST /struktur/merkezler '{"ad":"RBAC qadağan"}' "$T_maliyyeci")"
  yoxla "baxici POST /auth/qeydiyyat" "403" \
    "$(kod_cisim POST /auth/qeydiyyat '{"email":"qadagan@arti.edu.az","parol":"12345678","ad_soyad":"Test Testov"}' "$T_baxici")"

  # Təmizlik
  local qalan=0
  for x in $YARADILANLAR; do
    [ "$x" = "$ilk" ] && continue
    curl -s -o /dev/null -X DELETE "$API/struktur/merkezler/$x" \
      -H "Authorization: Bearer $T_admin" 2>/dev/null
    qalan=$((qalan + 1))
  done
  printf "    ${BOZ}   → %s test mərkəzi təmizləndi${SIFIR}\n" "$qalan"
}

# ══════════════════════════════════════════════════════════════════════
addim_20() {
  bashliq 20 "Seed skripti — istifadəçilər yaradılır?" "§20"

  fayl_var "scripts/seed-auth.ts" "seed-auth.ts"
  daxildir "package.json-da seed:auth" 'seed:auth' "$(cat package.json 2>/dev/null)"
  daxildir "tsx devDependencies-də" '"tsx"' "$(cat package.json 2>/dev/null)"
  daxildir "⚠️ process.env DATABASE_URL oxunur" "DATABASE_URL" "$(cat scripts/seed-auth.ts 2>/dev/null)"
  daxildir "bcrypt hash işlədilir" "hashSync\|hash(" "$(cat scripts/seed-auth.ts 2>/dev/null)"
  daxildir "⚠️ Idempotent (upsert / ON CONFLICT)" "upsert\|ON CONFLICT\|update" \
    "$(cat scripts/seed-auth.ts 2>/dev/null)"

  alt "Seed-i işə sal (2 dəfə — idempotent olmalıdır)"
  if npm run seed:auth >/dev/null 2>&1; then
    yoxla "1-ci işə salma" "exit 0" "exit 0"
  else
    yoxla "1-ci işə salma" "exit 0" "XƏTA"
    printf "    ${BOZ}   'tsx' quraşdırılıbmı? → npm install -D tsx@^4.19.0${SIFIR}\n"
  fi
  local birinci
  birinci=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT count(*)::int FROM kadrlar.istifadeciler" 2>/dev/null || echo 0)

  npm run seed:auth >/dev/null 2>&1
  local ikinci
  ikinci=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
    "SELECT count(*)::int FROM kadrlar.istifadeciler" 2>/dev/null || echo 0)
  yoxla "⚠️ 2-ci işə salma eyni say (idempotent)" "$birinci" "$ikinci"

  alt "Bazada 4 istifadəçi"
  yoxla "İstifadəçi sayı 4" "4" "$ikinci"

  alt "Hər rol mövcuddur"
  for rol in admin muhendis maliyyeci baxici; do
    local n
    n=$(psql -U "$DB_ISTIFADECI" -w -d "$BAZA" -tAc \
      "SELECT count(*)::int FROM kadrlar.istifadeciler WHERE rol='$rol'" 2>/dev/null || echo 0)
    yoxla "$rol rolu" "1" "$n"
  done

  alt "TAM BACKEND — seed-dən sonra giriş işləyir"
  if [ "$SERVER_VAR" -eq 1 ]; then
    yoxla "admin girişi" "200" \
      "$(kod_cisim POST /auth/login '{"email":"admin@arti.edu.az","parol":"123456"}')"
    yoxla "baxici girişi" "200" \
      "$(kod_cisim POST /auth/login '{"email":"baxici@arti.edu.az","parol":"123456"}')"
  else
    printf "    ${SARI}⚠${SIFIR}  Server işləmir — giriş yoxlanılmadı\n"
    ATLANDI=$((ATLANDI + 1))
  fi
}

# ══════════════════════════════════════════════════════════════════════
addim_21() {
  bashliq 21 "Testlər — unit + e2e" "§21"

  fayl_var "src/auth/auth.service.spec.ts" "Auth unit testləri"
  fayl_var "test/backend3.e2e-spec.ts" "Backend-3 e2e testləri"
  fayl_var "vitest.config.ts" "vitest.config.ts"
  fayl_var "vitest.config.e2e.ts" "vitest.config.e2e.ts"

  alt "⚠️ e2e testləri unit konfiqurasiyasından XARİC edilib"
  daxildir "exclude: e2e-spec" "e2e-spec" "$(cat vitest.config.ts 2>/dev/null)"

  alt "Unit testlər"
  local unit
  unit=$(NO_COLOR=1 npm test 2>&1 | grep -E '^\s*Tests\s' | grep -oE '[0-9]+ passed' | grep -oE '^[0-9]+' | head -1)
  yoxla "Unit testlər keçir" "1" "$([ "${unit:-0}" -gt 0 ] && echo 1 || echo 0)"
  printf "    ${BOZ}   → %s test${SIFIR}\n" "${unit:-0}"

  alt "e2e testlər"
  local e2e
  e2e=$(NO_COLOR=1 npx vitest run --config vitest.config.e2e.ts 2>&1 \
    | grep -E '^\s*Tests\s' | grep -oE '[0-9]+ passed' | grep -oE '^[0-9]+' | head -1)
  yoxla "e2e testlər keçir" "1" "$([ "${e2e:-0}" -gt 0 ] && echo 1 || echo 0)"
  printf "    ${BOZ}   → %s test${SIFIR}\n" "${e2e:-0}"

  alt "TAM BACKEND — build"
  if npm run build >/dev/null 2>&1; then
    yoxla "npm run build" "exit 0" "exit 0"
  else
    yoxla "npm run build" "exit 0" "XƏTA"
  fi
}

# ══════════════════════════════════════════════════════════════════════
addim_22() {
  bashliq 22 "Backend-2 testləri token ilə yeniləndimi?" "§22"

  fayl_var "test/backend2.e2e-spec.ts" "backend2.e2e-spec.ts"
  local m; m=$(cat test/backend2.e2e-spec.ts 2>/dev/null)

  daxildir "Token dəyişəni var" "token" "$m"
  daxildir "api() köməkçisi var" "const api" "$m"
  daxildir "Login beforeAll-da" "auth/login" "$m"
  daxildir "Bearer başlığı əlavə olunur" "Bearer" "$m"

  alt "⚠️ Sonsuz rekursiya yoxdur (api() özünü çağırmır)"
  yoxdur "api() özünü çağırmır" 'const api = () =>[[:space:]]*api()' "$m"

  alt "TAM BACKEND — backend2 e2e testləri keçir"
  local n
  n=$(test_sayi "test/backend2.e2e-spec.ts")
  yoxla "backend2.e2e keçir" "1" "$([ "${n:-0}" -gt 0 ] && echo 1 || echo 0)"
  printf "    ${BOZ}   → %s test${SIFIR}\n" "${n:-0}"

  alt "Bütün e2e faylları"
  ls test/*.e2e-spec.ts 2>/dev/null | while read -r f; do
    printf "    ${BOZ}   • %s${SIFIR}\n" "$f"
  done
}

# ══════════════════════════════════════════════════════════════════════
siyahi() {
  cat <<'SIYAHISON'
  ══════════════════════════════════════════════════════════════
   DS_Backend-3 — ADDIM-ADDIM YOXLAMA SİYAHISI
  ══════════════════════════════════════════════════════════════
    N   NƏ YOXLANILIR                                   DƏRS
   ─────────────────────────────────────────────────────────────
    1   Mühit (node, baza, 48 cədvəl)                    §2
    2   Auth paketləri (5 paket + tsx)                   §2
    4   JWT token strukturu (offline)                    §4
    6   bcrypt hash/compare (offline)                    §6
    7   DTO validasiya qaydaları                         §7
    9   Dekoratorlar + build                             §9
   10   JwtStrategy                                      §10
   11   JwtAuthGuard → tokensiz 401                      §11
   12   RolesGuard → rol yoxlaması                       §12
   13   ⚠  Açar uyğunluğu → token al, yadda saxla        §13
   14   AuthService → login + timing attack              §14
   15   AuthController → 4 endpoint                      §15
   16   AuthModule → registerAsync                       §16
   17   AuditInterceptor → jurnal                        §17
   18   app.module → guard sırası                        §18
   19   RBAC matrisi (4 rol × əməliyyat)                 §19
   20   Seed → 4 istifadəçi (idempotent)                 §20
   21   Testlər (unit + e2e)                             §21
   22   Backend-2 testləri (token ilə)                   §22
   ─────────────────────────────────────────────────────────────
    hamisi  — 1→22 hamısı
    7 12    — 7-dən 12-yə qədər
    13      — yalnız 13-cü addım
  ══════════════════════════════════════════════════════════════
  Server tələb edən addımlar: 11, 12, 13, 14, 15, 17, 19, 20
  Server: npm run start:dev
SIYAHISON
}

icra_et() {
  case "$1" in
    1)  addim_1  ;;   2)  addim_2  ;;   4)  addim_4  ;;
    6)  addim_6  ;;   7)  addim_7  ;;   9)  addim_9  ;;
    10) addim_10 ;;   11) addim_11 ;;   12) addim_12 ;;
    13) addim_13 ;;   14) addim_14 ;;   15) addim_15 ;;
    16) addim_16 ;;   17) addim_17 ;;   18) addim_18 ;;
    19) addim_19 ;;   20) addim_20 ;;   21) addim_21 ;;
    22) addim_22 ;;
    *)  printf "${SARI}  ⚠  %s nömrəli addım yoxdur${SIFIR}\n" "$1" ;;
  esac
}

# ── GİRİŞ ─────────────────────────────────────────────────────────────
cd "$(dirname "$0")/.." 2>/dev/null || { echo "XƏTA: layihə qovluğu tapılmadı"; exit 1; }

BUTUN_ADDIMLAR="1 2 4 6 7 9 10 11 12 13 14 15 16 17 18 19 20 21 22"

# Server işləyirmi?
if curl -s -o /dev/null --max-time 3 "$API/saglamliq" 2>/dev/null; then
  SERVER_VAR=1
else
  SERVER_VAR=$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 "$API/saglamliq" 2>/dev/null)
  case "$SERVER_VAR" in
    200) SERVER_VAR=1 ;;
    *)   SERVER_VAR=0 ;;
  esac
fi

case "${1:-hamisi}" in
  siyahi|-s|--siyahi)
    siyahi
    exit 0
    ;;
  hamisi|-h|--hamisi|"")
    printf "\n${MAVI}╔══════════════════════════════════════════════════════════════╗${SIFIR}\n"
    printf   "${MAVI}║   DS_Backend-3 — TAM ADDIM-ADDIM YOXLAMA                    ║${SIFIR}\n"
    printf   "${MAVI}╚══════════════════════════════════════════════════════════════╝${SIFIR}\n"
    if [ "$SERVER_VAR" -eq 1 ]; then
      printf "  ${YASIL}●${SIFIR} Server: ${YASIL}işləyir${SIFIR} — %s\n" "$API"
    else
      printf "  ${SARI}●${SIFIR} Server: ${SARI}işləmir${SIFIR} — canlı yoxlamalar atlanacaq\n"
      printf "  ${BOZ}  Ayrı terminalda: npm run start:dev${SIFIR}\n"
    fi
    for n in $BUTUN_ADDIMLAR; do icra_et "$n"; done
    ;;
  *)
    if [ -n "${2:-}" ]; then
      for n in $BUTUN_ADDIMLAR; do
        if [ "$n" -ge "$1" ] && [ "$n" -le "$2" ]; then icra_et "$n"; fi
      done
    else
      icra_et "$1"
    fi
    ;;
esac

printf "\n${MAVI}══════════════════════════════════════════════════════════════${SIFIR}\n"
printf "  NƏTİCƏ:  ${YASIL}%d keçdi${SIFIR}" "$KECDI"
[ "$XETA" -gt 0 ] && printf "   ${QIRMIZI}%d xəta${SIFIR}" "$XETA"
[ "$ATLANDI" -gt 0 ] && printf "   ${SARI}%d atlandı${SIFIR}" "$ATLANDI"
printf "\n"
if [ "$XETA" -eq 0 ]; then
  printf "  ${YASIL}✅ BÜTÜN YOXLAMALAR KEÇDİ${SIFIR}\n"
else
  printf "  ${QIRMIZI}❌ %d YOXLAMA UĞURSUZ${SIFIR}\n" "$XETA"
fi
printf "${MAVI}══════════════════════════════════════════════════════════════${SIFIR}\n\n"

[ "$XETA" -eq 0 ]
