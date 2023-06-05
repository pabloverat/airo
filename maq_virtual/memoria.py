# memoria.py

import math
import json
from utils import DECODE

class Memoria:
    
    def __init__(self) -> None:
        
        self.func_name = ""
        self.ret = None
        
        self.values_mapper = {
            # "vars_bool"   : [],
            "vars_char"   : [],
            "vars_int"    : [],
            "vars_float"  : [],
            "vars_frame"  : [],
            "vars_string" : [],
            "temps_bool"  : [],
            "temps_int"   : [],
            "temps_float" : [],
            "temps_ptr" : [],
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
            'temps_ptr':   0,
        }

    def free(self) -> None:
        self.values_mapper = {
            # "vars_bool"   : [],
            "vars_char"   : [],
            "vars_int"    : [],
            "vars_float"  : [],
            "vars_frame"  : [],
            "vars_string" : [],
            "temps_bool"  : [],
            "temps_int"   : [],
            "temps_float" : [],
            "temps_ptr" : [],
        }


    def era(self, resources_tuple) -> None:
        vars_resources, temps_resources = resources_tuple
        # vars
        temp_dict = {str("vars_"+DECODE[int(tipo)]): amount for tipo, amount in vars_resources.items()}
        self.values_mapper.update({k: [None]*amount for k, amount in temp_dict.items()})
        # temps
        # print("vars_resources:", vars_resources)
        # print("temps_resources:", temps_resources)
        temp_dict = {str("temps_"+DECODE[int(k)]): v for k, v in temps_resources.items()}
        self.values_mapper.update({k: [None]*amount for k, amount in temp_dict.items()})

    
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
                    temps_ptr=None,
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
        self.base_addresses_mapper['temps_ptr']   = temps_ptr   if temps_ptr   is not None else self.base_addresses_mapper['temps_ptr']
    
        
    def find_type_from_address_base(self, address_base) -> str:
        if address_base not in self.base_addresses_mapper.values():
            raise Exception(f"address not admittable to one of the bases in func {self.func_name}")
            
        mydict = self.base_addresses_mapper
        return list(mydict.keys())[list(mydict.values()).index(address_base)]
            
    
    def get_registry(self, address, operator=None):
        # print("address:", address)
        address = int(address)
        item_base = math.floor(address/1000)*1000
        type = self.find_type_from_address_base(address_base=item_base)
        if "ptr" not in type:
            cast = getattr(self, type[type.find("_")+1:])
            # print("got here, type:", type)
            value = self.values_mapper[type][address-item_base]
            # print("got here, value:", value)
            # if value is None:
            #     raise Exception("variable referenced before assignment")
            return cast(value)
        else:
            # print("ay ojo se viene un getget de pointer")
            pointed_address = self.values_mapper[type][address-item_base]
            # print("pointed_address:", pointed_address, "pointer_address:", address)
            return self.get_registry(pointed_address)
        
    
    def set_registry(self, value, address, operator=None) -> None:
        address = int(address)
        item_base = math.floor(address/1000)*1000
        type = self.find_type_from_address_base(address_base=item_base)
        if operator == 'assign' and "ptr" in type:
            # print("ay ojo se viene un getset de pointer")
            pointed_address = self.values_mapper[type][address-item_base]
            # print("pointed_address:", pointed_address, "pointer_address:", address)
            self.set_registry(value, pointed_address)
        else:
            self.values_mapper[type].append(None)
            self.values_mapper[type][address-item_base] = value
            
            
        # if "ptr" not in type:
        #     self.values_mapper[type].append(None)
        #     self.values_mapper[type][address-item_base] = value
        # else:
        #     print("ay ojo se viene un set de pointer")
        #     pointed_address = self.values_mapper[type][address-item_base]
        #     print("pointed_address:", pointed_address, "pointer_address:", address)
        #     self.set_registry(value, pointed_address)
            
    
    def fill_from_dict(self, mem_dict:dict) -> None:
        for value, address in mem_dict.items():
            self.set_registry(value=value, address=address)
            
            
    def print(self) -> None:
        print(json.dumps(self.values_mapper, indent=4))
        
        
    def int(self, val) -> int:
        return int(float(val))
    
    def float(self, val) -> float:
        return float(val)
    
    def bool(self, val) -> bool:
        return bool(val)
    
    def string(self, val) -> str:
        return str(val)