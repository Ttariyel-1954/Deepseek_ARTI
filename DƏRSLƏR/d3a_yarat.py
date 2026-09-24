#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-3A — qurucu.

Addım 27–31-in geniş izahlarını, real kodunu və HƏQİQİ çıxışlarını bir
HTML dərsinə yığır. Həm də 10 yekun testi ayrı .sh faylları kimi yazır.

İSTİFADƏ:
    python3 d3a_yarat.py            # keşdən qur
    python3 d3a_yarat.py --icra     # hər şeyi yenidən icra et və qur
"""
from __future__ import annotations

import html
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
DERS_Q = KOK / "DƏRSLƏR"
BACKEND = pathlib.Path(os.environ.get("BACKEND", str(KOK / "DS_Backend")))
CIXIS = DERS_Q / "DS_Backend-3A.html"
TEST_Q = DERS_Q / "testler"
KES = pathlib.Path("/tmp/d3a_kes.json")
PORT = os.environ.get("TEST_PORT", "4000")
API = os.environ.get("TEST_A", "http://localhost:%s/api/v1" % PORT)


def yukle(ad):
    p = DERS_Q / ("d3a_%s.py" % ad)
    spec = importlib.util.spec_from_file_location("d3a_" + ad, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


METIN = yukle("metin")
TEST_MOD = yukle("testler")
ADIMLAR = METIN.ADIMLAR
TESTLER = TEST_MOD.TESTLER
PRELUDE = 'LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"'


def e(m):
    return html.escape(str(m), quote=False)


def goster(yol: str) -> str:
    """Faylın MƏZMUNUNU göstərir — `cat >` sarğısı olmadan (istinad üçün)."""
    return ('<div class="kod-blok">\n'
            '    <div class="kod-basliq"><span>%s (istinad)</span>'
            '<button class="kopyala">KOPYALA</button></div>\n'
            '<pre><code>%s</code></pre>\n  </div>\n'
            % (e(yol), e(fayl(yol))))


def sarla(skript: str) -> str:
    """Testi interaktiv shell-ə yapışdırmaq üçün təhlükəsiz hala salır."""
    return (PRELUDE + "\n\n"
            "# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.\n"
            "(\n" + skript.strip("\n") + "\n)\n")


def muhit(layihe=BACKEND):
    o = os.environ.copy()
    o.update({"npm_config_cache": "/tmp/npmcache", "NO_COLOR": "1",
              "TERM": "dumb", "PYTHONIOENCODING": "utf-8",
              "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8",
              "PORT": PORT, "A": API})
    if layihe:
        o["LAYIHE"] = str(layihe)
    else:
        o.pop("LAYIHE", None)
    o.pop("DATABASE_URL", None)
    o.pop("PGHOST", None)
    return o


def islet(emr, timeout=1200, cwd=None, layihe=BACKEND):
    r = subprocess.run(["bash", "-c", emr], cwd=str(cwd or BACKEND),
                       env=muhit(layihe),
                       capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8", errors="replace")
    return re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr).rstrip()


def fayl(yol):
    p = BACKEND / yol
    if not p.exists():
        raise SystemExit("XƏTA: fayl tapılmadı: %s" % p)
    return p.read_text(encoding="utf-8").rstrip("\n")


GIRIS = ('# ⚠️ Əvvəlcə layihə qovluğuna keçirik — yoxdursa yaradılır.\n'
         '# Beləliklə bu bloku HARADAN yapışdırsanız da işləyir.\n'
         'mkdir -p "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"\n'
         'cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"\n')


def blok(yol, govde, bashliq=None):
    dir_ = os.path.dirname(yol)
    pre = ("mkdir -p %s\n" % dir_) if dir_ else ""
    ad = bashliq or yol
    kod = GIRIS + pre + "cat > %s <<'EOF'\n%s\nEOF" % (yol, govde)
    return ('  <div class="kod-blok b-kod">\n'
            '    <div class="kod-basliq"><span>%s</span>'
            '<button class="kopyala">KOPYALA</button></div>\n'
            '<pre><code>%s</code></pre>\n  </div>\n'
            % (e(ad), e(kod)))


# ── İCRA ────────────────────────────────────────────────────────────
def icra():
    kes = {"addim": {}, "test": {}}
    print("ADDIMLAR (%d):" % len(ADIMLAR))
    for a in ADIMLAR:
        if a["no"] == 1 and a["c"].strip():
            # ⚠️ ADDIM 1 yol dəyişəni TƏYİN ETMİR — standart dəyər işlədilir,
            # yəni istifadəçinin REAL qovluğu. HEÇ NƏ SİLİNMİR və HEÇ NƏ
            # BOŞALDILMIR: əmr sadəcə `mkdir -p` + `cd` + `ls` + `npm install`
            # edir. Beləliklə istifadəçinin işi toxunulmaz qalır.
            cixis = islet(a["c"], cwd=pathlib.Path.home(), layihe="")
        else:
            cixis = islet(a["c"]) if a["c"].strip() else ""
        kes["addim"][str(a["no"])] = cixis
        print("  ✓ ADDIM %-2d %-44s (%d sətir)"
              % (a["no"], a["ad"][:44], len(cixis.splitlines())))
    print("\nTESTLƏR (%d):" % len(TESTLER))
    TEST_Q.mkdir(parents=True, exist_ok=True)
    for t in TESTLER:
        yol = TEST_Q / ("%s.sh" % t["no"])
        yol.write_text(sarla(t["skript"]), encoding="utf-8")
        r = subprocess.run(["bash", str(yol)], cwd=str(BACKEND), env=muhit(),
                           capture_output=True, text=True, timeout=1200,
                           encoding="utf-8", errors="replace")
        cixis = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr).rstrip()
        kes["test"][t["no"]] = {"kod": r.returncode, "cixis": cixis}
        print("  %s %-6s %-42s (exit %d)"
              % ("✓" if r.returncode == 0 else "✗", t["no"], t["ad"][:42],
                 r.returncode))
    KES.write_text(json.dumps(kes, ensure_ascii=False, indent=1), encoding="utf-8")
    return kes


def kesden():
    if not KES.exists():
        raise SystemExit("XƏTA: keş yoxdur — --icra ilə işlədin")
    return json.loads(KES.read_text(encoding="utf-8"))


# ── HTML ────────────────────────────────────────────────────────────
CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
       background:#eef2f7; color:#1e293b; line-height:1.85; padding:2rem 1rem; font-size:16.5px; }
.konteyner { max-width:1150px; margin:0 auto; background:#fff; border-radius:22px;
             box-shadow:0 15px 40px -15px rgba(15,23,42,.25); padding:3rem 3rem 4rem; }
header { border-bottom:5px solid #0f766e; padding-bottom:1.8rem; margin-bottom:2rem; }
header h1 { font-size:2.1rem; color:#115e59; margin-bottom:.4rem; }
header .alt { color:#64748b; }
header .meta { display:flex; gap:.5rem; flex-wrap:wrap; margin-top:1rem; }
header .meta span { background:#ccfbf1; color:#115e59; padding:.25rem .8rem;
                    border-radius:999px; font-size:.82rem; font-weight:600; }
h2 { color:#0f766e; }
.giris { background:#f0fdfa; border-left:5px solid #14b8a6; border-radius:10px;
         padding:1.3rem 1.6rem; margin:1.6rem 0; }
.giris h2 { font-size:1.15rem; margin-bottom:.6rem; }
.giris ul, .giris ol { margin:.5rem 0 .5rem 1.4rem; }
.giris li { margin-bottom:.3rem; }
.mund { background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px;
        padding:1.3rem 1.5rem; margin-bottom:2.2rem; }
.mund h2 { font-size:1.05rem; margin-bottom:.7rem; }
.mund a { display:block; text-decoration:none; color:#334155; padding:.28rem .5rem;
          border-radius:7px; font-size:.9rem; }
.mund a:hover { background:#ccfbf1; color:#115e59; }
.addim { border-top:3px solid #0f766e; margin-top:2.8rem; padding-top:1.4rem; }
.addim-basliq { font-size:1.35rem; color:#115e59; display:flex; gap:.7rem;
                align-items:baseline; margin-bottom:1rem; }
.addim-no { background:#0f766e; color:#fff; border-radius:8px; padding:.1rem .65rem;
            font-size:.95rem; flex-shrink:0; }
.hisse { margin:1.3rem 0; border-radius:12px; padding:1.1rem 1.3rem; }
.hisse-basliq { display:block; font-size:.78rem; font-weight:800; letter-spacing:.6px;
                text-transform:uppercase; margin-bottom:.7rem; }
.hisse-a { background:#f0fdfa; border-left:5px solid #14b8a6; }
.hisse-a .hisse-basliq { color:#0f766e; }
.hisse-b { background:#f8fafc; border-left:5px solid #64748b; }
.hisse-b .hisse-basliq { color:#475569; }
.hisse-c { background:#fffbeb; border-left:5px solid #f59e0b; }
.hisse-c .hisse-basliq { color:#b45309; }
.hisse-d { background:#faf5ff; border-left:5px solid #a855f7; }
.hisse-d .hisse-basliq { color:#7e22ce; }
.anlayis { background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px;
           padding:1rem 1.2rem; margin:1rem 0; }
.anlayis h4 { color:#1d4ed8; font-size:.92rem; margin-bottom:.5rem; }
.anlayis dl { display:grid; grid-template-columns:auto 1fr; gap:.35rem .9rem; font-size:.92rem; }
.anlayis dt { font-weight:700; color:#1e40af; }
.anlayis dd { color:#334155; }
.fayl-ad { background:#1e293b; color:#93c5fd; font-family:ui-monospace,Menlo,monospace;
           font-size:.82rem; padding:.4rem .8rem; border-radius:8px 8px 0 0; margin-top:.9rem; }
pre { background:#1e293b; color:#e2e8f0; padding:1rem 1.1rem; border-radius:0 0 8px 8px;
      overflow-x:auto; font-size:.84rem; line-height:1.6;
      font-family:ui-monospace,SFMono-Regular,Menlo,monospace; margin-bottom:.5rem; }
pre.cixis { background:#f0fdf4; color:#14532d; border:1px solid #86efac; border-radius:8px; }
pre.komanda { background:#0f172a; color:#a7f3d0; border-radius:8px; }
code { font-family:ui-monospace,Menlo,monospace; }
.hisse p code, .giris code, .anlayis code { background:#e2e8f0; padding:.08rem .35rem;
      border-radius:5px; font-size:.88em; color:#0f172a; }
.olmaz { background:#fef2f2; border:1px solid #fecaca; border-radius:10px;
         padding:1rem 1.2rem; margin-top:.9rem; }
.olmaz h4 { color:#b91c1c; font-size:.9rem; margin-bottom:.5rem; }
.olmaz pre { background:#fff; color:#7f1d1d; margin:0; }
.oldu { background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px;
        padding:1rem 1.2rem; margin-top:.9rem; }
.oldu h4 { color:#15803d; font-size:.9rem; margin-bottom:.4rem; }
.sual { margin-top:1rem; }
.sual details { background:#fff; border:1px solid #e2e8f0; border-radius:9px;
                padding:.6rem .9rem; margin-bottom:.5rem; }
.sual summary { cursor:pointer; font-weight:700; color:#0f766e; font-size:.94rem; }
.sual p { margin-top:.5rem; color:#334155; font-size:.94rem; }
.test { border:1px solid #e2e8f0; border-radius:16px; padding:1.5rem 1.6rem;
        margin-bottom:1.7rem; }
.test h3 { font-size:1.1rem; display:flex; gap:.6rem; align-items:baseline; margin-bottom:.6rem; }
.test h3 .no { background:#0f766e; color:#fff; padding:.1rem .6rem; border-radius:7px;
               font-size:.86rem; flex-shrink:0; }
.test .giris-metn { color:#475569; font-size:.95rem; margin-bottom:1rem; }
.neticə { background:#065f46; color:#a7f3d0; font-size:.76rem; font-weight:700;
          padding:.35rem .8rem; border-radius:8px 8px 0 0; letter-spacing:.4px; }
.kod-blok { margin-bottom:.9rem; }
.kod-basliq { display:flex; justify-content:space-between; align-items:center;
  background:#334155; color:#cbd5e1; font-size:.76rem; font-weight:700;
  letter-spacing:.4px; padding:.38rem .85rem; border-radius:8px 8px 0 0;
  text-transform:uppercase; }
.kod-blok pre { border-radius:0 0 8px 8px; margin-bottom:0; }
.kod-basliq.cixis-basliq { background:#4c1d95; color:#ddd6fe; }
.kopyala, .kopyala-hamisi { background:#0d9488; color:#fff; border:none;
  padding:.26rem .72rem; border-radius:6px; font-size:.72rem; font-weight:800;
  cursor:pointer; letter-spacing:.3px; font-family:inherit; }
.kopyala:hover, .kopyala-hamisi:hover { background:#0f766e; }
.kopyala.ok, .kopyala-hamisi.ok { background:#16a34a; }
.kopyala-hamisi { display:block; width:100%; margin:.2rem 0 1rem; padding:.55rem;
  font-size:.8rem; background:#115e59; }
.cixis-xeber { background:#fef2f2; border:1px solid #fecaca; color:#b91c1c;
  border-radius:8px; padding:.55rem .9rem; font-size:.88rem; margin-bottom:.7rem; }
footer { margin-top:3rem; padding-top:1.4rem; border-top:2px solid #e2e8f0;
         color:#94a3b8; font-size:.85rem; text-align:center; }
@media print { body{background:#fff;padding:0;} .konteyner{box-shadow:none;padding:0;} }
"""


