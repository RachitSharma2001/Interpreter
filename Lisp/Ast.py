class Ast(object):
    pass

class Root(Ast):
    def __init__(self, group_of_children):
        self.group_of_children = group_of_children
    
    def get_children(self):
        return self.group_of_children

    def __repr__(self):
        printable_repr = ""
        for child in self.group_of_children:
            printable_repr += child.__repr__()
        return printable_repr

class ArithmeticOperator(Ast):
    def __init__(self, operator, group_of_children):
        self.operator = operator
        self.group_of_children = group_of_children
    
    def get_operator(self):
        return self.operator
    
    def get_children(self):
        return self.group_of_children

    def __repr__(self):
        printable_repr = ""
        for child in self.group_of_children:
            printable_repr += child.__repr__()
        printable_repr += self.operator + ", "
        return printable_repr

class UnaryOperator(Ast):
    def __init__(self, operator, child):
        self.operator = operator
        self.child = child 
    
    def get_operator(self):
        return self.operator
    
    def get_child(self):
        return self.child

    def __repr__(self):
        printable_repr = '{}UnOp({}), '.format(self.child.__repr__(), self.operator)
        return printable_repr

class NumericConstant(Ast):
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def get_value(self):
        return self.value

    def get_type(self):
        return self.type

    def __repr__(self):
        printable_repr = str(self.value) + ", "
        return printable_repr