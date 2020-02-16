#include <Python.h>
#include "Bfm.h"
#include "BfmMsg.h"

static int gil_takes = 0;
static int gil_releases = 0;
static PyObject *bfm_call_method = 0;

static PyGILState_STATE TAKE_GIL() {
	PyGILState_STATE state = PyGILState_Ensure();
	gil_takes++;
	return state;
}

static void DROP_GIL(PyGILState_STATE state) {
	PyGILState_Release(state);
	gil_releases++;
}

/**
 * bfm_get_count()
 *
 * Returns the number of BFMs registered with PyBFMs
 */
static PyObject *bfm_get_count(PyObject *self, PyObject *args) {
    (void)self;
    (void)args;
    return PyLong_FromUnsignedLong(Bfm::get_bfms().size());
}

/**
 * bfm_get_info()
 *
 * Returns information about a specific BFM
 */
static PyObject *bfm_get_info(PyObject *self, PyObject *args) {
    uint32_t id;

    (void)self;

    if (!PyArg_ParseTuple(args, "i", &id)) {
        return NULL;
    }

    Bfm *bfm = Bfm::get_bfms().at(id);

    return Py_BuildValue("ss",
    		bfm->get_instname().c_str(),
			bfm->get_clsname().c_str());
}

/**
 * bfm_send_msg()
 *
 * Sends a message to a specific BFM
 * - bfm_id
 * - msg_id
 * - param_l
 * - type_l
 */
static PyObject *bfm_send_msg(PyObject *self, PyObject *args) {
    uint32_t bfm_id, msg_id;
    PyObject *param_l, *type_l;
    (void)self;

    if (!PyArg_ParseTuple(args, "iiOO", &bfm_id, &msg_id, &param_l, &type_l)) {
        return NULL;
    }

    BfmMsg *msg = new BfmMsg(msg_id);


    for (uint32_t i=0; i<PyList_Size(param_l); i++) {
    	PyObject *t = PyList_GetItem(type_l, i);
    	PyObject *v = PyList_GetItem(param_l, i);
    	MsgParamType ptype = (MsgParamType)PyLong_AsLong(t);

    	switch (ptype) {
    	case ParamType_Si: {
    		msg->add_param_si(PyLong_AsUnsignedLongLong(v));
    	} break;
    	case ParamType_Ui: {
    		msg->add_param_ui(PyLong_AsLongLong(v));
    	} break;
    	case ParamType_Str: {
    		fprintf(stdout, "TODO: STR param\n"); break;
    	} break;
    	default: fprintf(stdout, "Unknown param\n");
    	}
    }

    Bfm::get_bfms().at(bfm_id)->send_msg(msg);

    return Py_BuildValue("");
}

/**
 * bfm_recv_msg()
 *
 * Receives a message from a BFM to pass on to Python
 */
static void bfm_recv_msg(uint32_t bfm_id, BfmMsg *msg) {
    PyGILState_STATE gstate;
    PyObject *param_l;

    gstate = TAKE_GIL();

    param_l = PyList_New(msg->num_params());
    for (uint32_t i=0; i<msg->num_params(); i++) {
    	const MsgParam *param = msg->get_param(i);
        switch (param->ptype) {
        case ParamType_Ui: {
        	PyList_SetItem(param_l, i, PyLong_FromUnsignedLongLong(param->pval.ui64));
    	} break;
    	case ParamType_Si: {
    		PyList_SetItem(param_l, i, PyLong_FromLongLong(param->pval.i64));
    	} break;
    	case ParamType_Str: {
    		PyList_SetItem(param_l, i, PyUnicode_FromString(param->pval.str));
    	}
    	}
    }

    PyObject_CallFunction(bfm_call_method, "iiO", bfm_id, msg->id(), param_l);

    DROP_GIL(gstate);

}

static PyObject *bfm_set_call_method(PyObject *self, PyObject *args) {
    PyObject *temp;

    (void)self;

    if (PyArg_ParseTuple(args, "O:callback", &temp)) {
        if (!PyCallable_Check(temp)) {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return 0;
        }
        Py_INCREF(temp);
        Py_XDECREF(bfm_call_method);
        bfm_call_method = temp;

        return Py_BuildValue("");
    } else {
        return 0;
    }
}

static PyMethodDef HdlSimMethods[] = {
	    // Note: methods for interacting with BFMs
	    {"bfm_get_count", bfm_get_count, METH_VARARGS, NULL},

		// - (typename,instname,clsname) of BFM
	    {"bfm_get_info", bfm_get_info, METH_VARARGS, NULL},

		// - Send a message to a BFM
	    {"bfm_send_msg", bfm_send_msg, METH_VARARGS, NULL},

		// - Sets the call-method function
	    {"bfm_set_call_method", bfm_set_call_method, METH_VARARGS, NULL},

		{NULL, NULL, 0, NULL}
};

static struct PyModuleDef pybfms_hdl_sim_module = {
		PyModuleDef_HEAD_INIT,
		"pybfms_core",
		"Python interface to HDL simulators for the PyBFMS library",
		-1,
		HdlSimMethods
};

PyMODINIT_FUNC PyInit_pybfms_core(void) {
	Bfm::set_recv_msg_f(&bfm_recv_msg);
	return PyModule_Create(&pybfms_hdl_sim_module);
}


