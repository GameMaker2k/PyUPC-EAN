#!/usr/bin/make -f

PREFIX?="/usr/local"
DESTDIR?="/"
CMAKE?="/usr/bin/cmake"
MAKE?="/usr/bin/make"
PYTHONTWO?="/usr/bin/python2"
PYTHONTHREE?="/usr/bin/python3"
.PHONY: all install installnoclean clean pythontwoinst pythonthreeinst pythontwoinstnoclean pythonthreeinstnoclean pythontwo pythonthree pythontwonoclean pythonthreenoclean 

all: clean pythontwonoclean pythonthreenoclean 

install: pythontwoinst pythonthreeinst 

installnoclean: pythontwoinstnoclean pythonthreeinstnoclean 

clean:
	if [ -d "./py2build/" ]; then cd "./py2build" && make clean; fi
	if [ -d "./py3build/" ]; then cd "./py3build" && make clean; fi
	rm -rfv "./build/" "./dist/" "./deb_dist/" "./PyUPC_EAN.egg-info/" "./py2build/" "./py3build"

pythontwoinst: pythontwo 
	if [ -d "./py2build/" ]; then cd "./py2build" && ${MAKE} DESTDIR=${DESTDIR} install; fi
	${MAKE} clean 

pythonthreeinst: pythonthree 
	if [ -d "./py3build/" ]; then cd "./py3build" && ${MAKE} DESTDIR=${DESTDIR} install; fi
	${MAKE} clean 

pythontwoinstnoclean: pythontwonoclean 
	if [ -d "./py2build/" ]; then cd "./py2build" && ${MAKE} DESTDIR=${DESTDIR} install; fi

pythonthreeinstnoclean: pythonthreenoclean 
	if [ -d "./py3build/" ]; then cd "./py3build" && ${MAKE} DESTDIR=${DESTDIR} install; fi

pythontwo:
	${MAKE} clean 
	mkdir -p -v "./py2build" && cd "./py2build" && ${CMAKE} -DPYTHON_EXECUTABLE:FILEPATH=${PYTHONTWO} -DCMAKE_INSTALL_PREFIX:PATH=${PREFIX} .. && ${MAKE}

pythonthree:
	${MAKE} clean 
	mkdir -p -v "./py3build" && cd "./py3build" && ${CMAKE} -DPYTHON_EXECUTABLE:FILEPATH=${PYTHONTHREE} -DCMAKE_INSTALL_PREFIX:PATH=${PREFIX} .. && ${MAKE}

pythontwonoclean:
	mkdir -p -v "./py2build" && cd "./py2build" && ${CMAKE} -DPYTHON_EXECUTABLE:FILEPATH=${PYTHONTWO} -DCMAKE_INSTALL_PREFIX:PATH=${PREFIX} .. && ${MAKE}

pythonthreenoclean:
	mkdir -p -v "./py3build" && cd "./py3build" && ${CMAKE} -DPYTHON_EXECUTABLE:FILEPATH=${PYTHONTHREE} -DCMAKE_INSTALL_PREFIX:PATH=${PREFIX} .. && ${MAKE}
