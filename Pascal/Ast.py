########################## Defines AST ##########################
import sys
class Constant(object):
    def __init__(self, value, type):
        self.value = value 
        self.type = type

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

class UnOp(object):
    def __init__(self, child, negative):
        self.child = child 
        self.negative = negative
    
    def is_negative(self):
        return self.negative
    
    def get_child(self):
        return self.child

class BinOp(object):
    def __init__(self, left_child, operand, right_child):
        self.left_child = left_child
        self.operand = operand 
        self.right_child = right_child

    def get_left_child(self):
        return self.left_child
    
    def get_right_child(self):
        return self.right_child
    
    def get_operand(self):
        return self.operand

class Variable(object):
    def __init__(self, var_tuple):
        self.type = var_tuple[0]
        self.name = var_tuple[1]

    def get_type(self):
        return self.type

    def get_value(self):
        return self.name
    
class Assign(object):
    def __init__(self, var, value):
        self.var = var 
        self.value = value 

    def get_variable(self):
        return self.var

    def get_value(self):
        return self.value

class Var_decl(object):
    def __init__(self, var_name, var_type):
        self.var_name = var_name 
        self.var_type = var_type

    def get_name(self):
        return self.var_name
    
    def get_type(self):
        return self.var_type

class Compound(object):
    def __init__(self, node_list):
        self.children = node_list 

    def get_children(self):
        return self.children

class Procedure(object):
    def __init__(self, child):
        self.child = child 
    
    def get_child(self):
        return self.child

class Block(object):
    def __init__(self, dec_tree_list, compound_tree):
        self.children = dec_tree_list + [compound_tree]
    
    def get_children(self):
        return self.children
