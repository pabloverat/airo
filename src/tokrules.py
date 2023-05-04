# tokrules.py

reserved = {
    'AND': 'AND',
    'bool': 'BOOL',
    'char': 'CHAR',
    'else': 'ELSE',
    'FALSE': 'FALSE',
    'float': 'FLOAT',
    'frame': 'FRAME',
    'func': 'FUNC',
    'int': 'INT',
    'load': 'LOAD',
    'main': 'MAIN',
    'not': 'NOT',
    'OR': 'OR',
    'Program': 'PROGRAM',
    'read':'READ',
    'return': 'RETURN',
    'then': 'THEN',
    'TRUE': 'TRUE',
    'var': 'VAR',
    'void': 'VOID',
    'when': 'WHEN',
    'while': 'WHILE',
    'write': 'WRITE'
}

tokens = [
    'ASGNMNT',
    'CLBRACE',
    'CLBRACKET',
    'CLPARENTH',
    'COLON',
    'COMMA',
    'DIVIDE',
    'EQUAL',
    'GREATER',
    'GREATEREQ',
    'LESS',
    'LESSEQ',
    'MINUS',
    'OPBRACE',
    'OPBRACKET',
    'OPPARENTH',
    'PLUS',
    'TIMES',
    'UNEQUAL',
    
    'ID',
    'CONST_FLOAT',
    'CONST_INT',
    'CONST_STRING',
] + list(reserved.values())

t_ASGNMNT 	= r'='
t_CLBRACE 	= r'\}'
t_CLBRACKET 	= r'\]'
t_CLPARENTH 	= r'\)'
t_COLON 		= r':'
t_COMMA 		= r','
t_DIVIDE		= r'/'
t_EQUAL 		= r'=='
# t_FLOAT		= r'\d+\.\d+'
t_GREATER 	= r'>'
t_GREATEREQ 	= r'>='
# t_ID 			= r'[a-zA-Z_][a-zA-Z_0-9]*'
# t_INT			= r'\d+'
t_LESS 		= r'<'
t_LESSEQ 		= r'<='
t_MINUS 		= r'-'
t_OPBRACE 	= r'\{'
t_OPBRACKET 	= r'\['
t_OPPARENTH 	= r'\('
t_PLUS 		= r'\+'
# t_STRING 		= r'"([^"\\]|\\.)*"'
t_TIMES 		= r'\*'
t_UNEQUAL 	= r'!='

def t_CONST_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CONST_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CONST_STRING(t):
    r'"([^"\\]|\\.)*"'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = ' \t'
#t_ignore = ' \t\n\r\f\v'