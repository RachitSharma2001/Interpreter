from Token import Token
from Token import INTEGER, PLUS, MINUS, UNKNOWN
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
        elif curr_token == '+' or curr_token == '-':
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
        if len(tokens_list) == 1 and tokens_list[0].is_type(INTEGER):
            return tokens_list[0].get_value()
        elif len(tokens_list) >= 3 and len(tokens_list) % 2 == 1 and tokens_list[0].is_type(INTEGER):
            sum = tokens_list[0].get_value()

            for ind in range(1, len(tokens_list), 2):
                if tokens_list[ind+1].is_type(INTEGER):
                    if tokens_list[ind].is_type(PLUS):
                        sum += tokens_list[ind+1].get_value()
                    elif tokens_list[ind].is_type(MINUS):
                        sum -= tokens_list[ind+1].get_value()
                    else:
                        raise Exception("Unidentified Expression given")
                else:
                    raise Exception("Unidentified Expression given")

            return sum
        else:
            raise Exception("Unidentified Expression given")