########################## Defines AST ##########################
class Ast(object):
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
            order = self.left_child.post_order()
        if self.right_child != None:
            order.append(self.right_child.post_order())
        order.append(self.node)