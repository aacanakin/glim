"""

The commands module provides developer defined commands
to the project.

Example
-------
from glim import Command

class HelloCommand(Command):

    name = 'hello'
    description = 'print hello given name'

    def configure(self):
        self.add_argument("--name", help = 'enter your name')

    def run(self, app):
        if self.args.name is not None:
            print 'hello %s' % self.args.name
        else:
            print 'hello'

you can access to this commands to run the following;

$ glim hello --name aras
# outputs hello aras

"""
from glim import Command
