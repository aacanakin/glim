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
# version: 0.7.7

import paths
paths.configure_sys_path()

from glim.app import App
from glim.utils import import_module
from glim.command import CommandAdapter

import glim.commands

import traceback
import argparse
import os
import sys

description = "glim ~ an elegant python framework for the web"

def main():
	# register the global parser
	preparser = argparse.ArgumentParser(description = description, add_help = False)
	preparser.add_argument('--env', '-e', dest = 'env', default = 'development', help = 'choose application environment')

	# parse existing options
	namespace, extra = preparser.parse_known_args()
	env = namespace.env

	parser = argparse.ArgumentParser(parents = [preparser], description = description, add_help = True)
	subparsers = parser.add_subparsers(title = 'commands', help = 'commands')

	# initialize a command adapter with subparsers
	commandadapter = CommandAdapter(subparsers)

	# register glim commands
	commandadapter.register(glim.commands)

	# register app commands
	appcommands = import_module('app.commands', pass_errors = True)
	commandadapter.register(appcommands)

	# check if a new app is being created
	new = True if 'new' in extra else False
	if new:
		app = None
	else:
		app = App(commandadapter, env)


	args = parser.parse_args()

	command = commandadapter.match(args)
	commandadapter.dispatch(command, app)

if __name__ == '__main__':
	main()
