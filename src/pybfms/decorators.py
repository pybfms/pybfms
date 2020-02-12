'''
Created on Feb 11, 2020

@author: ballance
'''
from bfm_core.bfm_type_info import BfmTypeInfo
from pybfms.bfm_mgr import BfmMgr


class bfm():
    '''
    Decorator to identify a BFM type.
    '''
    def __init__(self, hdl, has_init=False):
        self.hdl = hdl
        self.has_init = has_init

    def __call__(self, T):
        global import_info_l
        global export_info_l

        type_info = BfmTypeInfo(
            T, self.hdl, 
            import_info_l.copy(), 
            export_info_l.copy())
        BfmMgr.inst().add_type_info(T, type_info)
        import_info_l = []
        export_info_l = []
        
        return T

class export_task():

    def __init__(self, *args):
        self.signature = args

    def __call__(self, m):
        cocotb.bfms.register_bfm_export_info(
            cocotb.bfms.BfmMethodInfo(m, self.signature))
        return m

class import_task():
    '''
    Method that is being imported from the HDL environment
    '''

    def __init__(self, *args):
        self.signature = args

    def __call__(self, m):
        info = BfmMethodInfo(m, self.signature)
        cocotb.bfms.register_bfm_import_info(info)

        def import_taskw(self, *args):
            import simulator
            arg_l = []
            for a in args:
                arg_l.append(a)
            simulator.bfm_send_msg(
                self.bfm_info.id,
                info.id,
                arg_l,
                info.type_info)

        return import_taskw

