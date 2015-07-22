#!/usr/bin/env bash

pythonexec="$(command -v python2)"
${pythonexec} "./pypkg-gen.py" "$@"
