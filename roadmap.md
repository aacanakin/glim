- app structure
    + app folder should be completely seperate with extensions
    + app folder may not be app folder but parametric
    + generating new app from file tree instead of proto
    + parametrized paths (i.e parametric static folder)
- helpers
    + add helper functions to be used everywhere in framework
- config
    + the framework component configurations may be placed outside the `glim` dict
- extension system
    + extensions should be folders not
    + extensions to develop
        + Memcached
        + Mail
        + Message Queue (AWSQ, Rabbit, Iron, etc)
    + command line functions to create extension
    + command line functions to publish extension config (that one may be tricky)
    + extensions should be able to have commands (such as job producing/consuming, message queue stuff)
- facades
    + should be more extensible
    + use (*args, **kwargs) in booting
    + facades should be registered not booted
    + accessor property for facades to hold instances with different names
    + support for w/ w/out configuration
- command layer implementation
    + custom commands
    + after run function, all of the framework components should be accessible but web server
    + command line functions to create extensions
- exception handling
    + more verbose errors
    + custom exceptions to specify the errors
    + colored exceptions :)
- testing
    + Mockery implementation
    + unit tests (maybe)
- package release for PyPI
- performance
    + optimization
    + benchmarks
        + apache bench
