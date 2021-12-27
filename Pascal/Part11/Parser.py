from Token import *
from Ast import Compound, Assign, Variable, Var_decl, Block, Constant, BinOp, UnOp

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
        var_tree_list = self.declarations()
        compound_tree = self.compound_statement()
        return Block(var_tree_list, compound_tree)

    def declarations(self):
        self.eat(VAR)
        var_tree_list = []
        while True:
            new_var_trees = self.variable_declaration()
            self.eat(SEMI)
            var_tree_list += new_var_trees
            # declarations can only be followed by compound statements (starting with Begin)
            if self.curr_token.is_type(BEGIN):
                break 
        return var_tree_list

    def variable_declaration(self):
        var_names = [self.eat(ID)]
        while self.curr_token.is_type(COMMA):
            self.eat(COMMA)
            var_names.append(self.eat(ID))
        self.eat(COLON)
        var_tree_list = self.type_spec(var_names)
        return var_tree_list

    def type_spec(self, names):
        tree_list = []
        if self.curr_token.is_type(INTEGER):
            var_type = INTEGER
            self.eat(INTEGER)
        elif self.curr_token.is_type(REAL):
            var_type = REAL
            self.eat(REAL)
        else:
            raise Exception("Syntax error: invalid token", self.curr_token)
        for name in names:
            tree_list.append(Var_decl(name[1], var_type))
        return tree_list

    def compound_statement(self):
        self.eat(BEGIN)
        tree_list = self.statement_list()
        self.eat(END)
        return Compound(tree_list)
    
    def statement_list(self):
        list_nodes = [self.statement()]
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
        self.eat(ASSIGN)
        expr_node = self.expr()
        return Assign(var_node, expr_node)
    
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
            return Constant(int(res[1]), INTEGER)
        elif self.curr_token.is_type(REAL_CONST):
            res = self.eat(REAL_CONST)
            return Constant(float(res[1]), REAL)
        elif self.curr_token.is_type(LPAREN):
            self.eat(LPAREN)
            curr_tree = self.expr()
            self.eat(RPAREN)
            return curr_tree
        elif self.curr_token.is_type(ID):
            return self.variable()
        else:
            raise Exception("Syntax error - invalid operand: ", self.curr_token)

    def variable(self):
        var = self.eat(ID)
        return Variable(var)
       
    def eat(self, type):
        # If the type has a sought-after value, we would want to return it
        if type in (INTEGER_CONST, REAL_CONST, ID):
            if self.curr_token.is_type(type):
                res = (self.curr_token.get_type(), self.curr_token.get_value())
                self.curr_token = self.lexer.get_next_token()
                return res
            raise Exception('Syntax Error: Expected {} type, instead got {}'.format(type, self.curr_token.get_type()))
        else:
            if self.curr_token.is_type(type):
                self.curr_token = self.lexer.get_next_token()
                return
            raise Exception('Syntax Error: Expected {} type, instead got {}'.format(type, self.curr_token.get_type()))

