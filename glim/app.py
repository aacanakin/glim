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

from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.contrib.sessions import FilesystemSessionStore

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

        self.register_config()
        self.register_log()
        self.register_extensions()
        self.register_ssl_context()

        self.before = before

        # register session store
        try:
            self.session_store = FilesystemSessionStore(self.config['sessions']['path'])
        except:
            self.session_store = None

        # process routes, register urls
        ruleset = self.flatten_urls(self.urls)
        rule_map = []
        for rule in ruleset:
            rule_map.append(Rule(rule['url'], endpoint=rule['endpoint'], methods=rule['methods']))

        self.url_map = Map(rule_map)

        self.before()

        if 'assets' in self.config['app']:
            assets_url = self.config['app']['assets']['url']
            assets_path = self.config['app']['assets']['path']
            self.wsgi_app = SharedDataMiddleware(self.wsgi_app, {assets_url: assets_path})

    def register_config(self):
        """
        Function registers the Config facade using Config(Registry).
        """
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

    def dispatch_request(self, request):
        """
        Function dispatches the request. It also handles route
        filtering.

        Args
        ----
          request (werkzeug.wrappers.Request): the request
            object.

        Returns
        -------
          response (werkzeug.wrappers.Response): the response
            object.
        """
        adapter = self.url_map.bind_to_environ(request.environ)

        try:

            endpoint, values = adapter.match()

            cls, func = endpoint.split('.')
            if hasattr(self.mcontrollers, cls):
                obj = getattr(self.mcontrollers, cls)
                instance = obj(request)

                if hasattr(instance, func):
                    raw = getattr(instance, func)(** values)
                    if isinstance(raw, Response):
                        return raw
                    else:
                        return Response(raw)
            if self.config['app']['debugger']:
                raise AttributeError("Controller function is not found for endpoint %s" % endpoint)
            else:
                raise NotFound()

        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        """
        Function returns the wsgi app of glim framework.

        Args
        ----
          environ (unknown type): The werkzeug environment.
          start_response (function): The werkzeug's start_response
            function.

        Returns
        -------
          response (werkzeug.wrappers.Response): the dispatched response
            object.
        """
        request = Request(environ)

        if self.session_store is not None:

            sid = request.cookies.get(self.config['sessions']['id_header'])

            if sid is None:
                request.session = self.session_store.new()
            else:
                request.session = self.session_store.get(sid)

        response = self.dispatch_request(request)

        if self.session_store is not None:
            if request.session.should_save:
                self.session_store.save(request.session)
                response.set_cookie(self.config['sessions']['id_header'],
                                    request.session.sid)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        """
        Function returns wsgi app when it is instantiated
        """
        return self.wsgi_app(environ, start_response)
