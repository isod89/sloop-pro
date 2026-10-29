<p align="center"><img src="assets/logo/sloop-logo.png" alt="SLOOP" width="420"></p>

<p align="center"><b>SLOOP Pro — the SLOOP groovebox on the M-VAVE SMK-37.</b><br>
Free and open source (GPL-3.0). SLOOP by isod89, based on <a href="https://github.com/hugelton/Felucca">Felucca</a> by
Leo Kuroshita / Hügelton Instruments; the SMK-37 board layer by <a href="https://github.com/genkigenki/fm1-to-smk37">genkigenki</a>.
Everyone who made it possible: <a href="CREDITS.md">CREDITS.md</a>.</p>

<p align="center">
<a href="SLOOP-PRO.md"><b>SLOOP Pro: controls, menu, install</b></a> ·
<a href="DEMARRAGE-RAPIDE-PRO-FR.md">Démarrage rapide (français)</a> ·
<a href="TEST-SLOOP-PRO.md">Essais sur le SMK-37</a> ·
<a href="GUIDE.md">The SLOOP guide</a> ·
<a href="BUILDING.md">Building</a> ·
<a href="../../releases">Releases</a> ·
<a href="../../issues">Report a bug</a>
</p>

---

SLOOP turns the keyboard into a four-track groovebox you play live: **three synths and a drum machine**, twelve
synthesis engines, 153 sounds, 37 drum kits, your own samples, a song mode you play with your hands, 27 punch-in
effects, a piano-roll note editor, parameter locks, micro timing and fills. **SLOOP Pro** is that firmware on the
M-VAVE SMK-37 — with what the bigger keyboard brings:

| | |
|---|---|
| **37 velocity keys** | the 27 middle keys as SLOOP's, velocity from your unit's factory curves (KEY VELOCITY: dynamic, soft, hard, fixed); the outer 10 play notes, or drums on the drum track |
| **16 RGB pads** | the drum kit (default), the selected track's sound (NOTES) or its 16 steps, in the screen's track colours; the sound picker (turn K4); piano, mix and song tiles in the layers; PAD LIGHTS brightness |
| **4 faders, 5 banks** | A level, B filter, C reverb, D delay of the four tracks, E the selected synth track's envelope (ADSR) |
| **8 knobs** | MASTER, SELECT, track, sound, and the four dials, as on screen (or the SMK layout) |
| **Wheels and pedal** | pitch bend (BEND UP / DOWN), vibrato, a sustain pedal on the PEDAL jack |
| **MIDI** | USB MIDI and the TRS MIDI OUT jack (nothing left hanging when it is turned off), a full **DAW mode** with your own CC map |
| **Models** | SMK-37 Pro (and Starrykey 37 Play), SMK-37 Elite, MKE-P37: one package each, the installer picks the right one |

> **Status:** SLOOP Pro 2.8.4, a beta built on SLOOP 2.8.4 (fixes: no more distortion at the end of notes, 3.5 mm and USB; UNISON no longer stacks its voices in phase; PHYS strings in tune; NZ ARCADE, SAMPLE and GRAIN follow the top keys; a firm press on a layer button opens its pages; on REC READY a knob changes only its own value; the faders follow a real volume curve; the sustain pedal held as long as you like; no hanging note on TRS MIDI OUT; the lights no longer freeze after 25 days; the installer no longer freezes Chrome on Windows; the way back to the official firmware with V16). Install at your own risk (read the
> [safety notes](SLOOP-PRO.md#safety)); your unit's calibration is never written, and M-VAVE's own updater takes you
> back at any time.

## Install

1. Back up the keyboard's flash once (see [Safety](SLOOP-PRO.md#safety)).
2. Open the installer: **[isod89.github.io/sloop-pro](https://isod89.github.io/sloop-pro/)** in Chrome or Edge,
   nothing to build. (Or build it yourself on Windows: `INSTALL-SLOOP-PRO.bat` builds the three packages in WSL and
   opens the same installer from your computer.) The keyboard must run M-VAVE's V016 first: update an older one
   with M-VAVE's own updater.
3. Connect the SMK-37 straight to the computer (a USB data cable), close other MIDI apps, tick the box, press
   **Install SLOOP Pro**. The page reads the model and writes its package, then checks the keyboard after the restart.

The command line does the same: `python3 tools/fm1_install.py build/release/`. Details, the way back to the M-VAVE
firmware and what to do if something goes wrong: [SLOOP-PRO.md](SLOOP-PRO.md).

## Editor

The SLOOP web editor works with SLOOP Pro: sounds, sequences and the piano roll, the drum kits and samples, songs,
backups, and the SMK-37's **DAW MAP** tab. `OPEN-EDITOR-PRO.bat` opens it (after a build), or use the installer
page's link.

## For FM-1 owners

This repository still builds SLOOP for the FM-1 (`./build.sh`, as SLOOP 2.8.4). The FM-1
firmware and its installer live at [isod89/sloop-fm1](https://github.com/isod89/sloop-fm1); its README is kept here
as [README-SLOOP.md](README-SLOOP.md).

## Credits

SLOOP Pro stands on the open work of many people; [CREDITS.md](CREDITS.md) names each of them and what they did.

- **Felucca**: Leo Kuroshita ([@kurogedelic](https://github.com/kurogedelic)), Hügelton Instruments, the open FM-1
  firmware SLOOP is built on.
- **SLOOP**: isod89 and contributors ([README-SLOOP.md](README-SLOOP.md#credits-and-thanks)).
- **The SMK-37 port**: M. Geisler ([@genkigenki](https://github.com/genkigenki)):
  [fm1-to-smk37](https://github.com/genkigenki/fm1-to-smk37), the board layer, the SMK-37 features, the reference
  SLOOP port and the update library of the web installer.
- **[@ChanceTheMaker](https://github.com/ChanceTheMaker)**, [sloop-smk](https://github.com/ChanceTheMaker/sloop-smk):
  the ideas behind the pedal, the pad brightness, the envelope fader bank, the TRS note-off flush, honest save
  results and the installer's disposable MIDI session.
- **The second core**: [@andrerezemini](https://github.com/andrerezemini) (sloop-lab),
  [Charles Vestal](https://github.com/charlesvestal) (X0X), [@keremimo](https://github.com/keremimo) (Melodee).
- **And**: [@renebohne](https://github.com/renebohne), [@juanjiant-bit](https://github.com/juanjiant-bit) (JIANT FM),
  [@ordenador](https://github.com/ordenador), [AL-255](https://github.com/AL-255/FM-1-RE) (FM-1-RE),
  [kagaimiq](https://github.com/kagaimiq) (JieLi tools), and the Felucca and SLOOP communities.

M-VAVE, SMK-37, MKE-P37, Starrykey and FM-1 are trademarks of their respective owners; SLOOP Pro is not affiliated
with them. Licence: GPL-3.0 ([LICENSE](LICENSE), [LICENSING.md](LICENSING.md)).
