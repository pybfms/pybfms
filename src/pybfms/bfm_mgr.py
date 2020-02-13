'''
Created on Feb 11, 2020

@author: ballance
'''
import re
import importlib
from pybfms.bfm_info import BfmInfo

class BfmMgr():

    _inst = None

    def __init__(self):
        self.bfm_l = []
        self.bfm_type_info_m = {}
        self.m_initialized = False

    def add_type_info(self, T, type_info):
        self.bfm_type_info_m[T] = type_info

    @staticmethod
    def get_bfms():
        return BfmMgr.inst().bfm_l

    @staticmethod
    def find_bfm(path_pattern):
        inst = BfmMgr.inst()
        bfm = None

        path_pattern_re = re.compile(path_pattern)

        # Find the BFM instance that matches the specified pattern
        matches = (
            b
            for b in inst.bfm_l
            if path_pattern_re.match(b.bfm_info.inst_name)
        )

        return next(matches, None)

    @staticmethod
    def inst():
        if BfmMgr._inst is None:
            BfmMgr._inst = BfmMgr()

        return BfmMgr._inst

    def load_bfms(self):
        '''
        Obtain the list of BFMs from the native layer
        '''
        import simulator
        n_bfms = simulator.bfm_get_count()
        for i in range(n_bfms):
            info = simulator.bfm_get_info(i)
            instname = info[0]
            clsname = info[1]
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
            setattr(bfm, "bfm_info", bfm_info)

            self.bfm_l.append(bfm)

    @staticmethod
    async def init():
        import pybfms.hdl_sim
        inst = BfmMgr.inst()
        if not inst.m_initialized:
            print("TODO: fetch BFMs")
#            simulator.bfm_set_call_method(BfmMgr.call)
            BfmMgr.inst().load_bfms()
            inst.m_initialized = True

    @staticmethod
    def call(
            bfm_id,
            method_id,
            params):
        inst = BfmMgr.inst()
        bfm = inst.bfm_l[bfm_id]

        if not hasattr(bfm, "bfm_info"):
            raise AttributeError("BFM object does not contain 'bfm_info' field")

        bfm.bfm_info.call_method(method_id, params)
