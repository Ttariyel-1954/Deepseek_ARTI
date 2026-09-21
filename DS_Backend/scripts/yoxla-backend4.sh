#!/bin/bash
# ══════════════════════════════════════════════════════════════════════
#  BACKEND-4 — TAM QƏBUL TESTİ
#
#  Bu dərsdə əlavə edilən HƏR yeniliyi bir-bir yoxlayır:
#    • exceljs paketi və DEEPSEEK_* dəyişənləri
#    • EmbeddingService — 64 ölçülü normallaşdırılmış vektor
#    • RagService — sənədlər arasında kosinus axtarışı
#    • SqlKomlekciService — 10 reseptli AĞ SİYAHI (LLM SQL YAZMIR)
#    • Resept SIRASI — xüsusi «orta maaş» ümumi «maaş»-dan əvvəl
#    • DeepseekService — API açarı olmadan DEMO REJİM
#    • 6 AI + 2 Excel endpoint, RBAC matrisi ilə (cəmi 23 marshrut)
#    • SQL inyeksiya cəhdi — baza salamat qalır
#    • Excel faylının həqiqətən .xlsx olduğu (PK baytları)
#    • Excel sətirlərinin baza ilə üst-üstə düşməsi
#    • Dockerfile, docker-compose və GitHub Actions CI
#    • 42 unit + 39 e2e test
#
#  İSTİFADƏ:
#    # 1) Server ayrı terminalda işləməlidir:
#    PORT=4000 npm run start:prod
#    # 2) Digər terminalda:
#    bash scripts/yoxla-backend4.sh
# ══════════════════════════════════════════════════════════════════════

unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"

A="${A:-http://localhost:4000/api/v1}"
KOK="${A%/api/v1}"
BAZA="${BAZA:-arti_baza}"
DB_ISTIFADECI="${DB_ISTIFADECI:-arti_user}"
PAROL="${PAROL:-123456}"

YASIL=$'\033[32m'; QIRMIZI=$'\033[31m'; SARI=$'\033[33m'
MAVI=$'\033[36m';  BOZ=$'\033[90m';     SIFIR=$'\033[0m'

KECDI=0; XETA=0

# ── KÖMƏKÇİLƏR ────────────────────────────────────────────────────────
bashliq() {
  printf "\n${MAVI}════════════════════════════════════════════════════════════${SIFIR}\n"
  printf "${MAVI}  %s${SIFIR}\n" "$1"
  printf "${MAVI}════════════════════════════════════════════════════════════${SIFIR}\n"
}

yoxla() {   # yoxla "ad" "gözlənilən" "faktiki"
  if [ "$2" = "$3" ]; then
    printf "  ${YASIL}✓${SIFIR} %-50s ${BOZ}%s${SIFIR}\n" "$1" "$3"
    KECDI=$((KECDI + 1))
  else
    printf "  ${QIRMIZI}✗${SIFIR} %-50s ${QIRMIZI}%s${SIFIR} ${BOZ}(gözlənilən: %s)${SIFIR}\n" \
      "$1" "$3" "$2"
    XETA=$((XETA + 1))
  fi
}

# kod "metod" "yol" [token]
kod() {
  if [ -n "${3:-}" ]; then
    curl -s -o /dev/null -w '%{http_code}' -X "$1" "$A/$2" \
      -H "Authorization: Bearer $3" 2>/dev/null
  else
    curl -s -o /dev/null -w '%{http_code}' -X "$1" "$A/$2" 2>/dev/null
  fi
}

# kod_cisim "yol" "cisim" [token]
kod_cisim() {
  if [ -n "${3:-}" ]; then
    curl -s -o /dev/null -w '%{http_code}' -X POST "$A/$1" \
      -H 'Content-Type: application/json' \
      -H "Authorization: Bearer $3" -d "$2" 2>/dev/null
  else
    curl -s -o /dev/null -w '%{http_code}' -X POST "$A/$1" \
      -H 'Content-Type: application/json' -d "$2" 2>/dev/null
  fi
}

