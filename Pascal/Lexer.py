from Token import *
from Error import LexerError 

class Lexer(object):
    def __init__(self, command):
        self.command = command
        self.pos = 0
        self.line_num = 1
        self.col_num = 1

    def peek(self):
        if self.pos + 1 >= len(self.command):
            return None 
        return self.command[self.pos + 1]
    
    def advance(self, advance_amount):
        self.pos += advance_amount

    def get_from_dict(self, curr_char):
        next_char = self.peek()
        if next_char != None and (curr_char + next_char) in token_dict.keys():
            self.advance(2)
            return (curr_char+next_char)
        elif curr_char in token_dict.keys():
            self.advance(1)
            return curr_char
        return None

    def get_number(self, first_char):
        curr_char = first_char
        full_number = ""
        while not self.at_end() and (curr_char.isdigit() or curr_char == '.'):
            full_number += curr_char
            curr_char = self.peek()
            self.advance(1)
        return full_number
    
    def get_string(self, first_char):
        curr_char = first_char 
        full_string = ""
        while not self.at_end() and curr_char.isalnum():
            full_string += curr_char
            curr_char = self.peek()
            self.advance(1)
        return full_string

    def get_next_token(self):
        self.skip_whitespace()
        if self.at_end():
            return None 
        curr_char = self.command[self.pos]
        dict_token = self.get_from_dict(curr_char)
        if dict_token != None:
            return Token(dict_token, self.line_num, self.col_num)
        elif curr_char.isdigit():
            return Token(self.get_number(curr_char), self.line_num, self.col_num)
        elif curr_char.isalnum():
            return Token(self.get_string(curr_char), self.line_num, self.col_num)
        else:
            raise LexerError(curr_char)
    
    def skip_whitespace(self):
        while not self.at_end():
            if self.command[self.pos] == '\n':
                self.line_num += 1
                self.col_num = 1
            elif self.command[self.pos] == ' ':
                self.col_num += 1
            else:
                break
            self.advance(1)
        return

    def at_end(self):
        return self.pos >= len(self.command)

    def print_tokens(self):
        curr_token = self.get_next_token()
        while curr_token != None:
            print(curr_token)
            curr_token = self.get_next_token()