all: tests doc

tests:
	nosetests --with-doctest --with-coverage --cover-package=selendis

doc:
	$(MAKE) -C docs html
	
