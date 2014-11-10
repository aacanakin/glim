"""

The response module provides the werkzeug
wrapper object of any response that is returned
by controllers.

"""
from werkzeug.wrappers import Response as response

# an alias of werkzeug.wrappers.Response
Response = response
