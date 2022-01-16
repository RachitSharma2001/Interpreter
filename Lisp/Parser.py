from Ast import *
from Token import *
from Error import ParserError

'''
    Current Grammar: 
    Statement_list: (statement)+
    Statement: parenth | single_expr
    parenth: LPAREN (var_decl | op_expr | proc_decl | proc_call) RPAREN
    proc_decl: DEFINE LPAREN ID ID(ID)* RPAREN (LPAREN proc_decl RPAREN)* LPAREN (op_expr | proc_call) RPAREN
    proc_call: ID (num_expr)+
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
            return self.process_parenthesis_expr()
        elif self.curr_token.get_type() in (PLUS, MINUS, INT_CONST, REAL_CONST, ID): 
            return self.get_single_value()
        else:
            raise ParserError('Unable to parse token {}'.format(self.curr_token.get_type()))
    
    def process_parenthesis_expr(self):
        self.process_token_of_type(LPAREN)
        if self.curr_token.is_type(DEFINE):
            paren_expr = self.process_define_expr()
        elif self.curr_token.is_type(ID):
            paren_expr = self.process_proc_call()
        else:
            paren_expr = self.process_arith_op_expr()
        self.process_token_of_type(RPAREN)
        return paren_expr

    def process_define_expr(self):
        self.process_token_of_type(DEFINE)
        if self.curr_token.is_type(ID):
            return self.process_variable_decl_expr()
        else:
            return self.process_proc_declaration()
    
    # DEFINE LPAREN ID ID(ID)* RPAREN (LPAREN proc_decl RPAREN)* LPAREN (op_expr | proc_call) RPAREN
    def process_proc_declaration(self):
        self.process_token_of_type(LPAREN)
        proc_name, proc_args = self.get_formal_parameters()
        self.process_token_of_type(RPAREN)
        self.process_token_of_type(LPAREN)
        if self.curr_token.is_type(ID):
            proc_body = self.process_proc_call()
        else:
            proc_body = self.process_arith_op_expr()
        self.process_token_of_type(RPAREN)
        return ProcedureDeclaration(proc_name, proc_args, proc_body)

    def get_formal_parameters(self):
        name = self.process_token_of_type(ID)
        args = [self.process_token_of_type(ID)]
        while self.curr_token != None and self.curr_token.is_type(ID):
            args.append(self.process_token_of_type(ID))
        return name, args
    
    # proc_call: ID (num_expr)+
    def process_proc_call(self):
        proc_name = self.process_token_of_type(ID)
        args = [] 
        while not self.curr_token.is_type(RPAREN):
            args.append(self.process_arith_expr_args())
        return ProcedureCall(proc_name, args)

    def process_variable_decl_expr(self):
        var_name = self.process_token_of_type(ID) 
        var_value = self.process_arith_expr_args()
        return VariableDeclaration(var_name, var_value)

    def process_arith_expr_args(self):
        if self.curr_token.is_type(LPAREN):
            return self.process_arith_paren_expr()
        else:
            return self.get_single_value()

    def get_single_value(self):
        curr_token_type = self.curr_token.get_type()
        if curr_token_type in (PLUS, MINUS):
            operand = self.process_token_of_type(curr_token_type)
            return UnaryOperator(operand, self.get_single_value())
        elif curr_token_type == INT_CONST:
            return NumericConstant(curr_token_type, self.process_token_of_type(INT_CONST))
        elif curr_token_type == REAL_CONST:
            return NumericConstant(curr_token_type, self.process_token_of_type(REAL_CONST))
        elif curr_token_type == ID:
            return SingleVariable(self.process_token_of_type(ID))
        else:
            raise ParserError('Unexpected Token type {}'.format(curr_token_type))

    def process_arith_paren_expr(self):
        self.process_token_of_type(LPAREN)
        if self.curr_token.is_type(ID):
            parenth_expr = self.process_proc_call()
        else:
            parenth_expr = self.process_arith_op_expr()
        self.process_token_of_type(RPAREN)
        return parenth_expr

    def process_arith_op_expr(self):
        if self.curr_token != None and self.curr_token.get_type() in (PLUS,MINUS,MUL,DIV):
            operator = self.process_token_of_type(self.curr_token.get_type())
            group_of_children = [self.process_arith_expr_args()]
            while not (self.curr_token == None or self.curr_token.is_type(RPAREN)):
                group_of_children.append(self.process_arith_expr_args())
            return ArithmeticOperator(operator, group_of_children)
        else:
            raise ParserError('Expected Binary Operator, instead got {}'.format(self.curr_token))

    def process_token_of_type(self, type):
        if self.curr_token == None:
            raise ParserError('Expected {}, instead got None'.format(type))
        elif not self.curr_token.is_type(type):
            raise ParserError('Expected {}, instead got {}'.format(type, self.curr_token.get_type()))
        type_adapted_content = self.curr_token.get_content()
        if type == INT_CONST:
            type_adapted_content = int(type_adapted_content)
        elif type == REAL_CONST:
            type_adapted_content = float(type_adapted_content)
        elif type == ID:
            type_adapted_content = str(type_adapted_content)
        self.curr_token = self.lexer.get_next_token()
        return type_adapted_content
