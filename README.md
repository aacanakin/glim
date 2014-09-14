glim - 0.8.5
============

[Documentation(not complete)](http://aacanakin.github.io/glim)

[Changelog](https://github.com/aacanakin/glim/blob/master/CHANGELOG.md)

glim is a modern web framework on top of [Werkzeug](http://werkzeug.pocoo.org/), [SQLAlchemy](http://www.sqlalchemy.org/) and [Jinja2](http://jinja.pocoo.org/docs/dev/) inspired from [play](https://www.playframework.com/) & [laravel](http://laravel.com/). The aim is to build a lightweight architecture for web app development. The development philosophy here is to make the core small as possible but still not featureless. It has an extension system that can boot objects with configuration.(See [gredis](https://github.com/aacanakin/gredis) - a redis extension for glim)

Features
--------
- A powerful routing system which has grouping & filtering
- A model layer with use of SQLAlchemy's `declarative_base()`
- A controller layer for request handling, service calling, etc.
- A service layer to seperate database layer logic from models
- An object oriented command line layer with use of `argparse`
- An extension system that developers can integrate to the framework

Quick Start
-----------
```sh
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

# copy the sample configuration into the defined environment
$ cp app/config/default.py app/config/development.py

# start the web server
$ glim start
```

Alternative Installation (dev mode)
-----------------------------------
```sh
# clone the repo inside the project folder
$ git clone git@github.com:aacanakin/glim.git

# create & virtualenv
$ virtualenv venv
$ . venv/bin/activate

# install dependencies
$ pip install -r requirements

# generate a new app
$ python glim.py new

# copy the sample configuration
$ cp app/config/default.py app/config/development.py 

# run the web server
$ python glim.py start
```

Roadmap
-------
- extension commands should have config passed on run() ?
- add comparison matrix of other python frameworks to glim
- log module should have one internal logger one app logger
- no more manual tests, write some tests for;
    + facade tests
    + component tests
    + command layer tests
    + ORM and DB API stress tests
- exceptions
    + GlimError and its extensions
- extension system
    + extensions to develop
        * Mail
        * Message Queue (AWSQ, Rabbit, Iron, ZeroMQ etc)
        * MongoDB
        * Cassandra
        * migrations
            + rdb migrations to hold rdb changes
            + custom migrate & rollback functions
            + isolated connection that uses default connection for migrating
        * seeding
            + Seeds could add/remove db mock rows
            + seed & rollback functions
            + isolated connection that uses default connection for seeding
- model layer
    + renewing db connections & orm connections after db fails

glim is
-------
- small & lightweight
- great for painless web app development
- great for api development

glim isn't
----------
- django
- flask
- stable currently :(

NOTE: I'm changing lots of things currently. So the web server may not even start but feel free to play with it!
