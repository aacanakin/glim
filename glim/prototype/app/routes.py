"""
This module provides url definitions for glim framework.

Example - basic routing
-----------------------

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
    '/<any(about, help, imprint, class, "foo,bar"):page_name>':
    'PageController.resolve',
}

Example - route grouping/filtering
----------------------------------

# /api/auth matches to ApiController.auth
# /api/auth/me matches to ApiController.me
# /hello mathes to BaseController.hello

urls = {
    '/api' : {
        '/auth': 'ApiController.auth',
        '/me': 'ApiController.me'
    },
    '/hello': 'BaseController.hello'
}

"""

urls = {
    '/<name>': 'BaseController.hello'
}
