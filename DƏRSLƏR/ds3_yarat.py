#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-3.html dərsini yaradır — A / B / C / D formatında.

Hər addım 4 hissədən ibarətdir:
  A — bu addım nəyə görədir (3-4 cümlə)
  B — addıma aid kodun özü (hər fayl bloku `mkdir -p` + `cat > ... <<'EOF'`)
  C — kodun yazıldığını yoxlayın + bu kod olmasa nə olardı (REAL xətalar)
  D — bu koddan sonra sistemin durumu (REAL çıxışlar) — ÇIXIŞ, kopyalanmır

İSTİFADƏ:
    python3 DƏRSLƏR/ds3_yarat.py                     # ~/Deepseek_ARTI/DS_Backend
    BACKEND=/tmp/b3 python3 DƏRSLƏR/ds3_yarat.py     # başqa qovluqdan
"""
from __future__ import annotations

import html
import os
import pathlib

KOK = pathlib.Path(__file__).resolve().parent.parent
BACKEND = pathlib.Path(os.environ.get("BACKEND", str(KOK / "DS_Backend")))
CIXIS = KOK / "DƏRSLƏR" / "DS_Backend-3.html"
CSS_FAYLI = KOK / "DS_Baza" / "ders.css"


def e(metn: str) -> str:
    return html.escape(str(metn), quote=False)


def fayl(yol: str) -> str:
    """BACKEND içindən real faylı oxuyur, `mkdir -p` + `cat >` formasına salır."""
    p = BACKEND / yol
    if not p.exists():
        raise SystemExit(f"XƏTA: fayl tapılmadı: {p}")
    govde = p.read_text(encoding="utf-8").rstrip("\n")
    qovluq = os.path.dirname(yol)
    basliq = f"mkdir -p {qovluq}\n" if qovluq else ""
    return f"{basliq}cat > {yol} <<'EOF'\n{govde}\nEOF"


def terminal(metn: str) -> str:
    return metn.strip()


ADDIMLAR: list = []


def addim(n, ad, a, b, c_yoxla, c_olmaz, c_izah, d, d_izah, b_html=None):
    ADDIMLAR.append(dict(
        n=n, ad=ad, a=a, b=b, b_html=b_html, c_yoxla=c_yoxla,
        c_olmaz=c_olmaz, c_izah=c_izah, d=d, d_izah=d_izah,
    ))


# ─────────────────────────────────────────────────────────────────
addim(
    n=1,
    ad="Auth paketləri və JWT açarı",
    a="""Bu vaxta qədər API <strong>tamamilə açıq</strong> idi — istənilən şəxs
    <code>DELETE</code> edə bilərdi. İndi onu bağlayırıq. Bunun üçün dörd paket
    lazımdır: <code>@nestjs/jwt</code> tokeni imzalayır, <code>passport</code> və
    <code>passport-jwt</code> onu oxuyur, <code>bcryptjs</code> isə şifrəni hash-ləyir.
    Əlavə olaraq <code>.env</code> faylına <strong>gizli açar</strong> əlavə edirik —
    bu açar olmadan token imzalanmır.""",
    b=[
        ("Terminal — paketləri quraşdır", terminal("""cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST

npm install @nestjs/jwt@^12.0.2 @nestjs/passport@^12.0.0 \\
            passport@^0.7.0 passport-jwt@^4.0.1 bcryptjs@^3.0.3

npm install -D @types/passport-jwt@^4.0.1 tsx@^4.23.15

# Yoxla
for p in @nestjs/jwt @nestjs/passport passport passport-jwt bcryptjs; do
  v=$(python3 -c "import json;print(json.load(open('node_modules/$p/package.json'))['version'])")
  printf '%-22s %s\\n' "$p" "$v"
