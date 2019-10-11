
import os
from setuptools import setup

setup(
  name = "bfm_core",
  packages=['bfm_core'],
  package_dir = {'' : 'src'},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("bfm_core provides core libraries and scripts to support BFMS"),
  license = "Apache 2.0",
  keywords = ["SystemVerilog", "Verilog", "RTL", "CocoTB", "Python"],
  url = "https://github.com/sv-bfms/bfm_core",
  entry_points={
    'console_scripts': [
      'vlsim = vlsim.__main__:main'
    ]
  },
  setup_requires=[
    'setuptools_scm',
  ],
)

