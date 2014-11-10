"""

The view module is responsible for the server side
view layer of glim framework.

"""
from glim.core import Facade
from jinja2 import Environment, PackageLoader


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


class ViewFacade(Facade):
    accessor = View
