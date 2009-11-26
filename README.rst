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
 
Installation
============
 
This is a full django project, it can't just be installed as an app. Maybe once django supports nested apps... so, for now:
 
* add the stark package to the Python path
 
* syncdb (**important**: name the created user ``admin``)::

  $ python manage.py syncdb
 
* start the server: ::

  $ python manage.py runserver
 
* login to the admin side at http://127.0.0.1:8000/admin (you need to do this otherwise it will create an anonymous account when you load the game)
 
* load the game in your browser at http://127.0.0.1:8000
 
* run the timer script: ::

  $ python apps/timer
  
Demo Data
=========

There are two fixtures with a (very) basic world:

* ``api/apps/anima/fixtures/demo_data.json`` for players & mobs
* ``api/apps/world/fixtures/demo_data.json`` for rooms & connectors