# getir "yol" [token] → gövdə
getir() {
  if [ -n "${2:-}" ]; then
    curl -s "$A/$1" -H "Authorization: Bearer $2" 2>/dev/null
  else
    curl -s "$A/$1" 2>/dev/null
  fi
}

# gonder "yol" "cisim" [token] → gövdə
gonder() {
  if [ -n "${3:-}" ]; then
    curl -s -X POST "$A/$1" -H 'Content-Type: application/json' \
      -H "Authorization: Bearer $3" -d "$2" 2>/dev/null
  else
    curl -s -X POST "$A/$1" -H 'Content-Type: application/json' -d "$2" 2>/dev/null
  fi
}

# sahe "cisim" "açar" → sadə skalyar dəyər
sahe() {
  printf '%s' "$1" | grep -o "\"$2\":[^,}]*" | head -1 | sed "s/\"$2\"://" \
    | sed 's/^"//; s/"$//'
}

# sayi "cisim" "açar" → massivdəki element sayı (sadə üsul)
sayi() {
  printf '%s' "$1" | grep -o "\"$2\"" | wc -l | tr -d ' '
}

psq() { psql -U "$DB_ISTIFADECI" -d "$BAZA" -tA -c "$1" 2>/dev/null; }

# ── 0 · GİRİŞ ─────────────────────────────────────────────────────────
bashliq "0 · GİRİŞ — dörd rol üçün token"

gir() {   # gir "email"
  local c
  c="$(gonder 'auth/login' "{\"email\":\"$1\",\"parol\":\"$PAROL\"}")"
  printf '%s' "$c" | grep -o '"token":"[^"]*"' | head -1 | sed 's/"token":"//; s/"$//'
}

ADMIN="$(gir 'admin@arti.edu.az')"
MUHENDIS="$(gir 'muhendis@arti.edu.az')"
MALIYYECI="$(gir 'maliyyeci@arti.edu.az')"
BAXICI="$(gir 'baxici@arti.edu.az')"

yoxla "admin token alındı"     "var" "$([ -n "$ADMIN" ]     && echo var || echo yox)"
yoxla "muhendis token alındı"  "var" "$([ -n "$MUHENDIS" ]  && echo var || echo yox)"
yoxla "maliyyeci token alındı" "var" "$([ -n "$MALIYYECI" ] && echo var || echo yox)"
yoxla "baxici token alındı"    "var" "$([ -n "$BAXICI" ]    && echo var || echo yox)"

if [ -z "$ADMIN" ]; then
  printf "\n${QIRMIZI}Server işləmir və ya seed edilməyib — test dayandırıldı.${SIFIR}\n"
  printf "${SARI}  Əvvəlcə: PORT=4000 npm run start:prod${SIFIR}\n"
  exit 1
fi

# ── 1 · FAYLLAR VƏ PAKETLƏR ───────────────────────────────────────────
bashliq "1 · ADDIM 1, 2, 7, 8 — fayllar və paketlər"

yoxla "exceljs package.json-da"      "4.4.0" \
  "$(python3 -c "import json;print(json.load(open('package.json'))['dependencies'].get('exceljs','').lstrip('^'))" 2>/dev/null)"

yoxla "src/ai/embedding.service.ts"    "var" "$([ -f src/ai/embedding.service.ts ] && echo var || echo yox)"
yoxla "src/ai/rag.service.ts"          "var" "$([ -f src/ai/rag.service.ts ] && echo var || echo yox)"
yoxla "src/ai/sql-komlekci.service.ts" "var" "$([ -f src/ai/sql-komlekci.service.ts ] && echo var || echo yox)"
yoxla "src/ai/deepseek.service.ts"     "var" "$([ -f src/ai/deepseek.service.ts ] && echo var || echo yox)"
yoxla "src/ai/ai.service.ts"           "var" "$([ -f src/ai/ai.service.ts ] && echo var || echo yox)"
yoxla "src/ai/dto/sual.dto.ts"         "var" "$([ -f src/ai/dto/sual.dto.ts ] && echo var || echo yox)"
yoxla "src/ixrac/excel.service.ts"     "var" "$([ -f src/ixrac/excel.service.ts ] && echo var || echo yox)"
yoxla "Dockerfile"                     "var" "$([ -f Dockerfile ] && echo var || echo yox)"
yoxla ".dockerignore"                  "var" "$([ -f .dockerignore ] && echo var || echo yox)"
yoxla "docker-compose.yml"             "var" "$([ -f docker-compose.yml ] && echo var || echo yox)"
yoxla ".github/workflows/ci.yml"       "var" "$([ -f .github/workflows/ci.yml ] && echo var || echo yox)"

