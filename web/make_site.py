#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Leo Kuroshita (@kurogedelic), Hügelton Instruments
"""Make the site (GitHub Pages):

  index.html                  redirect to the installer
  firmware/felucca-VER.fwsc   the package
  webapp/installer/index.html index_pkg.html with fm1pkg.js, fm1ota.js and the metadata inlined
  webapp/editor/index.html    editor.html (+ fukiai.ttf, FUKIAI-LICENSE.txt)
  webapp/editor/sloop-editor.html  the editor in one file, for offline use (SLOOP 2.6): its icon font inlined,
                              its links to the installer and the font licence online; opened from the disk in
                              Chrome / Edge (file:// is a secure context: Web MIDI asks for permission)
  webapp/sw.js, webapp/sloop.webmanifest, webapp/icon-*.png  the site without internet (SLOOP 2.6): an app to
                              install; opened once online, the installer, the editor and the firmware are kept
                              by the browser and work offline, still on https (on Android a downloaded file opens
                              as content://, where Chrome refuses Web MIDI)
  src/                        not touched

  web/make_site.py build/felucca-X.Y.fwsc X.Y OUT_DIR [--beta]
  (--beta: web/beta_banner.html at the top of the installer: the beta channel, docs/beta)

  web/make_site.py --pro X.Y OUT_DIR build/sloop-pro.fwsc [build/sloop-pro-elite.fwsc build/sloop-pro-mke.fwsc]
  SLOOP Pro (the SMK-37 build): webapp/installer/ from index_pro.html with one package per model (it installs the
  one for the connected keyboard), firmware/sloop-pro[-elite|-mke]-X.Y.fwsc, the same editor (SLOOP Pro Editor).

The package identity (FM-1_9xx) is read from the package; the device reports it
after the install.
"""
import base64
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ONLINE = "https://isod89.github.io/sloop-fm1/"                 # (the offline editor's links)
ONLINE_PRO = "https://isod89.github.io/sloop-pro/"             # SLOOP Pro's site


def offline_editor(html, online=None):
    """editor.html as one file for the disk: the icon font inlined, the download link out, the relative links online"""
    online = online or ONLINE
    font = base64.b64encode((HERE / "fukiai.ttf").read_bytes()).decode()
    for a, b in (('url("fukiai.ttf")', 'url(data:font/ttf;base64,' + font + ')'),
                 ('href="../installer/"', 'href="' + online + 'webapp/installer/" target="_blank" rel="noopener"'),
                 ('href="FUKIAI-LICENSE.txt"', 'href="' + online + 'webapp/editor/FUKIAI-LICENSE.txt" target="_blank" rel="noopener"')):
        if html.count(a) != 1:
            raise SystemExit(f"editor.html must contain {a} once; update make_site.py")
        html = html.replace(a, b)
    for pat, what in ((r"<!--DL-->.*?<!--/DL-->", "<!--DL-->...<!--/DL-->"),       # (the file has no site
                      (r"<!--PWA-->.*?<!--/PWA-->", "<!--PWA-->...<!--/PWA-->"),    # around it: no app to
                      (r"/\*PWA\*/.*?/\*/PWA\*/", "/*PWA*/.../*/PWA*/"),           # install, no copy kept)
                      (r'<button id="install"[^>]*></button>\s*', '<button id="install">')):
        html, n = re.subn(pat, "", html, flags=re.S)
        if n != 1:
            raise SystemExit(f"editor.html must contain {what} once; update make_site.py")
    return html


ICONS = ("icon-192.png", "icon-512.png", "icon-maskable-512.png")


