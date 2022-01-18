from Lexer import Lexer
from Parser import Parser
from Token import *
from Error import SemanticError

class SymbolTable(object):
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent
    
    def add_symbol(self, symbol):
        self.table = symbol.add_to_table(self.table)

    def contains_var(self, var_name):
        if var_name in self.table.keys():
            return True
        elif self.parent != None:
            return self.parent.contains_var(var_name)
        else:
            return False

class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type
    
    def add_to_table(self, given_table):
        given_table[self.name] = self.type
        return given_table

    def get_name(self):
        return self.name 
    
    def get_type(self):
        return self.type 

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

class ProcSymbol(Symbol):
    def __init__(self, name, proc):
        super().__init__(name)
        self.proc = proc
    
    def add_to_table(self, given_table):
        given_table[self.proc.get_proc_name()] = self.proc
        return given_table
    
    def get_proc(self):
        return self.proc

class BuiltInType(Symbol):
    def __init__(self, name):
        super().__init__(name)

class SemanticAnalyzer():
    def __init__(self):
        pass 

    def check_logic_of_ast(self, ast):
        self.curr_scope = SymbolTable()
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
    
    def visit_ProcedureDeclaration(self, proc_decl):
        prev_scope = self.curr_scope
        self.curr_scope = SymbolTable(prev_scope)
        self.add_proc_to_scope(proc_decl)
        self.generic_visit(proc_decl.get_proc_body())
        self.curr_scope = prev_scope
    
    def add_proc_to_scope(self, proc_decl):
        for arg in proc_decl.get_proc_args():
            self.curr_scope.add_symbol(VarSymbol(arg, None))
        self.curr_scope.add_symbol(ProcSymbol(proc_decl.get_proc_name(), proc_decl))

    def visit_ProcedureCall(self, proc_call):
        pass
        # Get the called procedure name
        # check that the procedure actually exists in global scope
        # Get the number of arguments for that procedure 
        # Get the number of parameters passed into the procedure call 
        # If the above two numbers are not equal, throw an error

    def visit_VariableDeclaration(self, var_decl):
        var_name = var_decl.get_var_name()
        var_type = var_decl.get_var_type()
        var_value = var_decl.get_var_value()
        self.generic_visit(var_value)
        if self.curr_scope.contains_var(var_name):
            raise SemanticError('"{}" has already been defined'.format(var_name))
        self.curr_scope.add_symbol(VarSymbol(var_name, var_type))

    def visit_SingleVariable(self, var):
        var_name = var.get_var_name()
        if not self.curr_scope.contains_var(var_name):
            raise SemanticError('"{}" referenced but not defined'.format(var_name))

    def perform_numeric_operation(self, curr_sum, addend, operator):
        return

    def visit_UnaryOperator(self, unary_op):
        self.generic_visit(unary_op.get_child())

    def visit_NumericConstant(self, num_const):
        return 


