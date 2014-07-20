# from glim.core import Model
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from glim.facades import Database as DB

print 'base is not defined'
Base = declarative_base()
print 'base is defined'

class User(Base):

	__tablename__ = 'users'
	id = Column(Integer, primary_key = True)
	fullname = Column(String(255))
	title = Column(String(255))

	def __repr__(self):
		return "<User (name = %s,title = %s)" % (self.full_name, self.title)