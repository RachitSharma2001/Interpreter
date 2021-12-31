import os
from Interpreter import Interpreter

def get_file_as_one(file_dir, file):
    file_content = ""
    with open(file_dir+file) as opened_file:
        for line in opened_file.readlines():
            file_content += line
    return file_content

def get_file_as_group(file_dir, file):
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

''' 
    expected_output - string
    actual_output - integer or float
'''
def contents_differ(expected_output, actual_output):
    str_version_of_actual = str(actual_output)
    if has_unequal_len(expected_output, str_version_of_actual):
        return True
    for char_index in range(len(expected_output)):
        if expected_output[char_index] != str_version_of_actual[char_index]:
            return True
    return False 

def compare_each_item(output_file_contents, actual_file_contents):
    if has_unequal_len(output_file_contents, actual_file_contents):
        return False
    for output_index in range(len(output_file_contents)):
        expected_output = output_file_contents[output_index]
        actual_output = actual_file_contents[output_index]
        if contents_differ(expected_output, actual_output):
            return False
    return True 

input_file_dir = 'Tests/Input/'
output_file_dir = 'Tests/Output/'
input_file_group = os.listdir('Tests/Input')
output_file_group = os.listdir('Tests/Output')
interpreter = Interpreter()

if has_unequal_len(input_file_group, output_file_group):
    raise Exception('Unequal amount of input and output files')
all_tests_pass = True
for file_index in range(len(input_file_group)):
    input_file_contents = get_file_as_one(input_file_dir, input_file_group[file_index])
    output_file_contents = get_file_as_group(output_file_dir, output_file_group[file_index])
    output_from_interpreter = interpreter.interpret(input_file_contents)
    if not compare_each_item(output_file_contents, output_from_interpreter):
        print('Test #{} failed. Expected {}, got {}'.format(file_index+1, output_file_contents, output_from_interpreter))
        all_tests_pass = False
if all_tests_pass:
    print('All Tests Passed!')

# Get each file from Tests/Input
    # Enter the files data into Interpreter, and get the output
        # GEt the files contents
        # Pass them to the interpreter
    # Get the corresponding file in Tests/Output
    # Compare the interpreter output to the real output
        # Go over each character in the interpreter and real output
        # Compare the current characters
        # if they are different, signal that this test failed
    # If not correct, print out "Test # [num] failed, with output [interpreter output]"
        # If test failed, print out above, signal that at least one test failed
# If all test passed, print that out
