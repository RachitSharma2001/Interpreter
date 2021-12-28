from Token import INTEGER, REAL

class Symbol(object):
    def __init__(self, name, type = None):
        self.name = name 
        self.type = type

    def get_name(self):
        return name

    def get_type(self):
        return type 
    
class BuiltInSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __repr__(self):
        return "<{}:BuiltInSymbol>".format(self.name)

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type=type)
    
    def __repr__(self):
        return "<{}:{}>".format(self.name, self.type)

class ProcSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)
    
    def __repr__(self):
        return "<{}:ProcSymbol>".format(self.name)

class ScopedSymbolTable(object):
    def __init__(self, parent_scoped_table=None):
        self.parent_scoped_table = parent_scoped_table
        self.curr_scoped_table = {}
    
    def define(self, symbol_name, symbol):
        self.curr_scoped_table[symbol_name] = symbol 
    
    # Function to check if symbol is in current or enclosing scope
    def full_lookup(self, symbol_name):
        if symbol_name in self.curr_scoped_table.keys():
            return self.curr_scoped_table[symbol_name]
        elif self.parent_scoped_table != None:
            return self.parent_scoped_table.lookup(symbol_name)
        return None

    # Function to check if symbol is in the current scope
    def lookup(self, symbol_name):
        if symbol_name in self.curr_scoped_table.keys():
            return self.curr_scoped_table[symbol_name]
        return None

    def __repr__(self):
        str = "-----------------"
        for key in self.curr_scoped_table.keys():
            str += "{} : {}".format(key, self.curr_scoped_table[key])
        str += "-----------------"
        return str

class SemanticAnalyzer():
    def __init__(self):
        self.init_sym_table()
    
    def init_sym_table(self, parent_scope=None):
        self.curr_scope = ScopedSymbolTable(parent_scope)
        self.define_builtin_types()
    
    def define_builtin_types(self):
        self.curr_scope.define(INTEGER, BuiltInSymbol(INTEGER))
        self.curr_scope.define(REAL, BuiltInSymbol(REAL))
    
    def interpret(self, ast_node):
        self.visit_post_order(ast_node)
    
    def visit_post_order(self, ast_node):
        name_of_method = 'visit_post_order_' + type(ast_node).__name__
        visitor = getattr(self, name_of_method, self.error_visit)
        return visitor(ast_node)
    
    def error_visit(self, ast_node):
        raise Exception('No {} method exists'.format(type(ast_node).__name__))

    def visit_post_order_Constant(self, ast_node):
        return

    def visit_post_order_UnOp(self, ast_node):
        self.visit_post_order(ast_node.get_child())
        return
    
    def visit_post_order_BinOp(self, ast_node):
        self.visit_post_order(ast_node.get_left_child())
        self.visit_post_order(ast_node.get_right_child())
        return 
    
    def visit_post_order_Variable(self, ast_node, get_value=True):
        name = ast_node.get_value()
        if self.curr_scope.full_lookup(name) == None:
            raise Exception("Variable {} referenced but not defined".format(name))
        return
    
    def visit_post_order_Assign(self, ast_node):
        self.visit_post_order(ast_node.get_value())
        var_name = ast_node.get_variable().get_value()
        if self.curr_scope.full_lookup(var_name) == None:
            raise Exception('Variable {} referenced but not defined'.format(var_name))
        return
    
    def visit_post_order_Var_decl(self, ast_node):
        name = ast_node.get_name()
        type = ast_node.get_type()
        if self.curr_scope.lookup(type) == None:
            raise Exception('{} is not a valid type'.format(type))
        if self.curr_scope.lookup(name) != None:
            raise Exception('{} already defined'.format(name))
        self.curr_scope.define(name, VarSymbol(name, type))
        return
    
    def visit_post_order_Compound(self, ast_node):
        for child in ast_node.get_children():
            self.visit_post_order(child)
        return
    
    def visit_post_order_Proc_decl(self, ast_node):
        proc_name = ast_node.get_proc_name()
        self.curr_scope.define(proc_name, ProcSymbol(proc_name))
        # Save current scoped symbol table
        saved_sym_table = self.curr_scope
        # Reinitialize scoped symbol table
        self.init_sym_table(self.curr_scope)
        # Add parameters to current scoped symbol table
        params = ast_node.get_params()
        for param in params:
            param_name = param.get_name()
            if self.curr_scope.lookup(param_name) != None:
                raise Exception('{} already defined'.format(param_name))
            self.curr_scope.define(param_name, VarSymbol(param_name, param.get_type()))
        self.visit_post_order(ast_node.get_body())  
        self.curr_scope = saved_sym_table
        return

    def visit_post_order_Block(self, ast_node):
        for child in ast_node.get_children():
            self.visit_post_order(child)