def c_metn(a) -> str:
    """C blokunu mötərizəyə alır və B fayllarının yerində olduğunu yoxlayır.

    ⚠️ Şagird bir addımda BİRDƏN ÇOX fayl bloku olanda yalnız birini
    kopyalaya bilər (məsələn ADDIM 5-də «schema.prisma» var, amma
    «prisma.config.ts» yox). O zaman Prisma anlaşılmaz xəta verir.
    Bu yoxlama dərhal deyir ki, hansı fayl çatışmır.
    """
    c = a["c"].strip("\n")
    fayllar = a.get("fayllar", [])
    setir = ['cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"']
    if fayllar:
        setir += [
            '',
            '# ⚠️ ŞƏRT: bu addımın B blokundaki fayllar yerində olmalıdır',
            'catmadi=0',
            'for f in %s; do' % " ".join('"%s"' % f for f in fayllar),
            '  [ -f "$f" ] || { echo "  ✗ $f YOXDUR"; catmadi=1; }',
            'done',
            'if [ "$catmadi" = "1" ]; then',
            '  echo ""',
            '  echo "╔══════════════════════════════════════════════════════════╗"',
            '  echo "║  ⚠️  B BLOKUNDAKI FAYLLAR YOXDUR                         ║"',
            '  echo "║  HƏLL: bu addımın B blok(lar)ını KOPYALA ilə işlədin,    ║"',
            '  echo "║        sonra bu addıma qayıdın.                          ║"',
            '  echo "╚══════════════════════════════════════════════════════════╝"',
            '  exit 1',
            'fi',
            'echo "  ✓ B faylları yerindədir"',
        ]
    setir.append('')
    setir.append(c)
    return "(\n" + "\n".join(setir) + "\n)"


