#!/usr/bin/env python
#          _
#       | (_)          
#   __ _| |_ _ __ ___  
#  / _` | | | '_ ` _ \ 
# | (_| | | | | | | | |
#  \__, |_|_|_| |_| |_|
#   __/ |              
#  |___/               
#
#
# author: Aras Can Akin
# description: An elegant python framework for the web
# version: 0.7.2

from glim.app import App
from glim.utils import import_module
from glim.command import CommandAdapter

import glim.commands

import traceback
import argparse

description = "glim (0.6.7) ~ an elegant python framework for the web"

parser = argparse.ArgumentParser(description = description)
parser.add_argument('--env', '-e', default = 'development', help = 'choose application environment(development)')
subparsers = parser.add_subparsers(help = 'commands')

commandadapter = CommandAdapter(subparsers)

# register glim commands
commandadapter.register(glim.commands)

# register app commands
commandadapter.register(import_module('app.commands', 'commands'))

# parse the args
args = parser.parse_args()

# try to create the app, if not make it None
app = None
if args.which != 'new':
	app = App(args.env)

command = commandadapter.match(args)
commandadapter.dispatch(command, app)