#!/usr/bin/env sh

PYTHONDONTWRITEBYTECODE="x" PYTHONPATH="$(pwd)/upcean" $(/usr/bin/which python) -b -B -x "./upc.py" "$@"
