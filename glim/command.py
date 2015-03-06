"""
This module is responsible for registering, dispatching
command line utilities of glim framework. It also has a
Command class for other commands to extend it.
"""


import inspect
from termcolor import colored


class CommandAdapter(object):
    """
    This class is responsible for detecting, registering
    and dispatching command line utilities of glim framework.
    In glim, there are two types of commands namely Command and
    GlimCommand. The only difference of them is GlimCommand can
    access to app object in the runtime. The class is used for
    appending app.commands and glim.commands together. It is also
    used for extension command registering.

    Attributes
    ----------
      subparsers (argparse.Subparsers):
        The subparsers object that provides sub commands.
      commands (list):
        A list of Command objects
    """
    def __init__(self, subparsers):
        self.subparsers = subparsers
        self.commands = []

    def retrieve_commands(self, module):
        """
        Function smartly imports Command type classes given module

        Args
        ----
          module (module):
            The module which Command classes will be extracted from

        Returns
        -------
          commands (list):
            A list of Command instances

        Note:
          This function will not register any command class
          named "Command" or "GlimCommand".

          When extending Command class, be sure to have "Command"
          string on your custom commands.
        """
        commands = []

        for name, obj in inspect.getmembers(module):
            if name != 'Command' and 'Command' in name:
                if name != 'GlimCommand':
                    cobject = getattr(module, name)
                    commands.append(cobject)

        return commands

    def valid_name(self, name):
        """
        Function returns if command name is valid or not.

        Args
        ----
          name (string): The command line utility name.

        Returns
        -------
          valid (boolean): Returns true when valid, else false.
        """
        invalid = name is None or name == ''
        return not invalid

    def register(self, module):
        """
        Function registers into self.commands from module.

        Args
        ----
          module (module): The module name.
        """
        if module is not None:
            cmds = self.retrieve_commands(module)

            for c in cmds:
                if self.valid_name(c.name):
                    cmd = c(self.subparsers)
                    self.commands.append(cmd)
                else:
                    print(colored("Warning: Command %s has empty name. It won't be registered"
                                  % c, 'yellow'))

    def register_extension(self, module, extension):
        """
        Function registers into self.commands from module extension.
        All extension subcommands are registered using the name convention
        'extension:command'

        Example:
            If you have a redis extension namely 'gredis', the extension
            commands can be accessed by the following;

            $ python glim.py gredis:ping

        Args
        ----
          module (module): The module name.
          extension (string): The extension name.
        """
        if module is not None:
            cmds = self.retrieve_commands(module)
            commands = []

            for c in cmds:
                if self.valid_name(c.name):
                    name = '%s:%s' % (extension, c.name)
                    cmd = c(self.subparsers, name)
                    self.commands.append(cmd)

    def match(self, args):
        """
        Function dispatches the active command line utility.

        Args
        ----
          args (argparse.parse_args()):
            The parsed arguments using parser.parse_args() function.

        Returns
        -------
          command (glim.command.Command): the active command object.
        """
        command = None
        for c in self.commands:
            if c.name == args.which:
                c.args = args
                command = c
                break
        return command

    def is_glimcommand(self, command):
        """
        Function detects if a command is GlimCommand.

        Args
        ----
          command (glim.command.Command): the command object.

        Returns
        -------
          True or False
        """
        return isinstance(command, GlimCommand)

    def dispatch(self, command, app):
        """
        Function runs the active command.

        Args
        ----
          command (glim.command.Command): the command object.
          app (glim.app.App): the glim app object.

        Note:
          Exception handling should be done in Command class
          itself. If not, an unhandled exception may result
          in app crash!
        """
        if self.is_glimcommand(command):
            command.run(app)
        else:
            command.run()


class Command(object):
    """
    The base Command class is the base of all
    glim framework commands.

    Attributes
    ----------
      name (string): the command line utility name.
      description (string): command line help description.
      subparsers (argparse.Subparsers): The root of sub commands.
      parser (argparse.ArgumentParser): The object for parsing
        configured arguments.
      args (list): List of arguments defined in configure()

    Note:
      This command will not be registered into glim cli
      interface. It's just a base of all other classes.
    """
    name = None
    description = 'base command'

    # parser is the root parser
    def __init__(self, subparsers, name=None):

        if name is not None:
            self.name = name

        self.subparsers = subparsers
        self.parser = self.subparsers.add_parser(
            self.name,
            help=self.description
        )
        self.parser.set_defaults(which=self.name)

        self.args = None
        self.configure()

    def configure(self):
        """
        This function is a hook before the command line
        utility is run. Therefore, it's being used for
        setting up the command line utility. Mostly, arguments
        are registered here.
        """
        pass

    def add_argument(self, *args, **kwargs):
        """
        Function adds an argument to the cli utility.

        Args
        ----
          args (positional arguments): list of positional arguments
          kwargs (keyword arguments): list of keyword arguments

        Note: This function is an alias of parser.add_argument()
        """
        self.parser.add_argument(*args, **kwargs)

    def run(self):
        """
        This function is being called when the command line utility is fired.
        It is always called after configure() by glim.command.CommandAdapter
        """
        return


class GlimCommand(Command):
    """
    This class is an alias of glim.command.Command which has feature
    to access glim.app.App object on run()
    """
    def run(self, app):
        pass
