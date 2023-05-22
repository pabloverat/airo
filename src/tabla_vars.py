# tabla_vars.py

import json

class Tabla_Vars:

    def __init__(self) -> None:
        self.vars = {}
        self.vars_range = (1000, 4999)
        
        self.temps = {}
        self.temps_range = (5000, 9999)


    def add_temp(self, temp_type: int) -> str:
        """
        temp types:
        1 - bool    2 - char    3 - int
        4 - float   5 - frame
        """

        # possible virtual address for temp
        temp_address = self.temps_range[0] + len(self.temps)
        temp_name = "t" + str(len(self.temps))

        # is the address out of range?
        if temp_address > self.temps_range[1]:
            raise Exception("out of slots for temps")
        
        # is the variable's name already used?
        if temp_name in self.temps.keys():
            raise Exception(f"temp {temp_name} already exists")
        
        # add variable to vars var_table
        self.temps[temp_name] = {'tipo': temp_type, 'address': temp_address}
        
        return temp_name


    def add_var(self, var_name: str, var_type: int) -> None:
        """
        var types:
        1 - bool    2 - char    3 - int
        4 - float   5 - frame
        """
        
        # possible virtual address for variable
        var_address = self.vars_range[0] + len(self.vars)
        
        # is the address out of range?
        if var_address > self.vars_range[1]:
            raise Exception("out of slots for vars")
        
        # is the variable's name already used?
        if var_name in self.vars.keys():
            raise Exception(f"variable {var_name} already exists")
        
        # add variable to vars var_table
        self.vars[var_name] = {'tipo': var_type, 'address':var_address}

        
    def remove_var(self, var_name: str) -> None:
        if var_name in self.vars:
            self.vars.pop(var_name)
        else:
            raise Exception("not valid param for var_scope")


    def calculate_resources(self) -> int:
        return [val['tipo'] for val in self.vars.values()] + [temp['tipo'] for temp in self.temps.values()]

    def get_var_type(self, var_name: str) -> int:
        return self.vars[var_name]['tipo']


    def print_vars(self) -> None:
        pretty_vars = json.dumps(self.vars, indent=4, sort_keys=False)
        pretty_temps = json.dumps(self.temps, indent=4, sort_keys=False)
        print("vars: ", pretty_vars)
        print("temps: ", pretty_temps)
        # print("vars", self.vars)
        # print("temps", self.temps)