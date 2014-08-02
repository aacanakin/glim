from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from jinja2 import Environment, PackageLoader

from werkzeug.wrappers import Response

# registry class is for generic framework components register function with configuration
class Registry:

    def __init__(self, registrar):
        self.registrar = registrar

    def get(self, key):
        try :
            layers = key.split('.')
            value = self.registrar
            for key in layers:
                value = value[key]
            return value
        except:
            return None

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
        return self.registrar

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

# Base conroller class that extends all the controllers
class Controller:

    def __init__(self, request):
        self.request = request

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

class Service:
    pass

class View:

    def __init__(self, config):
        self.config = config
        paths = self.config['path'].split('/')
        self.env = Environment(
            loader = PackageLoader(paths[0],paths[1]
        ))

    # returns a template object given file
    def get(self, file):
        return self.env.get_template(file + '.html')

    def source(self, file, *args, **kwargs):
        tpl = self.get(file)
        return tpl.render(*args, **kwargs)

    def render(self, file, *args, **kwargs):
        return Response(self.source(file, *args, **kwargs), mimetype='text/html')

class IoC:

    def __init__(self, instances = {}):
        self.instances = instances

    def bind(self, key, value):
        self.instances[key] = value

    def resolve(self, key):
        try:
            return self.instances[key]
        except:
            return None

# metaclass for facade class
class DeflectToInstance(type):

    def __getattr__(selfcls, a): # selfcls in order to make clear it is a class object (as we are a metaclass)
        try:
            # first, inquiry the class itself
            return super(DeflectToInstance, selfcls).__getattr__(a)
        except AttributeError:
            # Not found, so try to inquiry the instance attribute:
            return getattr(selfcls.instance, a)

# class ClassNameDescriptor:

#     def __get__(self, instance, owner):
#         return owner.__name__

# facade that is used to hold instances statically with boot method
class Facade:

    __metaclass__ = DeflectToInstance

    instance = None

    @classmethod
    def boot(cls, object, configuration = {}):
        if cls.instance is None:
            cls.instance = object(configuration)
