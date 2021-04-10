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
    
    async def inbound_task_call(self):
        """Called when a request is received to call an exported task"""
        raise Exception("Backend.inbound_task_call() unimplemented")
    
    def fork(self, c):
        raise Exception("Backend.fork() unimplemented")
    
    async def join(self, t):
        raise Exception("Backend.join() unimplemented")
        
    
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
    
    async def inbound_task_call(self):
        """Called when a request is received to call an exported task"""
        from cocotb.triggers import Timer
        await Timer(0, units="ps")
        
    def fork(self, c):
        import cocotb
        return cocotb.fork(c)
    
    def join(self, t):
        from cocotb.triggers import Join
        return Join(t)
