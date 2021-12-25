########################## Defines AST ##########################
import sys
class Constant(object):
    def __init__(self, value):
        self.value = value 
    
    def visit_post_order(self, global_vars):
        return self.value

class UnOp(object):
    def __init__(self, child, negative):
        self.child = child 
        self.negative = negative
    
    def visit_post_order(self, global_vars):
        value = self.child.visit_post_order(global_vars)
        return (-1 if self.negative else 1) * value
    
class BinOp(object):
    def __init__(self, left_child, node, right_child):
        self.left_child = left_child
        self.node = node 
        self.right_child = right_child

    def visit_post_order(self, global_vars):
        left_side = self.left_child.visit_post_order(global_vars)
        right_side = self.right_child.visit_post_order(global_vars)
        if self.node == '+':
            return left_side + right_side 
        elif self.node == '-':
            return left_side - right_side
        elif self.node == '*':
            return left_side * right_side 
        elif self.node == '/':
            return left_side / right_side
        elif self.node == 'DIV':
            return int(left_side / right_side)

class Variable(object):
    def __init__(self, var_tuple):
        self.type = var_tuple[0]
        self.name = var_tuple[1]

    def get_type(self):
        return self.type

    def get_value(self):
        return self.name

    def visit_post_order(self, global_vars, get_value=True):
        if get_value:
            if self.name not in global_vars.keys():
                raise Exception('Variable {} referenced but not defined'.format(self.name))
            return global_vars[self.name]
        return self.name

class Assign(object):
    def __init__(self, var, value):
        self.var = var 
        self.value = value 

    def visit_post_order(self, global_vars):
        value = self.value.visit_post_order(global_vars)
        global_vars[self.var.get_value()] = value 
        return global_vars

class Var_decl(object):
    def __init__(self, var_name, var_type):
        self.var_name = var_name 
        self.var_type = var_type

    def visit_post_order(self, global_vars):
        global_vars[self.var_name] = -sys.maxsize
        return global_vars

class Compound(object):
    def __init__(self, node_list):
        self.children = node_list 

    def visit_post_order(self, global_vars):
        for child in self.children:
            global_vars = child.visit_post_order(global_vars)
        return global_vars

class Block(object):
    def __init__(self, var_tree_list, compound_tree):
        self.children = var_tree_list + [compound_tree]
    
    def visit_post_order(self, global_vars):
        for child in self.children:
            global_vars = child.visit_post_order(global_vars)
        return global_vars