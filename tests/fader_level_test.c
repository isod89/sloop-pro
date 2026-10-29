/* SPDX-License-Identifier: GPL-3.0-only */
/* SMK-37 Pro FADER BANK A (issue #7): faders 1..3 set the synth tracks' LEVEL over the whole travel: silent at the bottom,
 * LEVEL's top at the top, every position above the bottom heard, louder all the way up, half the travel the power-on
 * LEVEL (-4 dB; LEVEL is in 1/2 dB steps, 0..127: the travel read as LEVEL steps put half of it at -24 dB and under,
 * heard as muted). Fader 4 (the drums' LVL, linear) as before. firmware/src/ui_fbank.c fb_move, main.c smk_faders.
 *   cc -O2 -w -Ibuild/gen -Ifirmware/src -Ifirmware/hal tests/fader_level_test.c -lm */
#define UI_PAGES_HARNESS_ONLY 1
#include "ui_pages_test.c"
static uint8_t smk_fbank, smk_fbank_new;           /* (ui_input.c, SMK build) */
static char knob_digit(uint32_t role) { return role == EN_SELECT ? '2' : '5'; }
#include "../firmware/src/ui_fbank.c"

static int32_t db10(uint32_t f)                    /* track 1's LEVEL with fader 1 at f, dB x 10 (-999: silent) */
{
    fb_move(0, 0, f);
    return LEVEL_DB_X10[trk[0].p[P_LEVEL] & 127];
}
static int32_t peak(uint32_t f)                    /* track 1 (a held chord) through the mix, fader 1 at f */
{
    static int32_t o[2 * CTL];
    uint32_t b, i;
    int32_t pk = 0;
    fb_move(0, 0, f);
    for (b = 0; b < 40u; b++) {                    /* (the LEVEL glide settles) */
        mix_block(o, CTL);
        if (b >= 20u)
            for (i = 0; i < 2u * CTL; i++)
                pk = abs(o[i]) > pk ? abs(o[i]) : pk;
    }
    return pk;
}

int main(int argc, char **argv)
{
    uint32_t f, mono = 1, heard = 1;
    int32_t top, prev = -1000, d;
    outdir = argc > 1 ? argv[1] : "build/host";
    panel = PANEL_DEFAULT;
    layers_init();
    host_tracks_init();
    song.master_q12 = 4096;
    for (f = 0; f < NPART; f++) { set_engine_of(&trk[f], TRK_DEF[f][0]); apply_preset_to(&trk[f], TRK_DEF[f][1]); trk[f].engine = trk[f].eng_req; }
    go_home(); ui.force = 1; frame();

    fb_move(0, 0, 0);
    check(trk[0].p[P_LEVEL] == 0, "fader 1 at the bottom: track 1 silent (LEVEL 0)");
    fb_move(0, 0, 127);
    check(trk[0].p[P_LEVEL] == TP[P_LEVEL].max, "fader 1 at the top: LEVEL's top");
    top = db10(127);
    for (f = 1; f <= 127u; f++) {
        d = db10(f);
        mono &= d >= prev;
        heard &= trk[0].p[P_LEVEL] > 0;
        prev = d;
    }
    check(mono && heard, "every position above the bottom: heard (LEVEL > 0), louder all the way up");
    printf("fader_level: fader 1 at 1/4, 1/2, 3/4: %+.1f, %+.1f, %+.1f dB (LEVEL %d at 1/2; the top %+.1f dB)\n",
           db10(32) / 10.0, db10(64) / 10.0, db10(95) / 10.0, (fb_move(0, 0, 64), trk[0].p[P_LEVEL]), top / 10.0);
    check(db10(64) >= top - 120 && db10(64) <= top - 60, "half the travel: 6..12 dB under the top (GM's volume law)");
    check(trk[0].p[P_LEVEL] >= 102 && trk[0].p[P_LEVEL] <= 106, "half the travel: about LEVEL's power-on 104 (-4 dB)");
    check(db10(32) >= top - 300 && db10(95) >= top - 60, "a quarter: within 30 dB of the top, three quarters within 6 dB");
    {
        int16_t l77, l13;
        fb_move(0, 0, 77); l77 = trk[0].p[P_LEVEL];
        fb_move(0, 0, 13); l13 = trk[0].p[P_LEVEL];
        fb_move(0, 1, 77); fb_move(0, 2, 13);
        check(trk[1].p[P_LEVEL] == l77 && trk[2].p[P_LEVEL] == l13, "faders 2 and 3: tracks 2 and 3, the same law");
    }
    fb_move(0, TRK_DRUM, 64);
    check(song.g[G_DRLVL] == 64, "fader 4: the drums' LVL as before (linear, 0..127)");
    {   /* heard: track 1, a held chord, through the whole mix (MASTER at the top) */
        uint32_t k;
        int32_t p0, p1, ph, pt;
        for (k = 1; k < NTRK; k++)
            trk[k].p[P_MUTE] = 1;
        trk_note_on(&trk[0], 60, 100); trk_note_on(&trk[0], 64, 100); trk_note_on(&trk[0], 67, 100);
        p0 = peak(0); p1 = peak(8); ph = peak(64); pt = peak(127);
        printf("fader_level: track 1 through the mix, fader 1 at 0, 8, 64, 127: peak %d, %d, %d, %d\n", p0, p1, ph, pt);
        check(p0 == 0 && p1 > 0 && ph > p1 && pt >= ph && ph * 4 >= pt,
              "through the mix: silent at the bottom, heard low down, half the travel within 12 dB of the top");
    }
    printf("fader_level: %s\n", fails ? "FAIL" : "ok");
    return fails != 0;
}
