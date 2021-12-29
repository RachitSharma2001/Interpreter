class Error(Exception):
    def __init__(self, error_obj=None):
        if error_obj != None:
            self.error_val = error_obj.get_value()
            self.line_num = error_obj.get_line_num()
            self.col_num = error_obj.get_col_num()
        self.message = ""
    
    def __str__(self):
        return self.message

class LexerError(Error):
    def __init__(self, error_obj):
        super().__init__(error_obj)
        self.message = '"{}" not valid type ({}:{})'.format(self.error_val, self.line_num, self.col_num)

class ParserError(Error):
    def __init__(self, exp_type, error_obj):
        super().__init__(error_obj)
        self.message = 'Expected "{}", instead got "{}" ({}:{})'.format(exp_type, self.error_val, self.line_num, self.col_num)

class SemanticError(Error):
    def __init__(self, error_obj, redef=True):
        super().__init__(error_obj)
        if redef:
            self.message = '"{}" is already defined ({}:{})'.format(self.error_val, self.line_num, self.col_num)
        else:
            self.message = '"{}" referenced but not defined ({}:{})'.format(self.error_val, self.line_num, self.col_num)