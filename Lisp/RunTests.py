import os
import pytest
from Interpreter import Interpreter
from Error import ParserError

def get_file_content_as_one(file_dir, file):
    file_content = ""
    with open(file_dir+file) as opened_file:
        for line in opened_file.readlines():
            file_content += line
    return file_content

def get_group_of_lines_from_file(file_dir, file):
    file_results = []
    with open(file_dir+file) as opened_file:
        for line in opened_file.readlines():
            if line[-1] == '\n':
                line = line[0:len(line)-1]
            file_results.append(line)
    return file_results

'''
    group, compare_group - list of items or a string 
'''
def has_unequal_len(group, compare_group):
    return len(group) != len(compare_group)

def is_interpreter_output_correct(expected_output, interpreter_output):
    try:
        assert expected_output == interpreter_output
    except AssertionError:
        return False
    else:
        return True

input_file_dir = 'Tests/Input/'
output_file_dir = 'Tests/Output/'
input_file_group = os.listdir(input_file_dir)
output_file_group = os.listdir(output_file_dir)
interpreter = Interpreter()

if has_unequal_len(input_file_group, output_file_group):
    raise Exception('Unequal amount of input and output files')

for file_index in range(len(input_file_group)):
    input_code = get_file_content_as_one(input_file_dir, input_file_group[file_index])
    output_from_interpreter = interpreter.interpret(input_code)
    expected_output = get_group_of_lines_from_file(output_file_dir, output_file_group[file_index])
    if not is_interpreter_output_correct(expected_output, output_from_interpreter):
        print('Test {} FAILED!'.format(file_index+1))
        quit()
    else:
        print('Test {} passed'.format(file_index+1))

print("------------------------------------------------------")
print('All Tests Passed!')



