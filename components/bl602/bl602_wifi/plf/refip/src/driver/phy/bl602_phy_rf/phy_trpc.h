typedef struct trpc_env_tag trpc_env_tag, *trpc_env_tag;

struct trpc_env_tag {
    int8_t power_dbm_max_rf;
    int8_t power_dbm_min_rf;
    int8_t power_dbm_lim_reg;
    undefined field_0x3;
    int16_t channel_freq;
    int8_t temperature;
    int8_t temperature_compensate;
};

void trpc_get_default_power_idx(void);
void trpc_get_power_idx(void);
void trpc_get_rf_max_power(void);
void trpc_get_rf_min_power(void);
void trpc_init(void);
void trpc_power_get(void);
void trpc_update_power(void);
void trpc_update_power_11b(void);
void trpc_update_power_11g(void);
void trpc_update_power_11n(void);
void trpc_update_vs_channel(void);
void trpc_update_vs_temperature(void);
