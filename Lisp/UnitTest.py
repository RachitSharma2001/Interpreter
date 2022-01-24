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

interpret_code('(define (square x) (* x x)) (square 5)', 1)
interpret_code('(define (square x a) (* x a)) (square 3 5)', 2)
interpret_code('(define (square x a) (* x a)) (define (cube x) (* x x x)) (square (* 8 7 (+ 2)) (+ 12 9)) (cube (+ 9 2))', 3)
interpret_code('(define (square x) (* x x)) (define (f one two) (+ (square one) two)) (f 5 9)', 5)
#check_code('(define (square x a) (* x a)) (square 3 5)', 2)
#check_code('(define (square x) (* x x)) (define (f one two) (+ (square2 one) two))', 3)

'''
print('Test 2')
parser = Parser(Lexer('(define (square x a) (* x a)) (square 1)'))
sa = SemanticAnalyzer()
sa.check_logic_of_ast(parser.get_ast_from_code())'''