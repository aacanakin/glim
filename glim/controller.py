"""

This module holds controller components of
a typical glim app.

"""


class Controller:

    """

    The controller component is responsible for handling requests
    and returning appropriate response to the requests.

    Attributes
    ----------
      request (werkzeug.wrappers.Request): The current request
        object. This object is automatically passed by dispatch
        module.

    """

    def __init__(self, request):
        self.request = request


class RestController(Controller):

    """

    The rest controller is simply a shortcut to make the controller
    restful. The dispatcher calls the following functions according
    to the request method.

    """

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
