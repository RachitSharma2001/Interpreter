from Lexer import Lexer 
from Parser import Parser
from SemanticAnalyzer import SemanticAnalyzer

print('Test 1')
parser = Parser(Lexer('(define x 5) (define (square x) (* x x))'))
sa = SemanticAnalyzer()
sa.check_logic_of_ast(parser.get_ast_from_code())

print('Test 2')
parser = Parser(Lexer('(define x 5) (define (square a) (* x x))'))
sa = SemanticAnalyzer()
sa.check_logic_of_ast(parser.get_ast_from_code())

'''
parser = Parser(Lexer('(define x 5) (define (square a) (* a b))'))
sa = SemanticAnalyzer()
sa.check_logic_of_ast(parser.get_ast_from_code())
'''
print('Test 3')
parser = Parser(Lexer('(define x 5) (define (f x a) (+ x a)) (define (square b) (* a x))'))
sa = SemanticAnalyzer()
sa.check_logic_of_ast(parser.get_ast_from_code())