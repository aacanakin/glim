"""

The configuration module is responsible for
configuration management across the glim framework.

"""
from glim.core import Registry, Facade


class Config(Registry):

    """

    The configuration class is to hold framework level constants.
    It holds the dict in app.config.<env>.config.

    """


class ConfigFacade(Facade):
    accessor = Config
