from termcolor import colored
from glim.app import start as appify
# glim with use of click
import click

@click.group()
def glim():
    pass

@click.command()
@click.option('--host', default = '127.0.0.1', help = 'enter ip')
@click.option('--port', default = '8080', help = 'enter port')
@click.option('--env', default = 'development', help = 'enter environment (development)')
def start(host, port, env):
    print colored('glim %s server is running on %s:%s' % (env, host, port), 'green')
    appify(host, port, env)

@click.command()
@click.argument('name')
def new(name):
    print colored('Created new app %s' % name, 'blue')

@click.command()
@click.argument('name')
def model(name):
    print colored('Creating new model %s' % name, 'blue')

@click.command()
@click.argument('name')
def controller(name):
    print colored('Creating new controller %s' % name, 'blue')

@click.command()
def routes():
    print colored('Dumping all routes ..', 'blue')

glim.add_command(start)
glim.add_command(new)
glim.add_command(model)
glim.add_command(controller)
glim.add_command(routes)

if __name__ == '__main__':
    glim()