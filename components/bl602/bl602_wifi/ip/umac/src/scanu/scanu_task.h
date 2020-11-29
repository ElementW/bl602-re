
typedef struct scanu_raw_send_cfm scanu_raw_send_cfm, *scanu_raw_send_cfm;

typedef ulong uint32_t;

struct scanu_raw_send_cfm {
    uint32_t status;
};

typedef struct scanu_raw_send_req scanu_raw_send_req, *scanu_raw_send_req;

struct scanu_raw_send_req {
    void * pkt;
    uint32_t len;
};

typedef struct scanu_start_cfm scanu_start_cfm, *scanu_start_cfm;

typedef uchar uint8_t;

struct scanu_start_cfm {
    uint8_t status;
};

typedef struct scanu_start_req scanu_start_req, *scanu_start_req;

typedef struct scan_chan_tag scan_chan_tag, *scan_chan_tag;

typedef struct mac_ssid mac_ssid, *mac_ssid;

typedef struct mac_addr mac_addr, *mac_addr;

typedef uint32_t u32_l;

typedef ushort uint16_t;

typedef uint16_t u16_l;

typedef uint8_t u8_l;

typedef bool _Bool;

typedef char int8_t;

struct mac_addr {
    u8_l array[6];
};

struct mac_ssid {
    uint8_t length;
    uint8_t array[32];
    uint8_t array_tail[1];
};

struct scan_chan_tag {
    uint16_t freq;
    uint8_t band;
    uint8_t flags;
    int8_t tx_power;
    undefined field_0x5;
};

struct scanu_start_req {
    struct scan_chan_tag chan[42];
    struct mac_ssid ssid[2];
    struct mac_addr bssid;
    undefined field_0x146;
    undefined field_0x147;
    u32_l add_ies;
    u16_l add_ie_len;
    u8_l vif_idx;
    u8_l chan_cnt;
    u8_l ssid_cnt;
    _Bool no_cck;
    undefined field_0x152;
    undefined field_0x153;
};

#if 0 //TODO EXISTS ALEADY
/**
* @file scanu_task.h
* Header file for BL602
*/
#ifndef __SCANU_TASK_H__
#define __SCANU_TASK_H__

struct scanu_start_req {
    struct scan_chan_tag chan[42]; // +0
    struct mac_ssid ssid[2]; // +252
    struct mac_addr bssid; // +320
    uint32_t add_ies; // +328
    uint16_t add_ie_len; // +332
    uint8_t vif_idx; // +334
    uint8_t chan_cnt; // +335
    uint8_t ssid_cnt; // +336
    bool no_cck; // +337
};
struct scanu_raw_send_req {
    void *pkt; // +0
    uint32_t len; // +4
};
struct scanu_raw_send_cfm {
    uint32_t status; // +0
};
struct scanu_start_cfm {
    uint8_t status; // +0
};
const struct ke_state_handler scanu_state_handler[2];const struct ke_state_handler scanu_default_handler;ke_state_t scanu_state[1];

#endif // __SCANU_TASK_H__
#endf 0 //TODO EXISTS ALEADY
