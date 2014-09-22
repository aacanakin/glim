"""

The optional services layer of app.

Example
-------
from glim.core import Service
from glim.facades import Orm as ORM
from models import User

class UserService(Service):
    @staticmethod
    def register(full_name = 'Aras Can Akin', title = 'glim developer'):

        # generate an instance of User
        user = User(full_name, title)

        # writes a new user to the database session
        ORM.add(user)

        # commits the transaction
        ORM.commit()
"""

from glim.component import Service
