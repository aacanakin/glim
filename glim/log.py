"""
This module provides logging inside glim framework.
"""

from glim.core import Facade
from glim.exception import InvalidLoggerError
from termcolor import colored
import logging

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

CONFIG = {
    'glim': {
        'level': 'info',
        'format': '%(message)s',
        'colored': True,
        'file': None
    },
    'app': {
        'level': 'debug',
        'format': '%(message)s',
        'colored': True,
        'file': None
    }
}

class Log(object):
    """
    This class is the base for logging feature in glim.

    Attributes
    ----------
      config (dict): holds the configuration of logging.

    Usage
    -----
      log = Log(config)
      log.info("glim rocks") # prints a yellow colored msg
      log.error("whoopz") # prints a red colored msg
    """
    def __init__(self, name, config={}):

        if name not in CONFIG.keys():
            raise InvalidLoggerError("Invalid logger name %s" % name)

        if config:
            self.config = config
        else:
            self.config = CONFIG[name]

        self.logger = logging.getLogger(name)

        # set level
        level = LEVELS[self.config['level']] if 'level' in self.config else LEVELS['info']
        self.logger.setLevel(level)

        # create a log handler
        filepath = self.config['file'] if 'file' in self.config else None
        handler = None
        if filepath is None:
            handler = logging.StreamHandler()
        else:
            handler = logging.FileHandler(filepath)

        # set log format
        form = self.config['format'] if 'format' in self.config else None 
        formatter = logging.Formatter(form)
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def debug(self, msg):
        self.write(msg, LEVELS['debug'], 'cyan', attrs=['blink'])

    def info(self, msg):
        self.write(msg, LEVELS['info'], 'green')

    def warn(self, msg):
        self.write(msg, LEVELS['warning'], 'yellow', attrs=['reverse'])

    def error(self, msg):
        self.write(msg, LEVELS['error'], 'red')

    def critical(self, msg):
        self.write(msg, LEVELS['critical'], 'red', attrs=['reverse'])

    def write(self, msg, level=LEVELS['debug'], color=None, attrs=[]):
        if color is not None and self.config['colored']:
            msg = colored('%s' % msg, color, attrs=attrs)
        self.logger.log(level, '%s' % msg)


class LogFacade(Facade):
    accessor = Log


class GlimLogFacade(Facade):
    accessor = Log
