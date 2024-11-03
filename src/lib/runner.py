from lib.scanner import Scanner
from lib.parser import Parser
from lib.interpreter import Interpreter


def execute_file(filepath):
    input = _read_file(filepath)

    tokens = Scanner(input).scan()

    ast_nodes = Parser(tokens).parse()

    Interpreter(ast_nodes).execute()


def _read_file(filepath):
    with open(filepath) as file:
        return file.read()
