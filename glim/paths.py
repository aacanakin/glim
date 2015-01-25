"""

This module is responsible for handling paths of glim framework.

Usage
-----
import glim.paths

glim.paths.PROJECT_PATH # returns the project path
glim.paths.APP_PATH # returns the app folder path
glim.paths.GLIM_ROOT_PATH # returns the glim root path
glim.paths.PROTO_PATH # returns the prototype folder path
glim.paths.EXT_PATH # returns the extension folder path
glim.paths.VIEWS_PATH # returns the views folder path
glim.paths.ASSET_PATH # returns the assets folder path
glim.paths.STORAGE_PATH # returns the storage folder path

glim.paths.configure() # detect dev mode & configures the sys path
glim.paths.app_exists() # detects if the app is created
glim.paths.controllers() # returns the controllers path
glim.paths.config(env) # returns the configuration path given environment
glim.paths.start() # returns the app.start path
glim.paths.commands() # returns the app.commands path
glim.paths.routes() # returns the app.routes path
glim.paths.extensions(ext) #returns the extension path given extension name
glim.paths.extension_commands(ext) # returns the ext.<ext>.commands path

"""


import os
from termcolor import colored

PROJECT_PATH = os.getcwd()
APP_PATH = os.path.join(PROJECT_PATH, 'app')
GLIM_ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
PROTO_PATH = os.path.join(os.path.dirname(__file__), 'prototype')

VIEWS_PATH = os.path.join(APP_PATH, 'views')
ASSET_PATH = os.path.join(APP_PATH, 'assets')
STORAGE_PATH = os.path.join(APP_PATH, 'storage')

import sys
from pprint import pprint as p


def configure():
    if GLIM_ROOT_PATH == PROJECT_PATH:
        print(colored('Development mode is on, sys.path is being configured',
                      'yellow'))
        sys.path.pop(0)
        sys.path.insert(0, GLIM_ROOT_PATH)
    else:
        sys.path.insert(0, PROJECT_PATH)


def app_exists():
    return os.path.exists(APP_PATH)


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