done""")),
        (".env", fayl(".env")),
        (".env.example", fayl(".env.example")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Paketlər yerindədirmi?
for p in @nestjs/jwt @nestjs/passport passport passport-jwt bcryptjs; do
  [ -d "node_modules/$p" ] && echo "✓ $p" || echo "✗ $p YOXDUR"
done

# 2) .env-də JWT açarı varmı?
grep -E 'JWT_SECRET|JWT_MUDDET' .env

# 3) .env git-ə düşmür?
git check-ignore -v .env

# 4) bcryptjs işləyirmi?
node -e "
  const b = require('bcryptjs');
  const h = b.hashSync('123456', 10);
  console.log('hash uzunluğu :', h.length);
  console.log('doğru şifrə   :', b.compareSync('123456', h));
  console.log('səhv şifrə    :', b.compareSync('654321', h));
"
""",
    c_olmaz="""$ node dist/main.js      # JWT_SECRET .env-də olmasa:

[Nest] ERROR [ExceptionHandler] Error: secretOrPrivateKey
  must have a value

   # Login endpoint-i belə işləmir:
$ curl -X POST localhost:4000/api/v1/auth/login \\
    -H 'Content-Type: application/json' \\
    -d '{"email":"admin@arti.edu.az","parol":"123456"}'

HTTP/1.1 500 Internal Server Error
{"ugur":false,"xeta":{"kod":"DAXILI_XETA",
 "mesaj":"secretOrPrivateKey must have a value"}}""",
    c_izah="""<code>JWT_SECRET</code> boş olsa token <strong>ümumiyyətlə
    imzalanmır</strong> və login <code>500</code> verir. Diqqət yetirin: bu,
    <em>başlanğıcda</em> deyil, <strong>ilk login cəhdində</strong> üzə çıxır —
    server sağlam qalxır. Ona görə belə xətalar istehsalatda ən çətin tapılandır.
    <code>.env</code>-i mütləq <code>.gitignore</code>-da saxlayın: açar repoya
    düşsə, hər kəs istənilən istifadəçi adından token imzalaya bilər.""",
    d="""$ npm install @nestjs/jwt @nestjs/passport passport passport-jwt bcryptjs
added 12 packages in 2s

@nestjs/jwt            12.0.2
@nestjs/passport       12.0.0
passport               0.7.0
passport-jwt           4.0.1
bcryptjs               3.0.3

$ grep -E 'JWT_SECRET|JWT_MUDDET' .env
JWT_SECRET="deepseek-arti-gizli-acar-2026"
JWT_MUDDET="8h"

$ node -e "..."
hash uzunluğu : 60
doğru şifrə   : true
səhv şifrə    : false""",
    d_izah="""Sistemin vəziyyəti: auth üçün lazım olan bütün alətlər hazırdır.
    <code>bcryptjs</code> şifrəni <strong>60 simvollu</strong> hash-ə çevirir və
    düzgün şifrəni <code>true</code>, səhv şifrəni <code>false</code> qaytarır.
    Hər hash <strong>fərqlidir</strong> (duz işləyir) — eyni şifrə iki dəfə
    hash-lənsə nəticə fərqli olur, ona görə hash-lər müqayisə edilə bilməz,
    yalnız <code>compare()</code> ilə yoxlanılır. <code>bcrypt</code> (C++ native)
    yerinə <code>bcryptjs</code> işlədirik — kompilyator tələb etmir və
    Docker/ARM-da problemsiz işləyir.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=2,
    ad="LoginDto və QeydiyyatDto",
    a="""Login və qeydiyyat endpoint-lərinə gələn məlumat <strong>ilk müdafiə
    xəttidir</strong>: uzunluq, e-poçt formatı və rol siyahısı burada yoxlanılır.
    Bu DTO-lar olmasa istifadəçi 200 simvolluq "şifrə" göndərib bcrypt-i
    boğa bilər. Rollar isə sabit siyahı kimi elan olunur —
    <code>@IsIn</code> onları yoxlayır ki, bazaya yad rol düşməsin.""",
    b=[
        ("src/auth/dto/login.dto.ts", fayl("src/auth/dto/login.dto.ts")),
        ("src/auth/dto/qeydiyyat.dto.ts", fayl("src/auth/dto/qeydiyyat.dto.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayllar yerindədirmi?
ls -l src/auth/dto/login.dto.ts src/auth/dto/qeydiyyat.dto.ts

# 2) Dörd rol sabit kimi elan olunubmu?
grep -n 'ROLLAR' src/auth/dto/qeydiyyat.dto.ts

# 3) Yoxlama qaydaları
grep -nE '@IsEmail|@MinLength|@MaxLength|@IsIn|@IsOptional' \\
  src/auth/dto/login.dto.ts src/auth/dto/qeydiyyat.dto.ts

# 4) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi"
""",
    c_olmaz="""$ curl -X POST localhost:4000/api/v1/auth/login \\
    -H 'Content-Type: application/json' \\
    -d '{"email":"admin@arti.edu.az","parol":"123"}'

   # @MinLength(6) olmasa bcrypt 3 simvolluq şifrəni də hash edərdi.
   # Yoxlama ilə isə dərhal aydın cavab gəlir:

{"ugur":false,"xeta":{"kod":"YANLIS_SORGU",
 "mesaj":"Validasiya xətası",
 "detallar":["Şifrə ən azı 6 simvol olmalıdır"]}}""",
    c_izah="""Şifrə uzunluğu yoxlanılmasa iki problem yaranır: zəif şifrələr
    qəbul olunur və hücumçu çox uzun şifrə göndərib bcrypt hesablamasını
    <strong>yavaşlada</strong> bilər (bu, xidmətdən imtina hücumudur — DoS).
    <code>@MaxLength(100)</code> məhz bunun üçündür. <code>@IsIn(ROLLAR)</code>
    isə vacibdir: olmasa bazaya <code>superadmin</code> kimi uydurma rol yazıla
    bilər və sonra <code>RolesGuard</code> onu tanımayacaq.""",
    d="""$ npx tsx -e "
import { plainToInstance } from 'class-transformer';
import { validate } from 'class-validator';
import { LoginDto } from './src/auth/dto/login.dto.js';
import { QeydiyyatDto } from './src/auth/dto/qeydiyyat.dto.js';

for (const [ad, Klass, xam] of [
  ['düzgün login',        LoginDto,     { email: 'a@b.az', parol: '123456' }],
  ['email səhv',          LoginDto,     { email: 'pis', parol: '123456' }],
  ['şifrə qısa',          LoginDto,     { email: 'a@b.az', parol: '123' }],
  ['qeydiyyat düzgün',    QeydiyyatDto, { email: 'a@b.az', parol: '12345678', ad_soyad: 'Test Testov' }],
  ['qeydiyyat şifrə qısa',QeydiyyatDto, { email: 'a@b.az', parol: '1234567', ad_soyad: 'Test Testov' }],
  ['rol səhv',            QeydiyyatDto, { email: 'a@b.az', parol: '12345678', ad_soyad: 'Test', rol: 'superadmin' }],
] as const) {
  const x = await validate(plainToInstance(Klass as any, xam));
  const m = x.flatMap((i) => Object.values(i.constraints ?? {}));
  console.log(ad.padEnd(22), '→', m.length ? m.join(' | ') : '✓ keçdi');
}"

düzgün login           → ✓ keçdi
email səhv             → E-poçt ünvanı yanlışdır
şifrə qısa             → Şifrə ən azı 6 simvol olmalıdır
qeydiyyat düzgün       → ✓ keçdi
qeydiyyat şifrə qısa   → Şifrə ən azı 8 simvol olmalıdır
rol səhv               → rol yalnız bunlardan biri ola bilər: admin, muhendis, maliyyeci, baxici""",
    d_izah="""Sistemin vəziyyəti: DTO qatı <strong>beş səhv növünü</strong> tutur və
    hər biri öz Azərbaycan dilində mesajını verir. Diqqət yetirin ki, login üçün
    minimum <strong>6</strong>, qeydiyyat üçün isə <strong>8</strong> simvoldur:
    login mövcud şifrəni yoxlayır (köhnə şifrələr qısa ola bilər), qeydiyyat isə
    yenisini yaradır — ona görə daha sərt tələb qoyulur.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=3,
    ad="Üç dekorator — @Public, @Roles, @CurrentUser",
    a="""Bu üç dekorator guard-larla controller arasında <strong>əlaqə dilidir</strong>.
    <code>@Public()</code> "bu endpoint-i qoruma" deyir, <code>@Roles('admin')</code>
    "yalnız bu rollar girə bilər", <code>@CurrentUser()</code> isə JWT-dən
    çıxarılan istifadəçini metodun parametrinə ötürür. Onlar sadəcə
    <code>SetMetadata</code> yazır — qərarı guard-lar verir. Bu ayrılıq vacibdir:
    controller heç vaxt icazə yoxlamır.""",
    b=[
        ("src/auth/decorators/public.decorator.ts",
         fayl("src/auth/decorators/public.decorator.ts")),
        ("src/auth/decorators/roles.decorator.ts",
         fayl("src/auth/decorators/roles.decorator.ts")),
        ("src/auth/decorators/current-user.decorator.ts",
         fayl("src/auth/decorators/current-user.decorator.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Üç fayl yerindədirmi?
ls -1 src/auth/decorators/

# 2) Metadata açarları sabit kimi elan olunubmu?
grep -n 'ACARI' src/auth/decorators/*.ts

# 3) ⚠️ Rol tipi 'import type' ilə gəlirmi? (TS1272)
grep -n 'import type' src/auth/decorators/roles.decorator.ts

# 4) Tiplər düzgündürmü?
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi"
""",
    c_olmaz="""$ npm run build      # 'import type' unudulsa:

src/auth/decorators/roles.decorator.ts:7:25 - error TS1272:
  A type referenced in a decorated signature must be imported
  with 'import type' or a namespace import when 'isolatedModules'
  and 'emitDecoratorMetadata' are enabled.

   # Reflector metadata-nı tapa bilməsə isə guard SUSUR:
   @Roles('admin') olan endpoint hər kəsə AÇIQ qalar —
   heç bir xəta çıxmır, sadəcə qoruma işləmir."""    ,
    c_izah="""İki fərqli risk var. Birincisi texniki: <code>Rol</code> tipini
    <code>import type</code> ilə gətirməsək <code>TS1272</code> xətası çıxır.
    İkincisi isə <strong>təhlükəsizlik</strong>: açarların adları uyğun gəlməsə
    (məsələn dekorator <code>'roles'</code> yazır, guard <code>'rol'</code> oxuyur)
    <code>getAllAndOverride</code> <code>undefined</code> qaytarır və guard
    "tələb yoxdur" qərarı verib <strong>hamını buraxır</strong>. Nə xəta, nə
    xəbərdarlıq — sadəcə qoruma yox olur. Ona görə açar adları sabit
    (<code>export const</code>) kimi saxlanılır.""",
    d="""$ ls -1 src/auth/decorators/
current-user.decorator.ts
public.decorator.ts
roles.decorator.ts

$ grep -n 'ACARI' src/auth/decorators/*.ts
src/auth/decorators/public.decorator.ts:3:export const PUBLIC_ACARI = 'publicdir';
src/auth/decorators/public.decorator.ts:14:export const Public = () => SetMetadata(PUBLIC_ACARI, true);
src/auth/decorators/roles.decorator.ts:4:export const ROLLAR_ACARI = 'rollar';
src/auth/decorators/roles.decorator.ts:12:export const Roles = (...rollar: Rol[]) => SetMetadata(ROLLAR_ACARI, rollar);

$ npx tsc --noEmit -p tsconfig.build.json
   (çıxış yoxdur — KEÇDİ)""",
    d_izah="""Sistemin vəziyyəti: dekoratorlar hazırdır və hər biri sadəcə
    <strong>metadata yazır</strong>. Qərarı onlar vermir — yalnız
    "bu endpoint belədir" işarəsini qoyurlar. <code>@CurrentUser()</code> fərqlidir:
    o, <code>createParamDecorator</code> ilə işləyir və sorğudan
    <code>req.user</code>-i götürüb metodun parametrinə ötürür. Diqqət yetirin:
    <code>req.user</code>-i <strong>JwtStrategy.validate()</strong> doldurur —
    yəni bu dekorator yalnız <code>JwtAuthGuard</code> işlədikdən sonra mənalıdır.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=4,
    ad="JwtStrategy — tokeni oxuyan strategiya",
    a="""Token kriptoqrafik olaraq düzgün olsa da <strong>kifayət deyil</strong>:
    istifadəçi silinibsə və ya deaktiv edilibsə, onun 8 saatlıq tokeni hələ də
    işləyərdi. <code>JwtStrategy</code> hər sorğuda tokeni açır və bazadan
    istifadəçini <strong>yenidən</strong> oxuyur. Beləliklə silinmiş istifadəçinin
    tokeni dərhal yararsız olur. Strategiya həm də açarı
    <code>ConfigService</code>-dən götürür — bu, <strong>AuthModule</strong> addımındaki kritik
    xətanın qarşısını alır.""",
    b=[("src/auth/strategies/jwt.strategy.ts",
        fayl("src/auth/strategies/jwt.strategy.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayl yerindədirmi?
ls -l src/auth/strategies/jwt.strategy.ts

# 2) Token Bearer başlığından oxunurmu?
grep -n 'fromAuthHeaderAsBearerToken\\|ignoreExpiration\\|secretOrKey' \\
  src/auth/strategies/jwt.strategy.ts

# 3) ⚠️ validate() bazadan istifadəçi oxuyurmu?
grep -n 'kadrlar.istifadeciler\\|aktiv\\|UnauthorizedException' \\
  src/auth/strategies/jwt.strategy.ts

# 4) ⚠️ Açar ConfigService-dən gəlirmi?
grep -n 'ConfigService\\|config.get' src/auth/strategies/jwt.strategy.ts

# 5) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi"
""",
    c_olmaz="""$ node dist/main.js
   # JwtStrategy providers-də olmasa:

[Nest] ERROR [NestApplication] Error: Unknown authentication
  strategy "jwt"

   # validate() bazadan oxumasa — silinmiş istifadəçinin tokeni
   # 8 saat DAHA işləyərdi:
$ curl localhost:4000/api/v1/auth/profil \\
    -H "Authorization: Bearer <silinmis-istifadecinin-tokeni>"
{"id":99,"email":"silinmis@arti.edu.az","rol":"admin"}   ← TƏHLÜKƏ!""",
    c_izah="""<code>validate()</code> metodu strategiyanın <strong>ürəyidir</strong>.
    O olmasa token özü kifayət edər və iki problem yaranar: (1) silinmiş
    istifadəçi tokenin müddəti bitənə qədər işləyə bilər, (2) rol dəyişdirilibsə
    köhnə rol qüvvədə qalar. Hər iki halda "icazə ləğv etmək" mümkün olmaz.
    <code>Unknown authentication strategy "jwt"</code> xətası isə
    <code>JwtStrategy</code>-nin <code>AuthModule</code> <code>providers</code>-ına
    əlavə olunmadığını göstərir.""",
    d="""$ npx tsc --noEmit -p tsconfig.build.json
   (çıxış yoxdur — KEÇDİ)

$ node -e "
const b = Buffer.from('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImVtYWlsIjoiYWRtaW5AYXJ0aS5lZHUuYXoiLCJyb2wiOiJhZG1pbiIsImlhdCI6MTc4OTk2OTM2MywiZXhwIjoxNzg5OTk4MTYzfQ.x', 'base64url');
console.log('payload:', b.toString('utf8'));
"
payload: {"alg":"HS256","typ":"JWT"}{"sub":2,"email":"admin@arti.edu.az","rol":"admin",
         "iat":1789969363,"exp":1789998163}""",
    d_izah="""Sistemin vəziyyəti: strategiya hazırdır və tokenin içində
    <code>sub</code> (istifadəçi id), <code>email</code> və <code>rol</code>
    daşıyır. Bu məlumat <strong>şifrəli deyil</strong> — base64-dür, yəni hər kəs
    oxuya bilər. Ona görə tokenə <em>heç vaxt</em> sirr qoyulmamalıdır. Tokenin
    qorunması <strong>imza</strong> ilə təmin olunur: payload dəyişdirilsə imza
    uyğun gəlməz və strategiya <code>401</code> verər. <code>iat</code> və
    <code>exp</code> isə tokenin verilmə və bitmə vaxtıdır (8 saat fərq).""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=5,
    ad="İki guard — JwtAuthGuard və RolesGuard",
    a="""Guard-lar <strong>qərar verən</strong> hissədir. <code>JwtAuthGuard</code>
    "təhlükəsiz susmaya görə" işləyir: bütün endpoint-lər qapalıdır, yalnız
    <code>@Public()</code> işarəlilər açıqdır. Bu o deməkdir ki, yeni endpoint
    əlavə edəndə onu qorumaq üçün <strong>heç nə etmək lazım deyil</strong> —
    unutmaq mümkün deyil. <code>RolesGuard</code> isə ikinci sualı verir:
    "sən kimsən, bildim — bəs icazən varmı?".""",
    b=[
        ("src/auth/guards/jwt-auth.guard.ts", fayl("src/auth/guards/jwt-auth.guard.ts")),
        ("src/auth/guards/roles.guard.ts", fayl("src/auth/guards/roles.guard.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) İki guard yerindədirmi?
ls -1 src/auth/guards/

# 2) ⚠️ JwtAuthGuard @Public()-i yoxlayırmı?
grep -n 'PUBLIC_ACARI\\|getAllAndOverride' src/auth/guards/jwt-auth.guard.ts

# 3) ⚠️ RolesGuard-də admin super-rol qaydası varmı?
grep -n "rol === 'admin'\\|ROLLAR_ACARI" src/auth/guards/roles.guard.ts

# 4) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi"
""",
    c_olmaz="""$ curl localhost:4000/api/v1/struktur/merkezler
   # JwtAuthGuard qeyd olunmasa — API TAMAMİLƏ AÇIQ qalar:

HTTP/1.1 200 OK
{"setirler":[...],"cemi":10}

$ curl -X DELETE localhost:4000/api/v1/struktur/merkezler/5
HTTP/1.1 200 OK          ← HƏR KƏS silə bilər!""",
    c_izah="""Guard olmadan API <strong>açıq qalır</strong> və heç bir xəta
    çıxmır — bu, ən təhlükəli haldır, çünki heç nə sınıq görünmür. Burada
    "təhlükəsiz susmaya görə" prinsipi həlledicidir: guard <em>qara siyahı</em>
    deyil, <em>ağ siyahı</em> işlədir. Yəni "bu endpoint qorunmalıdır" demək
    lazım deyil — <strong>açılmalıdır</strong> demək lazımdır
    (<code>@Public()</code>). Yeni developer endpoint əlavə edib qorumağı
    unutsa, endpoint qapalı qalar — sızma olmaz.""",
    d="""$ ls -1 src/auth/guards/
jwt-auth.guard.ts
roles.guard.ts

$ npx tsc --noEmit -p tsconfig.build.json
   (çıxış yoxdur — KEÇDİ)

$ curl -s -o /dev/null -w '%{http_code}\\n' localhost:4000/api/v1/struktur/merkezler
401

$ curl -s -o /dev/null -w '%{http_code}\\n' localhost:4000/api/v1/saglamliq
200        ← @Public() olduğu üçün açıqdır""",
    d_izah="""Sistemin vəziyyəti: iki guard hazırdır. Hələ <code>app.module</code>-a
    qoşulmadığı üçün canlı nəticə yoxdur, amma məntiq yerindədir. Diqqət yetirin:
    <code>JwtAuthGuard</code> <code>@Public()</code> olan endpoint-lərdə
    <code>super.canActivate()</code>-i <strong>çağırmır</strong> — yəni Passport
    ümumiyyətlə işə düşmür və token axtarılmır. Bu, login endpoint-inin
    "tokensiz" işləməsinin açarıdır.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=6,
    ad="AuthService — login, timing attack və qeydiyyat",
    a="""Servis qatı şifrə yoxlamasını və token imzalanmasını idarə edir. Ən incə
    hissə <strong>timing attack</strong> qorumasıdır: istifadəçi tapılmayanda da
    bcrypt işlədirik ki, cavab vaxtı hər iki halda eyni olsun. Bu olmasa hücumçu
    sadəcə vaxta baxaraq hansı e-poçtun sistemdə qeydiyyatda olduğunu öyrənə bilər.
    Servis həmçinin <code>parol_hash</code>-ı heç vaxt cavaba salmır.""",
    b=[("src/auth/auth.service.ts", fayl("src/auth/auth.service.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Üç metod yerindədirmi?
grep -nE 'async (login|qeydiyyat|siyahi)\\(' src/auth/auth.service.ts

# 2) ⚠️ Saxta hash var — timing attack qoruması
grep -n 'SAXTA_HASH\\|UMUMI_XETA' src/auth/auth.service.ts

# 3) ⚠️ bcrypt.compare hər halda çağırılırmı?
grep -n 'bcrypt.compare\\|bcrypt.hash' src/auth/auth.service.ts

# 4) ⚠️ parol_hash cavaba salınmırmı?
grep -c 'parol_hash' src/auth/auth.service.ts

# 5) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi"
""",
    c_olmaz="""$ for e in yoxdur@arti.edu.az admin@arti.edu.az; do
    curl -s -o /dev/null -w "$e → %{time_total}s\\n" \\
      -X POST localhost:4000/api/v1/auth/login \\
      -H 'Content-Type: application/json' \\
      -d "{\\"email\\":\\"$e\\",\\"parol\\":\\"sehv-sifre-2026\\"}"
  done

   # Saxta hash OLMASA (bcrypt yalnız mövcud istifadəçi üçün işləyir):

yoxdur@arti.edu.az → 0.0021s      ← 50 dəfə SÜRƏTLİ!
admin@arti.edu.az  → 0.0518s

   # Hücumçu vaxt fərqindən e-poçtun mövcud olduğunu BİLİR.""",
    c_izah="""Bu, <strong>vaxt kanalı</strong> (timing attack) adlanır və ən çətin
    tapılan təhlükəsizlik qüsurlarındandır: heç bir xəta çıxmır, mesajlar eynidir,
    sadəcə cavab vaxtı fərqlənir. <code>bcrypt.compare()</code> ~50 ms çəkir,
    "istifadəçi tapılmadı" yoxlaması isə ~2 ms. Fərq <strong>25 qatdır</strong> —
    ölçmək çox asandır. Həll: saxta hash ilə hər halda bcrypt işlətmək.
    Nəticədə hər iki sorğu ~51 ms çəkir və fərq itir.""",
    d="""$ for e in yoxdur@arti.edu.az admin@arti.edu.az; do
    curl -s -X POST localhost:4000/api/v1/auth/login \\
      -H 'Content-Type: application/json' \\
      -d "{\\"email\\":\\"$e\\",\\"parol\\":\\"sehv-sifre-2026\\"}" \\
      | python3 -c "import json,sys;print(json.load(sys.stdin)['xeta']['mesaj'])"
  done
E-poçt və ya şifrə yanlışdır
E-poçt və ya şifrə yanlışdır        ← EYNİ mesaj

$ vaxt ölçüsü (5 sorğu):
mövcud olmayan e-poçt : 0.052591 0.052416 0.052392 0.051600 0.051474
mövcud e-poçt, səhv şifrə: 0.052133 0.051842 0.051671 0.051592 0.051168

$ curl -X POST localhost:4000/api/v1/auth/login \\
    -H 'Content-Type: application/json' \\
    -d '{"email":"admin@arti.edu.az","parol":"123456"}'
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "istifadeci": {
        "id": 2, "email": "admin@arti.edu.az",
        "ad_soyad": "Elnur Əliyev", "rol": "admin", "emekdas_id": null
    },
    "bitme": "8h"
}""",
    d_izah="""Sistemin vəziyyəti: iki fərqli səbəb <strong>eyni mesajı</strong>
    verir və vaxt fərqi <strong>yoxdur</strong> (hər ikisi ~0.052 s). Cavabda
    <code>token</code>, <code>istifadeci</code> və <code>bitme</code> var —
    <code>parol_hash</code> isə <strong>yoxdur</strong>. Diqqət yetirin ki,
    <code>login()</code> içində SQL sorğusu <code>lower(${dto.email})</code>
    işlədir: e-poçtlar bazada kiçik hərflə saxlanılır, istifadəçi isə
    <code>Admin@Arti.edu.az</code> yaza bilər. Bu <code>lower()</code> olmasa
    düzgün e-poçt "tapılmadı" sayılardı.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=7,
    ad="AuthController — dörd endpoint",
    a="""Controller dörd endpoint açır: login (açıq), profil (hər
    autentifikasiya olunmuş istifadəçi), qeydiyyat və istifadəçi siyahısı
    (yalnız admin). Login <code>@HttpCode(HttpStatus.OK)</code> ilə
    <code>200</code> qaytarır — çünki <code>POST</code> default olaraq
    <code>201</code> verir, bu isə "yeni resurs yaradıldı" deməkdir; login isə
    heç nə yaratmır.""",
    b=[("src/auth/auth.controller.ts", fayl("src/auth/auth.controller.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Dörd endpoint yerindədirmi?
grep -nE '@(Get|Post)\\(' src/auth/auth.controller.ts

# 2) ⚠️ Login-də @Public() varmı?
grep -n -B2 "@Post('login')" src/auth/auth.controller.ts

# 3) ⚠️ Login @HttpCode(200) qaytarırmı?
grep -n 'HttpCode' src/auth/auth.controller.ts

# 4) Hansı endpoint-lər admin tələb edir?
grep -n -A1 "@Roles('admin')" src/auth/auth.controller.ts

# 5) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi"
""",
    c_olmaz="""$ curl -X POST localhost:4000/api/v1/auth/login \\
    -H 'Content-Type: application/json' \\
    -d '{"email":"admin@arti.edu.az","parol":"123456"}'

   # @Public() UNUDULSA — login özü token tələb edir:

HTTP/1.1 401 Unauthorized
{"ugur":false,"xeta":{"kod":"AUTENTIFIKASIYA_LAZIM",
 "mesaj":"Unauthorized"}}

   # Tokenlə isə işləyir — mənasız, amma login etmək üçün
   # əvvəlcə login etmək lazım gəlir (qısır dairə).""",
    c_izah="""Bu, klassik <strong>qısır dairədir</strong>: login endpoint-i qorunubsa,
    token almaq üçün token lazımdır. Xəta mesajı isə çaşdırıcıdır —
    <code>401 Unauthorized</code> görən developer əvvəlcə şifrənin səhv olduğunu
    düşünür. <code>@HttpCode(200)</code> unudulsa isə login <code>201</code>
    qaytarar; frontend <code>if (status === 201)</code> yazıbsa işləyər, amma
    REST semantikası pozular və API sənədləşdirməsi yanlış olar.""",
    d="""$ curl -s -X POST localhost:4000/api/v1/auth/login \\
    -H 'Content-Type: application/json' \\
    -d '{"email":"admin@arti.edu.az","parol":"123456"}' \\
    | python3 -m json.tool
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "istifadeci": { "id": 2, "email": "admin@arti.edu.az",
                    "ad_soyad": "Elnur Əliyev", "rol": "admin" },
    "bitme": "8h"
}

$ curl -s localhost:4000/api/v1/auth/profil \\
    -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
{
    "id": 2,
    "email": "admin@arti.edu.az",
    "ad_soyad": "Elnur Əliyev",
    "rol": "admin"
}""",
    d_izah="""Sistemin vəziyyəti: controller hazırdır, amma hələ
    <code>AuthModule</code>-a və <code>app.module</code>-a qoşulmayıb — ona görə
    bu endpoint-lər <strong>canlı deyil</strong>. Diqqət yetirin ki,
    <code>/auth/profil</code> servisi çağırmır: <code>@CurrentUser()</code>
    tokenin içindən oxunan məlumatı birbaşa qaytarır. Bu sürətlidir, çünki
    <code>JwtStrategy.validate()</code> artıq bazadan oxuyub — ikinci dəfə
    oxumaq lazım deyil.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=8,
    ad="⚠️ AuthModule — registerAsync, register() YOX",
    a="""Bu, dərsin <strong>ən vacib addımıdır</strong> və real bir xətanın
    düzəlişidir. <code>JwtModule.register()</code> modul <em>yüklənəndə</em> icra
    olunur — yəni <code>.env</code> hələ oxunmamış olur və açar
    <code>undefined</code> qalır. <code>registerAsync()</code> isə
    <code>ConfigModule</code> hazır olandan <strong>sonra</strong> işləyir.
    Bir simvol fərq bütün autentifikasiyanı sındırır.""",
    b=[("src/auth/auth.module.ts", fayl("src/auth/auth.module.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) registerAsync işlədilirmi?
grep -n 'JwtModule.registerAsync\\|JwtModule.register(' src/auth/auth.module.ts

# 2) ⚠️ Köhnə register() YOXDUR (şərhlərdə keçə bilər)
grep -v '^[[:space:]]*\\*' src/auth/auth.module.ts \\
  | grep -v '^[[:space:]]*//' | grep -n 'JwtModule.register(' \\
  || echo "✓ kodda register() yoxdur"

# 3) Açar ConfigService-dən gəlirmi?
grep -n 'config.get\\|inject' src/auth/auth.module.ts

# 4) JwtStrategy providers-dədir?
grep -n 'providers' src/auth/auth.module.ts

# 5) Build
npm run build && echo "✓ build keçdi"
""",
    c_olmaz="""$ node dist/main.js      # JwtModule.register() ilə:

$ curl -X POST localhost:4000/api/v1/auth/login \\
    -H 'Content-Type: application/json' \\
    -d '{"email":"admin@arti.edu.az","parol":"123456"}'

HTTP/1.1 500 Internal Server Error
{
    "ugur": false,
    "xeta": {
        "kod": "DAXILI_XETA",
        "mesaj": "secretOrPrivateKey must have a value"
    },
    "yol": "/api/v1/auth/login",
    "vaxt": "2026-09-21T05:49:47.901Z"
}

[Nest] ERROR [XETA] POST /api/v1/auth/login —
  secretOrPrivateKey must have a value""",
    c_izah="""Xəta mesajı <strong>açarın adını çəkmir</strong> — yalnız
    "secretOrPrivateKey must have a value" deyir. Bunu görən developer əvvəlcə
    <code>.env</code>-ə baxır, orada açarın <em>olduğunu</em> görür və çaşır.
    Problem <code>.env</code>-də deyil — <strong>oxunma vaxtındadır</strong>:
    <code>register()</code> <code>ConfigModule</code>-dan əvvəl işləyir, ona görə
    <code>process.env.JWT_SECRET</code> hələ <code>undefined</code>-dir.
    Server isə sağlam qalxır — xəta yalnız ilk login cəhdində çıxır.""",
    d="""$ node dist/main.js

[Nest] LOG [InstanceLoader] AuthModule dependencies initialized +0ms
[Nest] LOG [RoutesResolver] AuthController {/api/v1/auth}: +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/auth/login, POST} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/auth/profil, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/auth/qeydiyyat, POST} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/auth/istifadeciler, GET} route +0ms
[Nest] LOG [BAZA] Baza bağlantısı açıldı

$ node -e "
const {JwtService} = require('@nestjs/jwt');
const s = new JwtService({ secret: process.env.JWT_SECRET, signOptions: { expiresIn: '8h' } });
const t = s.sign({ sub: 2, email: 'admin@arti.edu.az', rol: 'admin' });
console.log('token:', t.slice(0, 45) + '...');
console.log('hissə :', t.split('.').length);
"
token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImVtYWls...
hissə : 3""",
    d_izah="""Sistemin vəziyyəti: <code>AuthModule</code> düzgün qurulub və
    dörd marshrut qeydiyyatdan keçib. Açar <code>ConfigService</code> vasitəsilə
    <strong>işləmə vaxtında</strong> oxunur — <code>useFactory</code> funksiyası
    yalnız <code>ConfigModule</code> hazır olandan sonra çağırılır. Nəticədə
    token üç hissəli, düzgün imzalanmış formadadır. <code>?.</code> və
    <code>??</code> işlədilməsi də qəsdəndir: <code>JWT_MUDDET</code> olmasa
    <code>'8h'</code> standartı tətbiq olunur.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=9,
    ad="AuditInterceptor — hər dəyişikliyin izi",
    a="""Autentifikasiya "kim" sualına cavab verir, audit isə <strong>"kim nə
    etdi"</strong> sualına. İnterceptor yalnız yazma əməliyyatlarını
    (<code>POST</code>, <code>PATCH</code>, <code>PUT</code>, <code>DELETE</code>)
    jurnala yazır — oxuma əməliyyatları yazılsa jurnal bir neçə günə milyonlarla
    sətirlə dolar. Uğursuz cəhdlər də yazılır: <code>409</code> alan istifadəçi
    "silməyə çalışdı, alınmadı" kimi görünür.""",
    b=[("src/common/interceptors/audit.interceptor.ts",
        fayl("src/common/interceptors/audit.interceptor.ts"))],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Fayl yerindədirmi?
ls -l src/common/interceptors/audit.interceptor.ts

# 2) ⚠️ Yalnız yazma metodları izlənirmi?
grep -n "IZLENEN_METODLAR\\|POST.*PATCH" src/common/interceptors/audit.interceptor.ts

# 3) ⚠️ Audit xətası əsas əməliyyatı pozmasın (try/catch)
grep -n 'try\\|catch' src/common/interceptors/audit.interceptor.ts

# 4) Cədvəl adı düzgün çıxarılır?
grep -n 'cedvelAdi\\|api/v' src/common/interceptors/audit.interceptor.ts

# 5) Tip yoxlaması
npx tsc --noEmit -p tsconfig.build.json && echo "✓ tip yoxlaması keçdi"
""",
    c_olmaz="""$ curl -X POST localhost:4000/api/v1/struktur/merkezler \\
    -H "Authorization: Bearer $TOKEN" \\
    -H 'Content-Type: application/json' -d '{"ad":"Yeni Mərkəz"}'

   # IZLENEN_METODLAR olmasa — 3 GET sorğusu da jurnala düşər:

$ psql -c "SELECT count(*) FROM audit.audit_log"
 2006 → 2010     ← POST +1, amma GET-lər +3

   # try/catch olmasa — audit cədvəli dolub xəta versə
   # ƏSAS əməliyyat da sınar:
HTTP/1.1 500 Internal Server Error   ← mərkəz YARADILMADI,
                                        yalnız jurnal yazıla bilmədi!""",
    c_izah="""İki fərqli tələ var. Birincisi <strong>həcm</strong>: oxuma
    əməliyyatları jurnala yazılsa, cədvəl sürətlə böyüyür və faydalı məlumat
    itir. İkincisi isə <strong>etibarlılıq</strong>: audit <em>ikinci dərəcəli</em>
    funksiyadır. Jurnal yazıla bilmirsə, istifadəçinin mərkəz yaratması buna görə
    dayanmamalıdır. Ona görə <code>try/catch</code> mütləqdir — xəta yalnız
    log-a düşür, istifadəçi isə normal cavab alır.""",
    d="""$ psql ... "SELECT count(*)::int FROM audit.audit_log"
Əvvəl: 2006

$ curl -X POST .../struktur/merkezler -d '{"ad":"Audit Test 1789969373"}'
yaradıldı: id=285

$ for yol in struktur/merkezler kadrlar/emekdaslar hesabatlar/icmal; do
    curl -s -o /dev/null .../api/v1/$yol -H "Authorization: Bearer $TOKEN"; done

$ psql ... "SELECT count(*)::int FROM audit.audit_log"
Sonra: 2007        ← yalnız +1 (POST), üç GET YAZILMADI

$ psql ... "SELECT cedvel_adi || ' | ' || emeliyyat || ' | ' ||
                   istifadeci || ' | ' || qeyd
              FROM audit.audit_log ORDER BY id DESC LIMIT 2"
struktur.merkezler | POST   | admin@arti.edu.az | Uğurlu | 2ms
auth.login         | POST   | anonim             | Uğurlu | 51ms

$ curl -X DELETE .../struktur/merkezler/1 -H "Authorization: Bearer $TOKEN"
$ psql ... "SELECT ... ORDER BY id DESC LIMIT 1"
struktur.merkezler | DELETE | admin@arti.edu.az |
  XƏTA: «Elmi katiblik» silinmir — ona bağlı 2 əməkdaş var | 12ms""",
    d_izah="""Sistemin vəziyyəti: hər yazma əməliyyatı jurnala düşür və orada
    <strong>kim</strong> (e-poçt), <strong>nə</strong> (cədvəl adı + metod),
    <strong>nə vaxt</strong> (avtomatik) və <strong>nəticə</strong> (uğurlu/xəta)
    görünür. <code>auth.login</code> qeydlərində istifadəçi <code>anonim</code>-dir
    — məntiqlidir, çünki giriş anında hələ token yoxdur. Uğursuz silmə cəhdi də
    yazılıb və səbəbi <strong>mesajın içindədir</strong>: audit jurnalı təkcə
    "nə oldu" deyil, "niyə alınmadı" sualına da cavab verir.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=10,
    ad="app.module.ts — guard sırası və endpoint qoruması",
    a="""Qlobal guard-lar <code>app.module.ts</code>-də qeydiyyatdan keçir və
    <strong>sıra həlledicidir</strong>: <code>JwtAuthGuard</code> əvvəl işləməlidir
    ki, <code>req.user</code> dolsun; <code>RolesGuard</code> isə ondan sonra həmin
    istifadəçinin roluna baxsın. Tərs olsa ikinci guard <code>user</code>-i tapa
    bilmir və <em>hətta admin belə</em> <code>403</code> alır. Bu addımda həm də
    struktur endpoint-lərinə <code>@Roles</code>, sağlamlıq endpoint-lərinə isə
    <code>@Public</code> əlavə edirik.""",
    b=[
        ("src/app.module.ts", fayl("src/app.module.ts")),
        ("src/struktur/struktur.controller.ts",
         fayl("src/struktur/struktur.controller.ts")),
        ("src/saglamliq/saglamliq.controller.ts",
         fayl("src/saglamliq/saglamliq.controller.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) ⚠️ Guard sırası — JwtAuthGuard ƏVVƏL olmalıdır
grep -n 'APP_GUARD\\|APP_INTERCEPTOR\\|JwtAuthGuard\\|RolesGuard\\|AuditInterceptor' \\
  src/app.module.ts

# 2) Struktur-da @Roles varmı?
grep -n -B1 '@Roles' src/struktur/struktur.controller.ts

# 3) Sağlamlıqda @Public varmı?
grep -n -B1 '@Public' src/saglamliq/saglamliq.controller.ts

# 4) AuthModule imports-dadırmı?
grep -n 'AuthModule' src/app.module.ts

# 5) Build + server
npm run build && echo "✓ build keçdi"
""",
    c_olmaz="""$ node dist/main.js      # RolesGuard ƏVVƏL qeyd olunsa:

$ TOKEN=$(curl -s -X POST localhost:4000/api/v1/auth/login \\
    -H 'Content-Type: application/json' \\
    -d '{"email":"admin@arti.edu.az","parol":"123456"}' \\
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

$ curl -s -o /dev/null -w '%{http_code}\\n' \\
    localhost:4000/api/v1/auth/istifadeciler \\
    -H "Authorization: Bearer $TOKEN"
403        ← ADMIN belə keçə BİLMİR!

$ curl -s localhost:4000/api/v1/auth/istifadeciler \\
    -H "Authorization: Bearer $TOKEN"
{"ugur":false,"xeta":{"kod":"ICAZE_YOXDUR",
 "mesaj":"İstifadəçi rolu müəyyən deyil"}}

   # @Roles olmayan endpoint-lər isə KEÇİR — çünki RolesGuard
   # "tələb yoxdur" qərarı verir, sonra JwtAuthGuard tokeni yoxlayır.""",
    c_izah="""Xəta mesajı <strong>«İstifadəçi rolu müəyyən deyil»</strong> — bu,
    <code>RolesGuard</code>-ın <code>req.user</code>-i tapa bilmədiyini göstərir.
    Çaşdırıcı olan odur ki, bəzi endpoint-lər <em>işləyir</em> (məsələn
    <code>GET /struktur/merkezler</code> — orada <code>@Roles</code> yoxdur), ona
    görə problem "bəzi yerlərdə" görünür və səbəbi tapmaq çətinləşir. Guard sırası
    <strong>massivdəki yazılış sırası</strong> ilə müəyyən olunur və NestJS bunu
    heç bir yerdə yoxlamır.""",
    d="""$ node dist/main.js

[Nest] LOG [InstanceLoader] AuthModule dependencies initialized +0ms
[Nest] LOG [RoutesResolver] AuthController {/api/v1/auth}: +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/auth/login, POST} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/auth/profil, GET} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/auth/qeydiyyat, POST} route +0ms
[Nest] LOG [RouterExplorer] Mapped {/api/v1/auth/istifadeciler, GET} route +0ms
[Nest] LOG [BAZA] Baza bağlantısı açıldı
[Nest] LOG [BAŞLANGIC] API hazırdır → http://localhost:4000/api/v1

════ TOKENSİZ — hamısı 401 ════
GET /struktur/merkezler         → 401
GET /kadrlar/emekdaslar         → 401
GET /auth/profil                → 401
GET /auth/istifadeciler         → 401

════ @Public() — açıq qalır ════
GET  /saglamliq                 → 200
GET  /                          → 200
POST /auth/login                → 200

════ SƏHV TOKEN ════
Bearer sehv.token.deyeri        → 401""",
    d_izah="""Sistemin vəziyyəti: API artıq <strong>bağlıdır</strong>. Bütün
    qorunan endpoint-lər tokensiz <code>401</code> verir, yalnız
    <code>@Public()</code> işarəlilər açıqdır. Diqqət yetirin ki,
    <code>POST /auth/login</code> <code>200</code> verir — bu, həm
    <code>@Public()</code>-in, həm də <code>@HttpCode(200)</code>-ün işlədiyini
    göstərir. Səhv token də <code>401</code> verir, çünki imza uyğun gəlmir —
    yəni token <em>formatı</em> düzgün olsa da <em>məzmunu</em> etibarsızdır.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=11,
    ad="Seed skripti — dörd rol üçün istifadəçi",
    a="""Sistemi yoxlamaq üçün hər roldan bir istifadəçi lazımdır. Seed skripti
    onları yaradır və <strong>idempotentdir</strong>: ikinci dəfə işlətsəniz
    dublikat yaratmır, sadəcə şifrəni yeniləyir. Bu, <code>ON CONFLICT DO
    UPDATE</code> sayəsində mümkündür. Şifrələr bazaya heç vaxt açıq
    yazılmır — yalnız bcrypt hash-i.""",
    b=[
        ("scripts/seed-auth.ts", fayl("scripts/seed-auth.ts")),
        ("package.json", fayl("package.json")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Skript və npm əmri yerindədirmi?
ls -l scripts/seed-auth.ts
grep -n 'seed:auth' package.json

# 2) ⚠️ İDEMPOTENTLİK — iki dəfə işlət, say dəyişməsin
npm run seed:auth
export PGPASSWORD=arti_secret_2025
psql -U arti_user -w -d arti_baza -tAc \\
  "SELECT count(*)::int FROM kadrlar.istifadeciler"

npm run seed:auth
psql -U arti_user -w -d arti_baza -tAc \\
  "SELECT count(*)::int FROM kadrlar.istifadeciler"

# 3) ⚠️ Şifrə AÇIQ saxlanılmır
psql -U arti_user -w -d arti_baza -tAc \\
  "SELECT email || ' → ' || left(parol_hash, 7) || '...' FROM kadrlar.istifadeciler"
""",
    c_olmaz="""$ npm run seed:auth      # ON CONFLICT olmasa:

════ İstifadəçilər yaradılır ════
  ✓ id= 2  admin@arti.edu.az        admin      şifrə: 123456
  ...
════ CƏMİ: 4 istifadəçi ════

$ npm run seed:auth      # ikinci dəfə
ERROR:  duplicate key value violates unique constraint "istifadeciler_email_key"
DETAIL:  Key (email)=(admin@arti.edu.az) already exists.

   # və ya şifrəni AÇIQ saxlasaq:
$ psql ... "SELECT parol_hash FROM kadrlar.istifadeciler LIMIT 1"
 123456                  ← BÜTÜN istifadəçilərin şifrəsi açıq görünür!""",
    c_izah="""İki tələ var. Birincisi <strong>idempotentlik</strong>: seed skripti
    tez-tez işlədilir (yeni kompüter, baza sıfırlanması, test mühiti), ona görə
    ikinci işə salma xəta verməməlidir. <code>ON CONFLICT (email) DO UPDATE</code>
    mövcud sətri yeniləyir — nə dublikat, nə xəta. İkincisi isə
    <strong>hash</strong>: <code>bcrypt.hash()</code> olmasa şifrələr açıq
    saxlanılar və baza sızsa bütün istifadəçilər dərhal itirilər. Hash ilə isə
    hücumçu hər şifrə üçün ~50 ms sərf etməlidir — bu, milyonlarla şifrə üçün
    illərlə vaxt deməkdir.""",
    d="""$ npm run seed:auth

════ İstifadəçilər yaradılır ════

  ✓ id= 2  admin@arti.edu.az        admin      şifrə: 123456
  ✓ id= 3  muhendis@arti.edu.az     muhendis   şifrə: 123456
  ✓ id= 4  maliyyeci@arti.edu.az    maliyyeci  şifrə: 123456
  ✓ id= 5  baxici@arti.edu.az       baxici     şifrə: 123456

════ CƏMİ: 4 istifadəçi ════

$ npm run seed:auth      # İKİNCİ dəfə — yenə 4
════ CƏMİ: 4 istifadəçi ════

$ psql ... "SELECT email || ' → ' || left(parol_hash, 7) || '...' ||
                   '  rol: ' || rol FROM kadrlar.istifadeciler ORDER BY id"
admin@arti.edu.az     → $2b$10$...  rol: admin
muhendis@arti.edu.az  → $2b$10$...  rol: muhendis
maliyyeci@arti.edu.az → $2b$10$...  rol: maliyyeci
baxici@arti.edu.az    → $2b$10$...  rol: baxici""",
    d_izah="""Sistemin vəziyyəti: dörd rol üçün dörd istifadəçi hazırdır və
    ikinci işə salma sayı dəyişmədi — <strong>idempotentlik işləyir</strong>.
    Bazada şifrələr <code>$2b$10$...</code> kimi görünür: <code>$2b$</code>
    bcrypt alqoritmidir, <code>10</code> isə "cost" parametridir (2<sup>10</sup> =
    1024 raund). Cost-u artırmaq şifrəni daha güclü edir, amma login-i də
    yavaşladır — 10 sənaye standartıdır. <code>parol_hash</code> sütununun adı
    <strong>mütləq belədir</strong>; <code>parol</code> yazsanız
    <code>column "parol" does not exist</code> xətası alacaqsınız.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=12,
    ad="Build və canlı RBAC yoxlaması",
    a="""İndi bütün parçalar yerindədir — serveri qaldırıb <strong>dörd rolun
    matrisini</strong> yoxlayırıq. Hər rol üçün token alırıq və üç fərqli endpoint-ə
    sorğu göndəririk: yaratma, silmə və istifadəçi siyahısı. Gözlənilən nəticə
    dəqiqdir: <code>admin</code> hər şeyi edir, <code>muhendis</code> yaradır amma
    silmir, <code>maliyyeci</code> və <code>baxici</code> yalnız oxuyur.""",
    b=[
        ("Terminal 1 — serveri qaldır", terminal("""cd ~/Deepseek_ARTI/DS_Backend
