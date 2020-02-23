#!/bin/sh
#****************************************************************************
#* build.sh
#*
#* Build script for the pybfms binary wheel. This script is run inside 
#* the manylinux Docker container
#****************************************************************************

mkdir -p /build
cd /build

echo "Hello from PyPi build.sh"

BUILD_DIR=`pwd`
if test -f /proc/cpuinfo; then
  echo "cpuinfo exists"
  N_CORES=`cat /proc/cpuinfo | grep processor | wc -l`
else
  echo "cpuinfo DOES NOT exist"
  N_CORES=1
fi

cp -r /pybfms .

#********************************************************************
#* pybfms
#********************************************************************

# Add the build number to the version
#sed -i -e "s/{{BUILD_NUM}}/${BUILD_NUM}/g" setup.py

# for py in python27 rh-python35 rh-python36; do
for py in cp34-cp34m cp35-cp35m cp36-cp36m cp37-cp37m cp38-cp38; do
  echo "Python: ${py}"
  python=/opt/python/${py}/bin/python
  $python setup.py sdist bdist_wheel
  if test $? -ne 0; then exit 1; fi
done

for whl in dist/*.whl; do
  auditwheel repair $whl
  if test $? -ne 0; then exit 1; fi
done

rm -rf /pybfms/result
mkdir -p /pybfms/result

cp -r wheelhouse dist /pybfms/result


