# utiks.py

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