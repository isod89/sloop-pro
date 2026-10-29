/* SPDX-License-Identifier: GPL-3.0-only
 * SMK-37 Pro: Copyright (C) 2026 M. Geisler (genkigenki/makkuro) */
/* The FADER BANK screen: the banks, the active one lit, what faders 1..4 set (track colours).
 * FADER BANK opens it and then steps the bank, as < > and SELECT (K2, or K6) do; PATCH closes it, or it closes by itself.
 * SLOOP Pro: a fifth bank, E ENV: faders 1..4 the selected synth track's ATTACK, DECAY, SUSTAIN, RELEASE (after
 * ChanceTheMaker's sloop-smk); the drum track selected, E sets nothing. */
#ifndef FB_N
#define FB_N 5u                                    /* (ui_input.c has it too) */
#endif
static const char *const FB_NAME[FB_N] = {"LEVEL", "FILTR", "REVRB", "DELAY", "ENV"};
static const char *const FB_ENV[4] = {"ATTACK", "DECAY", "SUSTAIN", "RELEASE"};
#define FB_SHOW_MS 4000u                           /* up this long after the last change */
static uint8_t fb_open;
static uint32_t fb_t, fb_frame;                    /* last action (ms); the frame drawn last */

static int fb_shown(void)
{
    return fb_open && !ui.menu && ui.layer == LY_PLAY && !ui.hold_kind;
}
static void fb_set(uint32_t b)                     /* bank b, the screen up */
{
    smk_fbank = (uint8_t)(b % FB_N);
    smk_fbank_new = 1;
    fb_open = 1;
    fb_t = fm1_ms;
    ui.force = 1;
}
static void fb_close(void) { fb_open = 0; }
static void fb_expire(void)                        /* up FB_SHOW_MS after the last change */
{
    if (fb_open && fm1_ms - fb_t > FB_SHOW_MS)
        fb_open = 0, ui.force = 1;
}
static int fb_left(void)                           /* drawn last frame, not now: the page needs a redraw */
{
    int l = fb_frame && fb_frame + 1u == ui.frame;
    if (l)
        fb_frame = 0;
    return l;
}

/* what fader i sets in bank b (main.c smk_faders); bank E with the drum track selected: nothing (0) */
static const param_desc_t *fb_param(uint32_t b, uint32_t i, int16_t **vp)
{
    static const uint8_t TID[4] = {P_LEVEL, P_TFLT, P_REV, P_DLY}, GID[4] = {G_DRLVL, 0, G_DRREV, G_DRDLY};
    if (b == 4u) {                                 /* E ENV: the selected synth track's envelope */
        if (is_drum(TSEL))
            return 0;
        *vp = &TSEL->p[P_ATK + (i & 3u)];
        return &TP[P_ATK + (i & 3u)];
    }
    if (i == TRK_DRUM && b != 1u) {
        *vp = &song.g[GID[b & 3u]];
        return &GP[GID[b & 3u]];
    }
    *vp = &trk[i].p[TID[b & 3u]];
    return &TP[TID[b & 3u]];
}

/* (#7) a fader's position v (0..127) -> a synth track's LEVEL. LEVEL is in 1/2 dB steps (params.c F_DB: 0 off, 1 -55.5 dB ..
 * 112 0 dB .. 127 +7.5 dB); read as LEVEL steps, the travel's lower half was -55..-24 dB, heard as muted. GM's volume law
 * instead (40 log10(v / 127), as CC 11 EXPRESSION, core.h expr_gain): the gain (LEVEL_Q12) the nearest above
 * LEVEL_Q12[127] (v / 127)^2: 0 off, 1 the quietest step, half the travel -4 dB (LEVEL's power-on 104), the top 127 */
static int16_t fb_level(uint32_t v)
{
    uint32_t want = (LEVEL_Q12[127] * (v > 127u ? 127u : v) * (v > 127u ? 127u : v) + 16128u) / 16129u, l = 0;
    while (l < 127u && LEVEL_Q12[l] < want)
        l++;
    return (int16_t)l;
}

