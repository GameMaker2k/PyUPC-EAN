#!/bin/bash

scriptdir="$(realpath $(dirname $(readlink -f $0)))"
pyscriptfile="${scriptdir}/pydeb-gen.py"
pyshellfile="${scriptdir}/pydeb-gen.sh"
pythonexec="$(which python3)"
codename="trusty"
oldwd="$(pwd)"

if [ $# -eq 0 ]; then
 pydebdir="$(${pythonexec} "${pyscriptfile}" -c "${codename}" -g)"
 pydebparentdir="$(${pythonexec} "${pyscriptfile}" -s "${pydebdir}" -c "${codename}" -p)"
 pydebtarname="$(${pythonexec} "${pyscriptfile}" -s "${pydebdir}" -c "${codename}" -t)"
 pydebdirname="$(${pythonexec} "${pyscriptfile}" -s "${pydebdir}" -c "${codename}" -d)"
fi
if [ $# -gt 0 ]; then
 if [ $# -gt 1 ]; then
  codename="${2}"
 fi
 pydebdir="$(${pythonexec} "${pyscriptfile}" -s "${1}" -c "${codename}" -g)"
 pydebparentdir="$(${pythonexec} "${pyscriptfile}" -s "${pydebdir}" -c "${codename}" -p)"
 pydebtarname="$(${pythonexec} "${pyscriptfile}" -s "${pydebdir}" -c "${codename}" -t)"
 pydebdirname="$(${pythonexec} "${pyscriptfile}" -s "${pydebdir}" -c "${codename}" -d)"
fi

cd "${pydebparentdir}"
tar -cavvf "${pydebparentdir}/${pydebtarname}" --transform="s/$(basename ${pydebdir})/${pydebdirname}/" "$(basename ${pydebdir})"
file -z -k "${pydebparentdir}/${pydebtarname}"
cd "${pydebdir}"
${pythonexec} "${pyscriptfile}" -s "${pydebdir}" -c "${codename}"
cd "${oldwd}"