yoxla ".env → DEEPSEEK_API_KEY boşdur (demo)" "" \
  "$(grep '^DEEPSEEK_API_KEY=' .env | sed 's/^DEEPSEEK_API_KEY=//; s/"//g')"
yoxla ".env → DEEPSEEK_MODEL"  "deepseek-chat" \
  "$(grep '^DEEPSEEK_MODEL=' .env | sed 's/^DEEPSEEK_MODEL=//; s/"//g')"
yoxla ".env → DEEPSEEK_URL"    "https://api.deepseek.com" \
  "$(grep '^DEEPSEEK_URL=' .env | sed 's/^DEEPSEEK_URL=//; s/"//g')"

# ⚠️ TƏHLÜKƏSİZLİK: SQL xidməti LLM-ə qoşulmur, SQL koddadır
yoxla "sql-komlekci fetch çağırmır" "0" "$(grep -c 'fetch' src/ai/sql-komlekci.service.ts)"
yoxla "sql-komlekci DeepseekService-i import etmir" "0" \
  "$(grep -c 'deepseek' src/ai/sql-komlekci.service.ts)"

# ── 2 · GET /ai/statistika ────────────────────────────────────────────
bashliq "2 · GET /ai/statistika — AI qatının vəziyyəti (rol: HAMISI)"

yoxla "admin     → 200" "200" "$(kod GET 'ai/statistika' "$ADMIN")"
yoxla "muhendis  → 200" "200" "$(kod GET 'ai/statistika' "$MUHENDIS")"
yoxla "maliyyeci → 200" "200" "$(kod GET 'ai/statistika' "$MALIYYECI")"
yoxla "baxici    → 200" "200" "$(kod GET 'ai/statistika' "$BAXICI")"
yoxla "tokensiz  → 401" "401" "$(kod GET 'ai/statistika')"

ST="$(getir 'ai/statistika' "$ADMIN")"
yoxla "rejim = demo (açar boş)"  "demo" "$(sahe "$ST" rejim)"
yoxla "olcu = 64"                "64"   "$(sahe "$ST" olcu)"
yoxla "resept_sayi = 10"         "10"   "$(sahe "$ST" resept_sayi)"
yoxla "vektor bazası JSONB-dir"  "var" \
  "$(printf '%s' "$ST" | grep -q 'JSONB' && echo var || echo yox)"

# ── 3 · GET /ai/reseptler — AĞ SİYAHI VƏ SIRA ─────────────────────────
bashliq "3 · GET /ai/reseptler — 10 resept və SIRA qaydası"

RS="$(getir 'ai/reseptler' "$ADMIN")"
yoxla "resept sayı = 10"            "10" "$(sahe "$RS" say)"
yoxla "hər reseptdə 'açar' sahəsi"  "10" "$(sayi "$RS" 'açar')"
yoxla "hər reseptdə 'izah' sahəsi"  "10" "$(sayi "$RS" 'izah')"
yoxla "tokensiz → 401"              "401" "$(kod GET 'ai/reseptler')"

