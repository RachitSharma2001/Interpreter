from Token import Token
from Token import INTEGER, PLUS, MINUS, MUL, DIV, UNKNOWN
class Interpreter(object):
    def __init__(self, command):
        self.command = command
        self.pos = 0

    def run(self):
        if not self.is_next_token:
            raise Exception("Syntax error - requirement of at least one token")
        self.get_next_token()
        return self.parse()
    
    def get_next_token(self):
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
    
    def is_next_token(self):
        # Ignore all the current spaces
        while self.pos < len(self.command) and self.command[self.pos] == ' ':
            self.pos += 1
        return self.pos < len(self.command)
    
    def eat(self, type):
        print("Curr token: ", self.curr_token)
        if type == INTEGER and self.curr_token.is_type(type):
            res = self.curr_token.get_value()
            if self.is_next_token():
                self.get_next_token()
            return res
        elif (type == PLUS or type == MINUS or type == MUL or type == DIV) and self.curr_token.is_type(type):
            if self.is_next_token():
                self.get_next_token()
            return 0
        raise Exception("Syntax error - unable to understand token")
    
    def factor(self):
        return self.eat(INTEGER)

    def parse(self):
        print(self.curr_token)
        sum = self.factor()
        while self.curr_token.get_type() in (PLUS, MINUS, MUL, DIV):
            if self.curr_token.is_type(PLUS):
                self.eat(PLUS)
                sum += self.factor()
            elif self.curr_token.is_type(MINUS):
                self.eat(MINUS)
                sum -= self.factor()
            elif self.curr_token.is_type(MUL):
                self.eat(MUL)
                sum *= self.factor()
            elif self.curr_token.is_type(DIV):
                self.eat(DIV)
                sum = int(sum / self.factor())
        print((self.curr_token.get_type() in (PLUS, MINUS, MUL, DIV)))
        if self.is_next_token():
            print("Extra token: ", self.curr_token, self.curr_token.get_type())
            raise Exception("Syntax error - unable to understand token")
        return sum