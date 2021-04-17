'''
Created on Apr 16, 2021

@author: mballance
'''

from .backend import Backend

class objection(object):
    
    _inst = None
    
    def __init__(self):
        self.count = 0
        self.event_cb = []
        pass
    
    def add_event_cb(self, cb):
        self.event_cb.append(cb)
        
    def del_event_cb(self, cb):
        self.event_cb.remove(cb)
    
    async def wait(self):
        """Wait for all objections to be dropped"""

        if self.count > 0:        
            ev = Backend.inst().event()
        
            def cb(obj):
                nonlocal ev
                if obj.count == 0:
                    ev.set()
                
            self.add_event_cb(cb)
            await ev.wait()
            self.del_event_cb(cb)
    
    def raise_objection(self, count=1):
        self.count += count
        if len(self.event_cb) > 0:
            for cb in self.event_cb.copy():
                cb(self)
                
    def drop_objection(self, count=1):
        if self.count >= count:
            self.count -= count
        else:
            self.count = 0
        if len(self.event_cb) > 0:
            for cb in self.event_cb.copy():
                cb(self)
    
    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = cls()
        return cls._inst
        