# Resept sırası: ADDIM 4-də tapılan REAL SƏHVİN qarşısını alır
IZAHLAR="$(printf '%s' "$RS" | grep -o '"izah":"[^"]*"' | sed 's/"izah":"//; s/"$//')"
ORTA="$(printf '%s\n' "$IZAHLAR" | grep -n 'Orta əmək haqqı' | cut -d: -f1)"
UMUMI="$(printf '%s\n' "$IZAHLAR" | grep -n 'Ən çox maaş alan' | cut -d: -f1)"
yoxla "«orta maaş» resepti mövcuddur"   "var" "$([ -n "$ORTA" ] && echo var || echo yox)"
yoxla "«ümumi maaş» resepti mövcuddur"  "var" "$([ -n "$UMUMI" ] && echo var || echo yox)"
yoxla "xüsusi resept ümumidən ƏVVƏLdir" "var" \
  "$([ -n "$ORTA" ] && [ -n "$UMUMI" ] && [ "$ORTA" -lt "$UMUMI" ] && echo var || echo yox)"

# ── 4 · POST /ai/sual — TƏBİİ DİL ─────────────────────────────────────
bashliq "4 · POST /ai/sual — təbii dil → cədvəl (LLM SQL YAZMIR)"

yoxla "«Neçə əməkdaş var?» → 200" "200" \
  "$(kod_cisim 'ai/sual' '{"sual":"Neçə əməkdaş var?"}' "$ADMIN")"

S1="$(gonder 'ai/sual' '{"sual":"Neçə əməkdaş var?"}' "$ADMIN")"
yoxla "uygun_resept = true"          "true" "$(sahe "$S1" uygun_resept)"
yoxla "izah = «Ümumi əməkdaş sayı»"  "Ümumi əməkdaş sayı" "$(sahe "$S1" izah)"
yoxla "setir_sayi ≥ 1"               "var" \
  "$([ "$(sahe "$S1" setir_sayi)" -ge 1 ] 2>/dev/null && echo var || echo yox)"

S2="$(gonder 'ai/sual' '{"sual":"Orta maaş nə qədərdir?"}' "$ADMIN")"
yoxla "«Orta maaş…» → xüsusi resept"      "Orta əmək haqqı" "$(sahe "$S2" izah)"
yoxla "«Orta maaş…» SƏHV reseptə düşmür"  "yox" \
  "$(printf '%s' "$(sahe "$S2" izah)" | grep -q 'Ən çox maaş' && echo var || echo yox)"

S3="$(gonder 'ai/sual' '{"sual":"Ən çox maaş alan kimdir?"}' "$ADMIN")"
yoxla "«Ən çox maaş…» → ümumi resept" "Ən çox maaş alan 5 nəfər" "$(sahe "$S3" izah)"

S4="$(gonder 'ai/sual' '{"sual":"Banana qiyməti nə qədərdir?"}' "$ADMIN")"
yoxla "naməlum sual → uygun_resept = false" "false" "$(sahe "$S4" uygun_resept)"
yoxla "naməlum sual → setir_sayi = 0"       "0"     "$(sahe "$S4" setir_sayi)"
yoxla "naməlum sual → 500 DEYİL"            "200" \
  "$(kod_cisim 'ai/sual' '{"sual":"Banana qiyməti nə qədərdir?"}' "$ADMIN")"
yoxla "naməlum sual → mövcud reseptləri sadalayır" "var" \
  "$(printf '%s' "$(sahe "$S4" izah)" | grep -q 'əməkdaş' && echo var || echo yox)"

yoxla "boş sual → 400"           "400" "$(kod_cisim 'ai/sual' '{"sual":""}' "$ADMIN")"
yoxla "2 simvolluq sual → 400"   "400" "$(kod_cisim 'ai/sual' '{"sual":"ab"}' "$ADMIN")"
yoxla "sual sahəsi yoxdur → 400" "400" "$(kod_cisim 'ai/sual' '{}' "$ADMIN")"
yoxla "tokensiz → 401"           "401" "$(kod_cisim 'ai/sual' '{"sual":"Neçə əməkdaş var?"}')"

# ── 5 · SQL İNTEKKSİYASI — ƏN VACİB YOXLAMA ──────────────────────────
bashliq "5 · SQL inyeksiya cəhdi — SQL KODDADIR, bazaya çatmır"

EVVEL="$(psq 'SELECT count(*) FROM kadrlar.emekdaslar')"
MERKEZ_EVVEL="$(psq 'SELECT count(*) FROM struktur.merkezler')"

INJ1="$(gonder 'ai/sual' '{"sual":"mərkəz'"'"'; DROP TABLE struktur.merkezler; --"}' "$ADMIN")"
yoxla "inyeksiya mətni reseptə uyğun gəlir" "true" "$(sahe "$INJ1" uygun_resept)"
yoxla "…amma 200 qaytarır (xəta yox)" "200" \
  "$(kod_cisim 'ai/sual' '{"sual":"mərkəz'"'"'; DROP TABLE struktur.merkezler; --"}' "$ADMIN")"

