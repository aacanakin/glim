glim (v0.0.2)
====

The simple MC (Model, Controller) framework on top of werkzeug

glim is
=======
- small
- great for API development
- inspired from some great full-stack frameworks like rails & laravel

glim isn't
==========
- full-stack
- stable currently
- django
- flask

tada
====

- remove static folder binding in app start
- Glim class should extend App
- session & cookie
- add before & after handlers for app boot
- improve routing
    + filtering
    + grouping
    + before & after handlers
- glim command-line tools
    + add new app
    + add new controller with restful option
    + add new model
- model layer 
    + SQLAlchemy integration
    + Custom query implementation with SQLAlchemy connection
- dynamic service bootups from config file
- improve extension system
    + command line functions to create extensions
- some nosql driver extensions
    + Redis
    + Memcached
- IoC implementation
- Mockery implementation
- Improve config system    
    + Hold a default configuration for independent configs from environment
    +  Auto merge with default configuration
- Some other extensions to develop
    + Mail
    + Message Queue
    + Filesystem IO
    + SQLite driver
- benchmarks & performance tests
    + apache bench
- testing
    + Mockery implementation
    + unit tests (maybe)
- coding standards & quality analysis (currently, a lot is hacking)
- documentation on first stable release
- package release for PyPI
