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
* Deserialization
* containers
* item dropping 
* getting

Issues
======
* Getting the __setattr__ piece to work on Base broke some of the unit test
* load_world.py is throwing a __new__ TypeError
* Registry reset can only work using kwargs. using key={} doesn't reset to it

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


