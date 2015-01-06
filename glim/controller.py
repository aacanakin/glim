"""

This module holds controller components of
a typical glim app.

"""


class Controller(object):

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
