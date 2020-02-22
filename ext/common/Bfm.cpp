/******************************************************************************
 * Copyright cocotb contributors
 * Licensed under the Revised BSD License, see LICENSE for details.
 * SPDX-License-Identifier: BSD-3-Clause
 ******************************************************************************/
#include "Bfm.h"
#include <stdio.h>

#define EXTERN_C extern "C"

Bfm::Bfm(
        const std::string        &inst_name,
        const std::string        &cls_name,
        bfm_notify_f             notify_f,
        void                    *notify_data) :
        m_instname(inst_name),
        m_clsname(cls_name),
        m_notify_f(notify_f),
        m_notify_data(notify_data) {
    m_active_msg = 0;
    m_active_inbound_msg = 0;
}

Bfm::~Bfm() {
    if (m_active_msg) {
        delete m_active_msg;
        m_active_msg = 0;
    }
    if (m_active_inbound_msg) {
    	  delete m_active_inbound_msg;
    }
}

uint32_t Bfm::add_bfm(Bfm *bfm) {
    bfm->m_bfm_id = static_cast<uint32_t>(m_bfm_l.size());

    m_bfm_l.push_back(bfm);

    return bfm->m_bfm_id;
}

void Bfm::send_msg(BfmMsg *msg) {
    m_msg_queue.push_back(msg);
    if (m_notify_f) {
        m_notify_f(m_notify_data);
    }
}

int Bfm::claim_msg() {
	fprintf(stdout, "--> claim_msg\n");
	fflush(stdout);
    if (m_active_msg) {
        delete m_active_msg;
        m_active_msg = 0;
    }
    if (m_msg_queue.size() > 0) {
        m_active_msg = m_msg_queue.at(0);
        m_msg_queue.erase(m_msg_queue.begin());
        fprintf(stdout, "<-- claim_msg %p\n", m_active_msg);
        fflush(stdout);
        int32_t msg_id = static_cast<int32_t>(m_active_msg->id());
        fprintf(stdout, "  msg_id=%d\n", msg_id);
        fflush(stdout);
        return msg_id;
    } else {
        fprintf(stdout, "<-- claim_msg (-1)\n");
        fflush(stdout);
        return -1;
    }
}

void Bfm::begin_inbound_msg(uint32_t msg_id) {
	fprintf(stdout, "begin_inbound_msg\n");
	fflush(stdout);
    m_active_inbound_msg = new BfmMsg(msg_id);
}

void Bfm::send_inbound_msg() {
	fprintf(stdout, "--> send_inbound_msg\n");
	fflush(stdout);
    if (m_recv_msg_f) {
    	fprintf(stdout, "m_recv_msg_f=%p\n", m_recv_msg_f);
    	fflush(stdout);
        m_recv_msg_f(m_bfm_id, m_active_inbound_msg);
    } else {
        fprintf(stdout, "Error: Attempting to send a message (%d) before initialization\n",
                m_active_inbound_msg->id());
        fflush(stdout);
    }
	fprintf(stdout, "<-- send_inbound_msg\n");
	fflush(stdout);

    // Clean up
    delete m_active_inbound_msg;
    m_active_inbound_msg = 0;
	fprintf(stdout, "<-- send_inbound_msg (2)\n");
	fflush(stdout);
}

void Bfm::set_recv_msg_f(bfm_recv_msg_f f) {
	fprintf(stdout, "set_rev_msg_f: %p\n", f);
	fflush(stdout);
	m_recv_msg_f = f;
}

std::vector<Bfm *> Bfm::m_bfm_l;
bfm_recv_msg_f Bfm::m_recv_msg_f = 0;


EXTERN_C uint32_t bfm_get_count() {
	return Bfm::get_bfms().size();
}

EXTERN_C const char *bfm_get_instname(uint32_t bfm_id) {
	return Bfm::get_bfms().at(bfm_id)->get_instname().c_str();
}

EXTERN_C const char *bfm_get_clsname(uint32_t bfm_id) {
	return Bfm::get_bfms().at(bfm_id)->get_clsname().c_str();
}

EXTERN_C void bfm_send_msg(uint32_t bfm_id, BfmMsg *msg) {
	fprintf(stdout, "bfm_send_msg: bfm_id=%d msg=%p\n", bfm_id, msg);
	fprintf(stdout, "id=%d\n", msg->id());
	fflush(stdout);
	Bfm::get_bfms().at(bfm_id)->send_msg(msg);
	fprintf(stdout, "post-send\n");
	fflush(stdout);
}

EXTERN_C void bfm_set_recv_msg_callback(bfm_recv_msg_f f) {
	Bfm::set_recv_msg_f(f);
}
