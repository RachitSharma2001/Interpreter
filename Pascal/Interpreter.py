'''
def run(command):
    tokens = get_tokens(command)
    return parser(tokens)

def get_tokens(command):
    tokens_list = []
    for char in command:
        tokens_list.append(identify_type(char))
    return tokens_list

def identify_type(token):
    if token.isdigit():
        return ('Integer', int(token))
    elif token == '+':
        return ('Plus', token)
    else:
        return ('?', token)

def parser(tokens_list):
    if is_addition(tokens_list):
        return tokens_list[0][1] + tokens_list[2][1]
    else:
        return "Syntax error: Unidentified expression given"

def is_addition(tokens_list):
    if tokens_list[0][0] == 'Integer' and tokens_list[1][0] == 'Plus' and tokens_list[2][0] == 'Integer':
        return True
    return False'''
from Token import Token
from Token import INTEGER, PLUS, UNKNOWN
class Interpreter(object):
    def __init__(self, command):
        self.command = command
    
    def run(self):
        tokens_list = self.get_tokens()
        return self.parse(tokens_list)

    def get_tokens(self):
        tokens_list = []
        for char in self.command:
            tokens_list.append(Token(char))
        return tokens_list
    
    def parse(self, tokens_list):
        if self.is_addition(tokens_list):
            return int(tokens_list[0].get_value()) + int(tokens_list[2].get_value())
        raise Exception("Unidentified expression given")
    
    def is_addition(self, tokens_list):
        return tokens_list[0].is_type(INTEGER) and tokens_list[1].is_type(PLUS) and tokens_list[2].is_type(INTEGER)
