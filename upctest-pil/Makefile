PREFIX?="/usr/local"
DESTDIR?="/"
PYTHON?="/usr/bin/python"
.PHONY: clean all install sdist bdist gztar ztar tar zip egg rpm deb wininst msi
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
gztar:
	@${PYTHON} ./setup.py bdist --format=gztar
ztar:
	@${PYTHON} ./setup.py bdist --format=ztar
tar:
	@${PYTHON} ./setup.py bdist --format=tar
zip:
	@${PYTHON} ./setup.py bdist --format=zip
egg:
	PYTHONPATH="$(shell realpath ${DESTDIR}${PREFIX})/lib/python$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[0])').$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[1])')/site-packages"
	@${PYTHON} ./setup.py bdist-egg --prefix=${PREFIX} --root=${DESTDIR}
rpm:
	@${PYTHON} ./setup.py bdist_rpm --packager="Kazuki Przyborowski <kazuki.przyborowski@gmail.com>"
deb:
	@${PYTHON} ./setup.py --command-packages=stdeb.command bdist_deb
wininst:
	@${PYTHON} ./setup.py bdist_wininst
msi:
	@${PYTHON} ./setup.py bdist_msi