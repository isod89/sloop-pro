# SLOOP Pro 2.8.1 — les essais sur le SMK-37

Tout ce qu'il faut, dans l'ordre. Le guide rapide (commandes, menu) : [DEMARRAGE-RAPIDE-PRO-FR.md](DEMARRAGE-RAPIDE-PRO-FR.md) ;
la référence complète : [SLOOP-PRO.md](SLOOP-PRO.md).

## 0. Ce qu'il faut

- Le même environnement que pour SLOOP (INSTALL-SLOOP.bat) : WSL **MinUI-Build** avec la chaîne JieLi dans
  `/root/fm1-codex-deps/jieli/toolchain`, Python sur Windows avec Pillow.
- Les fichiers du SDK : déjà dans `build\deps\ac79` de ce dossier. (Sinon le script les prend dans le dossier
  `..\SLOOP` voisin.)
- Chrome ou Edge, un câble USB **de données** branché directement sur le PC (pas de hub).
- Pour la sauvegarde de la flash : [jl-uboot-tool](https://github.com/kagaimiq/jl-uboot-tool).

## 1. Compiler

Double-clic sur **`INSTALL-SLOOP-PRO.bat`**. Trois compilations (Pro, Elite, MKE-P37), quelques minutes. On doit voir :

- `S L O O P   P R O   2.8.1`
- « Building SLOOP Pro for the SMK-37 Pro / SMK-37 Elite / MKE-P37 »
- les paquets et leur SHA-256 dans `build\release\` (`sloop-pro.fwsc`, `sloop-pro-elite.fwsc`, `sloop-pro-mke.fwsc`)
- l'installateur qui s'ouvre : `http://localhost:8767/webapp/installer/`

**Garder la fenêtre noire ouverte** pendant toute l'installation.

- WSL ou chaîne ailleurs : dans PowerShell, `$env:SLOOP_WSL_DISTRO="..."`, `$env:SLOOP_TOOLCHAIN="/chemin/linux"`, puis
  `.\build-sloop-pro.ps1`.
- Erreur de compilation : envoyer les 30 dernières lignes (c'est la première compilation SMK-37 réelle de SLOOP Pro :
  c'est ici qu'on voit si tout tient dans la flash).

## 2. Avant d'installer

- Clavier sous le **« Sloop SMK » de ChanceTheMaker** (identité `SMK-37_9xx`) : sauvegarder ses projets là-bas,
  remettre le firmware M-VAVE (sa page de restauration, ou M-UPGRADE), puis revenir ici.
- Clavier sous le firmware M-VAVE, ou sous le build SMK-37 de genkigenki : on peut installer directement.
- Fermer toute application MIDI (DAW, M-UPGRADE, autres onglets de l'éditeur).

## 3. Installer

1. Modèle : **Automatique**. Cocher la case de risque. **Installer SLOOP Pro**. Autoriser le MIDI.
2. La ligne « Appareil : SMK-37 Pro_016 → paquet SMK-37 Pro_9xx » apparaît : vérifier que c'est le bon modèle.
3. Vérification → Passage en mode mise à jour → Écriture → Redémarrage → « Terminé : le clavier tourne SMK-37 Pro_9xx ».
4. **Ne rien débrancher pendant l'écriture.** Arrêt en route : rebrancher, Installer à nouveau (ça reprend).
   Le clavier ne démarre pas : **OCTAVE−** maintenu à l'allumage (SLOOP PRO USB RESCUE), puis réinstaller.

**Sous Windows, si la page reste bloquée à « Passage en mode mise à jour »** (Chrome garde le port MIDI du clavier
pendant son redémarrage) : fermer **complètement** Chrome / Edge, débrancher / rebrancher le clavier, puis double-clic sur
**`INSTALLER-USB-PRO.bat`** : il parle au clavier sans navigateur, trouve le bon paquet, reprend ou fait l'installation
et vérifie le clavier à la fin. (Le clavier n'a rien perdu : tant que l'écriture n'a pas commencé, il revient à son
firmware d'origine en le rallumant.)

Ligne de commande (la même chose) : `python tools\fm1_install.py build\release\` (Windows : rien à installer ; Linux / macOS : `pip install mido python-rtmidi`).

## 4. Sauvegarde complète de la flash (une fois, tout de suite après)

(Inutile si une sauvegarde complète de ce clavier existe déjà. L'installation n'écrit jamais l'étalonnage d'usine.)

1. Séquenceur arrêté : **OCTAVE− + OCTAVE+ maintenus 5 secondes**. Le clavier devient un disque **« WL82 UBOOT1.00 »**.
2. PowerShell **en administrateur**. `Get-Disk` : noter le numéro N du disque WL82 UBOOT.
3. Deux lectures :
   ```
   python jluboottool.py --device \\.\PhysicalDriveN --chip wl82 "read 0 0x100000 smk37-dump-1.bin"
   python jluboottool.py --device \\.\PhysicalDriveN --chip wl82 "read 0 0x100000 smk37-dump-2.bin"
   ```
4. Vérifier : 1 048 576 octets chacun ; `Get-FileHash smk37-dump-*.bin` identiques ; le texte `trimdat` à l'adresse
   **0xC1224** (éditeur hexa, par ex. HxD).
5. Garder les deux fichiers à deux endroits, privés. Éteindre, rallumer.

## 5. Les essais (noter OK / PAS OK et un détail)

| # | Action | Attendu |
|---|---|---|
| 1 | Allumer | Logo SLOOP, badge orange **PRO** à droite, « 2.8.1 » dessous |
| 2 | PATCH maintenu (menu) → K2 jusqu'à SYSTEM → ABOUT → OCT+ ; puis 2ND CORE | « SLOOP PRO », version, date ; 2ND CORE sur **OFF** (le défaut) |
| 3 | Les 37 touches, doux puis fort | Toutes jouent avec la nuance ; les 5 basses et 5 hautes : notes ; sur la piste 4 (batterie) : drums |
| 4 | Les 16 pads | Kit de batterie, orange, plus vifs quand ils sonnent ; rangée du haut = pads 1–8 |
| 4b | Les pads, de près : un coup sec ; des coups doux puis forts ; un roulement rapide sur un pad ; un pad tenu doucement | Un coup = **une** note (pas de double frappe), aussi vite qu'une touche ; la nuance suit la force, la même d'un coup égal à l'autre ; le roulement joue chaque coup ; tenu doucement en NOTES : une seule note qui tient |
| 5 | KNOB BANK + FADER BANK ensemble, une fois | « PADS: NOTES » : sur une piste synthé (K3), les pads jouent son son (rangée du bas F3–C4, du haut D4–G5), avec la nuance ; couleur de la piste, plus vive quand la note sonne. Une 2e fois : « PADS: STEPS », pads en mode PAS (haut = pas 1–8), un pad pose / efface un pas ; une 3e : retour au kit |
| 6 | K1–K8, lentement puis très vite | K1 volume, K2 tempo/pages, K3 piste, K4 sons (sur les pads) ; un cran = un pas. **La rotation rapide perd-elle des crans ?** |
| 7 | Faders, FADER BANK plusieurs fois | A niveau, B filtre, C reverb, D delay, **E enveloppe** (piste synthé : ATTACK DECAY SUSTAIN RELEASE à l'écran et à l'oreille ; batterie : « ENV: SELECT A SYNTH TRACK ») |
| 8 | Molettes pitch et mod | Le pitch monte / descend et revient juste au centre ; vibrato |
| 9 | **Pédale** branchée *avant* d'allumer, pied levé : accord, pédale enfoncée, lâcher les touches | Les notes tiennent, s'arrêtent au pied levé |
| 9b | Pads (DRUM KIT puis NOTES) : 20 frappes douces, 20 moyennes, 20 fortes, un doigt laissé posé après une frappe douce, un roulement rapide ; puis Menu → LIGHTS → PAD THRESHOLD (K6) sur LOW et HIGH | Une frappe = une note, même douce ; le roulement joue chaque coup ; LOW : un effleurement joue ; HIGH : il faut appuyer plus |
| 10 | Menu → LIGHTS → PAD LIGHTS (K8) : HIGH / MID / LOW | 1,5 s : les 16 pads deux par deux bleu, vert, jaune, orange, plus ou moins fort. **Un pad de la mauvaise couleur ?** |
| 11 | Synthé sur la prise TRS (adaptateur TRS → DIN) ; tenir une note, menu → MIDI → TRS MIDI OUT sur OFF | Le synthé joue, puis **se tait** au OFF |
| 12 | SEQ → page NOTES ; OCT+ maintenu sur un pas | Piano roll ; bande du bas SLIDE, NUDGE, FILL, MOVE, COPY, DELETE |
| 13 | Motif, SAVE dans une section, éteindre, rallumer, recharger | Tout revient (motif, sons, réglages, PAD LIGHTS) |
| 14 | < et > ensemble (mode DAW), un logiciel ouvert | Notes, encodeurs, faders, pads envoient du MIDI ; < + > revient en SYNTH |
| 15 | `OPEN-EDITOR-PRO.bat` → Connect | Connecté ; Sound, Steps, DAW MAP ; Projects → Backup enregistre un fichier |
| 16 | Réinstaller SLOOP Pro par-dessus | « Terminé », les projets sont toujours là |
| 16b | Éditeur → Samples : un WAV court (2–3 s) dans USR3, un long (6–7 s) dans USR4 ; un kit de batterie dans USR3+4 ; SAMPLE (SET USR3, USR4) et KIT USR3+4 sur le clavier | Les deux envois réussissent (le long : « 11 kHz ») ; USR3 et USR4 jouent ; le kit joue |
| 17 | (facultatif) Retour M-VAVE : Backup, Réglages → « Prepare the return to M-Vave », M-UPGRADE + firmware officiel ; puis réinstaller SLOOP Pro | Clavier d'origine, étalonnage intact ; SLOOP Pro se réinstalle |

## 6. Ce qu'il faut renvoyer

- Le modèle (Pro / Elite / MKE-P37) et la version d'origine (016…).
- Les numéros PAS OK, avec ce qui s'est passé.
- Une erreur de compilation ou d'installation : le texte, et le journal gris sous la barre de progression.
- Si demandé, la console série : `build-sloop-pro.ps1 -Diag`, installer ce paquet, menu → USB → USB SERIAL **ON**,
  redémarrer, un terminal série (PuTTY) sur le port COM du clavier : `status`, `smk`, `padtest`, `leds` — copier les
  réponses.
