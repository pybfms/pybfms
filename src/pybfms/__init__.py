
import os
from pybfms.decorators import *
from pybfms.types import *
import os
import sys

from enum import Enum, auto
from pybfms.backend import BackendCocotb

_backend = None

def init_backend(backend=None):
    global _backend
    
    if backend is None:
        # Only set the backend if if hasn't already been set
        if _backend is None:
            _backend = BackendCocotb()
    else:
        _backend = backend

    
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
    
def find_bfm(pattern):
    return BfmMgr.find_bfm(pattern)

def event():
    """
    Returns an event object for synchronization
    """
    return _backend.event()

def delay(time_ps, units=None):
    """
    Returns an awaitable object to delay for a period of simulation time
    """
    return _backend.delay(time_ps, units)

def delta():
    return _backend.delta()

def lock():
    return _backend.lock()
    
    
    
