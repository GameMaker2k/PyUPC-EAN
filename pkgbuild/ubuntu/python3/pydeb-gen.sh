#!/bin/bash

scriptdir="$(realpath $(dirname $(readlink -f $0)))"
pyscriptfile="${scriptdir}/pydeb-gen.py"
pyshellfile="${scriptdir}/pydeb-gen.sh"

if [ $# -eq 0 ]; then
 pydebdir="$(${pyscriptfile} -g)"
 pydebparentdir="$(${pyscriptfile} -p)"
 pydebtarname="$(${pyscriptfile} -t)"
 pydebdirname="$(${pyscriptfile} -d)"
fi
if [ $# -gt 0 ]; then
 pydebdir="$(${pyscriptfile} -s "${1}" -g)"
 pydebparentdir="$(${pyscriptfile} -s "${1}" -p)"
 pydebtarname="$(${pyscriptfile} -s "${1}" -t)"
 pydebdirname="$(${pyscriptfile} -s "${1}" -d)"
fi
oldwd="$(pwd)"

cd "${pydebparentdir}"
tar -cvf "${pydebparentdir}/${pydebtarname}" --transform="s/$(basename ${pydebdir})/${pydebdirname}/" "$(basename ${pydebdir})"
gzip --best --verbose "${pydebparentdir}/${pydebtarname}"
cd "${pydebdir}"
python3 "${scriptdir}/pydeb-gen.py" -s "${pydebdir}"
cd "${oldwd}"
