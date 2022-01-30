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

interpret_code('(define x 9)(define y 8)(define (f x) (* x y))(f 5)(define (f2 y) (- y (f x) (f y)))(f2 3)(f2 5)(f2 x)(f2 y)(define (f3 x y) (f (+ (f y) (f x) (f2 x) (f2 y))))(f3 x y)(f3 8 1)(f3 100 4)(f3 18 21)', 1)
