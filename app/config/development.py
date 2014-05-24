facades = [
	'Session',
	'Cookie',	
]

config = {

	'db' : {

		'default' : {
			'driver' : 'mysql',
			'host' : 'localhost',
			'schema' : 'test',
			'user' : 'root',
			'password' : '',
		},
	},

	'session' : {

	},

	'cookie' : {

	},

	'glim' : {
		'reloader' : True,
		'debugger' : True
	}
}
