config = {

	'extensions' : {

		# 'gredis' : {
		# 	'default' : {
		# 		'host' : 'localhost',
		# 		'port' : '1234',
		# 		'db'   : 0
		# 	}
		# }
	},

	# database configuration
	# 'db' : {
	# 	'default' : {
	# 		'driver' : 'mysql',
	# 		'host' : 'localhost',
	# 		'schema' : 'test',
	# 		'user' : 'root',
	# 		'password' : '',
	# 	},
	# },
	
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
		'id_header' : 'glim_session',
		'path' : 'app/storage/sessions',
	},
	
	# app specific configurations
	# reloader: detects changes in the code base and automatically restarts web server
	# debugger: enable werkzeug's default debugger

	'app' : {
		'reloader' : True,
		'debugger' : True,		
	}
}