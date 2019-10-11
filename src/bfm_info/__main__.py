'''
Created on Oct 10, 2019

@author: ballance
'''
import argparse
import importlib
import sys

from bfm_core.bfm_type_info import BfmTypeInfo
from bfm_core.decorators import bfm, HdlType, AbsLevel
from distutils.command.config import LANG_EXT


def add_paths(path_l):
    if path_l is None:
        return
    
    for p in path_l:
        sys.path.append(p)

def load_modules(module_l):
    if module_l is None:
        return
    
    for m in module_l:
        try:
            importlib.import_module(m)
        except Exception as e:
            print("Error: failed to load module \"" + m + "\"")
            exit(1)
            
def get_language(lang):
    lang_m = {
        "verilog": HdlType.Verilog
    }

    if lang in lang_m.keys():
        return lang_m[lang]
    else:
        print("Error: unsupported language \"" + lang + "\": " + str(lang_m.keys()))
        exit(1)
        
def get_type(t):
    type_m = {
        "signal": AbsLevel.Signal
    }
    
    if t in type_m.keys():
        return type_m[t]
    else:
        print("Error: unsupported type \"" + t + "\": " + str(type_m.keys()))
        exit(1)

def get_files(lang, t):
    file_m = {}
    
    lang_t = get_language(lang)
    type_t = get_type(t)
    
    for bfm in BfmTypeInfo.registered_bfm_info:
        if not lang_t in bfm.bfm_hdl.keys():
            print("Error: BFM \"" + str(bfm.T) + "\" does not support language \"" + lang + "\"")
            exit(1)
        else:
            file_l = []
            lang_info = bfm.bfm_hdl[lang_t]
            if type_t not in lang_info.keys():
                print("Error: BFM \"" + str(bfm.T) + "\" does not support type \"" + t + "\"")
            else:
                file_l.append(lang_info[type_t])
            file_m[bfm] = file_l
                
    return file_m

def cmd_srcpaths(args):
    add_paths(args.l)
    load_modules(args.m)
  
    file_m = get_files(args.language, args.type) 

    result = ""    
    for bfm in file_m.keys():
        file_l = file_m[bfm]
        
        for f in file_l:
            result += f 
            result += " "
        
    
    print(result)
        
    pass

def cmd_filelist(args):
    add_paths(args.l)
    load_modules(args.m)
  
    file_m = get_files(args.language, args.type) 

    fp = open(args.o, "w")
    for bfm in file_m.keys():
        fp.write("// Files for BFM: " + str(bfm.T) + "\n")
        
        file_l = file_m[bfm]
        
        for f in file_l:
            fp.write(f + "\n")
              
        fp.write("\n")
            
    fp.close()

def main():
    '''
    - srcpaths -language [lang] -type [signal]
    - filelist
    '''
    
    parser = argparse.ArgumentParser("bfm_info")
    cmdparser = parser.add_subparsers()
    
    paths = cmdparser.add_parser("srcpaths")
    paths.set_defaults(func=cmd_srcpaths)
    paths.add_argument("-language", required=True, choices={"verilog"})
    paths.add_argument("-type", required=True, choices={"signal"})
    paths.add_argument("-m", action="append")
    paths.add_argument("-l", action="append")
    filelist = cmdparser.add_parser("filelist")
    filelist.set_defaults(func=cmd_filelist)
    filelist.add_argument("-language", required=True, choices={"verilog"})
    filelist.add_argument("-type", required=True, choices={"signal"})
    filelist.add_argument("-o", default="bfm_files.f")
    filelist.add_argument("-m", action="append")
    filelist.add_argument("-l", action="append")
    
    args = parser.parse_args()

    if not hasattr(args, "func"):
        print("Error: no subcommand provided")
        exit(1)

    args.func(args)
            
    pass

if __name__ == "__main__":
    main()