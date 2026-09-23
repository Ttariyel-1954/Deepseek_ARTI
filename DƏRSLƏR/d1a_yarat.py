#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-1A — qurucu.

Addım 1–11-in geniş izahlarını, real kodunu və HƏQİQİ çıxışlarını bir
HTML dərsinə yığır. Həm də 10 yekun testi ayrı .sh faylları kimi yazır.

İSTİFADƏ:
    python3 d1a_yarat.py            # keşdən qur
    python3 d1a_yarat.py --icra     # hər şeyi yenidən icra et və qur
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
CIXIS = DERS_Q / "DS_Backend-1A.html"
TEST_Q = DERS_Q / "testler"
KES = pathlib.Path("/tmp/d1a_kes.json")
PORT = os.environ.get("TEST_PORT", "4000")
API = os.environ.get("TEST_A", "http://localhost:%s/api/v1" % PORT)


def yukle(ad):
    p = DERS_Q / ("d1a_%s.py" % ad)
    spec = importlib.util.spec_from_file_location("d1a_" + ad, p)
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


def sarla(skript: str) -> str:
    """Testi interaktiv shell-ə yapışdırmaq üçün təhlükəsiz hala salır."""
    return (PRELUDE + "\n\n"
            "# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır.\n"
            "(\n" + skript.strip("\n") + "\n)\n")


def muhit():
    o = os.environ.copy()
    o.update({"npm_config_cache": "/tmp/npmcache", "NO_COLOR": "1",
              "TERM": "dumb", "PYTHONIOENCODING": "utf-8",
              "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8",
              "PORT": PORT, "A": API, "LAYIHE": str(BACKEND)})
    o.pop("DATABASE_URL", None)
    o.pop("PGHOST", None)
    return o


def islet(emr, timeout=1200):
    r = subprocess.run(["bash", "-c", emr], cwd=str(BACKEND), env=muhit(),
                       capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8", errors="replace")
    return re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr).rstrip()


def fayl(yol):
    p = BACKEND / yol
    if not p.exists():
        raise SystemExit("XƏTA: fayl tapılmadı: %s" % p)
    return p.read_text(encoding="utf-8").rstrip("\n")


def blok(yol, govde, bashliq=None):
    dir_ = os.path.dirname(yol)
    pre = ("mkdir -p %s\n" % dir_) if dir_ else ""
    ad = bashliq or yol
    kod = pre + "cat > %s <<'EOF'\n%s\nEOF" % (yol, govde)
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


def addim_html(a, kes):
    cixis = kes["addim"].get(str(a["no"]), "")
    anlayis = "".join("<dt>%s</dt><dd>%s</dd>" % (e(k), v)
                      for k, v in a["anlayis"])
    fayllar = "".join(blok(y, fayl(y)) for y in a["fayllar"])
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
    <pre class="komanda"><code>%(c)s</code></pre>
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
        kod_izah=a["kod_izah"], c=e(a["c"].strip()), olmaz=e(a["olmaz"]),
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
<title>Backend 1A — Layihənin təməli və ilk işləyən API</title>
<style>%s</style>
</head>
<body>
<div class="konteyner">

<header>
  <h1>Backend 1A — Layihənin təməli və ilk işləyən API</h1>
  <p class="alt">Addım 1–11: layihə skeleti, TypeScript, <code>.env</code>,
  Prisma, baza bağlantısı, xəta filtri, sağlamlıq endpointi və serverin
  qalxması.</p>
  <p class="meta"><span>11 addım</span><span>10 yekun test</span>
  <span>I kurs üçün geniş izah</span><span>Hər çıxış realdır</span></p>
</header>

