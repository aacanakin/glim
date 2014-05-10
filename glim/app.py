# application initiation script
from glim.core import Config as C,App
from glim.services import Config
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect

class Glim:

    def __init__(self):
        pass

    def dispatch_request(self, request):
        return Response('Hello')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

def start(host = '127.0.0.1', port = '8080', environment = 'development'):

    try :

        module = __import__('config.%s' % environment, fromlist = ['config'])
        registry = module.config
        Config.boot(C, registry)
        Config.set('db.host', {
            'h' : 'o', 
            's' : ['t', 't', 't']
        })
        print Config.get('db.host.s')[0]

    except Exception, e:

        print e
        exit()