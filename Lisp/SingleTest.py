from Lexer import Lexer 
from Parser import Parser
from SemanticAnalyzer import SemanticAnalyzer
from Interpreter import Interpreter

def check_code(code, test_num):
    print('Test {}'.format(test_num))
    parser = Parser(Lexer(code))
    sa = SemanticAnalyzer()
    sa.check_logic_of_ast(parser.get_ast_from_code())
    print('---- Done ----')

def interpret_code(code, test_num):
    print('Test {}'.format(test_num))
    interpreter = Interpreter()
    code_output = interpreter.interpret(code)
    print('Code Output: {}'.format(code_output))
    print('---- Done ----')

interpret_code('(define (f2 x) (+ x x))(define x 5)(define (f y) (f2 10))(f x)', 1)