"""

The controllers of a typical glim app.

Example
-------
from glim import Controller
from glim import View

class HelloController(Controller):
    def hello(self):
        # render the jinja template by binding data
        # renders app/views/hello.html
        return View.render('hello', name = 'Aras')

# for ajax requests, if you tend to send html source
# of a rendered template, use View.source(*args, **kwargs)

"""

from glim import Controller
import json


class BaseController(Controller):

    def hello(self):
        return json.dumps({
            'error': None,
            'msg': 'Welcome to glim!'
        })
