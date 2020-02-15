'''
Created on Feb 11, 2020

@author: ballance
'''
import argparse
from pybfms.bfmgen import bfm_generate

def lib(args):
    """Return the path to the VPI library"""
    import pybfms_hdl_sim
    print(pybfms_hdl_sim.__file__)
    

def get_parser():
    parser = argparse.ArgumentParser(prog="pybfms")

    subparser = parser.add_subparsers()
    subparser.required = True
    subparser.dest = 'command'
    vpi_lib_cmd = subparser.add_parser("lib")
    vpi_lib_cmd.set_defaults(func=lib)
    vpi_lib_cmd.add_argument("-v", "--vpi", action="store_const", const="vpi")
    
    generate_cmd = subparser.add_parser("generate")
    generate_cmd.set_defaults(func=bfm_generate)
    generate_cmd.add_argument("-m", action='append')
    generate_cmd.add_argument("-l", "--language", default="vlog")
    generate_cmd.add_argument("-o", default=None)
    
    return parser
   
def main():
    """pybfms main command"""
    parser = get_parser() 
    
    args = parser.parse_args() 

    args.func(args)

if __name__ == "__main__":
    main()
