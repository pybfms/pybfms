
import os
from setuptools import setup
from distutils.extension import Extension

def find_source(bases):
    ret = []
    for base in bases:
        for file in os.listdir(base):
            if os.path.splitext(file)[1] in (".cpp", ".c"):
                ret.append(os.path.join(base, file))
            
    print("find_source: " + str(ret))
    return ret

pybfms_root = os.path.dirname(os.path.abspath(__file__))

setup(
  name = "pybfms",
  packages=['pybfms'],
  package_dir = {'' : 'src'},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("bfm_core provides core libraries and scripts to support BFMS"),
  license = "Apache 2.0",
  keywords = ["SystemVerilog", "Verilog", "RTL", "CocoTB", "Python"],
  url = "https://github.com/pybfms/pybfms",
  entry_points={
    'console_scripts': [
      'pybfms = pybfms.__main__:main'
    ]
  },
  setup_requires=[
    'setuptools_scm',
  ],
  ext_modules=[
      Extension("pybfms_hdl_sim", 
        include_dirs=[
            os.path.join(pybfms_root, 'ext/common'), 
            os.path.join(pybfms_root, 'ext/hdl_sim')],
        sources=find_source([
            os.path.join(pybfms_root, 'ext/common'), 
            os.path.join(pybfms_root, 'ext/hdl_sim')]
        )
    )]
)

