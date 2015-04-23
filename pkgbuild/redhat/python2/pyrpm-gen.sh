#!/bin/bash

scriptdir="$(realpath $(dirname $(readlink -f $0)))"
pyscriptfile="${scriptdir}/pyrpm-gen.py"
pyshellfile="${scriptdir}/pyrpm-gen.sh"
pythonexec="$(which python2)"
oldwd="$(pwd)"

if [ $# -eq 0 ]; then
 pyrpmdir="$(${pythonexec} "${pyscriptfile}" -g)"
 pyrpmparentdir="$(${pythonexec} "${pyscriptfile}" -s "${pyrpmdir}" -p)"
 pyrpmtarname="$(${pythonexec} "${pyscriptfile}" -s "${pyrpmdir}" -t)"
 pyrpmdirname="$(${pythonexec} "${pyscriptfile}" -s "${pyrpmdir}" -d)"
fi
if [ $# -gt 0 ]; then
 pyrpmdir="$(${pythonexec} "${pyscriptfile}" -s "${1}" -g)"
 pyrpmparentdir="$(${pythonexec} "${pyscriptfile}" -s "${pyrpmdir}" -p)"
 pyrpmtarname="$(${pythonexec} "${pyscriptfile}" -s "${pyrpmdir}" -t)"
 pyrpmdirname="$(${pythonexec} "${pyscriptfile}" -s "${pyrpmdir}" -d)"
fi

cd "${pyrpmparentdir}"
tar -cavvf "${pyrpmparentdir}/${pyrpmtarname}" --transform="s/$(basename ${pyrpmdir})/${pyrpmdirname}/" "$(basename ${pyrpmdir})"
file -z -k "${pyrpmparentdir}/${pyrpmtarname}"
cd "${pyrpmdir}"
${pythonexec} "${pyscriptfile}" -s "${pyrpmdir}"
cd "${pyrpmparentdir}"
mv -v "${pyrpmparentdir}/${pyrpmtarname}" "$(realpath "${pyrpmdir}/rpmbuild/SOURCES")/${pyrpmtarname}"
cd "${oldwd}"
