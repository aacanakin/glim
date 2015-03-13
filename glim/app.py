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
import glim.paths as paths

from termcolor import colored
from bottle import Bottle, route, request, response

class Glim(object):
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
    def __init__(self, commandadapter, mconfig=None, mroutes=None, mcontrollers=None, env='default', before=None):

        # register app
        self.commandadapter = commandadapter
        self.config = mconfig.config
        self.urls = mroutes.urls
        self.mcontrollers = mcontrollers;

        self.wsgi = Bottle()
        self.register_config()
        self.register_log()
        self.register_extensions()
        self.register_ssl_context()
        self.register_routes()

        self.before = before
        self.before()

    def register_config(self):
        """
        Function registers the Config facade using Config(Registry).
        """
        Config.register(self.config)

    def register_routes(self):
        """
        Function creates instances of controllers, adds into bottle routes
        """
        routes = self.flatten_urls(self.urls)
        self.controllers = {}
        controller_names = set()

        for route in routes:
            cname = route['endpoint'].split('.')[0]
            controller_names.add(cname)

        for cname in controller_names:
            attr = getattr(self.mcontrollers, cname)
            instance = attr(request, response)
            self.controllers[cname] = instance

        for route in routes:
            cname, aname = route['endpoint'].split('.')
            action = getattr(self.controllers[cname], aname)
            self.wsgi.route(route['url'], route['methods'], action)

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
                        if self.commandadapter is not None:
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

    def register_ssl_context(self):
        """
        Function detects ssl context
        """
        if not empty('ssl', self.config['app']):
            self.ssl_context = self.config['app']['ssl']
        else:
            self.ssl_context = None

    def flatten_urls(self, urls):
        """
        Function flatten urls for route grouping feature of glim.

        Args
        ----
          urls (dict): a dict of url definitions.
          current_key (unknown type): a dict or a string marking the
            current key that is used for recursive calls.
          ruleset (dict): the ruleset that is eventually returned to
            dispatcher.

        Returns
        -------
          ruleset (list): a list of ruleset dict with endpoint, url and method functions
        """
        available_methods = ['POST', 'PUT', 'OPTIONS', 'GET', 'DELETE', 'TRACE', 'COPY']
        ruleset = []
        for route, endpoint in urls.items():
            route_pieces = route.split(' ')
            try:
                methods = url = None
                if len(route_pieces) > 1:
                    methods = [route_pieces[0]]
                    url = route_pieces[1]
                else:
                    methods = available_methods
                    url = route_pieces[0]

                endpoint_pieces = endpoint.split('.')

                if len(endpoint_pieces) > 1:
                    rule = {'url': url, 'endpoint': endpoint, 'methods': methods}
                    ruleset.append(rule)
                else:
                    for method in available_methods:
                        rule = {
                            'url': url,
                            'endpoint': '%s.%s' % (endpoint, method.lower()),
                            'methods': [method]
                        }
                        ruleset.append(rule)
            except Exception as e:
                raise InvalidRouteDefinitionError()
        return ruleset
