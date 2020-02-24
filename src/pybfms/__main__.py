'''
Created on Feb 11, 2020

@author: ballance
'''
import argparse
import os
import sys
from pybfms.bfmgen import bfm_generate
from pybfms import get_libpybfms

def lib(args):
    libpath = get_libpybfms()

    print(libpath)
    

def get_parser():
    parser = argparse.ArgumentParser(prog="pybfms")

    subparser = parser.add_subparsers()
    subparser.required = True
    subparser.dest = 'command'
    vpi_lib_cmd = subparser.add_parser("lib", 
        help="Returns library-path information")
    vpi_lib_cmd.set_defaults(func=lib)
    vpi_lib_cmd.add_argument("--vpi", action="store_const", const="vpi",
        help="Return information about the Verilog VPI library")
    vpi_lib_cmd.add_argument("--dpi", action="store_const", const="dpi",
        help="Return information about the SystemVerilog DPI library")
    
    generate_cmd = subparser.add_parser("generate",
        help="Generates HDL source for selected BFMs")
    generate_cmd.set_defaults(func=bfm_generate)
    generate_cmd.add_argument("-m", action='append',
        help="Specifies a Python module in which to find BFMs")
    generate_cmd.add_argument("-l", "--language", default="vlog",
        choices=["vlog", "sv", "vhdl"],
        help="Specifies the desired output language")
    generate_cmd.add_argument("-o", default=None,
        help="Output filename")
    
    return parser
   
def main():
    """pybfms main command"""
    parser = get_parser() 
    
    args = parser.parse_args() 

    args.func(args)

if __name__ == "__main__":
    main()
