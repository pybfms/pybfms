/******************************************************************************
 * Copyright cocotb contributors
 * Licensed under the Revised BSD License, see LICENSE for details.
 * SPDX-License-Identifier: BSD-3-Clause
 ******************************************************************************/
#include "BfmMsg.h"
#include <string.h>
#include <stdio.h>

#define EXTERN_C extern "C"

BfmMsg::BfmMsg(uint32_t id) {
    m_id = id;
    m_idx = 0;
}

BfmMsg::~BfmMsg() {
}

void BfmMsg::add_param_ui(uint64_t p) {
	MsgParam param;
    param.ptype = ParamType_Ui;
    param.pval.ui64 = p;
    add_param(param);
}

void BfmMsg::add_param_si(int64_t p) {
    MsgParam param;
    param.ptype = ParamType_Si;
    param.pval.i64 = p;
    add_param(param);
}

void BfmMsg::add_param(const MsgParam &p) {
	m_param_l.push_back(p);
}

void BfmMsg::add_param_s(const char *p) {
	MsgParam param;
    param.ptype = ParamType_Str;
    m_str_l.push_back(p);
    param.pval.str = m_str_l.at(m_str_l.size()-1).c_str();
    add_param(param);
}

const MsgParam *BfmMsg::get_param() {
    MsgParam *ret = 0;
    if (m_idx < m_param_l.size()) {
        ret = &m_param_l[m_idx];
        m_idx++;
    }
    return ret;
}

const MsgParam *BfmMsg::get_param(uint32_t idx) const {
    const MsgParam *ret = 0;
    if (idx < m_param_l.size()) {
        ret = &m_param_l[idx];
    }
    return ret;
}

uint64_t BfmMsg::get_param_ui() {
    uint64_t ret = 0;
    if (m_idx < m_param_l.size()) {
        ret = m_param_l[m_idx].pval.ui64;
        m_idx++;
    } else {
        fprintf(stdout, "Error: Out-of-bound request\n");
    }
    return ret;
}

int64_t BfmMsg::get_param_si() {
    int64_t ret = 0;
    if (m_idx < m_param_l.size()) {
        ret = m_param_l[m_idx].pval.i64;
        m_idx++;
    }
    return ret;
}

const char *BfmMsg::get_param_str() {
    const char *ret = "";
    if (m_idx < m_param_l.size()) {
        ret = m_param_l[m_idx].pval.str;
        m_idx++;
    }
    return ret;
}

EXTERN_C void *bfm_msg_new(uint32_t msg_id) {
	BfmMsg *ret = new BfmMsg(msg_id);

	return ret;
}

EXTERN_C void bfm_msg_add_param_ui(BfmMsg *msg, uint64_t p) {
	msg->add_param_ui(p);
}

EXTERN_C void bfm_msg_add_param_si(BfmMsg *msg, int64_t p) {
	msg->add_param_si(p);
}

EXTERN_C uint32_t bfm_msg_id(BfmMsg *msg) {
	return msg->id();
}

EXTERN_C const MsgParam *bfm_msg_get_param(BfmMsg *msg) {
	return msg->get_param();
}

EXTERN_C uint32_t bfm_msg_param_type(MsgParam *p) {
	return p->ptype;
}

EXTERN_C uint64_t bfm_msg_param_ui(MsgParam *p) {
	return p->pval.ui64;
}

EXTERN_C int64_t bfm_msg_param_si(MsgParam *p) {
	return p->pval.i64;
}


