
import os

import_info_l = []
from enum import Enum, auto
export_info_l = []

def register_bfm_import_info(info):
    info.id = len(import_info_l)
    import_info_l.append(info)

def register_bfm_export_info(info):
    info.id = len(export_info_l)
    export_info_l.append(info)

def bfm_hdl_path(py_file, template):
    return os.path.join(
        os.path.dirname(os.path.abspath(py_file)),
        template)


class BfmType(Enum):
    Verilog = auto
    SystemVerilog = auto
