# utils.py

def get_resources_from_dir_func(dir_funcs, func_type=None, func_name=None):
    if func_type:
        return list({k:v for k,v in dir_funcs.items() if v['func_type']==func_type}.values())[0]['recursos']
    if func_name:
        return dir_funcs[func_name]['recursos']
    
def get_param_address_from_dir_func(dir_funcs, func_name=None, k=None):
    try:
        return dir_funcs[func_name]['params_addresses'][k]
    except:
        raise Exception(f"failed when attempting to get param address of func {func_name}")

ENCODE = {
    # data types
    'programa': -1,
    'void': 0,
    'bool': 1,
    'char': 2,
    'int': 3,
    'float': 4,
    'frame': 5,
    'string': 6,
    
    # arithmetic operators
    '+': 10,
    '-': 11,
    '*': 12,
    '/': 13,
    
    # # boolean operators
    # 'AND': 20,
    # 'OR': 21,
    # 'NOT': 22,
    
    # relational operators
    '==': 30,
    '!=': 31,
    '>': 32,
    '>=': 33,
    '<': 34,
    '<=': 35,
    
    # jumping operators
    'GOTO': 40,
    'GOTOF': 41,
    'GOTOV': 42,
    
    # modules operators
    'GOSUB': 50,
    'ERA': 51,
    'PARAM': 52,
    'ENDFUNC': 53,
    
    # I/O operators
    'ASSIGN': 60,
    'PRINT': 61,
    'READ': 62
}


DECODE = {
    # data types
    -1: 'programa',
    0: 'void',
    1: 'bool',
    2: 'char',
    3: 'int',
    4: 'float',
    5: 'frame',
    
    # arithmetic operators
    10: '+',
    11: '-',
    12: '*',
    13: '/',
    
    # relational operators
    30: '==',
    31: '!=',
    32: '>',
    33: '>=',
    34: '<',
    35: '<=',
    
    # jumping operators
    40: 'GOTO',
    41: 'GOTOF',
    42: 'GOTOV',
    
    # modules operators
    50: 'GOSUB',
    51: 'ERA',
    52: 'PARAM',
    53: 'ENDFUNC',
    
    # I/O operators
    60: 'ASSIGN',
    61: 'PRINT',
    62: 'READ',
}