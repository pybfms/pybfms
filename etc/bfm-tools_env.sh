#****************************************************************************
#* bfm-tools_env.sh
#*
#* Environment setup script for bfm-tools
#****************************************************************************


etc_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd)"
rootdir=`cd $etc_dir/.. ; pwd`



# Add a path to the simscripts directory
export PATH=$rootdir/packages/simscripts/bin:$PATH

# Force the PACKAGES_DIR
export PACKAGES_DIR=$rootdir/packages
