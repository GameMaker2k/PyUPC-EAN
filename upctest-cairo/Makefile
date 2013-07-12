PREFIX?="/usr/local"
DESTDIR?="/"
PYTHON?="/usr/bin/python"
.PHONY: all install
all:
	${PYTHON} ./setup.py build
install:
	PYTHONPATH="$(shell realpath ${DESTDIR}${PREFIX})/lib/python$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[0])').$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[1])')/site-packages"
	${PYTHON} ./setup.py install --prefix=${PREFIX} --root=${DESTDIR}