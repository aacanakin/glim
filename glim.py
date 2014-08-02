#!/usr/bin/env python

from termcolor import colored
from glim.app import App
# glim with use of click
import click
import shutil, errno
import os

@click.group()
def glim():
    pass

@click.command()
@click.option('--host', default = '127.0.0.1', help = 'enter ip')
@click.option('--port', default = '8080', help = 'enter port')
@click.option('--env', default = 'development', help = 'enter environment (development)')
def start(host, port, env):
    app = App(host, port, env)
    app.start()

@click.command()
def new():
    # resolve prototype path and its childs
    proto_path = 'glim/proto/project'
    cpath = os.path.dirname(os.path.realpath(__file__))
    try:
        copytree(proto_path, cpath)
        print colored('Created new glim app', 'blue')
    except:
        print colored('App already exists', 'red')

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

glim.add_command(start)
glim.add_command(new)

if __name__ == '__main__':
    glim()
