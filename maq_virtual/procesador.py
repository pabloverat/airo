# procesador.py

from obj_parser import Obj_Parser
from memoria import Memoria
from utils import ENCODE, get_resources_from_dir_func
import operator as opp
from operator import attrgetter

def main():
    
    # PARSING OVEJOTA
    objParser = Obj_Parser(obj_dir="./ovejota.obj")
    cuads, dir_funcs, consts = objParser.parse()
    
    print(dir_funcs)

    # MEMORY STACK
    mem_stack = [("$", "$")] # bottom of the stack (mem, dirRet)
    
    # GLOBAL MEMORY
    global_mem = Memoria()
    global_resources = get_resources_from_dir_func(dir_funcs, func_type=-1)
    global_mem.era(global_resources)
    global_mem.set_base(
        # vars_bool=11_000,
        vars_char=12_000,
        vars_int=13_000,
        vars_float=14_000,
        vars_frame=15_000,
        temps_bool=111_000,
        temps_int=113_000,
        temps_float=114_000,
    )
        
    # CONSTANTS MEMORY
    consts_mem = Memoria()
    consts_mem.set_base(
        vars_int=23_000,
        vars_float=24_000,
        vars_string=25_000,
    )
    consts_mem.fill_from_dict(consts)
        
    # LOCAL MEMORY
    local_mem = Memoria()
    local_mem.set_base(
        vars_bool=1_000,
        vars_char=2_000,
        vars_int=3_000,
        vars_float=4_000,
        vars_frame=5_000,
        temps_bool=101_000,
        temps_int=103_000,
        temps_float=104_000,
    )
    
    
    def try_get_registry(address):
        # print(address)
        try:
            val = consts_mem.get_registry(address=address)
            return val
        except:
            try:
                val = global_mem.get_registry(address=address)
                return val
            except:
                try:
                    val = local_mem.get_registry(address=address)
                    return val
                except:
                    raise Exception("get_registry impossible: address couldn't be resolved")
        
                
    def try_set_registry(value, address):
        try:
            consts_mem.set_registry(value=value, address=address)
        except:
            try:
                global_mem.set_registry(value=value, address=address)
            except:
                try:
                    local_mem.set_registry(value=value, address=address)
                except:
                    raise Exception("set_registry impossible: address couldn't be resolved")
    
    
    def binary_operation(left, right, operator):
        left_val = try_get_registry(left)
        right_val = try_get_registry(right)
        f = attrgetter(operator)(opp)
        result_val = f(left_val, right_val)
        try_set_registry(result_val, result)
    
    ip = 0
    while ip < len(cuads):
        print(cuads[ip])
        _, operation, left, right, result = cuads[ip]
        
        # arithmetic operators
        if operation == ENCODE['+']:
            binary_operation(left=left, right=right, operator='add')
            ip += 1
        
        if operation == ENCODE['-']:
            binary_operation(left=left, right=right, operator='sub')
            ip += 1
        
        if operation == ENCODE['*']:
            binary_operation(left=left, right=right, operator='mul')
            ip += 1
        
        if operation == ENCODE['/']:
            binary_operation(left=left, right=right, operator='truediv')
            ip += 1
        
        
        # relational operators
        if operation == ENCODE['==']:
            binary_operation(left=left, right=right, operator='eq')
            ip += 1
            
        if operation == ENCODE['!=']:
            binary_operation(left=left, right=right, operator='ne')
            ip += 1
            
        if operation == ENCODE['>']:
            binary_operation(left=left, right=right, operator='gt')
            ip += 1
            
        if operation == ENCODE['>=']:
            binary_operation(left=left, right=right, operator='ge')
            ip += 1
            
        if operation == ENCODE['<']:
            binary_operation(left=left, right=right, operator='lt')
            ip += 1
            
        if operation == ENCODE['<=']:
            binary_operation(left=left, right=right, operator='le')
            ip += 1
        

        # jumping operators
        if operation == ENCODE['GOTO']:
            ip = result

        if operation == ENCODE['GOTOF']:
            criteria = try_get_registry(address=left)
            ip = ip+1 if criteria else result

        if operation == ENCODE['GOTOV']:
            criteria = try_get_registry(address=left)
            ip = result if criteria else ip+1


        # modules operators
        if operation == ENCODE['GOSUB']:
            breadcrumb = ip
            ip = result

        if operation == ENCODE['ERA']:
            ip += 1

        if operation == ENCODE['PARAM']:
            ip += 1
        
        if operation == ENCODE['ENDFUNC']:
            ip = breadcrumb+1
        

        # I/O operators
        if operation == ENCODE['ASSIGN']:
            value = try_get_registry(address=left)
            try_set_registry(value=value, address=result)
            ip += 1
        
        if operation == ENCODE['PRINT']:
            value = try_get_registry(address=left)
            print(value)
            ip += 1
        
        if operation == ENCODE['READ']:
            value = float(input())
            try_set_registry(value=value, address=result)
            ip += 1



if __name__ == "__main__":
    main()