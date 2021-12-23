from Interpreter import Interpreter
while True:
    input_str = input('Enter Command: ')
    if input_str == 'Done':
        break
    inter = Interpreter(input_str)
    print(inter.run())