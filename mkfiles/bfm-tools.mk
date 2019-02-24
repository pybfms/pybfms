
BFM_TOOLS_MKFILES_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

ifneq (1,$(BFM_TOOLS_MKFILES_DIR))

BFM_TOOLS := $(abspath $(BFM_TOOLS_MKFILES_DIR)/..)
export BFM_TOOLS

BFM_TOOLS_GEN_FILES = $(1)/$(2)_api_pkg.sv $(1)/$(2)_api.svh $(1)/gvm/$(2)_bfm_base.h $(1)/gvm/$(2)_bfm_base.cpp $(1)/gvm/$(2)_rsp_if.h $(1)/gvm/$(2)_dpi.cpp

else # Rules

endif
