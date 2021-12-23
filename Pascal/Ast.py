########################## Defines AST ##########################
class Regular(object):
    def __init__(self, left_child, node, right_child):
        self.left_child = left_child
        self.node = node 
        self.right_child = right_child
    
    def __repr__(self):
        if self.left_child != None:
            print(self.left_child)
        if self.right_child != None:
            print(self.right_child)
        return ' {}'.format(self.node)

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
    
    def post_order(self):
        order = []
        for child in self.children:
            order += child.post_order()
        return order

class Assign(object):
    def __init__(self, var, value):
        self.var = var 
        self.value = value 
    
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
    def __init__(self, var_token):
        self.type = var_token.get_type()
        self.name = var_token.get_value()
    
    def post_order(self):
        return [(self.type, self.name)]