#!/usr/bin/make -f

PREFIX?="/usr/local"
DESTDIR?="/"
MAKE?="/usr/bin/make"
PYTHON?="/usr/bin/python2"
SDIST?="zip,gztar,bztar"
BDIST?="zip,gztar,bztar"
SETUPPY?="setup.py"
DESTURL?="https://pypi.python.org/pypi"

.PHONY: all build clean install sdist register bdist upload check

all: clean build

build:
	${PYTHON} ${SETUPPY} build

clean:
	${PYTHON} ${SETUPPY} clean

install:
	${PYTHON} ${SETUPPY} install --prefix=${PREFIX} --root=${DESTDIR}

sdist:
	${PYTHON} ${SETUPPY} sdist --formats=${SDIST}

register:
	${PYTHON} ${SETUPPY} register

bdist:
	${PYTHON} ${SETUPPY} bdist --format=${SDIST}

upload:
	${PYTHON} ${SETUPPY} -r ${DESTURL}

check:
	${PYTHON} ${SETUPPY} -m
