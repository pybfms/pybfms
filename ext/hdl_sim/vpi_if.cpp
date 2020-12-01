/******************************************************************************
 ******************************************************************************/

#include <stdint.h>
#include "vpi_user.h"
#include <stdio.h>
#include <string>
#ifndef _WIN32
#include <dlfcn.h>
#endif
#include "Bfm.h"

struct vpi_api_s {
	void (*vpi_get_value)(vpiHandle, p_vpi_value);
	vpiHandle (*vpi_put_value)(vpiHandle, p_vpi_value, p_vpi_time, PLI_INT32);
	vpiHandle (*vpi_handle)(PLI_INT32, vpiHandle);
	vpiHandle (*vpi_iterate)(PLI_INT32, vpiHandle);
	vpiHandle (*vpi_scan)(vpiHandle);
	PLI_INT32 (*vpi_free_object)(vpiHandle);
	PLI_BYTE8 *(*vpi_get_str)(PLI_INT32, vpiHandle);
	vpiHandle (*vpi_register_systf)(p_vpi_systf_data);
};

// TODO: VPI API implementation
struct vpi_api_func_s {
	const char *name;
	void **fptr;
};

static void *find_vpi_lib() {
	void *vpi_lib = dlopen(0, RTLD_LAZY);

	return vpi_lib;
}

static bool prv_vpi_api_tryload = false;
static bool prv_vpi_api_loaded = false;
static vpi_api_s prv_vpi_api;
static bool prv_debug = false;

static vpi_api_func_s api_tab[] = {
		{"vpi_get_value", (void **)&prv_vpi_api.vpi_get_value},
		{"vpi_put_value", (void **)&prv_vpi_api.vpi_put_value},
		{"vpi_handle", (void **)&prv_vpi_api.vpi_handle},
		{"vpi_iterate", (void **)&prv_vpi_api.vpi_iterate},
		{"vpi_scan", (void **)&prv_vpi_api.vpi_scan},
		{"vpi_free_object", (void **)&prv_vpi_api.vpi_free_object},
		{"vpi_get_str", (void **)&prv_vpi_api.vpi_get_str},
		{"vpi_register_systf", (void **)&prv_vpi_api.vpi_register_systf},
		{0, 0}
};

static bool load_vpi_api() {
	if (prv_vpi_api_tryload) {
		return prv_vpi_api_loaded;
	}

	// Only try to load the VPI API once
	prv_vpi_api_tryload = true;

	if (getenv("PYBFMS_VPI_DEBUG") &&
			getenv("PYBFMS_VPI_DEBUG")[0] == 1) {
		prv_debug = true;
	}

	void *vpi_lib = find_vpi_lib();
	if (prv_debug) {
		fprintf(stdout, "vpi_lib=%p\n", vpi_lib);
		fflush(stdout);
	}
	if (!vpi_lib) {
		fprintf(stdout, "Error: failed to find VPI library\n");
		return false;
	}

	for (uint32_t i=0; api_tab[i].name; i++) {
		void *val = dlsym(vpi_lib, api_tab[i].name);
		if (prv_debug) {
			fprintf(stdout, "VPI: %s=%p\n", api_tab[i].name, val);
			fflush(stdout);
		}
		if (!val) {
			fprintf(stdout, "Error: Failed to find symbol \"%s\" (%s)\n",
					api_tab[i].name, dlerror());
			return false;
		}
		(*api_tab[i].fptr) = val;
	}

	prv_vpi_api_loaded = true;
	return prv_vpi_api_loaded;
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

    if (!load_vpi_api()) {
    	return;
    }

    val.format = vpiIntVal;
    val.value.integer = 1;

    // Signal an event to cause the BFM to wake up
    prv_vpi_api.vpi_put_value((vpiHandle)notify_ev, &val, 0, vpiNoDelay);
}

/**
 * pybfms_register_tf()
 *
 * Implementation for the $pybfms_register system function.
 * Registers a new BFM with the system
 */
static int pybfms_register_tf(char *user_data) {
    if (!load_vpi_api()) {
    	return 1;
    }

    // Obtain arguments
    // - cls_name  -- passed in
    // - notify_ev -- passed in
    // - inst_name -- from call scope
    std::string inst_name, cls_name;
    vpiHandle notify_ev = 0;
    vpiHandle systf_h = prv_vpi_api.vpi_handle(vpiSysTfCall, 0);
    vpiHandle scope_h = prv_vpi_api.vpi_handle(vpiScope, systf_h);
    vpiHandle arg_it = prv_vpi_api.vpi_iterate(vpiArgument, systf_h);
    s_vpi_value val;
    vpiHandle arg;
    uint32_t id;

    (void)user_data;

    // Get the instance name from the context
    inst_name = prv_vpi_api.vpi_get_str(vpiFullName, scope_h);

    // Get the Python class name
    arg = prv_vpi_api.vpi_scan(arg_it);
    val.format = vpiStringVal;
    prv_vpi_api.vpi_get_value(arg, &val);
    cls_name = val.value.str;

    // Get the handle to the notify event
    notify_ev = prv_vpi_api.vpi_scan(arg_it);

    prv_vpi_api.vpi_free_object(arg_it);

    id = Bfm::add_bfm(new Bfm(inst_name, cls_name, &pybfms_notify, notify_ev));

    // Set return value
    val.format = vpiIntVal;
    val.value.integer = (int32_t)id;
    prv_vpi_api.vpi_put_value(systf_h, &val, 0, vpiNoDelay);

    return 0;
}

