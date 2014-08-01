# application initiation script
import os, sys, traceback
from glim.core import Facade, Config as C, IoC as ioc
from glim.db import Database as D, Orm as O
from glim.facades import Config, Database, Orm, Session, Cookie, IoC

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect

from termcolor import colored

def import_module(module, frm):

    try:

        m = __import__(module, fromlist = [frm])
        return m

    except Exception, e:

        print traceback.format_exc()
        exit()

class Glim:

    def __init__(self, urls = {}):

        ruleset = self.flatten_urls(urls)
        rule_map = []
        for url,rule in ruleset.items():
            rule_map.append(Rule(url, endpoint = rule))

        self.url_map = Map(rule_map)

    def flatten_urls(self, urls, current_key = "", ruleset = {}):

        for key in urls:
            # If the value is of type `dict`, then recurse with the value
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

        adapter = self.url_map.bind_to_environ(request.environ)

        try:

            endpoint, values = adapter.match()
            mcontroller = import_module('app.controllers', 'controllers')

            # detect filters
            filters = endpoint.split(',')
            endpoint_pieces = filters[-1].split('.')

            # if there exists any filter defined
            if len(filters) > 1:

                filters = filters[:-1]
                # here run filters
                for f in filters:

                    fpieces = f.split('.')
                    cls = fpieces[0]
                    fnc = fpieces[1]
                    mfilter = __import__('app.controllers', fromlist = ['controllers'])
                    obj = getattr(mfilter, cls)
                    ifilter = obj(request)
                    raw = getattr(ifilter, fnc)(** values)

                    if isinstance(raw, basestring):
                        return Response(raw)

                    if isinstance(raw, Response):
                        return raw

            cls = endpoint_pieces[0]

            restful = False
            try:
                fnc = endpoint_pieces[1]
            except:
                restful = True
                fnc = None

            obj = getattr(mcontroller, cls)
            instance = obj(request)

            raw = None
            if restful:
                raw = getattr(instance, request.method.lower()(** values))
            else:
                raw = getattr(instance, fnc)(** values)

            if isinstance(raw, Response):

                print 'response is Response()'
                return raw

            elif isinstance(raw, basestring):

                print 'response is string'
                return Response(raw)

            else:
                return Response('not found')

        except HTTPException, e:
            return e

    def wsgi_app(self, environ, start_response):

        request = Request(environ)
        response = self.dispatch_request(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):

        return self.wsgi_app(environ, start_response)

class App:

    def __init__(self, host = '127.0.0.1', port = 8080,  env = 'development'):

        self.mconfig = import_module(module = 'app.config.%s' % env, frm = 'config')
        self.boot_config()
        self.boot_db()
        self.boot_facades()
        self.boot_extensions()
        self.boot_ioc()

        # find out start
        mstart = import_module('app.start', 'start')
        self.before = mstart.before    

    def boot_config(self):

        registry = self.mconfig.config
        Config.boot(C, registry)

    def boot_db(self):

        if Config.get('db'):
            Database.boot(D, Config.get('db'))
            Orm.boot(o, Database.engines)

    def boot_facades(self):

        try:

            facades = self.mconfig.facades

            # boot facades
            for facade in facades:
                core_mstr = 'glim.core'
                facade_mstr = 'glim.facades'

                fromlist = facade

                core_module = __import__(core_mstr, fromlist = [facade])
                facade_module = __import__(facade_mstr, fromlist = [fromlist])

                core_class = getattr(core_module, facade)
                facade_class = getattr(facade_module, facade)

                config = Config.get(facade.lower())
                facade_class.boot(core_class, config)

        except Exception, e:

            print traceback.format_exc()
            exit()

    def boot_extensions(self, extensions = []):

        try:

            extensions = self.mconfig.extensions

            for extension in extensions:

                extension_config = Config.get('extensions.%s' % extension)
                extension_mstr = 'ext.%s' % extension
                extension_module = import_module(extension_mstr, extension)

                extension_class = getattr(extension_module, extension.title())

                # check if extension is bootable
                if issubclass(extension_class, Facade):

                    cextension_class = getattr(extension_module, '%sExtension' % (extension.title()))
                    extension_class.boot(cextension_class, extension_config)

        except Exception, e:

            print traceback.format_exc()
            exit()

    def boot_ioc(self):
        IoC.boot(ioc)

    def start(self, host = '127.0.0.1', port = '8080', env = 'development'):

        try:

            self.before()
            mroutes = import_module('app.routes', 'routes')
            app = Glim(mroutes.urls)
            print colored('Glim server started on %s environment' % env, 'green')
            run_simple(host, int(port), app, use_debugger = Config.get('glim.debugger'), use_reloader = Config.get('glim.reloader'))

        except Exception, e:

            print traceback.format_exc()
            exit()