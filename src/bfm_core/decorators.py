'''
Created on Oct 9, 2019

@author: ballance
'''
from enum import Enum, auto

from bfm_core.bfm_type_info import BfmTypeInfo


class HdlType(Enum):
    '''
    
    '''
    Verilog = auto()
    
class AbsLevel(Enum):
    '''
    '''
    Signal = auto()

class bfm():
    
    def __init__(self, bfm_hdl):
        self.bfm_hdl = bfm_hdl
        
    def __call__(self, T):
        BfmTypeInfo.register_bfm(BfmTypeInfo(T, self.bfm_hdl))
        return T


