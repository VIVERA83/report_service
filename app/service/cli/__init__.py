from .commands import CLIHandler
from .parser import create_name_space


class CLIRouter:
    def __init__(self):
        self.name_space = create_name_space()
        self.handler = CLIHandler()

    def run(self):
        command = self.handler.commands.get(self.name_space.report)
        if command:
            result = command(self.name_space.files)
            if result:
                print(result)
        else:
            print("Unknown command")
