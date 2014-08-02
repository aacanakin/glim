from glim.core import Controller
from glim.facades import View

class BaseController(Controller):
	def hello(self):
		return View.render('hello', name = 'Aras')