def addim_html(a, kes):
    cixis = kes["addim"].get(str(a["no"]), "")
    anlayis = "".join("<dt>%s</dt><dd>%s</dd>" % (e(k), v)
                      for k, v in a["anlayis"])
    fayllar = "".join(blok(y, fayl(y)) for y in a["fayllar"])
    fayllar += "".join(goster(y) for y in a.get("goster", []))
    suallar = "".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (q, c)
        for q, c in a["sual"])
    return """<section class="addim" id="a%(no)d">
<h2 class="addim-basliq"><span class="addim-no">%(no)d</span> %(ad)s</h2>

<div class="hisse hisse-a">
  <span class="hisse-basliq">A · Bu addım niyə var</span>
  %(a)s
  <div class="anlayis"><h4>Yeni anlayışlar</h4><dl>%(anlayis)s</dl></div>
</div>

<div class="hisse hisse-b">
  <span class="hisse-basliq">B · Kod</span>
  %(fayllar)s
  <button class="kopyala-hamisi" data-addim="a%(no)d">
    ADDIMIN BÜTÜN KODUNU KOPYALA (bütün fayllar bir yerdə)</button>
  <h4 style="margin-top:1rem;color:#334155">Kodun sətir-sətir izahı</h4>
  %(kod_izah)s
</div>

<div class="hisse hisse-c">
  <span class="hisse-basliq">C · Yoxlama — həqiqi çıxış</span>
  <p>Aşağıdaki əmrləri işlədin. Nəticə elə bu dərsin D hissəsində göstərilib:</p>
  <div class="kod-blok">
    <div class="kod-basliq"><span>Terminal əmrləri</span>
      <button class="kopyala">KOPYALA</button></div>
    <pre class="komanda"><code>%(cg)s</code></pre>
  </div>
  <div class="olmaz"><h4>⚠️ Bu kod olmasa nə olardı</h4><pre><code>%(olmaz)s</code></pre>
    <p>%(c_izah)s</p></div>
</div>

<div class="hisse hisse-d">
  <span class="hisse-basliq">D · Sistemin vəziyyəti — həqiqi çıxış</span>
  <p class="cixis-xeber">⚠️ Bu blok <strong>çıxışdır</strong> — kopyalamaq
  üçün deyil, oxumaq üçündür. Əmrlər C hissəsindədir.</p>
  <div class="kod-blok">
    <div class="kod-basliq cixis-basliq">
      <span>ÇIXIŞ — real nəticə</span></div>
    <pre class="cixis"><code>%(cixis)s</code></pre>
  </div>
  <div class="oldu"><h4>✔ Nəticə</h4>%(d_izah)s</div>
</div>

<div class="sual"><h4 style="color:#0f766e;font-size:.95rem">Tez-tez verilən suallar</h4>
%(suallar)s</div>
</section>""" % dict(
        no=a["no"], ad=e(a["ad"]), a=a["a"], anlayis=anlayis, fayllar=fayllar,
        kod_izah=a["kod_izah"],
        c=e(a["c"].strip()),
        cg=e(c_metn(a)),
        olmaz=e(a["olmaz"]),
        c_izah=a["c_izah"], cixis=e(cixis), d_izah=a["d_izah"], suallar=suallar)


