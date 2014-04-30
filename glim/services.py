# facade classes
from glim.core import App

class Facade(object):
	key = None

	@staticmethod
	def __getattr__(self, attr):
		def default(* args):
			instance = App.resolve(key)
			method = getattr(instance, attr)
			return instance.method(args)

class Config(Facade):
	key = 'config'

class Session(Facade):
	key = 'session'

class Router(Facade):
	key = 'router'