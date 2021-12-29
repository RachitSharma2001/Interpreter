from Token import *
from Ast import Block, Proc_decl, Compound, Var_decl, Assign, Variable, Param, Constant, BinOp, UnOp
from Error import ParserError

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = lexer.get_next_token()
        if self.curr_token == None:
            return
    
    def generate_ast(self):
        return self.program()

    def program(self):
        self.eat(PROGRAM)
        self.eat(ID)
        self.eat(SEMI)
        tree = self.block()
        self.eat(DOT)
        return tree
   
    def block(self):
        dec_tree_list = self.declarations()
        compound_tree = self.compound_statement()
        return Block(dec_tree_list, compound_tree)

    def declarations(self):
        total_list = []
        if self.curr_token.is_type(VAR):
            self.eat(VAR)
            var_tree_list = []
            while self.curr_token.is_type(ID):
                new_var_trees = self.variable_declaration()
                self.eat(SEMI)
                var_tree_list += new_var_trees
            total_list += var_tree_list
        while self.curr_token.is_type(PROCEDURE):
            self.eat(PROCEDURE)
            proc_token = self.curr_token
            proc_name = self.eat(ID)
            param_list = []
            if self.curr_token.is_type(LPAREN):
                self.eat(LPAREN)
                param_list += self.formal_param_list()
                self.eat(RPAREN)
            self.eat(SEMI)
            total_list += [Proc_decl(proc_name, param_list, self.block(), proc_token)]
            self.eat(SEMI)
        return total_list

    def formal_param_list(self):
        param_list = self.params()
        if self.curr_token.is_type(SEMI):
            self.eat(SEMI)
            param_list += self.formal_param_list()
        return param_list
    
    def params(self):
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

    def variable_declaration(self):
        var_names = [(self.curr_token, self.eat(ID))]
        while self.curr_token.is_type(COMMA):
            self.eat(COMMA)
            var_names.append((self.curr_token, self.eat(ID)))
        self.eat(COLON)
        var_type = self.type_spec()
        var_tree_list = []
        for orig_token, name in var_names:
            var_tree_list.append(Var_decl(name, var_type, orig_token))
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

    def compound_statement(self):
        self.eat(BEGIN)
        tree_list = self.statement_list()
        self.eat(END)
        return Compound(tree_list)
    
    def statement_list(self):
        returned_node = self.statement()
        if returned_node == None:
            return []
        list_nodes = [returned_node]
        while self.curr_token.is_type(SEMI):
            self.eat(SEMI)
            returned_node = self.statement()
            if returned_node == None:
                break
            list_nodes.append(returned_node)
        return list_nodes
    
    def statement(self):
        if self.curr_token.is_type(BEGIN):
            return self.compound_statement()
        elif self.curr_token.is_type(ID):
            return self.assignment_statement()
        else:
            return None

    def assignment_statement(self):
        var_node = self.variable()
        assign_token = self.curr_token
        self.eat(ASSIGN)
        expr_node = self.expr()
        return Assign(var_node, expr_node, assign_token)
    
    def expr(self):
        curr_tree = self.term()
        while not self.lexer.at_end():
            if self.curr_token.is_type(PLUS):
                self.eat(PLUS)
                right_child = self.term()
                curr_tree = BinOp(curr_tree, '+', right_child)
            elif self.curr_token.is_type(MINUS):
                self.eat(MINUS)
                right_child = self.term()
                curr_tree = BinOp(curr_tree, '-', right_child)
            else:
                break
        return curr_tree 
    
    def term(self):
        curr_tree = self.factor()
        while not self.lexer.at_end():
            if self.curr_token.is_type(MUL):
                self.eat(MUL)
                right_child = self.factor()
                curr_tree = BinOp(curr_tree, '*', right_child)
            elif self.curr_token.is_type(INTEGER_DIV):
                self.eat(INTEGER_DIV)
                right_child = self.factor()
                curr_tree = BinOp(curr_tree, 'DIV', right_child)
            elif self.curr_token.is_type(FLOAT_DIV):
                self.eat(FLOAT_DIV)
                right_child = self.factor()
                curr_tree = BinOp(curr_tree, '/', right_child)  
            else:
                break
        return curr_tree

    def factor(self):
        if self.curr_token.is_type(PLUS):
            self.eat(PLUS)
            return UnOp(self.factor(), False)
        elif self.curr_token.is_type(MINUS):
            self.eat(MINUS)
            return UnOp(self.factor(), True)
        elif self.curr_token.is_type(INTEGER_CONST):     
            res = self.eat(INTEGER_CONST)
            return Constant(res, INTEGER)
        elif self.curr_token.is_type(REAL_CONST):
            res = self.eat(REAL_CONST)
            return Constant(res, REAL)
        elif self.curr_token.is_type(LPAREN):
            self.eat(LPAREN)
            curr_tree = self.expr()
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