def test_html(t, kes):
    n = kes["test"].get(t["no"], {})
    xeta = n.get("kod", 0) != 0
    return """<article class="test" id="t-%(id)s">
  <h3><span class="no">%(no)s</span> %(ad)s</h3>
  <p class="giris-metn">%(giris)s</p>
  <div class="kod-blok">
    <div class="kod-basliq"><span>Terminal skripti —
      DƏRSLƏR/testler/%(no)s.sh</span>
      <button class="kopyala">KOPYALA</button></div>
    <pre><code>%(skript)s</code></pre>
  </div>
  <div class="neticə" style="background:%(rəng)s">GÖZLƏNİLƏN NƏTİCƏ — real çıxış (exit %(kod)s)</div>
<pre class="cixis" style="border-radius:0 0 8px 8px"><code>%(cixis)s</code></pre>
</article>""" % dict(
        id=t["no"].replace(".", "-"), no=e(t["no"]), ad=e(t["ad"]),
        giris=t["giris"], skript=e(sarla(t["skript"]).strip()),
        rəng="#7f1d1d" if xeta else "#065f46", kod=n.get("kod", "?"),
        cixis=e(n.get("cixis", "(icra edilməyib)")))


JS = """
// ⚠️ file:// ilə açıldıqda navigator.clipboard işləmir — ona görə
// köhnə üsul (execCommand) ehtiyat variant kimi saxlanılır.
function kopyalaMetn(metn, geri) {
  function kocur() {
    var t = document.createElement('textarea');
    t.value = metn;
    t.style.position = 'fixed';
    t.style.top = '-1000px';
    document.body.appendChild(t);
    t.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(t);
    geri();
  }
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(metn).then(geri).catch(kocur);
  } else {
    kocur();
  }
}

function qisaGeri(d, metn) {
  var kohne = d.textContent;
  d.textContent = metn;
  d.classList.add('ok');
  setTimeout(function () { d.textContent = kohne; d.classList.remove('ok'); }, 1800);
}

document.querySelectorAll('.kopyala').forEach(function (d) {
  d.addEventListener('click', function () {
    var kod = d.closest('.kod-blok').querySelector('pre code');
    kopyalaMetn(kod.innerText, function () { qisaGeri(d, 'KOPYALANDI'); });
  });
});

document.querySelectorAll('.kopyala-hamisi').forEach(function (d) {
  d.addEventListener('click', function () {
    var addim = document.getElementById(d.dataset.addim);
    var parcalar = [];
    addim.querySelectorAll('.b-kod pre code').forEach(function (k) {
      parcalar.push(k.innerText);
    });
    kopyalaMetn(parcalar.join('\\n\\n'), function () {
      qisaGeri(d, parcalar.length + ' KOD BLOKU KOPYALANDI');
    });
  });
});
"""


