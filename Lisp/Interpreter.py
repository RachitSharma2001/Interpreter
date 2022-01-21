from inspect import stack
from Token import *
from Lexer import Lexer
from Parser import Parser
from SemanticAnalyzer import SemanticAnalyzer
from Error import RuntimeError

class CallStack(object):
    def __init__(self):
        self.frame_name = ""
        self.top = None
    
    def push(self, frame_name):
        self.top = StackFrame(frame_name, self.top)
    
    def pop(self):
        if self.top == None:
            raise Exception('Pop called on call Stack with no stack frames')
        self.top = self.top.get_below_frame()

    def add_to_top_frame(self, key, value):
        if self.top == None:
            raise Exception('Call Stack is empty')
        self.top.add(key, value)

    def get_from_top_frame(self, key):
        return self.top.get(key)

    def __repr__(self):
        stack_str = '------- Call Stack --------\n'
        curr_frame = self.top
        while curr_frame != None:
            stack_str += curr_frame.__repr__()
            curr_frame = curr_frame.get_below_frame()
        stack_str += '--------------------------'
        return stack_str

class StackFrame(object):
    def __init__(self, frame_name, below_frame):
        self.name = frame_name
        self.below_frame = below_frame
        self.memory = {}
    
    def add(self, key, value):
        self.memory[key] = value
    
    def get(self, key):
        return self.memory[key]

    def get_below_frame(self):
        return self.below_frame
    
    def __repr__(self):
        frame_str = '--- {} ---\n'.format(self.name)
        for key in self.memory.keys():
            frame_str += '{} -> {}\n'.format(key, self.memory[key])
        frame_str += '----------\n'
        return frame_str

class Interpreter():
    def __init__(self):
        pass 
    
    def interpret(self, user_code):
        parser = Parser(Lexer(user_code))
        ast = parser.get_ast_from_code()
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.check_logic_of_ast(ast)
        self.call_stack = CallStack()
        return self.generic_visit(ast)
        
    def generic_visit(self, ast):
        name_of_visit_func = 'visit_' + type(ast).__name__
        visit_function = getattr(self, name_of_visit_func, self.visit_unknown)
        return visit_function(ast)
    
    def visit_unknown(self, ast):
        raise Exception('Given AST class {} does not exist'.format(type(ast).__name__))
    
    def visit_Root(self, root):
        self.call_stack.push('Root')
        output_of_children = self.get_root_children_output(root.get_children())
        self.call_stack.pop()
        return output_of_children
    
    def get_root_children_output(self, root_children):
        output_of_children = []
        for child in root_children:
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
        self.call_stack.add_to_top_frame(var_name, var_value)
        return None

    def visit_SingleVariable(self, var):
        var_name = var.get_var_name()
        return self.call_stack.get_from_top_frame(var_name)

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


