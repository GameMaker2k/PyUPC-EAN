#!/usr/bin/env bash

pythonexec="$(command -v python3)"
${pythonexec} "./pypkg-gen.py" "$@"
