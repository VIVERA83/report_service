from dataclasses import dataclass
import argparse

@dataclass
class CLINamespace:
    files: list[str]
    report: str

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("--report", required=True)
    return parser