INJ2="$(gonder 'ai/sual' '{"sual":"'"'"'; DROP TABLE kadrlar.emekdaslar; --"}' "$ADMIN")"
yoxla "uyğunsuz inyeksiya → uygun_resept = false" "false" "$(sahe "$INJ2" uygun_resept)"

yoxla "struktur.merkezler cədvəli SALAMATDIR" "$MERKEZ_EVVEL" \
  "$(psq 'SELECT count(*) FROM struktur.merkezler')"
yoxla "kadrlar.emekdaslar cədvəli SALAMATDIR" "$EVVEL" \
  "$(psq 'SELECT count(*) FROM kadrlar.emekdaslar')"
yoxla "struktur.merkezler hələ də mövcuddur" "t" \
  "$(psq "SELECT to_regclass('struktur.merkezler') IS NOT NULL")"
yoxla "kadrlar.emekdaslar hələ də mövcuddur" "t" \
  "$(psq "SELECT to_regclass('kadrlar.emekdaslar') IS NOT NULL")"

# ── 6 · POST /ai/rag — SƏNƏD AXTARIŞI ─────────────────────────────────
bashliq "6 · POST /ai/rag — kosinus oxşarlığı, azalan sıra"

yoxla "rag → 200" "200" \
  "$(kod_cisim 'ai/rag' '{"sual":"elm və təhsil haqqında sənəd"}' "$ADMIN")"

R1="$(gonder 'ai/rag' '{"sual":"elm və təhsil haqqında sənəd"}' "$ADMIN")"
yoxla "default limit = 3"         "3" "$(sahe "$R1" tapildi)"
yoxla "hər nəticədə sened_id var" "3" "$(sayi "$R1" sened_id)"
yoxla "hər nəticədə oxsarlıq var" "3" "$(sayi "$R1" oxsarlıq)"

# ballar AZALAN sıradadır
BALLAR="$(printf '%s' "$R1" | grep -o '"oxsarlıq":[0-9.]*' | sed 's/.*://')"
yoxla "oxşarlıqlar AZALAN sıradadır" "" \
  "$(printf '%s\n' "$BALLAR" | awk 'NR>1 && $1>e {print "xeta"} {e=$1}')"

# ballar 0..1 aralığındadır (normallaşdırma olmasa 1-dən böyük olardı)
yoxla "ballar 0..1 aralığındadır" "" \
  "$(printf '%s\n' "$BALLAR" | awk '$1<0 || $1>1 {print "xeta"}' | head -1)"

yoxla "normallaşdırma: vahid vektor uzunluğu" "var" \
  "$(printf '%s' "$BALLAR" | grep -qE '^(0|1)\.[0-9]+$' && echo var || echo yox)"

R2="$(gonder 'ai/rag' '{"sual":"elm və təhsil haqqında sənəd","limit":1}' "$ADMIN")"
yoxla "limit=1 → 1 nəticə" "1" "$(sahe "$R2" tapildi)"

yoxla "limit=11 → 400 (Max 10)" "400" \
  "$(kod_cisim 'ai/rag' '{"sual":"elm və təhsil","limit":11}' "$ADMIN")"
yoxla "limit=0 → 400 (Min 1)"   "400" \
  "$(kod_cisim 'ai/rag' '{"sual":"elm və təhsil","limit":0}' "$ADMIN")"
yoxla "tokensiz → 401" "401" "$(kod_cisim 'ai/rag' '{"sual":"elm və təhsil"}')"

