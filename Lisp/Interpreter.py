from inspect import stack
from Token import *
from Lexer import Lexer
from Parser import Parser
from SemanticAnalyzer import SemanticAnalyzer
from Error import RuntimeError

class CallStack(object):
    def __init__(self):
        self.top = None
    
    def push(self, given_frame):
        self.top = given_frame
    
    def pop(self):
        if self.top == None:
            raise Exception('Pop called on call Stack with no stack frames')
        self.top = self.top.get_frame_below()

    def peek(self):
        return self.top

    def add_to_top_frame(self, key, value):
        if self.top == None:
            raise Exception('Call Stack is empty')
        self.top.add(key, value)

    def get_from_valid_scope(self, key):
        if self.top == None:
            raise Exception('get_from_valid_scope() called on CallStack with no top frame')
        top_scope_res = self.top.get(key)
        if top_scope_res == None:
            return self._get_from_global_scope(key)
        return top_scope_res
    
    def _get_from_global_scope(self, key):
        return self._get_global_scope().get(key)
    
    def _get_global_scope(self):
        curr_scope = self.top
        while curr_scope.get_frame_below() != None:
            curr_scope = curr_scope.get_frame_below()
        return curr_scope

    def __repr__(self):
        stack_str = '------- Call Stack --------\n'
        curr_frame = self.top
        while curr_frame != None:
            stack_str += curr_frame.__repr__()
            curr_frame = curr_frame.get_below_frame()
        stack_str += '--------------------------'
        return stack_str

class StackFrame(object):
    def __init__(self, frame_name, frame_below):
        self.name = frame_name
        self.frame_below = frame_below
        self.memory = {}
    
    def add(self, key, value):
        self.memory[key] = value
    
    def get(self, key):
        if key in self.memory.keys():
            return self.memory[key]
        return None

    def get_frame_below(self):
        return self.frame_below
    
    def __repr__(self):
        frame_str = '--- {} ---\n'.format(self.name)
        for key in self.memory.keys():
            frame_str += '{} -> {}\n'.format(key, self.memory[key])
        frame_str += '----------\n'
        return frame_str

class Interpreter():
    def __init__(self):
        self.call_stack = CallStack()
    
    def interpret(self, user_code):
        parser = Parser(Lexer(user_code))
        ast = parser.get_ast_from_code()
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.check_logic_of_ast(ast)
        return self.generic_visit(ast)
        
    def generic_visit(self, ast):
        name_of_visit_func = 'visit_' + type(ast).__name__
        visit_function = getattr(self, name_of_visit_func, self.visit_unknown)
        return visit_function(ast)
    
    def visit_unknown(self, ast):
        raise Exception('Given AST class {} does not exist'.format(type(ast).__name__))
    
    def visit_Root(self, root):
        self.call_stack.push(StackFrame('Root', None))
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
            curr_sum = self.perform_numeric_operation(curr_sum, operator, child_value)
        return curr_sum
    
    def perform_numeric_operation(self, curr_sum, operator, addend):
        if curr_sum == None:
            return addend
        elif operator == '+':
            return curr_sum + addend
        elif operator == '-':
            return curr_sum - addend
        elif operator == '*':
            return curr_sum * addend
        elif operator == '/':
            return self.find_division_result(curr_sum, addend)

    def find_division_result(self, curr_sum, addend):
        if addend == 0:
            raise RuntimeError('Cannot divide by zero')
        # Check type of value - needed because python division results in float value no matter inputs
        elif isinstance(addend, int):
            return int(curr_sum / addend)
        else:
            return curr_sum / addend

    def visit_ProcedureDeclaration(self, proc_decl):
        self.call_stack.add_to_top_frame(proc_decl.get_proc_name(), proc_decl)
        return 

    def visit_ProcedureCall(self, proc_call):
        proc_decl_obj = self.call_stack.get_from_valid_scope(proc_call.get_proc_name())
        proc_frame = self.get_new_procedure_frame(proc_call, proc_decl_obj.get_proc_args())
        self.call_stack.push(proc_frame)
        proc_result = self.generic_visit(proc_decl_obj.get_proc_body())
        self.call_stack.pop()
        return proc_result
    
    def get_new_procedure_frame(self, proc_call_obj, expected_proc_args):
        proc_name = proc_call_obj.get_proc_name()
        given_proc_args = proc_call_obj.get_passed_args()
        proc_frame = StackFrame(proc_name, self.call_stack.peek())
        for args_index in range(len(expected_proc_args)):
            exp_arg_name = expected_proc_args[args_index]
            given_arg_value = self.generic_visit(given_proc_args[args_index])
            proc_frame.add(exp_arg_name, given_arg_value)
        return proc_frame
        
    def visit_VariableDeclaration(self, var_decl):
        var_name = var_decl.get_var_name()
        var_value = self.generic_visit(var_decl.get_var_value())
        self.call_stack.add_to_top_frame(var_name, var_value)
        return None

    def visit_SingleVariable(self, var):
        var_name = var.get_var_name()
        return self.call_stack.get_from_valid_scope(var_name)

    def visit_UnaryOperator(self, unary_op):
        operator = unary_op.get_operator()
        child_value = self.generic_visit(unary_op.get_child())
        return -child_value if operator == '-' else child_value 

    def visit_NumericConstant(self, num_const):
        # Check and assign type - needed in order to preserve type
        if num_const.get_type() == INT_CONST:
            return int(num_const.get_value())
        return float(num_const.get_value())       


