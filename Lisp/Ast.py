class Ast(object):
    pass

class Root(Ast):
    def __init__(self, children):
        self.children = children
    
    def __repr__(self):
        printable_repr = ""
        for child in self.children:
            printable_repr += child.__repr__()
        return printable_repr

class ArithmeticOperator(Ast):
    def __init__(self, operator, group_of_children):
        self.operator = operator
        self.group_of_children = group_of_children
    
    def __repr__(self):
        printable_repr = "["
        for child in self.group_of_children:
            printable_repr += child.__repr__()
            printable_repr += self.operator
        printable_repr += "]"
        return printable_repr

class UnaryOperator(Ast):
    def __init__(self, operator, child):
        self.operator = operator
        self.child = child 
    
    def __repr__(self):
        printable_repr = "(" + self.operator + self.child.__repr__() + ")"
        return printable_repr

class NumericConstant(Ast):
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        printable_repr = '({}, {})'.format(self.type, self.value)
        return printable_repr