static int pybfms_claim_msg_tf(char *user_data) {
    if (!load_vpi_api()) {
    	return 1;
    }

    vpiHandle systf_h = prv_vpi_api.vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = prv_vpi_api.vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;
    int32_t msg_id = -1;

    (void)user_data;

    // Get the BFM ID
    arg = prv_vpi_api.vpi_scan(arg_it);
    val.format = vpiIntVal;
    prv_vpi_api.vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    prv_vpi_api.vpi_free_object(arg_it);

    msg_id = Bfm::get_bfms().at(bfm_id)->claim_msg();

    // Set return value
    val.format = vpiIntVal;
    val.value.integer = msg_id;
    prv_vpi_api.vpi_put_value(systf_h, &val, 0, vpiNoDelay);

    return 0;
}

static int pybfms_get_param_i32_tf(char *user_data) {
    if (!load_vpi_api()) {
    	return 1;
    }

    vpiHandle systf_h = prv_vpi_api.vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = prv_vpi_api.vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;
    int64_t pval;

    (void)user_data;

    // Get the BFM ID
    arg = prv_vpi_api.vpi_scan(arg_it);
    val.format = vpiIntVal;
    prv_vpi_api.vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    prv_vpi_api.vpi_free_object(arg_it);

    BfmMsg *msg = Bfm::get_bfms().at(bfm_id)->active_msg();
    if (msg) {
    	pval = msg->get_param_si();
    } else {
    	pval = 0;
    }

    // Set return value
    val.format = vpiIntVal;
    val.value.integer = (int32_t)pval;
    prv_vpi_api.vpi_put_value(systf_h, &val, 0, vpiNoDelay);

    return 0;
}

static int pybfms_get_param_ui32_tf(char *user_data) {
    if (!load_vpi_api()) {
    	return 1;
    }

    vpiHandle systf_h = prv_vpi_api.vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = prv_vpi_api.vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;
    uint64_t pval;

    (void)user_data;

    // Get the BFM ID
    arg = prv_vpi_api.vpi_scan(arg_it);
    val.format = vpiIntVal;
    prv_vpi_api.vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    prv_vpi_api.vpi_free_object(arg_it);

    BfmMsg *msg = Bfm::get_bfms().at(bfm_id)->active_msg();
    if (msg) {
    	pval = msg->get_param_ui();
    } else {
    	pval = 0;
    }

    // Set return value
    val.format = vpiIntVal;
    // TODO: should really use reg?
    val.value.integer = (int32_t)pval;
    prv_vpi_api.vpi_put_value(systf_h, &val, 0, vpiNoDelay);

    return 0;
}

static int pybfms_begin_msg_tf(char *user_data) {
    if (!load_vpi_api()) {
    	return 1;
    }

    vpiHandle systf_h = prv_vpi_api.vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = prv_vpi_api.vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id, msg_id;

    (void)user_data;

    // Get the BFM ID
    arg = prv_vpi_api.vpi_scan(arg_it);
    val.format = vpiIntVal;
    prv_vpi_api.vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    // Get the msg ID
    arg = prv_vpi_api.vpi_scan(arg_it);
    val.format = vpiIntVal;
    prv_vpi_api.vpi_get_value(arg, &val);
    msg_id = (uint32_t)val.value.integer;

    prv_vpi_api.vpi_free_object(arg_it);

    Bfm::get_bfms().at(bfm_id)->begin_inbound_msg(msg_id);

    return 0;
}

static int pybfms_add_param_si_tf(char *user_data) {
    if (!load_vpi_api()) {
    	return 1;
    }

    vpiHandle systf_h = prv_vpi_api.vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = prv_vpi_api.vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;
    uint64_t pval = 0;

    (void)user_data;

    // Get the BFM ID
    arg = prv_vpi_api.vpi_scan(arg_it);
    val.format = vpiIntVal;
    prv_vpi_api.vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    // Get the parameter value
    arg = prv_vpi_api.vpi_scan(arg_it);
    val.format = vpiIntVal;
    prv_vpi_api.vpi_get_value(arg, &val);
    pval = (uint64_t)val.value.integer;

    prv_vpi_api.vpi_free_object(arg_it);

    BfmMsg *msg = Bfm::get_bfms().at(bfm_id)->active_inbound_msg();
    msg->add_param_si(pval);

    return 0;
}

