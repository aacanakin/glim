`Documentation <http://glim.readme.io>`__

`Roadmap <http://glim.readme.io/v0.8.6/docs/roadmap>`__

`Changelog <https://github.com/aacanakin/glim/blob/master/CHANGELOG.md>`__

glim is a modern web framework on top of `Werkzeug <http://werkzeug.pocoo.org/>`__, `SQLAlchemy <http://www.sqlalchemy.org/>`__ and `Jinja2 <http://jinja.pocoo.org/docs/dev/>`__ inspired from `play <https://www.playframework.com/>`__ & `laravel <http://laravel.com/>`__. The aim is to build a lightweight architecture for web app development. The development philosophy here is to make the core small as possible but still not featureless. It has an extension system that can boot objects with configuration.(See `gredis <https://github.com/aacanakin/gredis>`__ - a redis extension for glim)

Features
--------

-  A powerful routing system which has grouping & filtering
-  A model layer with use of SQLAlchemy's ``declarative_base()``
-  A controller layer for request handling, service calling, etc.
-  A service layer to seperate database layer logic from models
-  An object oriented command line layer with use of ``argparse``
-  An extension system that developers can integrate to the framework

Quick Start
-----------

::

    # create project folder
    $ mkdir <project>
    $ cd <project>

    # create a virtualenv
    $ virtualenv venv

    # activate the virtualenv
    $ . venv/bin/activate

    # install glim from pypi
    $ pip install glim

    # generate a new glim app
    $ glim new

    # start the web server
    $ glim start

glim is
-------

-  small & lightweight
-  great for painless web app development
-  great for api development

glim isn't
----------

-  django
-  flask
-  not stable currently :(

NOTE: I'm changing lots of things currently. So the web server may not
even start but feel free to play with it!
