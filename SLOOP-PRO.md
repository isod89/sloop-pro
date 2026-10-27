# SLOOP Pro: SLOOP on the M-Vave SMK-37

The M-Vave SMK-37 has the FM-1's chip (JieLi AC791N), so SLOOP runs on it as a target board: `BOARD=smk37`. That
build is **SLOOP Pro**: SLOOP 2.8.3 with the SMK-37's 37 velocity keys, 16 RGB pads, 4 faders, 8 knobs, wheels,
pedal and TRS MIDI out. Everything SMK-37-specific sits behind `BOARD_SMK37`; the FM-1 build is SLOOP, unchanged,
byte for byte.

> Unofficial firmware for the SMK-37, not affiliated with or endorsed by M-Vave. No warranty: install at your own
> risk and read [Safety](#safety) first.

The SMK-37 board layer is genkigenki's ([fm1-to-smk37](https://github.com/genkigenki/fm1-to-smk37), the reference
port on SLOOP 2.6 / 2.7); a few SLOOP Pro additions follow ChanceTheMaker's
[sloop-smk](https://github.com/ChanceTheMaker/sloop-smk) (the pedal, pad brightness, the envelope fader bank, no
hanging TRS notes, a save that never claims to be one when the flash failed).

## What SLOOP Pro adds to the SMK-37 layer

| | |
|---|---|
| SLOOP 2.8.3 | the kick no longer cut on a busy beat (a drum hit takes a free voice first, the kick last); the hold pages no longer flash on a quick tap; a free take keeps a held note under the ones played over it; a chopped sample played again starts from silence with its ATK (no click); the second core hardened (a USB backup no longer crashes it; if core 1 fails, one core goes on) |
| SLOOP 2.8.2 | hold a note under others: on a POLY track a held note keeps sounding while you record over it, goes on through the notes already there when you overdub, and SEQ > NOTES LEN runs on under later notes (a long bass under a melody); MONO: SET VOICE POLY when a key is played over a held one on a mono sound; no note left stuck when MIDI comes in too fast |
| SLOOP 2.8.1 | the NOTES piano roll and the per-step sheets (OCT+ held), FILTER RESO, STEP ADVANCE, DRUM PREVIEW, the punch-in fade (FX held + SELECT), MIDI Bank Select |
| Sustain pedal | the PEDAL jack: a footswitch of either polarity (the reading at power-on is "up": plug it in before switching on); the selected synth track sustains, CC 64 goes out over USB and TRS |
| The pads | a pad hit flashes white for 80 ms, whatever it shows; triggered as a drum module's: a threshold (HOME menu > PADS > PAD THRESHOLD: LOW, MID, HIGH, MAX; PADS > PAD SCOPE shows what a pad measures), the velocity at the peak of the hit, a 40 ms mask after each note and a retrigger cancel that follows the pad's decay: one tap is one note, also a soft one whose finger stays on the pad; rolls up to 16 hits a second |
| PAD LIGHTS | HOME menu > PADS > PAD LIGHTS (K6): HIGH (default), MID, LOW; each change lights the 16 pads in the tracks' colours for 1.5 s (a test of every pad) |
| FADER BANK E | ENV: faders 1–4 set the selected synth track's ATTACK, DECAY, SUSTAIN, RELEASE |
| TRS MIDI OUT | turned OFF (or a note-off lost to a full buffer): a note-off for every note still on, then sustain off and all notes off — nothing hangs on the other synth |
| Saving | a section the flash did not take shows NOT SAVED: FLASH ERROR and keeps what was saved before; the editor says so too |
| Installer | one page for the three models: it reads the keyboard's model and writes its package; a keyboard left in update mode is finished and checked; an FM-1 and ChanceTheMaker's firmwares are refused before anything is sent |

## Models

