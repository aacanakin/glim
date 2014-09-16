"""

This module holds the components of a typical glim
framework app.

"""


from jinja2 import Environment, PackageLoader
from werkzeug.wrappers import Response

from glim.core import Registry

# Extension class


class Extension():

    """

    The core extension component of glim. This class must
    be extended to be registered in glim extension development.
    The extension loader checks if the module of classes.

    """
    pass

# Base conroller class that extends all the controllers


class Controller:

    """

    The controller component is responsible for handling requests
    and returning appropriate response to the requests.

    Attributes
    ----------
      request (werkzeug.wrappers.Request): The current request
        object. This object is automatically passed by dispatch
        module.

    """

    def __init__(self, request):
        self.request = request

# Rest controller that


class RestController(Controller):

    """

    The rest controller is simply a shortcut to make the controller
    restful. The dispatcher calls the following functions according
    to the request method.

    """

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

    """

    The base class of Service layer. Currently, it is optional to extend.
    In service layer, it's recommended to use @staticmethod s if they are
    not holding states. Services layer is initially introduced for seperating
    database logic from SQLAlchemy models.

    """
    pass


class View:

    """

    The view layer base class is responsible for Jinja2 integration, template
    data binding and rendering using Jinja2 components.

    Attributes
    ----------
      config (dict): the 'view' key in your app.config.<env>.

    """

    def __init__(self, config):
        self.config = config
        package, folder = self.config['package'].split('.')

        self.env = Environment(
            loader=PackageLoader(package, folder)
        )

    def get(self, file):
        """

        Function returns a template object given path.

        Args
        ----
          file (string): The relative path of template file without
            file extension.

        Returns
        -------
          template (jinja2.Template): The jinja2 template object

        Note:
          It's strongly recommended to use this function on your
          Controller class because of possible path issues.

        """
        return self.env.get_template(file + '.html')

    def source(self, file, *args, **kwargs):
        """

        Function returns the html source of a rendered template.

        Args
        ----
          file (string): The relative path of template without
            file extension.
          args (positional arguments): The arguments that can be
            passed to template object in Jinja2
          kwargs (keyword arguments): The keyword arguments that
            can be passed to template object in Jinja2

        Returns
        -------
          source (string): The html rendered string of template.

        Note:
          This function is designed for html rendering from ajax.

          It's strongly recommended to use this function on your
          Controller class because of possible path issues.

        """
        tpl = self.get(file)
        return tpl.render(*args, **kwargs)

    def render(self, file, *args, **kwargs):
        """

        Function returns a Response of html rendered content.

        Args
        ----
          file (string): The relative path of template without
            file extension.
          args (positional arguments): The arguments that can be
            passed to template object in Jinja2
          kwargs (keyword arguments): The keyword arguments that
            can be passed to template object in Jinja2

        Returns
        -------
          response (werkzeug.wrappers.Response): The werkzeug
            response of html rendered jinja template.

        Note:
          It's strongly recommended to use this function on your
          Controller class because of possible path issues.

        """
        return Response(self.source(file, *args, **kwargs),
                        mimetype='text/html')
