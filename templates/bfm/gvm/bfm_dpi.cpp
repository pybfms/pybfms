/****************************************************************************
 * ${bfm}_dpi.cpp
 ****************************************************************************/
#include "${bfm}.h"

uint32_t ${bfm}_register(const char *path) {
	return ${bfm}_t::register_bfm(path);
}

${bfm_dpi_imports}

${bfm}_t					${bfm}_type;