# ── 7 · POST /ai/cavab — DEMO REJİM ───────────────────────────────────
bashliq "7 · POST /ai/cavab — API açarı OLMADAN işləyir"

yoxla "cavab → 200" "200" \
  "$(kod_cisim 'ai/cavab' '{"sual":"Elmi dərəcə ilə bağlı sənədlər hansılardır?"}' "$ADMIN")"

C1="$(gonder 'ai/cavab' '{"sual":"Elmi dərəcə ilə bağlı sənədlər hansılardır?"}' "$ADMIN")"
yoxla "demo = true"            "true" "$(sahe "$C1" demo)"
yoxla "model adında «demo» işarəsi" "var" \
  "$(printf '%s' "$(sahe "$C1" model)" | grep -q 'demo' && echo var || echo yox)"
yoxla "cavab boş deyil"        "var" \
  "$([ -n "$(sahe "$C1" cavab)" ] && echo var || echo yox)"
yoxla "istifadə_olunan_senedler var" "var" \
  "$(printf '%s' "$C1" | grep -q 'istifade_olunan_senedler' && echo var || echo yox)"
yoxla "token_sayi = 0 (demo)"  "0" "$(sahe "$C1" token_sayi)"

# ── 8 · POST /ai/vektorlasdir — RBAC ──────────────────────────────────
bashliq "8 · POST /ai/vektorlasdir — RBAC (yalnız admin, mühendis)"

yoxla "admin     → 200" "200" "$(kod POST 'ai/vektorlasdir' "$ADMIN")"
yoxla "muhendis  → 200" "200" "$(kod POST 'ai/vektorlasdir' "$MUHENDIS")"
yoxla "maliyyeci → 403" "403" "$(kod POST 'ai/vektorlasdir' "$MALIYYECI")"
yoxla "baxici    → 403" "403" "$(kod POST 'ai/vektorlasdir' "$BAXICI")"
yoxla "tokensiz  → 401" "401" "$(kod POST 'ai/vektorlasdir')"

R403="$(gonder 'ai/vektorlasdir' '{}' "$BAXICI")"
yoxla "403 → xeta.kod = ICAZE_YOXDUR" "var" \
  "$(printf '%s' "$R403" | grep -q 'ICAZE_YOXDUR' && echo var || echo yox)"

ST2="$(getir 'ai/statistika' "$ADMIN")"
yoxla "vektorlaşdırmadan sonra embedding > 0" "var" \
  "$([ "$(sahe "$ST2" embedding_sayi)" -gt 0 ] 2>/dev/null && echo var || echo yox)"

# ── 9 · EXCEL İXRACI ──────────────────────────────────────────────────
bashliq "9 · GET /ixrac/*.xlsx — həqiqi Excel faylı"

M="/tmp/arti_merkezler.xlsx"; E="/tmp/arti_emekdaslar.xlsx"
rm -f "$M" "$E"

KM="$(curl -s -o "$M" -w '%{http_code}' "$A/ixrac/merkezler.xlsx" \
  -H "Authorization: Bearer $ADMIN")"
KE="$(curl -s -o "$E" -w '%{http_code}' "$A/ixrac/emekdaslar.xlsx" \
  -H "Authorization: Bearer $ADMIN")"

yoxla "merkezler.xlsx → 200"  "200" "$KM"
yoxla "emekdaslar.xlsx → 200" "200" "$KE"

CT="$(curl -s -o /dev/null -D - "$A/ixrac/merkezler.xlsx" \
  -H "Authorization: Bearer $ADMIN" | grep -i '^content-type' | tr -d '\r' \
  | sed 's/^[Cc]ontent-[Tt]ype: //')"
yoxla "Content-Type düzgündür" \
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" "$CT"

CD="$(curl -s -o /dev/null -D - "$A/ixrac/merkezler.xlsx" \
  -H "Authorization: Bearer $ADMIN" | grep -i '^content-disposition' | tr -d '\r')"
