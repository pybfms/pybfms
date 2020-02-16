/******************************************************************************
 * Copyright cocotb contributors
 * Licensed under the Revised BSD License, see LICENSE for details.
 * SPDX-License-Identifier: BSD-3-Clause
 ******************************************************************************/
#ifndef INCLUDED_BFM_MSG_H
#define INCLUDED_BFM_MSG_H
#include <vector>
#include <string>
#include <utility>
#include <stdint.h>

enum MsgParamType {
    ParamType_Str,
    ParamType_Si,
    ParamType_Ui
};

struct MsgParam {
    MsgParamType           ptype;
    std::string            str;
    union {
        uint64_t           ui64;
        int64_t            i64;
        const char         *str;
    } pval;
};

struct BfmMsg {
public:

    BfmMsg(uint32_t id);

    virtual ~BfmMsg();

    uint32_t id() const { return m_id; }

    void add_param_ui(uint64_t p);

    void add_param_si(int64_t p);

    void add_param_s(const char *p);

    void add_param(const MsgParam &p);

    uint32_t num_params() const { return m_param_l.size(); }

    const MsgParam *get_param();

    const MsgParam *get_param(uint32_t idx) const;

    uint64_t get_param_ui();

    int64_t get_param_si();

    const char *get_param_str();

protected:

private:
    /**
     * Identifies the index of the inbound or outbound
     * task to call. An outbound (Python->HDL) message
     * with id=0 will call the first (0th) task marked
     * with the cocotb.bfm_import decorator.
     */
    uint32_t                                m_id;

    std::vector<MsgParam>					m_param_l;

#ifdef UNDEFINED
    /**
     * List of message parameters.
     */
    cocotb_bfm_msg_param_t                  *m_param_l;
    /**
     * Insert index into the parameter list. Adding
     * new parameters to the message increases _idx
     */
    uint32_t                                m_param_l_idx;
    /**
     * Maximum size of the parameter list. The parameter
     * list is expanded when _idx >= _max
     */
    uint32_t                                m_param_l_max;
#endif

    /**
     * The value of string parameters is stored in this
     * list. The parameter-list entry holds a pointer
     * to an element in this list.
     */
    std::vector<std::string>                m_str_l;

    /**
     * Read index into the parameter list. _idx is
     * increased when the BFM reads a parameter from
     * the message.
     */
    uint32_t                                m_idx;

};

#endif /* INCLUDED_BFM_MSG_H */

