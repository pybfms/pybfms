/******************************************************************************
 ******************************************************************************/

#include <stdint.h>
#include "vpi_user.h"
#include <stdio.h>
#include <string>

// TODO: VPI API implementation
static void				*prv_vpi_lib = 0;

static void *vpi_lib(void) {
	if (!prv_vpi_lib) {
	}
	return prv_vpi_lib;
}


/**
 * pybfms_notify()
 *
 * Callback function called by the BFM to notify that
 * there is a message to be received. In the VPI
 * implementation, this callback notifies the event
 * that the BFM is waiting on.
 */
static void pybfms_notify(void *notify_ev) {
    s_vpi_value val;

    val.format = vpiIntVal;
    val.value.integer = 1;

    // Signal an event to cause the BFM to wake up
    vpi_put_value((vpiHandle)notify_ev, &val, 0, vpiNoDelay);
}

/**
 * pybfms_register_tf()
 *
 * Implementation for the $pybfms_register system function.
 * Registers a new BFM with the system
 */
static int pybfms_register_tf(char *user_data) {
    // Obtain arguments
    // - cls_name  -- passed in
    // - notify_ev -- passed in
    // - inst_name -- from call scope
    std::string inst_name, cls_name;
    vpiHandle notify_ev = 0;
    vpiHandle systf_h = vpi_handle(vpiSysTfCall, 0);
    vpiHandle scope_h = vpi_handle(vpiScope, systf_h);
    vpiHandle arg_it = vpi_iterate(vpiArgument, systf_h);
    s_vpi_value val;
    vpiHandle arg;
    uint32_t id;

    (void)user_data;

    // Get the instance name from the context
    inst_name = vpi_get_str(vpiFullName, scope_h);

    // Get the Python class name
    arg = vpi_scan(arg_it);
    val.format = vpiStringVal;
    vpi_get_value(arg, &val);
    cls_name = val.value.str;

    // Get the handle to the notify event
    notify_ev = vpi_scan(arg_it);

    vpi_free_object(arg_it);

    id = pybfms_register(
            inst_name.c_str(),
            cls_name.c_str(),
            &pybfms_notify,
            notify_ev
            );

    // Set return value
    val.format = vpiIntVal;
    val.value.integer = (int32_t)id;
    vpi_put_value(systf_h, &val, 0, vpiNoDelay);

    return 0;
}

static int pybfms_claim_msg_tf(char *user_data) {
    vpiHandle systf_h = vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;
    int32_t msg_id = -1;

    (void)user_data;

    // Get the BFM ID
    arg = vpi_scan(arg_it);
    val.format = vpiIntVal;
    vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    vpi_free_object(arg_it);

    msg_id = pybfms_claim_msg(bfm_id);

    // Set return value
    val.format = vpiIntVal;
    val.value.integer = msg_id;
    vpi_put_value(systf_h, &val, 0, vpiNoDelay);

    return 0;
}

static int pybfms_get_param_i32_tf(char *user_data) {
    vpiHandle systf_h = vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;
    int64_t pval;

    (void)user_data;

    // Get the BFM ID
    arg = vpi_scan(arg_it);
    val.format = vpiIntVal;
    vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    vpi_free_object(arg_it);

    pval = pybfms_get_si_param(bfm_id);

    // Set return value
    val.format = vpiIntVal;
    val.value.integer = (int32_t)pval;
    vpi_put_value(systf_h, &val, 0, vpiNoDelay);

    return 0;
}

static int pybfms_get_param_ui32_tf(char *user_data) {
    vpiHandle systf_h = vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;
    uint64_t pval;

    (void)user_data;

    // Get the BFM ID
    arg = vpi_scan(arg_it);
    val.format = vpiIntVal;
    vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    vpi_free_object(arg_it);

    pval = pybfms_get_ui_param(bfm_id);

    // Set return value
    val.format = vpiIntVal;
    // TODO: should really use reg?
    val.value.integer = (int32_t)pval;
    vpi_put_value(systf_h, &val, 0, vpiNoDelay);

    return 0;
}

