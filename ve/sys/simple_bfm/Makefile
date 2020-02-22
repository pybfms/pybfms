
SIMPLE_BFM_DIR:=$(abspath $(dir $(lastword $(MAKEFILE_LIST))))
VE_SYS_DIR:=$(abspath $(SIMPLE_BFM_DIR)/..)
PYBFMS_DIR:=$(abspath $(VE_SYS_DIR)/../..)

PYTHONPATH:=$(PYBFMS_DIR)/src:$(SIMPLE_BFM_DIR)/build/lib.linux-x86_64-3.6:$(PYTHONPATH) 
#PYTHONPATH:=$(PYBFMS_DIR)/src:$(SIMPLE_BFM_DIR)/build:$(PYTHONPATH) 
export PYTHONPATH

# TODO: Icarus Specific
SIM_FLAGS += -m $(shell python3 -m pybfms lib --vpi)

ifeq ($(SIM),verilator)
  COMPILE_ARGS += -Wno-fatal
endif


TOPLEVEL_LANG ?= verilog

ifneq ($(TOPLEVEL_LANG),verilog)

all :
	@echo "Skipping test due to TOPLEVEL_LANG=$(TOPLEVEL_LANG) not being verilog"

clean::
	
else

COCOTB:=$(shell cocotb-config --share)

VERILOG_SOURCES = simple_bfm_top.sv pybfms.v
TOPLEVEL=simple_bfm_top

MODULE=simple_bfm_test

all : prereqs
	$(MAKE) $(COCOTB_RESULTS_FILE)

prereqs :
	python3 $(PYBFMS_DIR)/setup.py build_ext
	python3 -m pybfms generate -l vlog -m simple_bfm

clean::
	@rm -rf pybfms.*


include $(COCOTB)/makefiles/Makefile.inc
include $(VE_SYS_DIR)/common/cocotb/Makefile.sim

endif


