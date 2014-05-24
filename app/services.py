# services who interact with models
from glim.core import Service
from glim.facades import Database as DB
from models import User

class User(Service):
	@staticmethod
	def register(full_name = 'Aras Can', title = 'glim developer'):
		DB.execute("INSERT INTO users (full_name, title) VALUES ('%s', '%s')" % (full_name, title))
		# user = User(full_name = 'Aras Can Akin', title = 'glim developer')
		# print User.__table__
		# DB.session().add(user)
		# DB.session().commit()