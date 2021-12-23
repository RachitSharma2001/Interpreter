from Token import Token
from Token import INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN
from Token import BEGIN, END, DOT, ID, ASSIGN, SEMI
from Ast import Regular, Compound, Assign, Variable 
from Ast import REGULAR_NODE, COMPOUND_NODE, ASSIGN_NODE, VARIABLE_NODE
class Interpreter(object):
    def __init__(self, command):
        self.command = command
        self.pos = 0

    def run(self):
        self.curr_token = self.get_next_token()
        '''while self.curr_token != None:
            print(self.curr_token)
            self.curr_token = self.get_next_token()'''
        if self.curr_token == None:
            raise Exception("Syntax error - requirement of at least one token")
        parsed_ast = self.program()
        print(parsed_ast.post_order())
        return self.interpret(parsed_ast)
    
    # Functions for the lexer  
    ''' Returns the next token ''' 
    def get_next_token(self):
        self.skip_whitespace()
        if self.at_end():
            return None 
        token = self.command[self.pos]
        if token in ('+', '-', '*', '/', '(', ')', ';', '.'):
            self.pos += 1
            return Token(token)
        elif token.isdigit():
            self.pos += 1
            while not self.at_end():
                next_token = self.command[self.pos]
                if not next_token.isdigit():
                    break
                token += next_token
                self.pos += 1
            return Token(token)
        elif self.pos < len(self.command) - 1 and self.command[self.pos:self.pos+2] == ':=':
            self.pos += 2
            return Token(':=')
        elif token.isalnum():
            self.pos += 1
            while not self.at_end():
                curr_char = self.command[self.pos]
                if (token == 'Begin' and curr_char == ' '):
                    break 
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
        if type == INTEGER or type == ID:
            if self.curr_token.is_type(type):
                res = (self.curr_token.get_type(), self.curr_token.get_value())
                self.curr_token = self.get_next_token()
                return res
            raise Exception('Syntax Error: Expected {} type, instead got {}'.format(type, self.curr_token.get_type()))
        elif type in (PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, DOT, ASSIGN, BEGIN, SEMI, END):
            if self.curr_token.is_type(type):
                self.curr_token = self.get_next_token()
                return
            raise Exception('Syntax Error: Expected {} type, instead got {}'.format(type, self.curr_token.get_type()))
        else:
            raise Exception('Invalid type: ', type)

    # Functions for the parser 
    def program(self):
        tree = self.compound_statement()
        self.eat(DOT)
        return tree
    
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
                curr_tree = Regular(curr_tree, '+', right_child)
            elif self.curr_token.is_type(MINUS):
                self.eat(MINUS)
                right_child = self.term()
                curr_tree = Regular(curr_tree, '-', right_child)
            else:
                break
        return curr_tree 
    
    def term(self):
        curr_tree = self.factor()
        while not self.at_end():
            if self.curr_token.is_type(MUL):
                self.eat(MUL)
                right_child = self.factor()
                curr_tree = Regular(curr_tree, '*', right_child)
            elif self.curr_token.is_type(DIV):
                self.eat(DIV)
                right_child = self.factor()
                curr_tree = Regular(curr_tree, '/', right_child)
            else:
                break
        return curr_tree

    def factor(self):
        if self.curr_token.is_type(PLUS):
            self.eat(PLUS)
            return Regular(self.factor(), 'u+', None)
        elif self.curr_token.is_type(MINUS):
            self.eat(MINUS)
            return Regular(self.factor(), 'u-', None)
        elif self.curr_token.is_type(INTEGER):     
            res = self.eat(INTEGER)
            return Regular(None, res, None)
        elif self.curr_token.is_type(LPAREN):
            self.eat(LPAREN)
            curr_tree = self.expr()
            self.eat(RPAREN)
            return curr_tree
        elif self.curr_token.is_type(ID):
            return self.variable()
        else:
            raise Exception("Syntax error - invalid operand")
    
    def variable(self):
        var = self.eat(ID)
        return Variable(var)

    # Functions for the interpreter
    def interpret(self, ast_tree):
        post_order_list = ast_tree.post_order()
        global_vars = {}
        stack = []
        for child in post_order_list:
            if child in ('+', '-', '*', '/'):
                if child == '+':
                    stack[-2] += stack[-1]
                elif child == '-':
                    stack[-2] -= stack[-1]
                elif child == '*':
                    stack[-2] *= stack[-1]
                else:
                    stack[-2] /= stack[-1]
                stack.pop()
            elif child in ('u+', 'u-'):
                if child == 'u-':
                    stack[-1] *= -1
            elif child == ':=':
                global_vars[stack[-2]] = stack[-1]
                stack.pop()
                stack.pop()
            elif child[0] == 'Id':
                var_name = child[1]
                if var_name in global_vars.keys():
                    stack.append(global_vars[var_name])
                else:
                    stack.append(var_name)
            else:
                stack.append(child[1])
        return global_vars