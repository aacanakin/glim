import inspect

class CommandAdapter:

    def __init__(self, subparsers):
        self.subparsers = subparsers
        self.commands = []

    def retrieve_commands(self, module):
        commands = []

        for name, obj in inspect.getmembers(module):
            if name != 'Command' and 'Command' in name:
                cobject = getattr(module, name)
                commands.append(cobject)

        return commands

    def register(self, module):
        if module is not None:
            cmds = self.retrieve_commands(module)
            commands = []

            for c in cmds:
                cmd = c(self.subparsers)
                self.commands.append(cmd)

    def register_extension(self, module, extension):
        if module is not None:
            cmds = self.retrieve_commands(module)
            commands = []

            for c in cmds:
                name = '%s:%s' % (extension, c.name)
                cmd = c(self.subparsers, name)
                self.commands.append(cmd)

    def match(self, args):
        command = None
        for c in self.commands:
            if c.name == args.which:
                c.args = args
                command = c
                break
        return command

    def is_glimcommand(self, command):
        return isinstance(command, GlimCommand)

    def dispatch(self, command, app):
        if self.is_glimcommand(command):
            command.run(app)
        else:
            command.run()

class Command:

    name = 'base'
    description = 'base command'

    # parser is the root parser
    def __init__(self, subparsers, name = None):

        if name is not None:
            self.name = name

        self.subparsers = subparsers
        self.parser = self.subparsers.add_parser(
            self.name,
            help = self.description
        )
        self.parser.set_defaults(which = self.name)

        self.args = None
        self.configure()

    def configure(self):
        pass

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def run(self):
        return

class GlimCommand(Command):
    def run(self, app):
        pass