def app_files(out, version, fw_name, name="SLOOP",
              description="SLOOP for the M-VAVE FM-1: the editor and the installer, also without internet"):
    """webapp/: the manifest, the icons and sw.js with the list of what it keeps (relative to webapp/) and a
    stamp of their contents, so any change makes a new sw.js and the browser takes the new site"""
    app = out / "webapp"
    for f in ICONS:
        shutil.copy(HERE / f, app / f)
    manifest = {
        "name": name, "short_name": name, "id": "editor/", "start_url": "editor/", "scope": "./",
        "display": "standalone", "background_color": "#000000", "theme_color": "#000000",
        "description": description,
        "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                  {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                  {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
    }
    (app / "sloop.webmanifest").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    keep = {"installer/": app / "installer" / "index.html", "editor/": app / "editor" / "index.html",
            "sloop.webmanifest": app / "sloop.webmanifest"}
    for f in ([fw_name] if isinstance(fw_name, str) else fw_name):
        keep["../firmware/" + f] = out / "firmware" / f
    for f in ("fukiai.ttf", "FUKIAI-LICENSE.txt"):
        if (app / "editor" / f).exists():
            keep["editor/" + f] = app / "editor" / f
    for f in ("preview.js", "preview-worklet.js", "sloop-preview.wasm"):
        if (app / "editor" / f).exists():
            keep["editor/" + f] = app / "editor" / f
    for f in ICONS:
        keep[f] = app / f
    h = hashlib.sha256()
    for k in sorted(keep):
        h.update(k.encode() + b"\0" + keep[k].read_bytes())
    sw = (HERE / "sw.js").read_text(encoding="utf-8")
    for mark in ("/*STAMP*/", "/*FILES*/[]"):
        if sw.count(mark) != 1:
            raise SystemExit(f"sw.js must contain {mark} once; update make_site.py")
    sw = sw.replace("/*STAMP*/", f"{version}-{h.hexdigest()[:12]}").replace("/*FILES*/[]", json.dumps(sorted(keep)))
    (app / "sw.js").write_text(sw, encoding="utf-8")
    return sorted(keep)
BLOCKS, BLK, KEEP = 20, 0x30, 0x2F


def strip_module(src):
    src = re.sub(r"^export\s+", "", src, flags=re.M)
    return re.sub(r"^import .*?;\n", "", src, flags=re.M)


def product_of(raw):
    """the package identity: one marker byte after each of the first 20 blocks (fm1pkg.js productOf)"""
    return "".join(chr((m - i - 1) & 0xFF) for i in range(BLOCKS) if (m := raw[i * BLK + KEEP]) != 0x7D)


