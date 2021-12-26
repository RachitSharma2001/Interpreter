class Symbol(object):
    def __init__(self, name, type = None):
        self.name = name 
        self.type = type

    def get_name(self):
        return name

    def get_type(self):
        return type 
    
class BuiltInSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __repr__(self):
        return "<{}:BuiltInSymbol>".format(self.name)

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type=type)
    
    def __repr__(self):
        return "<{}:{}>".format(self.name, self.type)