| Model | Build | Package identity |
|---|---|---|
| SMK-37 Pro | `BOARD=smk37 ./build.sh` | `SMK-37 Pro_900` (`build/sloop-pro.fwsc`) |
| SMK-37 Elite | `BOARD=smk37 MODEL=elite ./build.sh` | `SMK-37 Elite_900` (`build/sloop-pro-elite.fwsc`) |
| MKE-P37 | `BOARD=smk37 MODEL=mke ./build.sh` | `MKE-P37_900` (`build/sloop-pro-mke.fwsc`) |
| Starrykey 37 Play | the SMK-37 Pro build | `SMK-37 Pro_900` |

They are one keyboard under several names. The `MODEL` builds differ only in the name the keyboard reports
(its identity, its update loader's, the update record's), so M-Vave's updater still recognises the unit for the way
back to the stock firmware. A release build: `--release X.Y` (identity `SMK-37 Pro_9XY`). All three at once:
`tools/build_pro.sh` (Linux / WSL) or `INSTALL-SLOOP-PRO.bat` (Windows). See [BUILDING.md](BUILDING.md) for the
toolchain.

## Install

Connect the keyboard straight to the computer over USB (a data cable), close other apps that use MIDI, then:

- **Windows:** `INSTALL-SLOOP-PRO.bat` builds the three packages in WSL and opens the installer page
  (<http://localhost:8767/webapp/installer/>, Chrome or Edge). `OPEN-EDITOR-PRO.bat` opens the editor later.
- **The installer page** (`web/index_pro.html`, built by `web/make_site.py --pro`): it reads the keyboard's model
  and writes that model's package (or the one you tick), checks each package's SHA-256 first, and checks the
  identity after the restart.
- **The command line:**

  ```sh
  python3 tools/fm1_install.py build/release/          # the three packages: the one for this keyboard
  python3 tools/fm1_install.py build/sloop-pro-elite.fwsc   # or one package (Python 3, mido, python-rtmidi)
  ```

Either way: the running firmware (the stock one or SLOOP Pro) starts the update loader and the package is written;
then the keyboard restarts and the installed identity is checked. A write cut off (cable, power) resumes when you
install again: the keyboard stays in update mode until it is finished. Updating later works the same way; projects,
presets, samples and settings are kept. A package never goes to the other device (FM-1 / SMK-37).

**From ChanceTheMaker's Sloop SMK** (or Felucca SMK, Melodee SMK, Doom: the keyboard reports `SMK-37_9xx`): those
firmwares take only their own packages, so go back to the M-Vave firmware first (their restore page, or M-UPGRADE),
then install SLOOP Pro. Back up your projects there first: their data is not SLOOP Pro's, and SLOOP Pro clears
another firmware's store at its first start.

**Your samples:** four slots, USR1 to USR4, as on the FM-1 (SAMPLE, GRAIN, the drum kits, KIT USR3+4). The SMK-37 has
half the FM-1's free flash for them, 40 KiB a slot: the web editor stores a slot at 22050 Hz when its sounds fit
(about 3.6 s) and at 11025 Hz when they do not, so a slot still holds about 7 s, as on the FM-1 (the editor says
"11 kHz" when it did). SLOOP Pro 2.8.1 had two 80 KiB slots (USR3 and USR4 refused samples): after the update, send
your samples again from your WAV files.

**Back to the stock firmware:** install the official package for your model with M-Vave's own updater (M-UPGRADE),
or give it to the installer: `python3 tools/fm1_install.py --force SMK-37_Pro_016.fwsc` (the installer reads the
stock package format). The SLOOP build keeps the stock update protocol, so the stock tools see the keyboard as usual.
The user sample slots USR1 to USR4 (0xC2000–0xE9FFF) are where the stock firmware keeps its key, knob and fader
mapping; it trusts that area while its end marker `usrdata` (0xEAFF8) is there. SLOOP erases the marker's sector
(0xEA000, the only sector it may touch there) before it first stores a sample in USRFLASH, and at power-on when the
marker sits over sample data, so the stock firmware rebuilds its factory mapping; an untouched stock mapping (with
your MIDI Suite presets) stays as it is. The web editor's Settings tab has **Prepare the return to M-Vave** to erase
the marker on request.

**If it does not start:** after two failed starts SLOOP Pro opens its USB recovery screen (SLOOP PRO USB RESCUE) (identity `SMK-37 Pro_000`,
or the model's), where the installer can write a package again; after a third it drops into the chip's mask-ROM
update mode (UBOOT).

## Knobs, faders, wheels

| FM-1 printed | SLOOP function | SMK-37 printed | on the SMK-37 |
|---|---|---|---|
| MASTER (pot, top left) | output volume | K1 | master volume (virtual pot, 24 steps a click; its curve: HOME menu > AUDIO > LIMITER) |
| SELECT (big encoder) | tempo (TRACKS), page ◀▶, visualiser style, menu section | K2 | SELECT: tempo / pages |
| ALGORITHM | select track 1–4 | K3 | track |
| PRESETS | sound (synth) / kit (drums) | K4 | sound / kit, the pad picker shows them |
| KNOB 1 | dial 1 on screen (blue) | K5 | dial 1 |
| KNOB 2 | dial 2 on screen (green) | K6 | dial 2 |
| KNOB 3 | dial 3 on screen (yellow) | K7 | dial 3 |
| KNOB 4 | dial 4 on screen (orange) | K8 | dial 4 |
| — | — | KNOB LAYOUT = SMK | HOME menu > SCREEN > KNOB LAYOUT (K7): K1–K4 the dials 1–4, K5 master volume, K6 SELECT, K7 PRESETS, K8 ALGORITHM (track); FM-1 (default) as above |
| — | — | FADER 1–4 | tracks 1–4 (4 = drums), by FADER BANK: A level, B filter (low-pass ◀ open ▶ high-pass), C reverb, D delay; E ENV: the selected synth track's ATTACK, DECAY, SUSTAIN, RELEASE; a fader takes over once moved |
| — (no wheels used by SLOOP) | — | PITCH wheel | pitch bend, selected synth track: HOME menu > PLAY > BEND UP (K6) / BEND DOWN (K7), OFF, 1, 2, 3, 4, 5, 7, 12 semitones each; default 7 / 7 |
| — | — | MOD wheel | vibrato 10 Hz, up to ±1 semitone (up = more) |
| — | — | PEDAL jack | sustain (a footswitch, either polarity: plugged in before power-on), the selected synth track; CC 64 out over USB and TRS (DAW mode: on CHANNEL) |

## Buttons

| FM-1 printed | SLOOP tap | SLOOP hold (layer) | SMK-37 printed | on the SMK-37 |
|---|---|---|---|---|
| PLAY | start / stop (LED flashes on every beat) | — | SEQ PLAY | PLAY |
| REC | record / arm | 2 s: clear track | SEQ REC | REC |
| HOME | TRACKS screen, again: visualiser | menu | PATCH | HOME |
| ENV | envelope pages (amp/filter shape) | — | CHORD | ENV |
| LFO | LFO pages (modulation) | — | NOTE REPEAT | LFO |
| FX | effect pages | punch-in FX on pads | FX | FX |
| SEL | key / chord pages | key layer (pads = piano: scale green, root brighter) | SCALE | SEL |
| EDIT | sound pages, drum kit | erase layer | PARA | EDIT |
| ARP | arp pages (MODE on K5: OFF switches the arpeggiator off) | note repeat (rolls) | ARP | ARP; LED lit while the selected track's arpeggiator runs |
| SEQ | step / pattern pages | step layer (steps 1–16) | SEQ | SEQ |
| GLO | global / master / system | mix layer (mute, solo, fill, tap) | GLOBE | GLO |
| SAVE | song screen / save | song layer (slots A–D: used green, free white) | BT | SAVE (SLOOP has no Bluetooth) |
| OCT− | octave down | drums: ghost hits | OCTAVE− | OCT− |
| OCT+ | octave up | drums: hard hits | OCTAVE+ | OCT+ |
| — | — | — | KNOB BANK | pins the pad sound picker open / closes it (lit while pinned or while K4 turns) |
| — | — | — | FADER BANK | the fader bank screen; pressed again, < > or SELECT: the next bank A→B→C→D→E (closes after 4 s; lit while up; closes the pad picker) |
| — | — | — | KNOB BANK + FADER BANK | the pads on the PLAY screen: DRUM KIT (default) → NOTES → STEPS (as the stock PAD BANK combo) |
| — | — | — | < | page back (as SELECT, never tempo); SEQ held or pads on STEPS: step page back; visualiser: style |
| — | — | — | > | page forward; SEQ held or pads on STEPS: step page forward; visualiser: style |
| — | — | — | < + > | SYNTH ↔ DAW mode ([DAW mode](#daw-mode)) |

## Keys and pads

| FM-1 | SLOOP | SMK-37 | on the SMK-37 |
|---|---|---|---|
| 27 keys F3–G5 | notes; in layers: tiles (steps, FX, mix…) | keys F3–G5 (middle 27) | same, with velocity |
| — | — | keys C3–E3 (lowest 5) | synth tracks: notes; drum track: C3 kick, D3 snare, E3 hat (black keys = left white key) |
| — | — | keys G#5–C6 (highest 5) | synth tracks: notes; drum track: G#5 cowbell, A5 open hat, B5 crash, C6 ride |
| LEDs under 27 keys | what is on / playing | 16 RGB pads | PLAY screen: DRUM KIT (default; a pad a drum sound whatever track is selected, velocity, recorded into the drum track while recording; orange, dim / bright while it sounds) or NOTES (KNOB BANK + FADER BANK once: the selected track's sound on the 16 white keys F3–G5, bottom row F3–C4, top row D4–G5, with velocity, as the keys: recorded into that track, QNT WHITE walks its scale; its colour, bright while a note sounds, the root's pads half, a silent pad dark) or STEPS (KNOB BANK + FADER BANK again; the selected track's 16 steps of the page, top row 1–8: empty dim white, set in the track's colour, playhead white; tap sets / clears; drums: the sound last played). Layers: SEQ / FX / GLO / SAVE tiles, SCALE piano, EDIT / ARP held the white keys |

## Velocity

HOME menu (PATCH held) > PLAY > **KEY VELOCITY**, on K5 (before: MIDI, K8), sets how the 37 keys and the pads play. It applies to the
notes, their MIDI out and the drum levels; OCT− / OCT+ held still play ghost / hard drums. Kept with the settings.

| KEY VELOCITY | the notes play |
|---|---|
| DYNAMIC (default) | as played (the unit's factory velocity curves) |
| SOFT | louder for a light touch (32 → 56, 64 → 96) |
| HARD | loud needs a hard hit (64 → 32, 100 → 78) |
| FIXED 64 | always 64 (drums: soft) |
| FIXED 100 | always 100, as the FM-1's keys (drums: normal) |
| FIXED 127 | always 127 (drums: hard) |

## HOME menu: the SMK-37 settings

HOME menu (PATCH held; sections SCREEN, LIGHTS, AUDIO, USB, SEQ, PLAY, MIDI, DAW, SYSTEM: four rows at most, one a
knob); SELECT walks the sections, the knobs set the rows (K5–K8, or K1–K4 with KNOB LAYOUT = SMK; the screen names
them), OCT+ steps the row under the cursor; SEQ PLAY and SEQ REC still start / stop and arm:

| Section | Row | Knob | Setting |
|---|---|---|---|
| SCREEN | COLOR, ZOOM | K5, K6 | as SLOOP's |
| SCREEN | KNOB LAYOUT | K7 | FM-1 (default): K1 MASTER, K2 SELECT, K3 ALGORITHM, K4 PRESETS, K5–K8 the dials. SMK: K1–K4 the dials, K5 MASTER, K6 SELECT, K7 PRESETS, K8 ALGORITHM. The knobs are endless: the new layout works at once. Switched to SMK, the menu's rows move to K1–K4 (K3 switches back) |
| LIGHTS | LIGHTS, NOTES | K5, K6 | as SLOOP's (the button lights; the FM-1's KEYS lights are left out: the SMK-37's keys have none) |
| PADS | PAD THRESHOLD | K5 | how firm a tap starts a note: LOW, MID (default), HIGH, MAX (kept in the FM-1's KEYS setting, shared with Clipper Pro). Raise it if a light touch sounds when it should not; lower it if soft taps are missed |
| PADS | PAD LIGHTS | K6 | the pads' brightness: HIGH (default), MID, LOW; each change shows on the 16 pads for 1.5 s |
| PADS | PAD SCOPE | OCT+ | the pads' trigger monitor, as a drum module's: the force of the pad hit last over 430 ms (white), PAD THRESHOLD (yellow), the guard a new hit must clear (red), its notes (green: on, blue: off). Two notes of one pad within 250 ms stop the picture: DOUBLE, how far apart, both velocities. OCT+ records again, OCT- goes back. Take a photo of a double and send it with your report |
| AUDIO | SPEAKER LOWCUT | K5 | as SLOOP's |
| AUDIO | LIMITER | K6 | SOFT (default): 9 dB more headroom at the power-on MASTER position, the limiter only near full scale, so a held chord keeps its level; MASTER's top as loud as before (turn it up for loudness). CLASSIC: SLOOP's limiter and MASTER curve |
| AUDIO | FILTER RESO | K7 | the track filter's resonance, OFF .. 10 (SLOOP 2.8) |
| USB | USB AUDIO, USB SERIAL, USB RATE | K5–K7 | as SLOOP's (USB SERIAL only in a build with the serial console) |
| SEQ | STEP ADVANCE, DRUM PREVIEW | K5, K6 | as SLOOP's (2.7.1) |
| PLAY | KEY VELOCITY | K5 | see [Velocity](#velocity) |
| PLAY | BEND UP | K6 | the pitch wheel up, on the internal sounds (the selected synth track): OFF, 1, 2, 3, 4, 5, 7 or 12 semitones, default 7. MIDI IN's pitch bend has its own (GLO > MIDI 2 > BEND) |
| PLAY | BEND DOWN | K7 | the same, down (default 7; e.g. +2 up, −12 down). The earlier BEND RANGE is read as both |
| PLAY | KNOB ACCEL | K8 | SLOOP's (SCREEN on the FM-1): ON (default), a fast turn moves further; OFF, one value a detent |
| MIDI | TRS MIDI OUT | K5 | ON (default) / OFF. The 3.5 mm jack sends what goes out over USB MIDI: the keys and pads (and the sequencer with GLO > SYSTEM > MIDI = SEQ, or DAW mode), on each track's MIDI channel, with or without a computer. NOT SENDING: the UART did not answer; set it again to retry |
| MIDI | MODE | K6 | SYNTH (default) / DAW ([DAW mode](#daw-mode); also `<` + `>`) |
| MIDI | CHANNEL | K7 | 1–16 (default 1): DAW mode's keys and every map entry on MAIN |
| MIDI | LOCAL | K8 | DAW mode: OFF (default; SLOOP silent) / ON (the keys play the selected track, NOTE pads the drum kit); also PATCH tapped |
| DAW | CC MAP | K5 | DEFAULT / USER (the map edited on the keyboard or in the web editor) |
| DAW | KNOBS | K6 | ABSOLUTE (0–127) / RELATIVE (64 ± the detents) |
| DAW | EDIT MAP | K7 | OCT+: the map editor (also PATCH held + OCTAVE+) |
| DAW | RESET MAP | K8 | how many entries differ from DEFAULT; OCT+ twice: USER = DEFAULT |

The jack is a MIDI **OUT** (UART1 on PC7, 31250 baud; there is no MIDI IN on the SMK-37). Connect it with a
TRS-to-DIN MIDI adapter. The SMK-37 is listed with a **type A** TRS jack (a community spec sheet; M-Vave's manual
only says "a 3.5 mm to MIDI adapter", and it has not been measured): if a synth does not respond, try a type B
adapter.

## DAW mode

**< + >** (the second pressed while the first is held) switches **SYNTH ↔ DAW**; so does HOME menu > MIDI > MODE.
A full screen says which. In DAW mode the keyboard is a MIDI controller (USB, and the TRS jack with TRS MIDI OUT on):
SLOOP's sequencer stops and the controls leave SLOOP alone. MIDI IN still plays SLOOP (a sound module for the DAW).

- **Keys:** notes on CHANNEL (HOME menu > MIDI, default 1), the lowest key C3 (48) at octave 0, velocity as KEY
  VELOCITY. OCTAVE− / OCTAVE+: the octave (±3; both: 0).
- **K1–K8** (as printed, whatever KNOB LAYOUT), **FADER 1–4**, the **16 pads**, **13 buttons** and the **wheels** send
  what the map says. KNOB BANK / FADER BANK: bank A / B of the knobs / faders (lit on B); both: the pads' bank.
  Knobs ABSOLUTE (0–127, kept per knob) or RELATIVE (64 ± the detents): HOME menu > DAW > KNOBS. `<` `>` send when
  let go. A knob, fader or wheel sends at most every 8 ms (the last value always); a CC TOGGLE flips once a press.
- **PATCH** tapped: **LOCAL** ON / OFF (PATCH lit: ON). ON: the keys also play the selected track, NOTE pads the drum
  kit (GM drum notes). OFF (default): SLOOP stays silent. PATCH held: the menu.
- **Screen:** DAW, CHANNEL, LOCAL; the last control touched (its name and bank, its message, the value, a bar); the
  fader and pad banks, the octave; the eight knobs as bars with their CCs.
- **Pads:** NOTE bank A blue, bank B green (dim, bright while held); CC yellow (dim, bright while held; a CC TOGGLE
  bright while on); OFF faint.

Default map (CC MAP DEFAULT). M-Vave's own DAW presets use Mackie Control on extra USB ports and its CC numbers are
not published, so the map uses free CCs (no bank select, data entry, volume, pan, pedals or channel mode). A pad or
button CC is 127 while held, 0 when let go.

| Control | Bank A | Bank B | Channel |
|---|---|---|---|
| K1–K8 | CC 70–77 | CC 102–109 | MAIN |
| FADER 1–4 | CC 20–23 | CC 24–27 | MAIN |
| PAD 9–16 (bottom row) | notes 36–43 | notes 52–59 | 10 |
| PAD 1–8 (top row) | notes 44–51 | notes 60–67 | 10 |
| `<` `>` | CC 110, 111 | | MAIN |
| SEQ PLAY, SEQ REC | CC 115, 117 | | MAIN |
| SEQ, FX, PARA | CC 112, 113, 114 | | MAIN |
| ARP, NOTE REPEAT | CC 118, 119 | | MAIN |
| SCALE, CHORD, GLOBE, BT | CC 85, 86, 87, 88 | | MAIN |
| Pitch wheel | pitch bend | | MAIN |
| Mod wheel | CC 1 | | MAIN |
| Keys | notes | | MAIN |

MAIN = HOME menu > MIDI > CHANNEL. **Your own map (USER):**

- **On the keyboard:** PATCH held + OCTAVE+ (or HOME menu > DAW > EDIT MAP). Touch a control (turn a knob, move a
  fader or a wheel, hit a pad, press a button), then KNOB 1 its TYPE (OFF, CC, CC TOGGLE, NOTE, MMC, PITCH BEND, as
  the control has them), KNOB 2 its NUMBER (CC, note or MMC command), KNOB 3 its CHANNEL (MAIN or 1–16); the screen
  names the knobs (K5–K7, or K1–K3 with KNOB LAYOUT = SMK). OCTAVE+: the next control; OCTAVE−: done. The banks
  switch as above. Editing puts CC MAP on USER.
- **In the web editor:** the DAW MAP tab (an SMK-37 with this firmware): the settings and the whole map; send, read,
  back to DEFAULT, save / open a file.
- HOME menu > DAW > **CC MAP**: DEFAULT / USER; **RESET MAP**: OCTAVE+ twice, USER = DEFAULT.

Kept in flash (0xB3000 / 0xB4000) with MODE, CHANNEL, LOCAL, CC MAP and KNOBS; without it: SYNTH, 1, OFF, DEFAULT,
ABSOLUTE.

## Hardware calibration

OCTAVE− + OCTAVE+ held at power-on (or HOME menu > SYSTEM > HARDWARE CALIBRATION): press each button and turn each
knob as the screen names it (K2 SELECT, K3 ALGORITHM, K4 PRESETS, K5–K8; with KNOB LAYOUT = SMK: K2–K4, K5 MASTER,
K6 SELECT, K7 PRESETS, K8 ALGORITHM: the same knobs, per printed knob), then the wheels, OCTAVE+ taking each step:

1. PITCH WHEEL, LET IT REST (its noise sets the dead band)
2. PITCH WHEEL, FULL DOWN (hold it there)
3. PITCH WHEEL, FULL UP
4. MOD WHEEL, AT THE BOTTOM
5. MOD WHEEL, FULL UP

The screen shows the wheel's reading. The full travel then gives the full range (BEND UP / DOWN, mod 0–127); at
power-on a pitch wheel resting near its taught rest is re-centred. 30 s without OCTAVE+ (or too little travel)
keeps the wheels as they were. Kept in flash with the settings (0xB1000 / 0xB2000); without it, or after updating,
the wheels calibrate themselves as before.

## The pad sound picker

Turning PRESETS (K4; K7 with KNOB LAYOUT = SMK) shows the sounds of the selected track's kind on the 16 pads and on the screen (8 × 2), in the
PRESETS order, 16 a page, then the user presets; on the drum track the drum kits. A pad loads its sound and plays a
short preview; < > step the pages. It closes by itself a moment after the last turn, unless KNOB BANK pinned it.
FADER BANK closes it (one screen at a time).

## Power-on and special combos (same as SLOOP on FM-1)

| Combo | Does |
|---|---|
| OCTAVE− held at power-on | USB rescue |
| OCTAVE− + OCTAVE+ held at power-on | hardware calibration (re-teach buttons, knobs and the wheels) |
| OCTAVE− + OCTAVE+ held 5 s, stopped | update mode (UBOOT) |
| KNOB BANK + FADER BANK (SMK-37) | the pads: DRUM KIT → NOTES → STEPS (DAW mode: the pads' bank A / B) |
| < + > (SMK-37) | SYNTH ↔ DAW mode |
| PATCH held + OCTAVE+ (SMK-37, DAW mode) | the DAW map editor |

## Safety

- **Back up the whole 1 MiB flash first**, over the chip's mask-ROM UBOOT mode (e.g. with `jl-uboot-tool`). The stock
  firmware has no way into UBOOT, so you need a USB_KEY dongle (as for the FM-1); with SLOOP installed, hold
  OCTAVE− and OCTAVE+ for 5 seconds while stopped. Keep the dump private: it holds data unique to your unit.
- **Never write 0xC0000–0xC1FFF** (Bluetooth pairing and the factory key / pad calibration, "trimdata") **or key_mac
  (0xFF000–0xFFFFF)**, and leave the stock resources (0xF4000–0xFDFFF) alone: they are unique to each unit and cannot
  be recreated. The firmware and its update loader write only an explicit allow-list of flash ranges (checked at
  compile time and again in the flash driver), but a manual UBOOT write can; restore only the ranges you need.
- `FELUCCA_UART` must stay 0 on the SMK-37 (PH8, the FM-1's MIDI IN, is a key-matrix row there): the build refuses
  otherwise. The SMK-37's TRS MIDI OUT is its own driver (`firmware/hal/smk_uart_tx.h`, `firmware/src/smk_midi_out.h`).
- Power the keyboard from a reliable USB port during an update and do not unplug it while the update screen is up.
