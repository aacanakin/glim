Roadmap
=======
- package release for PyPI
- migrations
    + rdb migrations to hold rdb changes
    + custom migrate & rollback functions
    + isolated connection that uses default connection but holds migrations in different db, sqlite db would be convenient
    + should be an extension to glim
- seeding
    + Seeds could add/remove db mock rows
    + seed & rollback functions
    + isolated connection that uses default connection but holds migrations in different db, sqlite db would be convenient
    + should be an extension to glim
- app structure
    + parametrized paths (i.e parametric static folder)
- config
    + the framework component configurations may be placed outside the `glim` dict
    + facades should be removed from config
    + providers should be added to config after ServiceProvider implementation
- extension system
    + extensions to develop
        * Memcached
        * Mail
        * Message Queue (AWSQ, Rabbit, Iron, ZeroMQ etc)
    + command line functions to create extension
    + extensions should be able to have commands (such as job producing/consuming, message queue stuff)
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
- removing ego from project
- add core features to readme