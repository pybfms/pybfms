'''
Created on Feb 22, 2020

@author: ballance
'''

class Backend():
    
    def event(self):
        raise Exception("Backend.event() unimplemented")
    
    def delay(self, time_ps, units=None):
        raise Exception("Backend.delay() unimplemented")
    
    def delta(self):
        raise Exception("Backend.delta() unimplemented")
        
    def lock(self):
        raise Exception("Backend.lock() unimplemented")
    
class BackendCocotb(Backend):
    
    def event(self):
        from cocotb.triggers import Event
        return Event()
    
    def delay(self, time_ps, units=None):
        from cocotb.triggers import Timer
        return Timer(time_ps, units)
    
    def delta(self):
        return self.delay(0)
        
    def lock(self):
        from cocotb.triggers import Lock
        return Lock()
    
    
        