# application initiation script
from glim.core import Config,App

def start(host = '127.0.0.1', port = '8080', environment = 'development'):

    try :

        module = __import__('app.config.%s' % environment, fromlist = ['config'])
        rconfig = module.config
        config = Config(rconfig)

        config.db['port'] = 4000
        App.bind('config', config)        

        print(App.resolve('config'))

    except Exception, e:

        print e
        exit()