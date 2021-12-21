INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, UNKNOWN = 'Integer', 'Plus', 'Minus', 'MUL', 'DIV', '(', ')', '?'
class Token(object):
    def interpret_type(self, char):
        if char.isdigit():
            return INTEGER
        elif char == '+':
            return PLUS
        elif char == '-':
            return MINUS
        elif char == '*':
            return MUL
        elif char == '/':
            return DIV
        elif char == '(':
            return LPAREN
        elif char == ')':
            return RPAREN
        return UNKNOWN
    
    def __init__(self, char):
        self.curr_token = (self.interpret_type(char), char)
    
    def is_type(self, given_type):
        return self.curr_token[0] == given_type

    def get_value(self):
        return int(self.curr_token[1])
    
    def get_type(self):
        return self.curr_token[0]

    def __repr__(self):
        return '({}, {})'.format(self.curr_token[0], self.curr_token[1])