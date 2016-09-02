#!/usr/bin/env bash

pythonexec="$(command -v python3)"
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
 pypkgdir="$(${pythonexec} "${pyscriptfile}" -g)"
 pypkgparentdir="$(${pythonexec} "${pyscriptfile}" -s "${pypkgdir}" -p)"
 pypkgtarname="$(${pythonexec} "${pyscriptfile}" -s "${pypkgdir}" -t)"
 pypkgdirname="$(${pythonexec} "${pyscriptfile}" -s "${pypkgdir}" -d)"
 pypkgsource="$(${pythonexec} "${pyscriptfile}" -s "${pypkgdir}" -e)"
fi
if [ $# -gt 0 ]; then
 if [ $# -gt 1 ]; then
  codename="${2}"
 fi
 pypkgdir="$(${pythonexec} "${pyscriptfile}" -s "${1}" -g)"
 pypkgparentdir="$(${pythonexec} "${pyscriptfile}" -s "${pypkgdir}" -p)"
 pypkgtarname="$(${pythonexec} "${pyscriptfile}" -s "${pypkgdir}" -t)"
 pypkgdirname="$(${pythonexec} "${pyscriptfile}" -s "${pypkgdir}" -d)"
 pypkgsource="$(${pythonexec} "${pyscriptfile}" -s "${pypkgdir}" -e)"
fi

cd "${pypkgdir}"
${pythonexec} "./setup.py" "sdist"
srcfiles="$(${pythonexec} "${pypkgdir}/setup.py" getsourceinfo)"
cd "${pydebparentdir}"
tar -cavvf "${pypkgparentdir}/${pypkgtarname}" --transform="s/$(basename ${pypkgdir})/${pydebdirname}/" ${srcfiles}
file -z -k "${pypkgparentdir}/${pypkgtarname}"
cd "${pypkgdir}"
${pythonexec} "${pypkgdir}/setup.py" cleansourceinfo
${pythonexec} "${pyscriptfile}" -s "${pypkgdir}"
cd "${pypkgparentdir}"
mv -v "${pypkgparentdir}/${pypkgtarname}" "$(${pyrealpath} "${pypkgdir}/${pypkgsource}")/${pypkgtarname}"
cd "${oldwd}"
