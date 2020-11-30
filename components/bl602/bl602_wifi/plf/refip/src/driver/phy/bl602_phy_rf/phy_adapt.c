float calc_ppm(rvec_t * rvec);
float calc_ppm_dsss(uint8_t rxv_freqoff);
float calc_ppm_ofdm(uint16_t rxv_freqoff);
typedef struct input_t input_t, *input_t;

struct input_t {
    int8_t rssi;
    int8_t lna;
    undefined field_0x2;
    undefined field_0x3;
    float ppm;
    uint8_t new;
    undefined field_0x9;
    undefined field_0xa;
    undefined field_0xb;
};

void pa_adapt(uint8_t id);
int8_t pa_alloc(uint32_t vif_addr);
void pa_free(uint8_t id);
void pa_input(uint8_t id, rx_hd * rhd);
void pa_reset(uint8_t id);
typedef struct pa_state_t pa_state_t, *pa_state_t;

struct pa_state_t {
    uint8_t used;
    undefined field_0x1;
    undefined field_0x2;
    undefined field_0x3;
    uint32_t vif_tag;
    struct input_t input_buffer[8];
    int8_t input_buffer_ptr;
    undefined field_0x69;
    undefined field_0x6a;
    undefined field_0x6b;
    uint32_t last_update;
    int8_t rss;
    int8_t rss_acq;
    int8_t rss_trk;
    int8_t rss_state;
    uint8_t rss_hit_count;
    undefined field_0x75;
    undefined field_0x76;
    undefined field_0x77;
    uint32_t rss_count;
    int8_t ris;
    undefined field_0x7d;
    undefined field_0x7e;
    undefined field_0x7f;
    float ce;
    int8_t ce_in;
    int8_t ce_acq;
    int8_t ce_trk;
    int8_t ce_state;
    int8_t ce_num_up_cmds;
    int8_t ce_num_dn_cmds;
    undefined field_0x8a;
    undefined field_0x8b;
};

typedef struct rvec_t rvec_t, *rvec_t;

struct rvec_t {
    uint32_t leg_length:12;
    uint32_t leg_rate:4;
    uint32_t ht_length:16;
    uint32_t _ht_length:4;
    uint32_t short_gi:1;
    uint32_t stbc:2;
    uint32_t smoothing:1;
    uint32_t mcs:7;
    uint32_t pre_type:1;
    uint32_t format_mod:3;
    uint32_t ch_bw:2;
    uint32_t n_sts:3;
    uint32_t lsig_valid:1;
    uint32_t sounding:1;
    uint32_t num_extn_ss:2;
    uint32_t aggregation:1;
    uint32_t fec_coding:1;
    uint32_t dyn_bw:1;
    uint32_t doze_not_allowed:1;
    uint32_t antenna_set:8;
    uint32_t partial_aid:9;
    uint32_t group_id:6;
    uint32_t reserved_1c:1;
    int32_t rssi1:8;
    int32_t rssi2:8;
    int32_t agc_lna:4;
    int32_t agc_rbb1:5;
    int32_t agc_dg:7;
    uint32_t reserved_1d:8;
    uint32_t rcpi:8;
    uint32_t evm1:8;
    uint32_t evm2:8;
    uint32_t freqoff_lo:8;
    uint32_t freqoff_hi:8;
    uint32_t reserved2b_1:8;
    uint32_t reserved2b_2:8;
    uint32_t reserved2b_3:8;
};

#if 0 //TODO EXISTS ALEADY
/**
* @file phy_adapt.c
* Source file for BL602
*/
#include "phy_adapt.h"


typedef struct {
    int8_t rssi;
 // +0
    int8_t lna;
 // +1
    float ppm;
 // +4
    uint8_t new;
 // +8
} input_t;

typedef struct {
    uint8_t used;
 // +0
    uint32_t vif_tag;
 // +4
    input_t input_buffer[8];
 // +8
    int8_t input_buffer_ptr;
 // +104
    uint32_t last_update;
 // +108
    int8_t rss;
 // +112
    int8_t rss_acq;
 // +113
    int8_t rss_trk;
 // +114
    int8_t rss_state;
 // +115
    uint8_t rss_hit_count;
 // +116
    uint32_t rss_count;
 // +120
    int8_t ris;
 // +124
    float ce;
 // +128
    int8_t ce_in;
 // +132
    int8_t ce_acq;
 // +133
    int8_t ce_trk;
 // +134
    int8_t ce_state;
 // +135
    int8_t ce_num_up_cmds;
 // +136
    int8_t ce_num_dn_cmds;
 // +137
} pa_state_t;

typedef struct {
    uint32_t leg_length:12;
 // +0
    uint32_t leg_rate:4;
 // +0
    uint32_t ht_length:16;
 // +0
    uint32_t _ht_length:4;
 // +4
    uint32_t short_gi:1;
 // +4
    uint32_t stbc:2;
 // +4
    uint32_t smoothing:1;
 // +4
    uint32_t mcs:7;
 // +4
    uint32_t pre_type:1;
 // +4
    uint32_t format_mod:3;
 // +4
    uint32_t ch_bw:2;
 // +4
    uint32_t n_sts:3;
 // +4
    uint32_t lsig_valid:1;
 // +4
    uint32_t sounding:1;
 // +4
    uint32_t num_extn_ss:2;
 // +4
    uint32_t aggregation:1;
 // +4
    uint32_t fec_coding:1;
 // +4
    uint32_t dyn_bw:1;
 // +4
    uint32_t doze_not_allowed:1;
 // +4
    uint32_t antenna_set:8;
 // +8
    uint32_t partial_aid:9;
 // +8
    uint32_t group_id:6;
 // +8
    uint32_t reserved_1c:1;
 // +8
    int32_t rssi1:8;
 // +8
    int32_t rssi2:8;
 // +12
    int32_t agc_lna:4;
 // +12
    int32_t agc_rbb1:5;
 // +12
    int32_t agc_dg:7;
 // +12
    uint32_t reserved_1d:8;
 // +12
    uint32_t rcpi:8;
 // +16
    uint32_t evm1:8;
 // +16
    uint32_t evm2:8;
 // +16
    uint32_t freqoff_lo:8;
 // +16
    uint32_t freqoff_hi:8;
 // +20
    uint32_t reserved2b_1:8;
 // +20
    uint32_t reserved2b_2:8;
 // +20
    uint32_t reserved2b_3:8;
 // +20
} rvec_t;

static pa_state_t pa_env[4];

void pa_init(void);
int8_t pa_alloc(uint32_t vif_addr);
void pa_free(uint8_t id);
void pa_reset(uint8_t id);
void pa_input(uint8_t id, struct rx_hd *rhd);
void pa_adapt(uint8_t id);




/** pa_init
 */
void pa_init(void)
{
	ASSER_ERR(FALSE);
	return;
}

/** pa_alloc
 */
int8_t pa_alloc(uint32_t vif_addr)
{
	ASSER_ERR(FALSE);
	return -1;
}

/** pa_free
 */
void pa_free(uint8_t id)
{
	ASSER_ERR(FALSE);
	return;
}

/** pa_reset
 */
void pa_reset(uint8_t id)
{
	ASSER_ERR(FALSE);
	return;
}

/** pa_input
 */
void pa_input(uint8_t id, struct rx_hd *rhd)
{
	ASSER_ERR(FALSE);
	return;
}

/** pa_adapt
 */
void pa_adapt(uint8_t id)
{
	ASSER_ERR(FALSE);
	return;
}
#endf 0 //TODO EXISTS ALEADY
