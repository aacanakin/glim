"""

This module is the resource for framework level exceptions.

"""


class GlimError(Exception):
    pass

class FolderExistsError(GlimError):
	pass

class InvalidLoggerError(GlimError):
	pass