def qur(kes):
    mund = "".join('<a href="#a%d">%d. %s</a>' % (a["no"], a["no"], e(a["ad"]))
                   for a in ADIMLAR)
    mund += "".join('<a href="#t-%s">%s %s</a>'
                    % (t["no"].replace(".", "-"), e(t["no"]), e(t["ad"]))
                    for t in TESTLER)
    govde = "".join(addim_html(a, kes) for a in ADIMLAR)
    testler = "".join(test_html(t, kes) for t in TESTLER)
    return """<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Backend 3A — Autentifikasiya: parol, token və qoruyucular</title>
<style>%s</style>
</head>
<body>
<div class="konteyner">

<header>
  <h1>Backend 3A — Autentifikasiya: parol, token və qoruyucular</h1>
  <p class="alt">Addım 27–31: parol təhlükəsizliyi
(<code>bcryptjs</code>, duz, dərəcə), istifadəçi qeydiyyatı və girişi,
JWT tokenləri (imza, müddət, saxtalaşdırma), qoruyucular
(<code>AuthGuard</code>, <code>RollerGuard</code>) və rol əsaslı
icazələr (RBAC).</p>
  <p class="meta"><span>5 addım</span><span>10 yekun test</span>
  <span>I kurs üçün geniş izah</span><span>Hər çıxış realdır</span></p>
</header>

<div class="giris">
  <h2>Bu dərs nədən bəhs edir</h2>
  <p>İndiyə qədər qurduğumuz API <strong>tamamilə açıqdır</strong> —
  hər kəs hər endpoint-i çağıra, hər məlumatı oxuya, hətta silə bilər.
  Bu dərsdə qapını bağlayırıq.</p>
  <p><strong>Dərs 3A beş addımdan ibarətdir:</strong></p>
  <ul>
    <li><strong>Parol təhlükəsizliyi</strong> — parolu niyə açıq
        saxlamaq olmaz, <em>hash</em> nədir, <em>duz</em> (salt) nə
        iş görür, niyə bcrypt <em>qəsdən yavaşdır</em>.</li>
    <li><strong>Qeydiyyat</strong> — istifadəçi yaratmaq, güclü parol
        qaydaları və <em>imtiyaz yüksəltmədən</em> qorunma.</li>
    <li><strong>Giriş və token</strong> — JWT nədir, niyə
        <em>şifrələnmir</em> sadəcə <em>imzalanır</em>, müddət nə deməkdir.</li>
    <li><strong>Qoruyucular</strong> — <code>AuthGuard</code> və
        <code>RollerGuard</code>, <code>@Ictimai()</code> dekoratoru,
        <strong>401 ilə 403 fərqi</strong>.</li>
    <li><strong>Canlı axın</strong> — qeydiyyat → giriş → token →
        qorunan endpoint → rol yoxlaması.</li>
  </ul>
  <p>⚠️ Dərs boyu <strong>real bazaya</strong> qarşı işləyirik: bazada
  artıq 4 istifadəçi var (<code>admin@</code>, <code>muhendis@</code>,
  <code>maliyyeci@</code>, <code>baxici@arti.edu.az</code>) və onların
  <strong>həqiqi bcrypt hash-ləri</strong> mövcuddur. Biz həmin real
  istifadəçilərlə giriş edib rollarını yoxlayacağıq.</p>
  <p><strong>Hər addım dörd hissədən ibarətdir:</strong>
  <strong>A</strong> — niyə, <strong>B</strong> — kod,
  <strong>C</strong> — yoxlama, <strong>D</strong> — həqiqi çıxış.
  Əlavə olaraq hər addımda <strong>«Yeni anlayışlar»</strong> lüğəti,
  <strong>«Kodun sətir-sətir izahı»</strong> və
  <strong>«Tez-tez verilən suallar»</strong> var.</p>
  <p><strong>Dərsin sonunda 10 yekun test var.</strong> Onları belə işlədin:</p>
  <p><code>cd ~/Deepseek_ARTI/DƏRSLƏR</code><br>
  <code>bash testler/yoxla.sh IIIA</code> — bütün 10 test<br>
  <code>bash testler/yoxla.sh IIIA.4</code> — yalnız bir test</p>
</div>

<div class="giris" style="background:#fef2f2;border-left-color:#ef4444">
  <h2 style="color:#b91c1c">⚠️ 3A dərsinə aid tanış xətalar</h2>
  <p>Autentifikasiya ilə işləyəndə ən çox rast gəlinən xətalar.</p>
  <dl style="display:grid;grid-template-columns:auto 1fr;gap:.6rem 1rem;
             font-size:.93rem;margin-top:.7rem">

    <dt><code>JWT_SECRET təyin olunmayıb və ya çox qısadır</code></dt>
    <dd>Server qalxmır — və bu, <em>yaxşıdır</em>. Səbəb: <code>.env</code>
        faylında <code>JWT_SECRET</code> yoxdur və ya 32 simvoldan
        qısadır. Həll:
        <code>openssl rand -base64 48</code> ilə sirr yaradıb
        <code>.env</code> faylına əlavə edin. ADDIM 31.</dd>

    <dt><code>secretOrPrivateKey must have a value</code></dt>
    <dd><code>JwtModule.register({ secret: process.env.JWT_SECRET })</code>
        yazıbsınız. Səbəb: bu sətir <em>fayl yüklənəndə</em> işləyir,
        <code>.env</code> isə <strong>sonra</strong> oxunur. Nəticə:
        <code>secret = undefined</code>. Həll:
        <code>JwtModule.registerAsync({ inject: [ConfigService], ... })</code>.
        ADDIM 31.</dd>

    <dt><code>Argument of type 'string' is not assignable to parameter
        of type 'number | StringValue | undefined'</code></dt>
    <dd><code>expiresIn: '1h'</code> yazmaq TypeScript 6-da xəta verir.
        Səbəb: <code>jsonwebtoken</code> xüsusi şablon tipi gözləyir.
        Həll: müd­dəti özümüz saniyəyə çevirək —
        <code>expiresIn: muddetiSaniyeye('1h')</code>. ADDIM 29.</dd>

    <dt><code>Cannot find module 'bcryptjs'</code><br>
        <code>Cannot find module '@nestjs/jwt'</code></dt>
    <dd>Paket yüklənməyib:
        <code>npm install @nestjs/jwt bcryptjs</code>.
        ⚠️ <code>bcryptjs</code> v3 tipləri ÖZÜ İLƏ GƏTİRİR —
        <code>@types/bcryptjs</code> lazım deyil.</dd>

    <dt><code>jwt malformed</code></dt>
    <dd>Token üç hissədən ibarət deyil. Səbəblər: token kəsilib,
        <code>Bearer</code> sözü də tokenə daxil edilib, ya da
        başlıq səhv formatdadır. Düzgün:
        <code>Authorization: Bearer eyJhbGci…</code> ADDIM 30.</dd>

    <dt><code>invalid signature</code></dt>
    <dd>İmza uyğun gəlmir. Səbəblər: (1) <code>JWT_SECRET</code>
        dəyişdirilib — köhnə tokenlər etibarsız oldu; (2) token
        saxtalaşdırılıb; (3) bir neçə server fərqli sirrlə işləyir.
        ADDIM 29.</dd>

    <dt><code>jwt expired</code></dt>
    <dd>Tokenin müddəti bitib. Bu, <em>normal</em> haldır — istifadəçi
        yenidən giriş etməlidir. Frontend 401 alanda giriş səhifəsinə
        yönləndirməlidir. ADDIM 29.</dd>

    <dt><code>401 Unauthorized</code> — hər sorğuda</dt>
    <dd>Token göndərilmir və ya səhv göndərilir. Yoxlayın:
        (1) başlığın adı <code>Authorization</code>-dır (kiçik hərflə
        yazsanız da olar); (2) format
        <code>Bearer &lt;token&gt;</code>; (3) <code>Bearer</code>-dən
        sonra BOŞLUQ var. ADDIM 30.</dd>

    <dt><code>403 Forbidden</code></dt>
    <dd>Token DÜZGÜNDÜR, istifadəçi tanınır — amma rolu kifayət etmir.
        Yenidən giriş etmək HEÇ NƏYİ dəyişmir. Administrator rolu
        dəyişməlidir. ADDIM 30.</dd>

    <dt>401 ilə 403-ü qarışdırmaq</dt>
    <dd>Ən çox edilən səhvdir. 401 = «səni tanımıram» (giriş lazım).
        403 = «tanıyıram, amma icazən yoxdur» (giriş kömək etmir).
        Qarışdırsaq frontend sonsuz giriş döngəsinə düşər.
        ADDIM 30.</dd>

    <dt>API cavabında <code>parol_hash</code> görünür</dt>
    <dd><strong>TƏCİLİ TƏHLÜKƏSİZLİK PROBLEMİ.</strong> Səbəb: Prisma
        sorğusunda <code>select</code> verilməyib və bütün sütunlar
        oxunur. Həll:
        <code>select: ISTIFADECI_SECIM</code> işlədin — beləliklə hash
        bazadan <em>heç oxunmur</em>. ADDIM 28.</dd>

    <dt><code>Nest can't resolve dependencies of AuthGuard</code></dt>
    <dd><code>AuthGuard</code> başqa modulda işlədilir, amma
        <code>AuthModule</code> onu <code>exports</code> etmir.
        Həll: <code>exports: [..., AuthGuard, RollerGuard]`.
        ADDIM 31.</dd>

    <dt><code>req.istifadeci</code> <code>undefined</code>-dır</dt>
    <dd>Guard-ların SIRASI səhvdir. <code>RollerGuard</code>
        <code>AuthGuard</code>-dan ƏVVƏL işləyirsə, rolu tapa bilmir —
        çünki istifadəçini sorğuya <code>AuthGuard</code> yazır. Düzgün
        sıra: <code>@UseGuards(AuthGuard, RollerGuard)</code>.
        ADDIM 31.</dd>

    <dt><code>@CariIstifadeci()</code> testdə işləmir</dt>
    <dd><code>createParamDecorator</code> yalnız metadata yaradır;
        əsl məntiq içəridə gizlənir və Nest onu sorğu gələndə çağırır.
        Ona görə məntiqi AYRI funksiya kimi yazıb ixrac edin
        (<code>cariIstifadeciFabriki</code>) — həm dekorator ondan
        istifadə edər, həm testlər birbaşa çağıra bilər. ADDIM 30.</dd>

    <dt><code>Cannot read properties of undefined (reading '…')</code><br>
        (<code>npx tsx</code> ilə Nest tətbiqi qaldıranda)</dt>
    <dd><code>tsx</code> <em>esbuild</em> işlədir və esbuild
        <code>emitDecoratorMetadata</code>-nı dəstəkləmir. Nest
        konstruktor tiplərini məhz bu metadatanı oxuyaraq öyrənir,
        ona görə DI işləmir. Həll: tətbiqi
        <code>node dist/main.js</code> ilə qaldırın. Servis
        səviyyəsindəki probe-lar isə <code>tsx</code> ilə işləyir —
        orada servisləri <em>əl ilə</em> yaradırıq.</dd>

    <dt>Tokeni <code>localStorage</code>-də saxlamaq</dt>
    <dd>İşləyir, amma <strong>XSS hücumuna qarşı həssasdır</strong>:
        səhifəyə yad JavaScript yeridilsə, tokeni oxuyub başqa yerə
        göndərə bilər. Daha təhlükəsiz yol:
        <code>httpOnly</code> + <code>Secure</code> +
        <code>SameSite</code> <em>cookie</em>. Bu, 3B dərsinin
        mövzusudur.</dd>

    <dt>Tokeni URL-də ötürmək (<code>?token=…</code>)</dt>
    <dd><strong>HEÇ VAXT ETMƏYİN.</strong> URL-lər brauzer tarixçəsində,
        server loqlarında, proxy loqlarında və <code>Referer</code>
        başlığında qalır. Token <em>yalnız</em>
        <code>Authorization</code> başlığı ilə ötürülməlidir.</dd>

    <dt>Mövcud e-poçtla qeydiyyat <code>400</code> verir (409 olmalıdır)</dt>
    <dd>Prisma <code>P2002</code> (unique pozuntusu) xətası
        <code>ConflictException</code>-a çevrilməlidir. <code>400</code>
        «məlumat səhvdir», <code>409</code> isə «resurs artıq var»
        deməkdir — frontend bu iki hala FƏRQLİ reaksiya verir.
        ADDIM 28.</dd>

    <dt>Mövcud olmayan ID-yə <code>PATCH</code> <code>500</code> verir</dt>
    <dd>Prisma <code>P2025</code> xətası xam halda yuxarı qalxır və
        <code>500</code> kimi görünür. ⚠️ Bu, monitorinq sistemini
        <em>yalançı alarmla</em> doldurur. Həll: yazmadan əvvəl
        <code>movcuddur(id)</code> yoxlaması və
        <code>NotFoundException</code>. ADDIM 28.</dd>

    <dt>Deaktiv hesab <code>400</code> verir (403 olmalıdır)</dt>
    <dd>Parol düzgün idi, yəni istifadəçi tanındı — maneə parol deyil,
        hesabın <em>vəziyyətidir</em>. Bu, məhz
        <code>403 Forbidden</code> halıdır. <code>400</code> versək,
        frontend «formu düzəlt» kimi başa düşər. ADDIM 28.</dd>

    <dt>⚠️⚠️ Test skriptində gövdə <em>yarımçıq</em> gedir və
        <code>400</code> qayıdır (bash 3.2 tələsi)</dt>
    <dd>macOS-un <strong>bash 3.2</strong>-də bu yazılış SƏHV işləyir:
        <pre style="background:#7f1d1d;color:#fff;border-radius:6px;padding:.7rem .9rem;font-size:.82rem;overflow-x:auto">gozle 'x' 401 "$(kod -X POST "$A" -d "{\"email\":\"$TE\"}")"
                 └──────── iç-içə dırnaqlar ────────┘</pre>
        <code>\"</code> ilə qorunan dırnaqlar itir, <code>{...}</code>
        isə <strong>qalin mötərizə genişlənməsinə</strong> (brace
        expansion) düşür — serverə <code>{"email":"..."}</code> yerinə
        <code>"email":"..."</code> gedir. Nəticə: <em>gözlənilməz</em>
        <code>400</code>, halbuki eyni sorğu əl ilə işləyir.
        <br><strong>Həll:</strong> gövdəni <em>dəyişəndə</em> saxlayın —
        <code>GOVDE='{"email":"…"}'</code> — və
        <code>-d "$GOVDE"</code> yazın. Eyni problem
        <code>$(...)</code>-nı başqa komutun <em>arqumenti</em> kimi
        işlətdikdə baş verir; təyin (<code>X=$(...)</code>) halında
        baş vermir. IIIA.6 testi bunun üçün xüsusi qeyd daşıyır.</dd>

    <dt>Test «keçdi» yazır, amma əslində uğursuzdur
        (<code>| sed</code> tələsi)</dt>
    <dd><code>if npx tsx prob.ts | sed 's/^/  /'; then …</code> —
        borunun (<em>pipe</em>) çıxış kodu <strong>SONUNCU</strong>
        komutdan götürülür. <code>sed</code> uğurlu olsa,
        <code>tsx</code> çöksə belə şərt <em>doğru</em> olar.
        <br><strong>Həll:</strong> əvvəlcə çıxışı fayla yazın, sonra
        kodu yoxlayın:
        <code>npx tsx prob.ts &gt;/tmp/p.log 2&gt;&amp;1 &amp;&amp; …</code>
        və ya <code>set -o pipefail</code> işlədin. IIIA.2 və IIIA.4
        testləri məhz bu səbəbdən yenidən yazıldı.</dd>

    <dt>BSD <code>sed</code>: <code>RE error: illegal byte sequence</code></dt>
    <dd>macOS-un <code>sed</code>-i qeyri-ASCII mətnlə bəzən belə xəta
        verir. Əvəzinə <code>awk '{ print "  " $0 }'</code> işlədin —
        bayt-bayt işləyir və problem yaratmır.</dd>
  </dl>
  <p style="margin-top:.7rem"><strong>Ümumi qayda:</strong> autentifikasiya
  xətaları iki kateqoriyaya bölünür — <em>«səni tanımıram»</em> (401)
  və <em>«icazən yoxdur»</em> (403). Əvvəlcə hansı kateqoriyada
  olduğunuzu müəyyənləşdirin, sonra səbəbi axtarın.</p>
</div>

<div class="mund"><h2>Mündəricat</h2>%s</div>

%s

<h2 style="margin-top:3rem;border-top:3px solid #0f766e;padding-top:1.4rem">
Yekun testlər — 10 test</h2>
<p style="color:#475569;margin-bottom:1.4rem">Aşağıdaki testlər Dərs 3A-da
öyrəndiyiniz hər şeyi yoxlayır. Hər testin yanında <em>həqiqi çıxış</em> var —
onunla tutuşdurun. Testlər bir-birindən asılı deyil.</p>
%s

<footer>
  ARTİ ERP · Backend 3A · 5 addım · 10 yekun test<br>
  Bütün çıxışlar real icradan götürülüb.
</footer>

</div>
<script>%s</script>
</body>
</html>
""" % (CSS, mund, govde, testler, JS)


