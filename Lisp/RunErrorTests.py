import unittest

class TestParserErrors(unittest.TestCase):
    def test_no_numbers_expr(self):
        


def check_error_raised(self, input_file_contents, expect_error_content, interpreter):
    with self.assertRaises(ParserError, expect_error_content):
        interpreter.interpret(input_file_contents)


input_file_dir = 'Tests/ErrorInput/'
output_file_dir = 'Tests/ErrorOutput/'
input_file_group = os.listdir(input_file_dir)
output_file_group = os.listdir(output_file_dir)

if has_unequal_len(input_file_group, output_file_group):
    raise Exception('Unequal amount of error input and output files')
for file_index in range(len(input_file_group)):
    input_file_contents = get_content_from_file(input_file_dir, input_file_group[file_index])
    expect_error_content = get_content_from_file(output_file_dir, output_file_group[file_index])
    self.check_error_raised(input_file_contents, expect_error_content, interpreter)
print ('All Error Tests Passed!')