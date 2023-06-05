# procesador.py

from obj_parser import Obj_Parser
from memoria import Memoria
from utils import ENCODE, get_resources_from_dir_func, get_param_address_from_dir_func, get_return_address_from_dir_func
from memory_bases import global_mem_bases, local_mem_bases, consts_mem_bases
import operator as opp
from operator import attrgetter
import json

def main():
    
    # PARSING OVEJOTA
    objParser = Obj_Parser(obj_dir="./ovejota.obj")
    cuads, dir_funcs, consts = objParser.parse()
    
    # print(consts)
    # print(json.dumps(dir_funcs, indent=4))
    
    # MEMORY STACK FOR CALL FUNCTIONS
    mem_stack = ["$"] # bottom of the stack
    current_context = [] # None
    passing_params = False
        
    # CONSTANTS MEMORY
    consts_mem = Memoria()
    consts_mem.set_base(**consts_mem_bases)
    consts_mem.fill_from_dict(consts)
    consts_mem.func_name = "consts"
    
    
    def try_get_registry(address, depth_in_stack=1, operator=None):
        try:
            # print("trying in consts")
            val = consts_mem.get_registry(address=address, operator=operator)
            return val
        except:
            try:
                # print("trying in globals")
                val = mem_stack[1].get_registry(address=address, operator=operator)
                return val
            except:
                try:
                    # print("trying in locals")
                    depth_in_stack = 2 if passing_params and mem_stack[-2].func_name != "Program" else 1
                    val = mem_stack[-depth_in_stack].get_registry(address=address, operator=operator)
                    return val
                except:
                    raise Exception("get_registry impossible: address couldn't be resolved")
        
                
    def try_set_registry(value, address, depth_in_stack=1, operator=None):
        try:
            consts_mem.set_registry(value=value, address=address, operator=operator)
        except:
            try:
                # print(mem_stack[1].print())
                mem_stack[1].set_registry(value=value, address=address, operator=operator)
            except:
                try:
                    depth_in_stack = 2 if passing_params and mem_stack[-2].func_name != "Program" else 1
                    mem_stack[-depth_in_stack].set_registry(value=value, address=address, operator=operator)
                except:
                    raise Exception("set_registry impossible: address couldn't be resolved")
    
    
    def binary_operation(left, right, operator):
        left_val = try_get_registry(left, operator=operator)
        right_val = try_get_registry(right, operator=operator)
        f = attrgetter(operator)(opp)
        result_val = f(left_val, right_val)
        try_set_registry(result_val, result)
    
    
    # RUN VIRTUAL MACHINE
    ip = 0
    while ip < len(cuads):
        # print(cuads[ip])
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
            passing_params = False
            mem_stack[-1].ret = ip
            ip = result

        if operation == ENCODE['ERA']:
            # print(cuads[ip])
            
            current_context.append(left)
            resources = get_resources_from_dir_func(dir_funcs, func_name=left)
            if left == "Program":
                # GLOBAL MEMORY
                global_mem = Memoria()
                global_mem.set_base(**global_mem_bases)
                global_mem.func_name = "Program"
                global_mem.era(resources)
                mem_stack.append(global_mem)
                
            else:
                # new local memory for context's resources 
                local_mem = Memoria()
                local_mem.set_base(**local_mem_bases)
                local_mem.era(resources)
                local_mem.func_name = current_context[-1]
                
                # stacking memory in case of recursion
                local_mem.ret = ip
                mem_stack.append(local_mem)
                passing_params = True
                
            ip += 1

        if operation == ENCODE['PARAM']:
            arg_address = left
            arg_value = try_get_registry(arg_address)
            k = right
            param_address = get_param_address_from_dir_func(dir_funcs=dir_funcs, func_name=current_context[-1], k=k)
            # suspending passing params just to pass result to new memory
            passing_params=False
            try_set_registry(value=arg_value, address=param_address)
            passing_params=True
            # resuming passsing params in case there are more params
            ip += 1
        
        if operation == ENCODE['ENDFUNC']:
            # free current context and local memory  
            current_context.pop()
            mem_stack[-1].free()
            
            # reobtaining stacked memory for recursion
            old_mem = mem_stack.pop()
            ret = old_mem.ret
            ip = ret + 1
            
        if operation == ENCODE['RETURN']:
            address_to_return = left
            value_to_return = try_get_registry(address=address_to_return)
            address_to_catch = get_return_address_from_dir_func(dir_funcs=dir_funcs, func_name=current_context[-1])
            try_set_registry(value=value_to_return, address=address_to_catch)
            ip += 1
        

        # I/O operators
        if operation == ENCODE['ASSIGN']:
            value = try_get_registry(address=left)
            try_set_registry(value=value, address=result, operator='assign')
            ip += 1
        
        if operation == ENCODE['PRINT']:
            # print("\t", mem_stack[-1].values_mapper)
            value = try_get_registry(address=left)
            print("output:", value)
            ip += 1
        
        if operation == ENCODE['READ']:
            value = float(input("input: "))
            try_set_registry(value=value, address=result)
            ip += 1

        if operation == ENCODE['VERIFY']:
            ip += 1
            pass


if __name__ == "__main__":
    main()