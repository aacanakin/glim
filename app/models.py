# from glim.core import Model
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from glim.facades import Database as DB

Base = declarative_base()
Base.metadata.create_all(DB.engine())

class User(Base):
	__tablename__ = 'users'
	user_id = Column(Integer, primary_key = True)
	full_name = Column(String)
	title = Column(String)

	def __repr__(self):
		return "<User (name = %s,title = %s)" % (self.full_name, self.title)

print User.__table__