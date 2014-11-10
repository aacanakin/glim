"""

This module holds classes for the database & model & orm layers
of glim framework.

"""

from glim.core import Facade
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:

    """

    The class that holds & manipulates database connections
    using SQLAlchemy's DB API.

    Attributes
    ----------
      config (dict): The dictionary to hold the configuration of
        connections.
      connections (dict): The list of sqlalchemy connections.
      sessions (dict): The list of sqlalchemy session that are
        used by the orm.
      engines (dict): The list of sqlalchemy engines.
      active (string): The active connection alias.

    Usage
    -----
    db = Database(config)
    sql = "INSERT INTO users (full_name, title)
           VALUES ('%s','%s')" % (full_name, title))"
    db.execute(sql)
    db.connection('name').execute(sql)

    """

    def __init__(self, config):
        self.active = 'default'
        self.config = config
        self.connections = {}
        self.sessions = {}
        self.engines = {}

        for k, config in self.config.items():

            cstring = '%s://%s@%s/%s' % (
                config['driver'],
                config['user'],
                config['password'],
                config['schema']
            )

            engine = create_engine(cstring)
            connection = engine.connect()
            Session = sessionmaker(bind=engine)
            session = Session()

            self.engines[k] = engine
            self.sessions[k] = session
            self.connections[k] = connection

    def __getattr__(self, attr):
        return getattr(self.connections[self.active], attr)

    def session(self):
        """

        Function returns the session object of active connection.

        Returns
        -------
          session (sqlalchemy.orm.session.Session): The active
            session that is used by Orm layer.

        """
        return self.sessions[self.active]

    def engine(self, key=None):
        """

        Function returns the active engine object.

        Args
        ----
          key (string): a string based key to represent
            connection dict.

        Returns
        -------
          engine (sqlalchemy.engine.Engine): The active
            engine for db connection.

        """
        if key:
            return self.engines[key]
        else:
            return self.engines[self.active]

    def connection(self, key=None):
        """

        Function sets the active connection and
        returns the self for chaining connections.

        Args
        ----
          key (string): The connection alias.

        Returns
        -------
          db (glim.db.Database): self for method
            chaining.

        """
        if key:
            self.active = key
        else:
            self.active = 'default'

        return self

    def get(self, key=None):
        """

        Function returns the engine object
        optionally given key.

        Args
        ----
          key (string): The connection alias.

        Returns
        -------
          connection (sqlalchemy.engine.Connection):
            the created connection from active engine.

        """
        if key:
            return self.connections[key]
        else:
            return self.connections[self.active]

    def close(self):
        """Function closes the database connections."""
        for connection in self.config.items():
            connection.close()


class DatabaseFacade(Facade):
    accessor = Database

# an alias of sqlalchemy.ext.declarative.declarative_base
Model = declarative_base()


class Orm:

    """

    This class is responsible for handling orm operations
    using SQLAlchemy.

    Attributes
    ----------
      engines (list): a list of sqlalchemy engines.

    Usage
    -----
        user = User(full_name, title) # a sqlalchemy model
        ORM.add(user) # adds the user object into session
        ORM.commit() # commits the transaction

    """

    def __init__(self, engines):
        self.active = 'default'
        self.engines = engines
        self.sessions = {}
        DBSession = sessionmaker()
        for k, engine in engines.items():
            DBSession.configure(bind=engine)
            self.sessions[k] = DBSession()

    def __getattr__(self, attr):
        return getattr(self.sessions[self.active], attr)

    def session(key='default'):
        """

        Function sets the active orm session and returns
        self for method chaining.

        Args
        ----
          key (string): String based alias of session.

        Returns
        -------
          orm (glim.db.Orm): self.

        """
        self.active = key
        return self

class OrmFacade(Facade):
    accessor = Orm