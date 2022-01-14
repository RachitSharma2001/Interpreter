from Lexer import Lexer
from Parser import Parser
from Token import *
from Error import SemanticError

class SymbolTable(object):
    def __init__(self) -> None:
        self.table = {}
    
    def add_var_symbol(self, var_symbol):
        self.table[var_symbol.get_name()] = var_symbol.get_type()

    def contains_var(self, var_name):
        return var_name in self.table.keys()

class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type
    
    def get_name(self):
        return self.name 
    
    def get_type(self):
        return self.type 

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

class BuiltInType(Symbol):
    def __init__(self, name):
        super().__init__(name)

class SemanticAnalyzer():
    def __init__(self):
        pass 

    def check_logic_of_ast(self, ast):
        self.symbol_table = SymbolTable()
        self.generic_visit(ast)
        return
        
    def generic_visit(self, ast):
        name_of_visit_func = 'visit_' + type(ast).__name__
        visit_function = getattr(self, name_of_visit_func, self.visit_unknown)
        return visit_function(ast)
    
    def visit_unknown(self, ast):
        raise Exception('Given AST class {} does not exist'.format(type(ast).__name__))
    
    def visit_Root(self, root):
        for child in root.get_children():
            self.generic_visit(child)
    
    def visit_ArithmeticOperator(self, arithmatic_op):
        for child in arithmatic_op.get_children():
            self.generic_visit(child)
    
    def visit_VariableDeclaration(self, var_decl):
        var_name = var_decl.get_var_name()
        var_type = var_decl.get_var_type()
        var_value = var_decl.get_var_value()
        self.generic_visit(var_value)
        if self.symbol_table.contains_var(var_name):
            raise SemanticError('"{}" has already been defined'.format(var_name))
        self.symbol_table.add_var_symbol(VarSymbol(var_name, var_type))

    def visit_SingleVariable(self, var):
        var_name = var.get_var_name()
        if not self.symbol_table.contains_var(var_name):
            raise SemanticError('"{}" referenced but not defined'.format(var_name))

    def perform_numeric_operation(self, curr_sum, addend, operator):
        return

    def visit_UnaryOperator(self, unary_op):
        self.generic_visit(unary_op.get_child())

    def visit_NumericConstant(self, num_const):
        return 


