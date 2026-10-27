# SLOOP Pro — démarrage rapide (SMK-37)

SLOOP Pro, c'est SLOOP 2.8.2 sur le clavier M-VAVE SMK-37 (Pro, Elite, MKE-P37, Starrykey 37 Play). Tout le
fonctionnement de SLOOP reste le même ; ce guide dit où sont les choses sur le SMK-37 et comment l'installer.
La référence complète (en anglais) : [SLOOP-PRO.md](SLOOP-PRO.md). Le guide de SLOOP : [GUIDE.md](GUIDE.md) et
[DEMARRAGE-RAPIDE-FR.md](DEMARRAGE-RAPIDE-FR.md).

> Firmware non officiel, sans garantie, à installer à vos risques. L'étalonnage d'usine de votre clavier n'est
> jamais écrit, et l'outil officiel de M-VAVE permet toujours de revenir en arrière.

## 1. Installer

**Une seule fois, avant la toute première installation : sauvegardez la flash complète (1 Mo)** avec
[jl-uboot-tool](https://github.com/kagaimiq/jl-uboot-tool), deux lectures identiques, et vérifiez que le texte
`trimdat` est à l'adresse `0xC1224` (procédure : `docs/02-update-and-recovery.md` du kit fm1-to-smk37, section 3).
Gardez ce fichier pour vous : il contient des données propres à votre clavier.

**Sous Windows :**

1. Double-cliquez `INSTALL-SLOOP-PRO.bat`. Il compile les trois paquets dans WSL (la même installation que pour
   SLOOP : distribution `MinUI-Build`, la chaîne JieLi, les fichiers du SDK dans `build\deps\ac79` — copiez ce
   dossier depuis votre dossier `sloop-fm1` si besoin), les met dans `build\release\` avec leurs SHA-256, puis ouvre
   l'installateur dans le navigateur (`http://localhost:8767/webapp/installer/`).
2. Branchez le SMK-37 directement sur l'ordinateur (câble USB de données), fermez les autres logiciels MIDI.
3. Chrome ou Edge : cochez la case, **Installer SLOOP Pro**. La page lit le modèle du clavier et envoie le bon paquet
   (`sloop-pro.fwsc`, `sloop-pro-elite.fwsc` ou `sloop-pro-mke.fwsc`). Ne débranchez rien pendant l'écriture.
4. Le clavier redémarre ; la page vérifie qu'il annonce bien SLOOP Pro (`SMK-37 Pro_9xx`, etc.).

Ligne de commande : `python tools/fm1_install.py build\release\` (Python 3, `pip install mido python-rtmidi`).

**Si l'écriture s'arrête** (câble, coupure) : rebranchez et relancez l'installation — le clavier reste en mode mise
à jour et l'écriture reprend. **Si SLOOP Pro ne démarre pas** : maintenez OCTAVE− en l'allumant (écran
SLOOP PRO USB RESCUE) et réinstallez.

**Vous avez le « Sloop SMK » de ChanceTheMaker** (identité `SMK-37_9xx`) ? Il n'accepte que ses propres paquets :
sauvegardez vos projets, revenez d'abord au firmware M-VAVE (sa page de restauration ou M-UPGRADE), puis installez
SLOOP Pro.

**Revenir au firmware M-VAVE :** sauvegarde des projets dans l'éditeur (Projets → Backup), onglet Réglages :
« Prepare the return to M-Vave », puis M-UPGRADE (l'outil officiel) avec le firmware de votre modèle.

## 2. Les commandes du SMK-37

| SMK-37 | Dans SLOOP Pro |
|---|---|
| K1 | volume général (MASTER) |
| K2 | SELECT : tempo, pages |
| K3 | piste 1–4 |
| K4 | son / kit — les pads montrent les sons (sélecteur de sons) |
| K5–K8 | les 4 molettes de l'écran (bleu, vert, jaune, orange) |
| PATCH | HOME (maintenu : le menu) |
| CHORD / NOTE REPEAT / FX / SCALE / PARA / ARP / SEQ / GLOBE / BT | ENV / LFO / FX / SEL / EDIT / ARP / SEQ / GLO / SAVE |
| SEQ PLAY / SEQ REC | PLAY / REC |
| OCTAVE− / OCTAVE+ | OCT− / OCT+ |
| KNOB BANK | épingle le sélecteur de sons |
| FADER BANK | l'écran des banques de faders, puis banque suivante A→B→C→D→E |
| KNOB BANK + FADER BANK | pads : KIT DE BATTERIE → NOTES (le son de la piste choisie) → PAS (STEPS) |
| < / > | page précédente / suivante (SEQ maintenu : pages de pas) |
| < + > | mode SYNTH ↔ DAW (contrôleur MIDI) |
| 27 touches du milieu (F3–G5) | les 27 touches du FM-1, avec la vélocité |
| 5 touches basses, 5 hautes | notes en plus ; sur la piste batterie : grosse caisse, caisse claire, charleston… |
| Faders 1–4 | pistes 1–4. A niveau, B filtre, C reverb, D delay, **E enveloppe (ATTACK, DECAY, SUSTAIN, RELEASE de la piste synthé choisie)** |
| Molette pitch / mod | pitch bend (BEND UP / DOWN), vibrato |
| Prise PEDAL | **sustain** (pédale branchée avant d'allumer, pied levé) |
| Prise TRS | MIDI OUT (adaptateur TRS → DIN) |

## 3. Le menu (PATCH maintenu)

K2 change de section, K5–K8 règlent les lignes, OCT+ valide, OCT− ferme :
SCREEN · LIGHTS · PADS (**PAD THRESHOLD** : la force qu'il faut pour qu'un pad joue, LOW / MID / HIGH / MAX ; **PAD LIGHTS** : luminosité des pads HIGH / MID / LOW ; **PAD SCOPE** : ce que mesure le pad frappé, voir plus bas) · AUDIO (SPEAKER LOWCUT, LIMITER,
FILTER RESO) · USB · SEQ (STEP ADVANCE, DRUM PREVIEW) · PLAY (KEY VELOCITY, BEND UP, BEND DOWN, KNOB ACCEL) ·
MIDI (TRS MIDI OUT, MODE, CHANNEL, LOCAL) · DAW · SYSTEM (2ND CORE : OFF par défaut, HARDWARE CALIBRATION, …, ABOUT).

## Un pad qui joue deux fois : PAD SCOPE

Menu (PATCH maintenu) → section **PADS** → **PAD SCOPE**, OCT+. L'écran montre ce que mesure le dernier pad frappé
(430 ms) : en blanc la force, en jaune le seuil (PAD THRESHOLD), en rouge le seuil qu'un nouveau coup doit dépasser,
en vert les notes jouées, en bleu leur relâchement. Quand un pad joue deux notes en moins de 250 ms, l'image s'arrête
et affiche **DOUBLE**, l'écart en ms et les deux vélocités : **prenez une photo de l'écran** et envoyez-la. OCT+ :
recommencer ; OCT- : revenir au menu. (Un pad frappé s'allume en blanc un instant.)

## Vos samples

Quatre emplacements, **USR1 à USR4**, comme sur le FM-1 (moteurs SAMPLE et GRAIN, kits de batterie, KIT USR3+4), envoyés
depuis l'éditeur web (onglet Samples). Le SMK-37 a moitié moins de place que le FM-1 (40 Ko par emplacement) :
l'éditeur garde la qualité 22 kHz quand ça rentre (environ 3,6 s), sinon il passe l'emplacement en 11 kHz (il affiche
« 11 kHz ») pour garder environ 7 s, comme sur le FM-1. Après la mise à jour depuis SLOOP Pro 2.8.1 (deux
emplacements), renvoyez vos samples depuis vos fichiers WAV.

## 4. Liste de tests (à cocher sur le clavier)

Notez ce qui va et ce qui ne va pas, avec le modèle (Pro / Elite / MKE) et le numéro de ligne :

1. [ ] Installation depuis le firmware M-VAVE : la page indique le bon modèle et « Terminé ».
2. [ ] Démarrage : logo SLOOP avec le badge **PRO** orange, version 2.8.2 dessous. Menu > SYSTEM > ABOUT : « SLOOP PRO ».
3. [ ] Les 37 touches jouent, douces et fortes (vélocité) ; les 5 touches basses et hautes aussi.
4. [ ] Les 16 pads : kit de batterie (pads orange, plus vifs quand ils sonnent) ; KNOB BANK + FADER BANK : NOTES (le son de la piste choisie), encore une fois : les pas.
   La rangée du haut = pas 1–8.
5. [ ] Les 8 encodeurs : un cran = un pas, rien ne saute ; K1 = volume.
6. [ ] Faders : banques A à E. **E** : choisir une piste synthé, bouger les faders → l'enveloppe change à l'écran et à l'oreille.
7. [ ] Molettes : pitch bend revient bien au centre, vibrato.
8. [ ] **Pédale de sustain** branchée avant d'allumer : notes tenues tant qu'elle est enfoncée, relâchées au pied levé.
9. [ ] **PAD LIGHTS** : HIGH / MID / LOW, les 16 pads s'allument deux par deux en bleu, vert, jaune, orange pendant 1,5 s
   (dites-moi si un pad a une mauvaise couleur).
10. [ ] TRS MIDI OUT vers un synthé : les notes passent ; tenir une note et passer TRS MIDI OUT sur OFF → le synthé se tait.
11. [ ] SEQ → NOTES (2.8) : le piano roll, OCT+ maintenu sur un pas → la bande du bas (SLIDE, NUDGE, FILL, MOVE…).
12. [ ] Sauvegarde d'une section (SAVE), extinction, rallumage : tout est revenu (projets, réglages, PAD LIGHTS).
13. [ ] Mode DAW (< + >) dans un logiciel : notes, encodeurs, faders, pads envoient du MIDI.
14. [ ] L'éditeur web se connecte (onglets Sound, Steps, DAW MAP) ; sauvegarde et restauration (Backup).
15. [ ] Retour au firmware M-VAVE avec M-UPGRADE, puis réinstallation de SLOOP Pro.

En cas de souci, une version de diagnostic avec la console série : `build-sloop-pro.ps1 -Diag`, puis menu > USB >
USB SERIAL ON, redémarrage, et un terminal sur le port COM du clavier : `status`, `smk`, `padtest`, `leds` — copiez
la réponse.
