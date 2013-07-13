PREFIX?="/usr/local"
DESTDIR?="/"
PYTHON?="/usr/bin/python"
.PHONY: all install clean sdist bdist gztar ztar tar zip gztarsrc ztarsrc tarsrc zipsrc egg rpm deb wininst msi
all:
	${PYTHON} ./setup.py build
install:
	PYTHONPATH="$(shell realpath ${DESTDIR}${PREFIX})/lib/python$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[0])').$(shell ${PYTHON} -c 'import sys; print str(sys.version_info[1])')/site-packages"
	${PYTHON} ./setup.py install --prefix=${PREFIX} --root=${DESTDIR}
clean:
	${PYTHON} ./setup.py clean
	rm -rfv "./build/" "./dist/" "./deb_dist/" "./PyUPC_EAN.egg-info/"
sdist:
	${PYTHON} ./setup.py sdist
bdist:
	${PYTHON} ./setup.py bdist
gztar:
	${PYTHON} ./setup.py bdist --format=gztar
ztar:
	${PYTHON} ./setup.py bdist --format=ztar
tar:
	${PYTHON} ./setup.py bdist --format=tar
zip:
	${PYTHON} ./setup.py bdist --format=zip
gztarsrc:
	${PYTHON} ./setup.py sdist --format=gztar
ztarsrc:
	${PYTHON} ./setup.py sdist --format=ztar
tarsrc:
	${PYTHON} ./setup.py sdist --format=tar
zipsrc:
	${PYTHON} ./setup.py sdist --format=zip
egg:
	${PYTHON} ./setup.py bdist_egg
rpm:
	${PYTHON} ./setup.py bdist_rpm --packager="$(shell getent passwd ${USER} | cut -d: -f5 | cut -d, -f1) <$(shell echo ${USER})@$(shell hostname)>"
deb:
	${PYTHON} ./setup.py --command-packages=stdeb.command bdist_deb
wininst:
	${PYTHON} ./setup.py bdist_wininst
msi:
	${PYTHON} ./setup.py bdist_msi