def main(pkg, version, out):
    pkg, out = Path(pkg), Path(out)
    raw = pkg.read_bytes()
    product = product_of(raw)
    if not re.fullmatch(r"(FM-1|SMK-37 Pro|SMK-37 Elite|MKE-P37)_9\d\d", product):
        raise SystemExit(f"{pkg}: identity {product!r} is not a Felucca package (FM-1_9xx, SMK-37 Pro_9xx, SMK-37 Elite_9xx, MKE-P37_9xx)")
    if b"FELUCCA-LOADER-1" not in raw:              # marker of firmware/loader
        raise SystemExit(f"{pkg}: no Felucca update loader in it")
    html = (HERE / "index_pkg.html").read_text(encoding="utf-8")
    lib = strip_module((HERE / "fm1pkg.js").read_text(encoding="utf-8")) + "\n" + \
        strip_module((HERE / "fm1ota.js").read_text(encoding="utf-8"))
    name = f"sloop-{re.sub(r'[^A-Za-z0-9.-]', '-', version)}.fwsc"
    meta = json.dumps({"version": version, "product": product, "pkg": "../../firmware/" + name,
                       "sha256": hashlib.sha256(raw).hexdigest()})   # the page checks the download against it
    for mark in ("/*LIB*/", "/*META*/"):
        if html.count(mark) != 1:
            raise SystemExit(f"index_pkg.html must contain {mark} once; update make_site.py")
    html = html.replace("/*LIB*/", lib).replace("/*META*/", meta)
    logo = HERE.parent / "assets" / "logo" / "sloop-logo.svg"     # the SLOOP logo, inline
    html = html.replace("<!--LOGO-->", logo.read_text(encoding="utf-8") if logo.exists() else "<b>SLOOP</b>")
    inst, ed, fw = out / "webapp" / "installer", out / "webapp" / "editor", out / "firmware"
    for d in (inst, ed, fw):
        d.mkdir(parents=True, exist_ok=True)
    guide = HERE.parent / "output/pdf/Studio-0.3-guide-rapide-FR.pdf"
    guide_link = ""
    if guide.exists() and "--studio-guide" in sys.argv:   # LIVE: that guide describes the removed RYTHME tab
        shutil.copy(guide, out / guide.name)
        guide_link = '<p lang="fr"><a href="../../' + guide.name + '">Guide rapide illustré (PDF, 4 pages)</a></p>'
    html = html.replace("<!--STUDIO_GUIDE-->", guide_link)
    banner = ""
    if "--beta" in sys.argv:                       # the beta channel (docs/beta): what it is, what it implies
        notes = HERE / "beta_banner.html"
        banner = notes.read_text(encoding="utf-8") if notes.exists() else "<p><b>BETA</b></p>"
    html = html.replace("<!--BANNER-->", banner)
    for old in list(fw.glob("felucca-*.fwsc")) + list(fw.glob("sloop-*.fwsc")):   # one package: the current one
        old.unlink()
    shutil.copy(pkg, fw / name)
    ed_html = (HERE / "editor.html").read_text(encoding="utf-8")
    dl = f'download="sloop-editor-{re.sub(r"[^A-Za-z0-9.-]", "-", version)}.html"'
    if ed_html.count('download="sloop-editor.html"') != 1 or html.count('download="sloop-editor.html"') != 1:
        raise SystemExit('editor.html and index_pkg.html must link download="sloop-editor.html" once; update make_site.py')
    (ed / "index.html").write_text(ed_html.replace('download="sloop-editor.html"', dl), encoding="utf-8")
    (ed / "sloop-editor.html").write_text(offline_editor(ed_html), encoding="utf-8")
    (inst / "index.html").write_text(html.replace('download="sloop-editor.html"', dl), encoding="utf-8")
    for f in ("fukiai.ttf", "FUKIAI-LICENSE.txt"):
        if (HERE / f).exists():
            shutil.copy(HERE / f, ed / f)
    # Optional browser DSP, built separately without the hardware toolchain.
    for f in ("preview.js", "preview-worklet.js"):
        shutil.copy(HERE / f, ed / f)
    dsp = HERE.parent / "build" / "preview" / "sloop-preview.wasm"
    if dsp.exists():
        shutil.copy(dsp, ed / dsp.name)
    elif (ed / dsp.name).exists():
        (ed / dsp.name).unlink()  # never serve an old audio build as the current one
    app_files(out, version, name)
    (out / "index.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>SLOOP</title>'
        '<meta http-equiv="refresh" content="0; url=webapp/installer/">'
        '<a href="webapp/installer/">SLOOP installer</a>\n', encoding="utf-8")
    print(f"site: {out}: webapp/installer ({len(html)} B), webapp/editor, firmware/{name} ({len(raw)} B, {product})")


PRO_MODELS = (("SMK-37 Pro", ""), ("SMK-37 Elite", "-elite"), ("MKE-P37", "-mke"))   # SLOOP Pro: model -> file suffix


def editor_files(ed, version, title=None, online=None):
    """webapp/editor/: the editor, its offline copy, the icon font and the optional audio preview"""
    ed_html = (HERE / "editor.html").read_text(encoding="utf-8")
    if title:
        if ed_html.count("<title>SLOOP Editor</title>") != 1:
            raise SystemExit("editor.html must contain <title>SLOOP Editor</title> once; update make_site.py")
        ed_html = ed_html.replace("<title>SLOOP Editor</title>", f"<title>{title}</title>")
    dl = f'download="sloop-editor-{re.sub(r"[^A-Za-z0-9.-]", "-", version)}.html"'
    if ed_html.count('download="sloop-editor.html"') != 1:
        raise SystemExit('editor.html must link download="sloop-editor.html" once; update make_site.py')
    (ed / "index.html").write_text(ed_html.replace('download="sloop-editor.html"', dl), encoding="utf-8")
    (ed / "sloop-editor.html").write_text(offline_editor(ed_html, online), encoding="utf-8")
    for f in ("fukiai.ttf", "FUKIAI-LICENSE.txt"):
        if (HERE / f).exists():
            shutil.copy(HERE / f, ed / f)
    for f in ("preview.js", "preview-worklet.js"):
        shutil.copy(HERE / f, ed / f)
    dsp = HERE.parent / "build" / "preview" / "sloop-preview.wasm"
    if dsp.exists():
        shutil.copy(dsp, ed / dsp.name)
    elif (ed / dsp.name).exists():
        (ed / dsp.name).unlink()  # never serve an old audio build as the current one
    return dl


