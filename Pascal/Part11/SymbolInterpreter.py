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

class SymbolTable(object):
    def __init__(self):
        self.table = {}
    
    def define(self, symbol_name, symbol):
        self.table[symbol_name] = symbol 
    
    def lookup(self, symbol_name):
        if symbol_name in self.table.keys():
            return self.table[symbol_name]
        return None
    
    def __repr__(self):
        str = "-----------------"
        for key in self.table.keys():
            str += "{} : {}".format(key, self.table[key])
        str += "-----------------"
        return str

class SymbolInterpreter():
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.define_builtin_types()
    
    def define_builtin_types(self):
        self.symbol_table.define(INTEGER, BuiltInSymbol(INTEGER))
        self.symbol_table.define(REAL, BuiltInSymbol(REAL))

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
        if self.symbol_table.lookup(name) == None:
            raise Exception("Variable {} referenced but not defined".format(name))
        return
    
    def visit_post_order_Assign(self, ast_node):
        self.visit_post_order(ast_node.get_value())
        var_name = ast_node.get_variable().get_value()
        if self.symbol_table.lookup(var_name) == None:
            raise Exception('Variable {} referenced but not defined'.format(var_name))
    
    def visit_post_order_Var_decl(self, ast_node):
        name = ast_node.get_name()
        type = ast_node.get_type()
        if self.symbol_table.lookup(type) == None:
            raise Exception('{} is not a valid type'.format(type))
        self.symbol_table.define(name, VarSymbol(name, type))
        return
    
    def visit_post_order_Compound(self, ast_node):
        for child in ast_node.get_children():
            self.visit_post_order(child)
    
    def visit_post_order_Block(self, ast_node):
        for child in ast_node.get_children():
            self.visit_post_order(child)