<div class="giris">
  <h2>Bu dərs kim üçündür və necə oxunmalıdır</h2>
  <p>Bu dərs <strong>proqramlaşdırmaya yeni başlayan</strong> tələbələr
  üçündür. Heç bir NestJS, Prisma və ya TypeScript bilgisi tələb olunmur —
  hər anlayış yerində izah olunur.</p>
  <p><strong>Hər addım dörd hissədən ibarətdir:</strong></p>
  <ul>
    <li><strong>A — niyə:</strong> bu addım nə üçün lazımdır, hansı problemi
        həll edir.</li>
    <li><strong>B — kod:</strong> yazılacaq fayllar və <em>hər kodun sətir-sətir
        izahı</em>.</li>
    <li><strong>C — yoxlama:</strong> kodu necə yoxlamaq olar və bu kod
        olmasa nə baş verərdi.</li>
    <li><strong>D — vəziyyət:</strong> yoxlamanın <em>həqiqi çıxışı</em> və
        addımdan sonra sistemin vəziyyəti.</li>
  </ul>
  <p><strong>Necə oxumalı:</strong> addımları <em>sıra ilə</em> işlədin. Hər
  addımda əvvəl A-nı oxuyun, sonra B-dəki kodu yazın, sonra C ilə yoxlayın.
  D hissəsi sizin çıxışınızla üst-üstə düşməlidirsə, düzgün getmisiniz.</p>
  <p><strong>Dərsin sonunda 10 test var.</strong> Hər test ayrıca Terminal
  skriptidir və dərsdə öyrəndiyinizi yoxlayır. Onları belə işlədin:</p>
  <p><code>cd ~/Deepseek_ARTI/DƏRSLƏR</code><br>
  <code>bash testler/yoxla.sh IA</code> — bütün 10 test<br>
  <code>bash testler/yoxla.sh IA.4</code> — yalnız bir test</p>
</div>

<div class="giris" style="background:#fef2f2;border-left-color:#ef4444">
  <h2 style="color:#b91c1c">⚠️ Tanış xətalar və onların həlli</h2>
  <p>İşləyərkən bu xətalardan birini görsəniz, panikaya düşməyin —
  hamısının səbəbi və həlli aşağıdadır:</p>
  <dl style="display:grid;grid-template-columns:auto 1fr;gap:.5rem 1rem;
             font-size:.93rem;margin-top:.7rem">
    <dt><code>ENOENT: uv_cwd</code><br><code>process.cwd failed</code></dt>
    <dd>Terminalınız <strong>silinmiş bir qovluğun</strong> içindədir — dərs
        materialı yeniləndiyi üçün köhnə qovluq silinib. Həll:
        <code>cd ~/Deepseek_ARTI</code> və ya sadəcə yeni Terminal açın.</dd>

    <dt><code>npm error ENOENT ... package.json</code></dt>
    <dd>Terminal layihə qovluğunda deyil. <code>pwd</code> yazıb harada
        olduğunuzu yoxlayın, sonra
        <code>cd ~/Deepseek_ARTI/DS_Backend</code>.</dd>

    <dt><code>listen EADDRINUSE :::4000</code></dt>
    <dd>Port məşğuldur — köhnə bir server hələ işləyir. Həll:
        <code>lsof -ti:4000 | xargs kill</code></dd>

    <dt><code>Cannot find module './....js'</code></dt>
    <dd>İmport-da <code>.js</code> uzantısı unudulub. Bu qayda ADDIM 3-də
        izah olunub: fayl <code>.ts</code> olsa da, import
        <code>.js</code> ilə yazılır.</dd>

    <dt><code>PrismaClientInitializationError</code></dt>
    <dd>Prisma 7-də adapter verilməyib (ADDIM 6) — ya da
        <code>DATABASE_URL</code> oxunmur. <code>.env</code> faylını və
        <code>unset DATABASE_URL PGHOST</code> əmrini yoxlayın.</dd>

    <dt><code>TS1219 / TS1206 (decorator)</code></dt>
    <dd><code>experimentalDecorators</code> ayarı yoxdur (ADDIM 3).</dd>

    <dt><code>Nest can't resolve dependencies</code></dt>
    <dd>Modul <code>exports</code> etmir və ya <code>imports</code>-a
        əlavə olunmayıb (ADDIM 7 və 10).</dd>
  </dl>
  <p style="margin-top:.7rem"><strong>Ümumi qayda:</strong> xəta mətnini
  <em>son sətirindən</em> oxuyun — səbəb adətən orada yazılır. Sonra
  <code>pwd</code> ilə qovluğu, <code>ls</code> ilə faylları yoxlayın.</p>
</div>

<div class="mund"><h2>Mündəricat</h2>%s</div>

%s

<h2 style="margin-top:3rem;border-top:3px solid #0f766e;padding-top:1.4rem">
Yekun testlər — 10 test</h2>
<p style="color:#475569;margin-bottom:1.4rem">Aşağıdaki testlər Dərs 1A-da
öyrəndiyiniz hər şeyi yoxlayır. Hər testin yanında <em>həqiqi çıxış</em> var —
onunla tutuşdurun. Testlər bir-birindən asılı deyil.</p>
%s

<footer>
  ARTİ ERP · Backend 1A · 11 addım · 10 yekun test<br>
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
#   bash testler/yoxla.sh IA.4     → yalnız bir test
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
