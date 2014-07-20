# services who interact with models
from glim.core import Service
from glim.facades import Database as DB
from models import User

class UserService(Service):
	@staticmethod
	def register():
	# def register(full_name = 'Aras Can', title = 'glim developer'):
		# DB.execute("INSERT INTO users (full_name, title) VALUES ('%s', '%s')" % (full_name, title))
		user = User(fullname = "Aras Can Akin", title = "glim developer")		
		
		DB.session().add(user)
		DB.session().commit()