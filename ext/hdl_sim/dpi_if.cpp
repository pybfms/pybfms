/******************************************************************************
 * dpi_if.cpp
 ******************************************************************************/
#include <stdio.h>
#include "Bfm.h"

#define EXTERN_C extern "C"

EXTERN_C int pybfms_claim_msg(uint32_t id);
EXTERN_C int pybfms_end_msg(uint32_t bfm_id);

EXTERN_C uint32_t pybfms_register(
        const char                *inst_name,
        const char                *cls_name,
        bfm_notify_f              notify_f,
        void                      *notify_data) {

    return Bfm::add_bfm(new Bfm(
            inst_name,
            cls_name,
            notify_f,
            notify_data
            ));
}

// Returns the number of registered BFMs
EXTERN_C uint32_t pybfms_num_registered(void) {
    return static_cast<uint32_t>(Bfm::get_bfms().size());
}

// Returns the instance name of the specified BFM
EXTERN_C const char *pybfms_instname(uint32_t id) {
    return Bfm::get_bfms().at(id)->get_instname().c_str();
}

// Returns the class name of the specified BFM
EXTERN_C const char *pybfms_clsname(uint32_t id) {
    return Bfm::get_bfms().at(id)->get_clsname().c_str();
}

//
EXTERN_C int pybfms_claim_msg(uint32_t id) {
    return Bfm::get_bfms().at(id)->claim_msg();
}

EXTERN_C uint64_t pybfms_get_ui_param(uint32_t id) {
    Bfm *bfm = Bfm::get_bfms().at(id);
    BfmMsg *msg = bfm->active_msg();

    if (msg) {
        return msg->get_param_ui();
    } else {
        return 0;
    }
}

EXTERN_C int64_t pybfms_get_si_param(uint32_t id) {
    Bfm *bfm = Bfm::get_bfms().at(id);
    BfmMsg *msg = bfm->active_msg();

    if (msg) {
        return msg->get_param_si();
    } else {
        return 0;
    }
}

EXTERN_C const char *pybfms_get_str_param(uint32_t id) {
    Bfm *bfm = Bfm::get_bfms().at(id);
    BfmMsg *msg = bfm->active_msg();

    if (msg) {
        return msg->get_param_str();
    } else {
        return 0;
    }
}

EXTERN_C void pybfms_begin_msg(uint32_t bfm_id, uint32_t msg_id) {
    Bfm *bfm = Bfm::get_bfms().at(bfm_id);

    bfm->begin_inbound_msg(msg_id);
}

EXTERN_C void pybfms_add_si_param(uint32_t bfm_id, int64_t pval) {
    Bfm *bfm = Bfm::get_bfms().at(bfm_id);
    BfmMsg *msg = bfm->active_inbound_msg();

    if (msg) {
        msg->add_param_si(pval);
    } else {
        fprintf(stdout, "Error: attempting to add a signed parameter to a NULL message\n");
    }
}

EXTERN_C void pybfms_add_ui_param(uint32_t bfm_id, uint64_t pval) {
    Bfm *bfm = Bfm::get_bfms().at(bfm_id);
    BfmMsg *msg = bfm->active_inbound_msg();

    if (msg) {
        msg->add_param_ui(pval);
    } else {
        fprintf(stdout, "Error: attempting to add an unsigned parameter to a NULL message\n");
    }
}

EXTERN_C int pybfms_end_msg(uint32_t bfm_id) {
    Bfm *bfm = Bfm::get_bfms().at(bfm_id);

    bfm->send_inbound_msg();
    return 0;
}

#ifdef UNDEFINED
EXTERN_C void pybfms_send_msg(uint32_t   bfm_id,
        uint32_t                msg_id,
        uint32_t                paramc,
        pybfms_msg_param_t    *paramv) {
    Bfm *bfm = Bfm::get_bfms().at(bfm_id);
    BfmMsg *msg = new BfmMsg(msg_id, static_cast<int32_t>(paramc), paramv);
    bfm->send_msg(msg);
}
#endif

EXTERN_C void pybfms_set_recv_msg_f(bfm_recv_msg_f recv_msg_f) {
    Bfm::set_recv_msg_f(recv_msg_f);
}
