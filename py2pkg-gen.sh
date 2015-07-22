#!/bin/bash

pythonexec="$(which python2)"
${pythonexec} "./pypkg-gen.py" "$@"
