#!/usr/bin/env sh

PYTHONPATH="$(pwd)/upcean" $(/usr/bin/which python) -c "import upc" $*
