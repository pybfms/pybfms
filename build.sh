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

cd ${BUILD_DIR}/pybfms

# for py in python27 rh-python35 rh-python36; do
for py in cp35-cp35m cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39; do
  echo "Python: ${py}"
  ls
  python=/opt/python/${py}/bin/python
  echo "--> running ${python} on setup.py"
  $python setup.py sdist bdist_wheel
  if test $? -ne 0; then exit 1; fi
  echo "<-- running ${python} on setup.py"
done

for whl in dist/*.whl; do
  echo "--> running auditwheel `which auditwheel` on $whl"
  auditwheel repair $whl
  if test $? -ne 0; then exit 1; fi
  echo "<-- running auditwheel `which auditwheel` on $whl"
done

rm -rf /pybfms/result
mkdir -p /pybfms/result

cp -r wheelhouse dist /pybfms/result


