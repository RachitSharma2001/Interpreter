import os
import pytest
from Error import ParserError, RuntimeError, SemanticError, LexerError
from Interpreter import Interpreter

def get_file_content_as_one(file_dir, file):
    file_content = ""
    with open(file_dir+file) as opened_file:
        for line in opened_file.readlines():
            file_content += line
    return file_content

'''
    group, compare_group - list of items or a string 
'''
def has_unequal_len(group, compare_group):
    return len(group) != len(compare_group)

def does_interpreter_raise_exception(code_with_error, type_of_error, interpreter):
    if type_of_error == 'PE':
        class_of_error = ParserError
    elif type_of_error == 'RE':
        class_of_error = RuntimeError
    elif type_of_error == 'SE':
        class_of_error = SemanticError
    elif type_of_error == 'LE':
        class_of_error = LexerError
    else:
        raise Exception('{} not a valid error type'.format(type_of_error))
    try:
        with pytest.raises(class_of_error):
            interpreter.interpret(code_with_error)
    except:
        return False
    else:
        return True

input_file_dir = 'Tests/ErrorInput/'
output_file_dir = 'Tests/ErrorOutput/'
error_input_files = os.listdir(input_file_dir)
error_output_files = os.listdir(output_file_dir)
interpreter = Interpreter()

if has_unequal_len(error_input_files, error_output_files):
    raise Exception('Error input has different amount of files than error output!')

for file_index in range(len(error_input_files)):
    code_with_error = get_file_content_as_one(input_file_dir, error_input_files[file_index])
    type_of_error = get_file_content_as_one(output_file_dir, error_output_files[file_index])
    if not does_interpreter_raise_exception(code_with_error, type_of_error, interpreter):
        print('Test {} FAILED!'.format(file_index+1))
        quit()
    else:
        print('Test {} passed!'.format(file_index+1))

print("------------------------------------------------------")
print('All Tests Passed!')