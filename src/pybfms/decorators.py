'''
Created on Feb 11, 2020

@author: ballance
'''
from pybfms.bfm_mgr import BfmMgr
import os
from enum import Enum, auto
from pybfms.bfm_method_info import BfmMethodInfo
from pybfms.bfm_type_info import BfmTypeInfo

# Collects information about BFM import and export tasks
_import_info_l = []
_export_info_l = []

def bfm_hdl_path(py_file, template):
    """
    Returns the path to a BFM template located relative to the Python BFM file
    """
    return os.path.join(
        os.path.dirname(os.path.abspath(py_file)),
        template)

class BfmType(Enum):
    """
    Specifies BFM implementation language and interface
    """
    
    Verilog = auto() 
    """Verilog BFM interfaced via VPI"""
    
    SystemVerilog = auto() 
    """ SystemVerilog BFM interfaced via DPI"""

class bfm():
    '''
    Decorator to identify a BFM type.
    '''
    def __init__(self, hdl, has_init=False):
        """
        Parameters
        ----------
        hdl : dict of :class:`~pybfms.decorators.BfmType` : path
              Provides information about the HDL source that
              implements the BFM for various HDL languages
              
        has_init : bool
              Specifies whether this BFM has an `init` task.
              
        """
        self.hdl = hdl
        self.has_init = has_init

    def __call__(self, T):
        global _import_info_l, _export_info_l
        type_info = BfmTypeInfo(T, self.hdl, self.has_init,
            _import_info_l.copy(), _export_info_l.copy())
        BfmMgr.inst().add_type_info(T, type_info)
        _import_info_l.clear()
        _export_info_l.clear()
        
        return T

class export_task():
    """
    Identifies a BFM-class method that can be called from the HDL
    """

    def __init__(self, *args):
        """
        Parameters
        ----------
        args : list of data types
               Specifies the signature of the 
        """
        self.signature = args

    def __call__(self, m):
        global _export_info_l
        info = BfmMethodInfo(m, self.signature)
        info.id = len(_export_info_l)
        _export_info_l.append(info)
        return m

class import_task():
    '''
    Identifies a BFM-class method implemented in the HDL
    '''

    def __init__(self, *args):
        """
        Parameters
        ----------
        args : list of data types
               Specifies the signature of the 
        """
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

