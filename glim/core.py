from werkzeug.wrappers import Response as response

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
        for element in key.split('.')[:-1]:
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

Response = response

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

    # selfcls in order to make clear it is a class object (as we are a metaclass)
    def __getattr__(selfcls, a):
        try:
            # first, inquiry the class itself
            return super(DeflectToInstance, selfcls).__getattr__(a)
        except AttributeError:
            # Not found, so try to inquiry the instance attribute:
            return getattr(selfcls.instance, a)

# facade that is used to hold instances statically with boot method
class Facade:

    __metaclass__ = DeflectToInstance

    instance = None

    # accessor is the object which will be registered during runtime
    accessor = None

    @classmethod
    def boot(cls, *args, **kwargs):
        if cls.accessor is not None:
            if cls.instance is None:
                cls.instance = cls.accessor(*args, **kwargs)

    @classmethod
    def register(cls, config = {}):
        if cls.accessor is not None:
            if cls.instance is None:
                cls.instance = cls.accessor(config)

    @classmethod
    def _get(cls):
        return cls.instance