# make: your onestop entry to this project, complete with dependency resolution

all: dev

export PIP_DOWNLOAD_CACHE := .pip_cache

get_reqs = ve/bin/pip install -r REQUIREMENTS

dumpvar = ./dumpvar.bash

reqs:
	$(get_reqs)

dev:
	virtualenv ve --python=python2.7
	ve/bin/python setup.py develop
	$(get_reqs)

source:
	#/bin/bash -c 'source ve/bin/activate'
	. ve/bin/activate && which python
	which python



