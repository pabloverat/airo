# tabla_consts.py

import json
from cubo import ENCODE

class Tabla_Consts:
    
    def __init__(self) -> None:
        self.consts = {}
        self.consts_range = {
            # ENCODE["bool"]:  (21_000, 21_999),
            # ENCODE["char"]:  (22_000, 22_999),
            ENCODE["int"]:   (23_000, 24_999),
            ENCODE["float"]: (24_000, 24_999),
            ENCODE["string"]: (25_000, 29_999),
        }
        self.consts_counts = {
            # ENCODE["bool"]:  0,
            # ENCODE["char"]:  0,
            ENCODE["int"]:   0,
            ENCODE["float"]: 0,
            ENCODE["string"]: 0,
        }
        
    def add_const(self, const: int|float|str, type: int) -> int:
        
        # is the variable's name already used?
        if const in self.consts.keys():
            # print(f"const {const} already in table")
            return self.consts[const]
        
        # possible virtual address for const
        const_address = self.consts_range[type][0] + self.consts_counts[type]

        # is the address out of range?
        if const_address > self.consts_range[type][1]:
            raise Exception(f"outOfSlots: for consts of type {type}")
        
        # add const to const_table
        self.consts[const] = const_address
        self.consts_counts[type] += 1
        
        return const_address
    
        
    def print(self) -> None:
        pretty_consts = json.dumps(self.consts, indent=4, sort_keys=False)
        print(pretty_consts, "\n")


    def get_ovejota_str(self) -> str:
        pretty_consts = json.dumps(self.consts)
        return pretty_consts