from Token import *

class Lexer(object):
    def __init__(self, code_to_tokenize):
        self.code_to_tokenize = code_to_tokenize
        self.pos_in_code = 0 
    
    def get_next_token(self):
        self.skip_whitespace()
        if self.at_end():
            return None
        if self.curr_char_matches_token():
            curr_char = self.get_curr_char()
            self.advance()
            return Token(curr_char)
        elif self.curr_char_is_int():
            numeric_value = self.get_numeric_value()
            return Token(numeric_value)
        else:
            raise Exception('Unable to tokenize {} at position {}'.format(self.code_to_tokenize, self.pos_in_code))
    
    def advance(self):
        self.pos_in_code += 1

    def skip_whitespace(self):
        while not self.at_end() and self.get_curr_char() in (' ', '\n'):
            self.pos_in_code += 1
    
    def at_end(self):
        return self.pos_in_code >= len(self.code_to_tokenize)
    
    def curr_char_matches_token(self):
        return self.get_curr_char() in str_to_token.keys()
    
    def curr_char_is_int(self):
        return self.get_curr_char().isdigit()
    
    def get_numeric_value(self):
        numeric_value = ""
        while not self.at_end() and (self.curr_char_is_int() or self.get_curr_char() == '.'):
            numeric_value += self.get_curr_char()
            self.advance()
        return numeric_value

    def get_curr_char(self):
        return self.code_to_tokenize[self.pos_in_code]