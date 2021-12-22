from Token import Token
from Token import INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, UNKNOWN
from Ast import Ast
class Interpreter(object):
    def __init__(self, command):
        self.command = command
        self.pos = 0

    def run(self):
        self.get_next_token()
        if self.curr_token == None:
            raise Exception("Syntax error - requirement of at least one token")
        parsed_ast = self.parse_add_minus()
        return self.interpret(parsed_ast)
    
    def get_next_token(self):
        self.skip_whitespace()
        if not self.is_next_token():
            self.curr_token = None
            return
        token = self.command[self.pos]
        if token.isdigit():
            self.pos += 1
            while self.is_next_token():
                next_token = self.command[self.pos]
                if not next_token.isdigit():
                    break
                token += next_token
                self.pos += 1
            self.curr_token = Token(token)
        elif token in ('+', '-', '*', '/', '(', ')'):
            self.pos += 1
            self.curr_token = Token(token)
        else:
            raise Exception("Invalid token: " + token)
    
    def skip_whitespace(self):
        while self.is_next_token() and self.command[self.pos] == ' ':
            self.pos += 1
    
    def is_next_token(self):
        return self.pos < len(self.command)
    
    def eat(self, type):
        if type == INTEGER and self.curr_token.is_type(type):
            res = self.curr_token.get_value()
            if self.is_next_token():
                self.get_next_token()
            else:
                self.curr_token = None
            return res
        elif type in (PLUS, MINUS, MUL, DIV, LPAREN, RPAREN) and self.curr_token.is_type(type):
            if self.is_next_token():
                self.get_next_token()
            else:
                self.curr_token = None
            return 0
        raise Exception("Syntax error - unable to understand token")
    
    # Returns an AST 
    def parse_add_minus(self):
        curr_tree = self.parse_mult_div()
        while self.is_next_token() and not (self.curr_token.get_type() in (LPAREN, RPAREN)):
            if self.curr_token.is_type(PLUS):
                self.eat(PLUS)
                right_child = self.parse_mult_div()
                curr_tree = Ast(curr_tree, '+', right_child)
            elif self.curr_token.is_type(MINUS):
                self.eat(MINUS)
                right_child = self.parse_mult_div()
                curr_tree = Ast(curr_tree, '-', right_child)
            else:
                raise Exception("Syntax error - invalid operand")
        return curr_tree 
    
    def parse_mult_div(self):
        curr_tree = self.factor()
        while self.is_next_token() and not (self.curr_token.get_type() in (PLUS, MINUS, LPAREN, RPAREN)):
            if self.curr_token.is_type(MUL):
                self.eat(MUL)
                right_child = self.factor()
                curr_tree = Ast(curr_tree, '*', right_child)
            elif self.curr_token.is_type(DIV):
                self.eat(DIV)
                right_child = self.factor()
                curr_tree = Ast(curr_tree, '/', right_child)
            else:
                raise Exception("Syntax error - invalid operand")
        return curr_tree
    
    def factor(self):
        if self.curr_token.is_type(PLUS):
            self.eat(PLUS)
            return Ast(self.factor(), 'u+', None)
        elif self.curr_token.is_type(MINUS):
            self.eat(MINUS)
            return Ast(self.factor(), 'u-', None)
        elif self.curr_token.is_type(INTEGER):     
            res = self.eat(INTEGER)
            return Ast(None, res, None)
        elif self.curr_token.is_type(LPAREN):
            self.eat(LPAREN)
            curr_tree = self.parse_add_minus()
            self.eat(RPAREN)
            return curr_tree
        else:
            raise Exception("Syntax error - invalid operand")

    def interpret(self, parsed_ast):
        post_order = parsed_ast.post_order()
        integer_stack = []
        for val in post_order:
            if val in ('+', '-', '*', '/'):
                if val == '+':
                    integer_stack[-2] += integer_stack[-1]
                elif val == '-':
                    integer_stack[-2] -= integer_stack[-1]
                elif val == '*':
                    integer_stack[-2] *= integer_stack[-1]
                else:
                    integer_stack[-2] /= integer_stack[-1]
                integer_stack.pop()
            elif val in ('u+', 'u-'):
                if val == 'u-':
                    integer_stack[-1] *= -1
            else:
                integer_stack.append(val)
        if len(integer_stack) != 1:
            raise Exception("Program error - stack len not 1")
        return integer_stack[0]