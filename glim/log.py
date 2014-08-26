from termcolor import colored
import logging

class Log:

	LEVELS = {
		'debug'   : logging.DEBUG,
		'info'    : logging.INFO,
		'warning' : logging.WARNING,
		'error'   : logging.ERROR,
		'critical': logging.CRITICAL
	}

	CONFIG = {
		'level' : 'debug',
		'format' : '%(message)s',
	}

	def __init__(self, config = {}):
		if config:
			self.config = config
		else:
			self.config = Log.CONFIG

		lvl = Log.LEVELS[self.config['level']] if ('level' in self.config) else Log.LEVELS['info']
		filepath = self.config['file'] if 'file' in self.config else None
		fmt = self.config['format'] if 'format' in self.config else None

		logging.basicConfig(filename = filepath, level = lvl, format = fmt)

	def info(self, msg):
		logging.info(colored(msg, 'green'))

	def warning(self, msg):
		logging.warning(colored(msg, 'yellow', attrs = ['reverse']))

	def debug(self, msg):
		logging.debug(colored(msg, 'cyan', attrs = ['blink']))

	def error(self, msg):
		logging.debug(colored(msg, 'red'))

	def critical(self, msg):
		logging.critical(colored(msg, 'red', attrs = ['reverse']))
