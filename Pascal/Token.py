
BEGIN = 'Begin'
END = 'End'
DOT = 'Dot'
ID = 'Id'
ASSIGN = 'Assign'
SEMI = 'Semi'
VAR = 'VAR'
PROGRAM = 'Program'
COMMA = 'Comma'
COLON = 'Colon'
REAL = 'Real'
INTEGER_DIV = 'IntDiv'
FLOAT_DIV = 'FloatDiv'
INTEGER_CONST = 'IntConst'
REAL_CONST = 'RealConst'
INTEGER = 'Integer'
PLUS = 'Plus'
MINUS = 'Minus'
MUL = 'Mul'
LPAREN = '('
RPAREN = ')'


class Token(object):
    def interpret_type(self, lexeme):
        if lexeme == 'BEGIN':
            return BEGIN
        elif lexeme == 'END':
            return END
        elif lexeme == 'PROGRAM':
            return PROGRAM 
        elif lexeme == 'REAL':
            return REAL
        elif lexeme == 'INTEGER':
            return INTEGER
        elif lexeme == 'VAR':
            return VAR
        elif lexeme == ',':
            return COMMA
        elif lexeme == ':':
            return COLON 
        elif lexeme == 'DIV':
            return INTEGER_DIV
        elif lexeme == '.':
            return DOT
        elif lexeme == ':=':
            return ASSIGN 
        elif lexeme == ';':
            return SEMI
        elif lexeme[0].isdigit() and '.' in lexeme:
            return REAL_CONST
        elif lexeme.isdigit():
            return INTEGER_CONST
        elif lexeme == '+':
            return PLUS
        elif lexeme == '-':
            return MINUS
        elif lexeme == '*':
            return MUL
        elif lexeme == '/':
            return FLOAT_DIV
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
        if self.curr_token[1].isdigit():
            return int(self.curr_token[1])
        return self.curr_token[1]
    
    def get_type(self):
        return self.curr_token[0]

    def __repr__(self):
        return '({}, {})'.format(self.curr_token[0], self.curr_token[1])
