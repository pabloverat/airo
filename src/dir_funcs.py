# dir_funcs.py

import json
from tabla_vars import Tabla_Vars

class Dir_Funcs:
    
    def __init__(self) -> None:
        self.funcs = {}


    def add_func(self, func_name: str, func_type: int, dir_inicio: int, recursos: int = None, params: list = [], vars: Tabla_Vars = None) -> None:
        """
        func types:
        -1 -> programa
        0 -> void    1 -> bool    2 -> char
        3 -> int     4 -> float   5 -> frame
        """

        # is the function's name already used?
        if func_name in self.funcs.keys():
            raise Exception(f"func {func_name} already exists")

        # adding func to funcDir    
        self.funcs[func_name] = {'func_type': func_type, 'dir_inicio': dir_inicio, 'recursos': recursos, 'params': params, 'vars': vars}


    def get_func_type(self, func_name: str) -> int:
        return self.funcs[func_name]['func_type']


    def get_func_resources(self, func_name: str) -> list:
        return self.funcs[func_name]['recursos']


    def print_funcs(self) -> None:
        for func in self.funcs.items():
            temp_dict = func[1].copy()
            temp_dict.pop("vars")
            pretty = json.dumps(temp_dict, indent=4, sort_keys=False)
            print(func[0]) # function name
            print(pretty) # function atributes
            func[1]['vars'].print_vars() # function variables
            print()