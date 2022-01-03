from Lexer import Lexer
from Parser import Parser
from Token import *
from Error import RuntimeError

class Interpreter():
    def __init__(self):
        pass 
    
    def interpret(self, input_file_contents):
        parser = Parser(Lexer(input_file_contents))
        ast = parser.get_ast_from_code()
        return self.generic_visit(ast)
        
    def generic_visit(self, ast):
        name_of_visit_func = 'visit_' + type(ast).__name__
        visit_function = getattr(self, name_of_visit_func, self.visit_unknown)
        return visit_function(ast)
    
    def visit_unknown(self, ast):
        raise Exception('Given AST class {} does not exist'.format(type(ast).__name__))
    
    def visit_Root(self, root):
        #print('Visiting root: ', root)
        values_of_children = []
        for child in root.get_children():
            values_of_children.append(str(self.generic_visit(child)))
        return values_of_children
    
    def visit_ArithmeticOperator(self, arithmatic_op):
        #print('Visiting arithmetic op: ', arithmatic_op)
        operator = arithmatic_op.get_operator()
        curr_value = None
        for child in arithmatic_op.get_children():
            child_value = self.generic_visit(child)
            if curr_value == None:
                curr_value = child_value
            elif operator == '+':
                curr_value += child_value
            elif operator == '-':
                curr_value -= child_value
            elif operator == '*':
                curr_value *= child_value
            else:
                if child_value == 0:
                    raise RuntimeError('Runtime Exception: Divide by zero')
                elif isinstance(child_value, int):
                    curr_value = int(curr_value / child_value)
                else:
                    curr_value /= child_value
        return curr_value
    
    def visit_UnaryOperator(self, unary_op):
        #print('Visiting unary op: ', unary_op)
        operator = unary_op.get_operator()
        curr_value = self.generic_visit(unary_op.get_child())
        return -curr_value if operator == '-' else curr_value 

    def visit_NumericConstant(self, num_const):
        if num_const.get_type() == INT_CONST:
            return int(num_const.get_value())
        return float(num_const.get_value())       


