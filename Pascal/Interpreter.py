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
        return self.parse_add_minus()
    
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
        while self.is_next_token():
            if self.curr_token.is_type(PLUS):
                self.get_next_token()
                right_child = self.parse_mult_div()
                curr_tree = Ast(curr_tree, PLUS, right_child)
            elif self.curr_token.is_type(MINUS):
                self.get_next_token()
                right_child = self.parse_mult_div()
                curr_tree = Ast(curr_tree, MINUS, right_child)
            else:
                raise Exception("Syntax error - invalid operand")
        return curr_tree 
    
    def parse_mult_div(self):
        curr_tree = self.factor()
        while self.is_next_token() and not (self.curr_token.get_type() in (PLUS, MINUS)):
            if self.curr_token.is_type(MUL):
                self.get_next_token()
                right_child = self.factor()
                curr_tree = Ast(curr_tree, MUL, right_child)
            elif self.curr_token.is_type(DIV):
                self.get_next_token()
                right_child = self.factor()
                curr_tree = Ast(curr_tree, DIV, right_child)
            else:
                raise Exception("Syntax error - invalid operand")
        return curr_tree
    
    def factor(self):
        res = self.eat(INTEGER)
        return Ast(None, res, None)