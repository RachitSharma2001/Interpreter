from Token import *
class Lexer(object):
    def __init__(self, command):
        self.command = command
        self.pos = 0

    def get_next_token(self):
        self.skip_whitespace()
        if self.at_end():
            return None 
        token = self.command[self.pos]
        if self.pos < len(self.command) - 1 and self.command[self.pos:self.pos+2] == ':=':
            self.pos += 2
            return Token(':=')
        elif token in ('+', '-', '*', '/', '(', ')', ';', '.', ':', ','):
            self.pos += 1
            return Token(token)
        elif token.isdigit():
            self.pos += 1
            while not self.at_end():
                next_token = self.command[self.pos]
                if not next_token.isdigit() and next_token != '.':
                    break
                token += next_token
                self.pos += 1
            return Token(token)
        elif token.isalnum():
            self.pos += 1
            while not self.at_end():
                curr_char = self.command[self.pos]
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

    def print_tokens(self):
        curr_token = self.get_next_token()
        while curr_token != None:
            print(curr_token)
            curr_token = self.get_next_token()