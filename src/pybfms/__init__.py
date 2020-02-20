
import os
from pybfms.decorators import *
from pybfms.types import *
import os
import sys

from enum import Enum, auto

def bfm_hdl_path(py_file, template):
    return os.path.join(
        os.path.dirname(os.path.abspath(py_file)),
        template)


class BfmType(Enum):
    Verilog = auto
    SystemVerilog = auto
    
def get_libpybfms():
    """Return the path to the VPI library"""
    libpath = None
    for p in sys.path:
        if os.path.exists(os.path.join(p, "libpybfms.so")):
            libpath = os.path.join(p, "libpybfms.so")
            break
        
    if libpath is None:
        raise Exception("Failed to locate libpybfms.so on the PYTHONPATH")
    
    return libpath
    
    
