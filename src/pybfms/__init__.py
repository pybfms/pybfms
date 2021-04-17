
from enum import Enum, auto
import os
import sys
from typing import List

from pybfms.backend import BackendCocotb, Backend
from pybfms.decorators import *
from pybfms.types import *

from .objection import objection


def init_backend(backend=None):
    
    if backend is None:
        # Only set the backend if if hasn't already been set
        if Backend.inst() is None:
            Backend.set_inst(BackendCocotb())
    else:
        Backend.set_inst(backend)

    
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

async def init(backend=None, force=False):
    await BfmMgr.init()
    
def find_bfm(pattern, type=None):
    return BfmMgr.find_bfm(pattern, type)

def get_bfms() -> List:
    return BfmMgr.get_bfms()

def find_bfms(pattern, type=None) -> List:
    return BfmMgr.find_bfms(pattern, type)

def event():
    """
    Returns an event object for synchronization
    """
    return Backend.inst().event()

def delay(time_ps, units=None):
    """
    Returns an awaitable object to delay for a period of simulation time
    """
    return Backend.inst().delay(time_ps, units)

def delta():
    return Backend.inst().delta()

def fork(coro):
    """Forks a new co-routine"""
    return Backend.inst().fork(coro)

def lock():
    return Backend.inst().lock()

def backend():
    return Backend.inst()
    
    
    
