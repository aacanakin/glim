from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from glim.core import Registry

class Database:

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
        return self.sessions[self.active]

    def engine(self, key = None):

        if key:
            return self.engines[k]
        else:
            return self.engines[self.active]

    def connection(self, key = None):
        if key:
            self.active = key
        else:
            self.active = 'default'

        return self

    def get(self, key = None):
        if key:
            return self.connections[key]
        else:
            return self.connections[self.active]

    def close(self, key = None):
        for connection in self.config.items():
            connection.close()

Model = declarative_base()

class Orm:

    def __init__(self, engines):
        self.active = 'default'
        self.engines = engines
        self.sessions = {}
        DBSession = sessionmaker()
        for k, engine in engines.items():
            DBSession.configure(bind = engine)
            self.sessions[k] = DBSession()

    def __getattr__(self, attr):
        return getattr(self.sessions[self.active], attr)

    def session(key = 'default'):
        self.active = key
        return self


# class Migration:
# 	def __init__(self, connection):
# 		self.connection = connection

# 	def up(self):
# 		return

# 	def down(self):
# 		return

# class Schema:
# 	def __init__(self, connection):
# 		self.connection = connection

# 	def create(self):
# 		pass

# 	def alter(self):
# 		pass

# 	def drop(self):
# 		pass