from icecream import ic

from .parser import create_parser
from .commands import CLIHandler


class CLIRouter:
    def __init__(self):
        self.parser = create_parser()
        self.handler = CLIHandler()

    def run(self):
        args = self.parser.parse_args()
        command = self.handler.commands.get(args.report)
        if command:
            result= command(args.files)
            print(result)
            ic(result)
        else:
            print("Unknown command")