yoxla "Content-Disposition = attachment" "var" \
  "$(printf '%s' "$CD" | grep -q 'attachment' && echo var || echo yox)"
yoxla "fayl adı .xlsx ilə bitir" "var" \
  "$(printf '%s' "$CD" | grep -q '\.xlsx' && echo var || echo yox)"

# ⚠️ Ən vacib yoxlama: fayl həqiqətən ZIP-dir (xlsx = ZIP konteyneri), PK baytları
yoxla "merkezler PK baytları ilə başlayır" "504b" \
  "$(xxd -p -l 2 "$M" 2>/dev/null | tr 'A-Z' 'a-z')"
yoxla "emekdaslar PK baytları ilə başlayır" "504b" \
  "$(xxd -p -l 2 "$E" 2>/dev/null | tr 'A-Z' 'a-z')"

yoxla "merkezler ölçüsü > 5000 bayt" "var" \
  "$([ "$(wc -c < "$M" | tr -d ' ')" -gt 5000 ] && echo var || echo yox)"
yoxla "emekdaslar ölçüsü > 5000 bayt" "var" \
  "$([ "$(wc -c < "$E" | tr -d ' ')" -gt 5000 ] && echo var || echo yox)"

yoxla "file: merkezler = Excel 2007+" "var" \
  "$(file -b "$M" | grep -q 'Microsoft Excel 2007' && echo var || echo yox)"
yoxla "file: emekdaslar = Excel 2007+" "var" \
  "$(file -b "$E" | grep -q 'Microsoft Excel 2007' && echo var || echo yox)"

# Sətir sayı bazadakı ilə üst-üstə düşməlidir (+1 başlıq sətri)
DB_M="$(psq 'SELECT count(*) FROM struktur.merkezler')"
DB_E="$(psq 'SELECT count(*) FROM kadrlar.emekdaslar')"
XM="$(unzip -p "$M" xl/worksheets/sheet1.xml 2>/dev/null | grep -o '<row ' | wc -l | tr -d ' ')"
XE="$(unzip -p "$E" xl/worksheets/sheet1.xml 2>/dev/null | grep -o '<row ' | wc -l | tr -d ' ')"

yoxla "merkezler: Excel sətri = baza + başlıq"  "$((DB_M + 1))" "$XM"
yoxla "emekdaslar: Excel sətri = baza + başlıq" "$((DB_E + 1))" "$XE"
yoxla "Excel boş deyil (başlıqdan çox sətir)" "var" \
  "$([ "$XM" -gt 1 ] && echo var || echo yox)"

# İxrac oxuma əməliyyatıdır — dörd rolun hamısı ala bilər
yoxla "baxici    → merkezler.xlsx 200"  "200" "$(kod GET 'ixrac/merkezler.xlsx' "$BAXICI")"
yoxla "maliyyeci → emekdaslar.xlsx 200" "200" "$(kod GET 'ixrac/emekdaslar.xlsx' "$MALIYYECI")"
yoxla "tokensiz  → 401"                 "401" "$(kod GET 'ixrac/merkezler.xlsx')"

rm -f "$M" "$E"

# ── 10 · DOCKER VƏ CI/CD ──────────────────────────────────────────────
bashliq "10 · ADDIM 8 — Docker, docker-compose, GitHub Actions"

yoxla "Dockerfile → FROM node"                "var" \
  "$(grep -q 'FROM node' Dockerfile && echo var || echo yox)"
yoxla "Dockerfile çoxmərhələlidir (2+ FROM)"  "var" \
  "$([ "$(grep -c '^FROM' Dockerfile)" -ge 2 ] && echo var || echo yox)"
yoxla "Dockerfile → prisma generate"          "var" \
  "$(grep -q 'prisma generate' Dockerfile && echo var || echo yox)"
yoxla "Dockerfile yalnız istehsalat asılılıqları" "var" \
  "$(grep -q 'omit=dev' Dockerfile && echo var || echo yox)"
yoxla ".dockerignore → node_modules"          "var" \
  "$(grep -q 'node_modules' .dockerignore && echo var || echo yox)"
