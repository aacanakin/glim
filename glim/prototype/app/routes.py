"""
This module provides url definitions for glim framework.

Example - basic routing
-----------------------
In glim, the route definitions are restful by default.
The available http methods are the following;
    - POST
    - PUT
    - OPTIONS
    - GET
    - DELETE
    - TRACE
    - COPY

You can define by giving http method by the following;

urls = {
    'POST /profile': 'ProfileController.create',
    'PUT  /profile': 'ProfileController.update',
    'POST /profile': 'ProfileController.create'
}

OR you can automagically generate all available methods by a single route as the following;

urls = {
    '/profile': 'ProfileController'
    # This single line route definition generates the following;
    # 'GET     /profile': 'ProfileController.get'
    # 'PUT     /profile': 'ProfileController.put'
    # 'POST    /profile': 'ProfileController.post'
    # 'OPTIONS /profile': 'ProfileController.options'
    # 'DELETE  /profile': 'ProfileController.delete'
    # 'COPY    /profile': 'ProfileController.copy'
    # 'TRACE   /profile': 'ProfileController.trace'
}

The definition above creates routes for each available method. Moreover, you can
always create without giving http method. Also you can define parametrized routes like the following;

urls = {
    # matches get(year) function in PostController
    # year only matches when int
    '/post/<int:year>/' : 'PostController.get',

    # matches get(feed_name) function in FeedController
    '/feeds/<feed_name>': 'FeedController.get',

    # matches index(lang_code) function in HomeController
    # lang_code only matches for strings with length 2
    '/index/<string(length=2):lang_code>' : 'HomeController.index',

    # matches resolve(page_name) function in PageController
    # page_name only matches when it's the following pages
    '/<any(about, help, imprint, class, "foo,bar"):page_name>': 'PageController.resolve',
}

The parametrized route definitions are also all available to restful route definitions
"""

urls = {
    '/ping': 'AppController.ping'
}
