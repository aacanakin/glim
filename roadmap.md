Roadmap
=======
- do not register base command
- add comparison matrix of other python frameworks to glim
- log module should have one internal logger one app logger
- no more manual tests, write some tests for;
    + facade tests
    + component tests
    + command layer tests
    + ORM and DB API stress tests
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
