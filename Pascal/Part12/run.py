from Interpreter import Interpreter

def read_code(file_name):
    code_str = ""
    with open(file_name, 'r') as code_file:
        for line in code_file.readlines():
            if line[-1] == '\n':
                code_str += line[0:len(line)-1] + ' '
            else:
                code_str += line
    return code_str

file_name = input('File: ')
code_str = read_code(file_name)
inter = Interpreter(code_str)
print(inter.run())

