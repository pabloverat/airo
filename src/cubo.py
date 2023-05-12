# cubo.py

CONV = {
    # data types
    'programa': -1,
    'void': 0,
    'bool': 1,
    'char': 2,
    'int': 3,
    'float': 4,
    'frame': 5,
    
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
}

CUBO = {
    
    # artihmetic operations
    10: {
        3: {
            3:3, # int + int = int
            4:4  # int + float = float
        },
        4: {
            3:4, # float + int = float
            4:4  # float + float = float
        }
    },
    11: {
        3: {
            3:3, # int - int = int
            4:4  # int - float = float
        },
        4: {
            3:4, # float - int = float
            4:4  # float - float = float
        }
    },
    12: {
        3: {
            3:3, # int * int = int
            4:4  # int * float = float
        },
        4: {
            3:4, # float * int = float
            4:4  # float * float = float
        }
    },
    13: {
        3: {
            3:4, # int / int = float
            4:4  # int / float = float
        },
        4: {
            3:4, # float / int = float
            4:4  # float / float = float
        }
    },
    
    # # boolean operations
    # 20: {
    #     1: {
    #         1:1 # bool AND bool = bool
    #     }
    # },
    # 21: {
    #     1: {
    #         1:1 # bool OR bool = bool
    #     }
    # },
    # 22: {
    #     1: 1 # NOT bool = bool
    # },
    
    # relational operators
    30: {
        3: {
            3: 1, # int == int = bool
            4: 1  # int == float = bool
        },
        4: {
            3: 1, # float == int = bool
            4: 1  # float == float = bool
        }
    },
    31: {
        3: {
            3: 1, # int != int = bool
            4: 1  # int != float = bool
        },
        4: {
            3: 1, # float != int = bool
            4: 1  # float != float = bool
        }
    },
    32: {
        3: {
            3: 1, # int > int = bool
            4: 1  # int > float = bool
        },
        4: {
            3: 1, # float > int = bool
            4: 1  # float > float = bool
        }
    },
    33: {
        3: {
            3: 1, # int >= int = bool
            4: 1  # int >= float = bool
        },
        4: {
            3: 1, # float >= int = bool
            4: 1  # float >= float = bool
        }
    },
    34: {
        3: {
            3: 1, # int < int = bool
            4: 1  # int < float = bool
        },
        4: {
            3: 1, # float < int = bool
            4: 1  # float < float = bool
        }
    },
    35: {
        3: {
            3: 1, # int <= int = bool
            4: 1  # int <= float = bool
        },
        4: {
            3: 1, # float <= int = bool
            4: 1  # float <= float = bool
        }
    }
}