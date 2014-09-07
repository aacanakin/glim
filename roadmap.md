Roadmap
=======
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
        * job system
            + job producing/consuming using redis, rmq or zmq
- facades
    + should be more extensible
    + should have an option to be registered by Provider with custom registrations
    + accessor property for facades to hold instances with different names
- model layer
    + renewing db connections & orm connections after db fails
- tests
    + facade tests
    + component tests
    + command layer tests
    + ORM and DB API stress tests
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
