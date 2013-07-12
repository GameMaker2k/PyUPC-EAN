PREFIX?="/usr"
DESTDIR?="/"
PYTHON?="/usr/bin/python"
.PHONY: all install
all:
	${PYTHON} ./setup.py build
install:
	${PYTHON} ./setup.py install --prefix=${PREFIX} --root=${DESTDIR}