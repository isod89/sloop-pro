# SLOOP Pro: credits

SLOOP Pro is SLOOP on the M-VAVE SMK-37. It exists because many people shared their code, their research and their
time in the open. This page names everyone whose work is in it, what they did, and where to find it. Every part is
GPL-3.0-only unless the table at the end says otherwise ([LICENSING.md](LICENSING.md)).

## SLOOP Pro

- **isod89 (Sodwave)**, [isod89/sloop-pro](https://github.com/isod89/sloop-pro): SLOOP Pro, the port of SLOOP 2.8.1
  to the SMK-37, its installer page and its tests. The sustain pedal, PAD LIGHTS, FADER BANK E (envelope), the NOTES
  pad mode, the TRS note-off flush and honest save results were built on the ideas credited below.

## The foundations

- **Leo Kuroshita (@kurogedelic), Hügelton Instruments**, [Felucca](https://github.com/hugelton/Felucca): the open
  firmware for the FM-1 that SLOOP and SLOOP Pro are built on. Most of the code carries his copyright line. The
  engines, the sequencer, the web editor, the M-UPGRADE-compatible installer and update loader, the HAL, the FM6
  engine, the INSERT effects, LFO 2, the ANALOG filters, MIDI LEARN, the arpeggiator modes, and much more.
- **isod89 and the SLOOP contributors**, [isod89/sloop-fm1](https://github.com/isod89/sloop-fm1): SLOOP, the FM-1
  firmware that SLOOP Pro takes whole (2.8.1). Everyone credited in SLOOP is credited here too:
  [README-SLOOP.md, Credits and thanks](README-SLOOP.md#credits-and-thanks).

## The SMK-37 port

- **M. Geisler (genkigenki / makkuro)**, [fm1-to-smk37](https://github.com/genkigenki/fm1-to-smk37),
  [genkigenki/sloop-fm1](https://github.com/genkigenki/sloop-fm1) (Snoop37) and
  [genkigenki.github.io/smk37](https://genkigenki.github.io/smk37/). This is the work SLOOP Pro stands on. His
  commits are part of this repository's history, under his name.
  - The SMK-37 board layer: keys and velocity curves, the 16 RGB pads, faders, wheels, encoders, LEDs, the PEDAL
    and battery inputs, and the hardware calibration (`firmware/hal/smk_input.h` and the `smk_*` files).
  - The SMK-37's features: DAW mode and its map, the pad sound picker, the FADER BANK screen, KEY VELOCITY,
    TRS MIDI OUT, BEND UP / DOWN, KNOB LAYOUT, LIMITER SOFT / CLASSIC, and the DRUM KIT and STEPS pad modes.
  - The SMK-37 Elite and MKE-P37 builds, and the Starrykey 37 Play.
  - The way back to the M-VAVE firmware, and the package checks that refuse another board's firmware.
  - The reverse engineering and the documentation of the SMK-37: flash map, update protocol, package format and
    pitfalls.
  - The update library of SLOOP Pro's web installer (`web/fm1ota.js`): the version of his SMK-37 site that installs
    from Chrome on Windows.
- **ChanceTheMaker**, [sloop-smk](https://github.com/ChanceTheMaker/sloop-smk): the other SLOOP port to the SMK-37.
  SLOOP Pro rebuilt several of its ideas in its own code:
  - the measured levels of the sustain pedal;
  - pad brightness (PAD LIGHTS);
  - an envelope on the faders;
  - a flush so no MIDI note hangs on the TRS output;
  - reporting a save the flash did not take.

  His work on Windows USB installs and on the MIDI session also helped find why the first browser installs stalled.
  In SLOOP itself: the TRS MIDI input fix (Felucca Salt) and work on the MIDI clock.

## In the firmware SLOOP Pro runs (through SLOOP)

- **Andre Rezemini (andrerezemini)**, [sloop-lab](https://github.com/andrerezemini/sloop-lab): the sound on the
  second core, and 38 KB of RAM back (`firmware/src/cpu1.c`, SLOOP 2.7).
- **Charles Vestal**, [X0X](https://github.com/charlesvestal/fm1-x0x): the dual-core start and its HAL
  (`firmware/hal/fm1_cpu1.h`), and the supply levels for two cores.
- **keremimo**, [Melodee](https://github.com/keremimo/melodee): the dual-core start, with X0X; the TRS
  MIDI input fix and work on the MIDI clock, with ChanceTheMaker.
- **renebohne**: the played-note key lights, MIDI Program Change, and the CC 74 map that SLOOP 2.7
  follows.
- **juanjiant-bit**, [JIANT FM](https://github.com/juanjiant-bit/JIANT): the progressive knob acceleration and the
  LEVEL / PAN glide.
- **Mario Faúndez Vidal (@ordenador)**: the web editor's audio preview, the firmware's engines in the browser
  (WebAssembly). His commit is part of this history.
- **The Felucca and SLOOP communities**: the people who asked for, tested and reported the features listed in
  [README-SLOOP.md](README-SLOOP.md#credits-and-thanks).

## Research and tools

- **AL-255**, [FM-1-RE](https://github.com/AL-255/FM-1-RE): the FM-1's reverse engineering, which the SMK-37 work
  extends.
- **kagaimiq**, [jl-uboot-tool](https://github.com/kagaimiq/jl-uboot-tool) and the JieLi research: the full flash
  backup and the chip's recovery mode.
- **JieLi**, the [AC79 SDK](https://gitee.com/Jieli-Tech/fw-AC79_AIoT_SDK) (Apache-2.0): the build reads three of its
  files from your own checkout. None of them is in this repository.

## Sounds, fonts and libraries

These are listed with their licences in [LICENSING.md](LICENSING.md):

- **Samples:** Versilian Studios VSCO-2 CE and VCSL, and Sonic Pi, all CC0.
- **Fonts:** Terminus (SIL OFL 1.1) and the Fukiai icon font (MIT, Hügelton Instruments).
- **Engines:** CrispyZebra (the PHASE engine); klattsch by Tony Gies (the reference for the VOICE engine); msfa
  from Dexed by Google Inc. and Pascal Gauthier (FM6, Apache-2.0); DaisySP and Rings by Electrosmith and
  Emilie Gillet (PHYS, MIT).

## Testing

- Everyone who installs SLOOP Pro on an SMK-37 Pro, Elite, MKE-P37 or Starrykey 37 Play and reports back. Please do,
  in the [issues](https://github.com/isod89/sloop-pro/issues).

If your work is in SLOOP Pro and missing here, or credited wrongly, please open an issue: it will be fixed.

M-VAVE, SMK-37, MKE-P37, Starrykey and FM-1 are trademarks of their respective owners. SLOOP Pro is independent and
is not affiliated with them.
