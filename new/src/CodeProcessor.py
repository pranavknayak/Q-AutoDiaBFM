import ast

class CodeProcessor():
    def __init__(self, buggy, patched):
        self._buggy = str(buggy) 
        self._patched = str(patched)
        self._buggy_ast = (ast.parse(buggy))
        self._patched_ast = (ast.parse(patched))
    
    def get_buggy(self):
        return self._buggy
    
    def get_patched(self):
        return self._patched

    def set_buggy(self, buggy):
        self._buggy = buggy
    
    def set_patched(self, patched):
        self._patched = patched

    def get_buggy_ast(self):
        return self._buggy_ast
    
    def get_patched_ast(self):
        return self._patched_ast        
