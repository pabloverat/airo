# tabla_vars.py

import json

class Tabla_Vars:

    def __init__(self) -> None:
        self.globals = {}
        self.globals_range = (1000, 4999)
        self.locals = {}
        self.locals_range = (5000, 9999)


    def add_var(self, var_scope: int, var_name: str, var_type: int) -> None:
        """
        var types:
        1 - bool
        2 - char
        3 - int
        4 - float
        5 - frame
        
        var scopes:
        0 - globals
        1 - locals
        """
        
        # if scope is global:
        if var_scope == 0:
            
            # possible virtual address for global variable
            var_address = self.globals_range[0] + len(self.globals)
            
            # is the address out of range?
            if var_address > self.globals_range[1]:
                print("out of slots for globals")
                exit()
            
            # is the variable's name already used in the global scope?
            if var_name in self.globals.keys():
                print("variable already exists")
                exit()
            
            # add variable to globals var_table
            self.globals[var_name] = {'tipo': var_type, 'address':var_address}
        
        # if scope is local:
        elif var_scope == 1:
            
            # possible virtual address for local variable
            var_address = self.locals_range[0] + len(self.locals)
            
            # is the address out of range?
            if var_address > self.locals_range[1]:
                print("out of slots for locals")
                exit()
            
            # is the variable's name already used in the local scope?
            if var_name in self.locals.keys():
                print("variable already exists")
                exit()
                
            # add variable to locals var_table
            self.locals[var_name] = {'tipo': var_type, 'address':var_address}
            
        else:
            print("not valid param for var_scope")
            exit()

        
    def remove_var(self, var_scope: int, var_name: str) -> None:
        if var_scope == 0:
            self.globals.pop(var_name)
        elif var_scope == 1:
            self.locals.pop(var_name)
        else:
            print("not valid param for var_scope")
            exit()


    def get_var_type(self, var_name: str) -> int:
        return self.vars[var_name]['tipo']


    def print_vars(self) -> None:
        pretty = json.dumps(self.globals, indent=4, sort_keys=False)
        print("globals", pretty)
        pretty = json.dumps(self.locals, indent=4, sort_keys=False)
        print("locals", pretty)