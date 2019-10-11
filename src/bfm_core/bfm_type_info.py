'''
Created on Oct 10, 2019

@author: ballance
'''

class BfmTypeInfo():
    
    registered_bfm_info = []
    
    def __init__(self, T, bfm_hdl):
        self.T = T
        self.bfm_hdl = bfm_hdl
        
#         for lang in self.bfm_hdl.keys():
#             print("--> Lang: " + str(lang))
#             for level in self.bfm_hdl[lang].keys():
#                 print("  -- Level: " + str(level))
#             print("<-- Lang: " + str(lang))
#         
    @staticmethod
    def register_bfm(info):
        BfmTypeInfo.registered_bfm_info.append(info)
        
        
        