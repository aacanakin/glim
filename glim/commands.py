from command import GlimCommand
from termcolor import colored
from utils import copytree
from glim.facades import Log
import os
import traceback

class NewCommand(GlimCommand):

	name = 'new'
	description = 'generates a new glim app'

	def run(self, app):
		proto_path = 'glim/proto/project'
		currentpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

		try:
			copytree(proto_path, currentpath)
			print colored('A new glim app created successfully!', 'green')
		except Exception, e:
			print colored('App already exists', 'red')

class StartCommand(GlimCommand):

	name = 'start'
	description = 'start the glim app web server'

	def configure(self):
		self.add_argument("--host", help = "enter host", default = '127.0.0.1')
		self.add_argument("--port", help = "enter port", default = '8080')

	def run(self, app):
		Log.info('Glim server started on %s environment' % self.args.env)
		app.start(host = self.args.host, port = self.args.port)