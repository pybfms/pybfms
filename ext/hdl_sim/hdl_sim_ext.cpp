#include <Python.h>

static PyMethodDef HdlSimMethods[] = {
		{NULL, NULL, 0, NULL}
};

static struct PyModuleDef hdl_sim_module = {
		PyModuleDef_HEAD_INIT,
		"hdl_sim",
		"Python interface to HDL simulators for the PyBFMS library",
		-1,
		HdlSimMethods
};

PyMODINIT_FUNC PyInit_hdl_sim(void) {
	return PyModule_Create(&hdl_sim_module);
}