static int pybfms_add_param_ui_tf(char *user_data) {
    if (!load_vpi_api()) {
    	return 1;
    }

    vpiHandle systf_h = prv_vpi_api.vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = prv_vpi_api.vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;
    uint64_t pval = 0;

    (void)user_data;

    // Get the BFM ID
    arg = prv_vpi_api.vpi_scan(arg_it);
    val.format = vpiIntVal;
    prv_vpi_api.vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    // Get the parameter value
    arg = prv_vpi_api.vpi_scan(arg_it);
    val.format = vpiIntVal;
    prv_vpi_api.vpi_get_value(arg, &val);
    pval = (uint32_t)val.value.integer;

    prv_vpi_api.vpi_free_object(arg_it);

    BfmMsg *msg = Bfm::get_bfms().at(bfm_id)->active_inbound_msg();
    msg->add_param_ui(pval);

    return 0;
}

static int pybfms_end_msg_tf(char *user_data) {
    if (!load_vpi_api()) {
    	return 1;
    }

    vpiHandle systf_h = prv_vpi_api.vpi_handle(vpiSysTfCall, 0);
    vpiHandle arg_it = prv_vpi_api.vpi_iterate(vpiArgument, systf_h);
    vpiHandle arg;
    s_vpi_value val;
    uint32_t bfm_id;

    (void)user_data;

    // Get the BFM ID
    arg = prv_vpi_api.vpi_scan(arg_it);
    val.format = vpiIntVal;
    prv_vpi_api.vpi_get_value(arg, &val);
    bfm_id = (uint32_t)val.value.integer;

    prv_vpi_api.vpi_free_object(arg_it);

    Bfm *bfm = Bfm::get_bfms().at(bfm_id);
    bfm->send_inbound_msg();

    return 0;
}


static void register_bfm_tf(void) {
    s_vpi_systf_data tf_data;
    if (prv_debug) {

    if (!load_vpi_api()) {
    	fprintf(stdout, "Error: VPI API failed to load\n");
	fflush(stdout);
    	return;
    }

    // pybfms_register
    tf_data.type = vpiSysFunc;
    tf_data.tfname = "$pybfms_register";
    tf_data.sysfunctype = vpiIntFunc;
    tf_data.calltf = &pybfms_register_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    prv_vpi_api.vpi_register_systf(&tf_data);

    // pybfms_claim_msg
    tf_data.type = vpiSysFunc;
    tf_data.tfname = "$pybfms_claim_msg";
    tf_data.sysfunctype = vpiIntFunc;
    tf_data.calltf = &pybfms_claim_msg_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    prv_vpi_api.vpi_register_systf(&tf_data);

    // pybfms_get_param_i32
    tf_data.type = vpiSysFunc;
    tf_data.tfname = "$pybfms_get_param_i32";
    tf_data.sysfunctype = vpiIntFunc;
    tf_data.calltf = &pybfms_get_param_i32_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    prv_vpi_api.vpi_register_systf(&tf_data);

    // pybfms_get_param_ui32
    tf_data.type = vpiSysFunc;
    tf_data.tfname = "$pybfms_get_param_ui32";
    tf_data.sysfunctype = vpiIntFunc;
    tf_data.calltf = &pybfms_get_param_ui32_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    prv_vpi_api.vpi_register_systf(&tf_data);

    // pybfms_get_param_i64

    // pybfms_get_param_ui64

    // pybfms_begin_msg
    tf_data.type = vpiSysTask;
    tf_data.tfname = "$pybfms_begin_msg";
    tf_data.sysfunctype = vpiSysTask;
    tf_data.calltf = &pybfms_begin_msg_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    prv_vpi_api.vpi_register_systf(&tf_data);

    // pybfms_add_param_ui
    tf_data.type = vpiSysTask;
    tf_data.tfname = "$pybfms_add_param_ui";
    tf_data.sysfunctype = vpiSysTask;
    tf_data.calltf = &pybfms_add_param_ui_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    prv_vpi_api.vpi_register_systf(&tf_data);

    // pybfms_add_param_si
    tf_data.type = vpiSysTask;
    tf_data.tfname = "$pybfms_add_param_si";
    tf_data.sysfunctype = vpiSysTask;
    tf_data.calltf = &pybfms_add_param_si_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    prv_vpi_api.vpi_register_systf(&tf_data);

    // pybfms_add_param_str

    // pybfms_end_msg
    tf_data.type = vpiSysTask;
    tf_data.tfname = "$pybfms_end_msg";
    tf_data.sysfunctype = vpiSysTask;
    tf_data.calltf = &pybfms_end_msg_tf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    prv_vpi_api.vpi_register_systf(&tf_data);
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
