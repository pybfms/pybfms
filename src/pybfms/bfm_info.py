'''
Created on Feb 11, 2020

@author: ballance
'''

class BfmInfo():

    def __init__(self, bfm, id, inst_name, type_info):
        self.bfm = bfm
        self.id = id
        self.inst_name = inst_name
        self.type_info = type_info

    def call_method(self, method_id, params):
        self.type_info.export_info[method_id].T(
            self.bfm, *params)
