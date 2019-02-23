/****************************************************************************
 * ${bfm}_base.h
 *
 ****************************************************************************/
#pragma once

#include "${bfm}_rsp_if.h"
#include "GvmBfm.h"

class ${bfm}_base : public GvmBfm<${bfm}_rsp_if> {
public:

${bfm_dpi_export_method_decl}


};

