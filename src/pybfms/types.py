'''
Created on Feb 11, 2020

@author: ballance
'''

class bfm_param_int_t():

    sv_type_m = {
        8 : "byte",
        16 : "short",
        32 : "int",
        64 : "longint"
    }

    def __init__(self, w, s):
        self.w = w
        self.s = s

    def sv_type(self):
        if self.w in bfm_param_int_t.sv_type_m.keys():
            ret = bfm_param_int_t.sv_type_m[self.w]
            if not self.s:
                ret += " unsigned"
            return ret
        else:
            raise Exception("parameter-width \"" + str(self.w) + "\" not supported by SystemVerilog")

    def vl_type(self):
        ret = "reg"
        if self.s:
            ret += " signed"
        ret += "[" + str(self.w) + "-1:0]"

        return ret

# Constants for use in specifying BFM API signatures
int8_t = bfm_param_int_t(8, True)
uint8_t = bfm_param_int_t(8, False)
int16_t = bfm_param_int_t(16, True)
uint16_t = bfm_param_int_t(16, False)
int32_t = bfm_param_int_t(32, True)
uint32_t = bfm_param_int_t(32, False)
int64_t = bfm_param_int_t(64, True)
uint64_t = bfm_param_int_t(64, False)

