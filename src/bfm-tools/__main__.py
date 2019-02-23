
import argparse
from string import Template

#********************************************************************
#* gen_ifc()
#*
#* - gvm/<name>_base.cpp, <name>_base.h, <name>_rsp_if.h
#* - <name>_api_pkg.sv -- API to communicate BFM->UVM
#* - <name>_api.svh -- BFM API implementations
#********************************************************************
def gen_ifc(args):
    print("gen_ifc")

#********************************************************************
#* main()
#********************************************************************
def main():
    
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="subcmd")
    
    gen_bfm = subparser.add_argument("gen-ifc")
    gen_bfm.add_argument("-o", help="output directory")
    gen_bfm.add_argument("file", help="BFM Interface definition")
    
    args = parser.parse_args()

    if args.subcmd == "gen_ifc":
        gen_ifc(args)
    else:
        print("Error: unknown sub-command")
       

if name == "__main__":
    main()
    