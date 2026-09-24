#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DS_Backend-2B — qurucu.

Addım 22–26-nın geniş izahlarını, real kodunu və HƏQİQİ çıxışlarını bir
HTML dərsinə yığır. Həm də 10 yekun testi ayrı .sh faylları kimi yazır.

İSTİFADƏ:
    python3 d2b_yarat.py            # keşdən qur
    python3 d2b_yarat.py --icra     # hər şeyi yenidən icra et və qur
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
CIXIS = DERS_Q / "DS_Backend-2B.html"
TEST_Q = DERS_Q / "testler"
KES = pathlib.Path("/tmp/d2b_kes.json")
PORT = os.environ.get("TEST_PORT", "4000")
API = os.environ.get("TEST_A", "http://localhost:%s/api/v1" % PORT)


def yukle(ad):
    p = DERS_Q / ("d2b_%s.py" % ad)
    spec = importlib.util.spec_from_file_location("d2b_" + ad, p)
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
<title>Backend 2B — Statistika, əlaqələr, toplu əməliyyatlar və audit</title>
<style>%s</style>
</head>
<body>
<div class="konteyner">

<header>
  <h1>Backend 2B — Statistika, əlaqələr, toplu əməliyyatlar və audit</h1>
  <p class="alt">Addım 22–26: statistika (<code>groupBy</code>,
<code>aggregate</code>, PL/pgSQL funksiyaları), əlaqələr və N+1 problemi,
toplu əməliyyatlar və tranzaksiyalar, audit loqu və baza trigger-ləri,
optimallaşdırma (<code>EXPLAIN ANALYZE</code>) və marşrut sırası.</p>
  <p class="meta"><span>5 addım</span><span>10 yekun test</span>
  <span>I kurs üçün geniş izah</span><span>Hər çıxış realdır</span></p>
</header>

<div class="giris">
  <h2>Bu dərs nədən bəhs edir</h2>
  <p>2A-da <code>emekdaslar</code> üçün tam CRUD yazdıq: yaratmaq, oxumaq,
  dəyişmək, silmək. Bu, <strong>təməl</strong>dir — amma real ERP sistemi
  bununla bitmir.</p>
  <p>2B-də <strong>dörd yeni qat</strong> əlavə edirik:</p>
  <ul>
    <li><strong>Statistika</strong> — «neçə əməkdaş hansı mərkəzdədir?»,
        «orta maaş nə qədərdir?». Prisma-nın <code>groupBy</code> və
        <code>aggregate</code> funksiyaları, həm də bazada <em>artıq
        yazılmış</em> PL/pgSQL funksiyaları.</li>
    <li><strong>Əlaqələr</strong> — bir əməkdaşın doktorantları,
        sertifikatları, elmi şura üzvlüyü. Burada
        <strong>N+1 problemi</strong> ilə tanış olacaq və onu
        <em>ölçəcəyik</em>.</li>
    <li><strong>Toplu əməliyyatlar</strong> — 50 əməkdaşı bir sorğuda
        yaratmaq, toplu maaş artımı, və <strong>atomiklik</strong>:
        yarısı yazılıb yarısı yazılmayan partiya olmasın.</li>
    <li><strong>Audit loqu</strong> — kim, nə vaxt, nəyi dəyişdi. Bazada
        artıq <em>trigger</em> var; biz onu oxuyacaq və tətbiq
        səviyyəsində zənginləşdirəcəyik.</li>
  </ul>
  <p>Sonda <strong>optimallaşdırma</strong> və <strong>marşrut
  sırası</strong> mövzuları var. Marşrut sırası xüsusilə məkrdir: səhv
  sıra heç bir xəta mesajı vermir, sadəcə bir endpoint
  <em>sükutla işləmir</em>. Bunu canlı sübut edəcəyik.</p>
  <p>⚠️ Dərs boyu <strong>real bazaya</strong> qarşı işləyirik — 14 real
  əməkdaş, 48 cədvəl, 5 000-dən çox audit qeydi. Bütün çıxışlar
  <em>realdır</em>.</p>
  <p><strong>Hər addım dörd hissədən ibarətdir:</strong>
  <strong>A</strong> — niyə, <strong>B</strong> — kod,
  <strong>C</strong> — yoxlama, <strong>D</strong> — həqiqi çıxış.
  Əlavə olaraq hər addımda <strong>«Yeni anlayışlar»</strong> lüğəti,
  <strong>«Kodun sətir-sətir izahı»</strong> və
  <strong>«Tez-tez verilən suallar»</strong> var.</p>
  <p><strong>Dərsin sonunda 10 yekun test var.</strong> Onları belə işlədin:</p>
  <p><code>cd ~/Deepseek_ARTI/DƏRSLƏR</code><br>
  <code>bash testler/yoxla.sh IIB</code> — bütün 10 test<br>
  <code>bash testler/yoxla.sh IIB.4</code> — yalnız bir test</p>
