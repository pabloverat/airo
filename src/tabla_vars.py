# tabla_vars.py

import json
from collections import Counter
from cubo import ENCODE, DECODE, CUBO

class Tabla_Vars:

    def __init__(self) -> None:
        self.vars = {}
        self.vars_range = {
            # ENCODE["bool"]:  (1_000, 1_999),
            ENCODE["char"]:  (2_000, 2_999),
            ENCODE["int"]:   (3_000, 3_999),
            ENCODE["float"]: (4_000, 4_999),
            ENCODE["frame"]: (5_000, 9_999),
        }
        self.vars_counts = {
            # ENCODE["bool"]:  0,
            ENCODE["char"]:  0,
            ENCODE["int"]:   0,
            ENCODE["float"]: 0,
            ENCODE["frame"]: 0,
        }
        
        self.temps = {}
        self.temps_range = {
            ENCODE["bool"]:    (101_000, 101_999),
            # ENCODE["char"]:  (102_000, 102_999),
            ENCODE["int"]:     (103_000, 103_999),
            ENCODE["float"]:   (104_000, 104_999),
            # ENCODE["frame"]: (105_000, 108_999),
            ENCODE["ptr"]: (109_000, 109_999),
        }
        self.temps_counts = {
            ENCODE["bool"]:  0,
            # ENCODE["char"]:  0,
            ENCODE["int"]:   0,
            ENCODE["float"]: 0,
            # ENCODE["frame"]: 0,
            ENCODE["ptr"]: 0,
        }


    def add_temp(self, temp_type: int) -> str:
        """
        temp types:
        1 - bool    2 - char    3 - int
        4 - float   5 - frame   6 - ptr
        """
        # possible virtual address for temp
        temp_address_temp = self.temps_range[temp_type][0]
        temp_address = temp_address_temp + self.temps_counts[temp_type]
        temp_name = "t" + DECODE[temp_type] + str(self.temps_counts[temp_type])
        # is the address out of range?
        if temp_address > self.temps_range[temp_type][1]:
            raise Exception(f"outOfSlots: for temps of type {DECODE[temp_type]}")
        
        # is the variable's name already used?
        if temp_name in self.temps.keys():
            raise Exception(f"temp {temp_name} already exists")
        
        # add variable to vars var_table
        self.temps[temp_name] = {'tipo': temp_type, 'address': temp_address}
        self.temps_counts[temp_type] += 1
        
        return temp_name, temp_address


    def add_var(self, var_name: str, var_type: int, size: int=1, dims=None) -> None:
        """
        var types:
        1 - bool    2 - char    3 - int
        4 - float   5 - frame   6 - ptr
        """
        
        # possible virtual address for variable
        var_address = self.vars_range[var_type][0] + self.vars_counts[var_type]
        
        # is the address out of range?
        if var_address > self.vars_range[var_type][1]:
            raise Exception(f"outOfSlots: for var of type {var_type}")
        
        # is the variable's name already used?
        if var_name in self.vars.keys():
            raise Exception(f"duplicateVariable: {var_name} already exists")
        
        # for when var is array or matrix
        if dims:
            if not dims.next:
                # arrays
                size = dims.r
            else:
                # matrices
                size = dims.next.r
        else:
            size = 1
            
        # add variable to vars var_table
        self.vars[var_name] = {'tipo': var_type, 'address':var_address, 'dims':dims}
        self.vars_counts[var_type] += size

        
    def remove_var(self, var_name: str) -> None:
        if var_name in self.vars:
            self.vars.pop(var_name)
        else:
            raise Exception("not valid param for var_scope")


    def calculate_resources(self):
        return (self.vars_counts, self.temps_counts)


    def get_var_type(self, var_name: str) -> int:
        return self.vars[var_name]['tipo']


    def print_vars(self) -> None:
        def dims_num(var_content):
            if var_content['dims']:
                dims = 1
                if var_content['dims'].next:
                    dims = 2
                var_content['dims'] = dims
            return var_content
                
        vars = self.vars.copy()
        vars = {name: dims_num(v) for name,v in vars.items()}
        pretty_vars = json.dumps(vars, indent=4, sort_keys=False)
        pretty_temps = json.dumps(self.temps, indent=4, sort_keys=False)
        print("vars: ", pretty_vars)
        print("temps: ", pretty_temps)