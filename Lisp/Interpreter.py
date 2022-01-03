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
        results_of_children = []
        for child in root.get_children():
            results_of_children.append(str(self.generic_visit(child)))
        return results_of_children
    
    def visit_ArithmeticOperator(self, arithmatic_op):
        operator = arithmatic_op.get_operator()
        curr_sum = None
        for child in arithmatic_op.get_children():
            child_value = self.generic_visit(child)
            curr_sum = self.perform_numeric_operation(curr_sum, child_value, operator)
        return curr_sum
    
    def perform_numeric_operation(self, curr_sum, new_value, operator):
        if curr_sum == None:
            return new_value
        elif operator == '+':
            return curr_sum + new_value
        elif operator == '-':
            return curr_sum - new_value
        elif operator == '*':
            return curr_sum * new_value
        elif operator == '/':
            if new_value == 0:
                raise RuntimeError('Runtime Exception: Divide by zero')
            # Check type of value - needed because python division results in float value no matter inputs
            elif isinstance(new_value, int):
                return int(curr_sum / new_value)
            else:
                return curr_sum / new_value

    def visit_UnaryOperator(self, unary_op):
        operator = unary_op.get_operator()
        child_value = self.generic_visit(unary_op.get_child())
        return -child_value if operator == '-' else child_value 

    def visit_NumericConstant(self, num_const):
        # Check and assign type - needed in order to preserve type
        if num_const.get_type() == INT_CONST:
            return int(num_const.get_value())
        return float(num_const.get_value())       


