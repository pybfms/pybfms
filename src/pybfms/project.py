'''
Created on Dec 22, 2020

@author: mballance
'''

import os.path

def init_project(args):
    force = args.force
    name = args.name
    package = args.package
    
    if os.path.isfile("requirements.txt") and not force:
        raise Exception("requirements.txt exists")
    
    with open("requirements.txt", "w") as fp:
        fp.write(
"""
cocotb
pybfms
""")

    if os.path.isfile("setup.py") and not force:
        raise Exception("setup.py exists")
    
    with open("setup.py", "w") as fp:
        fp.write(
"""
import os

import sys, os.path, platform, warnings

from distutils import log
from distutils.core import setup, Command

VERSION = "0.0.1"
AUTHOR = "Author TBD"
AUTOR_EMAIL = "Author Email TBD"
DESCRIPTION = "Description TBD"
LICENSE = "Apache 2.0"
URL = "https://github.com/TBD"

if os.path.exists("etc/ivpm.info"):
    with open("etc/ivpm.info") as fp:
        for line in fp:
            if line.find("version=") != -1:
                VERSION = line[line.find("=")+1:].strip()
                break

if VERSION is None:
    raise Exception("Error: null version")

if "BUILD_NUM" in os.environ:
    VERSION += "." + os.environ["BUILD_NUM"]

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None

cmdclass = {
}
if bdist_wheel:
    cmdclass['bdist_wheel'] = bdist_wheel

setup(
  name = "%s",
  version=VERSION,
  packages=['%s'],
  package_dir = {'' : 'src'},
  package_data = {'%s': ['hdl/*.v']},
  author = AUTHOR,
  author_email = AUTHOR_EMAIL,
  description = DESCRIPTION,
  license = LICENSE,
  keywords = ["SystemVerilog", "Verilog", "RTL", "cocotb"],
  url = URL,
  setup_requires=[
    'setuptools_scm',
  ],
  cmdclass=cmdclass,
  install_requires=[
    'cocotb',
    'pybfms'
  ],
)

""" % (name, package, package))
        
    os.makedirs(os.path.join("src", package), exist_ok=True)
    
    if os.path.exists(os.path.join("src", package, "__init__.py")):
        raise Exception("Package already exists")
    
    with open(os.path.join("src", package, "__init__.py"), "w") as fp:
        fp.write("# TODO: import BFMs here\n")
    
        
    pass