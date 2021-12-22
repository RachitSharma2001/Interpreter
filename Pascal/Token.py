BEGIN, END, DOT, ID, ASSIGN, SEMI = 'Begin', 'End', 'Dot', 'Id', 'Assign', 'Semi'
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN = 'Integer', 'Plus', 'Minus', 'MUL', 'DIV', '(', ')'
class Token(object):
    def interpret_type(self, lexeme):
        if lexeme == 'Begin':
            return BEGIN
        elif lexeme == 'End':
            return END
        elif lexeme == '.':
            return DOT
        elif lexeme == ':=':
            return ASSIGN 
        elif lexeme == ';':
            return SEMI
        elif lexeme.isdigit():
            return INTEGER
        elif lexeme == '+':
            return PLUS
        elif lexeme == '-':
            return MINUS
        elif lexeme == '*':
            return MUL
        elif lexeme == '/':
            return DIV
        elif lexeme == '(':
            return LPAREN
        elif lexeme == ')':
            return RPAREN
        # if its none of the above, then likely a variable
        return ID
    
    def __init__(self, lexeme):
        self.curr_token = (self.interpret_type(lexeme), lexeme)
    
    def is_type(self, given_type):
        return self.curr_token[0] == given_type

    def get_value(self):
        return int(self.curr_token[1])
    
    def get_type(self):
        return self.curr_token[0]

    def __repr__(self):
        return '({}, {})'.format(self.curr_token[0], self.curr_token[1])