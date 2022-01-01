from Lexer import Lexer
from Parser import Parser

class Interpreter():
    def __init__(self):
        pass 
    def interpret(self, input_file_contents):
        parser = Parser(Lexer(input_file_contents))
        ast = parser.get_ast_from_code()
        print(ast)
        return []
