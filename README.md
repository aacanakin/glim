glim - 0.6.7
=============
Latest Documentation(not complete): http://aacanakin.github.io/glim
Roadmap: https://github.com/aacanakin/glim/blob/master/roadmap.md

Changelog: https://github.com/aacanakin/glim/blob/master/CHANGELOG.md

glim is the lightweight MVC(S) (Model, View, Controller, (Service)) framework on top of werkzeug inspired from play & laravel. The aim is to build a lightweight architecture for web app development. The development philosophy here is to make the core small as possible but still not featureless. It has an extension system that can boot objects with configuration.

The project depends on great open source python projects like SQLAlchemy, werkzeug, jinja2, etc.

quick start
-----------
- clone the repo
- inside the folder run following;
```
$ virtualenv venv & $. venv/bin/activate
$ pip install -r requirements
$ python glim.py new inside project folder
$ cp app/config/default.py app/config/development.py
$ python glim.py start
```

glim is
-------
- small & lightweight
- great for painless web app development
- great for api development

glim isn't
----------
- full-stack
- django
- flask
- not stable currently :(

NOTE: I'm changing lots of things currently. So the web server may not even start but feel free to play with it!