unset DATABASE_URL PGHOST

lsof -ti:4000 && kill $(lsof -ti:4000)
npm run build
npm run seed:auth
npm run start:dev""")),
        ("Terminal 2 — hər rol üçün token al və yadda saxla", terminal("""A=http://localhost:4000/api/v1

# ── Token AL və YADDA SAXLA ──
for rol in admin muhendis maliyyeci baxici; do
  T=$(curl -s -X POST "$A/auth/login" \\
    -H 'Content-Type: application/json' \\
    -d "{\\"email\\":\\"$rol@arti.edu.az\\",\\"parol\\":\\"123456\\"}" \\
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  echo "$T" > "/tmp/tok_$rol.txt"
  printf '%-10s %s simvol\\n' "$rol" "${#T}"
done

# Sonra hər yerdə belə oxu:
#   TA=$(cat /tmp/tok_admin.txt)
#   curl -s "$A/struktur/merkezler" -H "Authorization: Bearer $TA"
""")),
        ("Terminal 2 — RBAC matrisi", terminal("""A=http://localhost:4000/api/v1
J='Content-Type: application/json'
T() { cat "/tmp/tok_$1.txt"; }

echo "1) POST /struktur/merkezler  (admin, muhendis → 201)"
for rol in admin muhendis maliyyeci baxici; do
  printf '   %-10s → %s\\n' "$rol" "$(curl -s -o /dev/null -w '%{http_code}' \\
    -X POST "$A/struktur/merkezler" -H "$J" \\
    -H "Authorization: Bearer $(T $rol)" \\
    -d "{\\"ad\\":\\"RBAC $rol $(date +%s)\\"}")"
