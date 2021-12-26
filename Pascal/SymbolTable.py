class SymbolTable(object):
    def __init__(self):
        self.table = {}
    
    def define(self, symbol_name, symbol):
        self.table[symbol_name] = symbol 
    
    def lookup(self, symbol_name):
        if symbol_name in self.table.keys():
            return self.table[symbol_name]
        return None
    
    def __repr__(self):
        str = "-----------------"
        for key in self.table.keys():
            str += "{} : {}".format(key, self.table[key])
        str += "-----------------"
        return str