'''
Created on Feb 11, 2020

@author: ballance
'''
from pybfms.bfm_mgr import BfmMgr
import pybfms
from pybfms.bfm_method_info import BfmMethodInfo
from pybfms.bfm_type_info import BfmTypeInfo

# Collects information about BFM import and export tasks
_import_info_l = []
_export_info_l = []

class bfm():
    '''
    Decorator to identify a BFM type.
    '''
    def __init__(self, hdl, has_init=False):
        self.hdl = hdl
        self.has_init = has_init
        print("bfm decorator")

    def __call__(self, T):
        global _import_info_l, _export_info_l
        type_info = BfmTypeInfo(T, self.hdl, 
            _import_info_l.copy(), _export_info_l.copy())
        BfmMgr.inst().add_type_info(T, type_info)
        _import_info_l.clear()
        _export_info_l.clear()
        
        return T

class export_task():

    def __init__(self, *args):
        self.signature = args

    def __call__(self, m):
        global _export_info_l
        info = BfmMethodInfo(m, self.signature)
        info.id = len(_export_info_l)
        _export_info_l.append(info)
        return m

class import_task():
    '''
    Method that is being imported from the HDL environment
    '''

    def __init__(self, *args):
        self.signature = args

    def __call__(self, m):
        global _import_info_l
        info = BfmMethodInfo(m, self.signature)
        info.id = len(_import_info_l)
        _import_info_l.append(info)
        
        def import_taskw(self, *args):
            arg_l = []
            for a in args:
                arg_l.append(a)
            BfmMgr.inst().send_msg(
                self.bfm_info.id,
                info.id,
                arg_l,
                info.type_info)

        return import_taskw

