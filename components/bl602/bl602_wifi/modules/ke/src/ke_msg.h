
typedef struct ke_msg ke_msg, *ke_msg;

typedef struct co_list_hdr co_list_hdr, *co_list_hdr;

typedef ushort uint16_t;

typedef uint16_t ke_msg_id_t;

typedef uint16_t ke_task_id_t;

typedef ulong uint32_t;

struct co_list_hdr {
    struct co_list_hdr * next;
};

struct ke_msg {
    struct co_list_hdr hdr;
    ke_msg_id_t id;
    ke_task_id_t dest_id;
    ke_task_id_t src_id;
    uint16_t param_len;
    uint32_t[0] param;
};

void * ke_msg2param(ke_msg * msg);
void ke_msg_alloc(void);
void ke_msg_forward_and_change_id(void);
void ke_msg_free(void);
void ke_msg_send(void);
void ke_msg_send_basic(void);
typedef enum ke_msg_status_tag {
    KE_MSG_SAVED=2,
    KE_MSG_NO_FREE=1,
    KE_MSG_CONSUMED=0
} ke_msg_status_tag;

ke_msg * ke_param2msg(void * param_ptr);
typedef uint16_t ke_state_t;

