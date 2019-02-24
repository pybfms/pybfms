/****************************************************************************
 * ${bfm}_dpi.cpp
 *
 * Warning: This file is generated and should not be hand modified
 ****************************************************************************/
#include "${bfm}.h"

/********************************************************************
 * ${bfm}_register()
 *
 ********************************************************************/
extern "C" uint32_t ${bfm}_register(const char *path) {
	return ${bfm}_t::register_bfm(path);
}

${bfm_dpi_imports}

${bfm}_t					${bfm}_type;

