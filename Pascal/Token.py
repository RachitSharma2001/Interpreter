INTEGER, PLUS, UNKNOWN = 'Integer', 'Plus', '?'
class Token(object):
    def __init__(self, char):
        self.curr_token = (self.get_type(char), char)
    
    def is_type(self, given_type):
        return self.curr_token[0] == given_type

    def get_value(self):
        return self.curr_token[1]

    def get_type(self, char):
        if char.isdigit():
            return INTEGER
        elif char == '+':
            return PLUS
        return UNKNOWN
    
    def __repr__(self):
        return '({}, {})'.format(self.curr_token[0], self.curr_token[1])