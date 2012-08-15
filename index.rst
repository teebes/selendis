.. Stark documentation master file, created by
   sphinx-quickstart on Sun Aug 12 22:25:14 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Stark's documentation!
=================================

Contents:

.. toctree::
   :maxdepth: 2

   docs/toc.rst
   docs/roadmap.rst
   docs/rjson.rst
   docs/models.rst


Testing
=======

In the project root, run::

    nosetests --with-doctest --with-coverage --cover-package=stark 

Currently working on
====================
Enforcing type in the following scenario:
* Weak ref of undeclared model instance is encountered
* reference model instance is updated with a typed rjson model instance
* model instance in registry should be of the correct type


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


