Roadmap
=======
- package release for PyPI
- the framework should understand if its running in dev mode
    + a dev mode switch maybe to run glim/cli.py
    + automatically detect if glim is inside a virtual environment
- extension system
    + extensions to develop
        * Memcached
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
- tests
    + facade tests
    + component tests
    + command layer tests
    + ORM and DB API stress tests
- app structure
    + parametrized paths (i.e parametric static folder)
- config
    + the framework component configurations may be placed outside the `glim` dict
    + facades should be removed from config
    + providers should be added to config after ServiceProvider implementation
- facades
    + should be more extensible
    + should have an option to be registered by ServiceProvider
    + accessor property for facades to hold instances with different names
- exception handling
    + more verbose errors
    + option not to print 
    + custom exceptions to specify the errors
    + colored exceptions :)
- testing
    + Mockery implementation
    + unit tests (maybe)
- performance
    + optimization
    + benchmarks
