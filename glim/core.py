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

# App class is a simple dependancy injection kit plus some more functionality
class App(object):

    registrar = {}

    @staticmethod
    def bind(key, value):
        App.registrar[key] = value

    @staticmethod
    def resolve(key):
        return App.registrar[key]

# Base conroller class that extends all the controllers
class Controller(object):

    restful = False

    def __init__(self, request, response):
        self.request = request
        self.response = response
        self.restful = restful

# Config class
class Config(Registry):
    pass

# Session class
class Session(Registry):
    pass

# Route class
class Router(Registry):
    pass
