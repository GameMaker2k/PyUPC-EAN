#!/usr/bin/env sh

PYTHONPATH="$(pwd)/upcean" $(/usr/bin/which python) -b -B -x -c "import upc" $*
