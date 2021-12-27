from Token import *
from Lexer import Lexer
from Parser import Parser
from SymbolInterpreter import SymbolInterpreter
import sys

class Interpreter(object):
    def __init__(self, command):
        self.lexer = Lexer(command)
        self.global_vars = {}
    
    def run(self):
        parser = Parser(self.lexer)
        ast_node = parser.generate_ast()
        # Checks if any errors with symbols
        sym_int = SymbolInterpreter()
        sym_int.interpret(ast_node)
        self.interpret(ast_node)
        return self.global_vars

    def interpret(self, ast_node):
        self.visit_post_order(ast_node)
    
    def visit_post_order(self, ast_node):
        name_of_method = 'visit_post_order_' + type(ast_node).__name__
        visitor = getattr(self, name_of_method, self.error_visit)
        return visitor(ast_node)

    def error_visit(self, ast_node):
        raise Exception('No {} method exists'.format(type(ast_node).__name__))

    def visit_post_order_Constant(self, ast_node):
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
            return self.global_vars[name]
        return name
    
    def visit_post_order_Assign(self, ast_node):
        value = self.visit_post_order(ast_node.get_value())
        var_name = ast_node.get_variable().get_value()
        self.global_vars[var_name] = value 
    
    def visit_post_order_Var_decl(self, ast_node):
        self.global_vars[ast_node.get_name()] = -sys.maxsize
    
    def visit_post_order_Compound(self, ast_node):
        for child in ast_node.get_children():
            self.visit_post_order(child)
    
    # For now, we are not executing the procedure 
    def visit_post_order_Procedure(self, ast_node):
        return

    def visit_post_order_Block(self, ast_node):
        for child in ast_node.get_children():
            self.visit_post_order(child)