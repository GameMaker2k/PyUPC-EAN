PREFIX?="/usr/local"
DESTDIR?="/"
CMAKE?="/usr/bin/cmake"
MAKE?="/usr/bin/make"
PYTHONTWO?="/usr/bin/python"
PYTHONTHREE?="/usr/bin/python"
.PHONY: all install clean pythontwo pythonthree

all: pythontwo pythonthree

install:
	if [ -d "./py2build/" ]; then cd "./py2build" && ${MAKE} DESTDIR=${DESTDIR} install; fi
	if [ -d "./py3build/" ]; then cd "./py3build" && ${MAKE} DESTDIR=${DESTDIR} install; fi

clean:
	if [ -d "./py2build/" ]; then cd "./py2build" && make clean; fi
	if [ -d "./py3build/" ]; then cd "./py3build" && make clean; fi
	rm -rfv "./build/" "./dist/" "./deb_dist/" "./PyUPC_EAN.egg-info/" "./py2build/" "./py3build"

pythontwo:
	mkdir -p -v "./py2build" && cd "./py2build" && ${CMAKE} -DPYTHON_EXECUTABLE:FILEPATH=${PYTHONTWO} -DCMAKE_INSTALL_PREFIX:PATH=${PREFIX} .. && ${MAKE}

pythonthree:
	mkdir -p -v "./py3build" && cd "./py3build" && ${CMAKE} -DPYTHON_EXECUTABLE:FILEPATH=${PYTHONTWO} -DCMAKE_INSTALL_PREFIX:PATH=${PREFIX} .. && ${MAKE}
