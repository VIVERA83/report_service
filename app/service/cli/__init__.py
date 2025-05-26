from .parser import create_name_space
from .commands import CLIHandler


class CLIRouter:
    def __init__(self):
        self.name_space = create_name_space()
        self.handler = CLIHandler()

    def run(self):
        command = self.handler.commands.get(self.name_space.report)
        if command:
            result= command(self.name_space.files)
            print(result)
        else:
            print("Unknown command")
