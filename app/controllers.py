from glim.core import Controller
from werkzeug.wrappers import Response

from services import User

# controllers reside here

class BaseController(Controller):

    def hello(self):
        User.register(full_name = "Aras Can Akin", title = "glim developer")
        return Response('Welcome to glim!')
    def greet(self, name):
        return Response('Greetings %s' % name)

class RestfulController(Controller):

    def get(self):
        return Response('RESTful GET')

    def post(self):
        return Response('RESTful POST')

    def put(self):
        return Response('RESTful PUT')