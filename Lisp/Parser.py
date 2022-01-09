from Ast import *
from Token import *
from Error import ParserError

'''
    Statement_list: (statement)+
    Statement: parenth | single_expr
    parenth: LPAREN (var_decl | op_expr) RPAREN
    var_decl: DEFINE ID num_expr
    num_expr: single_expr | LPAREN op_expr RPAREN
    op_expr: (PLUS | MINUS | MUL | DIV) (num_expr)+
    single_expr: (PLUS | MINUS | empty) (INT | REAL | ID)
'''

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer 
        self.curr_token = self.lexer.get_next_token()

    def get_ast_from_code(self):
        lines_of_code = []
        while self.curr_token != None:
            lines_of_code.append(self.get_ast_from_single_line())
        return Root(lines_of_code)
    
    def get_ast_from_single_line(self):
        if self.curr_token.is_type(LPAREN):
            return self.get_parenthesis_expr()
        elif self.curr_token.get_type() in (PLUS, MINUS, INT_CONST, REAL_CONST, ID): 
            return self.get_single_number()
        else:
            raise ParserError(LPAREN, self.curr_token.get_type())
    
    def get_parenthesis_expr(self):
        self.process_token_of_type(LPAREN)
        if self.curr_token.is_type(DEFINE):
            paren_expr = self.get_variable_decl_expr()
        else:
            paren_expr = self.get_arith_op_expr()
        self.process_token_of_type(RPAREN)
        return paren_expr
    
    def get_single_number(self):
        curr_token_type = self.curr_token.get_type()
        if curr_token_type in (PLUS, MINUS):
            operand = self.process_token_of_type(curr_token_type)
            return UnaryOperator(operand, self.get_single_number())
        elif curr_token_type == INT_CONST:
            return NumericConstant(curr_token_type, self.process_token_of_type(INT_CONST))
        elif curr_token_type == REAL_CONST:
            return NumericConstant(curr_token_type, self.process_token_of_type(REAL_CONST))
        elif curr_token_type == ID:
            return SingleVariable(self.process_token_of_type(ID))
        else:
            raise ParserError('Value Operator', curr_token_type)

    def get_variable_decl_expr(self):
        self.process_token_of_type(DEFINE)
        var_name = self.process_token_of_type(ID) 
        var_value = self.get_math_expr()
        return VariableDeclaration(var_name, var_value)

    def get_math_expr(self):
        if self.curr_token.is_type(LPAREN):
            self.process_token_of_type(LPAREN)
            arith_op_expr = self.get_arith_op_expr()
            self.process_token_of_type(RPAREN)
            return arith_op_expr
        else:
            return self.get_single_number()

    def get_arith_op_expr(self):
        print('In arith op: ', self.curr_token)
        if self.curr_token != None and self.curr_token.get_type() in (PLUS,MINUS,MUL,DIV):
            operator = self.process_token_of_type(self.curr_token.get_type())
            group_of_children = [self.get_math_expr()]
            while not (self.curr_token == None or self.curr_token.is_type(RPAREN)):
                print('In arith op: ', self.curr_token)
                group_of_children.append(self.get_math_expr())
            print('In arith op, group of children: ', group_of_children)
            return ArithmeticOperator(operator, group_of_children)
        else:
            raise ParserError('Binary Operator', self.curr_token.get_type())

    def process_token_of_type(self, type):
        if self.curr_token == None:
            raise ParserError(type, None)
        elif not self.curr_token.is_type(type):
            raise ParserError(type, self.curr_token.get_type())
        type_adapted_content = self.curr_token.get_content()
        if type == INT_CONST:
            type_adapted_content = int(type_adapted_content)
        elif type == REAL_CONST:
            type_adapted_content = float(type_adapted_content)
        elif type == ID:
            type_adapted_content = str(type_adapted_content)
        self.curr_token = self.lexer.get_next_token()
        return type_adapted_content
