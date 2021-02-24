'''
Created on Feb 11, 2020

@author: ballance
'''
import re
import importlib
import ctypes
from pybfms.bfm_info import BfmInfo
from ctypes import cdll, c_uint, CFUNCTYPE, c_char_p, c_void_p, c_ulonglong,\
    c_longlong, c_ulong
from pybfms.bfm_type_info import BfmTypeInfo
from pybfms.bfm_method_info import MsgParamType
from enum import IntEnum
from pybfms.backend import BackendCocotb
import pybfms

class BuiltinMsgId(IntEnum):
    Init = 0x8000

RECV_MSG_FUNC_T = CFUNCTYPE(None, c_uint, c_void_p)

def recv_msg_func(bfm_id, msg):
    BfmMgr._recv_msg(bfm_id, msg)
    
recv_msg_func_p = RECV_MSG_FUNC_T(recv_msg_func)


class BfmMgr():

    _inst = None

    def __init__(self):
        from pybfms import get_libpybfms
        self.bfm_l = []
        self.bfm_type_info_m = {}
        self.m_initialized = False
        
        libpybfms_path = get_libpybfms()
        libpybfms = cdll.LoadLibrary(libpybfms_path)

        bfm_get_count = CFUNCTYPE(c_uint)
        self._get_count = bfm_get_count(("bfm_get_count", libpybfms), ())
        bfm_get_instname = CFUNCTYPE(c_char_p, c_uint)
        self._get_instname = bfm_get_instname(("bfm_get_instname", libpybfms), ((1, "bfm_id"),))
        bfm_get_clsname = CFUNCTYPE(c_char_p, c_uint)
        self._get_clsname = bfm_get_clsname(("bfm_get_clsname", libpybfms), ((1, "bfm_id"),))
        
        bfm_send_msg = CFUNCTYPE(None, c_uint, c_void_p)
        self._send_msg = bfm_send_msg(("bfm_send_msg", libpybfms), ((1, "bfm_id"), (1, "msg")))

        bfm_set_recv_msg_callback = CFUNCTYPE(None, c_void_p)
        self._set_recv_msg_callback = bfm_set_recv_msg_callback(
            ("bfm_set_recv_msg_callback", libpybfms), 
            ((1, "f"),))

        bfm_msg_new = CFUNCTYPE(c_void_p, c_uint)
        self._msg_new = bfm_msg_new(
            ("bfm_msg_new", libpybfms),
            ((1, "msg_id"),))
        bfm_msg_add_param_ui = CFUNCTYPE(None, c_void_p, c_ulonglong)
        self._msg_add_param_ui = bfm_msg_add_param_ui(
            ("bfm_msg_add_param_ui", libpybfms),
            ((1, "msg"), (1, "p")))
        bfm_msg_add_param_si = CFUNCTYPE(None, c_void_p, c_longlong)
        self._msg_add_param_si = bfm_msg_add_param_si(
            ("bfm_msg_add_param_si", libpybfms),
            ((1, "msg"), (1, "p")))
        bfm_msg_id = CFUNCTYPE(c_uint, c_void_p)
        self._msg_id = bfm_msg_id(
            ("bfm_msg_id", libpybfms),
            ((1, "msg"),))
        bfm_msg_get_param = CFUNCTYPE(c_void_p, c_void_p)
        self._msg_get_param = bfm_msg_get_param(
            ("bfm_msg_get_param", libpybfms),
            ((1, "msg"),))
        bfm_msg_param_type = CFUNCTYPE(c_uint, c_void_p)
        self._msg_param_type = bfm_msg_param_type(
            ("bfm_msg_param_type", libpybfms),
            ((1, "msg"),))
        bfm_msg_param_ui = CFUNCTYPE(c_ulonglong, c_void_p)
        self._msg_param_ui = bfm_msg_param_ui(
            ("bfm_msg_param_ui", libpybfms),
            ((1, "msg"),))
        bfm_msg_param_si = CFUNCTYPE(c_longlong, c_void_p)
        self._msg_param_si = bfm_msg_param_si(
            ("bfm_msg_param_si", libpybfms),
            ((1, "msg"),))
        

    def add_type_info(self, T, type_info):
        self.bfm_type_info_m[T] = type_info

    @staticmethod
    def get_bfms():
        inst = BfmMgr.inst()
        
        if not inst.m_initialized:
            raise Exception("PyBFMS not initialized. Must call 'await pybfms.init()'")
        
        return inst.bfm_l

    @staticmethod
    def find_bfm(path_pattern, type=None):
        inst = BfmMgr.inst()
        
        if not inst.m_initialized:
            raise Exception("PyBFMS not initialized. Must call 'await pybfms.init()'")
        
        bfm = None

        path_pattern_re = re.compile(path_pattern)

        # Find the BFM instance that matches the specified pattern
        matches = (
            b
            for b in inst.bfm_l
            if path_pattern_re.match(b.bfm_info.inst_name)
        )
       
        if type is None:
            return next(matches, None)
        else:
            for bfm in matches:
                if isinstance(bfm, type):
                    return bfm
        return None


    @staticmethod
    def inst():
        if BfmMgr._inst is None:
            BfmMgr._inst = BfmMgr()

        return BfmMgr._inst

    def _load_bfms(self):
        '''
        Obtain the list of BFMs from the native layer
        '''
        n_bfms = self._get_count()
        self.bfm_l.clear()
        for i in range(n_bfms):
            instname = self._get_instname(i).decode('utf-8')
            clsname = self._get_clsname(i).decode('utf-8')
            print("BFM: " + instname + " : " + clsname)
            try:
                pkgname, clsleaf = clsname.rsplit('.',1)
            except ValueError:
                raise Exception("Incorrectly-formatted BFM class name {!r}".format(clsname))

            try:
                pkg = importlib.import_module(pkgname)
            except Exception:
                raise Exception("Failed to import BFM package {!r}".format(pkgname))

            if not hasattr(pkg, clsleaf):
                raise Exception("Failed to find BFM class \"" + clsleaf + "\" in package \"" + pkgname + "\"")

            bfmcls = getattr(pkg, clsleaf)

            type_info = self.bfm_type_info_m[bfmcls]

            bfm = bfmcls()
            bfm_info = BfmInfo(
                bfm,
                len(self.bfm_l),
                instname,
                type_info)
            # Add
            bfm.bfm_info = bfm_info

            self.bfm_l.append(bfm)

    @staticmethod
    async def init(backend=None, force=False):
        pybfms.init_backend(backend)

        inst = BfmMgr.inst()

        if not inst.m_initialized or force:
            # Delay for a delta to allow BFMs to register
            last_count = 0
            for i in range(100):
                for j in range(2):
                    await pybfms.delta()

                this_count = inst._get_count()
                if last_count > 0 and this_count == last_count:
                    # Found at least one BFM, and no more showed up
                    break
                last_count = this_count

            if last_count == 0:
                print("Warning: PyBFMs did not detect any BFMs registering")

            inst._set_recv_msg_callback(recv_msg_func_p)
            inst._load_bfms()
            inst.m_initialized = True

            for bfm in inst.bfm_l:            
                if bfm.bfm_info.type_info.has_init:
                    # Send the initialization message
                    inst.send_msg(bfm.bfm_info.id, BuiltinMsgId.Init, [], [])
                    
                    # Give the BFM a chance to respond
                    for i in range(2):
                        await pybfms.delta()
                    
            
    @staticmethod
    def _recv_msg(bfm_id, msg):
        inst = BfmMgr.inst()
        msg_id = inst._msg_id(msg)
        
        params = []
        while True:
            p = inst._msg_get_param(msg)
            if p is None:
                break
            
            pt = inst._msg_param_type(p)
            if pt == MsgParamType.ParamType_Si:
                params.append(inst._msg_param_si(p))
            elif pt == MsgParamType.ParamType_Ui:
                params.append(inst._msg_param_ui(p))
            else:
                print("Error: unsupported parameter type " + str(pt))

        # Notify the backend so it can do any pre-execution housekeeping
#        pybfms.backend().inbound_task_call()
        inst.call(bfm_id, msg_id, params)

    def call(self, bfm_id, method_id, params):
        bfm = self.bfm_l[bfm_id]

        if not hasattr(bfm, "bfm_info"):
            raise AttributeError("BFM object does not contain 'bfm_info' field")

        bfm.bfm_info.call_method(method_id, params)
        
    def send_msg(self,
        bfm_id,
        msg_id,
        param_l,
        type_info_l):
        
        msg_p = self._msg_new(msg_id)
        
        for ti,p in zip(type_info_l, param_l):
            if ti == MsgParamType.ParamType_Ui:
                self._msg_add_param_ui(msg_p, p)
            elif ti == MsgParamType.ParamType_Si:
                self._msg_add_param_si(msg_p, p)
            else:
                raise Exception("unsupported message parameter type " + str(ti))

        self._send_msg(bfm_id, msg_p)

    
