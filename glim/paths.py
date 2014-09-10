import os
from termcolor import colored

PROJECT_PATH = os.getcwd()
APP_PATH = os.path.join(PROJECT_PATH, 'app')
GLIM_ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
PROTO_PATH = os.path.join(os.path.dirname(__file__), 'prototype')

EXT_PATH = os.path.join(PROJECT_PATH, 'ext')
VIEWS_PATH = os.path.join(APP_PATH, 'views')
STATIC_PATH = os.path.join(APP_PATH, 'static')
STORAGE_PATH = os.path.join(APP_PATH, 'storage')

import sys
from pprint import pprint as p

def configure():
	if GLIM_ROOT_PATH == PROJECT_PATH:
		print colored('Development mode is on, sys.path is being configured', 'yellow')
		sys.path.pop(0)
		sys.path.insert(0, GLIM_ROOT_PATH)
	else:
		sys.path.insert(0, PROJECT_PATH)

def app_exists():
	return os.path.exists(APP_PATH) and os.path.exists(EXT_PATH)

def controllers():
	return os.path.join(APP_PATH, 'controllers.py')

def config(env):
	return os.path.join(APP_PATH, 'config', '%s.py' % env)

def start():
	return os.path.join(APP_PATH, 'start.py')

def commands():
	return os.path.join(APP_PATH, 'commands.py')

def routes():
	return os.path.join(APP_PATH, 'routes.py')

def extensions(ext):
	return os.path.join(EXT_PATH, '%s' % ext, '%s.py' % ext)

def extension_commands(ext):
	return os.path.join(EXT_PATH, '%s' % ext, 'commands.py')