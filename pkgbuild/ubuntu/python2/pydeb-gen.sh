#!/bin/bash

python "$(realpath $(dirname $(readlink -f $0))/pydeb-gen.py)" "$(realpath $(dirname $(readlink -f $0))/../../../)"
