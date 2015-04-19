#!/bin/bash

oldwd=$(pwd)
python "$(realpath $(dirname $(readlink -f $0))/pydeb-gen.py)" "$(realpath $(dirname $(readlink -f $0))/../../../)"
cd "$(realpath $(dirname $(readlink -f $0))/../../../../)"
tar -cvf "./$(basename $(realpath $(dirname $(readlink -f $0))/../../../)).orig.tar" "$(basename $(realpath $(dirname $(readlink -f $0))/../../../))"
gzip --best --verbose "./$(basename $(realpath $(dirname $(readlink -f $0))/../../../)).orig.tar"
cd ${oldwd}
