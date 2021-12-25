from Ast import Compound, Assign, Variable, Var_decl, Block, Constant, BinOp, UnOp
import sys

BEGIN = 'Begin'
END = 'End'
DOT = 'Dot'
ID = 'Id'
ASSIGN = 'Assign'
SEMI = 'Semi'
VAR = 'VAR'
PROGRAM = 'Program'
COMMA = 'Comma'
COLON = 'Colon'
REAL = 'Real'
INTEGER_DIV = 'IntDiv'
FLOAT_DIV = 'FloatDiv'
INTEGER_CONST = 'IntConst'
REAL_CONST = 'RealConst'
INTEGER = 'Integer'
PLUS = 'Plus'
MINUS = 'Minus'
MUL = 'Mul'
LPAREN = '('
RPAREN = ')'

class Token(object):
    def interpret_type(self, lexeme):
        if lexeme == 'BEGIN':
            return BEGIN
        elif lexeme == 'END':
            return END
        elif lexeme == 'PROGRAM':
            return PROGRAM 
        elif lexeme == 'REAL':
            return REAL
        elif lexeme == 'INTEGER':
            return INTEGER
        elif lexeme == 'VAR':
            return VAR
        elif lexeme == ',':
            return COMMA
        elif lexeme == ':':
            return COLON 
        elif lexeme == 'DIV':
            return INTEGER_DIV
        elif lexeme == '.':
            return DOT
        elif lexeme == ':=':
            return ASSIGN 
        elif lexeme == ';':
            return SEMI
        elif lexeme[0].isdigit() and '.' in lexeme:
            return REAL_CONST
        elif lexeme.isdigit():
            return INTEGER_CONST
        elif lexeme == '+':
            return PLUS
        elif lexeme == '-':
            return MINUS
        elif lexeme == '*':
            return MUL
        elif lexeme == '/':
            return FLOAT_DIV
        elif lexeme == '(':
            return LPAREN
        elif lexeme == ')':
            return RPAREN
        # if its none of the above, then likely a variable
        return ID
    
    def __init__(self, lexeme):
        self.curr_token = (self.interpret_type(lexeme), lexeme)
    
    def is_type(self, given_type):
        return self.curr_token[0] == given_type

    def get_value(self):
        if self.curr_token[1].isdigit():
            return int(self.curr_token[1])
        return self.curr_token[1]
    
    def get_type(self):
        return self.curr_token[0]

    def __repr__(self):
        return '({}, {})'.format(self.curr_token[0], self.curr_token[1])

class Interpreter(object):
    def __init__(self, command):
        self.command = command
        self.pos = 0
        self.global_vars = {}

    def run(self):
        self.curr_token = self.get_next_token()
        '''while self.curr_token != None:
            print(self.curr_token)
            self.curr_token = self.get_next_token()'''
        if self.curr_token == None:
            raise Exception("Syntax error - requirement of at least one token")
        parsed_ast = self.program()
        self.interpret(parsed_ast)
        return self.global_vars

    # Functions for the lexer  
    ''' Returns the next token ''' 
    def get_next_token(self):
        self.skip_whitespace()
        if self.at_end():
            return None 
        token = self.command[self.pos]
        if self.pos < len(self.command) - 1 and self.command[self.pos:self.pos+2] == ':=':
            self.pos += 2
            return Token(':=')
        elif token in ('+', '-', '*', '/', '(', ')', ';', '.', ':', ','):
            self.pos += 1
            return Token(token)
        elif token.isdigit():
            self.pos += 1
            while not self.at_end():
                next_token = self.command[self.pos]
                if not next_token.isdigit() and next_token != '.':
                    break
                token += next_token
                self.pos += 1
            return Token(token)
        elif token.isalnum():
            self.pos += 1
            while not self.at_end():
                curr_char = self.command[self.pos]
                if not curr_char.isalnum():
                    break
                token += curr_char
                self.pos += 1
            return Token(token)
        else:
            raise Exception('Invalid Token: ', token)

    ''' Skips over white space '''
    def skip_whitespace(self):
        while not self.at_end() and self.command[self.pos] == ' ':
            self.pos += 1
        return
    
    ''' Determines if at end of code '''
    def at_end(self):
        return self.pos >= len(self.command)
    
    def eat(self, type):
        # If the type has a sought-after value, we would want to return it
        if type in (INTEGER_CONST, REAL_CONST, ID):
            if self.curr_token.is_type(type):
                res = (self.curr_token.get_type(), self.curr_token.get_value())
                self.curr_token = self.get_next_token()
                return res
            raise Exception('Syntax Error: Expected {} type, instead got {}'.format(type, self.curr_token.get_type()))
        else:
            if self.curr_token.is_type(type):
                self.curr_token = self.get_next_token()
                return
            raise Exception('Syntax Error: Expected {} type, instead got {}'.format(type, self.curr_token.get_type()))

    # Functions for the parser 
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
        while not self.at_end():
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
        while not self.at_end():
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
            return Constant(int(res[1]))
        elif self.curr_token.is_type(REAL_CONST):
            res = self.eat(REAL_CONST)
            return Constant(float(res[1]))
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

    # Functions for the interpreter
    def interpret(self, ast_node):
        self.visit_post_order(ast_node)
    
    def visit_post_order(self, ast_node):
        name_of_method = 'visit_post_order_' + type(ast_node).__name__
        visitor = getattr(self, name_of_method, self.error_visit)
        return visitor(ast_node)
    
    def error_visit(self, ast_node):
        raise Exception('No {} method exists'.format(type(ast_node).__name__))

    def visit_post_order_Constant(self, ast_node):
        print(ast_node.get_value())
        return ast_node.get_value()

    def visit_post_order_UnOp(self, ast_node):
        value = self.visit_post_order(ast_node.get_child())
        return (-1 if ast_node.is_negative() else 1) * value
    
    def visit_post_order_BinOp(self, ast_node):
        left_side = self.visit_post_order(ast_node.get_left_child())
        right_side = self.visit_post_order(ast_node.get_right_child())
        op = ast_node.get_operand()
        if op == '+':
            return left_side + right_side 
        elif op == '-':
            return left_side - right_side
        elif op == '*':
            return left_side * right_side 
        elif op == '/':
            return left_side / right_side
        elif op == 'DIV':
            return int(left_side / right_side)
    
    def visit_post_order_Variable(self, ast_node, get_value=True):
        name = ast_node.get_value()
        if get_value:
            if name not in self.global_vars.keys():
                raise Exception('Variable {} referenced but not defined'.format(name))
            return self.global_vars[name]
        return name
    
    def visit_post_order_Assign(self, ast_node):
        value = self.visit_post_order(ast_node.get_value())
        self.global_vars[ast_node.get_variable().get_value()] = value 
    
    def visit_post_order_Var_decl(self, ast_node):
        self.global_vars[ast_node.get_var_name()] = -sys.maxsize
    
    def visit_post_order_Compound(self, ast_node):
        for child in ast_node.get_children():
            self.visit_post_order(child)
    
    def visit_post_order_Block(self, ast_node):
        for child in ast_node.get_children():
            self.visit_post_order(child)