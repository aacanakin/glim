"""

The optional services layer of app.

Example
-------
from glim import Service
from glim import Orm
from models import User

class UserService(Service):
    @staticmethod
    def register(full_name = 'Aras Can Akin', title = 'glim developer'):

        # generate an instance of User
        user = User(full_name, title)

        # writes a new user to the database session
        Orm.add(user)

        # commits the transaction
        Orm.commit()
"""

from glim.component import Service
