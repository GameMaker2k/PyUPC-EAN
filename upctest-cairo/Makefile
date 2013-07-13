PREFIX?="/usr/local"
DESTDIR?="/"
PYTHON?="/usr/bin/python"
.PHONY: clean all install sdist bdist egg rpm wininst
clean:
	@${PYTHON} ./setup.py clean
	@rm -rfv "./build/" "./PyUPC_EAN.egg-info/" "./python-upcean_2.4.2-3_i386.deb"
all:
	@${PYTHON} ./setup.py build
install:
	PYTHONPATH="$(shell realpath ${DESTDIR}${PREFIX})/lib/python$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[0])').$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[1])')/site-packages"
	@${PYTHON} ./setup.py install --prefix=${PREFIX} --root=${DESTDIR}
sdist:
	PYTHONPATH="$(shell realpath ${DESTDIR}${PREFIX})/lib/python$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[0])').$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[1])')/site-packages"
	@${PYTHON} ./setup.py bdist --prefix=${PREFIX} --root=${DESTDIR}
bdist:
	PYTHONPATH="$(shell realpath ${DESTDIR}${PREFIX})/lib/python$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[0])').$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[1])')/site-packages"
	@${PYTHON} ./setup.py bdist --prefix=${PREFIX} --root=${DESTDIR}
egg:
	PYTHONPATH="$(shell realpath ${DESTDIR}${PREFIX})/lib/python$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[0])').$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[1])')/site-packages"
	@${PYTHON} ./setup.py bdist-egg --prefix=${PREFIX} --root=${DESTDIR}
rpm:
	PYTHONPATH="$(shell realpath ${DESTDIR}${PREFIX})/lib/python$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[0])').$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[1])')/site-packages"
	@${PYTHON} ./setup.py bdist-rpm --prefix=${PREFIX} --root=${DESTDIR}
wininst:
	PYTHONPATH="$(shell realpath ${DESTDIR}${PREFIX})/lib/python$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[0])').$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[1])')/site-packages"
	@${PYTHON} ./setup.py bdist-wininst --prefix=${PREFIX} --root=${DESTDIR}