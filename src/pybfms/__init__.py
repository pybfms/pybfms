
import os
from pybfms.decorators import *
from pybfms.types import *

from enum import Enum, auto

def bfm_hdl_path(py_file, template):
    return os.path.join(
        os.path.dirname(os.path.abspath(py_file)),
        template)


class BfmType(Enum):
    Verilog = auto
    SystemVerilog = auto
    
