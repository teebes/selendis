all: develop tests doc 

develop: 
	pip install -r REQUIREMENTS
	python setup.py develop
	rm -rf Selendis.egg-info

tests: 
	nosetests --with-doctest --with-coverage --cover-package=selendis

doc:
	$(MAKE) -C docs html


