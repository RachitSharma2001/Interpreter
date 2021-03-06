########################## Defines AST ##########################
import sys 

class Ast(object):
    def __init__(self, orig_token=None):
        self.orig_token = orig_token
    
    def get_orig_token(self):
        if self.orig_token == None:
            raise Exception('Error: Ast class does not have orig token')
        return self.orig_token

class Constant(Ast):
    def __init__(self, value, type):
        super().__init__()
        self.value = value 
        self.type = type

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

class UnaryOperator(Ast):
    def __init__(self, child, has_neg_sign):
        super().__init__()
        self.child = child 
        self.has_neg_sign = has_neg_sign
    
    def is_negative(self):
        return self.has_neg_sign
    
    def get_child(self):
        return self.child

class BinaryOperator(Ast):
    def __init__(self, left_child, operand, right_child):
        super().__init__()
        self.left_child = left_child
        self.operand = operand 
        self.right_child = right_child

    def get_left_child(self):
        return self.left_child
    
    def get_right_child(self):
        return self.right_child
    
    def get_operand(self):
        return self.operand

class Variable(Ast):
    def __init__(self, type, name, orig_token):
        super().__init__(orig_token)
        self.type = type
        self.name = name

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name
    
class Assign(Ast):
    def __init__(self, var, value):
        super().__init__()
        self.var = var 
        self.value = value 

    def get_variable(self):
        return self.var

    def get_value(self):
        return self.value

class Var_decl(Ast):
    def __init__(self, var_name, var_type, orig_token):
        super().__init__(orig_token)
        self.var_name = var_name 
        self.var_type = var_type
    
    def get_name(self):
        return self.var_name
    
    def get_type(self):
        return self.var_type

class Param(Ast):
    def __init__(self, param_name, param_type):
        super().__init__()
        self.param_name = param_name
        self.param_type = param_type
    
    def get_name(self):
        return self.param_name 
    
    def get_type(self):
        return self.param_type

class Proc_decl(Ast):
    def __init__(self, name, param_children, body, orig_token):
        super().__init__(orig_token)
        self.name = name
        self.param_children = param_children
        self.body = body
    
    def get_name(self):
        return self.name

    def get_params(self):
        return self.param_children

    def get_body(self):
        return self.body


class Compound(Ast):
    def __init__(self, node_list):
        super().__init__()
        self.children = node_list 

    def get_children(self):
        return self.children

class Block(Ast):
    def __init__(self, dec_tree_list, compound_tree):
        super().__init__()
        self.children = dec_tree_list + [compound_tree]
    
    def get_children(self):
        return self.children
