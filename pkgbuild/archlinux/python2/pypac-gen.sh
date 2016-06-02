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
pyscriptfile="${scriptdir}/pypac-gen.py"
pyshellfile="${scriptdir}/pypac-gen.sh"
oldwd="$(pwd)"

if [ $# -eq 0 ]; then
 pypacdir="$(${pythonexec} "${pyscriptfile}" -g)"
 pypacparentdir="$(${pythonexec} "${pyscriptfile}" -s "${pypacdir}" -p)"
 pypactarname="$(${pythonexec} "${pyscriptfile}" -s "${pypacdir}" -t)"
 pypacdirname="$(${pythonexec} "${pyscriptfile}" -s "${pypacdir}" -d)"
fi
if [ $# -gt 0 ]; then
 if [ $# -gt 1 ]; then
  codename="${2}"
 fi
 pypacdir="$(${pythonexec} "${pyscriptfile}" -s "${1}" -g)"
 pypacparentdir="$(${pythonexec} "${pyscriptfile}" -s "${pypacdir}" -p)"
 pypactarname="$(${pythonexec} "${pyscriptfile}" -s "${pypacdir}" -t)"
 pypacdirname="$(${pythonexec} "${pyscriptfile}" -s "${pypacdir}" -d)"
fi

cd "${pydebdir}"
${pythonexec} "./setup.py" "sdist"
srcfiles="$(${pythonexec} "${pydebdir}/setup.py" getsourceinfo)"
cd "${pydebparentdir}"
tar -cavvf "${pypacparentdir}/${pypactarname}" --transform="s/$(basename ${pydebdir})/${pydebdirname}/" ${srcfiles}
file -z -k "${pypacparentdir}/${pypactarname}"
cd "${pypacdir}"
${pythonexec} "${pyscriptfile}" -s "${pypacdir}"
cd "${pypacparentdir}"
mv -v "${pypacparentdir}/${pypactarname}" "$(${pyrealpath} "${pypacdir}/py2upc-ean")/${pypactarname}"
cd "${oldwd}"
