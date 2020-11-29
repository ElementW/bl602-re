
typedef union anon_union.conflict97f3_for_u anon_union.conflict97f3_for_u, *anon_union.conflict97f3_for_u;

typedef struct anon_struct.conflict9793 anon_struct.conflict9793, *anon_struct.conflict9793;

typedef struct anon_struct.conflict97ca anon_struct.conflict97ca, *anon_struct.conflict97ca;

typedef ulong uint32_t;

struct anon_struct.conflict97ca {
    uint32_t key[4];
};

struct anon_struct.conflict9793 {
    uint32_t tx_key[2];
    uint32_t rx_key[2];
};

union anon_union.conflict97f3_for_u {
    struct anon_struct.conflict9793 mic;
    struct anon_struct.conflict97ca mfp;
};

typedef union anon_union.conflict97f3 anon_union.conflict97f3, *anon_union.conflict97f3;

union anon_union.conflict97f3 {
    struct anon_struct.conflict9793 mic;
    struct anon_struct.conflict97ca mfp;
};

typedef struct key_info_tag key_info_tag, *key_info_tag;

typedef ulonglong __uint64_t;

typedef __uint64_t uint64_t;

typedef uchar uint8_t;

typedef bool _Bool;

struct key_info_tag {
    uint64_t rx_pn[9];
    uint64_t tx_pn;
    union anon_union.conflict97f3_for_u u;
    uint8_t cipher;
    uint8_t key_idx;
    uint8_t hw_key_idx;
    _Bool valid;
    undefined field_0x64;
    undefined field_0x65;
    undefined field_0x66;
    undefined field_0x67;
};

typedef struct mac_addr mac_addr, *mac_addr;

typedef ushort uint16_t;

struct mac_addr {
    uint16_t array[3];
};

typedef struct mac_edca_param_set mac_edca_param_set, *mac_edca_param_set;

struct mac_edca_param_set {
    uint8_t qos_info;
    uint8_t acm;
    undefined field_0x2;
    undefined field_0x3;
    uint32_t ac_param[4];
};

typedef struct mac_htcapability mac_htcapability, *mac_htcapability;

struct mac_htcapability {
    uint16_t ht_capa_info;
    uint8_t a_mpdu_param;
    uint8_t mcs_rate[16];
    undefined field_0x13;
    uint16_t ht_extended_capa;
    undefined field_0x16;
    undefined field_0x17;
    uint32_t tx_beamforming_capa;
    uint8_t asel_capa;
    undefined field_0x1d;
    undefined field_0x1e;
    undefined field_0x1f;
};

typedef struct mac_rateset mac_rateset, *mac_rateset;

struct mac_rateset {
    uint8_t length;
    uint8_t array[12];
};

typedef struct mac_scan_result mac_scan_result, *mac_scan_result;

typedef struct mac_ssid mac_ssid, *mac_ssid;

typedef struct scan_chan_tag scan_chan_tag, *scan_chan_tag;

typedef char int8_t;

struct mac_ssid {
    uint8_t length;
    uint8_t array[32];
    uint8_t array_tail[1];
};

struct mac_scan_result {
    struct mac_addr bssid;
    struct mac_ssid ssid;
    uint16_t bsstype;
    undefined field_0x2a;
    undefined field_0x2b;
    struct scan_chan_tag * chan;
    uint16_t beacon_period;
    uint16_t cap_info;
    _Bool valid_flag;
    int8_t rssi;
    int8_t ppm_rel;
    int8_t ppm_abs;
};

struct scan_chan_tag {
    uint16_t freq;
    uint8_t band;
    uint8_t flags;
    int8_t tx_power;
    undefined field_0x5;
};

typedef struct mac_sec_key mac_sec_key, *mac_sec_key;

struct mac_sec_key {
    uint8_t length;
    undefined field_0x1;
    undefined field_0x2;
    undefined field_0x3;
    uint32_t array[8];
};

typedef struct mac_sta_info mac_sta_info, *mac_sta_info;

typedef struct mac_vhtcapability mac_vhtcapability, *mac_vhtcapability;

struct mac_vhtcapability {
    uint32_t vht_capa_info;
    uint16_t rx_mcs_map;
    uint16_t rx_highest;
    uint16_t tx_mcs_map;
    uint16_t tx_highest;
};

struct mac_sta_info {
    struct mac_rateset rate_set;
    undefined field_0xd;
    undefined field_0xe;
    undefined field_0xf;
    struct mac_htcapability ht_cap;
    struct mac_vhtcapability vht_cap;
    uint32_t capa_flags;
    uint8_t phy_bw_max;
    uint8_t bw_cur;
    uint8_t uapsd_queues;
    uint8_t max_sp_len;
    uint8_t stbc_nss;
    undefined field_0x45;
    undefined field_0x46;
    undefined field_0x47;
};

#if 0 //TODO EXISTS ALEADY
/**
* @file mac.h
* Header file for BL602
*/
#ifndef __MAC_H__
#define __MAC_H__

struct mac_addr {
    uint16_t array[3]; // +0
};
struct mac_ssid {
    uint8_t length; // +0
    uint8_t array[32]; // +1
    uint8_t array_tail[1]; // +33
};
struct mac_rateset {
    uint8_t length; // +0
    uint8_t array[12]; // +1
};
struct key_info_tag {
    uint64_t rx_pn[9]; // +0
    uint64_t tx_pn; // +72
    union {
        struct {
            uint32_t tx_key[2]; // +0
            uint32_t rx_key[2]; // +8
        } mic;
        struct {
            uint32_t key[4]; // +0
        } mfp;
    } u; // +80
    uint8_t cipher; // +96
    uint8_t key_idx; // +97
    uint8_t hw_key_idx; // +98
    bool valid; // +99
};
struct mac_sec_key {
    uint8_t length; // +0
    uint32_t array[8]; // +4
};
struct mac_htcapability {
    uint16_t ht_capa_info; // +0
    uint8_t a_mpdu_param; // +2
    uint8_t mcs_rate[16]; // +3
    uint16_t ht_extended_capa; // +20
    uint32_t tx_beamforming_capa; // +24
    uint8_t asel_capa; // +28
};
struct mac_vhtcapability {
    uint32_t vht_capa_info; // +0
    uint16_t rx_mcs_map; // +4
    uint16_t rx_highest; // +6
    uint16_t tx_mcs_map; // +8
    uint16_t tx_highest; // +10
};
struct mac_edca_param_set {
    uint8_t qos_info; // +0
    uint8_t acm; // +1
    uint32_t ac_param[4]; // +4
};
struct mac_scan_result {
    struct mac_addr bssid; // +0
    struct mac_ssid ssid; // +6
    uint16_t bsstype; // +40
    struct scan_chan_tag *chan; // +44
    uint16_t beacon_period; // +48
    uint16_t cap_info; // +50
    bool valid_flag; // +52
    int8_t rssi; // +53
    int8_t ppm_rel; // +54
    int8_t ppm_abs; // +55
};
struct mac_sta_info {
    struct mac_rateset rate_set; // +0
    struct mac_htcapability ht_cap; // +16
    struct mac_vhtcapability vht_cap; // +48
    uint32_t capa_flags; // +60
    uint8_t phy_bw_max; // +64
    uint8_t bw_cur; // +65
    uint8_t uapsd_queues; // +66
    uint8_t max_sp_len; // +67
    uint8_t stbc_nss; // +68
};
const uint8_t mac_tid2ac[];const uint8_t mac_ac2uapsd[4];const uint8_t mac_id2rate[];const struct mac_addr mac_addr_bcst;

#endif // __MAC_H__
#endf 0 //TODO EXISTS ALEADY
