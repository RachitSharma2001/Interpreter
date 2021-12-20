from Token import Token
from Token import INTEGER, PLUS, MINUS, MUL, DIV, UNKNOWN
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
        elif token == '+' or token == '-' or token == '*' or token == '/':
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
        elif (type == PLUS or type == MINUS or type == MUL or type == DIV) and self.curr_token.is_type(type):
            if self.is_next_token():
                self.get_next_token()
            else:
                self.curr_token = None
            return 0
        raise Exception("Syntax error - unable to understand token")
    
    def factor(self):
        if self.curr_token == None:
            raise Exception("Syntax Error - Invalid operand")
        return self.eat(INTEGER)

    def parse_add_minus(self):
        sum = self.parse_mult_div()
        op = self.curr_token
        self.get_next_token()
        while op != None:
            right_half = self.parse_mult_div()
            if op.is_type(PLUS):
                sum += right_half
            elif op.is_type(MINUS):
                sum -= right_half
            else:
                raise Exception("Syntax error - unable to understand token")
            op = self.curr_token
            self.get_next_token()
        return sum
    
    def parse_mult_div(self):
        sum = self.factor()
        while not (self.curr_token == None or self.curr_token.is_type(PLUS) or self.curr_token.is_type(MINUS)):
            if self.curr_token.is_type(MUL):
                self.eat(MUL)
                sum *= self.factor()
            elif self.curr_token.is_type(DIV):
                self.eat(DIV)
                sum = int(sum / self.factor())
            else:
                raise Exception("Syntax error - unable to understand token")
        return sum