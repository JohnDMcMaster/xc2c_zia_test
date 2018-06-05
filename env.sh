# https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
export XC2CT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export XC2CT_GENHEADER=$XC2CT_DIR/utils/genheader.sh

source /opt/Xilinx/14.?/ISE_DS/settings64.sh
