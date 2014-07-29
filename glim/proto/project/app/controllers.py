from glim.core import Controller
from werkzeug.wrappers import Response

class BaseController(Controller):
	def hello(self):
		return Response('Welcome to glim!')