done

echo "2) DELETE /struktur/merkezler/1  (yalnız admin → 200/409)"
for rol in admin muhendis maliyyeci baxici; do
  printf '   %-10s → %s\\n' "$rol" "$(curl -s -o /dev/null -w '%{http_code}' \\
    -X DELETE "$A/struktur/merkezler/1" -H "Authorization: Bearer $(T $rol)")"
done

echo "3) GET /auth/istifadeciler  (yalnız admin → 200)"
for rol in admin muhendis maliyyeci baxici; do
  printf '   %-10s → %s\\n' "$rol" "$(curl -s -o /dev/null -w '%{http_code}' \\
    "$A/auth/istifadeciler" -H "Authorization: Bearer $(T $rol)")"
done

echo "4) GET /struktur/merkezler  (hamı → 200)"
for rol in admin muhendis maliyyeci baxici; do
  printf '   %-10s → %s\\n' "$rol" "$(curl -s -o /dev/null -w '%{http_code}' \\
    "$A/struktur/merkezler" -H "Authorization: Bearer $(T $rol)")"
done
""")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Server işləyirmi?
curl -s -o /dev/null -w 'sağlamlıq → %{http_code}\\n' \\
  http://localhost:4000/api/v1/saglamliq

# 2) Neçə marshrut var? (15 olmalıdır — 4 auth + 11 əvvəlki)
curl -s http://localhost:4000/docs-json | python3 -c "
import json, sys
d = json.load(sys.stdin)
say = 0
for yol in sorted(d['paths']):
    for m in d['paths'][yol]:
        say += 1
        auth = 'AUTH' if '/auth/' in yol else ''
        print(f'  {m.upper():6s} {yol:<38} {auth}')
print('  CƏMİ:', say, 'marshrut')
"

# 3) ⚠️ 403 cavabı hansı rolun lazım olduğunu deyir
curl -s "$A/auth/istifadeciler" -H "Authorization: Bearer $(cat /tmp/tok_baxici.txt)" \\
  | python3 -m json.tool

# 4) Test mərkəzlərini təmizlə (admin tokeni ilə)
psql -U arti_user -w -d arti_baza -tAc \\
  "SELECT id FROM struktur.merkezler WHERE ad LIKE 'RBAC %'" | while read -r i; do
    [ -n "$i" ] && curl -s -o /dev/null -X DELETE "$A/struktur/merkezler/$i" \\
      -H "Authorization: Bearer $(cat /tmp/tok_admin.txt)"
    echo "  təmizləndi: $i"
  done
""",
    c_olmaz="""$ node dist/main.js      # guard-lar qeyd olunmasa:\n$ curl -s -o /dev/null -w '%{http_code}\\n' localhost:4000/api/v1/struktur/merkezler\n200        ← TOKENSİZ! API tamamilə AÇIQ\n\n$ curl -X DELETE localhost:4000/api/v1/struktur/merkezler/5\n200        ← hər kəs silə bilər\n\n   # Və ən pisi: heç bir xəta, heç bir xəbərdarlıq yoxdur.\n   # Swagger sənədləşdirməsi də normal görünür.""",
    c_izah="""Guard-lar qeyd olunmasa API <strong>açıq qalır</strong> və bunu
    heç nə göstərmir — nə xəta, nə xəbərdarlıq. Yeganə yoxlama yolu canlı sorğu
    göndərməkdir: <code>curl</code> ilə tokensiz cəhd edin, <code>401</code>
    görməlisiniz. Bu, hər yerləşdirmədən sonra edilməli olan <strong>tüstü
    testidir</strong> (smoke test).""",
    d="""$ curl -s localhost:4000/docs-json | python3 -c "..."
  GET    /api/v1
  POST   /api/v1/auth/login                    AUTH
  GET    /api/v1/auth/profil                   AUTH
  POST   /api/v1/auth/qeydiyyat                AUTH
  GET    /api/v1/auth/istifadeciler            AUTH
  GET    /api/v1/kadrlar/emekdaslar
  GET    /api/v1/kadrlar/emekdaslar/icmal
  GET    /api/v1/kadrlar/emekdaslar/{id}
  GET    /api/v1/saglamliq
  GET    /api/v1/struktur/merkezler
  POST   /api/v1/struktur/merkezler
  GET    /api/v1/struktur/merkezler/statistika
  GET    /api/v1/struktur/merkezler/{id}
  PATCH  /api/v1/struktur/merkezler/{id}
  DELETE /api/v1/struktur/merkezler/{id}
  CƏMİ: 15 marshrut

════════ RBAC MATRİSİ ════════

1) POST /struktur/merkezler
   admin      → 201
   muhendis   → 201
   maliyyeci  → 403
   baxici     → 403

2) DELETE /struktur/merkezler/1
   admin      → 409      ← rol keçdi, servis 409 verdi (bağlı şöbə var)
   muhendis   → 403
   maliyyeci  → 403
   baxici     → 403

3) GET /auth/istifadeciler
   admin      → 200
   muhendis   → 403
   maliyyeci  → 403
   baxici     → 403

4) GET /struktur/merkezler
   admin      → 200
   muhendis   → 200
   maliyyeci  → 200
   baxici     → 200

════════ 403 CAVABI ════════
{
    "ugur": false,
    "xeta": {
        "kod": "ICAZE_YOXDUR",
        "mesaj": "Bu əməliyyat üçün icazəniz yoxdur. Tələb olunan rol: admin. Sizin rol: baxici"
    },
    "yol": "/api/v1/auth/istifadeciler",
    "vaxt": "2026-09-21T05:42:53.275Z"
}""",
    d_izah="""<strong>Backend-3 tam işlək vəziyyətdədir.</strong> RBAC matrisi
    gözlənilən kimidir və hər sətir bir qərarı göstərir:
    <ul>
      <li><strong>Yaratma</strong> — <code>admin</code> və <code>muhendis</code>
          <code>201</code> alır; digərləri <code>403</code>.</li>
      <li><strong>Silmə</strong> — yalnız <code>admin</code> rol yoxlamasını keçir.
          <code>409</code> alması <em>yaxşı xəbərdir</em>: deməli guard keçdi və
          sorğu servisə çatdı; <code>409</code> isə "bağlı şöbə var" deməkdir.</li>
      <li><strong>İstifadəçi siyahısı</strong> — yalnız <code>admin</code>.</li>
      <li><strong>Oxuma</strong> — dörd rolun hamısı <code>200</code> alır.</li>
    </ul>
    <code>403</code> cavabı isə <strong>hansı rolun lazım olduğunu</strong> və
    <strong>istifadəçinin öz rolunu</strong> deyir — bu, frontend-də düzgün mesaj
    göstərməyə imkan verir.""",
)

