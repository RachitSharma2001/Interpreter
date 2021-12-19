
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
    return False