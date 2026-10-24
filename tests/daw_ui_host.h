/* SPDX-License-Identifier: GPL-3.0-only */
/* tests/daw_ui_test.c: what the SMK-37 HOME menu (ui_menu.c with BOARD_SMK37) and ui_daw.c need on the FM-1 UI harness
 * (ui_pages_test.c includes this before ui_menu.c): the SMK headers, and the DAW part of seq.c (the audio context's:
 * keys, pads) as plain variables. */
#include "smk_vel.h"
#include "smk_wheel.h"
#define SMO_TX_DONE() 1
#define SMO_TX_PUT(b) (void)(b)
#include "smk_midi_out.h"
#include "smk_knobs.h"
static void knob_layout_apply(void) {}
/* the pads (lcd.c, SMK-37): what the menu's PAD LIGHTS (SLOOP Pro) and the DAW lights set */
#define SMK_NPAD 16u
static uint32_t padled_hold_until;
static uint8_t padled_dim, pads[16][3];
static void padled_set(uint32_t p, uint8_t r, uint8_t g, uint8_t b) { pads[p & 15u][0] = r, pads[p & 15u][1] = g, pads[p & 15u][2] = b; }
static void padled_dim_set(uint32_t d) { padled_dim = (uint8_t)(d > 2u ? 2u : d); }
#include "smk_daw.h"
static uint8_t daw_edit, daw_pbank;
static int8_t daw_oct;
static uint16_t daw_pdown;
static uint8_t daw_tog[DAW_N];
static uint32_t daw_tog_t[DAW_N];
static volatile uint8_t daw_touch_pad;
static volatile uint16_t daw_last, daw_last_v;
static volatile uint32_t daw_last_n;
static void daw_shown(uint32_t i, uint32_t v)
{
    daw_last = (uint16_t)(i + 1u);
    daw_last_v = (uint16_t)v;
    daw_last_n++;
}
static volatile int32_t perf_bend, perf_modw;      /* (voice.c, SMK-37) */
static void daw_set(uint32_t on, int splash);
static void daw_edit_open(void);