ISLEDICI = r'''#!/bin/bash
# YEKUN TESTLƏR — işlədici
#   bash testler/yoxla.sh IA       → Dərs 1A-nın 10 testi
#   bash testler/yoxla.sh IB       → Dərs 1B-nin 10 testi
#   bash testler/yoxla.sh IIA      → Dərs 2A-nın 10 testi
#   bash testler/yoxla.sh IIB      → Dərs 2B-nin 10 testi
#   bash testler/yoxla.sh IIIA     → Dərs 3A-nın 10 testi
#   bash testler/yoxla.sh IIIA.4   → yalnız bir test
#   bash testler/yoxla.sh --siyahi → testlərin siyahısı
cd "$(dirname "$0")" || exit 1
unset DATABASE_URL PGHOST
YASIL=$'\033[32m'; QIRMIZI=$'\033[31m'; MAVI=$'\033[36m'; SIFIR=$'\033[0m'
KECDI=0; XETA=0; ISLENDI=0

if [ "$1" = "--siyahi" ] || [ "$1" = "-s" ]; then
  echo "Mövcud testlər:"
  for f in $(ls [A-Z]*.sh 2>/dev/null | sort -t. -k1,1 -k2,2n); do
    printf '  %s\n' "${f%.sh}"
  done
  exit 0
fi

if [ -z "$1" ]; then
  FAYLLAR=$(ls [A-Z]*.sh 2>/dev/null | sort -t. -k1,1 -k2,2n); BASLIQ="BÜTÜN TESTLƏR"
elif [ -f "$1.sh" ]; then
  FAYLLAR="$1.sh"; BASLIQ="TEST $1"
elif ls "$1".*.sh >/dev/null 2>&1; then
  FAYLLAR=$(ls "$1".*.sh 2>/dev/null | sort -t. -k1,1 -k2,2n); BASLIQ="DƏRS $1"
else
  echo "⚠️ «$1» tapılmadı. Siyahı: bash testler/yoxla.sh --siyahi"; exit 1
fi

SAY=0; for f in $FAYLLAR; do SAY=$((SAY + 1)); done
printf "\n${MAVI}════════════════════════════════════════════════════════════════${SIFIR}\n"
printf "${MAVI}  %s — %d test${SIFIR}\n" "$BASLIQ" "$SAY"
printf "${MAVI}════════════════════════════════════════════════════════════════${SIFIR}\n"
for f in $FAYLLAR; do
  printf "\n${MAVI}── %s ──────────────────────────────────────────────────────${SIFIR}\n" "${f%.sh}"
  if bash "$f"; then
    printf "${YASIL}  ✓ %s KEÇDİ${SIFIR}\n" "${f%.sh}"; KECDI=$((KECDI + 1))
  else
    printf "${QIRMIZI}  ✗ %s UĞURSUZ${SIFIR}\n" "${f%.sh}"; XETA=$((XETA + 1))
  fi
  ISLENDI=$((ISLENDI + 1))
done
printf "\n${MAVI}════════════════════════════════════════════════════════════════${SIFIR}\n"
printf "  İŞLƏDİLDİ: %d   ${YASIL}KEÇDİ: %d${SIFIR}   ${QIRMIZI}UĞURSUZ: %d${SIFIR}\n" "$ISLENDI" "$KECDI" "$XETA"
[ "$XETA" -eq 0 ] && { printf "  ${YASIL}✓ HAMISI KEÇDİ${SIFIR}\n"; exit 0; }
printf "  ${QIRMIZI}✗ %d TEST UĞURSUZ${SIFIR}\n" "$XETA"; exit 1
'''


def main():
    kes = icra() if "--icra" in sys.argv else kesden()
    (TEST_Q / "yoxla.sh").write_text(ISLEDICI, encoding="utf-8")
    os.chmod(TEST_Q / "yoxla.sh", 0o755)
    CIXIS.write_text(qur(kes), encoding="utf-8")
    s = CIXIS.read_text(encoding="utf-8")
    print("\n✅ %s" % CIXIS.relative_to(KOK))
    print("   %d sətir · %d addım · %d test"
          % (len(s.splitlines()), len(ADIMLAR), len(TESTLER)))


if __name__ == "__main__":
    main()