yoxla "compose → postgres xidməti"            "var" \
  "$(grep -q 'postgres' docker-compose.yml && echo var || echo yox)"
yoxla "compose → depends_on"                  "var" \
  "$(grep -q 'depends_on' docker-compose.yml && echo var || echo yox)"
yoxla "CI → npm ci"                           "var" \
  "$(grep -q 'npm ci' .github/workflows/ci.yml && echo var || echo yox)"
yoxla "CI → npm run build"                    "var" \
  "$(grep -q 'npm run build' .github/workflows/ci.yml && echo var || echo yox)"
yoxla "CI → vitest.config.e2e.ts"             "var" \
  "$(grep -q 'vitest.config.e2e.ts' .github/workflows/ci.yml && echo var || echo yox)"
yoxla "CI → postgres health check"            "var" \
  "$(grep -q 'health-cmd pg_isready' .github/workflows/ci.yml && echo var || echo yox)"

# ── 11 · MARSHRUTLAR ──────────────────────────────────────────────────
bashliq "11 · Bütün marshrutlar — Backend-4 sonrası"

SW="$(curl -s "$KOK/docs-json" 2>/dev/null)"
yollar() { printf '%s' "$SW" | grep -o "\"/api/v1$1[^\"]*\"" | sort -u | wc -l | tr -d ' '; }

yoxla "Swagger cavab verir"          "var" "$([ -n "$SW" ] && echo var || echo yox)"
yoxla "fərqli yol sayı = 20"         "20"  "$(yollar '')"
yoxla "AI marshrutları = 6"          "6"   "$(yollar '/ai')"
yoxla "ixrac marshrutları = 2"       "2"   "$(yollar '/ixrac')"
yoxla "auth marshrutları = 4"        "4"   "$(yollar '/auth')"
yoxla "kadrlar marshrutları = 3"     "3"   "$(yollar '/kadrlar')"
yoxla "struktur marshrutları = 3"    "3"   "$(yollar '/struktur')"

# Backend-3-də 15 idi → +8 (6 AI + 2 ixrac) = 23 metod+yol cütü
CUT="$(printf '%s' "$SW" | grep -oE '"(get|post|patch|put|delete)":' | wc -l | tr -d ' ')"
yoxla "metod+yol cütü = 23" "23" "$CUT"

# ── 12 · TESTLƏR ──────────────────────────────────────────────────────
bashliq "12 · ADDIM 10 — unit və e2e testlər"

UNIT_XAM="$(npm test 2>&1 | tr -d '\r')"
UNIT="$(printf '%s' "$UNIT_XAM" | grep -oE 'Tests +[0-9]+ passed' | head -1 | grep -oE '[0-9]+')"
yoxla "unit testlər keçir = 42" "42" "${UNIT:-0}"

E2E_XAM="$(npx vitest run --config vitest.config.e2e.ts 2>&1 | tr -d '\r')"
E2E="$(printf '%s' "$E2E_XAM" | grep -oE 'Tests +[0-9]+ passed' | head -1 | grep -oE '[0-9]+')"
yoxla "e2e testlər keçir = 39" "39" "${E2E:-0}"

yoxla "cəmi test = 81" "81" "$(( ${UNIT:-0} + ${E2E:-0} ))"

# ── NƏTİCƏ ────────────────────────────────────────────────────────────
printf "\n${MAVI}════════════════════════════════════════════════════════════${SIFIR}\n"
if [ "$XETA" -eq 0 ]; then
  printf "  ${YASIL}✓ BÜTÜN YENİLİKLƏR İŞLƏYİR${SIFIR} — ${YASIL}%d${SIFIR} yoxlama keçdi\n" "$KECDI"
else
  printf "  ${QIRMIZI}✗ %d YOXLAMA UĞURSUZ${SIFIR} — ${YASIL}%d${SIFIR} keçdi\n" "$XETA" "$KECDI"
fi
printf "${MAVI}════════════════════════════════════════════════════════════${SIFIR}\n"

[ "$XETA" -eq 0 ] && exit 0 || exit 1