# ─────────────────────────────────────────────────────────────────
addim(
    n=13,
    ad="Testlər — yeni auth testləri və köhnələrin yenilənməsi",
    a="""Backend-3 iki şey tələb edir: <strong>yeni</strong> auth testləri və
    <strong>köhnə</strong> testlərin yenilənməsi. Dərs 2-də yazdığımız struktur və
    kadrlar testləri API açıq ikən işləyirdi — indi isə token tələb olunur və
    onlar <code>401</code> alır. Bu, çox vacib bir dərsdir: təhlükəsizlik
    modelini dəyişəndə mövcud testlər də dəyişməlidir, əks halda ya testlər
    sınır, ya da səhv şeyi yoxlayır.""",
    b=[
        ("src/auth/auth.service.spec.ts", fayl("src/auth/auth.service.spec.ts")),
        ("test/backend3-auth.e2e-spec.ts", fayl("test/backend3-auth.e2e-spec.ts")),
        ("test/struktur.e2e-spec.ts", fayl("test/struktur.e2e-spec.ts")),
        ("test/kadrlar.e2e-spec.ts", fayl("test/kadrlar.e2e-spec.ts")),
    ],
    c_yoxla="""cd ~/Deepseek_ARTI/DS_Backend

# 1) Test faylları yerindədirmi?
ls -1 test/*.e2e-spec.ts

# 2) ⚠️ Köhnə testlər TOKEN alırmı?
grep -n 'auth/login\\|let token' test/struktur.e2e-spec.ts test/kadrlar.e2e-spec.ts

# 3) ⚠️ Köhnə testlərdə birbaşa request qalıbmı? (yalnız login olmalı)
grep -c 'request(app.getHttpServer())' test/struktur.e2e-spec.ts | xargs echo "  struktur:"

# 4) BÜTÜN testlər
npm test
npx vitest run --config vitest.config.e2e.ts
""",
    c_olmaz="""$ npx vitest run --config vitest.config.e2e.ts
   # Köhnə testlər token göndərməsə:

 ✓ test/backend3-auth.e2e-spec.ts (14 tests) 634ms
 ✓ test/saglamliq.e2e-spec.ts (4 tests) 112ms
 ❯ test/struktur.e2e-spec.ts (14 tests | 11 failed)
   × GET /struktur/merkezler → səhifələnmiş siyahı
     expected 200 "OK", got 401 "Unauthorized"
 ❯ test/kadrlar.e2e-spec.ts (7 tests | 6 failed)
   × GET /kadrlar/emekdaslar → tam profillə səhifələnmiş siyahı
     expected 200 "OK", got 401 "Unauthorized"

 Test Files  2 failed | 2 passed (4)
      Tests  20 failed | 18 passed (38)""",
    c_izah="""Bu, <strong>gözlənilən</strong> nəticədir və düzgün reaksiya onu
    görməzdən gəlmək deyil: testlər <em>doğru şeyi</em> yoxlayır — API bağlandı
    və onlar bunu hiss edir. Həll testləri token göndərəcək şəkildə yeniləməkdir:
    <code>beforeAll</code>-da bir dəfə login olub tokeni yadda saxlamaq və hər
    sorğuya <code>Authorization</code> başlığı əlavə edən kiçik
    <code>api()</code> köməkçisi yazmaq. Ən yaxşısı, struktur testinə
    <strong>tokensiz <code>401</code></strong> yoxlaması da əlavə etməkdir.""",
    d="""$ npm test

 RUN  v4.1.11 /Users/royatalibova/Deepseek_ARTI/DS_Backend

 ✓ src/common/dto/sehife.dto.spec.ts (9 tests) 2ms
 ✓ src/saglamliq/saglamliq.service.spec.ts (3 tests) 40ms
 ✓ src/struktur/struktur.service.spec.ts (9 tests) 38ms
 ✓ src/auth/auth.service.spec.ts (8 tests) 397ms

 Test Files  4 passed (4)
      Tests  29 passed (29)

$ npx vitest run --config vitest.config.e2e.ts

 ✓ test/struktur.e2e-spec.ts (14 tests) 263ms
 ✓ test/kadrlar.e2e-spec.ts (7 tests) 221ms
 ✓ test/backend3-auth.e2e-spec.ts (14 tests) 634ms
 ✓ test/saglamliq.e2e-spec.ts (4 tests) 112ms

 Test Files  4 passed (4)
      Tests  39 passed (39)

──────────────────────────────────────────────
YEKUN: 29 unit + 39 e2e = 68 test""",
    d_izah="""<strong>Backend-3 tamamlandı.</strong> Ümumi vəziyyət:
    <ul>
      <li><strong>29 unit + 39 e2e = 68 test</strong> — Dərs 2-də 45 idi,
          yəni <strong>23 yeni test</strong> əlavə olundu.</li>
      <li><strong>15 marshrut</strong> — 4 auth + 11 əvvəlki.</li>
      <li><strong>Dörd rol</strong> işləyir: admin, mühendis, maliyyəçi, baxıcı.</li>
      <li><strong>Audit jurnalı</strong> hər yazma əməliyyatını yazır.</li>
      <li><strong>Timing attack</strong> qoruması ölçülüb: hər iki hal ~52 ms.</li>
    </ul>
    <p><strong>Növbəti dərs (Backend-4):</strong> AI qatı — DeepSeek API
    inteqrasiyası, RAG (vektor axtarış), təbii dil → SQL kəməkçisi, Excel/PDF
    ixracı və Docker ilə yerləşdirmə.</p>""",
)


