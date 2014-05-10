# metaclass for Service class
class DeflectToInstance(type):
    def __getattr__(selfcls, a): # selfcls in order to make clear it is a class object (as we are a metaclass)
        try:
            # first, inquiry the class itself
            return super(DeflectToInstance, selfcls).__getattr__(a)
        except AttributeError:
            # Not found, so try to inquiry the instance attribute:
            return getattr(selfcls.instance, a)

# facade that is used for saving complex
class Service:
	__metaclass__ = DeflectToInstance

	instance = None

	@classmethod
	def boot(cls, object, configuration = {}):
		if cls.instance is None:
			cls.instance = object(configuration)	

class Config(Service):
	pass

class Session(Service):
	pass

class Router(Service):
	pass