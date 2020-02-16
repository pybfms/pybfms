
import cocotb
from cocotb.triggers import Timer

import pybfms

@cocotb.test()
def runtest(dut):
    print("Hello from Python")
    yield Timer(0)
    pybfms.BfmMgr.init()
    bfm = pybfms.BfmMgr.find_bfm(".*bfm_0")
    print("bfm=" + str(bfm))
    bfm.hdl_task(5)