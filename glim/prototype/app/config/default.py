"""

The configuration module

NOTE:
  This is a SAMPLE of configuration. This configuration
  can't be run on glim. It's needed to copy this configuration into
  defined environment. If development.py doesn't exist,
  Run the following;

  $ cp app/config/default.py app/config/development.py

  Here, "development" is the environment. You can run configuration
  using the following;

  $ glim start --env development # loads the development configuration

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

        # 'app' : {
        #   'level': 'info',
        #   'format': '[%(levelname)s] - application : %(message)s',
        #   'colored': True,
        #   # 'file' : 'app/storage/logs/app.log'
        # },

        # 'glim' : {
            # 'level' : 'info',
            # 'format' : '[%(levelname)s] : %(message)s',
            # 'colored': True
            # 'file' : 'app/storage/logs/glim.log'  
        # },

    },

    # werkzeug sessions configuration
    'sessions': {
        # session id prefix
        'id_header': 'glim_session',
        'path': glim.paths.STORAGE_PATH,
    },

    # the glim.app.App configuration
    'app': {
        'reloader': True,
        'debugger': True,
        'assets': {
            'path': glim.paths.ASSET_PATH,
            'url': '/assets'
        },
        # 'ssl': 'adhoc' # werkzeug server automatically generates for a key, cert tuple
        # 'ssl': ('ssl.cert', 'ssl.key')
    }
}
