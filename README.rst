`Documentation <http://glim.readme.io>`__

`Roadmap <http://glim.readme.io/v0.8.6/docs/roadmap>`__

`Changelog <https://github.com/aacanakin/glim/blob/master/CHANGELOG.md>`__

glim is a modern web framework on top of `Werkzeug <http://werkzeug.pocoo.org/>`__, `SQLAlchemy <http://www.sqlalchemy.org/>`__ and `Jinja2 <http://jinja.pocoo.org/docs/dev/>`__ inspired from `play <https://www.playframework.com/>`__ & `laravel <http://laravel.com/>`__. TThe aim is to build a lightweight architecture for web app development. The development philosophy here is to make the core small as possible but still not featureless. It has a conventional extension system that can boot objects with configuration. It also has a handful set of extensions for view rendering, templating and performing database operations. You can check `glim_extensions <http://github.com/aacanakin/glim-extensions/>`__ for much more information.

Features
--------

- Convention over configuration
- A powerful routing system which has grouping & filtering
- A controller layer for request handling, service calling, etc.
- A set of handful extensions that includes SQLAlchemy, Jinja2, redis, etc. integrations
- An object oriented command line layer
- An extension system that developers can integrate to the framework

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

Cutting edge
------------

::

    # clone the repo inside the project folder
    $ git clone git@github.com:aacanakin/glim.git

    # enter the folder
    $ cd glim

    # create & virtualenv
    $ virtualenv venv
    $ . venv/bin/activate

    # install dependencies
    $ pip install -r requirements.txt

    # generate a new app
    $ python glim.py new

    # run the web server
    $ python glim.py start

glim is
-------

- small & lightweight
- great for painless web app development
- great for api/web-service development

glim isn't
----------

- django
- flask
- stable currently :(

NOTE: The framework is in its early stages in development. So, there are lots of backward incompatible changes constantly. So the web server may not even start but feel free to play with it!

