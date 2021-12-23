########################## Defines AST ##########################
COMPOUND_NODE, REGULAR_NODE, ASSIGN_NODE, VARIABLE_NODE = 1, 2, 3, 4
class Regular(object):
    def __init__(self, left_child, node, right_child):
        self.left_child = left_child
        self.node = node 
        self.right_child = right_child
    
    def type(self):
        return REGULAR

    def post_order(self):
        order = []
        if self.left_child != None:
            order += self.left_child.post_order()
        if self.right_child != None:
            order += self.right_child.post_order()
        order.append(self.node)
        return order

class Compound(object):
    def __init__(self, node_list):
        self.children = node_list 
    
    def type(self):
        return COMPOUND

    def post_order(self):
        order = []
        for child in self.children:
            order += child.post_order()
        return order

class Assign(object):
    def __init__(self, var, value):
        self.var = var 
        self.value = value 
    
    def type(self):
        return ASSIGN

    def post_order(self):
        order = []
        order += self.var.post_order()
        if self.value.post_order() != None:
            order += self.value.post_order()
        else:
            order.append(self.value)
        order.append(':=')
        return order     

class Variable(object):
    def __init__(self, var_tuple):
        self.type = var_tuple[0]
        self.name = var_tuple[1]
    
    def type(self):
        return VARIABLE

    def get_type(self):
        return self.type
    
    def get_value(self):
        return self.name

    def post_order(self):
        return [(self.type, self.name)]