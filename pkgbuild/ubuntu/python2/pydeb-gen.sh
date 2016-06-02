#!/usr/bin/env bash

pythonexec="$(command -v python2)"
if hash realpath 2>/dev/null; then
 pyrealpath="$(command -v realpath)"
 scriptdir="$(${pyrealpath} $(dirname $(readlink -f $0)))"
else
 scriptdir="$(dirname $(readlink -f $0))"
 pyrealpath="${pythonexec} ${scriptdir}/realpath.py"
 scriptdir="$(${pyrealpath} ${scriptdir})"
 pyrealpath="${pythonexec} ${scriptdir}/realpath.py"
fi
pyscriptfile="${scriptdir}/pydeb-gen.py"
pyshellfile="${scriptdir}/pydeb-gen.sh"
codename="xenial"
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

cd "${pydebdir}"
${pythonexec} "./setup.py" "sdist"
srcfiles="$(${pythonexec} "${pydebdir}/setup.py" getsourceinfo)"
cd "${pydebparentdir}"
tar -cavvf "${pydebparentdir}/${pydebtarname}" --transform="s/$(basename ${pydebdir})/${pydebdirname}/" ${srcfiles}
file -z -k "${pydebparentdir}/${pydebtarname}"
cd "${pydebdir}"
${pythonexec} "${pyscriptfile}" -s "${pydebdir}" -c "${codename}"
cd "${oldwd}"