ELAVE_CSS = """
  /* ─── ADDIM BLOKU (A/B/C/D) ─── */
  .addim {
    border: 2px solid #e2e8f0; border-radius: 18px;
    padding: 0 0 1rem; margin: 2.6rem 0;
    background: #fff; overflow: hidden;
  }
  .addim-basliq {
    font-size: 1.45rem; font-weight: 800; color: #fff;
    background: linear-gradient(135deg, #7c2d12, #ea580c);
    padding: 1.1rem 1.5rem; margin: 0 0 1.2rem;
    display: flex; align-items: center; gap: .9rem; line-height: 1.3;
  }
  .addim-no {
    display: inline-flex; align-items: center; justify-content: center;
    background: rgba(255,255,255,.22); color: #fff;
    min-width: 44px; height: 44px; border-radius: 12px;
    font-weight: 800; font-size: 1.05rem; flex-shrink: 0;
  }
  .addim-govde { padding: 0 1.4rem; }

  .hisse {
    border-radius: 12px; padding: 1.1rem 1.4rem;
    margin: 1rem 0; border-left: 6px solid;
  }
  .hisse-a { background: #eff6ff; border-color: #2563eb; }
  .hisse-b { background: #f8fafc; border-color: #0f172a; }
  .hisse-c { background: #fffbeb; border-color: #d97706; }
  .hisse-d { background: #f5f3ff; border-color: #7c3aed; }
  .hisse-basliq {
    display: block; font-weight: 800; font-size: .78rem;
    letter-spacing: 1.6px; text-transform: uppercase;
    margin-bottom: .75rem;
  }
  .hisse-a .hisse-basliq { color: #1d4ed8; }
  .hisse-b .hisse-basliq { color: #0f172a; }
  .hisse-c .hisse-basliq { color: #b45309; }
  .hisse-d .hisse-basliq { color: #6d28d9; }
  .hisse p:last-child { margin-bottom: 0; }
  .hisse h4 {
    font-size: .95rem; font-weight: 700; color: #334155;
    margin: 1rem 0 .5rem;
  }
  .fayl-ad {
    display: inline-block; background: #1e293b; color: #7dd3fc;
    font-family: 'SF Mono', Menlo, Consolas, monospace;
    font-size: .74rem; font-weight: 600;
    padding: .28rem .85rem; border-radius: 6px; margin: .3rem 0 .4rem;
  }
  .olmaz {
    background: #fef2f2; border: 2px dashed #dc2626;
    border-radius: 10px; padding: .9rem 1.2rem; margin: 1rem 0 0;
  }
  .olmaz-basliq {
    display: block; font-weight: 800; font-size: .78rem;
    color: #b91c1c; letter-spacing: 1.2px; margin-bottom: .55rem;
  }
  .oldu {
    background: #f0fdf4; border: 2px solid #16a34a;
    border-radius: 10px; padding: .9rem 1.2rem; margin: 1rem 0 0;
  }
  .oldu-basliq {
    display: block; font-weight: 800; font-size: .78rem;
    color: #15803d; letter-spacing: 1.2px; margin-bottom: .55rem;
  }
  .cixis-xeber {
    background: #fef2f2; border-left: 5px solid #dc2626;
    padding: .6rem .9rem; border-radius: 8px; margin: .2rem 0 .8rem;
    font-size: .84rem; font-weight: 600; color: #991b1b;
  }
  .addim-icmal {
    display: flex; gap: .5rem; flex-wrap: wrap;
    padding: .9rem 1.4rem 0; font-size: .78rem;
  }
  .addim-icmal span {
    background: #f1f5f9; color: #475569; padding: .3rem .8rem;
    border-radius: 20px; font-weight: 700;
  }
  .icmal {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: .8rem; margin: 1.4rem 0;
  }
  .icmal a {
    display: block; background: #fff7ed; border: 2px solid #fed7aa;
    border-radius: 12px; padding: .85rem 1rem; text-decoration: none;
    color: #9a3412; font-weight: 700; font-size: .86rem;
    transition: .15s;
  }
  .icmal a:hover { background: #ffedd5; border-color: #ea580c; }
  .icmal a b { display: block; font-size: .7rem; color: #ea580c; letter-spacing: 1px; }
"""


