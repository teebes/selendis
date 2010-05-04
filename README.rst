***************
Getting Started
***************

What is Stark?
==============
 
Stark is an attempt at a web-based visual mud. It built using HTML5, JavaScript
and Django and therefore cross-platform (with the notable exception of IE,
which does yet yet support HTML5).
 
* Built around 2 public APIs, one action-oriented for best client performance and one RESTful.

* Server-side is `Django <http://djangoproject.com/>`_ served by Apache with mod-wsgi using `django_piston <http://bitbucket.org/teebes/django-piston/`_ for the REST api and sqlite3 as the db (for now)
 
* Client-side is Javascript using `processing.js <http://processingjs.org/>`_ (which uses the HTML5 <canvas> element) for the graphics and `jQuery <http://jquery.com/>`_ API calls and UI

Requirements
============
 
You need django and a custom fork of django-piston installed (links above). There are right now no other requirements and as much as possible I'd like to keep it that way.
 
**Important note**: At time of this writing, you need at least piston 0.2.3rc1 in order for it to work with the latest Django builds. That's more recent than the "latest release" links on bitbucket so be sure to checkout straight form the mercurial repo:

::

  $ hg clone http://bitbucket.org/teebes/django-piston/

There is a pip requirements file included so it's very easy to create an isolated Python virtual environment with everything you need:

::

  $ easy_install pip
  $ pip install virtualenv

Once Stark is installed, run in its root directory:

::

  $ virtualenv ve --no-site-packages
  $ pip install -r REQUIREMENTS -e VE
  $ source ve/bin/activate

You should now have all of the requirements are ready to go.
 
Installation
============
 
This is a full django project, it can't just be installed as an app:
 
* add the stark package to the Python path
 
* syncdb (go ahead and create a superuser)::

  $ python manage.py syncdb
 
* start the server: ::

  $ python manage.py runserver
 
* go the game at http://127.0.0.1:8000

* click the 'login' link, log on as the superuser you created

* If this is your first time trying out Stark, you should seriously consider loading the demo data to get a feel for what the world can be like.
  
Demo Data
=========

There are two fixtures with a (very) basic world:

* ``api/apps/world/fixtures/demo_data.json`` for rooms & connectors
* ``api/apps/anima/fixtures/demo_data.json`` for players & mobs

You can load them with: ::

  $ python manage.py loaddata demo_data

Documentation
=============

The sphinx docs are seriously out of date at the moment. I've ended up rewriting most of the game over the last couple of months and a lot of the structure is now radically different. I'll update as soon as the project is stable enough that I know I won't need to rewrite half of it soon.
