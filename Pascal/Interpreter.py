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
        self.pos = 0
    
    def run(self):
        tokens_list = self.get_tokens()
        return self.parse(tokens_list)

    def get_tokens(self):
        tokens_list = []
        while self.is_next_token():
            tokens_list.append(self.get_next_token())
        print(tokens_list)
        return tokens_list
    
    '''
        This assumes that the current token is not a space
    '''
    def get_next_token(self):
        curr_token = self.command[self.pos]
        if curr_token.isdigit():
            self.pos += 1
            while self.is_next_token():
                next_token = self.peek()
                if not next_token.isdigit():
                    break
                curr_token += next_token
                self.pos += 1
            return Token(curr_token)
        elif curr_token == '+':
            self.pos += 1
            return Token(curr_token)
        else:
            raise Exception("Invalid token: " + curr_token)

    def peek(self):
        if not self.is_next_token():
            raise Exception("Error in code: called peek but no next token")
        return self.command[self.pos]
    
    '''
        Returns true if there is a non space token after this current position
        Return false otherwise
    '''
    def is_next_token(self):
        # Ignore all the current spaces
        while self.pos < len(self.command) and self.command[self.pos] == ' ':
            self.pos += 1
        return self.pos < len(self.command)
    
    def parse(self, tokens_list):
        if self.is_addition(tokens_list):
            return int(tokens_list[0].get_value()) + int(tokens_list[2].get_value())
        raise Exception("Unidentified expression given")
    
    def is_addition(self, tokens_list):
        return tokens_list[0].is_type(INTEGER) and tokens_list[1].is_type(PLUS) and tokens_list[2].is_type(INTEGER)
