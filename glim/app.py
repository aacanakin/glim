"""Module for app object

This module is responsible for instantiating a typical glim framework app.
It registers glim framework components, extensions and wsgi app.

"""

# application initiation script
import os
import sys
import traceback

from glim.facades import (Config, Database, Orm, Session, Cookie, IoC, View,
                          Log)
from glim.utils import import_module
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

    def __init__(self, commandadapter, env='default'):

        self.commandadapter = commandadapter

        self.mconfig = import_module('app.config.%s' % env)
        if self.mconfig is None:
            print(colored('Configuration for %s not found' % env, 'red'))
            exit()

        self.config = self.mconfig.config

        self.register_config()
        self.register_log()
        self.register_database()
        self.register_ioc()
        self.register_view()
        self.register_extensions()

        # find out start
        mstart = import_module('app.start')
        self.before = mstart.before

    def register_config(self):
        """Function registers the Config facade using Config(Registry)."""
        Config.register(self.config)

    def register_database(self):
        """

        Function registers the Orm and Database facades
        using glim.db.Orm and glim.db.Database.

        Note:
          It registers db.Database when 'db' key is defined in
            app.config.<env>.
          It registers db.Orm when 'orm' : True exists in app.config.<env>.

        Note:
          In configuration, 'orm' : True won't be able to register
          if 'db' key is absent in app.config.<env>.

        """
        if 'db' in self.config.keys():
            if self.config['db']:
                Database.register(self.config['db'])
                if 'orm' in self.config.keys():
                    if self.config['orm']:
                        Orm.register(Database.engines)

    def register_extensions(self, extensions=[]):
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

                # extension module base string
                ext_bstr = 'ext.%s' % (extension)

                # start script
                ext_sstr = '%s.start' % ext_bstr

                ext_startmodule = import_module(ext_sstr, pass_errors=True)
                if ext_startmodule is not None:
                    before = getattr(ext_startmodule, 'before')
                    before(config)

                # register extension commands if exists
                ext_cmdstr = '%s.%s' % (ext_bstr, 'commands')

                ext_cmd_module = import_module(ext_cmdstr, pass_errors=True)
                if ext_cmd_module is not None:
                    self.commandadapter.register_extension(
                        ext_cmd_module, extension)

        except Exception as e:
            print(traceback.format_exc())
            Log.error(e)

    def register_ioc(self):
        """Function registers IoC facade using IoC class in glim.core.IoC."""
        IoC.register()

    def register_view(self):
        """

        Function registers View facade using configuration in app.config.<env>.

        Note:
          The view layer will be disabled there isn't any 'view' key in
            app.config.<env>.

        """
        if 'views' in self.config:
            View.register(self.config['views'])

    def register_log(self):
        """

        Function registers Log facade using configuration in app.config.<env>.

        Note:
          The Log facade will be registered using default configuration
          if there isn't any 'log' key in app.config.<env>.

        """
        if 'log' in self.config:
            Log.register(self.config['log'])
        else:
            Log.register()

    def start(self, host='127.0.0.1', port='8080', env='development'):
        """

        Function initiates a werkzeug wsgi app using app.routes.py.

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

            if 'static' in self.config['app']:
                app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
                    self.config['app']['static']['url']:
                    self.config['app']['static']['path']
                })

            run_simple(host, int(port), app,
                       use_debugger=self.config['app']['debugger'],
                       use_reloader=self.config['app']['reloader'])

        except Exception as e:
            print(traceback.format_exc())
            exit()
