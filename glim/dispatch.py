"""

This module is responsible for the wsgi part of glim framework.

"""


from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.utils import redirect
from werkzeug.contrib.sessions import FilesystemSessionStore

from glim.utils import import_module
import glim.paths as paths


try:
    basestring
except NameError:
    # 'basestring' is undefined, so it must be Python 3
    basestring = (str, bytes)


class Glim:

    """

    The class that holds the wsgi app of glim framework.

    Attributes
    ----------
      config (dict): The 'glim' key of app.config.<env>.
      session_store (werkzeug.contrib.sessions.FilesystemSessionStore):
        The session store in case of session usage.
      url_map (werkzeug.routing.Map): The url map of wsgi app.

    Usage
    -----
      app = Glim(urls, config)

      # start the web server
      run_simple(host, int(port), app, use_debugger=True, use_reloader=True)

    """

    def __init__(self, urls={}, config={}):
        self.config = config

        try:
            self.session_store = FilesystemSessionStore(
                self.config['sessions']['path']
            )
        except:
            self.session_store = None

        ruleset = self.flatten_urls(urls)
        rule_map = []
        for url, rule in ruleset.items():
            rule_map.append(Rule(url, endpoint=rule))

        self.url_map = Map(rule_map)

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
            mcontroller = import_module('app.controllers')

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
                    mfilter = mcontroller
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
                raw = getattr(instance, request.method.lower())(**values)
            else:
                raw = getattr(instance, fnc)(** values)

            if isinstance(raw, Response):
                return raw
            else:
                return Response(raw)

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
                response.set_cookie(
                    self.config['sessions']['id_header'],
                    request.session.sid
                )

        return response(environ, start_response)

    def __call__(self, environ, start_response):

        return self.wsgi_app(environ, start_response)
