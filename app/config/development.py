services = [
	# bunch of services to be loaded up when web server starts
]

extensions = [
	# bunch of extensions to be loaded up when web server starts
]

config = {

	# mysql database configuration

	'db' : {
		'host'	   : 'localhost',
		'schema'   : 'test',
		'user' 	   : 'root',
		'password' : '',
	},

	# app specific configurations
	# reloader: detects changes in the code base and automatically restarts web server
	# debugger: enable werkzeug's default debugger

	'glim' : {
		'reloader' : True,
		'debugger' : True
	}
}