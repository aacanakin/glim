import os
import glim.paths

config = {

	'extensions' : {
		# 'gredis' : {
		# 	'default' : {
		# 		'host' : 'localhost',
		# 		'port' : '6379',
		# 		'db'   : 0
		# 	}
		# }
	},

	# database configuration
	'db' : {
		# 'default' : {
		# 	'driver' : 'mysql',
		# 	'host' : 'localhost',
		# 	'schema' : 'test',
		# 	'user' : 'root',
		# 	'password' : '',
		# },
	},

	'orm' : True,
	
	'log' : {
		# 'level' : 'info',
		# 'format' : '[%(levelname)s] : %(message)s',
		# 'file' : 'app/storage/logs/debug.log'
	},

	'views' : {
		# package to be loaded by jinja2
		'package' : 'app.views'
	},

	'sessions' : {
		# session id prefix
		'id_header' : 'glim_session',
		'path' : glim.paths.STORAGE_PATH,
	},
	
	'app' : {
		'reloader' : True,
		'debugger' : True,
		'static' : {
			'path' : glim.paths.STATIC_PATH,
			'url'  : '/static'
		}
	}
}
