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
# /api/auth/me filtered by ApiController.check_auth
# if check_auth function returns any Response,
# then ApiController.me would not be called

urls = {
    '/api' : {
        '/auth' : 'ApiController.auth',
        '/me' : [
            'ApiController.check_auth',
            'ApiController.me'
        ]
    }
}

"""

urls = {
    '/': 'BaseController.hello'
}
