# application initiation script
import os
from glim.core import Config as C,App
from glim.services import Config

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect

class Glim:

    def __init__(self, urls = [], environment = 'development'):

        self.urls = urls
        rule_map = []
        for raw_rule in self.urls:
            for k,v in raw_rule.items():
                rule_map.append(Rule(k, endpoint = v))

        self.url_map = Map(rule_map)

    def dispatch_request(self, request):

        adapter = self.url_map.bind_to_environ(request.environ)

        try:
            endpoint, values = adapter.match()
            print 'endpoint %s' % endpoint
            mcontroller = __import__('app.controllers', fromlist = ['controllers'])
            endpoint_pieces = endpoint.split('.')
            cls = endpoint_pieces[0]

            restful = False
            try :
                fnc = endpoint_pieces[1]
            except:
                restful = True
                fnc = None

            obj = getattr(mcontroller, cls)
            instance = obj(request)
            if restful:
                return getattr(instance, request.method.lower())(** values)
            else :
                return getattr(instance, fnc)(** values)

        except HTTPException, e:
            return e

        return Response('Welcome to Glim')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def start(host = '127.0.0.1', port = '8080', environment = 'development', with_static = False, use_reloader = True):

    try :

        mconfig = __import__('app.config.%s' % environment, fromlist = ['config'])
        mroutes = __import__('app.routes', fromlist = ['routes'])

        registry = mconfig.config
        services = mconfig.services
        Config.boot(C, registry)

        app = Glim(mroutes.urls)

        if with_static:
            app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
                '/static':  os.path.join(os.path.dirname(__file__), 'app/static')
            })

        run_simple(host, int(port), app, use_debugger = True, use_reloader = True)

        # service bootups
        # for service in services:
        #     fromlist = service.split('.')[-1]
        #     module = '.'.join(service.split('.')[0:2])
        #     m = __import__(module, fromlist = [fromlist])
        #     service_conf =

        # print 'fromlist = %s' % fromlist
        # print 'module = %s' % module
        # print 'service = %s' % service
        # print 'm = %s' % m

    except Exception, e:

        print e
        exit()
