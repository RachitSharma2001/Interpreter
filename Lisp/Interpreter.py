from Token import *
from Lexer import Lexer
from Parser import Parser
from SemanticAnalyzer import SemanticAnalyzer
from Error import RuntimeError

class Interpreter():
    def __init__(self):
        pass 
    
    def interpret(self, user_code):
        parser = Parser(Lexer(user_code))
        ast = parser.get_ast_from_code()
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.check_logic_of_ast(ast)
        self.global_memory = {}
        return self.generic_visit(ast)
        
    def generic_visit(self, ast):
        name_of_visit_func = 'visit_' + type(ast).__name__
        visit_function = getattr(self, name_of_visit_func, self.visit_unknown)
        return visit_function(ast)
    
    def visit_unknown(self, ast):
        raise Exception('Given AST class {} does not exist'.format(type(ast).__name__))
    
    def visit_Root(self, root):
        output_of_children = []
        for child in root.get_children():
            visit_value = self.generic_visit(child)
            if not visit_value == None:
                output_of_children.append(str(visit_value))
        return output_of_children
    
    def visit_ArithmeticOperator(self, arithmatic_op):
        operator = arithmatic_op.get_operator()
        curr_sum = None
        for child in arithmatic_op.get_children():
            child_value = self.generic_visit(child)
            curr_sum = self.perform_numeric_operation(curr_sum, child_value, operator)
        return curr_sum
    
    def visit_ProcedureDeclaration(self, proc_decl):
        return 

    def visit_ProcedureCall(self, proc_call):
        return
    
    def visit_VariableDeclaration(self, var_decl):
        var_name = var_decl.get_var_name()
        var_value = self.generic_visit(var_decl.get_var_value())
        self.global_memory[var_name] = var_value
        return None

    def visit_SingleVariable(self, var):
        var_name = var.get_var_name()
        return self.global_memory[var_name]

    def perform_numeric_operation(self, curr_sum, addend, operator):
        if curr_sum == None:
            return addend
        elif operator == '+':
            return curr_sum + addend
        elif operator == '-':
            return curr_sum - addend
        elif operator == '*':
            return curr_sum * addend
        elif operator == '/':
            if addend == 0:
                raise RuntimeError('Cannot divide by zero')
            # Check type of value - needed because python division results in float value no matter inputs
            elif isinstance(addend, int):
                return int(curr_sum / addend)
            else:
                return curr_sum / addend

    def visit_UnaryOperator(self, unary_op):
        operator = unary_op.get_operator()
        child_value = self.generic_visit(unary_op.get_child())
        return -child_value if operator == '-' else child_value 

    def visit_NumericConstant(self, num_const):
        # Check and assign type - needed in order to preserve type
        if num_const.get_type() == INT_CONST:
            return int(num_const.get_value())
        return float(num_const.get_value())       


