glim - 0.7.8
============
Latest Documentation: http://aacanakin.github.io/glim

glim is the lightweight MVC(S) (Model, View, Controller, (Service)) framework on top of werkzeug inspired from play & laravel. The aim is to build a lightweight architecture for web app development. The development philosophy here is to make the core small as possible but still not featureless.

glim currently has
------------------
- powerful url routing w/ filtering & grouping
- configuration module for different environments
- SQLAlchemy integration
- sql query builder in model layer
- an extension system that developers can integrate it to the base
  framework
- a view layer with jinja2
- session & cookie support

glim will have
--------------
- commands module that enables easier to use command line utilities
- more & more extensions

glim is
-------
- lightweight
- build on top of werkzeug
- dependent on some great open source python projects (See reqs file)
- great for API development
- also great 

glim isn't
----------
- full-stack
- django
- flask
- stable currently :(