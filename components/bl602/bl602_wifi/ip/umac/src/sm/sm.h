
void sm_add_chan_ctx(void);
void sm_assoc_rsp_handler(void);
void sm_auth_handler(void);
void sm_auth_send(void);
void sm_connect_ind.conflict1(void);
void sm_deauth_handler(void);
void sm_disconnect(void);
void sm_disconnect_process(void);
typedef struct sm_env_tag sm_env_tag, *sm_env_tag;

typedef struct sm_connect_req sm_connect_req, *sm_connect_req;

typedef struct sm_connect_ind sm_connect_ind, *sm_connect_ind;

typedef struct co_list co_list, *co_list;

typedef bool _Bool;

typedef struct mac_addr mac_addr, *mac_addr;

typedef struct mac_ssid mac_ssid, *mac_ssid;

typedef struct mac_addr mac_addr, *mac_addr;

typedef struct scan_chan_tag scan_chan_tag, *scan_chan_tag;

typedef ulong uint32_t;

typedef uint32_t u32_l;

typedef ushort uint16_t;

typedef uint16_t u16_l;

typedef _Bool bool_l;

typedef uchar uint8_t;

typedef uint8_t u8_l;

typedef struct co_list_hdr co_list_hdr, *co_list_hdr;

typedef char int8_t;

struct co_list_hdr {
    struct co_list_hdr * next;
};

struct co_list {
    struct co_list_hdr * first;
    struct co_list_hdr * last;
};

struct mac_addr {
    u8_l array[6];
};

struct mac_addr {
    uint16_t array[3];
};

struct sm_env_tag {
    struct sm_connect_req * connect_param;
    struct sm_connect_ind * connect_ind;
    struct co_list bss_config;
    _Bool join_passive;
    _Bool ft_over_ds;
    undefined field_0x12;
    undefined field_0x13;
    int exist_ssid_idx;
    struct mac_addr ft_old_bssid;
    undefined field_0x1e;
    undefined field_0x1f;
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

struct sm_connect_req {
    struct mac_ssid ssid;
    struct mac_addr bssid;
    struct scan_chan_tag chan;
    undefined field_0x2e;
    undefined field_0x2f;
    u32_l flags;
    u16_l ctrl_port_ethertype;
    u16_l ie_len;
    u16_l listen_interval;
    bool_l dont_wait_bcmc;
    u8_l auth_type;
    u8_l uapsd_queues;
    u8_l vif_idx;
    undefined field_0x3e;
    undefined field_0x3f;
    u32_l ie_buf[64];
    _Bool is_supplicant_enabled;
    uint8_t phrase[64];
    uint8_t phrase_pmk[64];
    undefined field_0x1c1;
    undefined field_0x1c2;
    undefined field_0x1c3;
};

struct sm_connect_ind {
    u16_l status_code;
    struct mac_addr bssid;
    bool_l roamed;
    u8_l vif_idx;
    u8_l ap_idx;
    u8_l ch_idx;
    bool_l qos;
    u8_l acm;
    u16_l assoc_req_ie_len;
    u16_l assoc_rsp_ie_len;
    undefined field_0x12;
    undefined field_0x13;
    u32_l assoc_ie_buf[200];
    u16_l aid;
    u8_l band;
    undefined field_0x337;
    u16_l center_freq;
    u8_l width;
    undefined field_0x33b;
    u32_l center_freq1;
    u32_l center_freq2;
    u32_l ac_param[4];
};

void sm_get_bss_params(void);
void sm_init(void);
void sm_join_bss(void);
void sm_scan_bss(void);
