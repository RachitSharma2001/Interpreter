from Interpreter import Interpreter

def read_code():
    code_str = ""
    with open('Code.txt', 'r') as code_file:
        for line in code_file.readlines():
            if line[-1] == '\n':
                code_str += line[0:len(line)-1] + ' '
            else:
                code_str += line
    return code_str

code_str = read_code()
inter = Interpreter(code_str)
print(inter.run())

