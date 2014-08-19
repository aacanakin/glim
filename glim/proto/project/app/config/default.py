facades = [
	# bunch of services to be loaded up when web server starts
]

extensions = [
	# bunch of extensions to be loaded up when web server starts
	# 'gredis'
]

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
	'views' : {
		'path' : 'app/views',
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