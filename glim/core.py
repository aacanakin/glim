"""
This module holds the core classes of glim framework.
They're used inside glim framework and glim framework extensions.
"""


class Registry(object):
    """
    This class is basically a dictionary supercharged with
    useful functions.

    Attributes
    ----------
      registrar (dict): A registrar to hold a generic
        configuration of a class.

    Usage
    -----
      config = {
        'a' : 'b',
        'c' : {
            'd' : 'e'
        }
      }
      reg = Registry(config)
      reg.get('a') # returns b
      reg.get('c.d') # returns e
      reg.set('f', 'g') # sets 'f' key of dict
      reg.get('f') # returns g
    """
    def __init__(self, registrar):
        self.registrar = registrar

    def get(self, key):
        """
        Function deeply gets the key with "." notation

        Args
        ----
          key (string): A key with the "." notation.

        Returns
        -------
          reg (unknown type): Returns a dict or a primitive
            type.
        """
        try:
            layers = key.split('.')
            value = self.registrar
            for key in layers:
                value = value[key]
            return value
        except:
            return None

    def set(self, key, value):
        """
        Function deeply sets the key with "." notation

        Args
        ----
          key (string): A key with the "." notation.
          value (unknown type): A dict or a primitive type.
        """
        target = self.registrar
        for element in key.split('.')[:-1]:
            target = target.setdefault(element, dict())
        target[key.split(".")[-1]] = value

    def flush(self):
        """
        Function clears the registrar

        Note:
          After this function is called, all of your data
          in your registry will be lost. So, use this smartly.
        """
        self.registrar.clear()

    def update(self, registrar):
        """
        Function batch updates the registry. This function is an
        alias of dict.update()

        Args
        ----
          registrar (dict): A dict of configuration.

        Note:
          After this function is called, all of your data may be
          overriden and lost by the registrar you passed. So, use
          this smartly.
        """
        self.registrar.update(registrar)

    def all(self):
        """
        Function returns all the data in registrar.

        Returns
        -------
          registrar (dict): The current registry in the class.
        """
        return self.registrar

    def __str__(self):
        return self.registrar


class DeflectToInstance(type):
    """
    The magical class to deflect object calls to instances. This
    metaclass is used in Facade implemention. Thanks for the stackoverflow
    guy!
    """
    # selfcls in order to make clear it is a class object (as we are a
    # metaclass)

    def __getattr__(selfcls, a):
        try:
            # first, inquiry the class itself
            return super(DeflectToInstance, selfcls).__getattr__(a)
        except AttributeError:
            # Not found, so try to inquiry the instance attribute:
            return getattr(selfcls.instance, a)


# we are creating this MetaMixin class instance because Python 3 does not
# support the __metaclass__ attribute (as in Python 2), while Python 2 does not
# support the metaclass=DeflectToInstance keyword argument (as in Python 3). To
# solve the issue we create a basic class which is constructed with the right
# metaclass and then make Facade inherit from it.
MetaMixin = DeflectToInstance('MetaMixin', (object,), {})


# facade that is used to hold instances statically with boot method
class Facade(MetaMixin):
    """
    This magical class is basically a singleton implementation without
    using any kind of singleton :) It's used to register glim framework
    instances for only once and reach the class without disturbing readability.
    """

    instance = None

    # accessor is the object which will be registered during runtime
    accessor = None

    @classmethod
    def boot(cls, *args, **kwargs):
        """
        Function creates the instance of accessor with dynamic
        positional & keyword arguments.

        Args
        ----
          args (positional arguments): the positional arguments
            that are passed to the class of accessor.
          kwargs (keyword arguments): the keyword arguments
            that are passed to the class of accessor.
        """
        if cls.accessor is not None:
            if cls.instance is None:
                cls.instance = cls.accessor(*args, **kwargs)

    @classmethod
    def register(cls, config={}):
        """
        This function is basically a shortcut of boot for accessors
        that have only the config dict argument.

        Args
        ----
          config (dict): the configuration dictionary
        """
        if cls.accessor is not None:
            if cls.instance is None:
                cls.instance = cls.accessor(config)

    @classmethod
    def _get(cls):
        """Function returns the instance"""
        return cls.instance

