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
      request (bottle.request): Thread safe bottle request object
      response (bottle.response): Thread safe bottle response object
    """
    def __init__(self, request, response):
        self.request = request
        self.response = response
