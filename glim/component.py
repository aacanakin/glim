from jinja2 import Environment, PackageLoader
from werkzeug.wrappers import Response

from glim.core import Registry

# Extension class
class Extension():
    pass

# Base conroller class that extends all the controllers
class Controller:

    def __init__(self, request):
        self.request = request

# Rest controller that
class RestController(Controller):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

class Service:
    pass

class View:

    def __init__(self, config):
        self.config = config
        package, folder = self.config['package'].split('.')

        self.env = Environment(
            loader = PackageLoader(package, folder
        ))

    # returns a template object given file
    def get(self, file):
        return self.env.get_template(file + '.html')

    def source(self, file, *args, **kwargs):
        tpl = self.get(file)
        return tpl.render(*args, **kwargs)

    def render(self, file, *args, **kwargs):
        return Response(self.source(file, *args, **kwargs), mimetype = 'text/html')
