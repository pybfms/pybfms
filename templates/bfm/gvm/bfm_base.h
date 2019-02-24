/****************************************************************************
 * ${bfm}_base.h
 *
 ****************************************************************************/
#pragma once
#include <stdint.h>
#include "${bfm}_rsp_if.h"
#include "GvmBfm.h"

class ${bfm}_base : public GvmBfm<${bfm}_rsp_if> {
public:

	${bfm}_base(${bfm}_rsp_if *rsp_if=0);

	virtual ~${bfm}_base();

${bfm_dpi_export_method_decl}


};

