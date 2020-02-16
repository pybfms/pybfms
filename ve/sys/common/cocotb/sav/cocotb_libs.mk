
COCOTB_SHARE_DIR:=$(shell cocotb-config --share)
export COCOTB_SHARE_DIR

all-libs : cocotb-libs cocotb-vpi-libs cocotb-vhpi-libs

# Default to Icarus if no simulator defined
SIM ?= icarus

USER_DIR ?= $(shell pwd)
export USER_DIR

vpi-libs : cocotb-libs cocotb-vpi-libs


include $(COCOTB_SHARE_DIR)/lib/Makefile

cocotb-libs : $(COCOTB_LIBS)

cocotb-vpi-libs : $(COCOTB_VPI_LIB)

cocotb-vhpi-libs : $(COCOTB_VHPI_LIB)

cocotb-fli-libs : $(COCOTB_FLI_LIB)

