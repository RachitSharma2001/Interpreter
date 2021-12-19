from Interpreter import run
while True:
    input_str = input('Enter Command: ')
    if input_str == 'Done':
        break
    print(run(input_str))