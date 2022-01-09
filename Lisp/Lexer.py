from Token import *
from Error import LexerError

class Lexer(object):
    def __init__(self, code_to_tokenize):
        self.code_to_tokenize = code_to_tokenize
        self.pos_in_code = 0 
    
    def get_next_token(self):
        self.skip_whitespace()
        if self.at_end():
            return None
        curr_char = self.get_curr_char()
        if self.is_builtin_type(curr_char):
            self.advance()
            return Token(curr_char)
        elif self.is_int(curr_char):
            numeric_value = self.get_numeric_value()
            return Token(numeric_value)
        elif self.is_valid_varchar(curr_char):
            var_name = ''
            while not self.at_end() and self.is_valid_varchar(self.get_curr_char()):
                var_name += self.get_curr_char()
                self.advance()
            return Token(var_name)
        else:
            raise LexerError('Unable to tokenize {} at position {}'.format(self.code_to_tokenize, self.pos_in_code))
    
    def advance(self):
        self.pos_in_code += 1

    def skip_whitespace(self):
        while not self.at_end() and self.get_curr_char() in (' ', '\n'):
            self.pos_in_code += 1
    
    def at_end(self):
        return self.pos_in_code >= len(self.code_to_tokenize)
    
    def is_builtin_type(self, curr_char):
        return curr_char in str_to_token.keys()
    
    def is_int(self, curr_char):
        return curr_char.isdigit()
    
    def is_valid_varchar(self, curr_char):
        return curr_char.isalnum() or curr_char == '_'

    def get_numeric_value(self):
        numeric_value = ""
        while not self.at_end() and (self.is_int(self.get_curr_char()) or self.get_curr_char() == '.'):
            numeric_value += self.get_curr_char()
            self.advance()
        return numeric_value
    
    def get_curr_char(self):
        return self.code_to_tokenize[self.pos_in_code]