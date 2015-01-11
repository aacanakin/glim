"""

This module is responsible for instantiating a typical glim framework app.
It registers glim framework components, extensions and wsgi app.

"""


# application initiation script
import os
import sys
import traceback

from glim import Config, Log, GlimLog
from glim.utils import import_module, empty
from glim.dispatch import Glim

import glim.paths as paths

from werkzeug.serving import run_simple
from werkzeug.wsgi import SharedDataMiddleware
from termcolor import colored


class App:

    """

    This class is responsible for registering the components of
    a typical glim framework app

    Attributes
    ----------
      commandadapter (glim.command.CommandAdapter):
        The commandadapter object which is responsible for dispatching commands
      env (string):
        application environment variable passed from command line
      mconfig (module):
        The configuration module imported from app.config.<env>
      config (dict):
        The configuration dictionary by environment which resides in
            app.config.<env>
      before (method):
        The before hook function for registering a function before app starts

    """

    def __init__(self, commandadapter, mconfig=None, env='default', before=None):

        self.commandadapter = commandadapter
        self.config = mconfig.config

        self.register_config()
        self.register_log()
        self.register_extensions()

        self.before = before

    def register_config(self):
        """Function registers the Config facade using Config(Registry)."""
        Config.register(self.config)

    def register_extensions(self):
        """

        Function registers extensions given extensions list

        Args
        ----
          extensions (list) : the extensions dict on app.config.<env>

        Raises
        ------
          Exception: Raises exception when extension can't be loaded
            properly.

        """
        try:
            for extension, config in self.config['extensions'].items():

                extension_bstr = ''

                # gather package name if exists
                extension_pieces = extension.split('.')

                # if the extensions is not in glim_extensions package
                if len(extension_pieces) > 1:
                    extension_bstr = '.'.join(extension_pieces)
                else: # if the extension is in glim_extensions package
                    extension_bstr = 'glim_extensions.%s' % extension_pieces[0]

                extension_module = import_module(extension_bstr)

                if extension_module:
                    extension_startstr = '%s.%s' % (extension_bstr, 'start')
                    extension_start = import_module(extension_startstr, pass_errors=True)

                    extension_cmdsstr = '%s.%s' % (extension_bstr, 'commands')
                    extension_cmds = import_module(extension_cmdsstr, pass_errors=True)

                    if extension_start is not None:
                        before = extension_start.before
                        before(config)

                    if extension_cmds is not None:
                        self.commandadapter.register_extension(extension_cmds, extension_pieces[0])
                else:
                    GlimLog.error('Extension %s could not be loaded' % extension)

        except Exception as e:
            GlimLog.error(traceback.format_exc())

    def register_log(self):
        """

        Function registers Log facade using configuration in app.config.<env>.

        Note:
          The Log facade will be registered using default configuration
          if there isn't any 'log' key in app.config.<env>.

        """
        if not empty('log', self.config):

            if not empty('glim', self.config['log']):
                GlimLog.boot(name='glim', config=self.config['log']['glim'])
            else:
                GlimLog.boot(name='glim')

            if not empty('app', self.config['log']):
                Log.boot(name='app', config=self.config['log']['app'])
            else:
                Log.boot(name='app')
        else:
            Log.boot(name='app')
            GlimLog.boot(name='glim')

    def start(self, host='127.0.0.1', port='8080', env='development'):
        """

        Function initiates a werkzeug wsgi app using app.routes module.

        Note:
          Function will register a static path for css, js, img, etc. files
          using SharedDataMiddleware, else it won't register any static script
          path.

        Args
        ----
          host (string): the host ip address to start the web server
          port (string): the port of ip address
          env  (string): the application environment

        Raises
        ------
          Exception: Raises any exception coming from werkzeug's web server

        """
        try:
            self.before()
            mroutes = import_module('app.routes')
            app = Glim(mroutes.urls, self.config['app'])

            if 'assets' in self.config['app']:
                app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
                    self.config['app']['assets']['url']:
                    self.config['app']['assets']['path']
                })

            run_simple(host, int(port), app,
                       use_debugger=self.config['app']['debugger'],
                       use_reloader=self.config['app']['reloader'])

        except Exception as e:
            print(traceback.format_exc())
            exit()
