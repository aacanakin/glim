"""
This module holds commands of internal
glim framework commands to manipulate
a typical glim framework app.
"""


import os, traceback
from termcolor import colored

from werkzeug.serving import run_simple
from glim.command import GlimCommand
from glim.utils import copytree
from glim.exception import FolderExistsError
from glim import GlimLog, Config

import glim.paths as paths


class NewCommand(GlimCommand):
    """
    This class is responsible for generating a new glim app.

    Attributes
    ----------
      glim.command.GlimCommand Attributes
    """
    name = 'new'
    description = 'generates a new glim app'

    def configure(self):
        """
        Function adds the optional name argument for creating an app with
        project name.
        """
        self.add_argument("name", nargs='?', help="enter project name", default=None)

    def run(self, app):
        """Function copies the prototype folder into os.getcwd() path."""
        project_path = os.getcwd()
        if self.args.name is not None:
            project_path = os.path.join(project_path, self.args.name)

        proto_path = paths.PROTO_PATH

        try:
            copytree(proto_path, project_path)
            print(colored('A new glim app created successfully! Happy coding :)', 'green'))
        except FolderExistsError as e:
            print(e)
            print(colored('App already exists', 'red'))


class StartCommand(GlimCommand):
    """
    This class is responsible for starting wsgi of glim framework app.

    Attributes
    ----------
      glim.command.GlimCommand Attributes
    """
    name = 'start'
    description = 'start the glim app web server'

    def configure(self):
        """Function adds optional host, port variables."""
        self.add_argument("--host", help="enter host", default='127.0.0.1')
        self.add_argument("--port", help="enter port", default='8080')

    def run(self, app):
        """Function starts the web server given configuration."""
        GlimLog.info('Glim server started on %s environment' % self.args.env)
        try:
            extra_files = None
            if Config.get('app.reloader'):
                extra_dirs = [Config.get('app.assets.path'), ]
                extra_files = extra_dirs[:]
                for extra_dir in extra_dirs:
                    for dirname, dirs, files in os.walk(extra_dir):
                        for filename in files:
                            filename = os.path.join(dirname, filename)
                            if os.path.isfile(filename):
                                extra_files.append(filename)

            run_simple(self.args.host, int(self.args.port), app,
                       use_debugger=Config.get('app.debugger'),
                       use_reloader=Config.get('app.reloader'),
                       ssl_context=app.ssl_context,
                       reloader_type='stat',
                       extra_files=extra_files)

        except Exception as e:
            print(traceback.format_exc())
            exit()
