"""

This module holds the Facade classes of core objects. These
facades are registered by the glim.app.App in constructor.

Usage
-----
from glim.facades import Config
Config.get('hello') # calls the function of glim.core.Config

"""

from glim.core import Facade, Config as config, IoC as ioc
from glim.db import Database as database, Orm as orm
from glim.component import View as view
from glim.log import Log as log


class Config(Facade):
    accessor = config


class Session(Facade):
    pass


class Cookie(Facade):
    pass


class Database(Facade):
    accessor = database


class Orm(Facade):
    accessor = orm


class IoC(Facade):
    accessor = ioc


class View(Facade):
    accessor = view


class Log(Facade):
    accessor = log
