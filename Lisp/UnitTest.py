from Lexer import Lexer 
from Parser import Parser

def printTest(parser):
    print(p.get_ast_from_code())
    print('---------------------')

single_arg_code = '(define (square x) (* x x)) (square 25) (square 4)'
p = Parser(Lexer(single_arg_code))
printTest(p)

multi_arg_code = '(define (add x y z d) (+ (* a d) (+ y z d) 4)) (add 3 1 5.2 213.1)'
p = Parser(Lexer(multi_arg_code))
printTest(p)

proc_in_arg_code = '(define (square something somethingelse) (square (triangle somethingelse somethingelse somethingelse somethingelse somethingelse somethingelse)))'
p = Parser(Lexer(proc_in_arg_code))
printTest(p)

proc_call_code = '(* (triangle 1 2 3 4 5 6) (square (/ 5 5)) (* 1 2 (+ 1 2 3)) (- 12 3))'
p = Parser(Lexer(proc_call_code))
printTest(p)