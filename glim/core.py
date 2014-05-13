# core module has all the cool stuff

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

# Route class
class Router(Registry):
    pass

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

# metaclass for Service class
class DeflectToInstance(type):
    def __getattr__(selfcls, a): # selfcls in order to make clear it is a class object (as we are a metaclass)
        try:
            # first, inquiry the class itself
            return super(DeflectToInstance, selfcls).__getattr__(a)
        except AttributeError:
            # Not found, so try to inquiry the instance attribute:
            return getattr(selfcls.instance, a)

# SERVICES

# facade that is used for saving complex
class Service:
    __metaclass__ = DeflectToInstance

    instance = None

    @classmethod
    def boot(cls, object, configuration = {}):
        if cls.instance is None:
            cls.instance = object(configuration)