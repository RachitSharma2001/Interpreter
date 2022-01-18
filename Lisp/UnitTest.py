from Lexer import Lexer 
from Parser import Parser
from SemanticAnalyzer import SemanticAnalyzer

def check_code(code, test_num):
    print('Test {}'.format(test_num))
    parser = Parser(Lexer(code))
    sa = SemanticAnalyzer()
    sa.check_logic_of_ast(parser.get_ast_from_code())
    print('---- Done ----')


check_code('(define (square x) (* x x)) (square 5)', 1)
check_code('(define (square x a) (* x a)) (square 3 5)', 2)
check_code('(define (square x) (* x x)) (define (f one two) (+ (square one) two))', 3)
check_code('(define (square x) (* x x)) (define (f one two) (+ (square one two) two))', 4)
'''
print('Test 2')
parser = Parser(Lexer('(define (square x a) (* x a)) (square 1)'))
sa = SemanticAnalyzer()
sa.check_logic_of_ast(parser.get_ast_from_code())'''