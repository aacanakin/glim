# application initiation script
import os, sys, traceback

from glim.core import Facade, Config as config, IoC as ioc
from glim.component import View as view
from glim.db import Database as database, Orm as orm
from glim.log import Log as log
from glim.facades import Config, Database, Orm, Session, Cookie, IoC, View, Log
from glim.utils import import_module
from glim.dispatch import Glim

import glim.paths as paths

from werkzeug.serving import run_simple
from werkzeug.wsgi import SharedDataMiddleware
from termcolor import colored

class App:

    def __init__(self, commandadapter, env = 'development'):

        self.commandadapter = commandadapter

        self.mconfig = import_module('app.config.%s' % env)
        if self.mconfig is None:
            print colored('Configuration for %s not found' % env, 'red')
            exit()

        self.config = self.mconfig.config

        self.register_config()
        self.register_log()
        self.register_database()
        self.register_extensions()
        self.register_ioc()
        self.register_view()
        
        # find out start
        mstart = import_module('app.start')
        self.before = mstart.before

    def register_config(self):
        Config.register(config, self.config)

    def register_database(self):
        if 'db' in self.config.keys():
            Database.register(database, self.config['db'])
            Orm.register(orm, Database.engines)

    def register_extensions(self, extensions = []):
        try:
            for extension, config in self.config['extensions'].items():

                # extension module base string
                ext_bstr = 'ext.%s' % (extension)

                # extension core module string
                ext_cmstr = '%s.%s' % (ext_bstr, extension)

                # extension module object
                ext_module = import_module(ext_cmstr)

                # extension class
                ext_class = getattr(ext_module, extension.title())

                # check if extension is bootable
                if issubclass(ext_class, Facade):
                    cext_class = getattr(ext_module, '%sExtension' % (extension.title()))
                    ext_class.register(cext_class, config)

                # register extension commands if exists
                ext_cmdstr = '%s.%s' % (ext_bstr, 'commands')

                ext_cmd_module = import_module(ext_cmdstr, pass_errors = True)
                if ext_cmd_module is not None:
                    self.commandadapter.register_extension(ext_cmd_module, extension)

        except Exception, e:
            Log.error(e)

    def register_ioc(self):
        IoC.register(ioc)

    def register_view(self):
        if 'views' in self.config:
            View.register(view, self.config['views'])

    def register_log(self):
        if 'log' in self.config:
            Log.register(log, self.config['log'])
        else:
            Log.register(log)

    def start(self, host = '127.0.0.1', port = '8080', env = 'development', with_static = True):
        try:
            self.before()
            mroutes = import_module('app.routes')
            app = Glim(mroutes.urls, self.config['app'])

            if with_static:
                dirname = os.path.dirname
                static_path = os.path.join(dirname(dirname(__file__)), 'app/static')
                app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
                    '/static' : static_path
                })

            run_simple(host, int(port), app, use_debugger = self.config['app']['debugger'], use_reloader = self.config['app']['reloader'])

        except Exception, e:
            print traceback.format_exc()
            exit()