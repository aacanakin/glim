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

from werkzeug.serving import run_simple
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.utils import redirect
from werkzeug.contrib.sessions import FilesystemSessionStore
from termcolor import colored

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
            self.session_store = FilesystemSessionStore(
                self.config['sessions']['path'])
        except:
            self.session_store = None

        # process routes, register urls
        ruleset = self.flatten_urls(self.urls)
        rule_map = []
        for url, rule in ruleset.items():
            rule_map.append(Rule(url, endpoint=rule))

        self.url_map = Map(rule_map)

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

    def flatten_urls(self, urls, current_key="", ruleset={}):
        """
        Function flatten urls for route grouping feature of glim. Thanks
        for the stackoverflow guy!

        Args
        ----
          urls (dict): a dict of url definitions.
          current_key (unknown type): a dict or a string marking the
            current key that is used for recursive calls.
          ruleset (dict): the ruleset that is eventually returned to
            dispatcher.

        Returns
        -------
          ruleset (dict): the ruleset to be bound.
        """
        for key in urls:
            # If the value is of type `dict`, then recurse with the
            # value
            if isinstance(urls[key], dict):
                self.flatten_urls(urls[key], current_key + key)
            # Else if the value is type of list, meaning it is a filter
            elif isinstance(urls[key], (list, tuple)):
                k = ','.join(urls[key])
                ruleset[current_key + key] = k
            else:
                ruleset[current_key + key] = urls[key]

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

            endpoint_pieces = endpoint.split('.')
            cls = endpoint_pieces[0]

            restful = False
            fnc = None
            if len(endpoint_pieces) is 1:
                restful = True
            else:
                fnc = endpoint_pieces[1]

            obj = getattr(self.mcontrollers, cls)
            instance = obj(request)

            raw = None
            if restful:
                raw = getattr(instance, request.method.lower())(**values)
            else:
                raw = getattr(instance, fnc)(** values)

            if isinstance(raw, Response):
                return raw
            else:
                return Response(raw)

        #TODO: add other type of exceptions for better Exception handling
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

            if 'assets' in self.config['app']:
                self.wsgi_app = SharedDataMiddleware(self.wsgi_app, {
                    self.config['app']['assets']['url']:
                    self.config['app']['assets']['path']
                })

            # stat poll static files if assets is defined
            extra_files = None
            if self.config['app']['reloader']:
                extra_dirs = [self.config['app']['assets']['path'], ]
                extra_files = extra_dirs[:]
                for extra_dir in extra_dirs:
                    for dirname, dirs, files in os.walk(extra_dir):
                        for filename in files:
                            filename = os.path.join(dirname, filename)
                            if os.path.isfile(filename):
                                extra_files.append(filename)

            run_simple(host, int(port), self,
                   use_debugger=self.config['app']['debugger'],
                   use_reloader=self.config['app']['reloader'],
                   ssl_context=self.ssl_context,
                   reloader_type='stat',
                   extra_files=extra_files)

        except Exception as e:
            print(traceback.format_exc())
            exit()


    def __call__(self, environ, start_response):
        """
        Function returns wsgi app when it is instantiated
        """
        return self.wsgi_app(environ, start_response)
