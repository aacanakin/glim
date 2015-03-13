"""
The controllers of a typical glim app.

Example - Html rendering
------------------------
from glim import Controller
from glim_extensions.view import View

class HelloController(Controller):
    def hello(self):
        # render the jinja template by binding data
        # renders app/views/hello.html
        return View.render('hello', name = 'Aras')

# for ajax requests, if you tend to send html source
# of a rendered template, use View.source(*args, **kwargs)

Example - JsonResponse
----------------------
from glim import Controller

class BaseController(Controller):
	def hello(self):
		return {'error': None}
		# outputs {"error": null} with application/json header
"""

from glim import Controller

class AppController(Controller):
	def ping(self):
		return {'error': None, 'message': 'pong'}
