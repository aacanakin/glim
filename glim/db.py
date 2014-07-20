from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.
from sqlalchemy import create_engine
from glim.core import Registry

class Migration:
	def __init__(self, connection):
		self.connection = connection

	def up(self):
		return

	def down(self):
		return

def Schema:
	def __init__(self, connection):
		self.connection = connection

	def create(self):
		pass

	def alter(self):
		pass

	def drop(self):
		pass