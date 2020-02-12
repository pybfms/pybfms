/******************************************************************************
 * Copyright cocotb contributors
 * Licensed under the Revised BSD License, see LICENSE for details.
 * SPDX-License-Identifier: BSD-3-Clause
 ******************************************************************************/
#ifndef INCLUDED_BFM_H
#define INCLUDED_BFM_H
#include <stdint.h>
#include <string>
#include <vector>
#include "BfmMsg.h"

typedef void (*bfm_recv_msg_f)(
		uint32_t		msg_id,
		BfmMsg			*msg);

typedef void (*bfm_notify_f)(void *);


class Bfm {
public:

    Bfm(
            const std::string        &inst_name,
            const std::string        &cls_name,
            bfm_notify_f             notify_f,
            void                    *notify_data
            );

    virtual ~Bfm();

    static uint32_t add_bfm(Bfm *bfm);

    static const std::vector<Bfm *> &get_bfms() { return m_bfm_l; }

    const std::string &get_instname() const { return m_instname; }

    const std::string &get_clsname() const { return m_clsname; }

    void send_msg(BfmMsg *msg);

    int claim_msg();

    BfmMsg *active_msg() const { return m_active_msg; }

    void begin_inbound_msg(uint32_t msg_id);

    BfmMsg *active_inbound_msg() const { return m_active_inbound_msg; }

    void send_inbound_msg();

    static void set_recv_msg_f(bfm_recv_msg_f f) { m_recv_msg_f = f; }

protected:

private:
    /**
     * Index (ID) of the BFM. Used in routing messages
     * to the appropriate BFM in Python
     */
    uint32_t                         m_bfm_id;
    /**
     * Instance name of the BFM from simulation
     */
    std::string                      m_instname;
    /**
     * Python class typename used for this BFM
     */
    std::string                      m_clsname;

    /**
     * Callback function that the BFM calls when
     * an outbound (Python->HDL) message is available
     */
    bfm_notify_f                      m_notify_f;
    /**
     * User data passed to the notify callback function
     */
    void                             *m_notify_data;
    /**
     * List of queued output (Python->HDL) messages
     */
    std::vector<BfmMsg *>         m_msg_queue;

    /**
     * The HDL tasks used for processing messages
     * work on a single message at a time. This is
     * the message currently being processed
     */
    BfmMsg                        *m_active_msg;

    /**
     * The HDL tasks used to build an inbound
     * (HDL->Python) build up a message iteratively.
     * This is a pointer to the message currently
     * being built.
     */
    BfmMsg                        *m_active_inbound_msg;

    /**
     * Callback function to handle inbound (HDL->Python)
     * messages. This function is called by the BFM
     * whenever the HDL BFM sends a message
     */
    static bfm_recv_msg_f            m_recv_msg_f;

    /**
     * List of BFM class instances.
     */
    static std::vector<Bfm *>     m_bfm_l;


};

#endif /* INCLUDED_BFM_H */
