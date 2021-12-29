PROCEDURE = 'PROCEDURE'
BEGIN = 'BEGIN'
END = 'END'
DOT = 'DOT'
ID = 'ID'
ASSIGN = 'ASSIGN'
SEMI = 'SEMI'
VAR = 'VAR'
PROGRAM = 'PROGRAM'
COMMA = 'COMMA'
COLON = 'COLON'
REAL = 'REAL'
INTEGER_DIV = 'IntDiv'
FLOAT_DIV = 'FloatDiv'
INTEGER_CONST = 'IntConst'
REAL_CONST = 'RealConst'
INTEGER = 'INTEGER'
PLUS = '+'
MINUS = '-'
MUL = '*'
LPAREN = '('
RPAREN = ')'

token_dict = {
    'PROGRAM' : PROGRAM,
    'PROCEDURE' : PROCEDURE,
    'BEGIN' : BEGIN,
    'VAR' : VAR,
    'END' : END,
    'INTEGER' : INTEGER,
    'REAL' : REAL,
    ':=' : ASSIGN,
    '.' : DOT,
    ',' : COMMA,
    ':' : COLON,
    ';' : SEMI,
    '+' : PLUS,
    '-' : MINUS,
    '*' : MUL,
    'DIV' : INTEGER_DIV,
    '/' : FLOAT_DIV,
    '(' : LPAREN,
    ')' : RPAREN
}

class Token(object):
    def __init__(self, lexeme, line_num, col_num):
        self.curr_token = (self.interpret_type(lexeme), lexeme)
        self.line_num = line_num
        self.col_num = col_num 
    
    def interpret_type(self, lexeme):
        if lexeme in token_dict.keys():
            return token_dict[lexeme]
        elif lexeme[0].isdigit() and '.' in lexeme:
            return REAL_CONST
        elif lexeme.isdigit():
            return INTEGER_CONST
        return ID

    def is_type(self, given_type):
        return self.curr_token[0] == given_type

    def get_type(self):
        return self.curr_token[0]

    def get_value(self):
        if self.is_type(INTEGER_CONST):
            return int(self.curr_token[1])
        elif self.is_type(REAL_CONST):
            return float(self.curr_token[1])
        return self.curr_token[1]

    def get_line_num(self):
        return self.line_num

    def get_col_num(self):
        return self.col_num

    def __repr__(self):
        return '({}, {})'.format(self.curr_token[0], self.curr_token[1])
