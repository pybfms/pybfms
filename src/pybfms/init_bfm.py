'''
Created on Dec 22, 2020

@author: mballance
'''

import os

def init_bfm(args):
    global bfm_py_template
    global bfm_v_template
    bfmname = args.classname
    hdlname = ""
    
    package = None
   
    if package is None:
        if os.path.isdir("src"):
            for d in os.listdir("src"):
                print("d=" + str(d))
                if os.path.isdir(os.path.join("src", d)) and d != "." and d != "..":
                    package = d
                    break
        else:
            raise Exception("No 'src' directory")
        
    # Replace non-initial capital letters
    # with the lower-case version and an underscore
   
    for i,c in enumerate(bfmname):
        if i == 0:
            hdlname += c.lower()
        elif c.isupper():
            hdlname += "_" + c.lower()
        else:
            hdlname += c
            
    print("Classname: " + bfmname + " hdl: " + hdlname)
    
    print("package=" + str(package))
    
    os.makedirs(os.path.join("src", package), exist_ok=True)
    os.makedirs(os.path.join("src", package, "hdl"), exist_ok=True)

    with open(os.path.join("src", package, bfmname + ".py"), "w") as fp:
        fp.write(bfm_py_template % (hdlname,hdlname,bfmname))
                 
    with open(os.path.join("src", package, "hdl", hdlname + ".v"), "w") as fp:
        fp.write(bfm_v_template % (hdlname,hdlname,hdlname))
                 
    pass


bfm_py_template = """
import pybfms

@pybfms.bfm(hdl={
    pybfms.BfmType.Verilog : pybfms.bfm_hdl_path(__file__, "hdl/%s.v"),
    pybfms.BfmType.SystemVerilog : pybfms.bfm_hdl_path(__file__, "hdl/%s.v"),
    }, has_init=True)
class %s():

    def __init__(self):
        self.busy = pybfms.lock()
        self.is_reset = False
        self.reset_ev = pybfms.event()
        pass
        
    @pybfms.export_task()
    def _set_praameters(self):
        pass
        
    @pybfms.export_task()
    def _reset(self):
        self.is_reset = True
        self.reset_ev.set()
        
        
"""

bfm_v_template = """
/****************************************************************************
 * %s.v
 * 
 ****************************************************************************/

module %s #(
        ) (
        input                            clock,
        input                            reset
        );
        
    reg            in_reset = 0;
    
    always @(posedge clock or posedge reset) begin
        if (reset) begin
            in_reset <= 1;
        end else begin
            if (in_reset) begin
                _reset();
                in_reset <= 1'b0;
            end
        end
    end
        
    task init;
    begin
        $display("%s: %%m");
        // TODO: pass parameter values
        _set_parameters();
    end
    endtask
	
    // Auto-generated code to implement the BFM API
`ifdef PYBFMS_GEN
${pybfms_api_impl}
`endif

endmodule
"""
