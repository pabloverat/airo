# tabla_consts.py

import json

class Tabla_Consts:
    
    def __init__(self) -> None:
        self.consts = {}
        self.consts_range = (0, 999)
        
    def add_const(self, const: int|float|str, type: int) -> None:
        
        # is the variable's name already used?
        if const in self.consts.keys():
            print(f"const {const} already in table")
            return
        
        # possible virtual address for const
        const_address = self.consts_range[0] + len(self.consts)

        # is the address out of range?
        if const_address > self.consts_range[1]:
            raise Exception("out of slots for consts")
        
        # add const to const_table
        self.consts[const] = (const_address, type)
        
    def print(self) -> None:
        pretty_consts = json.dumps(self.consts, indent=4, sort_keys=False)
        print("consts: ", pretty_consts, "\n")