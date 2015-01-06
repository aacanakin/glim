"""

This module holds the components of a typical glim
framework app.

"""

from werkzeug.wrappers import Response
from glim.core import Registry


class Service(object):

    """

    The base class of Service layer. Currently, it is optional to extend.
    In service layer, it's recommended to use @staticmethod s if they are
    not holding states. Services layer is initially introduced for seperating
    database logic from SQLAlchemy models.

    """
    pass
