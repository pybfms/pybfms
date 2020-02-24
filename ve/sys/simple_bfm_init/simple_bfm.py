
import pybfms

@pybfms.bfm(hdl={
    pybfms.BfmType.Verilog : pybfms.bfm_hdl_path(__file__, "hdl/simple_bfm.sv"),
    pybfms.BfmType.SystemVerilog : pybfms.bfm_hdl_path(__file__, "hdl/simple_bfm.sv")
    }, has_init=True)
class SimpleBFM():
    
    def __init__(self):
        print("Hello from init")
        self.py_task_calls = 0
        pass
    
    @pybfms.import_task(pybfms.uint32_t)
    def hdl_task(self, val):
        pass

    @pybfms.export_task(pybfms.uint32_t)
    def py_task(self, val):
        print("py_task: " + str(val))
        self.py_task_calls += 1
        
    @pybfms.export_task(pybfms.uint32_t)
    def set_parameters(self, P):
        print("set_parameters: P=" + str(P))
    
    
    
