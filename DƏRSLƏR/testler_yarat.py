#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YEKUN TESTLƏR — qurucu.

Dərs 1–4 üçün 65 test skriptini yazır, HAMISINI həqiqətən icra edir və
real çıxışları sənədə salır.

İSTİFADƏ:
    python3 testler_yarat.py              # yalnız HTML qur (keşdən)
    TEST_LAYIHE=~/Deepseek_ARTI/DS_Backend \
    TEST_A=http://localhost:4000/api/v1 \
    python3 testler_yarat.py --icra       # hamısını icra et və qur
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
CIXIS = DERS_Q / "Yekun_Testler.html"
ISCI = pathlib.Path("/tmp/yekun_testler")
KES_JSON = pathlib.Path("/tmp/yekun_testler_cixis.json")

LAYIHE = os.environ.get("TEST_LAYIHE", str(KOK / "DS_Backend"))
API = os.environ.get("TEST_A", "http://localhost:4000/api/v1")


def yukle(ad: str):
    p = DERS_Q / f"testler_{ad}.py"
    spec = importlib.util.spec_from_file_location(f"t_{ad}", p)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul.DERSLER


DERSLER = yukle("d1") + yukle("d2") + yukle("d3")


def e(metn: str) -> str:
    return html.escape(str(metn), quote=False)


def kecid(no: str) -> str:
    return "t-" + no.replace(".", "-")


# ── İCRA ─────────────────────────────────────────────────────────────
def icra_et() -> dict:
    ISCI.mkdir(parents=True, exist_ok=True)
    ortam = os.environ.copy()
    ortam.update({
        "LAYIHE": LAYIHE,
        "A": API,
        "npm_config_cache": "/tmp/npmcache",
        "NO_COLOR": "1",
        "TERM": "dumb",
        "PYTHONIOENCODING": "utf-8",
        "LANG": "en_US.UTF-8",
        "LC_ALL": "en_US.UTF-8",
    })
    ortam.pop("DATABASE_URL", None)
    ortam.pop("PGHOST", None)

    netice = {}
    cem = sum(len(d["testler"]) for d in DERSLER)
    for ders in DERSLER:
        for t in ders["testler"]:
            yol = ISCI / f"{t['no']}.sh"
            yol.write_text(t["skript"].strip("\n") + "\n", encoding="utf-8")
            r = subprocess.run(["bash", str(yol)], env=ortam, cwd=LAYIHE,
                               capture_output=True, text=True, timeout=900,
                               encoding="utf-8", errors="replace")
            cixis = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr).rstrip()
            netice[t["no"]] = {"kod": r.returncode, "cixis": cixis}
            print("  %s %-6s %-46s (exit %d, %d sətir)" % (
                "✓" if r.returncode == 0 else "✗", t["no"], t["ad"][:46],
                r.returncode, len(cixis.splitlines())))

    KES_JSON.write_text(json.dumps(netice, ensure_ascii=False, indent=1),
                        encoding="utf-8")
    print("\n  ✓ %d skript icra edildi" % cem)
    return netice


def kesden() -> dict:
    if not KES_JSON.exists():
        raise SystemExit("XƏTA: keş yoxdur — əvvəlcə --icra ilə işlədin")
    return json.loads(KES_JSON.read_text(encoding="utf-8"))