</div>

<div class="giris" style="background:#fef2f2;border-left-color:#ef4444">
  <h2 style="color:#b91c1c">⚠️ 2B dərsinə aid tanış xətalar</h2>
  <p>Bu dərsdə ən çox rast gəlinən və ən məkрli xətalar aşağıdadır.</p>
  <dl style="display:grid;grid-template-columns:auto 1fr;gap:.6rem 1rem;
             font-size:.93rem;margin-top:.7rem">

    <dt><code>GET /emekdaslar/statistika</code> → <code>400</code><br>
        <code>Validation failed (numeric string is expected)</code></dt>
    <dd><strong>Dərsin ən məkrli xətası.</strong> Statistika endpointi
        heç vaxt çağırılmır, çünki <code>@Get(':id')</code> ondan
        <em>əvvəl</em> qeydiyyatdan keçib və «statistika» sözünü ID kimi
        tutur. Heç bir xəta mesajı səbəbi demir. Həll:
        <code>controllers</code> massivində <code>:id</code> olan
        controller-i <strong>ƏN SONA</strong> qoyun. Ətraflı:
        <strong>ADDIM 26</strong>.</dd>

    <dt><code>PathError: Unexpected ( at index …</code><br>
        <code>:id([0-9]+)</code> yazanda</dt>
    <dd>Express 5 + <code>path-to-regexp</code> 8 marşrutda <em>inline
        regex</em> dəstəkləmir. Express 4-də işləyən
        <code>:id(\d+)</code> sintaksisi artıq <strong>işləmir</strong>.
        Həll: sıra qaydasına güvənin, ya da yolu dəyişin.</dd>

    <dt><code>Unknown argument relationLoadStrategy</code></dt>
    <dd>Prisma 7-də bu seçim generator blokunda xüsusi ayar tələb edir.
        Bizim sxemdə aktiv deyil. Nəticə: hər əlaqə üçün AYRI SQL
        sorğusu gedir (ölçülmüş: 6 əlaqə = 12 sorğu). ADDIM 23.</dd>

    <dt><code>Unknown argument include</code> — <code>groupBy</code> içində</dt>
    <dd><code>groupBy</code> əlaqələri <strong>dəstəkləmir</strong>.
        Yalnız qruplaşdırılan sütunlar və aqreqatlar qaytarılır. Adları
        göstərmək üçün ikinci sorğu göndərib <code>Map</code> ilə
        birləşdirmək lazımdır. ADDIM 22.</dd>

    <dt><code>Cannot read properties of undefined (reading 'biri')</code><br>
        (<code>npx tsx</code> ilə Nest tətbiqi qaldıranda)</dt>
    <dd><strong>Vacib tapıntı:</strong> <code>tsx</code> <em>esbuild</em>
        işlədir və esbuild <code>emitDecoratorMetadata</code>-nı
        dəstəkləmir. Ona görə Nest konstruktor tiplərini oxuya bilmir və
        DI işləmir. Həll: Nest tətbiqini <strong>build edilmiş</strong>
        <code>dist/</code>-dən işlədin (<code>node dist/main.js</code>).
        Servis səviyyəsindəki testlər üçün isə <code>tsx</code> yararlıdır —
        orada servisi <em>əl ilə</em> yaradırıq.</dd>

    <dt><code>createManyAndReturn</code> → <em>Do not know how to serialize
        a BigInt</em></dt>
    <dd>Metod işləyir, sadəcə nəticəni <code>console.log</code> və ya
        <code>JSON.stringify</code> ilə çap etmək olmur. Həll: ID-ləri
        <code>String(s.id)</code> ilə çevirin. ADDIM 24.</dd>

    <dt><code>createMany</code> sətirləri QAYTARMIR</dt>
    <dd><code>createMany</code> yalnız <code>{ count: N }</code> verir.
        Yaradılan sətirləri görmək üçün
        <strong><code>createManyAndReturn</code></strong> işlədin
        (PostgreSQL-də dəstəklənir). ADDIM 24.</dd>

    <dt>Təkrar e-poçt <code>createMany</code>-də — HEÇ NƏ yazılmır</dt>
    <dd>Bu, xəta deyil, <strong>ATOMİKLİK</strong>dir. Bir sətir
        pozuntunu pozsa, PostgreSQL bütün <code>INSERT</code>-u ləğv edir.
        İstəyirsinizsə <code>skipDuplicates: true</code> işlədin — o zaman
        təkrar olanlar sadəcə atlanır. ADDIM 24.</dd>

    <dt><code>updateMany</code> <code>count</code>-u göndərilən ID
        sayından AZ-dır</dt>
    <dd>Bəzi ID-lər mövcud deyil. Bu, xəta deyil — sadəcə istifadəçiyə
        <strong>bildirmək</strong> lazımdır («3 göndərdiniz, 2 dəyişdi»).
        Sükutla az iş görmək ən pis davranışdır. ADDIM 24.</dd>

    <dt>+10%% artımdan sonra −10%% düzəliş əvvəlki dəyəri qaytarmır</dt>
    <dd>Riyazidir: <code>3000 × 1.1 = 3300</code>, amma
        <code>3300 × 0.9 = 2970 ≠ 3000</code>. Geri qaytarmaq üçün
        <strong>BÖLMƏK</strong> lazımdır (<code>÷1.1</code>), ya da dəqiq
        qiyməti yenidən yazmaq. ADDIM 24.</dd>

    <dt>Audit loqunda gözlənilməz qeydlər</dt>
    <dd>Bazada <code>audit.fn_audit_yaz()</code> trigger-i var və o,
        <strong>dörd cədvəli</strong> avtomatik izləyir
        (<code>kadrlar.emekdaslar</code>, <code>elm.tedqiqat_layiheleri</code>,
        <code>maliyye.budce</code>, <code>maliyye.satinalmalar</code>).
        Hər <code>INSERT</code>/<code>UPDATE</code>/<code>DELETE</code>
        loqa düşür. ADDIM 25.</dd>

    <dt>Audit loqu artmır — tranzaksiya geri qaytarılıb</dt>
    <dd>Trigger <strong>COMMIT</strong> anında işləyir. Tranzaksiya
        <code>ROLLBACK</code> olsa, nə məlumat, nə də audit qeydi qalır.
        Bu, <em>düzgün</em> davranışdır. ADDIM 25.</dd>

    <dt><code>division by zero</code> — faiz hesablamasında</dt>
    <dd>Əmsalı sıfıra bölmək. <code>faiz = -100</code> göndərsəniz
        <code>1 + (-100/100) = 0</code> olar və <code>multiply: 0</code>
        bütün maaşları <strong>sıfırlayar</strong>. Ona görə DTO-da
        <code>@Min(-50)</code> qoyulub. ADDIM 24.</dd>

    <dt>Kiçik bazada «paralel daha sürətlidir» nəticəsi ÇIXMIR</dt>
    <dd>14 sətirdə şəbəkə və keş vaxtı hər şeyi üstələyir (6 ms vs 7 ms).
        Fərqi görmək üçün <strong>bir neçə dəfə ölçüb minimumu</strong>
        götürmək lazımdır. Real fərq 10 000+ sətirdə görünür. ADDIM 23.</dd>

    <dt>İndeks var, amma sorğu <code>Seq Scan</code> işlədir</dt>
    <dd>Planlaşdırıcı (planner) qərar verir. Cəmi 14 sətir varsa,
        cədvəli başdan-başa oxumaq indeksdən <em>daha sürətlidir</em>.
        Seçicilik aşağıdırsa (14%% uyğunluq) da indeks işlədilmir.
        Yoxlamaq üçün <code>EXPLAIN ANALYZE</code>. ADDIM 26.</dd>

    <dt><code>ILIKE '%%mətn%%'</code> heç vaxt indeks işlətmir</dt>
    <dd>B-ağacı indeksi yalnız <em>soldan</em> uyğunluqda kömək edir.
        <code>%%</code> ilə başlayan axtarış üçün
        <code>pg_trgm</code> genişlənməsi və <code>GIN</code> indeksi
        lazımdır. ADDIM 26.</dd>
  </dl>
  <p style="margin-top:.7rem"><strong>Ümumi qayda:</strong> əvvəlcə
  <em>ölçün</em> (<code>EXPLAIN ANALYZE</code>, sorğu sayğacı), sonra
  optimallaşdırın. «Yəqin ki, bu yavaşdır» — optimallaşdırmanın ən pis
  başlanğıcıdır.</p>
</div>

<div class="mund"><h2>Mündəricat</h2>%s</div>

%s

<h2 style="margin-top:3rem;border-top:3px solid #0f766e;padding-top:1.4rem">
Yekun testlər — 10 test</h2>
<p style="color:#475569;margin-bottom:1.4rem">Aşağıdaki testlər Dərs 2B-də
öyrəndiyiniz hər şeyi yoxlayır. Hər testin yanında <em>həqiqi çıxış</em> var —
onunla tutuşdurun. Testlər bir-birindən asılı deyil.</p>
%s

<footer>
  ARTİ ERP · Backend 2B · 5 addım · 10 yekun test<br>
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
#   bash testler/yoxla.sh IIB.4    → yalnız bir test
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
