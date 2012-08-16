.. Stark documentation master file, created by
   sphinx-quickstart on Sun Aug 12 22:25:14 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Selendis
========

TOC:

.. toctree::
   :maxdepth: 2

   roadmap.rst
   api_reference.rst

Testing
=======

In the project root, run::

    nosetests --with-doctest --with-coverage --cover-package=selendis

Currently working on
====================
* Root Makefile
* 0.1 deliverables

Model notes:
============
Base:
    name
    items

Anima: hp, mp, dp, lvl, exp, room, stats (can stats be schemaless)
Room:
    x, y z
Item

Future
======

* combat:
    - weapon based hits
    - messages
    - corpse creation / looting
    - no armor mitigation
* stats
* equipment



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


