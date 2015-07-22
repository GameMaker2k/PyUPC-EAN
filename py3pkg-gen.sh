#!/bin/bash

pythonexec="$(which python3)"
${pythonexec} "./pypkg-gen.py" "$@"
