'''
Created on Feb 11, 2020

@author: ballance
'''
import argparse
import os
import sys
from pybfms.bfmgen import bfm_generate
from pybfms import get_libpybfms
from pybfms.project import init_project
from pybfms.init_bfm import init_bfm

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
    
    init_bfm_cmd = subparser.add_parser("init_bfm",
        help="Create the outline of a BFM")
    init_bfm_cmd.add_argument("classname",
        help="Specifies the class name of the BFM")
    init_bfm_cmd.add_argument("-f","--force", action='store_true',
        help="Force overwrite of existing files")
    init_bfm_cmd.add_argument("-package",
        help="Specifies the package name")
    init_bfm_cmd.set_defaults(func=init_bfm)
    
    init_project_cmd = subparser.add_parser("init_project",
        help="Initialize a PyBFMS project with setup.py, etc")
    init_project_cmd.add_argument("name",
        help="Specifies the name of the project")
    init_project_cmd.add_argument("package",
        help="Specifies the name of the Python package")
    init_project_cmd.add_argument("-f","--force", action='store_true',
        help="Force overwrite of existing files")
    init_project_cmd.set_defaults(func=init_project)
    
    return parser
   
def main():
    """pybfms main command"""
    parser = get_parser() 
    
    args = parser.parse_args() 

    args.func(args)

if __name__ == "__main__":
    main()