def main_pro(version, out, pkgs):
    """SLOOP Pro's site: one package per SMK-37 model; the installer picks the one for the connected keyboard"""
    out = Path(out)
    vtag = re.sub(r"[^A-Za-z0-9.-]", "-", version)
    entries, names, raws = [], [], {}
    for pkg in map(Path, pkgs):
        raw = pkg.read_bytes()
        product = product_of(raw)
        m = re.fullmatch(r"(SMK-37 Pro|SMK-37 Elite|MKE-P37)_9\d\d", product)
        if not m:
            raise SystemExit(f"{pkg}: identity {product!r} is not a SLOOP Pro package (SMK-37 Pro / SMK-37 Elite / MKE-P37_9xx)")
        if b"FELUCCA-LOADER-1" not in raw:
            raise SystemExit(f"{pkg}: no Felucca update loader in it")
        if m[1] in raws:
            raise SystemExit(f"{pkg}: a second package for {m[1]}")
        raws[m[1]] = (product, raw)
    if "SMK-37 Pro" not in raws:
        raise SystemExit("--pro: the SMK-37 Pro package is needed (it also serves the Starrykey 37 Play)")
    inst, ed, fw = out / "webapp" / "installer", out / "webapp" / "editor", out / "firmware"
    for d in (inst, ed, fw):
        d.mkdir(parents=True, exist_ok=True)
    for old in list(fw.glob("felucca-*.fwsc")) + list(fw.glob("sloop-*.fwsc")):   # the current packages only
        old.unlink()
    for model, sfx in PRO_MODELS:
        if model not in raws:
            continue
        product, raw = raws[model]
        name = f"sloop-pro{sfx}-{vtag}.fwsc"
        (fw / name).write_bytes(raw)
        names.append(name)
        entries.append({"product": product, "pkg": "../../firmware/" + name, "sha256": hashlib.sha256(raw).hexdigest()})
    html = (HERE / "index_pro.html").read_text(encoding="utf-8")
    lib = strip_module((HERE / "fm1pkg.js").read_text(encoding="utf-8")) + "\n" + \
        strip_module((HERE / "fm1ota.js").read_text(encoding="utf-8"))
    for mark in ("/*LIB*/", "/*META*/"):
        if html.count(mark) != 1:
            raise SystemExit(f"index_pro.html must contain {mark} once; update make_site.py")
    html = html.replace("/*LIB*/", lib).replace("/*META*/", json.dumps({"version": version, "pkgs": entries}))
    logo = HERE.parent / "assets" / "logo" / "sloop-logo.svg"
    html = html.replace("<!--LOGO-->", logo.read_text(encoding="utf-8") if logo.exists() else "<b>SLOOP</b>")
    banner = ""
    if "--beta" in sys.argv:
        notes = HERE / "beta_banner.html"
        banner = notes.read_text(encoding="utf-8") if notes.exists() else "<p><b>BETA</b></p>"
    html = html.replace("<!--BANNER-->", banner)
    dl = editor_files(ed, version, "SLOOP Pro Editor", ONLINE_PRO)
    if html.count('download="sloop-editor.html"') != 1:
        raise SystemExit('index_pro.html must link download="sloop-editor.html" once; update make_site.py')
    (inst / "index.html").write_text(html.replace('download="sloop-editor.html"', dl), encoding="utf-8")
    app_files(out, version, names, "SLOOP Pro",
              "SLOOP Pro for the M-VAVE SMK-37: the editor and the installer, also without internet")
    (out / "index.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>SLOOP Pro</title>'
        '<meta http-equiv="refresh" content="0; url=webapp/installer/">'
        '<a href="webapp/installer/">SLOOP Pro installer</a>\n', encoding="utf-8")
    print(f"site: {out}: webapp/installer ({len(html)} B), webapp/editor, firmware/" + ", ".join(
        f"{n} ({e['product']})" for n, e in zip(names, entries)))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--pro":
        args = [a for a in sys.argv[2:] if a != "--beta"]
        if len(args) < 3:
            sys.exit(__doc__)
        main_pro(args[0], args[1], args[2:])
        sys.exit(0)
    args = [a for a in sys.argv[1:] if a not in ("--studio-guide", "--beta")]
    if len(args) != 3:
        sys.exit(__doc__)
    main(*args)
