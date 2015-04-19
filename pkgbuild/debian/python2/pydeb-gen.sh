#!/bin/bash

oldwd=$(pwd)
cd "$(realpath $(dirname $(readlink -f $0))/../../../../)"
tar -cvf "$(realpath $(dirname $(readlink -f $0))/../../../../)/$(python "$(realpath $(dirname $(readlink -f $0))/pydeb-gen.py)" --get-tar-name)" --transform="s/$(basename $(realpath $(dirname $(readlink -f $0))/../../../))/$(python "$(realpath $(dirname $(readlink -f $0))/pydeb-gen.py)" --get-dir-name)/" "$(basename $(realpath $(dirname $(readlink -f $0))/../../../))"
gzip --best --verbose "$(realpath $(dirname $(readlink -f $0))/../../../../)/$(python "$(realpath $(dirname $(readlink -f $0))/pydeb-gen.py)" --get-tar-name)"
cd ${oldwd}
python "$(realpath $(dirname $(readlink -f $0))/pydeb-gen.py)" "$(realpath $(dirname $(readlink -f $0))/../../../)"
