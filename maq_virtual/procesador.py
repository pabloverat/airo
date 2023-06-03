# procesador.py

from obj_parser import Obj_Parser
from memoria import Memoria
from utils import ENCODE
import operator as opp
from operator import attrgetter

def main():
    
    # PARSING OVEJOTA
    objParser = Obj_Parser(obj_dir="./ovejota.obj")
    cuads, dir_funcs, consts = objParser.parse()
    # print(cuads, "\n\n", dir_funcs, "\n\n", consts)

    # MEMORY STACK
    mem_stack = [("$", "$")] # bottom of the stack (mem, dirRet)
    
    # GLOBAL MEMORY
    global_mem = Memoria()
    global_mem.set_base(
        vars_bool=11_000,
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
    
    consts_mem.print()
    
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
    
    # for cuad in cuads:
    #     print(cuad)
    # consts_mem.print()
    
    def try_get_registry(address):
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
                    Exception("get_registry impossible: address not found in memory")
        
                
            
        
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
                    Exception("set_registry impossible: address not found in memory")
    
    
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
        
        if operation == ENCODE['-']:
            binary_operation(left=left, right=right, operator='sub')
        
        if operation == ENCODE['*']:
            binary_operation(left=left, right=right, operator='mul')
        
        if operation == ENCODE['/']:
            binary_operation(left=left, right=right, operator='truediv')
        
        # relational operators
        if operation == ENCODE['==']:
            binary_operation(left=left, right=right, operator='eq')
            
        if operation == ENCODE['!=']:
            binary_operation(left=left, right=right, operator='ne')
            
        if operation == ENCODE['>']:
            binary_operation(left=left, right=right, operator='gt')
            
        if operation == ENCODE['>=']:
            binary_operation(left=left, right=right, operator='ge')
            
        if operation == ENCODE['<']:
            binary_operation(left=left, right=right, operator='lt')
            
        if operation == ENCODE['<=']:
            binary_operation(left=left, right=right, operator='le')
        

        # jumping operators
        if operation == ENCODE['GOTO']:
            # ip = result
            pass
        if operation == ENCODE['GOTOF']:
            
            pass
        if operation == ENCODE['GOTOV']:
            pass
        
        
        # modules operators
        if operation == ENCODE['GOSUB']:
            pass
        if operation == ENCODE['ERA']:
            pass
        if operation == ENCODE['PARAM']:
            pass
        if operation == ENCODE['ENDFUNC']:
            pass
        

        # I/O operators
        if operation == ENCODE['ASSIGN']:
            value = try_get_registry(address=left)
            try_set_registry(value=value, address=result)
            pass
        
        if operation == ENCODE['PRINT']:
            value = try_get_registry(address=left)
            print(value)
            pass
        
        if operation == ENCODE['READ']:
            pass
        
        # move instruction pointer
        ip += 1


if __name__ == "__main__":
    main()