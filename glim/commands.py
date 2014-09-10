import os
from termcolor import colored

from glim.command import GlimCommand
from glim.utils import copytree
from glim.facades import Log

import glim.paths as paths

class NewCommand(GlimCommand):

	name = 'new'
	description = 'generates a new glim app'

	def configure(self):
		self.add_argument("name", nargs='?', help="enter project name", default=None)

	def run(self, app):
		project_path = os.getcwd()
		if self.args.name is not None:
			project_path = os.path.join(project_path, self.args.name)

		proto_path = paths.PROTO_PATH

		try:
			copytree(proto_path, project_path)
			print colored('A new glim app created successfully!', 'green')
		except Exception, e:
			print e
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