"""

The configuration module

NOTE:
  This the default of configuration. A good practice would be keeping
  separate config.py for separate environments. config.<environment>.py would
  be a good format to keep it. Put config.py to gitignore and run copy in
  your deployment script.

  $ glim start

"""

import os
import glim.paths

config = {

    # the configurations of extensions
    'extensions': {
        # 'gredis' : {
        #   'default' : {
        #       'host' : 'localhost',
        #       'port' : '6379',
        #       'db'   : 0
        #   }
        # }
    },

    # logging configuration, it has a default configuration
    # if you don't provide one.
    'log' : {

        'app' : {
          'level': 'info',
          'format': '[%(levelname)s] - application : %(message)s',
          'colored': True
          # 'file' : 'app/storage/logs/app.log'
        },

        'glim' : {
            'level' : 'info',
            'format' : '[%(levelname)s] : %(message)s',
            'colored': True
            # 'file' : 'app/storage/logs/glim.log'
        },

    },

    # the glim.app.App configuration
    'app': {
        'server': {
            'host': '127.0.0.1',
            'port': 8080,
            'wsgi': 'wsgiref',
            'reloader': True,
            'debugger': True,
            'options': {}
        },
        'assets': {
            'path': glim.paths.ASSET_PATH,
            'url': '/assets'
        }
    }
}
