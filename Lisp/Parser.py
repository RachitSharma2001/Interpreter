from Ast import *
from Token import *
class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer 
        self.curr_token = self.lexer.get_next_token()
    
    def get_ast_from_code(self):
        lines_of_code = []
        while self.curr_token != None:
            lines_of_code.append(self.get_ast_from_single_line())
        return lines_of_code
    
    def get_ast_from_single_line(self):
        if self.curr_token.is_type(LPAREN):
            return self.get_parenthesis_expr()
        elif self.curr_token.get_type() in (PLUS, MINUS):
            return self.get_unary_operator()
        elif self.curr_token.get_type() in (INT_CONST, REAL_CONST):
            return self.get_numeric_constant()
        else:
            raise Exception('Syntax Error: Unable to parse {} type'.format(self.curr_token.get_type()))
    
    def get_parenthesis_expr(self):
        self.process_token_of_type(LPAREN)
        arith_expr = self.get_arithmetic_expr()
        self.process_token_of_type(RPAREN)
        return arith_expr

    def get_unary_operator(self):
        operand = self.process_token_of_type(self.curr_token.get_type())
        if not self.curr_token.get_type() in (INT_CONST, REAL_CONST):
            raise Exception('Expected Integer or Real constant, instead got {}'.format(token_type))
        return UnaryOperator(operand, self.get_numeric_constant())

    def get_numeric_constant(self):
        token_type = self.curr_token.get_type()
        return NumericConstant(token_type, self.process_token_of_type(token_type))

    def get_arithmetic_expr(self):
        if self.curr_token.get_type() in (PLUS,MINUS,MUL,DIV):
            operator = self.process_token_of_type(self.curr_token.get_type())
            group_of_children = [self.get_ast_from_single_line()]
            while not (self.curr_token == None or self.curr_token.is_type(RPAREN)):
                group_of_children.append(self.get_ast_from_single_line())
            return ArithmeticOperator(operator, group_of_children)
        else:
            raise Exception('Syntax error: Expected binary operator, instead got {}'.format(self.curr_token.get_type()))
    
    def process_token_of_type(self, type):
        if not self.curr_token.is_type(type):
            raise Exception('Type error: Expected {}, got {}'.format(type, self.curr_token.get_type()))
        type_adapted_content = self.curr_token.get_content()
        if type == INT_CONST:
            type_adapted_content = int(type_adapted_content)
        elif type == REAL_CONST:
            type_adapted_content = float(type_adapted_content)
        self.curr_token = self.lexer.get_next_token()
        return type_adapted_content
