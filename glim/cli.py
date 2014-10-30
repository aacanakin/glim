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
# A modern python framework for the web

__author__ = "Aras Can Akin"

from . import paths
paths.configure()

from termcolor import colored

from glim.app import App
from glim.utils import import_module
from glim.command import CommandAdapter

import glim.commands

import traceback
import argparse
import os
import sys

description = "glim ~ a modern python framework for the web"


def main():
    """

    The single entry point to glim command line interface.Main method is called
    from pypi console_scripts key or by glim.py on root.This function
    initializes a new app given the glim commands and app commands if app
    exists.

    Usage
    -----
      $ python glim/cli.py start
      $ python glim.py start (on root folder)

    """
    # register the global parser
    preparser = argparse.ArgumentParser(
        description=description, add_help=False)
    preparser.add_argument(
        '--env', '-e', dest='env', default='development',
        help='choose application environment'
    )

    # parse existing options
    namespace, extra = preparser.parse_known_args()
    env = namespace.env

    # register the subparsers
    parser = argparse.ArgumentParser(parents=[preparser],
                                     description=description, 
                                     add_help=True)

    subparsers = parser.add_subparsers(title='commands', help='commands')

    # initialize a command adapter with subparsers
    commandadapter = CommandAdapter(subparsers)

    # register glim commands
    commandadapter.register(glim.commands)

    # register app commands
    appcommands = import_module('app.commands', pass_errors=True)
    commandadapter.register(appcommands)

    # check if a new app is being created
    new = True if 'new' in extra else False

    if ('help' in extra) or ('--help' in extra) or ('-h' in extra):
        help = True
    else:
        help = False

    # check if help is being called when the app is not created
    if paths.app_exists() is False and help is True:
        parser.print_help()
        exit()

    # load the config module
    mconfig = import_module('app.config.%s' % env)

    # check if mconfig is None
    if mconfig is None:
        print(colored('Configuration for "%s" environment is not found' % env, 'red'))
        exit()

    # create the app
    app = None if new else App(commandadapter, mconfig, env)

    args = parser.parse_args()

    command = commandadapter.match(args)
    commandadapter.dispatch(command, app)

if __name__ == '__main__':
    main()
