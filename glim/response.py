"""

The response module provides the werkzeug
wrapper object of any response that is returned
by controllers.

"""
import json
from werkzeug.wrappers import Response as response

# an alias of werkzeug.wrappers.Response
Response = response

class JsonResponse(Response):
    """
    The JsonResponse is an alias of response with response data as dict


    Attributes
    ----------
      response (dict): The response dictionary to be converted to json object
      status (int): Integer HTTP status code
      headers (dict): A dictionary of headers to make the response
      mimetype (string): The mimetype of response
      direct_passthrough (bool): Boolean value if werkzeug passthrough is chosen or not
    """
    def __init__(self, response=None,
                 status=None, headers=None,
                 mimetype=None, content_type=None,
                 direct_passthrough=False):
        if response:
            response = json.dumps(response)
        Response.__init__(self, response=response, status=status,
                          headers=headers, mimetype=mimetype,
                          content_type=content_type,
                          direct_passthrough=direct_passthrough)
