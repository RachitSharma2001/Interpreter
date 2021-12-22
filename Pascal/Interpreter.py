from Token import Token
from Token import INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN
from Token import BEGIN, END, DOT, ID, ASSIGN, SEMI
from Ast import Ast
class Interpreter(object):
    def __init__(self, command):
        self.command = command
        self.pos = 0

    def run(self):
        while True:
            curr_token = self.get_next_token()
            print(curr_token)
            if curr_token == None:
                break
        '''if self.curr_token == None:
            raise Exception("Syntax error - requirement of at least one token")
        parsed_ast = self.parse_add_minus()
        return self.interpret(parsed_ast)'''
    
    # Functions for the lexer  
    ''' Returns the next token ''' 
    def get_next_token(self):
        self.skip_whitespace()
        if self.at_end():
            return None 
        token = self.command[self.pos]
        if token in ('+', '-', '*', '/', '(', ')', ';', '.'):
            self.pos += 1
            return Token(token)
        elif token.isdigit():
            self.pos += 1
            while not self.at_end():
                next_token = self.command[self.pos]
                if not next_token.isdigit():
                    break
                token += next_token
                self.pos += 1
            return Token(token)
        elif self.pos < len(self.command) - 1 and self.command[self.pos:self.pos+2] == ':=':
            self.pos += 2
            return Token(':=')
        elif token.isalnum():
            self.pos += 1
            while not self.at_end():
                curr_char = self.command[self.pos]
                if (token == 'Begin' and curr_char == ' '):
                    break 
                if not curr_char.isalnum():
                    break
                token += curr_char
                self.pos += 1
            return Token(token)
        else:
            raise Exception('Invalid Token: ', token)

    def skip_whitespace(self):
        while not self.at_end() and self.command[self.pos] == ' ':
            self.pos += 1
        return

    def at_end(self):
        return self.pos >= len(self.command)
    