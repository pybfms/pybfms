'''
Created on Feb 15, 2020

@author: ballance
'''
from pybfms.bfm_method_param_info import BfmMethodParamInfo
from pybfms.types import bfm_param_int_t
from enum import IntEnum, auto

class MsgParamType(IntEnum):
    ParamType_Str = 0
    ParamType_Si = auto()
    ParamType_Ui = auto()
    
class BfmMethodInfo():
    '''
    Information about a single BFM method
    - Method type
    - User-specified parameter signature
    '''

    def __init__(self, T, signature):
        fullname = T.__qualname__
        fi = T.__code__

        self.T = T
        self.signature = []
        self.type_info = []
        self.id = -1

        locals_idx = fullname.find("<locals>")
        if locals_idx != -1:
            fullname = fullname[locals_idx+len("<locals>."):]

        if fullname.find('.') == -1:
            raise Exception("Attempting to register a global method as a BFM method")

        args = fi.co_varnames[1:fi.co_argcount]
        if len(signature) != len(args):
            raise Exception("Wrong number of parameter-type elements: expect " + str(len(args)) + " but received " + str(len(signature)))


        for a,t in zip(args, signature):
            self.signature.append(BfmMethodParamInfo(a, t))
            if isinstance(t, bfm_param_int_t):
                if t.s:
                    self.type_info.append(MsgParamType.ParamType_Si)
                else:
                    self.type_info.append(MsgParamType.ParamType_Ui)

                        