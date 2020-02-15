#include <Python.h>

static PyMethodDef HdlSimMethods[] = {
		{NULL, NULL, 0, NULL}
};

static struct PyModuleDef pybfms_hdl_sim_module = {
		PyModuleDef_HEAD_INIT,
		"pybfms_hdl_sim",
		"Python interface to HDL simulators for the PyBFMS library",
		-1,
		HdlSimMethods
};

PyMODINIT_FUNC PyInit_pybfms_hdl_sim(void) {
	return PyModule_Create(&pybfms_hdl_sim_module);
}