static int pybfms_begin_msg_tf(char *user_data) {
    vpiHandle systf_h = vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id, msg_id;

    (void)user_data;

    // Get the BFM ID
    arg = vpi_scan(arg_it);
    val.format = vpiIntVal;
    vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    // Get the msg ID
    arg = vpi_scan(arg_it);
    val.format = vpiIntVal;
    vpi_get_value(arg, &val);
    msg_id = (uint32_t)val.value.integer;

    vpi_free_object(arg_it);

    pybfms_begin_msg(bfm_id, msg_id);

    return 0;
}

static int pybfms_add_param_si_tf(char *user_data) {
    vpiHandle systf_h = vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;
    uint64_t pval = 0;

    (void)user_data;

    // Get the BFM ID
    arg = vpi_scan(arg_it);
    val.format = vpiIntVal;
    vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    // Get the parameter value
    arg = vpi_scan(arg_it);
    val.format = vpiIntVal;
    vpi_get_value(arg, &val);
    pval = (uint64_t)val.value.integer;

    vpi_free_object(arg_it);

    pybfms_add_ui_param(bfm_id, pval);

    return 0;
}

static int pybfms_add_param_ui_tf(char *user_data) {
    vpiHandle systf_h = vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;
    uint64_t pval = 0;

    (void)user_data;

    // Get the BFM ID
    arg = vpi_scan(arg_it);
    val.format = vpiIntVal;
    vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    // Get the parameter value
    arg = vpi_scan(arg_it);
    val.format = vpiIntVal;
    vpi_get_value(arg, &val);
    pval = (uint32_t)val.value.integer;

    vpi_free_object(arg_it);

    pybfms_add_ui_param(bfm_id, pval);

    return 0;
}

static int pybfms_end_msg_tf(char *user_data) {
    vpiHandle systf_h = vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;

    (void)user_data;

    // Get the BFM ID
    arg = vpi_scan(arg_it);
    val.format = vpiIntVal;
    vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    vpi_free_object(arg_it);

    pybfms_end_msg(bfm_id);

    return 0;
}


static void register_bfm_tf(void) {
    s_vpi_systf_data tf_data;


    // pybfms_register
    tf_data.type = vpiSysFunc;
    tf_data.tfname = "$pybfms_register";
    tf_data.calltf = &pybfms_register_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    vpi_register_systf(&tf_data);

    // pybfms_claim_msg
    tf_data.type = vpiSysFunc;
    tf_data.tfname = "$pybfms_claim_msg";
    tf_data.calltf = &pybfms_claim_msg_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    vpi_register_systf(&tf_data);

    // pybfms_get_param_i32
    tf_data.type = vpiSysFunc;
    tf_data.tfname = "$pybfms_get_param_i32";
    tf_data.calltf = &pybfms_get_param_i32_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    vpi_register_systf(&tf_data);

    // pybfms_get_param_ui32
    tf_data.type = vpiSysFunc;
    tf_data.tfname = "$pybfms_get_param_ui32";
    tf_data.calltf = &pybfms_get_param_ui32_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    vpi_register_systf(&tf_data);

    // pybfms_get_param_i64

    // pybfms_get_param_ui64

    // pybfms_begin_msg
    tf_data.type = vpiSysTask;
    tf_data.tfname = "$pybfms_begin_msg";
    tf_data.calltf = &pybfms_begin_msg_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    vpi_register_systf(&tf_data);

    // pybfms_add_param_ui
    tf_data.type = vpiSysTask;
    tf_data.tfname = "$pybfms_add_param_ui";
    tf_data.calltf = &pybfms_add_param_ui_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    vpi_register_systf(&tf_data);

    // pybfms_add_param_si
    tf_data.type = vpiSysTask;
    tf_data.tfname = "$pybfms_add_param_si";
    tf_data.calltf = &pybfms_add_param_si_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    vpi_register_systf(&tf_data);

    // pybfms_add_param_str

    // pybfms_end_msg
    tf_data.type = vpiSysTask;
    tf_data.tfname = "$pybfms_end_msg";
    tf_data.calltf = &pybfms_end_msg_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    vpi_register_systf(&tf_data);
}

void (*vlog_startup_routines[])() = {
	register_bfm_tf,
    0
};


// For non-VPI compliant applications that cannot find vlog_startup_routines symbol
void vlog_startup_routines_bootstrap() {
    for (int i = 0; vlog_startup_routines[i]; i++) {
    	void (*routine)() = vlog_startup_routines[i];
        routine();
    }
}
