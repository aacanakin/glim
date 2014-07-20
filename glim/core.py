from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# registry class is for generic framework components register function with configuration
class Registry:

    def __init__(self, registrar):
        self.registrar = registrar

    def get(self, key):
        layers = key.split('.')
        value = self.registrar
        for key in layers:
            value = value[key]
        return value

    def set(self, key, value):
        target = self.registrar
        for element in key.split(".")[:-1]:
            target = target.setdefault(element, dict())
        target[key.split(".")[-1]] = value

    def flush(self):
        self.registrar.clear()

    def update(self, registrar):
        self.registrar.update(registrar)

    def all(self):
        return self.registrar

    def __str__(self):
        print self.registrar
        return ""

# Config class
class Config(Registry):
    pass

# Session class
class Session(Registry):
    pass

# Cookie Class
class Cookie(Registry):
    pass

# Route class
class Router(Registry):
    pass

# Extension class
class Extension(Registry):
    pass

# Database related components
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

# App class is a simple dependancy injection kit plus some more functionality
class App:

    def __init__(self, registrar):
        self.registrar = registrar

    def bind(self, key, value):
        App.registrar[key] = value

    def resolve(self, key):
        return App.registrar[key]

# Base conroller class that extends all the controllers
class Controller:

    def __init__(self, request):
        self.request = request

class Service:

    def __init__(self, session):
        self.session = session

# Rest controller that
class RestController(Controller):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

# metaclass for facade class
class DeflectToInstance(type):
    def __getattr__(selfcls, a): # selfcls in order to make clear it is a class object (as we are a metaclass)
        try:
            # first, inquiry the class itself
            return super(DeflectToInstance, selfcls).__getattr__(a)
        except AttributeError:
            # Not found, so try to inquiry the instance attribute:
            return getattr(selfcls.instance, a)

class ClassNameDescriptor:
    def __get__(self, instance, owner):
        return owner.__name__

# facade that is used to hold instances statically with boot method
class Facade:
    __metaclass__ = DeflectToInstance

    instance = None

    @classmethod
    def boot(cls, object, configuration = {}):
        if cls.instance is None:
            cls.instance = object(configuration)