class Error(Exception):
    def __init__(self, message):
        self.message = message 
    
    def __str__(self):
        return self.message

class ParserError(Error):
    def __init__(self, expected_type, given_type):
        self.expected_type = expected_type
        self.given_type = given_type
        super().__init__('Expected {}, received {}'.format(expected_type, given_type))

class RuntimeError(Error):
    def __init__(self, error_msg):
        self.error_msg = error_msg
        super().__init__(error_msg)
    