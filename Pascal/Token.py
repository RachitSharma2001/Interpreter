INTEGER, PLUS, MINUS, UNKNOWN = 'Integer', 'Plus', 'Minus', '?'
class Token(object):
    def __init__(self, char):
        self.curr_token = (self.get_type(char), char)
    
    def is_type(self, given_type):
        return self.curr_token[0] == given_type

    def get_value(self):
        return int(self.curr_token[1])

    def get_type(self, char):
        if char.isdigit():
            return INTEGER
        elif char == '+':
            return PLUS
        elif char == '-':
            return MINUS
        return UNKNOWN
    
    def __repr__(self):
        return '({}, {})'.format(self.curr_token[0], self.curr_token[1])