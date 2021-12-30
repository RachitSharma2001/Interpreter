from Token import *
from Ast import Block, Proc_decl, Compound, Var_decl, Assign, Variable, Param, Constant, BinaryOperator, UnaryOperator
from Error import ParserError

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = lexer.get_next_token()
        if self.curr_token == None:
            return
    
    def generate_ast(self):
        return self.analyze_header()

    def analyze_header(self):
        self.eat(PROGRAM)
        self.eat(ID)
        self.eat(SEMI)
        tree = self.analyze_body()
        self.eat(DOT)
        return tree
   
    def analyze_body(self):
        dec_tree_list = self.get_tree_from_declarations()
        compound_tree = self.get_tree_from_compound_statement()
        return Block(dec_tree_list, compound_tree)

    def get_tree_from_declarations(self):
        group_of_declarations = []
        if self.curr_token.is_type(VAR):
            group_of_declarations += self.get_group_of_variables()
        if self.curr_token.is_type(PROCEDURE):
            group_of_declarations += self.get_group_of_procedures()
        return group_of_declarations

    def get_group_of_variables(self):
        group_of_variables = []
        self.eat(VAR)
        while self.curr_token.is_type(ID):
            group_of_variables += self.get_individual_variable()
            self.eat(SEMI)
        return group_of_variables

    def get_group_of_procedures(self):
        group_of_procedures = []
        while self.curr_token.is_type(PROCEDURE):
            self.eat(PROCEDURE)
            procedure_token = self.curr_token
            procedure_name = self.eat(ID)
            group_of_params = []
            if self.curr_token.is_type(LPAREN):
                self.eat(LPAREN)
                group_of_params += self.get_group_of_parameters()
                self.eat(RPAREN)
            self.eat(SEMI)
            group_of_procedures += [Proc_decl(procedure_name, group_of_params, self.analyze_body(), procedure_token)]
            self.eat(SEMI)
        return group_of_procedures
    
    def get_group_of_parameters(self):
        param_list = self.get_individual_parameter()
        if self.curr_token.is_type(SEMI):
            self.eat(SEMI)
            param_list += self.get_group_of_parameters()
        return param_list
    
    def get_individual_parameter(self):
        var_names = [self.eat(ID)]
        while self.curr_token.is_type(COMMA):
            self.eat(COMMA)
            var_names.append(self.eat(ID))
        self.eat(COLON)
        var_type = self.type_spec()
        param_tree_list = []
        for name in var_names:
            param_tree_list.append(Param(name, var_type))
        return param_tree_list

    def get_individual_variable(self):
        orig_tokens = [self.curr_token]
        var_names = [self.eat(ID)]
        while self.curr_token.is_type(COMMA):
            self.eat(COMMA)
            orig_tokens.append(self.curr_token)
            var_names.append(self.eat(ID))
        self.eat(COLON)
        var_type = self.type_spec()
        var_tree_list = []
        for ind in range(len(var_names)):
            var_tree_list.append(Var_decl(var_names[ind], var_type, orig_tokens[ind]))
        return var_tree_list

    def type_spec(self):
        tree_list = []
        if self.curr_token.is_type(INTEGER):
            var_type = INTEGER
            self.eat(INTEGER)
        else:
            var_type = REAL
            self.eat(REAL)
        return var_type

    def get_tree_from_compound_statement(self):
        self.eat(BEGIN)
        group_of_statements = self.get_group_of_statements()
        self.eat(END)
        return Compound(group_of_statements)
    
    def get_group_of_statements(self):
        returned_node = self.get_tree_from_statement()
        if returned_node == None:
            return []
        list_nodes = [returned_node]
        while self.curr_token.is_type(SEMI):
            self.eat(SEMI)
            returned_node = self.get_tree_from_statement()
            if returned_node == None:
                break
            list_nodes.append(returned_node)
        return list_nodes
    
    def get_tree_from_statement(self):
        if self.curr_token.is_type(BEGIN):
            return self.get_tree_from_compound_statement()
        elif self.curr_token.is_type(ID):
            return self.get_tree_from_assignment()
        else:
            return None

    def get_tree_from_assignment(self):
        var_node = self.variable()
        assign_token = self.curr_token
        self.eat(ASSIGN)
        expr_node = self.get_tree_from_arithmetic()
        return Assign(var_node, expr_node)
    
    def get_tree_from_arithmetic(self):
        curr_tree = self.get_tree_from_muldiv()
        while not self.lexer.at_end():
            if self.curr_token.is_type(PLUS):
                self.eat(PLUS)
                right_child = self.get_tree_from_muldiv()
                curr_tree = BinaryOperator(curr_tree, '+', right_child)
            elif self.curr_token.is_type(MINUS):
                self.eat(MINUS)
                right_child = self.get_tree_from_muldiv()
                curr_tree = BinaryOperator(curr_tree, '-', right_child)
            else:
                break
        return curr_tree

    def get_tree_from_muldiv(self):
        curr_tree = self.factor()
        while not self.lexer.at_end():
            if self.curr_token.is_type(MUL):
                self.eat(MUL)
                right_child = self.factor()
                curr_tree = BinaryOperator(curr_tree, '*', right_child)
            elif self.curr_token.is_type(INTEGER_DIV):
                self.eat(INTEGER_DIV)
                right_child = self.factor()
                curr_tree = BinaryOperator(curr_tree, 'DIV', right_child)
            elif self.curr_token.is_type(FLOAT_DIV):
                self.eat(FLOAT_DIV)
                right_child = self.factor()
                curr_tree = BinaryOperator(curr_tree, '/', right_child)  
            else:
                break
        return curr_tree

    def factor(self):
        if self.curr_token.is_type(PLUS):
            self.eat(PLUS)
            return UnaryOperator(self.factor(), False)
        elif self.curr_token.is_type(MINUS):
            self.eat(MINUS)
            return UnaryOperator(self.factor(), True)
        elif self.curr_token.is_type(INTEGER_CONST):     
            res = self.eat(INTEGER_CONST)
            return Constant(res, INTEGER)
        elif self.curr_token.is_type(REAL_CONST):
            res = self.eat(REAL_CONST)
            return Constant(res, REAL)
        elif self.curr_token.is_type(LPAREN):
            self.eat(LPAREN)
            curr_tree = self.get_tree_from_arithmetic()
            self.eat(RPAREN)
            return curr_tree
        else:
            return self.variable()

    def variable(self):
        orig_token = self.curr_token
        var_name = self.eat(ID)
        return Variable(orig_token.get_type(), var_name, orig_token)
       
    def eat(self, type):
        # If the type has a sought-after value, we would want to return it
        if not self.curr_token.is_type(type):
            raise ParserError(type, self.curr_token)
        else:
            res = self.curr_token.get_value()
            self.curr_token = self.lexer.get_next_token()
            return res