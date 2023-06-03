# memoria.py

import math
import json

class Memoria:
    
    def __init__(self) -> None:
        
        self.values_mapper = {
            "vars_bool"   : [],
            "vars_char"   : [],
            "vars_int"    : [],
            "vars_float"  : [],
            "vars_frame"  : [],
            "vars_string" : [],
            "temps_bool"  : [],
            "temps_int"   : [],
            "temps_float" : [],
        }

        self.base_addresses_mapper = {
            'vars_bool':  0,
            'vars_char':  0,
            'vars_int':   0,
            'vars_float': 0,
            'vars_frame': 0,
            'vars_string': 0,
            'temps_bool':  0,
            'temps_int':   0,
            'temps_float': 0,
        }

    
    def set_base(self,
                    vars_bool=None,
                    vars_char=None,
                    vars_int=None,
                    vars_float=None,
                    vars_frame=None,
                    vars_string=None,
                    temps_bool=None,
                    temps_int=None,
                    temps_float=None,
                ) -> None:
        self.base_addresses_mapper['vars_bool']   = vars_bool   if vars_bool   is not None else self.base_addresses_mapper['vars_bool']
        self.base_addresses_mapper['vars_char']   = vars_char   if vars_char   is not None else self.base_addresses_mapper['vars_char']
        self.base_addresses_mapper['vars_int']    = vars_int    if vars_int    is not None else self.base_addresses_mapper['vars_int']
        self.base_addresses_mapper['vars_float']  = vars_float  if vars_float  is not None else self.base_addresses_mapper['vars_float']
        self.base_addresses_mapper['vars_frame']  = vars_frame  if vars_frame  is not None else self.base_addresses_mapper['vars_frame']
        self.base_addresses_mapper['vars_string'] = vars_string if vars_string is not None else self.base_addresses_mapper['vars_string']
        self.base_addresses_mapper['temps_bool']  = temps_bool  if temps_bool  is not None else self.base_addresses_mapper['temps_bool']
        self.base_addresses_mapper['temps_int']   = temps_int   if temps_int   is not None else self.base_addresses_mapper['temps_int']
        self.base_addresses_mapper['temps_float'] = temps_float if temps_float is not None else self.base_addresses_mapper['temps_float']
    
        
    def find_type_from_address_base(self, address_base) -> str:
        if address_base not in self.base_addresses_mapper.values():
            raise Exception("address not admittable to one of the bases")
            
        mydict = self.base_addresses_mapper
        return list(mydict.keys())[list(mydict.values()).index(address_base)]
            
    
    def get_registry(self, address):
        item_base = math.floor(address/1000)*1000
        type = self.find_type_from_address_base(address_base=item_base)
        cast = getattr(self, type[type.find("_")+1:])
        return cast(self.values_mapper[type][address-item_base])
        
    
    def set_registry(self, value, address) -> None:
        item_base = math.floor(address/1000)*1000
        type = self.find_type_from_address_base(address_base=item_base)
        # print("item_base", item_base)
        self.values_mapper[type].append(None)
        self.values_mapper[type][address-item_base] = value
    
    
    def fill_from_dict(self, mem_dict:dict) -> None:
        for value, address in mem_dict.items():
            self.set_registry(value=value, address=address)
            
            
    def print(self) -> None:
        print(json.dumps(self.values_mapper, indent=4))
        
        
    def int(self, val) -> int:
        return int(val)
    
    def float(self, val) -> float:
        return float(val)
    
    def string(self, val) -> str:
        return str(val)