/* fader i moved to v (0..127) in bank b (main.c smk_faders) */
static void fb_move(uint32_t b, uint32_t i, uint32_t v)
{
    int16_t *pv;
    switch (b) {
    case 4:                                           /* SLOOP Pro: E, the selected synth track's ATTACK, DECAY,
                                                       * SUSTAIN, RELEASE over their ranges (none on the drum track) */
        if (!is_drum(TSEL)) {
            const param_desc_t *d = &TP[P_ATK + i];
            TSEL->p[P_ATK + i] = (int16_t)(d->min + ((int32_t)d->max - d->min) * (int32_t)v / 127);
        }
        break;
    case 1:
        trk[i].p[P_TFLT] = (int16_t)((int32_t)v - 64);
        break;
    case 2:
        pv = i == TRK_DRUM ? &song.g[G_DRREV] : &trk[i].p[P_REV];
        *pv = (int16_t)v;
        break;
    case 3:
        pv = i == TRK_DRUM ? &song.g[G_DRDLY] : &trk[i].p[P_DLY];
        *pv = (int16_t)v;
        break;
    default:                                          /* A: the drums' LVL (linear, 0..127), the synths' LEVEL by GM's law */
        if (i == TRK_DRUM)
            song.g[G_DRLVL] = (int16_t)v;
        else
            trk[i].p[P_LEVEL] = fb_level(v);
        break;
    }
}

static void fb_draw(void)
{
    static uint32_t shown;
    uint32_t b = smk_fbank % FB_N, i, half, sig = b * 7919u + song.sel * 104729u;
    int16_t *vp;
    if (fb_frame + 1u != ui.frame) {               /* another screen was up: all of it */
        lcd_fill(0, 0, 240, 240, C_BLACK);
        ui.force = 1;
    }
    fb_frame = ui.frame;
    for (i = 0; i < 4u; i++)
        if (fb_param(b, i, &vp))
            sig = sig * 31u + (uint32_t)(*vp + 200);
    if (!ui.force && sig == shown)
        return;
    shown = sig;
    for (half = 0; half < 2u; half++) {
        cv_begin(240, 120, C_BLACK);
        if (!half) {
            cv_text(4, 2, &FONT_L, "FADER BANK", C_WHITE);
            for (i = 0; i < FB_N; i++) {           /* the banks (five, 48 px each) */
                int32_t x = (int32_t)i * 48 + 1, on = i == b;
                char l[2] = {(char)('A' + i), 0};
                cv_rect(x, 42, 46, 74, on ? C_WHITE : TE_G2);
                if (!on)
                    cv_rect(x + 1, 43, 44, 72, TE_G1);
                cv_text(x + 23 - text_w(&FONT_L, l) / 2, 48, &FONT_L, l, on ? C_BLACK : TE_G3);
                cv_text(x + 23 - text_w(&FONT_S, FB_NAME[i]) / 2, 90, &FONT_S, FB_NAME[i], on ? C_BLACK : TE_G3);
            }
        } else {
            for (i = 0; i < 4u; i++) {             /* the faders: F1 TRACK 1 ... value, a bar */
                int32_t y = 4 + (int32_t)i * 24, w;
                char lab[10] = "TRACK 1", val[12], v2[20];
                const char *unit = "";
                const param_desc_t *d = fb_param(b, i, &vp);
                char f[3] = {'F', (char)('1' + i), 0};
                if (!d) {                          /* E with the drum track selected */
                    if (!i)
                        cv_text(4, 28, &FONT_S, "ENV: SELECT A SYNTH TRACK", C_WHITE);
                    continue;
                }
                if (b == 4u)
                    str_cpy(lab, FB_ENV[i], sizeof lab);   /* (E: the selected track's, in its colour) */
                else if (i == TRK_DRUM)
                    str_cpy(lab, "DRUMS", sizeof lab);
                else
                    lab[6] = (char)('1' + i);
                param_format(d, *vp, val, &unit);
                str_cpy(v2, val, sizeof v2);
                str_cpy(v2 + str_len(v2), unit, sizeof v2 - str_len(v2));
                cv_text(4, y, &FONT_S, f, TE_COL[b == 4u ? song.sel % NTRK : i]);
                cv_text(32, y, &FONT_S, lab, TE_COL[b == 4u ? song.sel % NTRK : i]);
                cv_text(236 - text_w(&FONT_S, v2), y, &FONT_S, v2, C_WHITE);
                w = RATIO(d, *vp) * 204 / 1000;
                cv_rect(32, y + 17, 204, 3, TE_G1);
                cv_rect(32, y + 17, w < 1 ? 1 : w, 3, TE_COL[b == 4u ? song.sel % NTRK : i]);
            }
            {
                char h[24] = "< >  K2  FADER BANK";
                h[6] = knob_digit(EN_SELECT);          /* (SELECT: K2, or K6, HOME menu > SCREEN > KNOB LAYOUT) */
                cv_text((240 - text_w(&FONT_S, h)) / 2, 100, &FONT_S, h, TE_G3);
            }
        }
        cv_blit(0, half * 120u);
    }
}
