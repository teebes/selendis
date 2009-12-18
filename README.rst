***************
Getting Started
***************

What is Stark?
==============
 
Stark is an attempt at a web-based visual mud. It built using open
technologies that revolve around the browser and is therefore completely
cross-platform (including all modern smart phones).
 
* All client-server interactions are `RESTful <http://en.wikipedia.org/wiki/REST>`_, which therefore means that anyone can write clients and apps in any language that interact with that world
 
* Server-side is `Django <http://djangoproject.com/>`_ served by Apache with mod-wsgi using `django_piston <http://bitbucket.org/jespern/django-piston/wiki/Home>`_ for the REST api and sqlite3 as the db (for now)
 
* Client-side is Javascript using `processing.js <http://processingjs.org/>`_ (which uses the HTML5 <canvas> element) for the graphics and `jQuery <http://jquery.com/>`_ for the REST calls and UI

Requirements
============
 
You need django and django-piston installed (links above). There are right now no other requirements and as much as possible I'd like to keep it that way.
 
**Important note**: At time of this writing, you need at least piston 0.2.3rc1 in order for it to work with the latest Django builds. That's more recent than the "latest release" links on bitbucket so be sure to checkout straight form the mercurial repo:

::

  $ hg clone http://bitbucket.org/jespern/django-piston/
 
Installation
============
 
This is a full django project, it can't just be installed as an app. Maybe once django supports nested apps... so, for now:
 
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
