"""

This module holds the sqlalchemy models
for the app.

Example
-------
from glim import Model
from sqlalchemy import Column, Integer, String

class User(Model):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(255))
    title = Column(String(255))

    def __repr__(self):
        return "<User (name = %s,title = %s)>" % (self.full_name, self.title)

"""

from glim.db import Model