# ── HTML ─────────────────────────────────────────────────────────────
CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         background: #eef2f7; color: #1e293b; line-height: 1.8;
         padding: 2rem 1rem; font-size: 16px; }
  .container { max-width: 1080px; margin: 0 auto; background: #fff;
               border-radius: 22px; box-shadow: 0 15px 40px -15px rgba(15,23,42,.25);
               padding: 3rem 3rem 4rem; }
  header { border-bottom: 5px solid #1e40af; padding-bottom: 1.8rem; margin-bottom: 2rem; }
  header h1 { font-size: 2.1rem; color: #1e3a8a; margin-bottom: .5rem; }
  header .alt { color: #64748b; font-size: 1.02rem; }
  header .meta { display: flex; gap: .5rem; flex-wrap: wrap; margin-top: 1rem; }
  header .meta span { background: #dbeafe; color: #1e40af; padding: .25rem .8rem;
                      border-radius: 999px; font-size: .82rem; font-weight: 600; }

  .izah { background: #f0f9ff; border-left: 5px solid #0284c7; border-radius: 10px;
          padding: 1.1rem 1.4rem; margin: 1.5rem 0; font-size: .95rem; }
  .izah b { color: #075985; }
  .izah code { background: #e0f2fe; padding: .1rem .4rem; border-radius: 5px;
               font-size: .88em; }

  .mund { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px;
          padding: 1.4rem 1.6rem; margin-bottom: 2.5rem; }
  .mund h2 { font-size: 1.05rem; color: #334155; margin-bottom: .8rem; }
  .mund .setir { display: flex; flex-wrap: wrap; gap: .4rem; margin-bottom: .9rem; }
  .mund .setir b { color: #1e40af; font-size: .9rem; display: block; width: 100%;
                   margin-bottom: .2rem; }
  .mund a { text-decoration: none; background: #fff; border: 1px solid #cbd5e1;
            color: #334155; padding: .2rem .6rem; border-radius: 7px;
            font-size: .82rem; font-weight: 600; }
  .mund a:hover { background: #1e40af; color: #fff; border-color: #1e40af; }

  .ders-basliq { margin: 3rem 0 1.5rem; padding-bottom: .8rem;
                 border-bottom: 3px solid #1e40af; }
  .ders-basliq h2 { font-size: 1.5rem; color: #1e3a8a; }
  .ders-basliq p { color: #64748b; font-size: .95rem; margin-top: .4rem; }

  .test { border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.6rem 1.7rem;
          margin-bottom: 1.8rem; background: #fff; }
  .test > h3 { font-size: 1.12rem; color: #0f172a; margin-bottom: .7rem;
               display: flex; align-items: baseline; gap: .6rem; }
  .test > h3 .no { background: #1e40af; color: #fff; padding: .12rem .6rem;
                   border-radius: 7px; font-size: .88rem; font-weight: 700;
                   flex-shrink: 0; }
  .giris { color: #475569; font-size: .95rem; margin-bottom: 1.1rem; }
  .giris code { background: #f1f5f9; padding: .1rem .4rem; border-radius: 5px;
                font-size: .88em; color: #0f172a; }

  .blok { border-radius: 12px; overflow: hidden; margin-bottom: .9rem;
          border: 1px solid #e2e8f0; }
  .blok-basliq { display: flex; justify-content: space-between; align-items: center;
                 padding: .5rem .9rem; font-size: .78rem; font-weight: 700;
                 letter-spacing: .4px; text-transform: uppercase; }
  .blok pre { margin: 0; padding: .9rem 1rem; overflow-x: auto; font-size: .84rem;
              line-height: 1.6; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
  .skript .blok-basliq { background: #0f172a; color: #93c5fd; }
  .skript pre { background: #1e293b; color: #e2e8f0; }
  .netice .blok-basliq { background: #065f46; color: #a7f3d0; }
  .netice pre { background: #f0fdf4; color: #14532d; border-top: 2px solid #10b981; }

  .kopyala { background: #2563eb; color: #fff; border: none; padding: .28rem .7rem;
             border-radius: 6px; font-size: .72rem; font-weight: 700; cursor: pointer;
             letter-spacing: .3px; }
  .kopyala:hover { background: #1d4ed8; }
  .kopyala.ok { background: #059669; }

  .xeta-var .blok-basliq { background: #7f1d1d; color: #fecaca; }
  .xeta-var .netice pre { background: #fef2f2; color: #7f1d1d; border-top-color: #dc2626; }

  footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 2px solid #e2e8f0;
           color: #94a3b8; font-size: .85rem; text-align: center; }
  @media print {
    body { background: #fff; padding: 0; }
    .container { box-shadow: none; padding: 0; }
    .kopyala { display: none; }
    .test { break-inside: avoid; }
  }
"""

JS = """
document.querySelectorAll('.kopyala').forEach(function (duyme) {
  duyme.addEventListener('click', function () {
    var pre = duyme.closest('.blok').querySelector('pre');
    navigator.clipboard.writeText(pre.innerText).then(function () {
      duyme.textContent = 'KOPYALANDI';
      duyme.classList.add('ok');
      setTimeout(function () {
        duyme.textContent = 'KOPYALA';
        duyme.classList.remove('ok');
      }, 1600);
    });
  });
});
"""


def test_html(t: dict, kes: dict) -> str:
    n = kes.get(t["no"], {})
    cixis = n.get("cixis", "(icra edilməyib)")
    xeta = n.get("kod", 0) != 0
    return """<article class="test%s" id="%s">
  <h3><span class="no">%s</span> %s</h3>
  <p class="giris">%s</p>

  <div class="blok skript">
    <div class="blok-basliq"><span>Terminal — kopyala və işlət</span>
      <button class="kopyala">KOPYALA</button></div>
<pre><code>%s</code></pre>
  </div>

  <div class="blok netice">
    <div class="blok-basliq"><span>Gözlənilən nəticə — real çıxış</span>
      <span>exit %s</span></div>
<pre><code>%s</code></pre>
  </div>
</article>""" % (" xeta-var" if xeta else "", kecid(t["no"]), e(t["no"]), e(t["ad"]),
                  t["giris"], e(t["skript"].strip()), n.get("kod", "?"), e(cixis))


def qur(kes: dict) -> str:
    cem = sum(len(d["testler"]) for d in DERSLER)
    mund = []
    for d in DERSLER:
        kecidler = "".join(
            '<a href="#%s">%s</a>' % (kecid(t["no"]), t["no"])
            for t in d["testler"])
        mund.append('<div class="setir"><b>%s — %d test</b>%s</div>'
                    % (e(d["ad"]), len(d["testler"]), kecidler))

    govde = []
    for d in DERSLER:
        govde.append("""<div class="ders-basliq">
  <h2>%s</h2>
  <p>%s <strong>%d yekun test.</strong></p>
</div>""" % (e(d["ad"]), d["qisa"], len(d["testler"])))
        for t in d["testler"]:
            govde.append(test_html(t, kes))

    return """<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yekun testlər — Dərs 1–4 (65 test)</title>
<style>%s</style>
</head>
<body>
<div class="container">

<header>
  <h1>Yekun testlər — Dərs 1–4</h1>
  <p class="alt">Hər test ayrıca Terminal skriptidir. Kopyalayın, işlədin və
  çıxışı yanındaki nəticə ilə tutuşdurun. Testlər bir-birindən asılı deyil —
  istənilən sıra ilə işlədilə bilər.</p>
  <p class="meta">
    <span>Dərs 1 — 5 test</span>
    <span>Dərs 2 — 10 test</span>
    <span>Dərs 3 — 20 test</span>
    <span>Dərs 4 — 30 test</span>
    <span>CƏMİ %d test</span>
  </p>
</header>

<div class="izah">
  <p><b>⚠️ İşlətməzdən əvvəl — serveri qaldırın.</b> Testlərin çoxu canlı API-yə
  müraciət edir. Ayrı bir Terminal pəncərəsində bunu işlədin və açıq saxlayın:</p>
  <p style="margin-top:.6rem"><code>cd ~/Deepseek_ARTI/DS_Backend</code><br>
  <code>unset DATABASE_URL PGHOST</code><br>
  <code>PORT=4000 npm run start:prod</code></p>
  <p style="margin-top:.6rem"><b>İkinci qeyd:</b> hər skript öz girişini (token)
  özü alır — ona görə testlər bir-birindən asılı deyil. <b>Üçüncü qeyd:</b>
  <code>vaxt</code>, <code>gecikme_ms</code> kimi sahələr sizdə fərqli ola bilər;
  tutuşdurarkən əsas məzmuna baxın.</p>
</div>

<div class="mund">
  <h2>Mündəricat — hər testə birbaşa keçid</h2>
  %s
</div>

%s

<footer>
  ARTİ ERP · Yekun testlər · Dərs 1–4 · %d test<br>
  Bütün skriptlər real icra edilib — nəticələr həqiqi çıxışlardır.
</footer>

</div>
<script>%s</script>
</body>
</html>
""" % (CSS, cem, "".join(mund), "".join(govde), cem, JS)


def main() -> None:
    if "--icra" in sys.argv:
        print("İCRA EDİLİR (LAYIHE=%s, API=%s)" % (LAYIHE, API))
        kes = icra_et()
    else:
        kes = kesden()
        print("  ✓ keşdən oxundu (%d test)" % len(kes))
    CIXIS.write_text(qur(kes), encoding="utf-8")
    s = CIXIS.read_text(encoding="utf-8")
    print("✅ %s" % CIXIS.relative_to(KOK))
    print("   %d sətir · %d test" % (len(s.splitlines()),
                                     sum(len(d["testler"]) for d in DERSLER)))


if __name__ == "__main__":
    main()
