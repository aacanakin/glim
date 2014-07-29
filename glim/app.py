# application initiation script
import os, sys, traceback
from glim.core import Facade, Config as C, App
from glim.db import Database as D, Orm as O
from glim.facades import Config, Database, Orm, Session, Cookie

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect

class Glim:

    def __init__(self, urls = {}, environment = 'development'):

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
                ruleset[current_key] = k
            else:
                ruleset[current_key + key] = urls[key]
        return ruleset

    def dispatch_request(self, request):

        adapter = self.url_map.bind_to_environ(request.environ)

        try:
            endpoint, values = adapter.match()
            mcontroller = __import__('app.controllers', fromlist = ['controllers'])

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
                    response = getattr(ifilter, fnc)(** values)
                    if isinstance(response, Response):
                        return response

            cls = endpoint_pieces[0]

            restful = False
            try:
                fnc = endpoint_pieces[1]
            except:
                restful = True
                fnc = None

            obj = getattr(mcontroller, cls)
            instance = obj(request)
            if restful:
                return getattr(instance, request.method.lower())(** values)
            else:
                return getattr(instance, fnc)(** values)

        except HTTPException, e:
            return e

    def wsgi_app(self, environ, start_response):

        request = Request(environ)
        response = self.dispatch_request(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):

        return self.wsgi_app(environ, start_response)

def start(host = '127.0.0.1', port = '8080', environment = 'development', use_reloader = True):

    try :

        # boot config
        mconfig = __import__('app.config.%s' % environment, fromlist = ['config'])
        mroutes = __import__('app.routes', fromlist = ['routes'])

        registry = mconfig.config
        facades = mconfig.facades
        Config.boot(C, registry)

        # boot database
        if Config.get('db'):
            Database.boot(D, Config.get('db'))
            Orm.boot(O, Database.engines)

        # boot extensions
        extensions = mconfig.extensions
        for extension in extensions:

            extension_config = Config.get('extensions.%s' % extension)
            extension_mstr = 'ext.%s' % extension
            extension_module = __import__(extension_mstr, fromlist = [extension])

            extension_class = getattr(extension_module, extension.title())

            # check if extension is bootable
            if issubclass(extension_class, Facade):
                cextension_class = getattr(extension_module, '%sExtension' % (extension.title()))
                extension_class.boot(cextension_class, extension_config)

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

        app = Glim(mroutes.urls)

        run_simple(host, int(port), app, use_debugger = Config.get('glim.debugger'), use_reloader = Config.get('glim.reloader'))

    except Exception, e:

        print traceback.format_exc()
        print sys.exc_info()[0]
        exit()
