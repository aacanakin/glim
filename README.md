glim - 0.7.7
=============
[Documentation(not complete)](http://aacanakin.github.io/glim)

[Roadmap](https://github.com/aacanakin/glim/blob/master/roadmap.md)

[Changelog](https://github.com/aacanakin/glim/blob/master/CHANGELOG.md)

PyPI package will be hopefully released soon

glim is the lightweight MVC(S) (Model, View, Controller, (Service)) framework on top of werkzeug inspired from play & laravel. The aim is to build a lightweight architecture for web app development. The development philosophy here is to make the core small as possible but still not featureless. It has an extension system that can boot objects with configuration.(See [gredis](https://github.com/aacanakin/gredis) - a redis extension for glim)

The project depends on great open source python projects like SQLAlchemy, werkzeug, jinja2, etc.

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
- clone the repo
- inside the project folder run following statements;
```
# create a virtualenv
$ virtualenv venv

# activate the virtualenv
$ . venv/bin/activate

# install the package dependencies
$ pip install -r requirements

# initialize a new glim app
$ python glim.py new

# copy the sample configuration into the defined environment
$ cp app/config/default.py app/config/development.py

# start the web server
$ python glim.py start
```

glim is
-------
- small & lightweight
- great for painless web app development
- great for api development

glim isn't
----------
- django
- flask
- not stable currently :(

NOTE: I'm changing lots of things currently. So the web server may not even start but feel free to play with it!