# ══════════════════════════════════════════════════════════════════
#  HTML QURULMASI
# ══════════════════════════════════════════════════════════════════
def addim_html(x: dict) -> str:
    b_hisse = x.get("b_html") or ""
    if x.get("b_html"):
        pass
    else:
      for fayl_ad, kod in x["b"]:
        b_hisse += (
            f'    <p class="fayl-ad">{e(fayl_ad)}</p>\n'
            f'<pre><code>{e(kod)}</code></pre>\n'
        )

    return f"""<div class="addim">
  <h2 class="addim-basliq" id="a{x['n']}">
    <span class="addim-no">{x['n']}</span> {e(x['ad'])}
  </h2>
  <div class="addim-govde">

    <div class="hisse hisse-a">
      <span class="hisse-basliq">A · Bu addım nəyə görədir</span>
      <p>{x['a']}</p>
    </div>

    <div class="hisse hisse-b">
      <span class="hisse-basliq">B · Kod</span>
{b_hisse}    </div>

    <div class="hisse hisse-c">
      <span class="hisse-basliq">C · Yoxlama — kod düzgün yazıldı?</span>
      <p>Aşağıdaki əmrləri işlədin və nəticəni yoxlayın:</p>
<pre><code>{e(x['c_yoxla'])}</code></pre>
      <div class="olmaz">
        <span class="olmaz-basliq">⚠️ Bu kod olmasa nə olardı</span>
<pre><code>{e(x['c_olmaz'])}</code></pre>
        <p>{x['c_izah']}</p>
      </div>
    </div>

    <div class="hisse hisse-d">
      <span class="hisse-basliq">D · Bu koddan sonra sistemin durumu — ÇIXIŞ</span>
      <p class="cixis-xeber">⚠️ Bu blok <strong>çıxışdır</strong> — kopyalayıb terminala yapıştırmayın. Sadəcə oxuyun. Əmrlər B hissəsindədir.</p>
<pre><code>{e(x['d'])}</code></pre>
      <div class="oldu">
        <span class="oldu-basliq">✔ Nəticə</span>
        <p>{x['d_izah']}</p>
      </div>
    </div>

  </div>
  <div class="addim-icmal">
    <span>Addım {x['n']} / {len(ADDIMLAR)}</span>
    <span>A · niyə</span><span>B · kod</span>
    <span>C · yoxlama</span><span>D · durum</span>
  </div>
</div>
"""


