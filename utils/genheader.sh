# header for fuzzer generate.sh scripts

if [ -z "$XC2CT_DIR" ]; then
	echo "No XC2CT_DIR environment found. Make sure to source the env file first!"
	exit 1
fi

set -ex

# Get aliases, which don't seem to propagate correctly
# also the python path
pushd $XC2CT_DIR
source env.sh
popd

#test $# = 1
#test ! -e $1
mkdir -p $1
cd $1

