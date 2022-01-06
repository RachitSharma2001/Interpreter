import os
import pytest
from Error import ParserError
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

def check_exception(code_with_error, type_of_error, interpreter):
    if type_of_error == 'PE':
        with pytest.raises(ParserError):
            interpreter.interpret(code_with_error)

input_file_dir = 'Tests/ErrorInput/'
output_file_dir = 'Tests/ErrorOutput/'
error_input_files = os.listdir(input_file_dir)
error_output_files = os.listdir(output_file_dir)
interpreter = Interpreter()

if has_unequal_len(error_input_files, error_output_files):
    raise Exception('Error input as different amount of files than error output!')

for file_index in range(len(error_input_files)):
    code_with_error = get_file_content_as_one(input_file_dir, error_input_files[file_index])
    type_of_error = get_file_content_as_one(output_file_dir, error_output_files[file_index])
    check_exception(code_with_error, type_of_error, interpreter)

print('All Tests Passed!')
print("------------------------------------------------------")