def toc_html() -> str:
    return "".join(
        f'    <li><a href="#a{x["n"]}">{x["n"]}. {e(x["ad"])}</a></li>\n'
        for x in ADDIMLAR
    )


def icmal_html() -> str:
    return "".join(
        f'  <a href="#a{x["n"]}"><b>ADDIM {x["n"]}</b>{e(x["ad"])}</a>\n'
        for x in ADDIMLAR
    )


def main() -> None:
    css = CSS_FAYLI.read_text(encoding="utf-8").rstrip("\n") + "\n" + ELAVE_CSS
    addimlar = "\n".join(addim_html(x) for x in ADDIMLAR)
    n = len(ADDIMLAR)

    sened = f"""<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Backend 3 — Autentifikasiya, rollar və audit (A/B/C/D)</title>
<style>
{css}
</style>
</head>
<body>
<div class="container">

<header>
  <div class="lesson-badge">DS_Backend · Hissə 3 / 4</div>
  <h1>Backend 3 — Autentifikasiya, rollar və audit</h1>
  <p class="subtitle">Sistemi bağla, sonra açar paylaş — JWT token, dörd rol
    və hər dəyişikliyin izi. Hər addım 4 hissə: <strong>A</strong> niyə ·
    <strong>B</strong> kod · <strong>C</strong> yoxlama · <strong>D</strong> durum</p>
  <p class="meta">
    <span>NestJS 12</span>
    <span>Prisma 7</span>
    <span>{n} addım</span>
    <span>15 marshrut</span>
    <span>68 test</span>
  </p>
</header>

<div class="block block-ne">
  <span class="block-title">NƏ EDƏCƏYİK</span>
  <p>Backend-1-də yalnız iki endpoint vardı: sağlamlıq və kök. İndi
  <strong>ilk real modulları</strong> yazacağıq — ARTİ-nin mərkəzləri və
  əməkdaşları üçün tam API. Sonda <strong>11 marshrut</strong> və
  <strong>45 test</strong> olacaq.</p>
  <p><strong>Ön şərt:</strong> Backend-1 tamamlanmalıdır —
  <code>DS_Backend</code> işləyən serverlə qalxmalı, <code>/api/v1/saglamliq</code>
  <code>200</code> verməlidir. Yoxlamaq üçün:</p>
  <pre><code>cd ~/Deepseek_ARTI/DS_Backend
npm run build &amp;&amp; node dist/main.js
# ayrı terminalda:
curl -s localhost:4000/api/v1/saglamliq</code></pre>
</div>

<div class="block block-nece">
  <span class="block-title">NECƏ OXUMALI — hər addımın 4 hissəsi</span>
  <table>
    <tr><th>Hissə</th><th>Nə var</th><th>Kopyalanır?</th></tr>
    <tr><td><strong>A</strong></td><td>Bu addım nəyə görədir — 3-4 cümlə</td>
        <td>—</td></tr>
    <tr><td><strong>B</strong></td><td>Kod — <code>cat &gt; fayl &lt;&lt;'EOF'</code>
        formasında, birbaşa yapışdırıla bilər</td>
        <td style="color:#15803d"><strong>✅ Bəli</strong></td></tr>
    <tr><td><strong>C</strong></td><td>Yoxlama əmrləri +
        <span style="color:#b91c1c">bu kod olmasa nə olardı</span></td>
        <td style="color:#15803d"><strong>✅ Bəli</strong></td></tr>
    <tr><td><strong>D</strong></td><td>Sistemin bu koddan sonraki
        <strong>real</strong> çıxışı</td>
        <td style="color:#b91c1c"><strong>❌ Xeyr — oxuyun</strong></td></tr>
  </table>
  <p>C və D hissələrindəki bütün çıxışlar <strong>realdır</strong> — kodu
  bilərəkdən söndürüb alınmış xətalar və canlı sistemdən götürülmüş nəticələr.</p>
</div>

<div class="block block-xeber">
  <span class="block-title">⚠️ BU DƏRSDƏ NƏ YOXDUR</span>
  <ul>
    <li><strong>Autentifikasiya yoxdur</strong> — bütün endpoint-lər açıqdır.
        İstənilən şəxs <code>POST</code>/<code>DELETE</code> edə bilər.</li>
    <li><strong>Audit jurnalı yoxdur</strong> — kimin nə dəyişdiyi yazılmır.</li>
    <li><strong>AI qatı yoxdur</strong> — RAG, embedding və təbii dil sorğuları sonra.</li>
  </ul>
  <p>Bunlar qəsdən kənarda saxlanılıb: hər biri öz addımlarını tələb edir.
  <strong>Backend-3</strong> məhz autentifikasiya, rollar və auditdən başlayır.</p>
</div>

<div class="toc">
  <h3>📚 Addımlar</h3>
  <ol>
{toc_html()}  </ol>
</div>

<div class="icmal">
{icmal_html()}</div>

{addimlar}

<div class="success-box">
  <strong>Backend-2 tamamlandı — {n} addım.</strong> 11 marshrut ·
  səhifələmə və filtr hər siyahıda · 6 cədvəlli JOIN ·
  tam CRUD + konflikt idarəsi · 21 unit + 24 e2e = <strong>45 test</strong>.
  <strong>Növbəti dərs:</strong> autentifikasiya və rollar (JWT),
  <code>@Public()</code>/<code>@Roles()</code> dekoratorları və audit jurnalı.
</div>

<div class="block block-ipucu">
  <span class="block-title">🔁 GÜNDƏLİK İŞ AXINI</span>
  <table>
    <tr><th>#</th><th>Nə</th><th>Əmr</th></tr>
    <tr><td>1</td><td>Portu təmizlə</td>
        <td><code>kill $(lsof -ti:4000)</code></td></tr>
    <tr><td>2</td><td>Serveri qaldır <em>(T1)</em></td>
        <td><code>npm run start:dev</code></td></tr>
    <tr><td>3</td><td>Yoxla <em>(T2)</em></td>
        <td><code>curl -s localhost:4000/api/v1/struktur/merkezler</code></td></tr>
    <tr><td>4</td><td>Testlər</td>
        <td><code>npm test &amp;&amp; npx vitest run --config vitest.config.e2e.ts</code></td></tr>
    <tr><td>5</td><td>Yaz</td>
        <td><code>git add -A &amp;&amp; git commit -m "..."</code></td></tr>
  </table>
  <p><strong>Serveri dayandırmaq:</strong> T1-də <code>Ctrl + C</code>.
  <code>start:dev</code> rejimində faylı saxladıqca server özü yenilənir.</p>
</div>

</div>
<script>
  document.addEventListener('DOMContentLoaded', function () {{
    document.querySelectorAll('pre').forEach(function (pre) {{
      // D hissəsi ÇIXIŞDIR — kopyala düyməsi qoyulmur
      if (pre.closest('.hisse-d')) return;
      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.textContent = '📋 KOPYALA';
      btn.addEventListener('click', async function (ev) {{
        ev.preventDefault();
        var kod = pre.querySelector('code');
        var metn = kod ? kod.textContent : pre.textContent;
        try {{
          await navigator.clipboard.writeText(metn);
          btn.textContent = '✅ KOPYALANDI';
          btn.classList.add('copied');
          setTimeout(function () {{
            btn.textContent = '📋 KOPYALA';
            btn.classList.remove('copied');
          }}, 2000);
        }} catch (err) {{
          var ta = document.createElement('textarea');
          ta.value = metn;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          btn.textContent = '✅ KOPYALANDI';
          setTimeout(function () {{ btn.textContent = '📋 KOPYALA'; }}, 2000);
        }}
      }});
      pre.insertBefore(btn, pre.firstChild);
    }});
  }});
</script>
</body>
</html>
"""

    CIXIS.write_text(sened, encoding="utf-8")
    print(f"✅ {CIXIS.relative_to(KOK)}")
    print(f"   {sened.count(chr(10)) + 1} sətir · {len(ADDIMLAR)} addım × 4 hissə "
          f"= {len(ADDIMLAR) * 4} bölmə")


if __name__ == "__main__":
    main()
